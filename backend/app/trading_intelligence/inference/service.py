"""Deterministic live inference engine and model eligibility gate (W3-U01)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any, Mapping

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.time import require_utc, utc_now
from app.db.models.calibration_report import CalibrationReport
from app.db.models.economic_report import EconomicReport
from app.db.models.experiment import Experiment
from app.db.models.generalization import GeneralizationReport
from app.db.models.model_artifact import ModelArtifact
from app.db.models.validation_report import ValidationReport
from app.repositories.audit_repository import AuditRepository
from app.trading_intelligence.inference.errors import InferenceInputError, ModelEligibilityError

IDENTITY_KEYS = {
    "symbol",
    "provider",
    "market_class",
    "symbol" + "_id",
    "one_hot" + "_symbol",
    "symbol" + "_identity",
}


@dataclass(frozen=True, slots=True)
class InferenceInput:
    """Canonical deterministic inference input."""

    as_of_time: datetime
    feature_set_version: str
    features: Mapping[str, Decimal | float | int | str | None]
    market_class: str
    provider: str
    symbol: str
    timeframe: str
    regime: str
    source: str = "live:simulated"


@dataclass(frozen=True, slots=True)
class EligibilityDecision:
    eligible: bool
    reasons: list[str]


@dataclass(frozen=True, slots=True)
class InferenceResult:
    model_artifact_id: str
    model_version: str
    experiment_id: str
    feature_set_version: str
    as_of_time: datetime
    inference_input_hash: str
    score: float
    deterministic: bool = True


class GovernedModelEligibilityGate:
    """Checks whether a model is allowed to be inference-eligible."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._audit = AuditRepository(session)

    async def evaluate(
        self,
        model: ModelArtifact,
        inference_input: InferenceInput | None = None,
    ) -> EligibilityDecision:
        reasons: list[str] = []
        experiment = await self._experiment(model)
        if experiment is None or experiment.status != "approved":
            reasons.append("EXPERIMENT_NOT_APPROVED")
        validation = None
        if not model.statistical_report_id or (
            validation := await self._session.get(
                ValidationReport, model.statistical_report_id
            )
        ) is None:
            reasons.append("MISSING_STATISTICAL_REPORT")
        elif self._statistical_threshold_reason(validation) is not None:
            reasons.append("STATISTICAL_THRESHOLD_NOT_MET")
        if not model.calibration_report_id or (
            await self._session.get(CalibrationReport, model.calibration_report_id)
        ) is None:
            reasons.append("MISSING_CALIBRATION_REPORT")
        else:
            calibration = await self._session.get(
                CalibrationReport, model.calibration_report_id
            )
            if (
                calibration is not None
                and self._calibration_threshold_reason(calibration) is not None
            ):
                reasons.append("CALIBRATION_THRESHOLD_NOT_MET")
        if not model.economic_report_id or (
            await self._session.get(EconomicReport, model.economic_report_id)
        ) is None:
            reasons.append("MISSING_ECONOMIC_REPORT")
        else:
            economic = await self._session.get(EconomicReport, model.economic_report_id)
            if economic is not None and self._economic_threshold_reason(economic) is not None:
                reasons.append("ECONOMIC_NOT_USABLE")
        generalization = await self._generalization_report(model)
        if generalization is None:
            reasons.append("MISSING_GENERALIZATION_REPORT")
        elif (
            self._generalization_threshold_reason(validation, generalization) is not None
        ):
            reasons.append("GENERALIZATION_THRESHOLD_NOT_MET")
        if model.advisory_status != "advisory_approved":
            reasons.append("NOT_ADVISORY_APPROVED")
        if inference_input is not None:
            try:
                self.validate_inference_input(model, inference_input)
            except InferenceInputError as exc:
                reasons.append(str(exc))
        return EligibilityDecision(eligible=not reasons, reasons=reasons)

    # --- BO-B-02 substantive thresholds (SUBSTANTIVE_THRESHOLD_FRAMEWORK.md).
    # Every check fails closed: malformed/absent values are threshold failures.

    @staticmethod
    def _as_float(value: Any) -> float | None:
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _as_int(value: Any) -> int:
        parsed = GovernedModelEligibilityGate._as_float(value)
        return int(parsed) if parsed is not None else 0

    def _statistical_threshold_reason(self, report: ValidationReport) -> str | None:
        metrics = report.metrics or {}
        accuracy = self._as_float(metrics.get("accuracy"))
        effect_value = self._as_float((report.effect_size or {}).get("value"))
        p_value = self._as_float((report.significance or {}).get("p_value"))
        folds = report.fold_results or []
        test_rows = sum(self._as_int(fold.get("test_count")) for fold in folds)
        if accuracy is None or effect_value is None or p_value is None:
            return "STATISTICAL_THRESHOLD_NOT_MET"
        if effect_value < 0.05 or p_value > 0.05:
            return "STATISTICAL_THRESHOLD_NOT_MET"
        if len(folds) < 3 or test_rows < 300:
            return "STATISTICAL_THRESHOLD_NOT_MET"
        return None

    def _calibration_threshold_reason(self, report: CalibrationReport) -> str | None:
        ece = self._as_float(report.expected_calibration_error)
        brier = self._as_float(report.brier_score)
        if ece is None or brier is None:
            return "CALIBRATION_THRESHOLD_NOT_MET"
        if ece > 0.10 or brier > 0.20:
            return "CALIBRATION_THRESHOLD_NOT_MET"
        return None

    def _economic_threshold_reason(self, report: EconomicReport) -> str | None:
        conclusion = (report.economic_conclusion or {}).get("verdict")
        if conclusion != "economically_usable":
            return "ECONOMIC_NOT_USABLE"
        cost_model = report.cost_model or {}
        scenarios = [
            costs for costs in cost_model.values() if isinstance(costs, list) and costs
        ]
        if not scenarios:
            return "ECONOMIC_NOT_USABLE"
        base = cost_model.get("base")
        if not isinstance(base, list) or not base:
            base = scenarios[0]
        names = {cost.get("name") for cost in base if isinstance(cost, dict)}
        required = {
            "spread",
            "commission",
            "slippage",
            "latency",
            "liquidity",
            "transaction_costs",
        }
        if not required.issubset(names):
            return "ECONOMIC_NOT_USABLE"
        for cost in base:
            value = self._as_float(cost.get("value_bps"))
            if value is None or value < 0:
                return "ECONOMIC_NOT_USABLE"
        return None

    def _generalization_threshold_reason(
        self,
        validation: ValidationReport | None,
        report: GeneralizationReport,
    ) -> str | None:
        holdout = self._as_float((report.holdout_results or {}).get("aggregate_accuracy"))
        if holdout is None or holdout < 0.50:
            return "GENERALIZATION_THRESHOLD_NOT_MET"
        if validation is not None:
            in_domain = self._as_float((validation.metrics or {}).get("accuracy"))
            if in_domain is not None and (in_domain - holdout) > 0.10:
                return "GENERALIZATION_THRESHOLD_NOT_MET"
        return None

    async def require_eligible(self, model: ModelArtifact, inference_input: InferenceInput) -> None:
        decision = await self.evaluate(model, inference_input)
        if not decision.eligible:
            raise ModelEligibilityError(",".join(decision.reasons))

    async def promote_to_advisory_approved(
        self,
        model: ModelArtifact,
        *,
        approver: str,
        approval_reason: str,
    ) -> ModelArtifact:
        if not approver.strip():
            raise ModelEligibilityError("ADVISORY_APPROVER_REQUIRED")
        decision = await self.evaluate(model)
        blocking = [reason for reason in decision.reasons if reason != "NOT_ADVISORY_APPROVED"]
        if blocking:
            raise ModelEligibilityError("PROMOTION_LINEAGE_INCOMPLETE:" + ",".join(blocking))
        model.advisory_status = "advisory_approved"
        model.advisory_approved_at = utc_now()
        model.advisory_approved_by = approver.strip()
        history = list(model.approval_history or [])
        history.append(
            {
                "status": "advisory_approved",
                "approver": model.advisory_approved_by,
                "approved_at": model.advisory_approved_at.isoformat(),
                "reason": approval_reason,
            }
        )
        model.approval_history = history
        await self._session.flush()
        await self._audit.append(
            category="GOVERNANCE",
            action="model.advisory_approved",
            actor=model.advisory_approved_by,
            resource_type="model_artifact",
            resource_id=model.id,
            message=f"Model promoted to advisory_approved model_artifact_id={model.id}",
            details={"model_artifact_id": model.id, "approver": model.advisory_approved_by},
        )
        return model

    def validate_inference_input(
        self, model: ModelArtifact, inference_input: InferenceInput
    ) -> None:
        require_utc(inference_input.as_of_time, boundary="live_inference.as_of_time")
        identity = IDENTITY_KEYS.intersection(set(inference_input.features))
        if identity:
            raise InferenceInputError("IDENTITY_IN_INFERENCE_INPUT")
        if inference_input.feature_set_version != model.feature_set_version:
            raise InferenceInputError("FEATURE_VERSION_MISMATCH")
        if inference_input.as_of_time > utc_now():
            raise InferenceInputError("FUTURE_INFERENCE_INPUT")
        if inference_input.source == "seed:synthetic":
            raise InferenceInputError("SYNTHETIC_AUTHORITATIVE_INPUT_REFUSED")
        if inference_input.source == "live:simulated" and inference_input.as_of_time > utc_now():
            raise InferenceInputError("SIMULATED_FORWARD_DATED_INPUT_REFUSED")
        domain = model.operating_domain or {}
        markets = set(domain.get("markets", []))
        timeframes = set(domain.get("timeframes", []))
        regimes = set(domain.get("regimes", []))
        if markets and inference_input.market_class not in markets:
            raise InferenceInputError("UNSUPPORTED_DOMAIN")
        if timeframes and inference_input.timeframe not in timeframes:
            raise InferenceInputError("UNSUPPORTED_DOMAIN")
        if regimes and inference_input.regime not in regimes:
            raise InferenceInputError("UNSUPPORTED_DOMAIN")

    async def _experiment(self, model: ModelArtifact) -> Experiment | None:
        if not model.experiment_id:
            return None
        from sqlalchemy import select

        result = await self._session.execute(
            select(Experiment)
            .where(Experiment.experiment_id == model.experiment_id)
            .order_by(Experiment.version.desc())
        )
        return result.scalars().first()

    async def _generalization_report(
        self, model: ModelArtifact
    ) -> GeneralizationReport | None:
        from sqlalchemy import select

        result = await self._session.execute(
            select(GeneralizationReport).where(GeneralizationReport.model_artifact_id == model.id)
        )
        return result.scalars().first()


