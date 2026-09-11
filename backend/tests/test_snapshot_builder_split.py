"""W2-U04 reproducible snapshot builder and temporal split tests."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

import pytest

from app.ml.dataset import (
    CanonicalOHLCVRecord,
    DatasetSnapshotInput,
    MarketSeriesKey,
    ReproducibleSnapshotBuilder,
    SourceAuthority,
    TemporalSplitConfig,
    TemporalSplitEngine,
)
from app.ml.dataset.chronology_guard import QuarantineReason


def _utc(minute: int) -> datetime:
    return datetime(2026, 7, 13, 18, minute, tzinfo=timezone.utc)


def _series_key() -> MarketSeriesKey:
    return MarketSeriesKey(
        market_class="forex",
        provider="internal",
        symbol="EURUSD",
        timeframe="M1",
    )


def _record(minute: int, *, source: str = "sample:split.csv") -> CanonicalOHLCVRecord:
    price = Decimal("1.1000") + Decimal(minute) * Decimal("0.0010")
    return CanonicalOHLCVRecord(
        series_key=_series_key(),
        open_time=_utc(minute),
        open=price,
        high=price + Decimal("0.0020"),
        low=price - Decimal("0.0020"),
        close=price + Decimal("0.0010"),
        volume=Decimal("100"),
        source=source,
        authority_classification=SourceAuthority.AUTHORITATIVE,
        source_record_id=f"split-rec-{minute}",
    )


def _snapshot_input(*, dataset_id: str, version: int) -> DatasetSnapshotInput:
    return DatasetSnapshotInput(
        dataset_id=dataset_id,
        name="W2 U04 snapshot builder test",
        version=version,
        market="forex",
        timeframe="M1",
        start_time=_utc(0),
        end_time=_utc(9),
        source="sample:split.csv",
        feature_version="feature_set.v1",
        quality_score="pass",
        created_by="pytest",
    )


def _split_config(*, label_horizon_bars: int = 1, embargo_bars: int = 1) -> TemporalSplitConfig:
    return TemporalSplitConfig(
        split_id="temporal-v1",
        train_start=_utc(0),
        train_end=_utc(2),
        validation_start=_utc(5),
        validation_end=_utc(6),
        test_start=_utc(8),
        test_end=_utc(9),
        label_horizon_bars=label_horizon_bars,
        embargo_bars=embargo_bars,
    )


@pytest.mark.asyncio
async def test_snapshot_builder_rebuild_same_inputs_identical_hash(prepared_db: None) -> None:
    from app.db.session import session_scope

    records = [_record(i) for i in range(6)]
    async with session_scope() as session:
        builder = ReproducibleSnapshotBuilder(session)
        first = await builder.build_from_records(
            snapshot_input=_snapshot_input(dataset_id="builder-repro", version=1),
            series_key=_series_key(),
            records=records,
            as_of_time=_utc(9),
            ingestion_finished_at=_utc(9),
        )
        second = await builder.build_from_records(
            snapshot_input=_snapshot_input(dataset_id="builder-repro", version=2),
            series_key=_series_key(),
            records=records,
            as_of_time=_utc(9),
            ingestion_finished_at=_utc(9),
            feature_set_version="feature_set.v1.rebuild_check",
        )
        assert first.snapshot.content_hash == second.snapshot.content_hash
        assert all("symbol" not in row["features"] for row in first.matrix_rows)
        assert all("provider" not in row["features"] for row in first.matrix_rows)


@pytest.mark.asyncio
async def test_frozen_snapshot_immutable_new_version_created(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        builder = ReproducibleSnapshotBuilder(session)
        result = await builder.build_from_records(
            snapshot_input=_snapshot_input(dataset_id="builder-immutable", version=1),
            series_key=_series_key(),
            records=[_record(i) for i in range(4)],
            as_of_time=_utc(9),
            ingestion_finished_at=_utc(9),
        )
        with pytest.raises(ValueError, match="immutable"):
            await builder._datasets.freeze_from_canonical_records(  # noqa: SLF001
                snapshot=result.snapshot,
                records=[_record(i) for i in range(4)],
                as_of_time=_utc(9),
                ingestion_finished_at=_utc(9),
            )
        new_version = await builder._datasets.create_new_version_from_frozen(  # noqa: SLF001
            result.snapshot, version=2
        )
        assert new_version.status == "draft"
        assert new_version.version == 2


def test_random_split_rejected_and_temporal_split_hash_deterministic() -> None:
    engine = TemporalSplitEngine()
    rows = [
        {"row_id": f"r{i}", "as_of": _utc(i), "features": {"return_1": "0.1"}}
        for i in range(10)
    ]
    with pytest.raises(ValueError, match=QuarantineReason.SPLIT_LEAKAGE.value):
        bad = replace(_split_config(), split_strategy="random")
        engine.split(rows=rows, config=bad)

    split_one = engine.split(rows=rows, config=_split_config())
    split_two = engine.split(rows=list(reversed(rows)), config=_split_config())
    assert split_one.split_hash == split_two.split_hash
    assert len(split_one.train) == 3
    assert len(split_one.validation) == 2
    assert len(split_one.test) == 2


def test_label_horizon_crossing_rejected_and_embargoed_split_passes() -> None:
    engine = TemporalSplitEngine()
    rows = [
        {"row_id": f"r{i}", "as_of": _utc(i), "features": {"return_1": "0.1"}}
        for i in range(10)
    ]
    with pytest.raises(ValueError, match=QuarantineReason.LABEL_HORIZON_LEAKAGE.value):
        engine.split(rows=rows, config=_split_config(label_horizon_bars=3, embargo_bars=1))

    accepted = engine.split(rows=rows, config=_split_config(label_horizon_bars=1, embargo_bars=1))
    assert accepted.manifest["label_horizon_bars"] == 1
    assert accepted.manifest["embargo_bars"] == 1


@pytest.mark.asyncio
async def test_split_manifest_persisted_with_counts_and_hash(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        builder = ReproducibleSnapshotBuilder(session)
        result = await builder.build_from_records(
            snapshot_input=_snapshot_input(dataset_id="builder-split", version=1),
            series_key=_series_key(),
            records=[_record(i) for i in range(10)],
            as_of_time=_utc(9),
            ingestion_finished_at=_utc(9),
        )
        manifest = await builder.create_split_manifest(
            snapshot=result.snapshot,
            matrix_rows=result.matrix_rows,
            config=_split_config(),
        )
        assert manifest.split_strategy == "temporal"
        assert manifest.train_count == 3
        assert manifest.validation_count == 2
        assert manifest.test_count == 2
        assert manifest.split_hash
        assert manifest.manifest["counts"]["train"] == 3


@pytest.mark.asyncio
async def test_synthetic_records_excluded_from_snapshot_builder(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        builder = ReproducibleSnapshotBuilder(session)
        result = await builder.build_from_records(
            snapshot_input=_snapshot_input(dataset_id="builder-synthetic", version=1),
            series_key=_series_key(),
            records=[_record(0, source="seed:synthetic")],
            as_of_time=_utc(9),
            ingestion_finished_at=_utc(9),
        )
        assert result.snapshot.status == "quarantined"
        rows = await builder._datasets.list_quarantine(result.snapshot.id)  # noqa: SLF001
        assert rows[0].reason_code == QuarantineReason.SYNTHETIC_SOURCE_NOT_AUTHORITATIVE.value


def test_snapshot_builder_code_does_not_emit_symbol_identity_matrix_fields() -> None:
    root = Path(__file__).resolve().parents[1] / "app" / "ml" / "dataset"
    text = (root / "snapshot_builder.py").read_text(encoding="utf-8")
    assert '"symbol"' not in text
    assert '"provider"' not in text
    assert '"market_class"' not in text
