"""BO-B-ML2 research runner (DA evidence tooling, untracked).

Multiple-comparison-disciplined retry over the real OKX H1 corpus:
  Hypothesis budget: 1 primary + 2 secondary (≤ BO bound of 1+3).
  ALL hypotheses are pre-registered via the experiment registry (plan hashes
  + timestamps printed BEFORE any training) — no post-hoc selection.

  PRIMARY (P): direction@H1, full v1+v2 feature set (11 features).
  SECONDARY S1 (labeled exploratory): direction@H1, ablation subset
    {return_1, range_pct, rolling_return_3, atr_norm_14, structure_bos_rec}.
  SECONDARY S2 (labeled exploratory): magnitude target — next-bar range
    above the trailing 200-bar median — full v1+v2 feature set.

  Correction disclosure: the primary is evaluated alone at alpha=0.05;
  the secondaries are uncorrected and labeled inflation-prone (stated in the
  delivery report per BO-B-ML2 §1.4).
"""

from __future__ import annotations

import asyncio
import logging
import statistics
import sys
from pathlib import Path

logging.getLogger("app.core.time").setLevel(logging.ERROR)

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from sqlalchemy import func, select  # noqa: E402

from app.core.config import Settings  # noqa: E402
from app.core.time import coerce_external_utc  # noqa: E402
from app.db.models.dataset import DatasetSnapshot  # noqa: E402
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
from app.ml.features.definitions import (  # noqa: E402
    builtin_feature_set_v1,
    builtin_feature_set_v2,
)
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
TIER_LABEL = "BO-B-ML2 research_validation tier · historical:real corpus"
FEATURE_SET_VERSION = "feature_set.v2"
PRIMARY_FILTER = {
    "return_1", "range_pct", "rolling_return_3",
    "atr_norm_14", "roc_12", "ema_dist_20", "bband_pos_20",
    "vol_change_1", "hour_sin", "hour_cos", "structure_bos_rec",
}
S1_FILTER = {"return_1", "range_pct", "rolling_return_3", "atr_norm_14", "structure_bos_rec"}


def _sorted_key(feature_rows: list) -> list[dict]:
    ordered = sorted(feature_rows, key=lambda r: coerce_external_utc(r.as_of, source="runner"))
    return [
        {
            "row_id": row.id,
            "as_of": coerce_external_utc(row.as_of, source="runner"),
            "sort_key": (
                f"{row.symbol}|{coerce_external_utc(row.as_of, source='runner').isoformat()}"
            ),
        }
        for row in ordered
    ]


