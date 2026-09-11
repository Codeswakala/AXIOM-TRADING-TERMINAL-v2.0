"""Pure-Python baseline classifier (W2-U06 compatibility-safe)."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True, slots=True)
class BaselinePredictionResult:
    predictions: list[int]
    accuracy: float | None


class MajorityClassBaseline:
    """Deterministic majority-class baseline.

    This model is intentionally simple. W2-U06 proves governance and harness
    mechanics, not predictive skill.
    """

    framework = "pure-python-majority-baseline"

    # BO-B-02 §7: calibration requires probabilities; this baseline has no
    # skill-estimate probabilities. The probabilities it emits are the
    # DEGENERATE TRAINING PRIOR (constant class frequencies), provided only
    # so the calibration machinery can run — they are labeled degenerate and
    # must never be presented as calibrated confidence.
    PROBABILITIES_ARE_DEGENERATE = True

    def __init__(self, *, seed: int = 42) -> None:
        self.seed = seed
        self.majority_class: int | None = None
        self.class_counts: dict[int, int] = {}

    def fit(self, labels: Sequence[int]) -> None:
        if not labels:
            raise ValueError("baseline requires at least one training label")
        counts = Counter(int(label) for label in labels)
        # Deterministic tie-break: lowest class label.
        self.majority_class = sorted(counts.items(), key=lambda item: (-item[1], item[0]))[0][0]
        self.class_counts = dict(sorted(counts.items()))

    def predict(self, rows: Sequence[dict[str, float]]) -> list[int]:
        if self.majority_class is None:
            raise ValueError("baseline model has not been fit")
        return [self.majority_class for _ in rows]

    def predict_proba(self, rows: Sequence[dict[str, float]]) -> list[dict[str, float | bool]]:
        """Degenerate training-prior probabilities (BO-B-02 §7).

        Constant class frequencies across every row — explicitly labeled
        `degenerate_prior=True`. Not calibrated skill; calibration over these
        values measures the prior, not the model.
        """
        if self.majority_class is None:
            raise ValueError("baseline model has not been fit")
        total = sum(self.class_counts.values())
        class_1 = self.class_counts.get(1, 0) / total
        class_0 = self.class_counts.get(0, 0) / total
        return [
            {"class_0": class_0, "class_1": class_1, "degenerate_prior": True}
            for _ in rows
        ]

    def evaluate(
        self,
        rows: Sequence[dict[str, float]],
        labels: Sequence[int],
    ) -> BaselinePredictionResult:
        predictions = self.predict(rows)
        if not labels:
            return BaselinePredictionResult(predictions=predictions, accuracy=None)
        correct = sum(
            1
            for pred, label in zip(predictions, labels, strict=False)
            if pred == int(label)
        )
        return BaselinePredictionResult(predictions=predictions, accuracy=correct / len(labels))

    def artifact_payload(self, *, feature_columns: Sequence[str]) -> dict:
        return {
            "framework": self.framework,
            "seed": self.seed,
            "majority_class": self.majority_class,
            "class_counts": self.class_counts,
            "feature_columns": list(feature_columns),
        }
