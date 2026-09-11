"""W2-U10 generalization, registry maturation, and drift tests."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from app.db.models.calibration_report import CalibrationReport
from app.db.models.economic_report import EconomicReport
from app.db.models.experiment import Experiment
from app.db.models.model_artifact import ModelArtifact
from app.db.models.validation_report import ValidationReport
from app.ml.generalization import (
    Domain,
    GeneralizationInput,
    GeneralizationLeakageError,
    GeneralizationService,
)


def _utc(minute: int = 0) -> datetime:
    return datetime(2026, 7, 15, 13, minute, tzinfo=timezone.utc)


async def _artifact_chain(session):  # noqa: ANN001, ANN201
    experiment = Experiment(
        experiment_id="generalization-exp",
        version=1,
        status="approved",
        purpose="generalization unit",
        hypothesis="model may transfer across markets",
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
        name="generalization-model",
        version="1-42",
        status="research_only",
        framework="pure-python-majority-baseline",
        feature_set_version="feature_set.v1",
        metrics={"validation_accuracy": 0.55},
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
        metrics={"accuracy": 0.55},
        uncertainty={
            "confidence_interval": [0.45, 0.65],
            "bootstrap_distribution": [0.45, 0.55, 0.65],
        },
        fold_results=[{"fold": 1, "accuracy": 0.55}],
        effect_size={"value": 0.05},
        significance={"p_value": 0.3},
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
        brier_score="0.24",
        expected_calibration_error="0.10",
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
        cost_model={"base": []},
        scenario_results={"base": {"net_return_bps": -1.0}},
        statistical_conclusion={"verdict": "statistically_positive"},
        economic_conclusion={"verdict": "economically_unusable"},
        sensitivity_summary={"min_net_return_bps": -1.0, "max_net_return_bps": -1.0},
        per_slice={"market_class": {"forex": {"trade_count": 1}}},
        report_hash="economic-hash",
        research_status="research_only",
    )
    session.add(economic)
    await session.flush()
    return experiment, artifact, validation, calibration, economic


@pytest.mark.asyncio
async def test_trained_on_x_evaluated_on_y_generalization_report(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        _, artifact, *_ = await _artifact_chain(session)
        report = await GeneralizationService(session).create_report(
            experiment_id="generalization-exp",
            model_artifact_id=artifact.id,
            trained_on=Domain(markets=("forex",), timeframes=("M1",), regimes=("trend",)),
            evaluated_on=[
                GeneralizationInput(
                    market="crypto", timeframe="M1", regime="trend", accuracy=0.52, sample_count=40
                ),
                GeneralizationInput(
                    market="synthetic",
                    timeframe="M1",
                    regime="range",
                    accuracy=0.48,
                    sample_count=35,
                ),
            ],
            operating_domain=Domain(
                markets=("forex", "crypto"), timeframes=("M1",), regimes=("trend",)
            ),
        )
        assert report.research_status == "research_only"
        assert report.trained_on["markets"] == ["forex"]
        assert {item["market"] for item in report.evaluated_on} == {"crypto", "synthetic"}
        assert report.holdout_results["aggregate_accuracy"] is not None
        assert report.report_hash


@pytest.mark.asyncio
async def test_market_holdout_overlap_refused(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        _, artifact, *_ = await _artifact_chain(session)
        with pytest.raises(GeneralizationLeakageError, match="MARKET_HOLDOUT_LEAKAGE"):
            await GeneralizationService(session).create_report(
                experiment_id="generalization-exp",
                model_artifact_id=artifact.id,
                trained_on=Domain(markets=("forex",), timeframes=("M1",), regimes=("trend",)),
                evaluated_on=[
                    GeneralizationInput(
                        market="forex",
                        timeframe="M1",
                        regime="trend",
                        accuracy=0.5,
                        sample_count=10,
                    )
                ],
                operating_domain=Domain(markets=("forex",), timeframes=("M1",), regimes=("trend",)),
            )


def test_operating_domain_warning_pair() -> None:
    service = GeneralizationService(session=None)  # type: ignore[arg-type]
    domain = Domain(markets=("forex",), timeframes=("M1",), regimes=("trend",))
    assert service.domain_warning(domain, market="forex", timeframe="M1", regime="trend") is None
    warning = service.domain_warning(domain, market="crypto", timeframe="M1", regime="trend")
    assert warning is not None
    assert warning["warning"] == "UNSUPPORTED_DOMAIN"


@pytest.mark.asyncio
async def test_model_registry_matured_with_report_links_and_domain(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        _, artifact, validation, calibration, economic = await _artifact_chain(session)
        matured = await GeneralizationService(session).mature_registry_entry(
            model_artifact_id=artifact.id,
            statistical_report_id=validation.id,
            calibration_report_id=calibration.id,
            economic_report_id=economic.id,
            operating_domain=Domain(markets=("forex",), timeframes=("M1",), regimes=("trend",)),
            approval_note="research validated for forex M1 trend only",
        )
        assert matured.statistical_report_id == validation.id
        assert matured.calibration_report_id == calibration.id
        assert matured.economic_report_id == economic.id
        assert matured.operating_domain["markets"] == ["forex"]
        assert matured.research_status == "research_only"


@pytest.mark.asyncio
async def test_drift_signal_does_not_auto_retrain(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        _, artifact, *_ = await _artifact_chain(session)
        record = await GeneralizationService(session).record_drift_signal(
            model_artifact_id=artifact.id,
            drift_kind="feature_drift",
            window_start=_utc(0),
            window_end=_utc(10),
            signals={"drift_detected": True, "psi": 0.35},
            auto_retrain_requested=True,
        )
        assert record.drift_detected is True
        assert record.auto_retrain_requested is True
        assert record.retrain_triggered is False
        assert record.governance_required is True
        GeneralizationService(session).assert_no_auto_retrain(record)


@pytest.mark.asyncio
async def test_generalization_report_reproducible_same_hash(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        _, artifact, *_ = await _artifact_chain(session)
        kwargs = {
            "experiment_id": "generalization-exp",
            "model_artifact_id": artifact.id,
            "trained_on": Domain(markets=("forex",), timeframes=("M1",), regimes=("trend",)),
            "evaluated_on": [
                GeneralizationInput(
                    market="crypto", timeframe="M1", regime="trend", accuracy=0.52, sample_count=40
                )
            ],
            "operating_domain": Domain(
                markets=("forex", "crypto"), timeframes=("M1",), regimes=("trend",)
            ),
        }
        first = await GeneralizationService(session).create_report(**kwargs)
        second = await GeneralizationService(session).create_report(**kwargs)
        assert first.report_hash == second.report_hash


def test_no_identity_live_signal_or_auto_retrain_loop_added() -> None:
    root = Path(__file__).resolve().parents[1] / "app" / "ml" / "generalization"
    forbidden = ("symbol_id", "one_hot_symbol", "symbol_identity")
    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for needle in forbidden:
            assert needle not in text
    api_root = Path(__file__).resolve().parents[1] / "app" / "api" / "routes"
    for path in api_root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "live_signal" not in text
        assert "auto_retrain" not in text
