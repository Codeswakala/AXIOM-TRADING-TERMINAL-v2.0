"""BO-B-DATA Part B — research-tier proof runner (DA evidence tooling, untracked).

1. Verify market_series_metadata rows carry AUTHORITATIVE authority for the
   ingested historical:real series.
2. Freeze a research_validation snapshot over the REAL OKX BTCUSDT H1 corpus
   — must be frozen with ZERO quarantine events (guard at authoritative tier).
3. Negative control: research_validation tier over the SYNTHETIC EURUSD corpus
   — must quarantine with SYNTHETIC_SOURCE_NOT_AUTHORITATIVE.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from sqlalchemy import func, select  # noqa: E402

from app.core.config import Settings  # noqa: E402
from app.core.time import coerce_external_utc  # noqa: E402
from app.db.models.dataset import (  # noqa: E402
    DatasetQuarantineRecord,
    DatasetSnapshot,
)
from app.db.models.market_metadata import MarketSeriesMetadata  # noqa: E402
from app.db.session import get_session_factory, init_db  # noqa: E402
from app.ml.dataset.market_data_query import (  # noqa: E402
    CandleMarketDataQueryAdapter,
    MarketSeriesKey,
)
from app.ml.dataset.service import DatasetService, DatasetSnapshotInput  # noqa: E402

DB_URL = "sqlite+aiosqlite:////home/user/axiom/backend/axiom_dev.db"


async def main() -> None:
    init_db(Settings(database_url=DB_URL))
    factory = get_session_factory()

    async with factory() as session:
        print("[bdata] ---- metadata authority check ----")
        metadata_rows = (
            await session.execute(
                select(MarketSeriesMetadata).where(
                    MarketSeriesMetadata.source_authority == "authoritative"
                )
            )
        ).scalars().all()
        real_series = [
            (m.market_class, m.symbol, m.timeframe)
            for m in metadata_rows
            if m.symbol in {"BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT", "BTCUSD", "ETHUSD"}
        ]
        print(f"[bdata] AUTHORITATIVE metadata rows: {len(real_series)} -> {sorted(real_series)[:12]}")

        adapter = CandleMarketDataQueryAdapter(session, provider="internal")
        key = MarketSeriesKey(
            market_class="crypto", provider="internal", symbol="BTCUSDT", timeframe="H1"
        )
        records = await adapter.get_candles(series_key=key, source_filter="historical:real")
        print(f"[bdata] real BTCUSDT H1 candles: {len(records)}")
        print(
            f"[bdata] first={coerce_external_utc(records[0].open_time, source='runner').isoformat()} "
            f"last={coerce_external_utc(records[-1].open_time, source='runner').isoformat()}"
        )

        svc = DatasetService(session)
        snapshot = await svc.create_draft_snapshot(
            DatasetSnapshotInput(
                dataset_id="ds-bdata-real-btcusdt-h1",
                name="B-DATA real historical BTCUSDT H1 research-validation snapshot",
                version=1,
                market="crypto",
                timeframe="H1",
                start_time=coerce_external_utc(records[0].open_time, source="runner"),
                end_time=coerce_external_utc(records[-1].open_time, source="runner"),
                source="historical:real",
                feature_version="feature_set.v1",
                quality_score="pass",
                tier="research_validation",
                created_by="bdata-runner",
            )
        )
        frozen = await svc.freeze_from_query(
            snapshot=snapshot,
            query_port=adapter,
            market_class=key.market_class,
            provider=key.provider,
            symbol=key.symbol,
            timeframe=key.timeframe,
            as_of_time=coerce_external_utc(records[-1].open_time, source="runner"),
            ingestion_finished_at=coerce_external_utc(records[-1].open_time, source="runner"),
        )
        print(
            f"[bdata] research-tier REAL snapshot: status={frozen.status} "
            f"content_hash={frozen.content_hash[:16]}…"
        )
        quarantine = (
            await session.execute(
                select(func.count())
                .select_from(DatasetQuarantineRecord)
                .where(DatasetQuarantineRecord.dataset_snapshot_id == frozen.id)
            )
        ).scalar_one()
        print(f"[bdata] quarantine rows for real snapshot: {quarantine} (must be 0)")

        print("[bdata] ---- negative control: synthetic at research tier ----")
        synth_key = MarketSeriesKey(
            market_class="forex", provider="internal", symbol="EURUSD", timeframe="H1"
        )
        synth_records = await adapter.get_candles(series_key=synth_key, source_filter="synthetic")
        print(f"[bdata] synthetic EURUSD H1 candles: {len(synth_records)}")
        neg = await svc.create_draft_snapshot(
            DatasetSnapshotInput(
                dataset_id="ds-bdata-neg-control",
                name="B-DATA negative control (research tier over synthetic)",
                version=1,
                market="forex",
                timeframe="H1",
                start_time=coerce_external_utc(synth_records[0].open_time, source="runner"),
                end_time=coerce_external_utc(synth_records[-1].open_time, source="runner"),
                source="synthetic",
                feature_version="feature_set.v1",
                quality_score="pass",
                tier="research_validation",
                created_by="bdata-runner",
            )
        )
        neg_frozen = await svc.freeze_from_query(
            snapshot=neg,
            query_port=adapter,
            market_class=synth_key.market_class,
            provider=synth_key.provider,
            symbol=synth_key.symbol,
            timeframe=synth_key.timeframe,
            as_of_time=coerce_external_utc(synth_records[-1].open_time, source="runner"),
            ingestion_finished_at=coerce_external_utc(synth_records[-1].open_time, source="runner"),
        )
        print(f"[bdata] negative control status: {neg_frozen.status} (must be quarantined)")
        neg_reasons = (
            await session.execute(
                select(DatasetQuarantineRecord.reason_code)
                .where(DatasetQuarantineRecord.dataset_snapshot_id == neg_frozen.id)
                .limit(1)
            )
        ).scalars().all()
        print(f"[bdata] negative control reasons: {neg_reasons}")

        await session.commit()

    async with factory() as session:
        total = (
            await session.execute(select(func.count()).select_from(DatasetSnapshot))
        ).scalar_one()
        print(f"[bdata] dataset_snapshots total: {total}")


if __name__ == "__main__":
    asyncio.run(main())