async def main() -> None:
    init_db(Settings(database_url=DB_URL))
    await create_schema()
    factory = get_session_factory()

    async with factory() as session:
        print("[bml2] ingesting OKX H1 real corpus…")
        for symbol in TRAIN + HOLDOUT:
            result = await IngestionService(session).ingest_csv(
                path=CORPUS / f"okx_{symbol}_H1.csv",
                market_class="crypto",
                symbol=symbol,
                timeframe="H1",
                source="historical:real",
            )
            print(f"[bml2] ingested {symbol}: {result.rows_inserted} ({result.status})")
        await session.commit()

    async with factory() as session:
        adapter = CandleMarketDataQueryAdapter(session, provider="internal")
        svc = DatasetService(session)
        store = FeatureStoreService(session)
        await store.register_builtin_definitions()
        for feature in builtin_feature_set_v2():
            try:
                await store.register_definition(feature.spec)
            except Exception as exc:  # noqa: BLE001
                if "duplicate" not in str(exc):
                    raise

        async def freeze(symbols: list[str], dataset_id: str) -> tuple[DatasetSnapshot, list]:
            records = []
            for symbol in symbols:
                key = MarketSeriesKey(
                    market_class="crypto", provider="internal", symbol=symbol, timeframe="H1"
                )
                records.extend(
                    await adapter.get_candles(series_key=key, source_filter="historical:real")
                )
            snapshot = await svc.create_draft_snapshot(
                DatasetSnapshotInput(
                    dataset_id=dataset_id,
                    name=f"B-ML2 {dataset_id}",
                    version=1,
                    market="crypto",
                    timeframe="H1",
                    start_time=min(coerce_external_utc(r.open_time, source="runner") for r in records),
                    end_time=max(coerce_external_utc(r.open_time, source="runner") for r in records),
                    source="historical:real",
                    feature_version=FEATURE_SET_VERSION,
                    quality_score="pass",
                    tier="research_validation",
                    created_by="bml2-runner",
                )
            )
            frozen = await svc.freeze_from_canonical_records(
                snapshot=snapshot,
                records=records,
                as_of_time=max(coerce_external_utc(r.open_time, source="runner") for r in records),
                ingestion_finished_at=max(
                    coerce_external_utc(r.open_time, source="runner") for r in records
                ),
            )
            print(f"[bml2] snapshot {dataset_id}: {frozen.status} records={len(records)}")
            feature_rows: list = []
            v1v2 = list(builtin_feature_set_v1()) + list(builtin_feature_set_v2())
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
                    features=v1v2,
                    feature_set_version=FEATURE_SET_VERSION,
                    source_dataset_hash=frozen.content_hash,
                    tier="research_validation",
                )
                feature_rows.extend(rows)
            return frozen, feature_rows

        train_snapshot, train_rows = await freeze(TRAIN, "ds-bml2-train-core")
        holdout_snapshot, holdout_rows = await freeze(HOLDOUT, "ds-bml2-holdout")
        print(f"[bml2] feature rows: train={len(train_rows)} holdout={len(holdout_rows)}")

        row_dicts = _sorted_key(train_rows)
        n = len(row_dicts)
        split_config = TemporalSplitConfig(
            split_id="split-bml2-train",
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
            f"[bml2] split: train={manifest.train_count} val={manifest.validation_count} "
            f"test={manifest.test_count}"
        )

        # ------------------------------------------------------------------
        # PRE-REGISTRATION — ALL hypotheses, BEFORE any training (binding).
        # ------------------------------------------------------------------
        experiments = ExperimentRegistryService(session)
        hypotheses = [
            (
                "exp-bml2-primary",
                "PRIMARY",
                (
                    "Direction@H1, full v1+v2 feature set (11 causal "
                    "market-agnostic features) over real OKX H1 data"
                ),
                "The expanded feature set contains directional structure absent from the v1 set",
            ),
            (
                "exp-bml2-secondary-s1",
                "SECONDARY-S1 (labeled exploratory)",
                (
                    "Direction@H1, ablation subset {return_1, range_pct, "
                    "rolling_return_3, atr_norm_14, structure_bos_rec}"
                ),
                "Ablation: do volatility/structure features alone change the v1 result?",
            ),
            (
                "exp-bml2-secondary-s2",
                "SECONDARY-S2 (labeled exploratory)",
                (
                    "Magnitude target: next-bar range above the trailing "
                    "200-bar median, full v1+v2 feature set"
                ),
                "Target reformulation: does the expanded set predict range regime?",
            ),
        ]
        pre_registered = []
        for experiment_id, label, purpose, hypothesis in hypotheses:
            draft = await experiments.create_draft(
                ExperimentPlanInput(
                    experiment_id=experiment_id,
                    version=1,
                    purpose=f"BO-B-ML2 {label}: {purpose}",
                    hypothesis=hypothesis,
                    dataset_snapshot_id=train_snapshot.id,
                    dataset_content_hash=train_snapshot.content_hash or "",
                    split_manifest_id=manifest.id,
                    split_manifest_hash=manifest.split_hash,
                    feature_set_version=FEATURE_SET_VERSION,
                    model_family="pure_python_logistic_regression_sgd",
                    model_spec={"framework": "pure-python", "training_enabled": True},
                    evaluation_plan={"split_strategy": "temporal", "metrics": ["accuracy"]},
                    notes=f"{TIER_LABEL} · {label}",
                )
            )
            pre = await experiments.pre_register(draft)
            approved = await experiments.approve(pre, approver="bml2-operator-approver")
            pre_registered.append(approved)
            print(
                f"[bml2] PRE-REGISTERED {label} {approved.experiment_id} "
                f"plan_hash={approved.plan_hash} approved_at={approved.approval_timestamp}"
            )
        print(
            "[bml2] hypothesis budget: 1 primary + 2 secondary "
            "(bound: 1+3). Primary is the determination basis."
        )

        # ------------------------------------------------------------------
        # TRAINING + LIFECYCLE per hypothesis (after pre-registration).
        # ------------------------------------------------------------------
        labels = await derive_candle_labels(session, train_rows)
        holdout_labels = await derive_candle_labels(session, holdout_rows)

        # S2 labels: magnitude target (next-bar range above trailing median).
        s2_train: dict[str, int] = {}
        for symbol in TRAIN:
            key = MarketSeriesKey(
                market_class="crypto", provider="internal", symbol=symbol, timeframe="H1"
            )
            candles = await adapter.get_candles(series_key=key, source_filter="historical:real")
            rows_by_time = {
                coerce_external_utc(r.as_of, source="runner"): r.id for r in train_rows if r.symbol == symbol
            }
            ranges = [float(c.high) - float(c.low) for c in candles]
            for i in range(200, len(candles) - 1):
                median = statistics.median(ranges[i - 200 : i])
                row_id = rows_by_time.get(candles[i].open_time)
                if row_id is None:
                    continue
                s2_train[row_id] = 1 if ranges[i + 1] > median else 0

        hypotheses_specs = [
            ("PRIMARY", pre_registered[0], PRIMARY_FILTER, None),
            ("S1", pre_registered[1], S1_FILTER, None),
            ("S2", pre_registered[2], PRIMARY_FILTER, s2_train),
        ]
        test_start = row_dicts[int(n * 0.8)]["as_of"]

        for label, experiment, feature_filter, label_overrides in hypotheses_specs:
            print(f"[bml2] ==== hypothesis {label} ({experiment.experiment_id}) ====")
            trained = await PredictiveModelHarness(session).train(
                experiment_id=experiment.experiment_id,
                labels_from_candles=label_overrides is None,
                label_overrides=label_overrides,
                feature_filter=feature_filter,
                seed=42,
            )
            artifact = trained.artifact
            metrics = {
                k: (round(v, 4) if isinstance(v, float) else v)
                for k, v in (artifact.metrics or {}).items()
                if k != "model_note"
            }
            print(f"[bml2] model: {artifact.name} metrics={metrics}")

            row_labels = labels if label_overrides is None else label_overrides
            validation_rows = [
                {
                    "as_of": coerce_external_utc(row.as_of, source="runner"),
                    "features": {
                        k: float(v)
                        for k, v in row.features.items()
                        if k in feature_filter and v is not None
                    },
                    "label": row_labels[row.id],
                }
                for row in train_rows
                if row.id in row_labels
            ]
            validation_rows = [r for r in validation_rows if len(r["features"]) == len(feature_filter)]

            model = LogisticRegressionModel(seed=42)
            by_id = {row.id: row for row in train_rows}
            train_matrix: list[dict[str, float]] = []
            train_y: list[int] = []
            for item in split_rows.train:
                feature_row = by_id.get(item["row_id"])
                if feature_row is None or item["row_id"] not in row_labels:
                    continue
                feats = {
                    k: float(v)
                    for k, v in feature_row.features.items()
                    if k in feature_filter and v is not None
                }
                if len(feats) != len(feature_filter):
                    continue
                train_matrix.append(feats)
                train_y.append(row_labels[item["row_id"]])
            model.fit(train_matrix, train_y)

            validation = await StatisticalValidationService(session).validate(
                experiment_id=experiment.experiment_id,
                model_artifact_id=artifact.id,
                rows=validation_rows,
                config=ValidationConfig(train_window=500, test_window=150, step=150, embargo=1),
                model=model,
            )
            print(
                f"[bml2] validation: folds={len(validation.fold_results)} "
                f"accuracy={validation.metrics.get('accuracy')} "
                f"effect={validation.effect_size.get('value')} "
                f"p={validation.significance.get('p_value')}"
            )

            model.fit(train_matrix, train_y)
            test_labeled = [r for r in validation_rows if r["as_of"] >= test_start]
            proba = model.predict_proba([r["features"] for r in test_labeled])
            calibration = await CalibrationService(session).calibrate(
                experiment_id=experiment.experiment_id,
                model_artifact_id=artifact.id,
                validation_report_id=validation.id,
                observations=[
                    ProbabilityObservation(
                        probability=float(p["class_1"]),
                        label=r["label"],
                        market_class="crypto",
                        timeframe="H1",
                        regime="trend",
                    )
                    for p, r in zip(proba, test_labeled, strict=True)
                ],
                config=CalibrationConfig(),
            )
            print(
                f"[bml2] calibration: ECE={calibration.expected_calibration_error} "
                f"brier={calibration.brier_score}"
            )

            predictions = model.predict([r["features"] for r in test_labeled])
            trades = [
                HypotheticalTrade(
                    gross_return_bps=10.0 if pred == r["label"] else -10.0,
                    market_class="crypto",
                    timeframe="H1",
                    regime="trend",
                )
                for pred, r in zip(predictions, test_labeled, strict=True)
            ]
            scenario = CostScenario(
                name="base",
                costs=[
                    CostInput("spread", 1.0, CostProvenance.ASSUMED, 0.5, 2.0, "top-of-book class"),
                    CostInput("commission", 10.0, CostProvenance.PROVIDER_PUBLISHED, detail="OKX taker class"),
                    CostInput("slippage", 2.0, CostProvenance.ASSUMED, 1.0, 5.0, "H1 execution"),
                    CostInput("latency", 0.5, CostProvenance.ASSUMED, 0.0, 2.0, "no HFT"),
                    CostInput("liquidity", 1.0, CostProvenance.ASSUMED, 0.0, 3.0, "large-cap"),
                    CostInput("transaction_costs", 1.0, CostProvenance.ASSUMED, 0.5, 2.0, "roll class"),
                ],
            )
            economic = await EconomicValidationService(session).validate(
                experiment_id=experiment.experiment_id,
                model_artifact_id=artifact.id,
                validation_report_id=validation.id,
                calibration_report_id=calibration.id,
                trades=trades,
                statistical_conclusion={"verdict": "not_statistically_positive"},
                scenarios=[scenario],
            )
            print(
                f"[bml2] economic: verdict={economic.economic_conclusion.get('verdict')} "
                f"net_bps={economic.scenario_results.get('base', {}).get('net_return_bps')}"
            )

            eval_inputs = []
            for symbol in HOLDOUT:
                complete = [
                    r
                    for r in holdout_rows
                    if r.symbol == symbol
                    and r.id in holdout_labels
                    and all(
                        v is not None for k, v in r.features.items() if k in feature_filter
                    )
                ]
                matrix = [
                    {k: float(v) for k, v in r.features.items() if k in feature_filter}
                    for r in complete
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
                print(f"[bml2] holdout {symbol}: accuracy={accuracy} n={len(complete)}")
            generalization = await GeneralizationService(session).create_report(
                experiment_id=experiment.experiment_id,
                model_artifact_id=artifact.id,
                trained_on=Domain(markets=["crypto_core"], timeframes=["H1"], regimes=["trend"]),
                evaluated_on=eval_inputs,
                operating_domain=Domain(markets=["crypto_core"], timeframes=["H1"], regimes=["trend"]),
            )
            print(
                f"[bml2] generalization: holdout={generalization.holdout_results.get('aggregate_accuracy')}"
            )

            artifact.statistical_report_id = validation.id
            artifact.calibration_report_id = calibration.id
            artifact.economic_report_id = economic.id
            artifact.notes = f"{TIER_LABEL} · hypothesis={label}"
            validation.notes = f"{TIER_LABEL} · {label}"
            calibration.notes = f"{TIER_LABEL} · {label}"
            economic.notes = f"{TIER_LABEL} · {label}"
            generalization.notes = f"{TIER_LABEL} · {label}"
            await session.flush()

            gate = GovernedModelEligibilityGate(session)
            decision = await gate.evaluate(artifact)
            print(f"[bml2] eligibility ({label}): eligible={decision.eligible}")
            for reason in decision.reasons:
                print(f"[bml2]   reason: {reason}")
            try:
                await gate.promote_to_advisory_approved(
                    artifact,
                    approver="bml2-operator",
                    approval_reason=f"governed promotion attempt ({label})",
                )
                print(f"[bml2] {label}: PROMOTED")
            except ModelEligibilityError as exc:
                print(f"[bml2] {label}: NOT PROMOTED: {exc}")

        await session.commit()

    async with factory() as session:
        from app.db.models.calibration_report import CalibrationReport
        from app.db.models.economic_report import EconomicReport
        from app.db.models.experiment import Experiment
        from app.db.models.generalization import GeneralizationReport
        from app.db.models.model_artifact import ModelArtifact
        from app.db.models.validation_report import ValidationReport

        for model_class, label in (
            (Experiment, "experiments"),
            (ModelArtifact, "model_artifacts"),
            (ValidationReport, "validation_reports"),
            (CalibrationReport, "calibration_reports"),
            (EconomicReport, "economic_reports"),
            (GeneralizationReport, "generalization_reports"),
        ):
            total = (
                await session.execute(select(func.count()).select_from(model_class))
            ).scalar_one()
            print(f"[bml2] {label}: {total}")


if __name__ == "__main__":
    asyncio.run(main())
