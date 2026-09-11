"""B-01 dev-database execution runner (DA evidence tooling, untracked).

Steps executed against backend/axiom_dev.db (fresh, auto-created):
  corpus generation -> API ingestion (done via HTTP, see b01_api_ingestion.log)
  -> snapshot freeze (pipeline_validation tier)
  -> temporal split manifests -> feature computation + quality reports
  -> negative control: research-tier freeze attempt over the synthetic corpus
     must quarantine.
Prints per-table row counts as Level-I evidence.
"""

from __future__ import annotations

import asyncio
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from sqlalchemy import func, select  # noqa: E402

from app.db.models.dataset import (  # noqa: E402
    DatasetLineageRecord,
    DatasetQuarantineRecord,
    DatasetSeriesMember,
    DatasetSnapshot,
)
from app.db.models.dataset_split import DatasetSplitManifest  # noqa: E402
from app.db.models.feature import FeatureRecord  # noqa: E402
from app.db.models.feature_definition import (  # noqa: E402
    FeatureDefinition,
    FeatureQualityReport,
)
from app.db.models.ingestion_run import IngestionRun  # noqa: E402
from app.db.models.market_metadata import MarketSeriesMetadata  # noqa: E402
from app.core.config import Settings  # noqa: E402
from app.db.session import get_session_factory, init_db  # noqa: E402
from app.ml.dataset.market_data_query import CandleMarketDataQueryAdapter  # noqa: E402
from app.ml.dataset.service import DatasetService, DatasetSnapshotInput  # noqa: E402
from app.ml.dataset.split_engine import TemporalSplitConfig, TemporalSplitEngine  # noqa: E402
from app.ml.dataset.split_store import store_manifest  # noqa: E402
from app.ml.dataset.synthetic_corpus import (  # noqa: E402
    CORPUS_SERIES_KEYS,
    generate_series,
    write_corpus_csv,
)
from app.ml.features.store import FeatureStoreService  # noqa: E402

DB_URL = "sqlite+aiosqlite:////home/user/axiom/backend/axiom_dev.db"
CORPUS_DIR = Path("/home/user/axiom/backend/tests/fixtures/b01_corpus")
BARS = 2000


async def _count(session, model, *, label: str) -> None:
    total = (await session.execute(select(func.count()).select_from(model))).scalar_one()
    print(f"[b01] {label}: {total}")