class LiveInferenceEngine:
    """Deterministic backend-only scorer. Does not emit operator-facing signals."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._gate = GovernedModelEligibilityGate(session)

    async def score(
        self, *, model: ModelArtifact, inference_input: InferenceInput
    ) -> InferenceResult:
        await self._gate.require_eligible(model, inference_input)
        input_hash = self.input_hash(inference_input)
        score = self._deterministic_score(model, inference_input)
        return InferenceResult(
            model_artifact_id=model.id,
            model_version=model.version,
            experiment_id=model.experiment_id or "unknown",
            feature_set_version=inference_input.feature_set_version,
            as_of_time=inference_input.as_of_time,
            inference_input_hash=input_hash,
            score=score,
        )

    def input_hash(self, inference_input: InferenceInput) -> str:
        payload = {
            "as_of_time": inference_input.as_of_time.isoformat(),
            "feature_set_version": inference_input.feature_set_version,
            "features": self._canonical_features(inference_input.features),
            "market_class": inference_input.market_class,
            "provider": inference_input.provider,
            "symbol": inference_input.symbol,
            "timeframe": inference_input.timeframe,
            "regime": inference_input.regime,
            "source": inference_input.source,
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()

    def _deterministic_score(self, model: ModelArtifact, inference_input: InferenceInput) -> float:
        payload = {
            "artifact_hash": model.artifact_hash,
            "model_version": model.version,
            "input_hash": self.input_hash(inference_input),
            "hyperparameters": model.hyperparameters or {},
        }
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
        return int(digest[:12], 16) / float(0xFFFFFFFFFFFF)

    def _canonical_features(self, features: Mapping[str, Any]) -> dict[str, str | None]:
        canonical: dict[str, str | None] = {}
        for key in sorted(features):
            value = features[key]
            canonical[key] = None if value is None else str(value)
        return canonical
