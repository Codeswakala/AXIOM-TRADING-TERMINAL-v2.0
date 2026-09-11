"""BO-B-ML research runner (DA evidence tooling, untracked).

The substantive research program over REAL data:
  corpus   : OKX H1 {BTC,ETH,SOL,XRP,ADA,DOGE}-USDT, historical:real
  training : BTC+ETH+SOL (research_validation snapshot + features + split)
  holdout  : XRP, ADA, DOGE (unseen instruments)
  lifecycle: pre-register -> approve -> logistic SGD -> walk-forward ->
             calibration -> economic (six-class realistic crypto costs) ->
             cross-instrument generalization -> governed eligibility
  outcome  : honest — promoted ONLY on genuine threshold passage.
"""

from __future__ import annotations

import asyncio
import logging
import sys
from pathlib import Path

# Suppress the per-candle naive-datetime boundary warnings (100K+ rows would
# flood the evidence log; the boundary behavior itself is unchanged).
logging.getLogger("app.core.time").setLevel(logging.ERROR)

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from sqlalchemy import func, select  # noqa: E402

from app.core.config import Settings  # noqa: E402
from app.core.time import coerce_external_utc  # noqa: E402
from app.db.models.calibration_report import CalibrationReport  # noqa: E402
from app.db.models.dataset import DatasetSnapshot  # noqa: E402
from app.db.models.dataset_split import DatasetSplitManifest  # noqa: E402
from app.db.models.economic_report import EconomicReport  # noqa: E402
from app.db.models.experiment import Experiment  # noqa: E402
from app.db.models.feature import FeatureRecord  # noqa: E402
from app.db.models.generalization import GeneralizationReport  # noqa: E402
from app.db.models.model_artifact import ModelArtifact  # noqa: E402
from app.db.models.validation_report import ValidationReport  # noqa: E402
from app.db.session import create_schema, get_session_factory, init_db  # noqa: E402
from app.ingestion.service import IngestionService  # noqa: E402
from app.ml.calibration.service import (  # noqa: E402
    CalibrationConfig,
    CalibrationService,
    ProbabilityObservation,
)
from app.ml.dataset.market_data_query import (  # noqa: E402
    CandleMarketDataQueryAdapter,
    MarketSeriesKey,
)
from app.ml.dataset.service import DatasetService, DatasetSnapshotInput  # noqa: E402
from app.ml.dataset.split_engine import TemporalSplitConfig, TemporalSplitEngine  # noqa: E402
from app.ml.dataset.split_store import store_manifest  # noqa: E402
from app.ml.economic.service import (  # noqa: E402
    CostInput,
    CostProvenance,
    CostScenario,
    EconomicValidationService,
    HypotheticalTrade,
)
from app.ml.experiments import ExperimentPlanInput, ExperimentRegistryService  # noqa: E402
from app.ml.features.store import FeatureStoreService  # noqa: E402
from app.ml.generalization.service import (  # noqa: E402
    Domain,
    GeneralizationInput,
    GeneralizationService,
)
from app.ml.models.harness import derive_candle_labels  # noqa: E402
from app.ml.models.logistic_regression import (  # noqa: E402
    LogisticRegressionModel,
    PredictiveModelHarness,
)
from app.ml.validation.service import (  # noqa: E402
    StatisticalValidationService,
    ValidationConfig,
)
from app.trading_intelligence.inference.errors import ModelEligibilityError  # noqa: E402
from app.trading_intelligence.inference.service import (  # noqa: E402
    GovernedModelEligibilityGate,
)

DB_URL = "sqlite+aiosqlite:////home/user/axiom/backend/axiom_dev.db"
CORPUS = Path("/home/user/axiom/backend/tests/fixtures/bdata_corpus")
TRAIN = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
HOLDOUT = ["XRPUSDT", "ADAUSDT", "DOGEUSDT"]
TIER_LABEL = "BO-B-ML research_validation tier · historical:real corpus"


async def _count(session, model, label: str) -> None:
    total = (await session.execute(select(func.count()).select_from(model))).scalar_one()
    print(f"[bml] {label}: {total}")


