"""BO-B-ML Phase 1 — deterministic pure-Python logistic regression (SGD).

Algorithm choice (Doc 09 §12 dependency reasoning):
  - Logistic regression via stochastic gradient descent, implemented in pure
    Python over the standard library only. NO new dependency is introduced:
    no numpy/scipy/sklearn. Rationale:
    1. Necessity: the task (directional prediction from a small set of
       price-normalized features) needs a linear probabilistic classifier —
       logistic regression is the canonical, explainable choice; an SGD core
       is ~60 lines of arithmetic and does not justify a compiled stack.
    2. Maintenance/security: zero new supply-chain surface (the B-00.2
       severity/exception policy stays untouched); pure-Python is fully
       auditable by ITRGA line-by-line.
    3. Portability: runs on the existing interpreter matrix unchanged.

Properties (binding per P1.2):
  - Deterministic: seeded RNG; fixed feature order; identical inputs →
    identical coefficients, probabilities, artifact payload.
  - Market-agnostic: consumes only the builtin causal features; no symbol /
    provider / market identity anywhere (asserted).
  - Explainable: per-feature coefficients + intercept + scaler parameters are
    surfaced in the artifact payload.
  - Real probabilities: sigmoid outputs per row (never a degenerate prior).
"""

from __future__ import annotations

import hashlib
import json
import math
import random
from typing import Any, Mapping, Sequence

from app.ml.models.baseline import BaselinePredictionResult
from app.ml.models.harness import BaselineModelHarness, TrainingResult
from app.repositories.audit_repository import AuditRepository


def _sigmoid(value: float) -> float:
    if value >= 0:
        z = math.exp(-value)
        return 1.0 / (1.0 + z)
    z = math.exp(value)
    return z / (1.0 + z)


class LogisticRegressionModel:
    """Seeded SGD logistic regression with L2 regularization.

    Fits on standardized features (mean/std computed from the training matrix
    only — no leakage across splits). Probabilities are real sigmoid outputs.
    """

    framework = "pure-python-logistic-regression-sgd"

    def __init__(
        self,
        *,
        seed: int = 42,
        learning_rate: float = 0.5,
        epochs: int = 40,
        l2_penalty: float = 1e-3,
    ) -> None:
        self.seed = seed
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.l2_penalty = l2_penalty
        self.feature_order: list[str] = []
        self.coefficients: dict[str, float] = {}
        self.intercept: float = 0.0
        self.scaler: dict[str, tuple[float, float]] = {}
        self._fitted = False

    def _standardize(self, rows: Sequence[dict[str, float]]) -> list[dict[str, float]]:
        feature_order = sorted(rows[0].keys())
        self.feature_order = feature_order
        self.scaler = {}
        for key in feature_order:
            values = [row[key] for row in rows]
            mean = sum(values) / len(values)
            variance = sum((v - mean) ** 2 for v in values) / len(values)
            std = math.sqrt(variance) if variance > 1e-12 else 1.0
            self.scaler[key] = (mean, std)
        return [
            {key: (row[key] - self.scaler[key][0]) / self.scaler[key][1] for key in feature_order}
            for row in rows
        ]

    def fit(self, rows: Sequence[dict[str, float]], labels: Sequence[int]) -> None:
        if not rows:
            raise ValueError("logistic regression requires at least one training row")
        if len(rows) != len(labels):
            raise ValueError("row/label length mismatch")
        matrix = self._standardize(rows)
        target = [int(label) for label in labels]
        rng = random.Random(self.seed)
        weights = {key: rng.uniform(-0.01, 0.01) for key in self.feature_order}
        intercept = 0.0
        count = len(matrix)
        for _epoch in range(self.epochs):
            order = list(range(count))
            rng.shuffle(order)
            for index in order:
                row = matrix[index]
                linear = intercept + sum(weights[key] * row[key] for key in self.feature_order)
                prediction = _sigmoid(linear)
                error = prediction - target[index]
                for key in self.feature_order:
                    gradient = error * row[key] + self.l2_penalty * weights[key]
                    weights[key] -= self.learning_rate * gradient
                intercept -= self.learning_rate * error
        self.coefficients = {key: float(weights[key]) for key in self.feature_order}
        self.intercept = float(intercept)
        self._fitted = True

    def _require_fit(self) -> None:
        if not self._fitted:
            raise ValueError("logistic regression model has not been fit")

    def _probability(self, row: dict[str, float]) -> float:
        self._require_fit()
        linear = self.intercept + sum(
            self.coefficients[key] * row[key] for key in self.feature_order
        )
        return _sigmoid(linear)

    def predict_proba(self, rows: Sequence[dict[str, float]]) -> list[dict[str, float]]:
        self._require_fit()
        return [
            {"class_0": round(1.0 - p, 12), "class_1": round(p, 12)}
            for p in (self._probability(row) for row in rows)
        ]

    def predict(self, rows: Sequence[dict[str, float]]) -> list[int]:
        self._require_fit()
        return [1 if self._probability(row) >= 0.5 else 0 for row in rows]

    def evaluate(
        self, rows: Sequence[dict[str, float]], labels: Sequence[int]
    ) -> BaselinePredictionResult:
        predictions = self.predict(rows)
        if not labels:
            return BaselinePredictionResult(predictions=predictions, accuracy=None)
        correct = sum(
            1 for pred, label in zip(predictions, labels, strict=True) if pred == int(label)
        )
        return BaselinePredictionResult(predictions=predictions, accuracy=correct / len(labels))

    def artifact_payload(self) -> dict[str, Any]:
        self._require_fit()
        return {
            "framework": self.framework,
            "seed": self.seed,
            "learning_rate": self.learning_rate,
            "epochs": self.epochs,
            "l2_penalty": self.l2_penalty,
            "feature_order": list(self.feature_order),
            "coefficients": dict(self.coefficients),
            "intercept": self.intercept,
            "scaler": {key: [mean, std] for key, (mean, std) in self.scaler.items()},
        }


