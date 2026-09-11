"""BO-B-DATA Part A — authority-label hardening tests (fail-first).

The binding rule: AUTHORITATIVE may only be granted through an explicit,
declared real-data label (`historical:real`). The legacy fixture convention
(`sample:*` / `csv:*` / `test`) must no longer manufacture authority, and an
unlabeled real-data ingest must be quarantined from research-tier snapshots.

Pre-fix expectations (bdata_probe_prefix.log): the classification asserts
fail because the legacy convention still maps to AUTHORITATIVE.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from sqlalchemy import select

from app.db.models.dataset import DatasetQuarantineRecord
from app.db.models.market_metadata import MarketSeriesMetadata
from app.db.session import session_scope
from app.ingestion.service import IngestionService
from app.ml.dataset.chronology_guard import QuarantineReason, SourceAuthority
from app.ml.dataset.market_data_query import authority_from_source
from app.ml.dataset.service import DatasetService, DatasetSnapshotInput
from app.ml.dataset.synthetic_corpus import generate_series, write_corpus_csv


def test_bdata_only_explicit_real_label_is_authoritative() -> None:
    """A2/A4: the explicit real-data label is authoritative; every legacy
    fixture label is non-authoritative."""
    assert authority_from_source("historical:real") is SourceAuthority.AUTHORITATIVE
    assert authority_from_source("sample:eurusd_h1_sample.csv") is SourceAuthority.UNKNOWN
    assert authority_from_source("csv:whatever.csv") is SourceAuthority.UNKNOWN
    assert authority_from_source("test") is SourceAuthority.UNKNOWN
    # B-01 additive labels unchanged:
    assert authority_from_source("synthetic") is SourceAuthority.SYNTHETIC
    assert authority_from_source("seed:synthetic") is SourceAuthority.SYNTHETIC
    assert authority_from_source("live:simulated") is SourceAuthority.SIMULATED


async def test_bdata_unlabeled_ingest_persists_non_authoritative_metadata(
    prepared_db: None,
) -> None:
    """A3: ingesting without an explicit label takes the honest default
    (`csv:{filename}`) and the metadata row records UNKNOWN authority — never
    authoritative."""
    rows = generate_series(market_class="forex", symbol="EURUSD", bars=12)
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "bdata_unlabeled.csv"
        write_corpus_csv(path, rows)
        async with session_scope() as session:
            result = await IngestionService(session).ingest_csv(
                path=path,
                market_class="forex",
                symbol="EURUSD",
                timeframe="H1",
            )
            assert result.rows_inserted == 12
        async with session_scope() as session:
            metadata = (
                await session.execute(
                    select(MarketSeriesMetadata).where(
                        MarketSeriesMetadata.symbol == "EURUSD",
                        MarketSeriesMetadata.timeframe == "H1",
                    )
                )
            ).scalars().all()
            assert metadata, "no metadata row for unlabeled ingest"
            assert metadata[0].source_authority == SourceAuthority.UNKNOWN.value


async def test_bdata_unlabeled_ingest_quarantined_from_research_tier(
    prepared_db: None,
) -> None:
    """A4(c): a research-validation snapshot must refuse data whose label is
    not an explicit real-data declaration — with the UNKNOWN-authority reason,
    not a silent acceptance."""
    from dataclasses import replace

    rows = generate_series(market_class="forex", symbol="GBPUSD", bars=24)
    # The default unlabeled-ingest path stamps rows with `csv:{filename}`;
    # simulate exactly that (no explicit declaration).
    unlabeled = [
        replace(bar, source="csv:bdata_unlabeled_gbp.csv") for bar in rows
    ]
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "bdata_unlabeled_gbp.csv"
        write_corpus_csv(path, rows)
        async with session_scope() as session:
            result = await IngestionService(session).ingest_csv(
                path=path,
                market_class="forex",
                symbol="GBPUSD",
                timeframe="H1",
            )
            assert result.rows_inserted == 24
        async with session_scope() as session:
            svc = DatasetService(session)
            snapshot = await svc.create_draft_snapshot(
                DatasetSnapshotInput(
                    dataset_id="ds-bdata-unlabeled",
                    name="B-DATA unlabeled research-tier attempt",
                    version=1,
                    market="forex",
                    timeframe="H1",
                    start_time=rows[0].open_time,
                    end_time=rows[-1].open_time,
                    source="csv:bdata_unlabeled_gbp.csv",
                    feature_version="feature_set.v1",
                    quality_score="pass",
                    tier="research_validation",
                    created_by="bdata",
                )
            )
            frozen = await svc.freeze_from_candles(
                snapshot=snapshot,
                candles=unlabeled,
                provider="internal",
                as_of_time=rows[-1].open_time,
                ingestion_finished_at=rows[-1].open_time,
            )
            assert frozen.status == "quarantined"
            events = (
                await session.execute(
                    select(DatasetQuarantineRecord).where(
                        DatasetQuarantineRecord.dataset_snapshot_id == frozen.id
                    )
                )
            ).scalars().all()
            reasons = {event.reason_code for event in events}
            assert QuarantineReason.UNKNOWN_SOURCE_AUTHORITY.value in reasons, (
                f"expected UNKNOWN_SOURCE_AUTHORITY quarantine, got {reasons}"
            )
