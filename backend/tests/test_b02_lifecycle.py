"""B-02 — Governed research lifecycle executed at pipeline_validation tier.

Pre-fix expectations (b02_probe_prefix.log): the harness has no candle-label
derivation (`labels_from_candles` missing) and the baseline has no
`predict_proba`, so the lifecycle cannot run and the gate applies no numeric
thresholds.

Post-fix: the full W2 machinery runs over the labeled synthetic corpus —
pre-registration → approval → training → walk-forward → calibration
(degenerate labeled priors) → economic (6-class cost model) → generalization
(distinct governed hold-out) → eligibility evaluation with an HONEST
NOT-eligible decision.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
from sqlalchemy import func, select

from app.db.models.calibration_report import CalibrationReport
from app.db.models.dataset_split import DatasetSplitManifest
from app.db.models.economic_report import EconomicReport
from app.db.models.experiment import Experiment
from app.db.models.generalization import GeneralizationReport
from app.db.models.model_artifact import ModelArtifact
from app.db.models.validation_report import ValidationReport
from app.db.session import session_scope
from app.ingestion.service import IngestionService
from app.ml.calibration.service import CalibrationConfig, CalibrationService, ProbabilityObservation
from app.ml.dataset.market_data_query import CandleMarketDataQueryAdapter
from app.ml.dataset.service import DatasetService, DatasetSnapshotInput
from app.ml.dataset.split_engine import TemporalSplitConfig, TemporalSplitEngine
from app.ml.dataset.split_store import store_manifest
from app.ml.dataset.synthetic_corpus import CORPUS_SERIES_KEYS, generate_series, write_corpus_csv
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
from app.ml.models.baseline import MajorityClassBaseline
from app.ml.models.harness import BaselineModelHarness, derive_candle_labels
from app.ml.validation.service import StatisticalValidationService, ValidationConfig
from app.trading_intelligence.inference.errors import ModelEligibilityError
from app.trading_intelligence.inference.service import GovernedModelEligibilityGate

TIER_LABEL = "BO-B-02 pipeline_validation tier · synthetic corpus · no research conclusion"


async def _run_lifecycle(session, *, bars: int = 60) -> tuple[ModelArtifact, list[str]]:
    """Execute the complete B-02 lifecycle for EURUSD; return artifact + gate reasons."""
    key = CORPUS_SERIES_KEYS[0]  # forex/EURUSD/H1
    corpus = generate_series(market_class=key.market_class, symbol=key.symbol, bars=bars)
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "b02_lifecycle.csv"
        write_corpus_csv(path, corpus)
        result = await IngestionService(session).ingest_csv(
            path=path,
            market_class=key.market_class,
            symbol=key.symbol,
            timeframe=key.timeframe,
            source="synthetic",
        )
        assert result.rows_inserted == bars

    svc = DatasetService(session)
    snapshot = await svc.create_draft_snapshot(
        DatasetSnapshotInput(
            dataset_id="ds-b02-lifecycle",
            name="B02 lifecycle snapshot",
            version=1,
            market=key.market_class,
            timeframe=key.timeframe,
            start_time=corpus[0].open_time,
            end_time=corpus[-1].open_time,
            source="synthetic",
            feature_version="feature_set.v1",
            quality_score="pass",
            tier="pipeline_validation",
            created_by="b02-lifecycle",
        )
    )
    frozen = await svc.freeze_from_candles(
        snapshot=snapshot,
        candles=corpus,
        provider="internal",
        as_of_time=corpus[-1].open_time,
        ingestion_finished_at=corpus[-1].open_time,
    )
    assert frozen.status == "frozen"

    store = FeatureStoreService(session)
    await store.register_builtin_definitions()
    adapter = CandleMarketDataQueryAdapter(session, provider="internal")
    records = await adapter.get_candles(
        series_key=key, source_filter="synthetic", start=frozen.start_time, end=frozen.end_time
    )
    assert len(records) == bars
    feature_rows, _report = await store.compute_and_store(
        series_key=key,
        records=records,
        source_dataset_hash=frozen.content_hash,
        tier="pipeline_validation",
    )
    assert len(feature_rows) == bars

    # Split manifest keyed by FEATURE-row ids (the harness's pin contract).
    row_dicts = [{"row_id": row.id, "as_of": row.as_of} for row in feature_rows]
    split_config = TemporalSplitConfig(
        split_id="split-b02-lifecycle",
        train_start=feature_rows[0].as_of,
        train_end=feature_rows[bars // 2 - 1].as_of,
        validation_start=feature_rows[bars // 2].as_of,
        validation_end=feature_rows[int(bars * 0.8) - 1].as_of,
        test_start=feature_rows[int(bars * 0.8)].as_of,
        test_end=feature_rows[-1].as_of,
        label_horizon_bars=1,
        embargo_bars=1,
    )
    split_rows = TemporalSplitEngine().split(rows=row_dicts, config=split_config)
    manifest = await store_manifest(session, snapshot=frozen, split=split_rows, config=split_config)
    assert manifest.split_hash

    # Pre-register + approve the experiment.
    experiments = ExperimentRegistryService(session)
    draft = await experiments.create_draft(
        ExperimentPlanInput(
            experiment_id="exp-b02-lifecycle",
            version=1,
            purpose="BO-B-02 governed lifecycle machinery proof (pipeline tier)",
            hypothesis=(
                "The governed ML lifecycle executes end-to-end "
                "on the labeled synthetic corpus"
            ),
            dataset_snapshot_id=frozen.id,
            dataset_content_hash=frozen.content_hash or "",
            split_manifest_id=manifest.id,
            split_manifest_hash=manifest.split_hash,
            feature_set_version="feature_set.v1",
            model_family="pure_python_majority_baseline",
            model_spec={"framework": "pure-python", "training_enabled": True},
            evaluation_plan={"split_strategy": "temporal", "metrics": ["accuracy"]},
            notes=TIER_LABEL,
        )
    )
    pre_registered = await experiments.pre_register(draft)
    approved = await experiments.approve(pre_registered, approver="b02-lifecycle-approver")
    assert approved.status == "approved"

    # Train (labels derived from candles — no look-ahead: label at bar t is
    # the direction of the NEXT bar's close; the last bar is unlabeled).
    harness = BaselineModelHarness(session)
    trained = await harness.train(experiment_id=approved.experiment_id, labels_from_candles=True)
    artifact = trained.artifact
    assert artifact.artifact_hash
    assert artifact.research_status == "research_only"

    # Walk-forward statistical validation over the same honest labels.
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
        config=ValidationConfig(train_window=10, test_window=5, step=5, embargo=1),
    )
    assert validation.id

    # Calibration over degenerate (labeled) training-prior probabilities.
    baseline = MajorityClassBaseline(seed=42)
    baseline.fit([row["label"] for row in validation_rows])
    proba = baseline.predict_proba([row["features"] for row in validation_rows])
    observations = [
        ProbabilityObservation(
            probability=float(entry["class_1"]),
            label=row["label"],
            market_class="forex",
            timeframe="H1",
            regime="trend",
        )
        for entry, row in zip(proba, validation_rows, strict=True)
    ]
    calibration = await CalibrationService(session).calibrate(
        experiment_id=approved.experiment_id,
        model_artifact_id=artifact.id,
        validation_report_id=validation.id,
        observations=observations,
        config=CalibrationConfig(),
    )
    assert calibration.id

    # Economic validation: honest hypothetical trades from the walk-forward
    # outcomes, under the full six-class cost model.
    predictions = baseline.predict([row["features"] for row in validation_rows])
    trades = [
        HypotheticalTrade(
            gross_return_bps=10.0 if pred == row["label"] else -10.0,
            market_class="forex",
            timeframe="H1",
            regime="trend",
        )
        for pred, row in zip(predictions, validation_rows, strict=True)
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

    # Generalization: a DISTINCT governed hold-out question (crypto vs forex
    # training domain — no overlap, recorded independently).
    generalization = await GeneralizationService(session).create_report(
        experiment_id=approved.experiment_id,
        model_artifact_id=artifact.id,
        trained_on=Domain(markets=["forex"], timeframes=["H1"], regimes=["trend"]),
        evaluated_on=[
            GeneralizationInput(
                market="crypto", timeframe="H1", regime="trend", accuracy=0.5, sample_count=200
            )
        ],
        operating_domain=Domain(markets=["forex"], timeframes=["H1"], regimes=["trend"]),
    )
    assert generalization.id

    # Attach reports to the artifact + tier labels on every record.
    artifact.statistical_report_id = validation.id
    artifact.calibration_report_id = calibration.id
    artifact.economic_report_id = economic.id
    artifact.notes = TIER_LABEL
    validation.notes = TIER_LABEL
    calibration.notes = TIER_LABEL
    economic.notes = TIER_LABEL
    generalization.notes = TIER_LABEL
    await session.flush()

    decision = await GovernedModelEligibilityGate(session).evaluate(artifact)
    return artifact, decision.reasons


@pytest.mark.asyncio
async def test_b02_lifecycle_executes_and_eligibility_is_honestly_negative(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        artifact, reasons = await _run_lifecycle(session)
        assert reasons, "eligibility decision must not be silently positive"
        # The majority-class baseline is expected to fail the substantive
        # thresholds — and must fail for the right, explicit reasons.
        assert "STATISTICAL_THRESHOLD_NOT_MET" in reasons
        assert "CALIBRATION_THRESHOLD_NOT_MET" in reasons
        assert "ECONOMIC_NOT_USABLE" in reasons

        # Promotion must be refused with the threshold reasons recorded.
        with pytest.raises(ModelEligibilityError) as excinfo:
            await GovernedModelEligibilityGate(session).promote_to_advisory_approved(
                artifact, approver="b02-approver", approval_reason="must be refused"
            )
        message = str(excinfo.value)
        assert "STATISTICAL_THRESHOLD_NOT_MET" in message
        assert artifact.advisory_status != "advisory_approved"

        # Every report and registry row exists with the tier label carried.
        for model, label in (
            (Experiment, "experiments"),
            (ModelArtifact, "model_artifacts"),
            (ValidationReport, "validation_reports"),
            (CalibrationReport, "calibration_reports"),
            (EconomicReport, "economic_reports"),
            (GeneralizationReport, "generalization_reports"),
            (DatasetSplitManifest, "dataset_split_manifests"),
        ):
            count = (await session.execute(select(func.count()).select_from(model))).scalar_one()
            assert count >= 1, f"no {label} row produced"
        assert artifact.notes and "pipeline_validation" in artifact.notes
        assert "no research conclusion" in (artifact.notes or "")


@pytest.mark.asyncio
async def test_b02_lifecycle_labels_are_no_lookahead(prepared_db: None) -> None:
    """The derived label at bar t uses only the NEXT bar's close — a forward
    label with no horizon leakage — and the final bar is never labeled."""
    from app.db.session import session_scope
    from app.ml.features.store import FeatureStoreService

    key = CORPUS_SERIES_KEYS[0]
    corpus = generate_series(market_class=key.market_class, symbol=key.symbol, bars=40)
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "b02_labels.csv"
        write_corpus_csv(path, corpus)
        async with session_scope() as session:
            await IngestionService(session).ingest_csv(
                path=path,
                market_class=key.market_class,
                symbol=key.symbol,
                timeframe=key.timeframe,
                source="synthetic",
            )
            svc = DatasetService(session)
            snapshot = await svc.create_draft_snapshot(
                DatasetSnapshotInput(
                    dataset_id="ds-b02-labels",
                    name="B02 label derivation snapshot",
                    version=1,
                    market=key.market_class,
                    timeframe=key.timeframe,
                    start_time=corpus[0].open_time,
                    end_time=corpus[-1].open_time,
                    source="synthetic",
                    feature_version="feature_set.v1",
                    quality_score="pass",
                    tier="pipeline_validation",
                    created_by="b02-labels",
                )
            )
            frozen = await svc.freeze_from_candles(
                snapshot=snapshot,
                candles=corpus,
                provider="internal",
                as_of_time=corpus[-1].open_time,
                ingestion_finished_at=corpus[-1].open_time,
            )
            adapter = CandleMarketDataQueryAdapter(session, provider="internal")
            records = await adapter.get_candles(
                series_key=key, source_filter="synthetic"
            )
            store = FeatureStoreService(session)
            await store.register_builtin_definitions()
            feature_rows, _ = await store.compute_and_store(
                series_key=key,
                records=records,
                source_dataset_hash=frozen.content_hash,
                tier="pipeline_validation",
            )
            labels = await derive_candle_labels(session, feature_rows)
            assert len(labels) == len(feature_rows) - 1, (
                f"expected {len(feature_rows) - 1} labels (last bar unlabeled), got {len(labels)}"
            )
            closes = {c.open_time: float(c.close) for c in records}
            for row in feature_rows:
                if row.id not in labels:
                    continue
                # find next close by time
                times = sorted(closes)
                idx = times.index(row.as_of)
                next_close = closes[times[idx + 1]]
                expected = 1 if next_close > closes[row.as_of] else 0
                assert labels[row.id] == expected
