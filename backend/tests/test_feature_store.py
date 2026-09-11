"""W2-U03 feature definition framework and feature store tests."""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

import pytest

from app.ml.dataset import (
    CanonicalOHLCVRecord,
    MarketMetadataService,
    MarketSeriesKey,
    MarketSeriesMetadataRead,
    SourceAuthority,
)
from app.ml.features import (
    ComputableFeature,
    DuplicateFeatureDefinitionError,
    FeatureDefinitionSpec,
    FeatureInputRejectedError,
    FeatureStoreService,
    NonCausalFeatureError,
    builtin_feature_set_v1,
)


def _utc(minute: int) -> datetime:
    return datetime(2026, 7, 13, 16, minute, tzinfo=timezone.utc)


def _series_key() -> MarketSeriesKey:
    return MarketSeriesKey(
        market_class="forex",
        provider="internal",
        symbol="EURUSD",
        timeframe="M1",
    )


def _record(minute: int, *, source: str = "sample:feature.csv") -> CanonicalOHLCVRecord:
    base = Decimal("1.1000") + Decimal(minute) * Decimal("0.0010")
    return CanonicalOHLCVRecord(
        series_key=_series_key(),
        open_time=_utc(minute),
        open=base,
        high=base + Decimal("0.0020"),
        low=base - Decimal("0.0020"),
        close=base + Decimal("0.0010"),
        volume=Decimal("100"),
        source=source,
        authority_classification=SourceAuthority.AUTHORITATIVE,
        source_record_id=f"feature-rec-{minute}",
    )


@pytest.mark.asyncio
async def test_feature_definition_uniqueness(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        service = FeatureStoreService(session)
        spec = builtin_feature_set_v1()[0].spec
        await service.register_definition(spec)
        with pytest.raises(DuplicateFeatureDefinitionError):
            await service.register_definition(spec)


def test_non_causal_feature_definition_rejected() -> None:
    spec = FeatureDefinitionSpec(
        feature_name="future_close_peek",
        feature_version="v1",
        formula_spec={"uses_future": True, "formula": "close_t_plus_1"},
        input_requirements={"ohlc": True},
        lookback_window=1,
        causal=False,
    )
    with pytest.raises(NonCausalFeatureError, match="FEATURE_LOOKAHEAD"):
        ComputableFeature(spec, lambda records, index: records[index + 1].close)


@pytest.mark.asyncio
async def test_feature_store_compute_hash_reproducible_and_quality_report(
    prepared_db: None,
) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        service = FeatureStoreService(session)
        await service.register_builtin_definitions()
        records = [_record(0), _record(1), _record(2)]
        feature_rows, report = await service.compute_and_store(
            series_key=_series_key(),
            records=records,
            source_dataset_hash="dataset-hash-123",
        )
        first_hash = report.content_hash
        recomputed = service.compute_feature_hash(
            feature_rows, feature_set_version="feature_set.v1"
        )
        assert first_hash == recomputed
        assert report.missing_rate >= 0.0
        assert report.leakage_checks["causal"] is True
        assert report.leakage_checks["identity_fields_excluded"] is True
        assert all("symbol" not in row.features for row in feature_rows)
        assert all("provider" not in row.features for row in feature_rows)
        assert all("market_class" not in row.features for row in feature_rows)


@pytest.mark.asyncio
async def test_feature_output_excludes_identity_but_evaluation_metadata_readable(
    prepared_db: None,
) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        metadata = MarketMetadataService(session)
        await metadata.upsert_metadata(
            MarketSeriesMetadataRead(
                series_key=_series_key(),
                session_calendar="forex-weekday",
                tick_size=Decimal("0.00001"),
                price_precision=5,
                timezone_assumption="UTC",
                source_authority=SourceAuthority.AUTHORITATIVE,
            )
        )
        service = FeatureStoreService(session)
        feature_rows, _ = await service.compute_and_store(
            series_key=_series_key(),
            records=[_record(0), _record(1), _record(2)],
            source_dataset_hash="dataset-hash-identity-test",
        )
        feature_keys = set(feature_rows[-1].features)
        assert feature_keys.isdisjoint({"symbol", "provider", "market_class", "symbol_id"})
        eval_metadata = await service.get_evaluation_metadata(_series_key())
        assert eval_metadata is not None
        assert eval_metadata.series_key.symbol == "EURUSD"
        assert eval_metadata.metadata_role == "governance_evaluation_only"


@pytest.mark.asyncio
async def test_forward_dated_guarded_record_blocked_before_feature_computation(
    prepared_db: None,
) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        service = FeatureStoreService(session)
        with pytest.raises(FeatureInputRejectedError, match="FUTURE_OPEN_TIME"):
            await service.compute_and_store(
                series_key=_series_key(),
                records=[_record(0), _record(5)],
                source_dataset_hash="dataset-hash-future",
                as_of_time=_utc(1),
                ingestion_finished_at=_utc(1),
            )


def test_feature_code_uses_query_port_not_candle_orm() -> None:
    root = Path(__file__).resolve().parents[1] / "app" / "ml" / "features"
    offenders: list[str] = []
    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        if "app.db.models.candle" in text or "CandleRepository" in text:
            offenders.append(path.name)
    assert offenders == []


def test_no_symbol_identity_feature_pattern_in_feature_modules() -> None:
    root = Path(__file__).resolve().parents[1] / "app" / "ml" / "features"
    forbidden = ("symbol_id", "one_hot_symbol", "symbol_identity")
    offenders: list[str] = []
    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for needle in forbidden:
            if needle in text:
                offenders.append(f"{path.name}:{needle}")
    assert offenders == []
