"""W2-U07 statistical validation framework tests."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

import pytest

from app.db.models.dataset import DatasetSnapshot
from app.db.models.dataset_split import DatasetSplitManifest
from app.db.models.feature import FeatureRecord
from app.ml.experiments import ExperimentPlanInput, ExperimentRegistryService
from app.ml.models import BaselineModelHarness
from app.ml.validation import (
    MissingUncertaintyError,
    NonTemporalValidationError,
    StatisticalValidationService,
    ValidationConfig,
)


def _utc(minute: int) -> datetime:
    return datetime(2026, 7, 14, 14, 0, tzinfo=timezone.utc) + timedelta(minutes=minute)


async def _model_artifact_fixture(session):  # noqa: ANN001, ANN201
    snapshot = DatasetSnapshot(
        dataset_id="validation-dataset",
        name="Validation dataset",
        version=1,
        market="forex",
        timeframe="M1",
        start_time=_utc(0),
        end_time=_utc(89),
        source="sample:validation.csv",
        feature_version="feature_set.v1",
        quality_score="pass",
        status="frozen",
        content_hash="validation-dataset-hash",
        frozen_at=_utc(89),
        market_scope={"markets": ["forex", "crypto"]},
    )
    session.add(snapshot)
    await session.flush()

    rows: list[FeatureRecord] = []
    for idx in range(90):
        label = 1 if idx % 3 != 0 else 0
        row = FeatureRecord(
            feature_set_version="feature_set.v1",
            provider="internal",
            market_class="forex",
            symbol="EURUSD",
            timeframe="M1",
            as_of=_utc(idx),
            features={
                "return_1": str(Decimal(idx + 1) / Decimal("1000")),
                "range_pct": str(Decimal("0.01")),
                "label_direction": label,
            },
            quality_score="pass",
            source="sample:validation.csv",
            source_dataset_hash=snapshot.content_hash,
        )
        session.add(row)
        rows.append(row)
    await session.flush()

    split = DatasetSplitManifest(
        dataset_snapshot_id=snapshot.id,
        split_id="validation-split-v1",
        split_strategy="temporal",
        label_horizon_bars=1,
        embargo_bars=1,
        train_start=_utc(0),
        train_end=_utc(59),
        validation_start=_utc(61),
        validation_end=_utc(74),
        test_start=_utc(76),
        test_end=_utc(89),
        train_count=60,
        validation_count=14,
        test_count=14,
        split_hash="validation-split-hash",
        manifest={
            "feature_set_version": "feature_set.v1",
            "split_strategy": "temporal",
            "row_ids": {
                "train": [row.id for row in rows[:60]],
                "validation": [row.id for row in rows[61:75]],
                "test": [row.id for row in rows[76:90]],
            },
        },
        quality_summary="validation unit split",
    )
    session.add(split)
    await session.flush()

    registry = ExperimentRegistryService(session)
    plan = ExperimentPlanInput(
        experiment_id="validation-approved-exp",
        version=1,
        purpose="Validation framework unit test",
        hypothesis="Validation report includes uncertainty and temporal folds",
        dataset_snapshot_id=snapshot.id,
        dataset_content_hash=snapshot.content_hash,
        split_manifest_id=split.id,
        split_manifest_hash=split.split_hash,
        feature_set_version="feature_set.v1",
        model_family="pure_python_majority_baseline",
        model_spec={"framework": "pure-python", "seed": 42},
        evaluation_plan={"split_strategy": "temporal", "metrics": ["accuracy"]},
    )
    experiment = await registry.create_draft(plan)
    await registry.pre_register(experiment)
    await registry.approve(experiment, approver="pytest")
    training = await BaselineModelHarness(session).train(
        experiment_id=experiment.experiment_id
    )
    artifact = training.artifact
    validation_rows = [
        {
            "as_of": row.as_of,
            "features": {k: float(v) for k, v in row.features.items() if k != "label_direction"},
            "label": int(row.features["label_direction"]),
        }
        for row in rows
    ]
    return experiment, artifact, validation_rows


@pytest.mark.asyncio
async def test_walk_forward_validation_report_with_uncertainty_persisted(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        experiment, artifact, rows = await _model_artifact_fixture(session)
        report = await StatisticalValidationService(session).validate(
            experiment_id=experiment.experiment_id,
            model_artifact_id=artifact.id,
            rows=rows,
            config=ValidationConfig(train_window=30, test_window=10, step=10, embargo=2),
        )
        assert report.research_status == "research_only"
        assert report.experiment_id == experiment.experiment_id
        assert report.model_artifact_id == artifact.id
        assert "confidence_interval" in report.uncertainty
        assert "bootstrap_distribution" in report.uncertainty
        assert report.effect_size["metric"] == "accuracy_minus_null"
        assert "p_value" in report.significance
        assert report.fold_results
        assert report.report_hash


@pytest.mark.asyncio
async def test_random_cv_and_embargo_violation_refused(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        experiment, artifact, rows = await _model_artifact_fixture(session)
        service = StatisticalValidationService(session)
        with pytest.raises(NonTemporalValidationError, match="NON_TEMPORAL_CV"):
            await service.validate(
                experiment_id=experiment.experiment_id,
                model_artifact_id=artifact.id,
                rows=rows,
                config=ValidationConfig(strategy="random"),
            )
        with pytest.raises(ValueError, match="not enough rows|positive"):
            await service.validate(
                experiment_id=experiment.experiment_id,
                model_artifact_id=artifact.id,
                rows=rows[:5],
                config=ValidationConfig(train_window=20, test_window=10, step=5, embargo=1),
            )


def test_report_without_uncertainty_rejected() -> None:
    service = StatisticalValidationService(session=None)  # type: ignore[arg-type]
    with pytest.raises(MissingUncertaintyError, match="VALIDATION_UNCERTAINTY_MISSING"):
        service.validate_report_contract(
            {
                "metrics": {"accuracy": 0.5},
                "fold_results": [{"accuracy": 0.5}],
                "effect_size": {"value": 0.0},
                "significance": {"p_value": 1.0},
            }
        )


@pytest.mark.asyncio
async def test_seeded_validation_reproducible_same_report_hash(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        experiment, artifact, rows = await _model_artifact_fixture(session)
        service = StatisticalValidationService(session)
        config = ValidationConfig(train_window=30, test_window=10, step=10, embargo=2, seed=7)
        first = await service.validate(
            experiment_id=experiment.experiment_id,
            model_artifact_id=artifact.id,
            rows=rows,
            config=config,
        )
        second = await service.validate(
            experiment_id=experiment.experiment_id,
            model_artifact_id=artifact.id,
            rows=rows,
            config=config,
        )
        assert first.report_hash == second.report_hash
        assert first.metrics == second.metrics
        assert first.uncertainty == second.uncertainty


def test_no_validation_live_signal_or_identity_feature_route_added() -> None:
    api_root = Path(__file__).resolve().parents[1] / "app" / "api" / "routes"
    for path in api_root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "live_signal" not in text
        assert "model/signal" not in text

    validation_root = Path(__file__).resolve().parents[1] / "app" / "ml" / "validation"
    for path in validation_root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "symbol_id" not in text
        assert "one_hot_symbol" not in text
        assert "symbol_identity" not in text
