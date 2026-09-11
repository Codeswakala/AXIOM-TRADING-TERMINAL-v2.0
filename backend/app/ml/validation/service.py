"""Statistical validation framework (W2-U07)."""

from __future__ import annotations

import hashlib
import json
import math
import random
from dataclasses import asdict, dataclass
from typing import Any, Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.experiment import Experiment
from app.db.models.model_artifact import ModelArtifact
from app.db.models.validation_report import ValidationReport
from app.ml.models.baseline import MajorityClassBaseline
from app.ml.validation.errors import (
    EmbargoViolationError,
    MissingUncertaintyError,
    NonTemporalValidationError,
    ValidationPinError,
)
from app.repositories.audit_repository import AuditRepository


@dataclass(frozen=True, slots=True)
class ValidationConfig:
    strategy: str = "walk_forward"
    train_window: int = 20
    test_window: int = 5
    step: int = 5
    embargo: int = 1
    metric: str = "accuracy"
    confidence_level: float = 0.95
    bootstrap_samples: int = 200
    seed: int = 42


class StatisticalValidationService:
    """Produces research-only validation reports with mandatory uncertainty."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._audit = AuditRepository(session)

    async def validate(
        self,
        *,
        experiment_id: str,
        model_artifact_id: str,
        rows: Sequence[dict],
        config: ValidationConfig,
        model: Any | None = None,
    ) -> ValidationReport:
        """Statistical walk-forward validation.

        ``model`` (BO-B-ML): an optional fit/predict/evaluate-compatible model
        measured inside the folds. Default remains the W2-U06 majority-class
        baseline (backward compatible — no existing behavior changed).
        """
        self._validate_config(config)
        experiment = await self._load_experiment(experiment_id)
        artifact = await self._load_artifact(model_artifact_id, experiment)
        fold_results = self._walk_forward(rows=rows, config=config, model=model)
        fold_model_label = getattr(model, "framework", None) or "majority_class_baseline"
        accuracies = [fold["accuracy"] for fold in fold_results]
        aggregate_accuracy = sum(accuracies) / len(accuracies) if accuracies else None
        uncertainty = self._bootstrap_ci(accuracies, config=config)
        effect_size = self._effect_size(aggregate_accuracy)
        significance = self._significance(accuracies)
        payload = {
            "experiment_id": experiment.experiment_id,
            "model_artifact_id": artifact.id,
            "fold_model": fold_model_label,
            "validation_kind": config.strategy,
            "metrics": {"accuracy": aggregate_accuracy},
            "uncertainty": uncertainty,
            "fold_results": fold_results,
            "effect_size": effect_size,
            "significance": significance,
            "config": asdict(config),
            "research_status": "research_only",
        }
        self.validate_report_contract(payload)
        report_hash = hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode("utf-8")
        ).hexdigest()
        report = ValidationReport(
            experiment_id=experiment.experiment_id,
            model_artifact_id=artifact.id,
            validation_kind=config.strategy,
            metrics=payload["metrics"],
            uncertainty=uncertainty,
            fold_results=fold_results,
            effect_size=effect_size,
            significance=significance,
            config=asdict(config),
            report_hash=report_hash,
            research_status="research_only",
            notes=(
                f"Research-only statistical validation report; "
                f"fold model={fold_model_label}; no live signal."
            ),
        )
        self._session.add(report)
        await self._session.flush()
        await self._audit.append(
            category="ML",
            action="validation.report_created",
            actor="system",
            resource_type="validation_report",
            resource_id=report.id,
            message=f"Validation report created experiment={experiment.experiment_id}",
            details={"experiment_id": experiment.experiment_id, "report_hash": report_hash},
        )
        return report

    def validate_report_contract(self, payload: dict) -> None:
        required = ["metrics", "uncertainty", "effect_size", "significance", "fold_results"]
        missing = [key for key in required if not payload.get(key)]
        if missing:
            raise MissingUncertaintyError(f"VALIDATION_UNCERTAINTY_MISSING: {missing}")
        uncertainty = payload["uncertainty"]
        if "confidence_interval" not in uncertainty or "bootstrap_distribution" not in uncertainty:
            raise MissingUncertaintyError("VALIDATION_UNCERTAINTY_MISSING")

    async def _load_experiment(self, experiment_id: str) -> Experiment:
        from sqlalchemy import select

        result = await self._session.execute(
            select(Experiment)
            .where(Experiment.experiment_id == experiment_id)
            .order_by(Experiment.version.desc())
        )
        experiment = result.scalars().first()
        if experiment is None or experiment.status != "approved":
            raise ValidationPinError("VALIDATION_EXPERIMENT_NOT_APPROVED")
        return experiment

    async def _load_artifact(self, artifact_id: str, experiment: Experiment) -> ModelArtifact:
        artifact = await self._session.get(ModelArtifact, artifact_id)
        if artifact is None or artifact.experiment_id != experiment.experiment_id:
            raise ValidationPinError("VALIDATION_ARTIFACT_PIN_MISMATCH")
        if artifact.dataset_content_hash != experiment.dataset_content_hash:
            raise ValidationPinError("VALIDATION_DATASET_PIN_MISMATCH")
        if artifact.split_manifest_hash != experiment.split_manifest_hash:
            raise ValidationPinError("VALIDATION_SPLIT_PIN_MISMATCH")
        return artifact

    def _validate_config(self, config: ValidationConfig) -> None:
        if config.strategy.lower() in {"random", "shuffle", "random_cv"}:
            raise NonTemporalValidationError("NON_TEMPORAL_CV")
        if config.strategy not in {"walk_forward", "blocked_time_series_cv", "oos_holdout"}:
            raise NonTemporalValidationError("NON_TEMPORAL_CV")
        if min(config.train_window, config.test_window, config.step) <= 0:
            raise ValueError("validation windows and step must be positive")
        if config.embargo < 0:
            raise EmbargoViolationError("EMBARGO_VIOLATION")

    def _walk_forward(
        self,
        *,
        rows: Sequence[dict],
        config: ValidationConfig,
        model: Any | None = None,
    ) -> list[dict]:
        ordered = sorted(rows, key=lambda row: row["as_of"].isoformat())
        folds: list[dict] = []
        start = 0
        while True:
            train_start = start
            train_end = train_start + config.train_window
            test_start = train_end + config.embargo
            test_end = test_start + config.test_window
            if test_end > len(ordered):
                break
            if test_start < train_end + config.embargo:
                raise EmbargoViolationError("EMBARGO_VIOLATION")
            train_rows = ordered[train_start:train_end]
            test_rows = ordered[test_start:test_end]
            matrix = [row["features"] for row in test_rows]
            labels = [int(row["label"]) for row in test_rows]
            fold_model = model or MajorityClassBaseline(seed=config.seed)
            if model is None:
                fold_model.fit([int(row["label"]) for row in train_rows])
            else:
                fold_model.fit(
                    [row["features"] for row in train_rows],
                    [int(row["label"]) for row in train_rows],
                )
            result = fold_model.evaluate(matrix, labels)
            folds.append(
                {
                    "fold": len(folds) + 1,
                    "train_start": train_rows[0]["as_of"].isoformat(),
                    "train_end": train_rows[-1]["as_of"].isoformat(),
                    "test_start": test_rows[0]["as_of"].isoformat(),
                    "test_end": test_rows[-1]["as_of"].isoformat(),
                    "train_count": len(train_rows),
                    "test_count": len(test_rows),
                    "accuracy": result.accuracy,
                }
            )
            start += config.step
        if not folds:
            raise ValueError("not enough rows for walk-forward validation")
        return folds

    def _bootstrap_ci(self, values: Sequence[float | None], *, config: ValidationConfig) -> dict:
        clean = [float(value) for value in values if value is not None]
        if not clean:
            raise MissingUncertaintyError("VALIDATION_UNCERTAINTY_MISSING")
        rng = random.Random(config.seed)
        distribution: list[float] = []
        for _ in range(config.bootstrap_samples):
            sample = [clean[rng.randrange(len(clean))] for _ in clean]
            distribution.append(sum(sample) / len(sample))
        distribution.sort()
        alpha = 1.0 - config.confidence_level
        lo_index = max(0, int((alpha / 2) * len(distribution)))
        hi_index = min(len(distribution) - 1, int((1 - alpha / 2) * len(distribution)) - 1)
        return {
            "method": "percentile_bootstrap",
            "confidence_level": config.confidence_level,
            "confidence_interval": [distribution[lo_index], distribution[hi_index]],
            "bootstrap_distribution": distribution,
        }

    def _effect_size(self, aggregate_accuracy: float | None) -> dict:
        if aggregate_accuracy is None:
            raise MissingUncertaintyError("VALIDATION_UNCERTAINTY_MISSING")
        null_accuracy = 0.5
        return {
            "metric": "accuracy_minus_null",
            "null": null_accuracy,
            "value": aggregate_accuracy - null_accuracy,
        }

    def _significance(self, values: Sequence[float | None]) -> dict:
        clean = [float(value) for value in values if value is not None]
        if not clean:
            raise MissingUncertaintyError("VALIDATION_UNCERTAINTY_MISSING")
        mean = sum(clean) / len(clean)
        if len(clean) == 1:
            p_value = 1.0
        else:
            variance = sum((value - mean) ** 2 for value in clean) / (len(clean) - 1)
            stderr = math.sqrt(variance / len(clean)) if variance > 0 else 0.0
            if stderr == 0:
                p_value = 1.0 if mean == 0.5 else 0.0
            else:
                z = abs((mean - 0.5) / stderr)
                p_value = math.erfc(z / math.sqrt(2))
        return {"test": "normal_approx_accuracy_vs_0.5", "p_value": p_value}
