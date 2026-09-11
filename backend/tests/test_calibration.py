"""W2-U08 calibration and probability-quality tests."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from app.db.models.experiment import Experiment
from app.db.models.model_artifact import ModelArtifact
from app.db.models.validation_report import ValidationReport
from app.ml.calibration import (
    CalibrationConfig,
    CalibrationReportInvalidError,
    CalibrationService,
    ProbabilityObservation,
)


def _utc() -> datetime:
    return datetime(2026, 7, 14, 16, 0, tzinfo=timezone.utc)


def _well_calibrated() -> list[ProbabilityObservation]:
    low = [
        ProbabilityObservation(
            probability=0.1, label=0, market_class="forex", timeframe="M1", regime="quiet"
        )
        for _ in range(9)
    ]
    high = [
        ProbabilityObservation(
            probability=0.9, label=1, market_class="crypto", timeframe="M1", regime="trend"
        )
        for _ in range(9)
    ]
    return [
        *low,
        ProbabilityObservation(
            probability=0.1, label=1, market_class="forex", timeframe="M1", regime="quiet"
        ),
        *high,
        ProbabilityObservation(
            probability=0.9, label=0, market_class="crypto", timeframe="M1", regime="trend"
        ),
    ]


def _miscalibrated() -> list[ProbabilityObservation]:
    return [
        ProbabilityObservation(
            probability=0.9,
            label=(1 if i % 2 == 0 else 0),
            market_class="forex",
            timeframe="M1",
            regime="mixed",
        )
        for i in range(20)
    ]


def test_miscalibrated_fixture_flagged_and_well_calibrated_not_flagged() -> None:
    service = CalibrationService(session=None)  # type: ignore[arg-type]
    config = CalibrationConfig(bin_count=10, warning_threshold_ece=0.15)
    bad = service.build_payload(observations=_miscalibrated(), config=config)
    good = service.build_payload(observations=_well_calibrated(), config=config)
    assert "POORLY_CALIBRATED" in bad["warnings"]
    assert "POORLY_CALIBRATED" not in good["warnings"]
    assert bad["brier_score"] > good["brier_score"]
    assert bad["expected_calibration_error"] > config.warning_threshold_ece


def test_calibration_curve_brier_ece_and_per_slice_shape() -> None:
    service = CalibrationService(session=None)  # type: ignore[arg-type]
    payload = service.build_payload(observations=_well_calibrated(), config=CalibrationConfig())
    assert "brier_score" in payload
    assert "expected_calibration_error" in payload
    assert len(payload["bins"]) == 10
    assert payload["per_slice"]["market_class"]["forex"]["count"] == 10
    assert payload["per_slice"]["market_class"]["crypto"]["count"] == 10
    assert payload["per_slice"]["regime"]["quiet"]["count"] == 10


def test_base_rate_null_majority_baseline_not_significant_skill() -> None:
    service = CalibrationService(session=None)  # type: ignore[arg-type]
    labels = [1] * 8 + [0] * 2
    predictions = [1] * 10
    result = service.base_rate_significance(predictions=predictions, labels=labels)
    assert result["base_rate"] == 0.8
    assert result["accuracy"] == 0.8
    assert result["skill_over_base_rate"] == 0.0
    assert result["significant_skill"] is False


def test_calibration_report_without_bins_uncertainty_rejected() -> None:
    service = CalibrationService(session=None)  # type: ignore[arg-type]
    with pytest.raises(CalibrationReportInvalidError, match="CALIBRATION"):
        service.validate_report_contract(
            {
                "brier_score": 0.1,
                "expected_calibration_error": 0.1,
                "bin_scheme": {"bin_count": 10},
                "per_slice": {},
                "base_rate": 0.5,
                "base_rate_significance": {"significant_skill": False},
            }
        )


async def _pins(session):  # noqa: ANN001, ANN201
    experiment = Experiment(
        experiment_id="calibration-exp",
        version=1,
        status="approved",
        purpose="calibration unit",
        hypothesis="calibration report persists",
        dataset_snapshot_id="snapshot-id",
        dataset_content_hash="dataset-hash",
        split_manifest_id="split-id",
        split_manifest_hash="split-hash",
        feature_set_version="feature_set.v1",
        model_family="pure_python_majority_baseline",
        model_spec={"framework": "pure-python"},
        evaluation_plan={"split_strategy": "temporal"},
        approval_timestamp=_utc(),
        approver="pytest",
        plan_hash="plan-hash",
    )
    session.add(experiment)
    await session.flush()
    artifact = ModelArtifact(
        name="calibration-model",
        version="1-42",
        status="research_only",
        framework="pure-python-majority-baseline",
        feature_set_version="feature_set.v1",
        metrics={"validation_accuracy": 0.5},
        experiment_id=experiment.experiment_id,
        dataset_snapshot_id="snapshot-id",
        dataset_content_hash="dataset-hash",
        split_manifest_hash="split-hash",
        artifact_hash="artifact-hash",
        research_status="research_only",
    )
    session.add(artifact)
    await session.flush()
    validation = ValidationReport(
        experiment_id=experiment.experiment_id,
        model_artifact_id=artifact.id,
        validation_kind="walk_forward",
        metrics={"accuracy": 0.5},
        uncertainty={"confidence_interval": [0.4, 0.6], "bootstrap_distribution": [0.4, 0.5, 0.6]},
        fold_results=[{"fold": 1, "accuracy": 0.5}],
        effect_size={"value": 0.0},
        significance={"p_value": 1.0},
        config={"strategy": "walk_forward"},
        report_hash="validation-hash",
        research_status="research_only",
    )
    session.add(validation)
    await session.flush()
    return experiment, artifact, validation


@pytest.mark.asyncio
async def test_calibration_report_persisted_and_reproducible(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        experiment, artifact, validation = await _pins(session)
        service = CalibrationService(session)
        first = await service.calibrate(
            experiment_id=experiment.experiment_id,
            model_artifact_id=artifact.id,
            validation_report_id=validation.id,
            observations=_well_calibrated(),
            config=CalibrationConfig(seed=7),
        )
        second = await service.calibrate(
            experiment_id=experiment.experiment_id,
            model_artifact_id=artifact.id,
            validation_report_id=validation.id,
            observations=_well_calibrated(),
            config=CalibrationConfig(seed=7),
        )
        assert first.report_hash == second.report_hash
        assert first.research_status == "research_only"
        assert first.bins
        assert first.per_slice["market_class"]["forex"]["count"] == 10


def test_no_identity_or_live_signal_added_by_calibration() -> None:
    calibration_root = Path(__file__).resolve().parents[1] / "app" / "ml" / "calibration"
    for path in calibration_root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "symbol_id" not in text
        assert "one_hot_symbol" not in text
        assert "symbol_identity" not in text
    api_root = Path(__file__).resolve().parents[1] / "app" / "api" / "routes"
    for path in api_root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "live_signal" not in text
        assert "model/signal" not in text
