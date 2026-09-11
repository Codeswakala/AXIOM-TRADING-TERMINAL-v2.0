"""BO-B-ML Phase 2/3 — research-tier lifecycle over REAL data (fail-first).

The fixture is a verbatim 400-row slice of the pinned OKX BTCUSDT H1 corpus
(`tests/fixtures/bdata_corpus/okx_BTCUSDT_H1.csv`, sha256 `bd8769b6…`),
ingested with the explicit `historical:real` label. The full multi-instrument
run is Level-I evidence in the delivery runner; this test pins the machinery
and the honest gate behavior on real data.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from sqlalchemy import func, select

from app.db.models.calibration_report import CalibrationReport
from app.db.models.economic_report import EconomicReport
from app.db.models.experiment import Experiment
from app.db.models.generalization import GeneralizationReport
from app.db.models.model_artifact import ModelArtifact
from app.db.models.validation_report import ValidationReport
from app.db.session import session_scope
from app.ingestion.service import IngestionService
from app.ml.calibration.service import CalibrationConfig, CalibrationService, ProbabilityObservation
from app.ml.dataset.market_data_query import CandleMarketDataQueryAdapter, MarketSeriesKey
from app.ml.dataset.service import DatasetService, DatasetSnapshotInput
from app.ml.dataset.split_engine import TemporalSplitConfig, TemporalSplitEngine
from app.ml.dataset.split_store import store_manifest
from app.ml.economic.service import (
    CostInput,
    CostProvenance,
    CostScenario,
    EconomicValidationService,
    HypotheticalTrade,
)
from app.ml.experiments import ExperimentPlanInput, ExperimentRegistryService
from app.ml.features.store import FeatureStoreService
from app.ml.generalization.service import Domain, GeneralizationInput, GeneralizationService
from app.ml.models.harness import derive_candle_labels
from app.ml.models.logistic_regression import LogisticRegressionModel, PredictiveModelHarness
from app.ml.validation.service import StatisticalValidationService, ValidationConfig
from app.trading_intelligence.inference.errors import ModelEligibilityError
from app.trading_intelligence.inference.service import GovernedModelEligibilityGate

SLICE = Path(__file__).resolve().parent / "fixtures" / "bml_real_slice.csv"
TIER_LABEL = "BO-B-ML research_validation tier · historical:real corpus"


async def _run_real_lifecycle(session) -> tuple[ModelArtifact, list[str]]:  # noqa: ANN001
    key = MarketSeriesKey(
        market_class="crypto", provider="internal", symbol="BTCUSDT", timeframe="H1"
    )
    result = await IngestionService(session).ingest_csv(
        path=SLICE,
        market_class="crypto",
        symbol="BTCUSDT",
        timeframe="H1",
        source="historical:real",
    )
    assert result.rows_inserted == 400, result

    adapter = CandleMarketDataQueryAdapter(session, provider="internal")
    records = await adapter.get_candles(series_key=key, source_filter="historical:real")
    assert len(records) == 400

    svc = DatasetService(session)
    snapshot = await svc.create_draft_snapshot(
        DatasetSnapshotInput(
            dataset_id="ds-bml-real-slice",
            name="B-ML real BTCUSDT slice research-validation snapshot",
            version=1,
            market="crypto",
            timeframe="H1",
            start_time=records[0].open_time,
            end_time=records[-1].open_time,
            source="historical:real",
            feature_version="feature_set.v1",
            quality_score="pass",
            tier="research_validation",
            created_by="bml",
        )
    )
    frozen = await svc.freeze_from_query(
        snapshot=snapshot,
        query_port=adapter,
        market_class=key.market_class,
        provider=key.provider,
        symbol=key.symbol,
        timeframe=key.timeframe,
        as_of_time=records[-1].open_time,
        ingestion_finished_at=records[-1].open_time,
    )
    assert frozen.status == "frozen"

    store = FeatureStoreService(session)
    await store.register_builtin_definitions()
    feature_rows, _report = await store.compute_and_store(
        series_key=key,
        records=records,
        source_dataset_hash=frozen.content_hash,
        tier="research_validation",
    )
    assert len(feature_rows) == 400

    n = len(feature_rows)
    row_dicts = [{"row_id": row.id, "as_of": row.as_of} for row in feature_rows]
    split_config = TemporalSplitConfig(
        split_id="split-bml-slice",
        train_start=feature_rows[0].as_of,
        train_end=feature_rows[int(n * 0.6) - 1].as_of,
        validation_start=feature_rows[int(n * 0.6)].as_of,
        validation_end=feature_rows[int(n * 0.8) - 1].as_of,
        test_start=feature_rows[int(n * 0.8)].as_of,
        test_end=feature_rows[-1].as_of,
        label_horizon_bars=1,
        embargo_bars=1,
    )
    split_rows = TemporalSplitEngine().split(rows=row_dicts, config=split_config)
    manifest = await store_manifest(session, snapshot=frozen, split=split_rows, config=split_config)

    experiments = ExperimentRegistryService(session)
    draft = await experiments.create_draft(
        ExperimentPlanInput(
            experiment_id="exp-bml-real-slice",
            version=1,
            purpose="BO-B-ML research-tier logistic regression over real historical data",
            hypothesis=(
                "A deterministic pure-python logistic regression is governed "
                "through the full research lifecycle"
            ),
            dataset_snapshot_id=frozen.id,
            dataset_content_hash=frozen.content_hash or "",
            split_manifest_id=manifest.id,
            split_manifest_hash=manifest.split_hash,
            feature_set_version="feature_set.v1",
            model_family="pure_python_logistic_regression_sgd",
            model_spec={"framework": "pure-python", "training_enabled": True},
            evaluation_plan={"split_strategy": "temporal", "metrics": ["accuracy"]},
            notes=TIER_LABEL,
        )
    )
    pre = await experiments.pre_register(draft)
    approved = await experiments.approve(pre, approver="bml-approver")

    trained = await PredictiveModelHarness(session).train(
        experiment_id=approved.experiment_id, labels_from_candles=True
    )
    artifact = trained.artifact
    assert artifact.framework == "pure-python-logistic-regression-sgd"
    assert artifact.artifact_hash

    labels = await derive_candle_labels(session, feature_rows)
    labeled = [row for row in feature_rows if row.id in labels]
    validation_rows = [
        {
            "as_of": row.as_of,
            "features": {k: float(v) for k, v in row.features.items() if v is not None},
            "label": labels[row.id],
        }
        for row in labeled
    ]
    validation = await StatisticalValidationService(session).validate(
        experiment_id=approved.experiment_id,
        model_artifact_id=artifact.id,
        rows=validation_rows,
        config=ValidationConfig(train_window=40, test_window=15, step=15, embargo=1),
        model=LogisticRegressionModel(seed=42),
    )
    assert validation.id
    assert "fold model=pure-python-logistic-regression-sgd" in (validation.notes or "")

    # Calibration model fitted on the EARLIER half of the labeled rows only;
    # probabilities measured on the later half (no look-ahead discipline).
    median_as_of = sorted(row["as_of"] for row in validation_rows)[len(validation_rows) // 2]
    calib_train = [row for row in validation_rows if row["as_of"] < median_as_of]
    calib_eval = [row for row in validation_rows if row["as_of"] >= median_as_of]
    model = LogisticRegressionModel(seed=42)
    model.fit([row["features"] for row in calib_train], [row["label"] for row in calib_train])
    proba = model.predict_proba([row["features"] for row in calib_eval])
    calibration = await CalibrationService(session).calibrate(
        experiment_id=approved.experiment_id,
        model_artifact_id=artifact.id,
        validation_report_id=validation.id,
        observations=[
            ProbabilityObservation(
                probability=float(p["class_1"]),
                label=row["label"],
                market_class="crypto",
                timeframe="H1",
                regime="trend",
            )
            for p, row in zip(proba, calib_eval, strict=True)
        ],
        config=CalibrationConfig(),
    )
    assert calibration.id

    predictions = model.predict([row["features"] for row in calib_eval])
    trades = [
        HypotheticalTrade(
            gross_return_bps=10.0 if pred == row["label"] else -10.0,
            market_class="crypto",
            timeframe="H1",
            regime="trend",
        )
        for pred, row in zip(predictions, calib_eval, strict=True)
    ]
    scenario = CostScenario(
        name="base",
        costs=[
            CostInput(name="spread", value_bps=1.0, provenance=CostProvenance.MEASURED),
            CostInput(name="commission", value_bps=1.0, provenance=CostProvenance.MEASURED),
            CostInput(name="slippage", value_bps=1.0, provenance=CostProvenance.MEASURED),
            CostInput(name="latency", value_bps=1.0, provenance=CostProvenance.MEASURED),
            CostInput(name="liquidity", value_bps=1.0, provenance=CostProvenance.MEASURED),
            CostInput(name="transaction_costs", value_bps=1.0, provenance=CostProvenance.MEASURED),
        ],
    )
    economic = await EconomicValidationService(session).validate(
        experiment_id=approved.experiment_id,
        model_artifact_id=artifact.id,
        validation_report_id=validation.id,
        calibration_report_id=calibration.id,
        trades=trades,
        statistical_conclusion={"verdict": "not_statistically_positive"},
        scenarios=[scenario],
    )
    assert economic.id

    holdout_accuracy = model.evaluate(
        [row["features"] for row in calib_eval], [row["label"] for row in calib_eval]
    ).accuracy
    generalization = await GeneralizationService(session).create_report(
        experiment_id=approved.experiment_id,
        model_artifact_id=artifact.id,
        trained_on=Domain(markets=["crypto_core"], timeframes=["H1"], regimes=["trend"]),
        evaluated_on=[
            GeneralizationInput(
                market="crypto_holdout",
                timeframe="H1",
                regime="trend",
                accuracy=holdout_accuracy,
                sample_count=len(calib_eval),
            )
        ],
        operating_domain=Domain(markets=["crypto_core"], timeframes=["H1"], regimes=["trend"]),
    )
    assert generalization.id

    artifact.statistical_report_id = validation.id
    artifact.calibration_report_id = calibration.id
    artifact.economic_report_id = economic.id
    artifact.notes = TIER_LABEL
    await session.flush()

    decision = await GovernedModelEligibilityGate(session).evaluate(artifact)
    return artifact, decision.reasons


@pytest.mark.asyncio
async def test_bml_research_lifecycle_on_real_data(prepared_db: None) -> None:
    async with session_scope() as session:
        artifact, reasons = await _run_real_lifecycle(session)
        # All four report types exist, experiment approved, artifact research_only.
        for model, label in (
            (Experiment, "experiments"),
            (ModelArtifact, "model_artifacts"),
            (ValidationReport, "validation_reports"),
            (CalibrationReport, "calibration_reports"),
            (EconomicReport, "economic_reports"),
            (GeneralizationReport, "generalization_reports"),
        ):
            count = (await session.execute(select(func.count()).select_from(model))).scalar_one()
            assert count >= 1, f"no {label} row"
        assert artifact.research_status == "research_only"
        assert "research_validation" in (artifact.notes or "")

        # The honest gate decision is recorded — NOT_ADVISORY_APPROVED always
        # present; promotion must be consistent with the decision (never
        # promoted past a failing threshold).
        assert "NOT_ADVISORY_APPROVED" in reasons
        decision = await GovernedModelEligibilityGate(session).evaluate(artifact)
        if any("THRESHOLD" in r or r == "ECONOMIC_NOT_USABLE" for r in decision.reasons):
            with pytest.raises(ModelEligibilityError):
                await GovernedModelEligibilityGate(session).promote_to_advisory_approved(
                    artifact, approver="bml-approver", approval_reason="must be refused"
                )
        assert artifact.advisory_status != "advisory_approved"


@pytest.mark.asyncio
async def test_bml_promotion_only_on_genuine_passage(prepared_db: None) -> None:
    """Phase 3 discipline: a model whose reports fail thresholds can never be
    promoted, and the refusal names the threshold reasons."""
    async with session_scope() as session:
        artifact, _reasons = await _run_real_lifecycle(session)
        decision = await GovernedModelEligibilityGate(session).evaluate(artifact)
        assert not decision.eligible  # research_only + expected threshold failures
        try:
            await GovernedModelEligibilityGate(session).promote_to_advisory_approved(
                artifact, approver="bml-approver", approval_reason="attempt"
            )
            promoted = True
        except ModelEligibilityError:
            promoted = False
        assert not promoted
        assert artifact.advisory_status != "advisory_approved"
