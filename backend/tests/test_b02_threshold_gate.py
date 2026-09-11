"""B-02 — Substantive-threshold gate tests (BO-B-02 §B-02.2).

Pre-fix expectations (b02_probe_prefix.log): the gate checks report EXISTENCE
only, so every threshold test fails because the new rejection reasons do not
exist; `predict_proba` does not exist on the baseline; the threshold ADR does
not exist.

Post-fix: the gate enforces numeric thresholds and fails closed; a
threshold-passing model (positive machinery proof) promotes; the degenerate
baseline probabilities are labeled.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import pytest

from app.db.models.calibration_report import CalibrationReport
from app.db.models.economic_report import EconomicReport
from app.db.models.experiment import Experiment
from app.db.models.generalization import GeneralizationReport
from app.db.models.model_artifact import ModelArtifact
from app.db.models.validation_report import ValidationReport
from app.ml.models.baseline import MajorityClassBaseline
from app.trading_intelligence.inference.errors import ModelEligibilityError
from app.trading_intelligence.inference.service import GovernedModelEligibilityGate


def _utc(minute: int = 0) -> datetime:
    return datetime(2026, 7, 15, 10, minute, tzinfo=timezone.utc)


FULL_COST_MODEL = {
    "base": [
        {"name": "spread", "value_bps": 1.0},
        {"name": "commission", "value_bps": 1.0},
        {"name": "slippage", "value_bps": 1.0},
        {"name": "latency", "value_bps": 1.0},
        {"name": "liquidity", "value_bps": 1.0},
        {"name": "transaction_costs", "value_bps": 1.0},
    ]
}


async def _model_with_reports(
    session,
    *,
    accuracy: float = 0.72,
    effect: float = 0.22,
    p_value: float = 0.001,
    folds: int = 3,
    test_rows: int = 300,
    ece: float = 0.05,
    brier: float = 0.18,
    economic_verdict: str = "economically_usable",
    net_return_bps: float = 5.0,
    cost_model: dict | None = None,
    holdout_accuracy: float = 0.70,
    metrics: dict | None = None,
) -> tuple[ModelArtifact, list[str]]:
    suffix = uuid4().hex[:8]
    experiment = Experiment(
        experiment_id=f"b02-thr-{suffix}",
        version=1,
        status="approved",
        purpose="B02 threshold fixture",
        hypothesis="threshold gate enforcement",
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
        name=f"b02-model-{suffix}",
        version="1-42",
        status="research_only",
        framework="pure-python-majority-baseline",
        feature_set_version="feature_set.v1",
        metrics={"validation_accuracy": accuracy},
        experiment_id=experiment.experiment_id,
        dataset_snapshot_id="snapshot-id",
        dataset_content_hash="dataset-hash",
        split_manifest_hash="split-hash",
        artifact_hash="artifact-hash",
        research_status="research_only",
        operating_domain={"markets": ["forex"], "timeframes": ["H1"], "regimes": ["trend"]},
        advisory_status="advisory_approved",
    )
    session.add(artifact)
    await session.flush()
    validation = ValidationReport(
        experiment_id=experiment.experiment_id,
        model_artifact_id=artifact.id,
        validation_kind="walk_forward",
        metrics=metrics or {"accuracy": accuracy},
        uncertainty={"confidence_interval": [0.65, 0.79], "bootstrap_distribution": [0.72]},
        fold_results=[
            {"fold": i + 1, "accuracy": accuracy, "test_count": test_rows // folds}
            for i in range(folds)
        ],
        effect_size={"metric": "accuracy_minus_null", "null": 0.5, "value": effect},
        significance={"test": "normal_approx_accuracy_vs_0.5", "p_value": p_value},
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
        brier_score=str(brier),
        expected_calibration_error=str(ece),
        bin_scheme={"bin_count": 10},
        bins=[{"bin": 0, "count": 1, "avg_confidence": 0.5, "observed_rate": 0.5}],
        per_slice={"market_class": {"forex": {"count": 1}}},
        warnings=[],
        base_rate="0.50",
        base_rate_significance={"significant_skill": True},
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
        cost_model=cost_model if cost_model is not None else FULL_COST_MODEL,
        scenario_results={"base": {"net_return_bps": net_return_bps}},
        statistical_conclusion={"verdict": "statistically_positive"},
        economic_conclusion={"verdict": economic_verdict},
        sensitivity_summary={
            "min_net_return_bps": net_return_bps,
            "max_net_return_bps": net_return_bps,
        },
        per_slice={"market_class": {"forex": {"trade_count": 1}}},
        report_hash="economic-hash",
        research_status="research_only",
    )
    session.add(economic)
    await session.flush()
    generalization = GeneralizationReport(
        experiment_id=experiment.experiment_id,
        model_artifact_id=artifact.id,
        trained_on={"markets": ["forex"], "timeframes": ["H1"], "regimes": ["trend"]},
        evaluated_on=[{"market": "crypto", "timeframe": "H1", "regime": "trend"}],
        holdout_results={"aggregate_accuracy": holdout_accuracy},
        operating_domain=artifact.operating_domain,
        unsupported_domain_warnings=[],
        report_hash="generalization-hash",
        research_status="research_only",
    )
    session.add(generalization)
    await session.flush()
    artifact.statistical_report_id = validation.id
    artifact.calibration_report_id = calibration.id
    artifact.economic_report_id = economic.id
    await session.flush()
    return artifact, [accuracy, effect, p_value]


def test_b02_threshold_adr_exists_and_enumerates_gates() -> None:
    doc = Path(__file__).resolve().parents[1] / "docs" / "SUBSTANTIVE_THRESHOLD_FRAMEWORK.md"
    assert doc.is_file(), "substantive-threshold ADR missing"
    text = doc.read_text(encoding="utf-8")
    for gate in ("statistical", "calibration", "economic", "generalization"):
        assert gate in text, f"gate {gate} not defined in threshold ADR"


def test_b02_baseline_probabilities_are_degenerate_and_labeled() -> None:
    model = MajorityClassBaseline(seed=42)
    model.fit([1, 1, 0])
    proba = model.predict_proba([{"x": 1.0}, {"x": 2.0}])
    assert len(proba) == 2
    first = proba[0]
    assert abs(first["class_0"] - 1 / 3) < 1e-9
    assert abs(first["class_1"] - 2 / 3) < 1e-9
    assert first["degenerate_prior"] is True


@pytest.mark.asyncio
async def test_b02_statistical_threshold_not_met(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        artifact, _ = await _model_with_reports(
            session, accuracy=0.51, effect=0.01, p_value=0.4, folds=1, test_rows=5
        )
        decision = await GovernedModelEligibilityGate(session).evaluate(artifact)
        assert not decision.eligible
        assert "STATISTICAL_THRESHOLD_NOT_MET" in decision.reasons


@pytest.mark.asyncio
async def test_b02_calibration_threshold_not_met(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        artifact, _ = await _model_with_reports(session, ece=0.2, brier=0.3)
        decision = await GovernedModelEligibilityGate(session).evaluate(artifact)
        assert "CALIBRATION_THRESHOLD_NOT_MET" in decision.reasons


@pytest.mark.asyncio
async def test_b02_economic_not_usable(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        artifact, _ = await _model_with_reports(
            session, economic_verdict="economically_unusable", net_return_bps=-3.0
        )
        decision = await GovernedModelEligibilityGate(session).evaluate(artifact)
        assert "ECONOMIC_NOT_USABLE" in decision.reasons


@pytest.mark.asyncio
async def test_b02_generalization_threshold_not_met(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        # in-domain accuracy 0.72, holdout 0.55 -> degradation 0.17 > 0.10
        artifact, _ = await _model_with_reports(session, holdout_accuracy=0.55)
        decision = await GovernedModelEligibilityGate(session).evaluate(artifact)
        assert "GENERALIZATION_THRESHOLD_NOT_MET" in decision.reasons


@pytest.mark.asyncio
async def test_b02_malformed_report_fails_closed(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        artifact, _ = await _model_with_reports(session, metrics={"nothing": 0.0})
        decision = await GovernedModelEligibilityGate(session).evaluate(artifact)
        assert not decision.eligible
        assert "STATISTICAL_THRESHOLD_NOT_MET" in decision.reasons


@pytest.mark.asyncio
async def test_b02_gate_passes_all_thresholds_and_promotes(prepared_db: None) -> None:
    """Positive machinery proof: a model whose reports genuinely pass every
    numeric threshold is eligible and promotable — the gate is threshold
    driven, not permanently closed."""
    from app.db.session import session_scope

    async with session_scope() as session:
        artifact, _ = await _model_with_reports(session)
        artifact.advisory_status = "research_only"
        await session.flush()
        gate = GovernedModelEligibilityGate(session)
        decision = await gate.evaluate(artifact)
        assert decision.eligible is False  # not yet approved
        assert "NOT_ADVISORY_APPROVED" in decision.reasons
        assert not [r for r in decision.reasons if "THRESHOLD" in r or r == "ECONOMIC_NOT_USABLE"]
        promoted = await gate.promote_to_advisory_approved(
            artifact, approver="b02-test-approver", approval_reason="threshold machinery proof"
        )
        assert promoted.advisory_status == "advisory_approved"


@pytest.mark.asyncio
async def test_b02_promotion_blocked_by_thresholds(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        artifact, _ = await _model_with_reports(
            session, accuracy=0.51, effect=0.01, p_value=0.4, folds=1, test_rows=5
        )
        artifact.advisory_status = "research_only"
        await session.flush()
        with pytest.raises(ModelEligibilityError) as excinfo:
            await GovernedModelEligibilityGate(session).promote_to_advisory_approved(
                artifact, approver="b02-approver", approval_reason="should be refused"
            )
        assert "STATISTICAL_THRESHOLD_NOT_MET" in str(excinfo.value)