async def main() -> None:
    init_db(Settings(database_url=DB_URL))
    await create_schema()
    factory = get_session_factory()

    async with factory() as session:
        # 1. Ingest the real corpus (historical:real).
        print("[bml] ingesting OKX H1 real corpus…")
        for symbol in TRAIN + HOLDOUT:
            result = await IngestionService(session).ingest_csv(
                path=CORPUS / f"okx_{symbol}_H1.csv",
                market_class="crypto",
                symbol=symbol,
                timeframe="H1",
                source="historical:real",
            )
            print(f"[bml] ingested {symbol}: {result.rows_inserted} rows ({result.status})")
        await session.commit()

    async with factory() as session:
        adapter = CandleMarketDataQueryAdapter(session, provider="internal")
        svc = DatasetService(session)
        store = FeatureStoreService(session)
        await store.register_builtin_definitions()

        async def freeze_and_features(symbols: list[str], dataset_id: str) -> tuple[DatasetSnapshot, list[FeatureRecord]]:
            records = []
            for symbol in symbols:
                key = MarketSeriesKey(
                    market_class="crypto", provider="internal", symbol=symbol, timeframe="H1"
                )
                series_records = await adapter.get_candles(
                    series_key=key, source_filter="historical:real"
                )
                records.extend(series_records)
            snapshot = await svc.create_draft_snapshot(
                DatasetSnapshotInput(
                    dataset_id=dataset_id,
                    name=f"B-ML {dataset_id}",
                    version=1,
                    market="crypto",
                    timeframe="H1",
                    start_time=min(coerce_external_utc(r.open_time, source="runner") for r in records),
                    end_time=max(coerce_external_utc(r.open_time, source="runner") for r in records),
                    source="historical:real",
                    feature_version="feature_set.v1",
                    quality_score="pass",
                    tier="research_validation",
                    created_by="bml-runner",
                )
            )
            frozen = await svc.freeze_from_canonical_records(
                snapshot=snapshot,
                records=records,
                as_of_time=max(coerce_external_utc(r.open_time, source="runner") for r in records),
                ingestion_finished_at=max(coerce_external_utc(r.open_time, source="runner") for r in records),
            )
            print(
                f"[bml] snapshot {dataset_id}: {frozen.status} "
                f"hash={frozen.content_hash[:16]}… records={len(records)}"
            )
            feature_rows: list[FeatureRecord] = []
            for symbol in symbols:
                key = MarketSeriesKey(
                    market_class="crypto", provider="internal", symbol=symbol, timeframe="H1"
                )
                series_records = await adapter.get_candles(
                    series_key=key, source_filter="historical:real"
                )
                rows, _ = await store.compute_and_store(
                    series_key=key,
                    records=series_records,
                    source_dataset_hash=frozen.content_hash,
                    tier="research_validation",
                )
                feature_rows.extend(rows)
            return frozen, feature_rows

        train_snapshot, train_rows = await freeze_and_features(TRAIN, "ds-bml-train-core")
        holdout_snapshot, holdout_rows = await freeze_and_features(HOLDOUT, "ds-bml-holdout")
        print(f"[bml] feature rows: train={len(train_rows)} holdout={len(holdout_rows)}")

        # 2. Temporal split across the training-domain feature rows.
        ordered = sorted(train_rows, key=lambda r: coerce_external_utc(r.as_of, source="runner"))
        n = len(ordered)
        row_dicts = [
            {
                "row_id": row.id,
                "as_of": coerce_external_utc(row.as_of, source="runner"),
                # BO-B-ML reproducibility: deterministic cross-series tie-break
                # (symbol + timestamp is unique per row).
                "sort_key": f"{row.symbol}|{coerce_external_utc(row.as_of, source='runner').isoformat()}",
            }
            for row in ordered
        ]
        split_config = TemporalSplitConfig(
            split_id="split-bml-train",
            train_start=row_dicts[0]["as_of"],
            train_end=row_dicts[int(n * 0.6) - 1]["as_of"],
            validation_start=row_dicts[int(n * 0.6)]["as_of"],
            validation_end=row_dicts[int(n * 0.8) - 1]["as_of"],
            test_start=row_dicts[int(n * 0.8)]["as_of"],
            test_end=row_dicts[-1]["as_of"],
            label_horizon_bars=1,
            embargo_bars=1,
        )
        split_rows = TemporalSplitEngine().split(rows=row_dicts, config=split_config)
        manifest = await store_manifest(
            session, snapshot=train_snapshot, split=split_rows, config=split_config
        )
        print(
            f"[bml] split: train={manifest.train_count} val={manifest.validation_count} "
            f"test={manifest.test_count} hash={manifest.split_hash[:16]}…"
        )

        # 3. Pre-register + approve the experiment.
        experiments = ExperimentRegistryService(session)
        draft = await experiments.create_draft(
            ExperimentPlanInput(
                experiment_id="exp-bml-logistic-core",
                version=1,
                purpose=(
                    "BO-B-ML substantive research: logistic regression over "
                    "real historical OKX H1 data (BTC/ETH/SOL), hold-out XRP/ADA/DOGE"
                ),
                hypothesis=(
                    "A deterministic pure-python logistic regression trained on "
                    "price-normalized causal features produces calibrated "
                    "probabilities on real data"
                ),
                dataset_snapshot_id=train_snapshot.id,
                dataset_content_hash=train_snapshot.content_hash or "",
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
        approved = await experiments.approve(pre, approver="bml-operator-approver")
        print(f"[bml] experiment: {approved.experiment_id} status={approved.status}")

        # 4. Train the logistic model.
        trained = await PredictiveModelHarness(session).train(
            experiment_id=approved.experiment_id, labels_from_candles=True, seed=42
        )
        artifact = trained.artifact
        metrics = {
            k: (round(v, 4) if isinstance(v, float) else v)
            for k, v in (artifact.metrics or {}).items()
            if k != "model_note"
        }
        print(f"[bml] model: {artifact.name} hash={artifact.artifact_hash[:16]}… metrics={metrics}")

        # 5. Labels + model reconstruction from the exact train-split rows
        # (same seed + same input sequence as the harness → identical model).
        labels = await derive_candle_labels(session, train_rows)
        by_id = {row.id: row for row in train_rows}
        train_matrix: list[dict[str, float]] = []
        train_y: list[int] = []
        for item in split_rows.train:
            row_id = item["row_id"]
            feature_row = by_id.get(row_id)
            if feature_row is None or row_id not in labels:
                continue
            feats = {
                k: float(v) for k, v in feature_row.features.items() if v is not None
            }
            if len(feats) != 3:
                continue
            train_matrix.append(feats)
            train_y.append(labels[row_id])
        model = LogisticRegressionModel(seed=42)
        model.fit(train_matrix, train_y)
        print(f"[bml] reconstructed model rows={len(train_matrix)}")

        labeled = [row for row in train_rows if row.id in labels]
        validation_rows = [
            {
                "as_of": coerce_external_utc(row.as_of, source="runner"),
                "features": {k: float(v) for k, v in row.features.items() if v is not None},
                "label": labels[row.id],
            }
            for row in labeled
        ]
        # Walk-forward statistical validation measuring the LOGISTIC model.
        validation = await StatisticalValidationService(session).validate(
            experiment_id=approved.experiment_id,
            model_artifact_id=artifact.id,
            rows=validation_rows,
            config=ValidationConfig(train_window=500, test_window=150, step=150, embargo=1),
            model=model,
        )
        print(
            f"[bml] validation: folds={len(validation.fold_results)} "
            f"accuracy={validation.metrics.get('accuracy')} "
            f"effect={validation.effect_size.get('value')} "
            f"p={validation.significance.get('p_value')}"
        )

        # 6. Calibration over real probabilities on the test-period rows.
        # The walk-forward loop re-fit the shared instance per fold; restore
        # the ARTIFACT state (fit on the exact train split) before measuring.
        model.fit(train_matrix, train_y)
        test_start = row_dicts[int(n * 0.8)]["as_of"]
        test_labeled = [
            row for row in validation_rows if row["as_of"] >= test_start
        ]
        proba = model.predict_proba([row["features"] for row in test_labeled])
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
                for p, row in zip(proba, test_labeled, strict=True)
            ],
            config=CalibrationConfig(),
        )
        print(
            f"[bml] calibration: ECE={calibration.expected_calibration_error} "
            f"brier={calibration.brier_score} base_rate={calibration.base_rate}"
        )

        # 7. Economic validation — realistic crypto cost model.
        predictions = model.predict([row["features"] for row in test_labeled])
        trades = [
            HypotheticalTrade(
                gross_return_bps=10.0 if pred == row["label"] else -10.0,
                market_class="crypto",
                timeframe="H1",
                regime="trend",
            )
            for pred, row in zip(predictions, test_labeled, strict=True)
        ]
        scenario = CostScenario(
            name="base",
            costs=[
                CostInput("spread", 1.0, CostProvenance.ASSUMED, 0.5, 2.0, "typical OKX top-of-book spread class"),
                CostInput("commission", 10.0, CostProvenance.PROVIDER_PUBLISHED, detail="OKX taker fee class"),
                CostInput("slippage", 2.0, CostProvenance.ASSUMED, 1.0, 5.0, "H1-bar execution assumption"),
                CostInput("latency", 0.5, CostProvenance.ASSUMED, 0.0, 2.0, "no HFT assumption"),
                CostInput("liquidity", 1.0, CostProvenance.ASSUMED, 0.0, 3.0, "large-cap pairs"),
                CostInput("transaction_costs", 1.0, CostProvenance.ASSUMED, 0.5, 2.0, "withdrawal/roll costs class"),
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
            f"[bml] economic: verdict={economic.economic_conclusion.get('verdict')} "
            f"net_bps={economic.scenario_results.get('base', {}).get('net_return_bps')}"
        )

        # 8. Cross-instrument generalization (distinct governed question).
        holdout_labels = await derive_candle_labels(session, holdout_rows)
        eval_inputs = []
        for symbol in HOLDOUT:
            complete = [
                r
                for r in holdout_rows
                if r.symbol == symbol
                and r.id in holdout_labels
                and all(v is not None for v in r.features.values())
            ]
            matrix = [
                {k: float(v) for k, v in r.features.items()} for r in complete
            ]
            y = [holdout_labels[r.id] for r in complete]
            accuracy = model.evaluate(matrix, y).accuracy if matrix else None
            eval_inputs.append(
                GeneralizationInput(
                    market=f"crypto_holdout_{symbol.lower()}",
                    timeframe="H1",
                    regime="trend",
                    accuracy=accuracy or 0.0,
                    sample_count=len(complete),
                )
            )
            print(f"[bml] holdout {symbol}: accuracy={accuracy} n={len(complete)}")
        generalization = await GeneralizationService(session).create_report(
            experiment_id=approved.experiment_id,
            model_artifact_id=artifact.id,
            trained_on=Domain(markets=["crypto_core"], timeframes=["H1"], regimes=["trend"]),
            evaluated_on=eval_inputs,
            operating_domain=Domain(markets=["crypto_core"], timeframes=["H1"], regimes=["trend"]),
        )
        print(
            f"[bml] generalization: trained_on={generalization.trained_on} "
            f"holdout={generalization.holdout_results.get('aggregate_accuracy')}"
        )

        # 9. Governed eligibility — the honest decision.
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
        print(f"[bml] eligibility: eligible={decision.eligible}")
        for reason in decision.reasons:
            print(f"[bml]   reason: {reason}")
        try:
            await gate.promote_to_advisory_approved(
                artifact, approver="bml-operator", approval_reason="governed promotion attempt"
            )
            print("[bml] PROMOTED")
        except ModelEligibilityError as exc:
            print(f"[bml] NOT PROMOTED (honest negative): {exc}")

        await session.commit()

    async with factory() as session:
        print("[bml] ---- row counts ----")
        await _count(session, Experiment, "experiments")
        await _count(session, ModelArtifact, "model_artifacts")
        await _count(session, ValidationReport, "validation_reports")
        await _count(session, CalibrationReport, "calibration_reports")
        await _count(session, EconomicReport, "economic_reports")
        await _count(session, GeneralizationReport, "generalization_reports")
        await _count(session, DatasetSplitManifest, "dataset_split_manifests")
        await _count(session, FeatureRecord, "feature_records")


if __name__ == "__main__":
    asyncio.run(main())