class PredictiveModelHarness(BaselineModelHarness):
    """Governed training path for the logistic regression model.

    Inherits the B-02 harness's experiment/snapshot/split pin resolution
    (pre-registration + approval machinery) — the predictive path is the same
    governed path, not a parallel ungoverned one.
    """

    def __init__(self, session: Any) -> None:  # noqa: ANN401
        super().__init__(session)
        self._audit = AuditRepository(session)

    async def train(
        self,
        *,
        experiment_id: str,
        seed: int = 42,
        labels_from_candles: bool = True,
        label_overrides: Mapping[str, int] | None = None,
        feature_filter: set[str] | None = None,
    ) -> TrainingResult:
        from app.db.models.model_artifact import ModelArtifact
        from app.ml.models.harness import IDENTITY_KEYS

        experiment = await self._load_approved_experiment(experiment_id)
        snapshot = await self._resolve_snapshot(experiment)
        split = await self._resolve_split(experiment, snapshot)
        from app.ml.models.errors import NonTemporalSplitError

        if split.split_strategy not in {"temporal", "walk_forward"}:
            raise NonTemporalSplitError("NON_TEMPORAL_SPLIT")

        rows = await self._load_feature_rows(experiment)
        by_id = {row.id: row for row in rows}
        row_ids = split.manifest.get("row_ids") or {}
        train_rows = self._rows_from_manifest(by_id, row_ids.get("train", []), split_name="train")
        validation_rows = self._rows_from_manifest(
            by_id, row_ids.get("validation", []), split_name="validation"
        )
        test_rows = self._rows_from_manifest(by_id, row_ids.get("test", []), split_name="test")

        from app.ml.models.harness import derive_candle_labels

        label_overrides = label_overrides or None
        if labels_from_candles and label_overrides is None:
            label_overrides = await derive_candle_labels(self._session, rows)

        train_x, train_y, feature_columns = self._matrix_and_labels(
            train_rows, label_overrides=label_overrides, feature_filter=feature_filter
        )
        val_x, val_y, _ = self._matrix_and_labels(
            validation_rows,
            expected_columns=feature_columns,
            label_overrides=label_overrides,
            feature_filter=feature_filter,
        )
        test_x, test_y, _ = self._matrix_and_labels(
            test_rows,
            expected_columns=feature_columns,
            label_overrides=label_overrides,
            feature_filter=feature_filter,
        )

        identity = IDENTITY_KEYS.intersection(set(feature_columns))
        if identity:
            from app.ml.models.errors import IdentityInModelInputError

            raise IdentityInModelInputError(f"IDENTITY_IN_MODEL_INPUT: {sorted(identity)}")

        model = LogisticRegressionModel(seed=seed)
        model.fit(train_x, train_y)
        metrics = {
            "train_accuracy": model.evaluate(train_x, train_y).accuracy,
            "validation_accuracy": model.evaluate(val_x, val_y).accuracy,
            "test_accuracy": model.evaluate(test_x, test_y).accuracy,
            "model_note": (
                "Deterministic pure-python logistic regression (SGD); "
                "coefficients and scaler surfaced for operator explanation."
            ),
        }
        payload = {
            "experiment_id": experiment.experiment_id,
            "experiment_version": experiment.version,
            "dataset_snapshot_id": snapshot.id,
            "dataset_content_hash": snapshot.content_hash,
            "split_manifest_hash": split.split_hash,
            "feature_set_version": experiment.feature_set_version,
            "model": model.artifact_payload(),
            "metrics": metrics,
        }
        artifact_hash = hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode("utf-8")
        ).hexdigest()
        artifact = ModelArtifact(
            name=f"logistic-{experiment.experiment_id}",
            version=f"{experiment.version}-{seed}",
            status="research_only",
            framework=model.framework,
            feature_set_version=experiment.feature_set_version,
            supported_markets=snapshot.market_scope,
            metrics=metrics,
            artifact_uri=f"sha256:{artifact_hash}",
            notes="Research-only logistic regression artifact; no live signal or execution use.",
            experiment_id=experiment.experiment_id,
            dataset_snapshot_id=snapshot.id,
            dataset_content_hash=snapshot.content_hash,
            split_manifest_hash=split.split_hash,
            hyperparameters={
                "seed": seed,
                "learning_rate": model.learning_rate,
                "epochs": model.epochs,
                "l2_penalty": model.l2_penalty,
            },
            artifact_hash=artifact_hash,
            research_status="research_only",
        )
        self._session.add(artifact)
        await self._session.flush()
        await self._audit.append(
            category="ML",
            action="model.logistic_trained",
            actor="system",
            resource_type="model_artifact",
            resource_id=artifact.id,
            message=f"Logistic regression model trained for experiment={experiment.experiment_id}",
            details={"experiment_id": experiment.experiment_id, "artifact_hash": artifact_hash},
        )
        return TrainingResult(artifact=artifact, artifact_hash=artifact_hash, metrics=metrics)
