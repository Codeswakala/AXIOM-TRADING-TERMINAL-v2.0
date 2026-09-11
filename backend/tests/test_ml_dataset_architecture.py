"""W2-U01 dataset architecture and chronology guard tests."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.candle import Candle
from app.ml.dataset import (
    CandleMarketDataQueryAdapter,
    ChronologyGuard,
    DatasetService,
    DatasetSnapshotInput,
    GuardRecord,
    GuardStage,
    MarketSeriesKey,
    QuarantineReason,
    SourceAuthority,
)


def _utc(minute: int = 0) -> datetime:
    return datetime(2026, 7, 13, 10, minute, tzinfo=timezone.utc)


async def _add_candle(
    session: AsyncSession,
    *,
    symbol: str = "EURUSD",
    minute: int = 0,
    source: str = "sample:unit.csv",
) -> Candle:
    candle = Candle(
        market_class="forex",
        symbol=symbol,
        timeframe="M1",
        open_time=_utc(minute),
        open=Decimal("1.1000"),
        high=Decimal("1.1100"),
        low=Decimal("1.0900"),
        close=Decimal("1.1050"),
        volume=Decimal("100"),
        source=source,
    )
    session.add(candle)
    await session.flush()
    return candle


def _snapshot_input(version: int = 1) -> DatasetSnapshotInput:
    return DatasetSnapshotInput(
        dataset_id="ds-w2-u01-unit",
        name="W2 U01 unit dataset",
        version=version,
        market="forex",
        timeframe="M1",
        start_time=_utc(0),
        end_time=_utc(5),
        source="sample:unit.csv",
        feature_version="features.none.v0",
        quality_score="pass",
        created_by="pytest",
        # BO-B-DATA A2: fixture sources are non-authoritative; machinery
        # tests therefore declare the pipeline_validation tier.
        tier="pipeline_validation",
    )


@pytest.mark.asyncio
async def test_dataset_snapshot_freeze_hash_lineage_and_new_version(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        candles = [await _add_candle(session, minute=0), await _add_candle(session, minute=1)]
        service = DatasetService(session)
        snapshot = await service.create_draft_snapshot(_snapshot_input())
        frozen = await service.freeze_from_candles(
            snapshot=snapshot,
            candles=candles,
            provider="internal",
            as_of_time=_utc(5),
            ingestion_finished_at=_utc(5),
        )
        assert frozen.status == "frozen"
        assert frozen.content_hash
        assert frozen.dataset_id
        assert frozen.market == "forex"
        assert frozen.timeframe == "M1"
        assert frozen.source == "sample:unit.csv"
        assert frozen.feature_version == "features.none.v0"
        assert frozen.quality_score == "pass"
        assert frozen.created_at.tzinfo is not None

        same_hash = service.compute_content_hash(
            snapshot=frozen,
            records=[
                service._guard_record_from_canonical(  # noqa: SLF001 - white-box reproducibility
                    service._canonical_from_candle_like(c, provider="internal"),  # noqa: SLF001
                    as_of_time=_utc(5),
                    ingestion_finished_at=_utc(5),
                )
                for c in candles
            ],
        )
        assert same_hash == frozen.content_hash

        with pytest.raises(ValueError, match="immutable"):
            await service.freeze_from_candles(
                snapshot=frozen,
                candles=candles,
                provider="internal",
                as_of_time=_utc(5),
                ingestion_finished_at=_utc(5),
            )

        new_version = await service.create_new_version_from_frozen(frozen, version=2)
        assert new_version.version == 2
        assert new_version.status == "draft"


@pytest.mark.asyncio
async def test_no_anonymous_dataset_rejected(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        service = DatasetService(session)
        bad = _snapshot_input()
        bad = DatasetSnapshotInput(
            dataset_id="",
            name=bad.name,
            version=bad.version,
            market=bad.market,
            timeframe=bad.timeframe,
            start_time=bad.start_time,
            end_time=bad.end_time,
            source=bad.source,
            feature_version=bad.feature_version,
            quality_score=bad.quality_score,
        )
        with pytest.raises(ValueError, match="anonymous/incomplete"):
            await service.create_draft_snapshot(bad)


@pytest.mark.asyncio
async def test_forward_dated_record_quarantined_with_reason(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        future = await _add_candle(session, minute=5)
        service = DatasetService(session)
        snapshot = await service.create_draft_snapshot(_snapshot_input())
        result = await service.freeze_from_candles(
            snapshot=snapshot,
            candles=[future],
            provider="internal",
            as_of_time=_utc(1),
            ingestion_finished_at=_utc(1),
        )
        assert result.status == "quarantined"
        rows = await service.list_quarantine(snapshot.id)
        assert rows[0].reason_code == QuarantineReason.FUTURE_OPEN_TIME.value


def _guard_record(
    minute: int,
    *,
    source: str = "sample:unit.csv",
    authority: SourceAuthority = SourceAuthority.AUTHORITATIVE,
    as_of_minute: int = 10,
    source_record_id: str | None = None,
    self_declared_as_of_time: datetime | None = None,
) -> GuardRecord:
    return GuardRecord(
        source_record_id=source_record_id or f"rec-{minute}-{source}",
        market_class="forex",
        provider="internal",
        symbol="EURUSD",
        timeframe="M1",
        open_time=_utc(minute),
        source=source,
        authority=authority,
        ingestion_finished_at=_utc(as_of_minute),
        as_of_time=_utc(as_of_minute),
        self_declared_as_of_time=self_declared_as_of_time,
    )


def test_out_of_order_authoritative_quarantined_not_resorted() -> None:
    guard = ChronologyGuard()
    accepted, quarantine = guard.validate_records(
        [_guard_record(2), _guard_record(1)],
        stage=GuardStage.DATASET_CONSTRUCTION,
    )
    assert [r.open_time for r in accepted] == [_utc(2)]
    assert quarantine[0].reason == QuarantineReason.OUT_OF_ORDER_TIME


def test_synthetic_and_forward_simulated_excluded_from_authoritative_training() -> None:
    guard = ChronologyGuard()
    accepted, quarantine = guard.validate_records(
        [
            _guard_record(0, source="seed:synthetic", authority=SourceAuthority.SYNTHETIC),
            _guard_record(1, source="live:simulated", authority=SourceAuthority.SIMULATED),
        ],
        stage=GuardStage.DATASET_CONSTRUCTION,
    )
    assert accepted == []
    assert {q.reason for q in quarantine} == {
        QuarantineReason.SYNTHETIC_SOURCE_NOT_AUTHORITATIVE,
        QuarantineReason.SIMULATED_FORWARD_DATED,
    }


def test_random_split_rejected_and_label_horizon_leakage_rejected() -> None:
    guard = ChronologyGuard()
    with pytest.raises(ValueError, match=QuarantineReason.SPLIT_LEAKAGE.value):
        guard.validate_temporal_split(split_strategy="random")

    with pytest.raises(ValueError, match=QuarantineReason.LABEL_HORIZON_LEAKAGE.value):
        guard.validate_label_horizon(
            label_start=_utc(4),
            label_horizon_end=_utc(6),
            validation_start=_utc(5),
            embargo=timedelta(minutes=0),
        )


def test_spoofed_future_safe_timestamp_cannot_bypass_authoritative_anchor() -> None:
    guard = ChronologyGuard()
    accepted, quarantine = guard.validate_records(
        [_guard_record(5, as_of_minute=1, self_declared_as_of_time=_utc(9))],
        stage=GuardStage.INGESTION,
    )
    assert accepted == []
    assert quarantine[0].reason == QuarantineReason.FUTURE_OPEN_TIME


@pytest.mark.asyncio
async def test_market_data_query_port_lists_and_fetches_candles(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        await _add_candle(session, symbol="EURUSD", minute=0)
        adapter = CandleMarketDataQueryAdapter(session)
        series = await adapter.list_series()
        assert any(item.symbol == "EURUSD" and item.provider == "internal" for item in series)
        candles = await adapter.get_candles(
            series_key=MarketSeriesKey(
                market_class="forex",
                provider="internal",
                symbol="EURUSD",
                timeframe="M1",
            )
        )
        assert len(candles) == 1
        assert candles[0].series_key.market_class == "forex"
        metadata = await adapter.get_source_metadata(source="sample:unit.csv")
        # BO-B-DATA A2: fixture labels no longer manufacture authority.
        assert metadata.authority == "unknown"
        real_metadata = await adapter.get_source_metadata(source="historical:real")
        assert real_metadata.authority == "authoritative"


def test_ml_dataset_modules_do_not_introduce_symbol_identity_feature_pattern() -> None:
    root = Path(__file__).resolve().parents[1] / "app" / "ml"
    forbidden = ("symbol_id", "one_hot_symbol", "symbol_identity")
    offenders: list[str] = []
    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for needle in forbidden:
            if needle in text:
                offenders.append(f"{path.relative_to(root)}:{needle}")
    assert offenders == []
