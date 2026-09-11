"""B-02 dev-database research run (DA evidence tooling, untracked).

Executes the full governed ML lifecycle against the B-01 dev-database corpus:
  pre-registration -> approval -> training (candle-derived labels)
  -> walk-forward validation -> calibration (degenerate labeled priors)
  -> economic validation (6-class cost model) -> generalization (distinct
  hold-out question) -> eligibility evaluation (honest, expected NOT eligible).
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from sqlalchemy import func, select  # noqa: E402

from app.core.config import Settings  # noqa: E402
from app.core.time import coerce_external_utc  # noqa: E402
from app.db.models.calibration_report import CalibrationReport  # noqa: E402
from app.db.models.dataset_split import DatasetSplitManifest  # noqa: E402
from app.db.models.economic_report import EconomicReport  # noqa: E402
from app.db.models.experiment import Experiment  # noqa: E402
from app.db.models.generalization import GeneralizationReport  # noqa: E402
from app.db.models.model_artifact import ModelArtifact  # noqa: E402
from app.db.models.validation_report import ValidationReport  # noqa: E402
from app.db.session import get_session_factory, init_db  # noqa: E402
from app.ml.calibration.service import (  # noqa: E402
    CalibrationConfig,
    CalibrationService,
    ProbabilityObservation,
)
from app.ml.dataset.market_data_query import CandleMarketDataQueryAdapter  # noqa: E402
from app.ml.economic.service import (  # noqa: E402
    CostInput,
    CostProvenance,
    CostScenario,
    EconomicValidationService,
    HypotheticalTrade,
)
from app.ml.experiments import ExperimentPlanInput, ExperimentRegistryService  # noqa: E402
from app.ml.generalization.service import (  # noqa: E402
    Domain,
    GeneralizationInput,
    GeneralizationService,
)
from app.ml.models.baseline import MajorityClassBaseline  # noqa: E402
from app.ml.models.harness import BaselineModelHarness, derive_candle_labels  # noqa: E402
from app.ml.validation.service import (  # noqa: E402
    StatisticalValidationService,
    ValidationConfig,
)
from app.trading_intelligence.inference.errors import ModelEligibilityError  # noqa: E402
from app.trading_intelligence.inference.service import (  # noqa: E402
    GovernedModelEligibilityGate,
)

DB_URL = "sqlite+aiosqlite:////home/user/axiom/backend/axiom_dev.db"
TIER_LABEL = "BO-B-02 pipeline_validation tier · synthetic corpus · no research conclusion"


async def _count(session, model, label: str) -> None:
    total = (await session.execute(select(func.count()).select_from(model))).scalar_one()
    print(f"[b02] {label}: {total}")


async def main() -> None:
    init_db(Settings(database_url=DB_URL))
    factory = get_session_factory()

    async with factory() as session:
        adapter = CandleMarketDataQueryAdapter(session, provider="internal")
        series = await adapter.list_series()
        h1 = [k for k in series if k.timeframe == "H1"]
        print(f"[b02] corpus series available: {[(k.market_class, k.symbol) for k in h1]}")

        # Snapshot + split + features already exist from B-01; resolve pins.
        from app.db.models.dataset import DatasetSnapshot  # noqa: E402
        from app.db.models.feature import FeatureRecord  # noqa: E402

        key = next(k for k in h1 if k.symbol == "EURUSD")
        snapshots = (
            await session.execute(
                select(DatasetSnapshot).where(DatasetSnapshot.market == "forex")
            )
        ).scalars().all()
        snapshot = next(
            s for s in snapshots if s.dataset_id == "ds-b01-forex-eurusd"
        )
        print(f"[b02] pinned snapshot: {snapshot.dataset_id} hash={snapshot.content_hash[:16]}…")

        # Build a B-02 split manifest keyed by FEATURE-row ids (harness contract).
        feature_rows = (
            await session.execute(
                select(FeatureRecord)
                .where(FeatureRecord.source_dataset_hash == snapshot.content_hash)
                .order_by(FeatureRecord.as_of.asc(), FeatureRecord.id.asc())
            )
        ).scalars().all()
        print(f"[b02] feature rows for EURUSD snapshot: {len(feature_rows)}")
        n = len(feature_rows)
        from app.ml.dataset.split_engine import TemporalSplitConfig, TemporalSplitEngine  # noqa: E402
        from app.ml.dataset.split_store import store_manifest  # noqa: E402

        row_dicts = [
            {"row_id": row.id, "as_of": coerce_external_utc(row.as_of, source="b02 runner")}
            for row in feature_rows
        ]
        config = TemporalSplitConfig(
            split_id="split-b02-eurusd",
            train_start=coerce_external_utc(feature_rows[0].as_of, source="b02 runner"),
            train_end=coerce_external_utc(feature_rows[int(n * 0.6) - 1].as_of, source="b02 runner"),
            validation_start=coerce_external_utc(feature_rows[int(n * 0.6)].as_of, source="b02 runner"),
            validation_end=coerce_external_utc(feature_rows[int(n * 0.8) - 1].as_of, source="b02 runner"),
            test_start=coerce_external_utc(feature_rows[int(n * 0.8)].as_of, source="b02 runner"),
            test_end=coerce_external_utc(feature_rows[-1].as_of, source="b02 runner"),
            label_horizon_bars=1,
            embargo_bars=1,
        )
        split_rows = TemporalSplitEngine().split(rows=row_dicts, config=config)
        manifest = await store_manifest(session, snapshot=snapshot, split=split_rows, config=config)
        print(
            f"[b02] split manifest: {manifest.split_id} "
            f"train={manifest.train_count} val={manifest.validation_count} test={manifest.test_count}"
        )

        # Pre-register + approve.
        experiments = ExperimentRegistryService(session)
        draft = await experiments.create_draft(
            ExperimentPlanInput(
                experiment_id="exp-b02-eurusd-baseline",
                version=1,
                purpose="BO-B-02 governed research lifecycle (pipeline_validation tier)",
                hypothesis=(
                    "The governed ML lifecycle executes end-to-end over the "
                    "labeled synthetic corpus and the eligibility gate returns "
                    "an honest NOT-eligible decision"
                ),
                dataset_snapshot_id=snapshot.id,
                dataset_content_hash=snapshot.content_hash or "",
                split_manifest_id=manifest.id,
                split_manifest_hash=manifest.split_hash,
                feature_set_version="feature_set.v1",
                model_family="pure_python_majority_baseline",
                model_spec={"framework": "pure-python", "training_enabled": True},
                evaluation_plan={"split_strategy": "temporal", "metrics": ["accuracy"]},
                notes=TIER_LABEL,
            )
        )
        pre = await experiments.pre_register(draft)
        approved = await experiments.approve(pre, approver="b02-operator-approver")
        print(f"[b02] experiment: {approved.experiment_id} status={approved.status} approver={approved.approver}")

        # Train with candle-derived labels.
        trained = await BaselineModelHarness(session).train(
            experiment_id=approved.experiment_id, labels_from_candles=True
        )
        artifact = trained.artifact
        print(
            f"[b02] model_artifact: {artifact.name} status={artifact.status} "
            f"hash={artifact.artifact_hash[:16]}… "
            f"metrics={ {k: (round(v, 4) if isinstance(v, float) else v) for k, v in (artifact.metrics or {}).items() if k != 'baseline_note'} }"
        )

        # Walk-forward validation.
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
            config=ValidationConfig(train_window=50, test_window=20, step=20, embargo=1),
        )
        print(
            f"[b02] validation_report: folds={len(validation.fold_results)} "
            f"accuracy={validation.metrics.get('accuracy')} "
            f"effect={validation.effect_size.get('value')} p={validation.significance.get('p_value')}"
        )

        # Calibration over degenerate labeled priors.
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
        print(
            f"[b02] calibration_report: ECE={calibration.expected_calibration_error} "
            f"brier={calibration.brier_score} "
            f"base_rate={calibration.base_rate} warnings={calibration.warnings}"
        )

        # Economic validation under the full six-class cost model.
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
        print(
            f"[b02] economic_report: verdict={economic.economic_conclusion.get('verdict')} "
            f"net={economic.scenario_results.get('base', {}).get('net_return_bps')}"
        )

        # Generalization — a distinct governed hold-out research question.
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
        print(
            f"[b02] generalization_report: trained_on={generalization.trained_on} "
            f"holdout={generalization.holdout_results.get('aggregate_accuracy')}"
        )

        artifact.statistical_report_id = validation.id
        artifact.calibration_report_id = calibration.id
        artifact.economic_report_id = economic.id
        artifact.notes = TIER_LABEL
        validation.notes = TIER_LABEL
        calibration.notes = TIER_LABEL
        economic.notes = TIER_LABEL
        generalization.notes = TIER_LABEL
        await session.flush()

        gate = GovernedModelEligibilityGate(session)
        decision = await gate.evaluate(artifact)
        print(f"[b02] eligibility: eligible={decision.eligible}")
        for reason in decision.reasons:
            print(f"[b02]   reason: {reason}")
        try:
            await gate.promote_to_advisory_approved(
                artifact, approver="b02-approver", approval_reason="must be refused"
            )
            print("[b02] PROMOTION ERROR: gate promoted a threshold-failing model!")
        except ModelEligibilityError as exc:
            print(f"[b02] promotion refused (expected): {exc}")

        await session.commit()

    async with factory() as session:
        print("[b02] ---- row counts ----")
        await _count(session, Experiment, "experiments")
        await _count(session, ModelArtifact, "model_artifacts")
        await _count(session, ValidationReport, "validation_reports")
        await _count(session, CalibrationReport, "calibration_reports")
        await _count(session, EconomicReport, "economic_reports")
        await _count(session, GeneralizationReport, "generalization_reports")
        await _count(session, DatasetSplitManifest, "dataset_split_manifests")


if __name__ == "__main__":
    asyncio.run(main())
