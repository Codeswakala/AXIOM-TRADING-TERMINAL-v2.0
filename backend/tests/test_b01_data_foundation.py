"""B-01 — Data Foundation: fail-first + invariant tests (BO-B-01).

Pre-fix expectations (recorded in b01_probe_prefix.log):
- synthetic / historical:real source labels are unclassified (UNKNOWN authority);
- DatasetSnapshotInput has no tier concept;
- no split-manifest persistence exists;
- ingestion does not upsert market_series_metadata;
- the validation-tier rule document does not exist.

Post-fix: every test here passes, pinning the B-01 contract.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
from sqlalchemy import func, select

from app.db.models.dataset import (
    DatasetLineageRecord,
    DatasetQuarantineRecord,
    DatasetSeriesMember,
    DatasetSnapshot,
)
from app.db.models.dataset_split import DatasetSplitManifest
from app.db.models.feature import FeatureRecord
from app.db.models.feature_definition import FeatureQualityReport
from app.db.models.market_metadata import MarketSeriesMetadata
from app.db.session import session_scope
from app.ingestion.service import IngestionService
from app.ml.dataset.chronology_guard import QuarantineReason, SourceAuthority
from app.ml.dataset.market_data_query import (
    CandleMarketDataQueryAdapter,
    CanonicalOHLCVRecord,
    MarketSeriesKey,
    authority_from_source,
)
from app.ml.dataset.service import DatasetService, DatasetSnapshotInput
from app.ml.dataset.split_engine import TemporalSplitConfig, TemporalSplitEngine
from app.ml.dataset.split_store import store_manifest
from app.ml.dataset.synthetic_corpus import (
    CORPUS_SERIES_KEYS,
    SyntheticBar,
    generate_series,
    write_corpus_csv,
)
from app.ml.features.store import FeatureStoreService


def _bars(n: int, market_class: str = "forex", symbol: str = "EURUSD") -> list[SyntheticBar]:
    return generate_series(
        market_class=market_class, symbol=symbol, bars=n, timeframe="H1"
    )


def _canonical(bars: list[SyntheticBar], key: MarketSeriesKey) -> list[CanonicalOHLCVRecord]:
    return [
        CanonicalOHLCVRecord(
            series_key=key,
            open_time=bar.open_time,
            open=bar.open,
            high=bar.high,
            low=bar.low,
            close=bar.close,
            volume=bar.volume,
            source=bar.source,
            ingestion_run_id=None,
            authority_classification=authority_from_source(bar.source),
            source_record_id=bar.record_id,
        )
        for bar in bars
    ]


def test_b01_source_label_classification_is_honest() -> None:
    """Additive label contract: synthetic is never authoritative; the explicit
    real label is the only new authoritative path."""
    assert authority_from_source("synthetic") is SourceAuthority.SYNTHETIC
    assert authority_from_source("historical:real") is SourceAuthority.AUTHORITATIVE
    assert authority_from_source("seed:synthetic") is SourceAuthority.SYNTHETIC
    assert authority_from_source("live:simulated") is SourceAuthority.SIMULATED
    assert authority_from_source("no-such-label") is SourceAuthority.UNKNOWN


def test_b01_validation_tier_document_is_present_and_binding() -> None:
    """B-01.1a: the tier rule exists as a documented, referenced artifact and
    enumerates the four governed tiers."""
    doc = (
        Path(__file__).resolve().parents[1] / "docs" / "VALIDATION_TIER_SEPARATION.md"
    )
    assert doc.is_file(), "validation tier separation document missing"
    text = doc.read_text(encoding="utf-8")
    for tier in (
        "pipeline_validation",
        "research_validation",
        "economic_validation",
        "generalization_validation",
    ):
        assert tier in text, f"tier {tier} not enumerated in the rule document"


async def test_b01_unknown_tier_rejected(prepared_db: None) -> None:
    """Tier is validated at snapshot creation; typos fail closed."""
    bars = _bars(3)
    async with session_scope() as session:
        svc = DatasetService(session)
        with pytest.raises(ValueError):
            await svc.create_draft_snapshot(
                DatasetSnapshotInput(
                    dataset_id="ds-b01-x",
                    name="x",
                    version=1,
                    market="forex",
                    timeframe="H1",
                    start_time=bars[0].open_time,
                    end_time=bars[-1].open_time,
                    source="synthetic",
                    feature_version="v1",
                    quality_score="pass",
                    tier="not_a_tier",
                )
            )


async def test_b01_synthetic_corpus_freezes_under_pipeline_validation_tier(
    prepared_db: None,
) -> None:
    """The pipeline-validation tier accepts labeled synthetic data (the corpus
    this unit produces), with labels carried end-to-end in lineage rows."""
    bars = _bars(30)
    async with session_scope() as session:
        svc = DatasetService(session)
        snapshot = await svc.create_draft_snapshot(
            DatasetSnapshotInput(
                dataset_id="ds-b01-forex-pipe",
                name="B01 synthetic forex pipeline-validation snapshot",
                version=1,
                market="forex",
                timeframe="H1",
                start_time=bars[0].open_time,
                end_time=bars[-1].open_time,
                source="synthetic",
                feature_version="feature_set.v1",
                quality_score="pass",
                tier="pipeline_validation",
                created_by="b01",
            )
        )
        assert snapshot.source_policy["tier"] == "pipeline_validation"
        assert snapshot.source_policy["authoritative_only"] is False

        frozen = await svc.freeze_from_candles(
            snapshot=snapshot,
            candles=bars,
            provider="internal",
            as_of_time=bars[-1].open_time,
            ingestion_finished_at=bars[-1].open_time,
        )
        assert frozen.status == "frozen"
        assert frozen.content_hash

        lineage = (
            await session.execute(
                select(func.count()).select_from(DatasetLineageRecord).where(
                    DatasetLineageRecord.dataset_snapshot_id == frozen.id
                )
            )
        ).scalar_one()
        assert lineage == 30, f"expected 30 lineage rows, got {lineage}"
        members = (
            await session.execute(
                select(func.count()).select_from(DatasetSeriesMember).where(
                    DatasetSeriesMember.dataset_snapshot_id == frozen.id
                )
            )
        ).scalar_one()
        assert members >= 1


async def test_b01_synthetic_corpus_quarantined_under_research_tier(
    prepared_db: None,
) -> None:
    """The tier gate works in the STRICT direction: the same synthetic corpus
    must not enter a research-validation snapshot, and the quarantine reason
    must be the synthetic-class rejection (not an unknown-source fallback)."""
    bars = _bars(20)
    async with session_scope() as session:
        svc = DatasetService(session)
        snapshot = await svc.create_draft_snapshot(
            DatasetSnapshotInput(
                dataset_id="ds-b01-forex-research",
                name="B01 synthetic forex research-tier attempt",
                version=1,
                market="forex",
                timeframe="H1",
                start_time=bars[0].open_time,
                end_time=bars[-1].open_time,
                source="synthetic",
                feature_version="feature_set.v1",
                quality_score="pass",
                tier="research_validation",
                created_by="b01",
            )
        )
        frozen = await svc.freeze_from_candles(
            snapshot=snapshot,
            candles=bars,
            provider="internal",
            as_of_time=bars[-1].open_time,
            ingestion_finished_at=bars[-1].open_time,
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
        assert QuarantineReason.SYNTHETIC_SOURCE_NOT_AUTHORITATIVE.value in reasons, (
            f"expected synthetic-class rejection, got {reasons}"
        )


async def test_b01_split_manifest_persisted_with_counts(prepared_db: None) -> None:
    """The temporal split engine's manifest is persisted to
    dataset_split_manifests with train/validation/test counts and hash."""
    bars = _bars(120)
    async with session_scope() as session:
        svc = DatasetService(session)
        snapshot = await svc.create_draft_snapshot(
            DatasetSnapshotInput(
                dataset_id="ds-b01-split",
                name="B01 split manifest snapshot",
                version=1,
                market="forex",
                timeframe="H1",
                start_time=bars[0].open_time,
                end_time=bars[-1].open_time,
                source="synthetic",
                feature_version="feature_set.v1",
                quality_score="pass",
                tier="pipeline_validation",
                created_by="b01",
            )
        )
        await svc.freeze_from_candles(
            snapshot=snapshot,
            candles=bars,
            provider="internal",
            as_of_time=bars[-1].open_time,
            ingestion_finished_at=bars[-1].open_time,
        )
        rows = [
            {"row_id": f"b01-{i}", "as_of": bar.open_time}
            for i, bar in enumerate(bars)
        ]
        config = TemporalSplitConfig(
            split_id="split-b01-forex",
            train_start=bars[0].open_time,
            train_end=bars[39].open_time,
            validation_start=bars[40].open_time,
            validation_end=bars[79].open_time,
            test_start=bars[80].open_time,
            test_end=bars[119].open_time,
            label_horizon_bars=1,
            embargo_bars=1,
        )
        engine = TemporalSplitEngine()
        split_rows = engine.split(rows=rows, config=config)
        manifest = await store_manifest(
            session, snapshot=snapshot, split=split_rows, config=config
        )
        assert manifest.split_hash == split_rows.split_hash
        assert manifest.train_count == 40
        assert manifest.validation_count == 40
        assert manifest.test_count == 40
        stored = (
            await session.execute(
                select(DatasetSplitManifest).where(
                    DatasetSplitManifest.dataset_snapshot_id == snapshot.id
                )
            )
        ).scalars().all()
        assert len(stored) == 1
        assert stored[0].manifest["split_strategy"] == "temporal"


async def test_b01_ingestion_upserts_series_metadata(prepared_db: None) -> None:
    """Every ingested series carries a truthful metadata row with its source
    authority (synthetic corpus → synthetic authority, never authoritative)."""
    rows = _bars(25)
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "b01_eurusd.csv"
        write_corpus_csv(path, rows)
        async with session_scope() as session:
            service = IngestionService(session)
            result = await service.ingest_csv(
                path=path,
                market_class="forex",
                symbol="EURUSD",
                timeframe="H1",
                source="synthetic",
            )
            assert result.status in {"completed", "completed_with_errors"}
            assert result.rows_inserted == 25

        async with session_scope() as session:
            metadata = (
                await session.execute(
                    select(MarketSeriesMetadata).where(
                        MarketSeriesMetadata.market_class == "forex",
                        MarketSeriesMetadata.symbol == "EURUSD",
                        MarketSeriesMetadata.timeframe == "H1",
                    )
                )
            ).scalars().all()
            assert metadata, "no market_series_metadata row after ingestion"
            assert metadata[0].source_authority == SourceAuthority.SYNTHETIC.value


async def test_b01_features_computed_with_quality_report_and_no_identity(
    prepared_db: None,
) -> None:
    """B-01.3: builtin definitions register, features compute over the corpus
    with lineage, a quality report is produced, and the no-symbol-identity
    boundary holds."""
    bars = _bars(60)
    key = CORPUS_SERIES_KEYS[0]
    async with session_scope() as session:
        svc = DatasetService(session)
        snapshot = await svc.create_draft_snapshot(
            DatasetSnapshotInput(
                dataset_id="ds-b01-features",
                name="B01 feature snapshot",
                version=1,
                market=key.market_class,
                timeframe=key.timeframe,
                start_time=bars[0].open_time,
                end_time=bars[-1].open_time,
                source="synthetic",
                feature_version="feature_set.v1",
                quality_score="pass",
                tier="pipeline_validation",
                created_by="b01",
            )
        )
        frozen = await svc.freeze_from_candles(
            snapshot=snapshot,
            candles=bars,
            provider="internal",
            as_of_time=bars[-1].open_time,
            ingestion_finished_at=bars[-1].open_time,
        )

        store = FeatureStoreService(session)
        definitions = await store.register_builtin_definitions()
        assert {d.feature_name for d in definitions} >= {
            "return_1",
            "range_pct",
            "rolling_return_3",
        }

        records = _canonical(bars, key)
        output, report = await store.compute_and_store(
            series_key=key,
            records=records,
            source_dataset_hash=frozen.content_hash,
            tier="pipeline_validation",
        )
        assert len(output) == 60
        assert isinstance(report, FeatureQualityReport)
        assert report.source_dataset_hash == frozen.content_hash
        for row in output:
            assert "symbol" not in row.features
            assert "provider" not in row.features
            assert "market_class" not in row.features

        stored = (
            await session.execute(select(func.count()).select_from(FeatureRecord))
        ).scalar_one()
        assert stored == 60
        reports = (
            await session.execute(
                select(func.count()).select_from(FeatureQualityReport)
            )
        ).scalar_one()
        assert reports >= 1


async def test_b01_full_pipeline_end_to_end(prepared_db: None) -> None:
    """The whole B-01 pipeline in one governed pass: corpus → ingestion →
    metadata → snapshot (pipeline tier) → split manifest → features."""
    corpus = {
        ("forex", "EURUSD"): _bars(60, market_class="forex", symbol="EURUSD"),
        ("crypto", "BTCUSD"): _bars(60, market_class="crypto", symbol="BTCUSD"),
    }
    with tempfile.TemporaryDirectory() as tmp:
        for (market_class, symbol), rows in corpus.items():
            path = Path(tmp) / f"b01_{symbol}.csv"
            write_corpus_csv(path, rows)
            async with session_scope() as session:
                result = await IngestionService(session).ingest_csv(
                    path=path,
                    market_class=market_class,
                    symbol=symbol,
                    timeframe="H1",
                    source="synthetic",
                )
                assert result.rows_inserted == 60

    async with session_scope() as session:
        svc = DatasetService(session)
        adapter = CandleMarketDataQueryAdapter(session, provider="internal")
        series = await adapter.list_series()
        keys = [k for k in series if k.timeframe == "H1"]
        assert len(keys) >= 2, f"expected 2 ingested H1 series, got {keys}"

        store = FeatureStoreService(session)
        await store.register_builtin_definitions()

        for key in keys:
            records = await adapter.get_candles(
                series_key=key, source_filter="synthetic"
            )
            assert len(records) == 60
            snapshot = await svc.create_draft_snapshot(
                DatasetSnapshotInput(
                    dataset_id=f"ds-b01-e2e-{key.symbol.lower()}",
                    name=f"B01 E2E {key.symbol} snapshot",
                    version=1,
                    market=key.market_class,
                    timeframe=key.timeframe,
                    start_time=records[0].open_time,
                    end_time=records[-1].open_time,
                    source="synthetic",
                    feature_version="feature_set.v1",
                    quality_score="pass",
                    tier="pipeline_validation",
                    created_by="b01-e2e",
                )
            )
            frozen = await svc.freeze_from_query(
                snapshot=snapshot,
                query_port=adapter,
                market_class=key.market_class,
                provider=key.provider,
                symbol=key.symbol,
                timeframe=key.timeframe,
                as_of_time=records[-1].open_time,
                ingestion_finished_at=records[-1].open_time,
            )
            assert frozen.status == "frozen"

            row_dicts = [
                {"row_id": r.source_record_id or str(i), "as_of": r.open_time}
                for i, r in enumerate(records)
            ]
            config = TemporalSplitConfig(
                split_id=f"split-e2e-{key.symbol.lower()}",
                train_start=records[0].open_time,
                train_end=records[19].open_time,
                validation_start=records[20].open_time,
                validation_end=records[39].open_time,
                test_start=records[40].open_time,
                test_end=records[59].open_time,
                label_horizon_bars=1,
                embargo_bars=1,
            )
            split_rows = TemporalSplitEngine().split(rows=row_dicts, config=config)
            await store_manifest(
                session, snapshot=frozen, split=split_rows, config=config
            )

            output, _report = await store.compute_and_store(
                series_key=key,
                records=records,
                source_dataset_hash=frozen.content_hash,
                tier="pipeline_validation",
            )
            assert len(output) == 60

        snapshot_count = (
            await session.execute(select(func.count()).select_from(DatasetSnapshot))
        ).scalar_one()
        manifest_count = (
            await session.execute(
                select(func.count()).select_from(DatasetSplitManifest)
            )
        ).scalar_one()
        feature_count = (
            await session.execute(select(func.count()).select_from(FeatureRecord))
        ).scalar_one()
        metadata_count = (
            await session.execute(
                select(func.count()).select_from(MarketSeriesMetadata)
            )
        ).scalar_one()
        assert snapshot_count == 2
        assert manifest_count == 2
        assert feature_count == 120
        assert metadata_count >= 2
