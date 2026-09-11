"""W2-U09 economic validation framework tests."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from app.db.models.calibration_report import CalibrationReport
from app.db.models.experiment import Experiment
from app.db.models.model_artifact import ModelArtifact
from app.db.models.validation_report import ValidationReport
from app.ml.economic import (
    CostInput,
    CostInputInvalidError,
    CostProvenance,
    CostScenario,
    EconomicReportInvalidError,
    EconomicValidationService,
    HypotheticalTrade,
)


def _utc() -> datetime:
    return datetime(2026, 7, 15, 10, 0, tzinfo=timezone.utc)


def _scenario(name: str, multiplier: float = 1.0) -> CostScenario:
    def assumed(cost_name: str, value: float) -> CostInput:
        return CostInput(
            name=cost_name,
            value_bps=value * multiplier,
            provenance=CostProvenance.ASSUMED,
            low_bps=value * multiplier * 0.5,
            high_bps=value * multiplier * 1.5,
            detail="unit-test assumed range",
        )

    return CostScenario(
        name=name,
        costs=[
            assumed("spread", 1.0),
            assumed("commission", 0.5),
            assumed("slippage", 1.0),
            assumed("latency", 0.5),
            assumed("liquidity", 0.5),
            assumed("transaction_costs", 0.5),
        ],
    )


def _trades(gross_bps: float = 2.0) -> list[HypotheticalTrade]:
    return [
        HypotheticalTrade(
            gross_return_bps=gross_bps,
            market_class="forex",
            timeframe="M1",
            regime="mixed",
        )
        for _ in range(10)
    ]


async def _pins(session):  # noqa: ANN001, ANN201
    experiment = Experiment(
        experiment_id="economic-exp",
        version=1,
        status="approved",
        purpose="economic validation unit",
        hypothesis="statistical positive may be economically negative",
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
        name="economic-model",
        version="1-42",
        status="research_only",
        framework="pure-python-majority-baseline",
        feature_set_version="feature_set.v1",
        metrics={"validation_accuracy": 0.6},
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
        metrics={"accuracy": 0.6},
        uncertainty={
            "confidence_interval": [0.55, 0.65],
            "bootstrap_distribution": [0.55, 0.6, 0.65],
        },
        fold_results=[{"fold": 1, "accuracy": 0.6}],
        effect_size={"value": 0.1},
        significance={"p_value": 0.04},
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
        brier_score="0.2",
        expected_calibration_error="0.1",
        bin_scheme={"bin_count": 10},
        bins=[{"bin": 0, "count": 1, "avg_confidence": 0.5, "observed_rate": 0.5}],
        per_slice={"market_class": {"forex": {"count": 1}}},
        warnings=[],
        base_rate="0.5",
        base_rate_significance={"significant_skill": True},
        config={"bin_count": 10},
        report_hash="calibration-hash",
        research_status="research_only",
    )
    session.add(calibration)
    await session.flush()
    return experiment, artifact, validation, calibration


def test_cost_model_requires_provenance_and_sensitivity() -> None:
    with pytest.raises(CostInputInvalidError, match="ASSUMED_COST_REQUIRES_SENSITIVITY"):
        CostInput("spread", 1.0, CostProvenance.ASSUMED).validate()

    scenario = _scenario("base")
    scenario.validate()
    payload = EconomicValidationService(session=None).build_payload(  # type: ignore[arg-type]
        trades=_trades(),
        statistical_conclusion={"verdict": "statistically_positive", "metric": "accuracy"},
        scenarios=[scenario],
    )
    assert payload["cost_model"]["base"]
    assert all("provenance" in item for item in payload["cost_model"]["base"])


def test_statistically_positive_but_economically_negative_reported_separately() -> None:
    payload = EconomicValidationService(session=None).build_payload(  # type: ignore[arg-type]
        trades=_trades(gross_bps=2.0),
        statistical_conclusion={"verdict": "statistically_positive", "accuracy": 0.6},
        scenarios=[_scenario("base", multiplier=1.0)],
    )
    assert payload["statistical_conclusion"]["verdict"] == "statistically_positive"
    assert payload["economic_conclusion"]["verdict"] == "economically_unusable"
    assert (
        payload["economic_conclusion"]["headline"] == "STATISTICALLY_POSITIVE_ECONOMICALLY_NEGATIVE"
    )


def test_conflated_or_undeclared_cost_report_rejected() -> None:
    service = EconomicValidationService(session=None)  # type: ignore[arg-type]
    with pytest.raises(EconomicReportInvalidError, match="CONFLATED"):
        service.validate_report_contract(
            {
                "statistical_conclusion": {"same": True},
                "economic_conclusion": {"same": True},
                "scenario_results": {"base": {"net_return_bps": 1}},
                "cost_model": {
                    "base": [
                        {"name": "spread", "provenance": "assumed", "low_bps": 1, "high_bps": 2}
                    ]
                },
            }
        )
    with pytest.raises(CostInputInvalidError, match="UNDECLARED_COST_PROVENANCE"):
        service.validate_report_contract(
            {
                "statistical_conclusion": {"verdict": "statistically_positive"},
                "economic_conclusion": {"verdict": "economically_unusable"},
                "scenario_results": {"base": {"net_return_bps": -1}},
                "cost_model": {"base": [{"name": "spread"}]},
            }
        )


def test_scenario_sensitivity_and_per_slice() -> None:
    payload = EconomicValidationService(session=None).build_payload(  # type: ignore[arg-type]
        trades=_trades(gross_bps=8.0),
        statistical_conclusion={"verdict": "statistically_positive"},
        scenarios=[
            _scenario("optimistic", 0.5),
            _scenario("base", 1.0),
            _scenario("pessimistic", 2.0),
        ],
    )
    assert set(payload["scenario_results"]) == {"optimistic", "base", "pessimistic"}
    assert (
        payload["sensitivity_summary"]["max_net_return_bps"]
        > payload["sensitivity_summary"]["min_net_return_bps"]
    )
    assert payload["per_slice"]["market_class"]["forex"]["trade_count"] == 10


@pytest.mark.asyncio
async def test_economic_report_persisted_and_reproducible(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        experiment, artifact, validation, calibration = await _pins(session)
        service = EconomicValidationService(session)
        kwargs = {
            "experiment_id": experiment.experiment_id,
            "model_artifact_id": artifact.id,
            "validation_report_id": validation.id,
            "calibration_report_id": calibration.id,
            "trades": _trades(gross_bps=2.0),
            "statistical_conclusion": {"verdict": "statistically_positive"},
            "scenarios": [_scenario("base")],
        }
        first = await service.validate(**kwargs)
        second = await service.validate(**kwargs)
        assert first.report_hash == second.report_hash
        assert first.research_status == "research_only"
        assert first.economic_conclusion["verdict"] == "economically_unusable"


def test_no_execution_or_live_signal_added_by_economic_validation() -> None:
    economic_root = Path(__file__).resolve().parents[1] / "app" / "ml" / "economic"
    forbidden = ("place_order", "cancel_order", "broker.", "broker ", "live_signal")
    for path in economic_root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for needle in forbidden:
            assert needle not in text

    api_root = Path(__file__).resolve().parents[1] / "app" / "api" / "routes"
    for path in api_root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "live_signal" not in text
        assert "place_order" not in text
        assert "cancel_order" not in text
