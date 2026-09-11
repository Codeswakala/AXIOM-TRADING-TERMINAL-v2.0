"""W2-U02 market-agnostic data access and metadata tests."""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.candle import Candle
from app.ml.dataset import (
    CANONICAL_MARKET_CLASSES,
    CandleMarketDataQueryAdapter,
    ChronologyGuard,
    DerivSyntheticIndicesAdapter,
    GuardRecord,
    GuardStage,
    MarketMetadataService,
    MarketSeriesKey,
    MarketSeriesMetadataRead,
    QuarantineReason,
    SourceAuthority,
)


def _utc(minute: int = 0) -> datetime:
    return datetime(2026, 7, 13, 12, minute, tzinfo=timezone.utc)


async def _add_candle(
    session: AsyncSession,
    *,
    market_class: str,
    symbol: str,
    minute: int,
    source: str,
) -> Candle:
    candle = Candle(
        market_class=market_class,
        symbol=symbol,
        timeframe="M1",
        open_time=_utc(minute),
        open=Decimal("1.0"),
        high=Decimal("1.1"),
        low=Decimal("0.9"),
        close=Decimal("1.05"),
        volume=Decimal("100"),
        source=source,
    )
    session.add(candle)
    await session.flush()
    return candle


def _guard_record(
    *,
    market_class: str,
    provider: str,
    symbol: str,
    minute: int,
    source: str = "sample:unit.csv",
) -> GuardRecord:
    return GuardRecord(
        source_record_id=f"{market_class}-{provider}-{symbol}-{minute}-{source}",
        market_class=market_class,
        provider=provider,
        symbol=symbol,
        timeframe="M1",
        open_time=_utc(minute),
        source=source,
        authority=SourceAuthority.AUTHORITATIVE,
        ingestion_finished_at=_utc(10),
        as_of_time=_utc(10),
    )


def test_market_series_key_rejects_new_top_level_market() -> None:
    assert "synthetic" in CANONICAL_MARKET_CLASSES
    try:
        MarketSeriesKey(market_class="deriv", provider="deriv", symbol="BOOM500", timeframe="M1")
    except ValueError as exc:
        assert "unsupported market_class" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("Deriv must not become a top-level market class")


def test_deriv_adapter_is_provider_under_synthetic_no_live_connection() -> None:
    adapter = DerivSyntheticIndicesAdapter()
    series = list(adapter.list_supported_series())
    assert adapter.provider_name == "deriv"
    assert adapter.market_class.value == "synthetic"
    assert series[0].series_key.market_class == "synthetic"
    assert series[0].series_key.provider == "deriv"
    assert series[0].source_authority == SourceAuthority.SYNTHETIC
    assert "no live Deriv connection" in (series[0].known_limitations or "")


@pytest.mark.asyncio
async def test_canonical_ohlcv_mapping_and_authority_across_markets(
    prepared_db: None,
) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        await _add_candle(
            session,
            market_class="forex",
            symbol="EURUSD",
            minute=0,
            source="sample:eurusd.csv",
        )
        await _add_candle(
            session,
            market_class="crypto",
            symbol="BTCUSD",
            minute=0,
            source="live:simulated",
        )
        adapter = CandleMarketDataQueryAdapter(session)
        series = await adapter.list_series()
        assert {item.market_class for item in series} >= {"forex", "crypto"}

        forex = await adapter.get_candles(
            series_key=MarketSeriesKey(
                market_class="forex", provider="internal", symbol="EURUSD", timeframe="M1"
            )
        )
        crypto = await adapter.get_candles(
            series_key=MarketSeriesKey(
                market_class="crypto", provider="internal", symbol="BTCUSD", timeframe="M1"
            )
        )
        # BO-B-DATA A2: the `sample:*` fixture label is non-authoritative;
        # only an explicit `historical:real` declaration grants authority.
        assert forex[0].authority_classification == SourceAuthority.UNKNOWN
        assert crypto[0].authority_classification == SourceAuthority.SIMULATED
        assert forex[0].natural_key[0:4] == ("forex", "internal", "EURUSD", "M1")


@pytest.mark.asyncio
async def test_metadata_stored_queryable_and_not_learned_feature(
    prepared_db: None,
) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        service = MarketMetadataService(session)
        key = MarketSeriesKey(
            market_class="synthetic",
            provider="deriv",
            symbol="DERIV_SYNTHETIC_INDEX_PLACEHOLDER",
            timeframe="M1",
        )
        await service.upsert_metadata(
            MarketSeriesMetadataRead(
                series_key=key,
                session_calendar="continuous-synthetic",
                tick_size=Decimal("0.01"),
                price_precision=2,
                timezone_assumption="UTC",
                source_authority=SourceAuthority.SYNTHETIC,
                known_limitations="provider skeleton only",
            )
        )
        loaded = await service.get_metadata(key)
        assert loaded is not None
        assert loaded.metadata_role == "governance_evaluation_only"
        assert loaded.series_key.market_class == "synthetic"
        assert await service.list_market_classes() == ["synthetic"]


def test_duplicate_and_ordering_validation_across_markets_and_providers() -> None:
    guard = ChronologyGuard()
    accepted, quarantine = guard.validate_records(
        [
            _guard_record(market_class="forex", provider="internal", symbol="EURUSD", minute=2),
            _guard_record(market_class="forex", provider="internal", symbol="EURUSD", minute=1),
            _guard_record(market_class="crypto", provider="internal", symbol="BTCUSD", minute=1),
            _guard_record(market_class="crypto", provider="internal", symbol="BTCUSD", minute=1),
        ],
        stage=GuardStage.DATASET_CONSTRUCTION,
        authoritative_training=False,
    )
    assert len(accepted) == 2
    assert {event.reason for event in quarantine} == {
        QuarantineReason.OUT_OF_ORDER_TIME,
        QuarantineReason.DUPLICATE_NATURAL_KEY,
    }


def test_provider_terms_do_not_leak_outside_provider_adapter() -> None:
    root = Path(__file__).resolve().parents[1] / "app" / "ml" / "dataset"
    offenders: list[str] = []
    for path in root.rglob("*.py"):
        if path.name in {"provider_adapters.py", "__init__.py"}:
            continue
        text = path.read_text(encoding="utf-8")
        if "DERIV_SYNTHETIC_INDEX_PLACEHOLDER" in text or "Deriv" in text:
            offenders.append(path.name)
    assert offenders == []


def test_ml_modules_use_query_port_not_scattered_candle_orm() -> None:
    root = Path(__file__).resolve().parents[1] / "app" / "ml"
    offenders: list[str] = []
    for path in root.rglob("*.py"):
        rel = path.relative_to(root).as_posix()
        if rel == "dataset/market_data_query.py":
            continue
        text = path.read_text(encoding="utf-8")
        if "app.db.models.candle" in text or "CandleRepository" in text:
            offenders.append(rel)
    assert offenders == []


def test_no_symbol_identity_learned_feature_pattern() -> None:
    root = Path(__file__).resolve().parents[1] / "app" / "ml"
    forbidden = ("symbol_id", "one_hot_symbol", "symbol_identity")
    offenders: list[str] = []
    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for needle in forbidden:
            if needle in text:
                offenders.append(f"{path.name}:{needle}")
    assert offenders == []