async def main() -> None:
    init_db(Settings(database_url=DB_URL))
    factory = get_session_factory()
    CORPUS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[b01] corpus_dir={CORPUS_DIR}")
    print("[b01] generating corpus CSVs (deterministic, source='synthetic')")
    for key in CORPUS_SERIES_KEYS:
        bars = generate_series(
            market_class=key.market_class, symbol=key.symbol, bars=BARS
        )
        write_corpus_csv(CORPUS_DIR / f"{key.market_class}_{key.symbol}_H1.csv", bars)
        print(
            f"[b01] corpus {key.market_class}/{key.symbol} bars={len(bars)} "
            f"first={bars[0].open_time.isoformat()} last={bars[-1].open_time.isoformat()}"
        )

    async with factory() as session:
        print("[b01] ---- negative control: research-tier freeze must quarantine ----")
        svc = DatasetService(session)
        key = CORPUS_SERIES_KEYS[0]
        bars = generate_series(market_class=key.market_class, symbol=key.symbol, bars=200)
        neg = await svc.create_draft_snapshot(
            DatasetSnapshotInput(
                dataset_id="ds-b01-negative-control",
                name="B01 negative control (research tier over synthetic)",
                version=1,
                market=key.market_class,
                timeframe=key.timeframe,
                start_time=bars[0].open_time,
                end_time=bars[-1].open_time,
                source="synthetic",
                feature_version="feature_set.v1",
                quality_score="pass",
                tier="research_validation",
                created_by="b01-runner",
            )
        )
        frozen_neg = await svc.freeze_from_candles(
            snapshot=neg,
            candles=bars,
            provider="internal",
            as_of_time=bars[-1].open_time,
            ingestion_finished_at=bars[-1].open_time,
        )
        print(f"[b01] negative control status: {frozen_neg.status}")
        qrows = (
            await session.execute(
                select(DatasetQuarantineRecord).where(
                    DatasetQuarantineRecord.dataset_snapshot_id == frozen_neg.id
                )
            )
        ).scalars().all()
        for q in qrows[:3]:
            print(f"[b01] quarantine: {q.reason_code} {q.symbol} {q.detail[:80]}")

        print("[b01] ---- freeze pipeline-validation snapshots over ingested corpus ----")
        adapter = CandleMarketDataQueryAdapter(session, provider="internal")
        series = await adapter.list_series()
        h1_keys = [k for k in series if k.timeframe == "H1"]
        print(f"[b01] ingested H1 series found: {len(h1_keys)} -> {[(k.market_class, k.symbol) for k in h1_keys]}")

        store = FeatureStoreService(session)
        definitions = await store.register_builtin_definitions()
        print(f"[b01] registered feature definitions: {[d.feature_name for d in definitions]}")

        for key in h1_keys:
            records = await adapter.get_candles(
                series_key=key, source_filter="synthetic"
            )
            print(f"[b01] series {key.market_class}/{key.symbol}: {len(records)} synthetic candles")
            snapshot = await svc.create_draft_snapshot(
                DatasetSnapshotInput(
                    dataset_id=f"ds-b01-{key.market_class}-{key.symbol.lower()}",
                    name=f"B01 {key.market_class}/{key.symbol} pipeline-validation snapshot",
                    version=1,
                    market=key.market_class,
                    timeframe=key.timeframe,
                    start_time=records[0].open_time,
                    end_time=records[-1].open_time,
                    source="synthetic",
                    feature_version="feature_set.v1",
                    quality_score="pass",
                    tier="pipeline_validation",
                    created_by="b01-runner",
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
            print(
                f"[b01] frozen {key.symbol}: status={frozen.status} "
                f"tier={frozen.source_policy['tier']} "
                f"content_hash={frozen.content_hash[:16]}…"
            )

            n = len(records)
            row_dicts = [
                {"row_id": r.source_record_id or str(i), "as_of": r.open_time}
                for i, r in enumerate(records)
            ]
            config = TemporalSplitConfig(
                split_id=f"split-b01-{key.symbol.lower()}",
                train_start=records[0].open_time,
                train_end=records[int(n * 0.5) - 1].open_time,
                validation_start=records[int(n * 0.5)].open_time,
                validation_end=records[int(n * 0.8) - 1].open_time,
                test_start=records[int(n * 0.8)].open_time,
                test_end=records[-1].open_time,
                label_horizon_bars=1,
                embargo_bars=1,
            )
            split_rows = TemporalSplitEngine().split(rows=row_dicts, config=config)
            manifest = await store_manifest(
                session, snapshot=frozen, split=split_rows, config=config
            )
            print(
                f"[b01] split {manifest.split_id}: train={manifest.train_count} "
                f"val={manifest.validation_count} test={manifest.test_count} "
                f"hash={manifest.split_hash[:16]}…"
            )

            output, report = await store.compute_and_store(
                series_key=key,
                records=records,
                source_dataset_hash=frozen.content_hash,
                tier="pipeline_validation",
            )
            print(
                f"[b01] features {key.symbol}: records={len(output)} "
                f"quality_report={report.id[:8]}… missing_rate={report.missing_rate} "
                f"leakage_checks={report.leakage_checks}"
            )

        await session.commit()

    async with factory() as session:
        print("[b01] ---- table row counts (post-execution) ----")
        await _count(session, IngestionRun, label="ingestion_runs")
        await _count(session, MarketSeriesMetadata, label="market_series_metadata")
        await _count(session, DatasetSnapshot, label="dataset_snapshots")
        await _count(session, DatasetLineageRecord, label="dataset_lineage_records")
        await _count(session, DatasetSeriesMember, label="dataset_series_members")
        await _count(session, DatasetSplitManifest, label="dataset_split_manifests")
        await _count(session, FeatureDefinition, label="feature_definitions")
        await _count(session, FeatureRecord, label="feature_records")
        await _count(session, FeatureQualityReport, label="feature_quality_reports")
        await _count(session, DatasetQuarantineRecord, label="dataset_quarantine_records")


if __name__ == "__main__":
    asyncio.run(main())
