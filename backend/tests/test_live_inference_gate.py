"""W3-U01 live inference engine and governed eligibility gate tests."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path
from uuid import uuid4

import pytest

from app.db.models.calibration_report import CalibrationReport
from app.db.models.economic_report import EconomicReport
from app.db.models.experiment import Experiment
from app.db.models.generalization import GeneralizationReport
from app.db.models.model_artifact import ModelArtifact
from app.db.models.validation_report import ValidationReport
from app.trading_intelligence.inference import (
    GovernedModelEligibilityGate,
    InferenceInput,
    InferenceInputError,
    LiveInferenceEngine,
    ModelEligibilityError,
)


def _utc(minute: int = 0) -> datetime:
    return datetime(2026, 7, 14, 15, 0, tzinfo=timezone.utc) + timedelta(minutes=minute)


def _input(**overrides) -> InferenceInput:  # noqa: ANN003, ANN201
    data = {
        "as_of_time": _utc(1),
        "feature_set_version": "feature_set.v1",
        "features": {"return_1": Decimal("0.01"), "range_pct": Decimal("0.02")},
        "market_class": "forex",
        "provider": "internal",
        "symbol": "EURUSD",
        "timeframe": "M1",
        "regime": "trend",
        "source": "live:simulated",
    }
    data.update(overrides)
    return InferenceInput(**data)


async def _eligible_artifact(session):  # noqa: ANN001, ANN201
    suffix = uuid4().hex[:8]
    experiment_id = f"w3-eligible-exp-{suffix}"
    experiment = Experiment(
        experiment_id=experiment_id,
        version=1,
        status="approved",
        purpose="W3 eligibility fixture",
        hypothesis="governed model may be advisory approved",
        dataset_snapshot_id="snapshot-id",
        dataset_content_hash="dataset-hash",
        split_manifest_id="split-id",
        split_manifest_hash="split-hash",
        feature_set_version="feature_set.v1",
        model_family="pure_python_majority_baseline",
        model_spec={"framework": "pure-python"},
        evaluation_plan={"split_strategy": "temporal"},
        approval_timestamp=_utc(0),
        approver="pytest",
        plan_hash="plan-hash",
    )
    session.add(experiment)
    await session.flush()
    artifact = ModelArtifact(
        name="w3-eligible-model",
        version="1-42",
        status="research_only",
        framework="pure-python-majority-baseline",
        feature_set_version="feature_set.v1",
        metrics={"validation_accuracy": 0.72},
        experiment_id=experiment.experiment_id,
        dataset_snapshot_id="snapshot-id",
        dataset_content_hash="dataset-hash",
        split_manifest_hash="split-hash",
        artifact_hash="artifact-hash",
        research_status="research_only",
        statistical_report_id=None,
        calibration_report_id=None,
        economic_report_id=None,
        operating_domain={"markets": ["forex"], "timeframes": ["M1"], "regimes": ["trend"]},
        advisory_status="research_only",
    )
    session.add(artifact)
    await session.flush()
    # BO-B-02: fixture reports must genuinely pass the substantive thresholds
    # (SUBSTANTIVE_THRESHOLD_FRAMEWORK.md) — promotion success is now
    # threshold-gated, not merely lineage-gated.
    validation = ValidationReport(
        experiment_id=experiment.experiment_id,
        model_artifact_id=artifact.id,
        validation_kind="walk_forward",
        metrics={"accuracy": 0.72},
        uncertainty={
            "confidence_interval": [0.65, 0.79],
            "bootstrap_distribution": [0.65, 0.72, 0.79],
        },
        fold_results=[
            {"fold": 1, "accuracy": 0.72, "test_count": 150},
            {"fold": 2, "accuracy": 0.72, "test_count": 150},
            {"fold": 3, "accuracy": 0.72, "test_count": 150},
        ],
        effect_size={"value": 0.22},
        significance={"p_value": 0.001},
        config={"strategy": "walk_forward"},
        report_hash="validation-hash",
        research_status="research_only",
    )
    session.add(validation)
    await session.flush()
    calibration = CalibrationReport(
        experiment_id=experiment.experiment_id,
        model_artifact_id=artifact.id,
        validation_report_id=validation.id,
        brier_score="0.18",
        expected_calibration_error="0.05",
        bin_scheme={"bin_count": 10},
        bins=[{"bin": 0, "count": 1, "avg_confidence": 0.5, "observed_rate": 0.5}],
        per_slice={"market_class": {"forex": {"count": 1}}},
        warnings=[],
        base_rate="0.50",
        base_rate_significance={"significant_skill": False},
        config={"bin_count": 10},
        report_hash="calibration-hash",
        research_status="research_only",
    )
    session.add(calibration)
    await session.flush()
    economic = EconomicReport(
        experiment_id=experiment.experiment_id,
        model_artifact_id=artifact.id,
        validation_report_id=validation.id,
        calibration_report_id=calibration.id,
        cost_model={
            "base": [
                {"name": "spread", "value_bps": 1.0},
                {"name": "commission", "value_bps": 1.0},
                {"name": "slippage", "value_bps": 1.0},
                {"name": "latency", "value_bps": 1.0},
                {"name": "liquidity", "value_bps": 1.0},
                {"name": "transaction_costs", "value_bps": 1.0},
            ]
        },
        scenario_results={"base": {"net_return_bps": 5.0}},
        statistical_conclusion={"verdict": "statistically_positive"},
        economic_conclusion={"verdict": "economically_usable"},
        sensitivity_summary={"min_net_return_bps": 5.0, "max_net_return_bps": 5.0},
        per_slice={"market_class": {"forex": {"trade_count": 1}}},
        report_hash="economic-hash",
        research_status="research_only",
    )
    session.add(economic)
    await session.flush()
    artifact.statistical_report_id = validation.id
    artifact.calibration_report_id = calibration.id
    artifact.economic_report_id = economic.id
    await session.flush()
    generalization = GeneralizationReport(
        experiment_id=experiment.experiment_id,
        model_artifact_id=artifact.id,
        trained_on={"markets": ["forex"], "timeframes": ["M1"], "regimes": ["trend"]},
        evaluated_on=[{"market": "crypto", "timeframe": "M1", "regime": "trend"}],
        holdout_results={"aggregate_accuracy": 0.70},
        operating_domain=artifact.operating_domain,
        unsupported_domain_warnings=[],
        report_hash="generalization-hash",
        research_status="research_only",
    )
    session.add(generalization)
    await session.flush()
    return artifact


@pytest.mark.asyncio
async def test_deterministic_inference_same_input_same_score_and_hash(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        artifact = await _eligible_artifact(session)
        gate = GovernedModelEligibilityGate(session)
        await gate.promote_to_advisory_approved(
            artifact, approver="ITRGA-test", approval_reason="unit test approval"
        )
        engine = LiveInferenceEngine(session)
        first = await engine.score(model=artifact, inference_input=_input())
        second = await engine.score(model=artifact, inference_input=_input())
        assert first.score == second.score
        assert first.inference_input_hash == second.inference_input_hash
        assert first.deterministic is True


@pytest.mark.asyncio
async def test_eligibility_refusals_by_reason(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        artifact = await _eligible_artifact(session)
        gate = GovernedModelEligibilityGate(session)
        decision = await gate.evaluate(artifact, _input())
        assert "NOT_ADVISORY_APPROVED" in decision.reasons

        artifact.statistical_report_id = None
        decision = await gate.evaluate(artifact, _input())
        assert "MISSING_STATISTICAL_REPORT" in decision.reasons
        artifact.statistical_report_id = "missing-stat"
        artifact.calibration_report_id = None
        decision = await gate.evaluate(artifact, _input())
        assert "MISSING_CALIBRATION_REPORT" in decision.reasons
        artifact.calibration_report_id = "missing-cal"
        artifact.economic_report_id = None
        decision = await gate.evaluate(artifact, _input())
        assert "MISSING_ECONOMIC_REPORT" in decision.reasons
        artifact.economic_report_id = "missing-econ"
        from sqlalchemy import delete

        from app.db.models.generalization import GeneralizationReport

        await session.execute(
            delete(GeneralizationReport).where(
                GeneralizationReport.model_artifact_id == artifact.id
            )
        )
        await session.flush()
        decision = await gate.evaluate(artifact, _input())
        assert "MISSING_GENERALIZATION_REPORT" in decision.reasons


@pytest.mark.asyncio
async def test_governed_promotion_refused_without_lineage_and_audited_on_success(
    prepared_db: None,
) -> None:
    from sqlalchemy import select

    from app.db.models.audit import AuditEvent
    from app.db.session import session_scope

    async with session_scope() as session:
        artifact = await _eligible_artifact(session)
        gate = GovernedModelEligibilityGate(session)
        artifact.economic_report_id = None
        with pytest.raises(ModelEligibilityError, match="PROMOTION_LINEAGE_INCOMPLETE"):
            await gate.promote_to_advisory_approved(
                artifact, approver="ITRGA-test", approval_reason="should fail"
            )

        artifact = await _eligible_artifact(session)
        with pytest.raises(ModelEligibilityError, match="ADVISORY_APPROVER_REQUIRED"):
            await gate.promote_to_advisory_approved(
                artifact, approver="", approval_reason="missing approver"
            )
        await gate.promote_to_advisory_approved(
            artifact, approver="ITRGA-test", approval_reason="unit test approval"
        )
        assert artifact.advisory_status == "advisory_approved"
        assert artifact.advisory_approved_at is not None
        result = await session.execute(
            select(AuditEvent.action).where(AuditEvent.resource_type == "model_artifact")
        )
        assert "model.advisory_approved" in {row[0] for row in result.all()}


@pytest.mark.asyncio
async def test_identity_out_of_domain_future_and_synthetic_inputs_refused(
    prepared_db: None,
) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        artifact = await _eligible_artifact(session)
        gate = GovernedModelEligibilityGate(session)
        await gate.promote_to_advisory_approved(
            artifact, approver="ITRGA-test", approval_reason="unit test approval"
        )
        with pytest.raises(InferenceInputError, match="IDENTITY_IN_INFERENCE_INPUT"):
            gate.validate_inference_input(artifact, _input(features={"symbol": "EURUSD"}))
        with pytest.raises(InferenceInputError, match="UNSUPPORTED_DOMAIN"):
            gate.validate_inference_input(artifact, _input(market_class="crypto"))
        with pytest.raises(InferenceInputError, match="FUTURE_INFERENCE_INPUT"):
            gate.validate_inference_input(artifact, _input(as_of_time=_utc(999999)))
        with pytest.raises(InferenceInputError, match="SYNTHETIC_AUTHORITATIVE_INPUT_REFUSED"):
            gate.validate_inference_input(artifact, _input(source="seed:synthetic"))
        with pytest.raises(InferenceInputError, match="FEATURE_VERSION_MISMATCH"):
            gate.validate_inference_input(artifact, _input(feature_set_version="wrong"))


def test_no_execution_signal_or_broker_path_in_inference_modules() -> None:
    root = Path(__file__).resolve().parents[1] / "app" / "trading_intelligence" / "inference"
    forbidden = ("place_order", "cancel_order", "broker.", "live_signal", "emit_signal")
    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for needle in forbidden:
            assert needle not in text

    api_root = Path(__file__).resolve().parents[1] / "app" / "api" / "routes"
    for path in api_root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "live_signal" not in text
        assert "emit_signal" not in text
