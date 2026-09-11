"""Calibration and probability-quality framework (W2-U08)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.calibration_report import CalibrationReport
from app.db.models.experiment import Experiment
from app.db.models.model_artifact import ModelArtifact
from app.db.models.validation_report import ValidationReport
from app.ml.calibration.errors import CalibrationPinError, CalibrationReportInvalidError
from app.repositories.audit_repository import AuditRepository


@dataclass(frozen=True, slots=True)
class CalibrationConfig:
    bin_count: int = 10
    scheme: str = "equal_width"
    warning_threshold_ece: float = 0.15
    seed: int = 42


@dataclass(frozen=True, slots=True)
class ProbabilityObservation:
    probability: float
    label: int
    market_class: str = "unknown"
    timeframe: str = "unknown"
    regime: str = "unknown"


class CalibrationService:
    """Creates research-only calibration reports."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._audit = AuditRepository(session)

    async def calibrate(
        self,
        *,
        experiment_id: str,
        model_artifact_id: str,
        validation_report_id: str,
        observations: Sequence[ProbabilityObservation],
        config: CalibrationConfig = CalibrationConfig(),
    ) -> CalibrationReport:
        experiment, artifact, validation = await self._resolve_pins(
            experiment_id=experiment_id,
            model_artifact_id=model_artifact_id,
            validation_report_id=validation_report_id,
        )
        payload = self.build_payload(observations=observations, config=config)
        payload.update(
            {
                "experiment_id": experiment.experiment_id,
                "model_artifact_id": artifact.id,
                "validation_report_id": validation.id,
                "research_status": "research_only",
            }
        )
        self.validate_report_contract(payload)
        report_hash = hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode("utf-8")
        ).hexdigest()
        report = CalibrationReport(
            experiment_id=experiment.experiment_id,
            model_artifact_id=artifact.id,
            validation_report_id=validation.id,
            brier_score=str(payload["brier_score"]),
            expected_calibration_error=str(payload["expected_calibration_error"]),
            bin_scheme=payload["bin_scheme"],
            bins=payload["bins"],
            per_slice=payload["per_slice"],
            warnings=payload["warnings"],
            base_rate=str(payload["base_rate"]),
            base_rate_significance=payload["base_rate_significance"],
            config=asdict(config),
            report_hash=report_hash,
            research_status="research_only",
            notes="Research-only calibration report; no live signal.",
        )
        self._session.add(report)
        await self._session.flush()
        await self._audit.append(
            category="ML",
            action="calibration.report_created",
            actor="system",
            resource_type="calibration_report",
            resource_id=report.id,
            message=f"Calibration report created experiment={experiment.experiment_id}",
            details={"experiment_id": experiment.experiment_id, "report_hash": report_hash},
        )
        return report

    def build_payload(
        self,
        *,
        observations: Sequence[ProbabilityObservation],
        config: CalibrationConfig,
    ) -> dict:
        if not observations:
            raise CalibrationReportInvalidError("CALIBRATION_EMPTY_OBSERVATIONS")
        probabilities = [self._clamp_probability(item.probability) for item in observations]
        labels = [int(item.label) for item in observations]
        bins = self._bins(observations=observations, config=config)
        brier = sum((p - y) ** 2 for p, y in zip(probabilities, labels, strict=True)) / len(labels)
        ece = sum(
            (item["count"] / len(labels))
            * abs(item["avg_confidence"] - item["observed_rate"])
            for item in bins
        )
        base_rate = sum(labels) / len(labels)
        warnings: list[str] = []
        if ece > config.warning_threshold_ece:
            warnings.append("POORLY_CALIBRATED")
        return {
            "brier_score": brier,
            "expected_calibration_error": ece,
            "bin_scheme": {"scheme": config.scheme, "bin_count": config.bin_count},
            "bins": bins,
            "per_slice": self._per_slice(observations=observations, config=config),
            "warnings": warnings,
            "base_rate": base_rate,
            "base_rate_significance": self.base_rate_significance(
                predictions=[1 if p >= 0.5 else 0 for p in probabilities],
                labels=labels,
            ),
        }

    def validate_report_contract(self, payload: dict) -> None:
        required = [
            "brier_score",
            "expected_calibration_error",
            "bin_scheme",
            "bins",
            "per_slice",
            "base_rate",
            "base_rate_significance",
        ]
        missing = [key for key in required if key not in payload]
        if missing:
            raise CalibrationReportInvalidError(f"CALIBRATION_REPORT_INCOMPLETE: {missing}")
        if not payload["bins"]:
            raise CalibrationReportInvalidError("CALIBRATION_BINS_REQUIRED")

    def base_rate_significance(self, *, predictions: Sequence[int], labels: Sequence[int]) -> dict:
        if not labels:
            raise CalibrationReportInvalidError("BASE_RATE_EMPTY_LABELS")
        base_rate = max(sum(labels) / len(labels), 1 - (sum(labels) / len(labels)))
        accuracy = sum(
            1
            for p, y in zip(predictions, labels, strict=True)
            if int(p) == int(y)
        ) / len(labels)
        skill_over_base_rate = accuracy - base_rate
        return {
            "null": "no_information_rate",
            "base_rate": base_rate,
            "accuracy": accuracy,
            "skill_over_base_rate": skill_over_base_rate,
            "significant_skill": skill_over_base_rate > 0,
        }

    async def _resolve_pins(
        self,
        *,
        experiment_id: str,
        model_artifact_id: str,
        validation_report_id: str,
    ) -> tuple[Experiment, ModelArtifact, ValidationReport]:
        from sqlalchemy import select

        result = await self._session.execute(
            select(Experiment)
            .where(Experiment.experiment_id == experiment_id)
            .order_by(Experiment.version.desc())
        )
        experiment = result.scalars().first()
        artifact = await self._session.get(ModelArtifact, model_artifact_id)
        validation = await self._session.get(ValidationReport, validation_report_id)
        if experiment is None or artifact is None or validation is None:
            raise CalibrationPinError("CALIBRATION_PIN_UNRESOLVED")
        if artifact.experiment_id != experiment.experiment_id:
            raise CalibrationPinError("CALIBRATION_MODEL_EXPERIMENT_MISMATCH")
        if validation.experiment_id != experiment.experiment_id:
            raise CalibrationPinError("CALIBRATION_VALIDATION_EXPERIMENT_MISMATCH")
        return experiment, artifact, validation

    def _bins(
        self,
        *,
        observations: Sequence[ProbabilityObservation],
        config: CalibrationConfig,
    ) -> list[dict]:
        bin_count = max(1, config.bin_count)
        buckets: list[list[ProbabilityObservation]] = [[] for _ in range(bin_count)]
        for item in observations:
            index = min(bin_count - 1, int(self._clamp_probability(item.probability) * bin_count))
            buckets[index].append(item)
        output: list[dict] = []
        for index, bucket in enumerate(buckets):
            if not bucket:
                output.append(
                    {
                        "bin": index,
                        "count": 0,
                        "avg_confidence": 0.0,
                        "observed_rate": 0.0,
                    }
                )
                continue
            avg_conf = sum(item.probability for item in bucket) / len(bucket)
            observed = sum(item.label for item in bucket) / len(bucket)
            output.append(
                {
                    "bin": index,
                    "count": len(bucket),
                    "avg_confidence": avg_conf,
                    "observed_rate": observed,
                }
            )
        return output

    def _per_slice(
        self,
        *,
        observations: Sequence[ProbabilityObservation],
        config: CalibrationConfig,
    ) -> dict:
        result: dict[str, dict] = {}
        for field in ("market_class", "timeframe", "regime"):
            values = sorted({getattr(item, field) for item in observations})
            result[field] = {}
            for value in values:
                subset = [item for item in observations if getattr(item, field) == value]
                if subset:
                    bins = self._bins(observations=subset, config=config)
                    ece = sum(
                        (item["count"] / len(subset))
                        * abs(item["avg_confidence"] - item["observed_rate"])
                        for item in bins
                    )
                    result[field][value] = {"count": len(subset), "ece": ece, "bins": bins}
        return result

    def _clamp_probability(self, value: float) -> float:
        if not 0.0 <= value <= 1.0:
            raise CalibrationReportInvalidError("PROBABILITY_OUT_OF_RANGE")
        return float(value)
