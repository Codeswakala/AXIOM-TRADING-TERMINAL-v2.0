"""Governed advisory signal production, guardrails, and history service (W3-U03)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Any, Literal
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.time import require_utc, utc_now
from app.db.models.advisory_signal import AdvisorySignal
from app.db.models.calibration_report import CalibrationReport
from app.db.models.economic_report import EconomicReport
from app.db.models.generalization import GeneralizationReport
from app.db.models.model_artifact import ModelArtifact
from app.repositories.audit_repository import AuditRepository
from app.trading_intelligence.inference import (
    GovernedModelEligibilityGate,
    InferenceInput,
    LiveInferenceEngine,
)

SignalState = Literal["emitted", "withheld", "warning", "expired", "superseded"]


@dataclass(frozen=True, slots=True)
class SignalGuardrailConfig:
    """Concrete emit-time freshness and guardrail thresholds."""

    max_input_staleness_seconds: int = 300
    signal_validity_seconds: int = 300
    calibration_warning_ece_threshold: float = 0.15


@dataclass(frozen=True, slots=True)
class AdvisorySignalHistoryFilter:
    """Read-only signal-history query filters."""

    signal_id: str | None = None
    model_artifact_id: str | None = None
    market_class: str | None = None
    symbol: str | None = None
    timeframe: str | None = None
    signal_state: str | None = None
    current_only: bool = False
    limit: int = 50


class AdvisorySignalService:
    """Creates inert advisory signal records and exposes read-only history."""

    def __init__(
        self,
        session: AsyncSession,
        guardrail_config: SignalGuardrailConfig | None = None,
    ) -> None:
        self._session = session
        self._audit = AuditRepository(session)
        if guardrail_config is None:
            settings = get_settings()
            guardrail_config = SignalGuardrailConfig(
                max_input_staleness_seconds=settings.signal_max_input_staleness_seconds,
                signal_validity_seconds=settings.signal_validity_seconds,
                calibration_warning_ece_threshold=settings.signal_calibration_warning_ece_threshold,
            )
        self._guardrails = guardrail_config

    async def produce(
        self,
        *,
        model: ModelArtifact,
        inference_input: InferenceInput,
        rationale: str | None,
        actor: str = "system",
        risk_notes: str | None = None,
        audit_correlation_id: str | None = None,
    ) -> AdvisorySignal:
        """Persist one governed advisory signal decision.

        The method always persists the decision. Eligibility, stale input,
        operating-domain, or rationale failures produce a withheld record;
        poor calibration or an unusable economic verdict produce warning records.
        """
        now = utc_now()
        as_of_time = require_utc(
            inference_input.as_of_time, boundary="advisory_signal.as_of_time"
        )
        assert as_of_time is not None
        input_staleness_seconds = max(0, int((now - as_of_time).total_seconds()))
        signal_validity_seconds = max(0, self._guardrails.signal_validity_seconds)
        expires_at = now + timedelta(seconds=signal_validity_seconds)
        freshness_status = "fresh"
        correlation_id = audit_correlation_id or str(uuid4())
        gate = GovernedModelEligibilityGate(self._session)
        engine = LiveInferenceEngine(self._session)
        input_hash = engine.input_hash(inference_input)
        decision = await gate.evaluate(model, inference_input)
        transitions = ["candidate", "eligible_checked"]
        generalization_report_id = await self._generalization_report_id(model)
        lineage = self._lineage(model, generalization_report_id)

        raw_score: float | None = None
        calibrated_confidence: float | None = None
        signal_direction = "withheld"
        calibration_status = "not_evaluated"
        economic_verdict = await self._economic_verdict(model)
        guardrail_reasons = self._unique(
            [
                *decision.reasons,
                *self._emit_time_domain_reasons(model, inference_input),
                *self._staleness_reasons(input_staleness_seconds),
            ]
        )
        if "STALE_INPUT" in guardrail_reasons:
            freshness_status = "stale"
        operating_domain_status = self._domain_status(guardrail_reasons)
        eligibility_reasons = list(guardrail_reasons)

        if guardrail_reasons:
            pre_expiry_state: SignalState = "withheld"
            state_reason = ",".join(guardrail_reasons)
            signal_rationale = f"Withheld by emit-time guardrail: {state_reason}"
        elif rationale is None or not rationale.strip():
            pre_expiry_state = "withheld"
            state_reason = "RATIONALE_REQUIRED"
            eligibility_reasons = [state_reason]
            signal_rationale = "Withheld because no advisory rationale was provided."
            operating_domain_status = "valid"
        else:
            result = await engine.score(model=model, inference_input=inference_input)
            raw_score = result.score
            calibration = await self._calibration_report(model)
            calibrated_confidence = self._calibrated_confidence(raw_score, calibration)
            calibration_status = self._calibration_status(calibration, inference_input)
            economic_verdict = await self._economic_verdict(model)
            signal_direction = self._classification(calibrated_confidence)
            operating_domain_status = "valid"
            signal_rationale = rationale.strip()
            warning_reasons = self._warning_reasons(calibration_status, economic_verdict)
            if warning_reasons:
                pre_expiry_state = "warning"
                state_reason = ",".join(warning_reasons)
                eligibility_reasons = warning_reasons
            else:
                pre_expiry_state = "emitted"
                state_reason = "ELIGIBLE"
                eligibility_reasons = []

        final_state = self._apply_expiry(
            pre_expiry_state=pre_expiry_state,
            transitions=transitions,
            expires_at=expires_at,
            now=now,
        )
        if final_state == "expired":
            state_reason = "SIGNAL_EXPIRED"
            freshness_status = "expired"
            eligibility_reasons = [state_reason]
        explainability = self._explainability_summary(
            model=model,
            inference_input=inference_input,
            input_hash=input_hash,
            signal_state=final_state,
            state_reason=state_reason,
            raw_score=raw_score,
            calibrated_confidence=calibrated_confidence,
            signal_direction=signal_direction,
            operating_domain_status=operating_domain_status,
            calibration_status=calibration_status,
            economic_verdict=economic_verdict,
            eligibility_reasons=eligibility_reasons,
            rationale=signal_rationale,
            input_staleness_seconds=input_staleness_seconds,
            signal_validity_seconds=signal_validity_seconds,
            expires_at=expires_at,
            freshness_status=freshness_status,
        )
        signal = AdvisorySignal(
            created_at=now,
            as_of_time=as_of_time,
            market_class=inference_input.market_class,
            provider=inference_input.provider,
            symbol=inference_input.symbol,
            timeframe=inference_input.timeframe,
            model_artifact_id=model.id,
            model_version=model.version,
            feature_set_version=inference_input.feature_set_version,
            experiment_id=model.experiment_id or "unknown",
            statistical_report_id=lineage["statistical_report_id"],
            calibration_report_id=lineage["calibration_report_id"],
            economic_report_id=lineage["economic_report_id"],
            generalization_report_id=lineage["generalization_report_id"],
            inference_input_hash=input_hash,
            raw_score=raw_score,
            calibrated_confidence=calibrated_confidence,
            input_staleness_seconds=input_staleness_seconds,
            signal_validity_seconds=signal_validity_seconds,
            expires_at=expires_at,
            freshness_status=freshness_status,
            signal_direction=signal_direction,
            signal_state=final_state,
            state_reason=state_reason,
            eligibility_reasons=eligibility_reasons,
            operating_domain_status=operating_domain_status,
            calibration_status=calibration_status,
            economic_verdict=economic_verdict,
            risk_notes=self._risk_notes(
                risk_notes,
                calibration_status,
                economic_verdict,
                eligibility_reasons,
                freshness_status,
            ),
            rationale=signal_rationale,
            explainability_summary=explainability,
            state_transition_history=transitions,
            audit_correlation_id=correlation_id,
        )
        self._session.add(signal)
        await self._session.flush()
        await self._audit_signal(
            signal=signal,
            actor=actor,
            input_hash=input_hash,
            calibrated_confidence=calibrated_confidence,
        )
        return signal

    async def list_history(self, filters: AdvisorySignalHistoryFilter) -> list[AdvisorySignal]:
        """Return persisted advisory signals through read-only history filters."""
        limit = min(max(filters.limit, 1), 200)
        stmt = select(AdvisorySignal)
        if filters.signal_id:
            stmt = stmt.where(AdvisorySignal.signal_id == filters.signal_id)
        if filters.model_artifact_id:
            stmt = stmt.where(AdvisorySignal.model_artifact_id == filters.model_artifact_id)
        if filters.market_class:
            stmt = stmt.where(AdvisorySignal.market_class == filters.market_class)
        if filters.symbol:
            stmt = stmt.where(AdvisorySignal.symbol == filters.symbol)
        if filters.timeframe:
            stmt = stmt.where(AdvisorySignal.timeframe == filters.timeframe)
        if filters.signal_state:
            stmt = stmt.where(AdvisorySignal.signal_state == filters.signal_state)
        if filters.current_only:
            stmt = stmt.where(AdvisorySignal.signal_state.in_(["emitted", "warning"]))
            stmt = stmt.where(AdvisorySignal.expires_at.is_not(None))
            stmt = stmt.where(AdvisorySignal.expires_at > utc_now())
        stmt = stmt.order_by(AdvisorySignal.created_at.desc()).limit(limit)
        result = await self._session.scalars(stmt)
        return list(result.all())

    async def get_signal(self, signal_id: str) -> AdvisorySignal | None:
        """Return a single advisory signal by id."""
        return await self._session.get(AdvisorySignal, signal_id)

    async def expire_due_signals(self, *, actor: str = "system") -> list[AdvisorySignal]:
        """Mark due emitted/warning records expired through the domain service."""
        now = utc_now()
        stmt = (
            select(AdvisorySignal)
            .where(AdvisorySignal.signal_state.in_(["emitted", "warning"]))
            .where(AdvisorySignal.expires_at.is_not(None))
            .where(AdvisorySignal.expires_at <= now)
        )
        result = await self._session.scalars(stmt)
        expired = list(result.all())
        for signal in expired:
            signal.signal_state = "expired"
            signal.state_reason = "SIGNAL_EXPIRED"
            signal.freshness_status = "expired"
            history = list(signal.state_transition_history or [])
            if not history or history[-1] != "expired":
                history.append("expired")
            signal.state_transition_history = history
            summary = dict(signal.explainability_summary or {})
            why = dict(summary.get("why") or {})
            why.update({"signal_state": "expired", "state_reason": "SIGNAL_EXPIRED"})
            summary["why"] = why
            freshness = dict(summary.get("freshness") or {})
            freshness["freshness_status"] = "expired"
            summary["freshness"] = freshness
            signal.explainability_summary = summary
        await self._session.flush()
        for signal in expired:
            await self._audit_signal(
                signal=signal,
                actor=actor,
                input_hash=signal.inference_input_hash,
                calibrated_confidence=signal.calibrated_confidence,
            )
        return expired

    async def _audit_signal(
        self,
        *,
        signal: AdvisorySignal,
        actor: str,
        input_hash: str,
        calibrated_confidence: float | None,
    ) -> None:
        await self._audit.append(
            category="ML",
            action=f"advisory_signal.{signal.signal_state}",
            actor=actor,
            resource_type="advisory_signal",
            resource_id=signal.signal_id,
            message=(
                f"Advisory signal {signal.signal_state} signal_id={signal.signal_id} "
                f"model_artifact_id={signal.model_artifact_id}"
            ),
            details={
                "signal_id": signal.signal_id,
                "model_artifact_id": signal.model_artifact_id,
                "signal_state": signal.signal_state,
                "state_reason": signal.state_reason,
                "freshness_status": signal.freshness_status,
                "expires_at": signal.expires_at.isoformat() if signal.expires_at else None,
                "inference_input_hash": input_hash,
                "calibrated_confidence": calibrated_confidence,
            },
            correlation_id=signal.audit_correlation_id,
        )

    async def _generalization_report_id(self, model: ModelArtifact) -> str | None:
        stmt = (
            select(GeneralizationReport.id)
            .where(GeneralizationReport.model_artifact_id == model.id)
            .order_by(GeneralizationReport.created_at.desc())
            .limit(1)
        )
        result = await self._session.scalars(stmt)
        return result.first()

    async def _calibration_report(self, model: ModelArtifact) -> CalibrationReport | None:
        if not model.calibration_report_id:
            return None
        return await self._session.get(CalibrationReport, model.calibration_report_id)

    async def _economic_verdict(self, model: ModelArtifact) -> str:
        if not model.economic_report_id:
            return "missing"
        report = await self._session.get(EconomicReport, model.economic_report_id)
        if report is None:
            return "missing"
        conclusion = report.economic_conclusion or {}
        verdict = conclusion.get("verdict") if isinstance(conclusion, dict) else None
        return str(verdict or "unknown")

    def _lineage(
        self, model: ModelArtifact, generalization_report_id: str | None
    ) -> dict[str, str | None]:
        return {
            "statistical_report_id": model.statistical_report_id,
            "calibration_report_id": model.calibration_report_id,
            "economic_report_id": model.economic_report_id,
            "generalization_report_id": generalization_report_id,
        }

    def _staleness_reasons(self, input_staleness_seconds: int) -> list[str]:
        if input_staleness_seconds > self._guardrails.max_input_staleness_seconds:
            return ["STALE_INPUT"]
        return []

    def _emit_time_domain_reasons(
        self, model: ModelArtifact, inference_input: InferenceInput
    ) -> list[str]:
        domain = model.operating_domain or {}
        checks = [
            ("providers", inference_input.provider),
            ("symbols", inference_input.symbol),
            ("sources", inference_input.source),
        ]
        for key, value in checks:
            allowed = set(domain.get(key, []))
            if allowed and value not in allowed:
                return ["UNSUPPORTED_DOMAIN"]
        return []

    def _calibrated_confidence(
        self, raw_score: float, calibration: CalibrationReport | None
    ) -> float | None:
        if calibration is None:
            return None
        bin_scheme = calibration.bin_scheme or {}
        bin_count = int(bin_scheme.get("bin_count") or len(calibration.bins or []) or 1)
        index = min(max(int(raw_score * bin_count), 0), max(bin_count - 1, 0))
        for item in calibration.bins or []:
            if int(item.get("bin", -1)) == index and int(item.get("count", 0)) > 0:
                return float(item.get("observed_rate", item.get("avg_confidence", 0.0)))
        try:
            return float(calibration.base_rate)
        except (TypeError, ValueError):
            return None

    def _calibration_status(
        self,
        calibration: CalibrationReport | None,
        inference_input: InferenceInput,
    ) -> str:
        if calibration is None:
            return "missing"
        warnings = [str(item) for item in (calibration.warnings or [])]
        if self._ece_value(calibration.expected_calibration_error) > (
            self._guardrails.calibration_warning_ece_threshold
        ):
            warnings.append("POORLY_CALIBRATED")
        if self._slice_ece_warns(calibration, inference_input):
            warnings.append("POORLY_CALIBRATED")
        if warnings:
            return "warning:" + ",".join(self._unique(warnings))
        return "calibrated"

    def _slice_ece_warns(
        self,
        calibration: CalibrationReport,
        inference_input: InferenceInput,
    ) -> bool:
        per_slice = calibration.per_slice or {}
        for field in ("market_class", "timeframe", "regime"):
            value = getattr(inference_input, field)
            field_slices = per_slice.get(field, {}) if isinstance(per_slice, dict) else {}
            slice_payload = field_slices.get(value) if isinstance(field_slices, dict) else None
            if isinstance(slice_payload, dict):
                if self._ece_value(slice_payload.get("ece")) > (
                    self._guardrails.calibration_warning_ece_threshold
                ):
                    return True
        return False

    def _ece_value(self, value: Any) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    def _warning_reasons(self, calibration_status: str, economic_verdict: str) -> list[str]:
        reasons: list[str] = []
        if calibration_status.startswith("warning"):
            reasons.extend(calibration_status.removeprefix("warning:").split(","))
        if self._economic_is_unusable(economic_verdict):
            reasons.append("ECONOMICALLY_UNUSABLE")
        return self._unique([reason for reason in reasons if reason])

    def _economic_is_unusable(self, economic_verdict: str) -> bool:
        verdict = economic_verdict.lower()
        return "unusable" in verdict or "negative" in verdict or "loss" in verdict

    def _apply_expiry(
        self,
        *,
        pre_expiry_state: SignalState,
        transitions: list[str],
        expires_at,
        now,
    ) -> SignalState:
        transitions.append(pre_expiry_state)
        if pre_expiry_state in {"emitted", "warning"} and expires_at <= now:
            transitions.append("expired")
            return "expired"
        return pre_expiry_state

    def _classification(self, calibrated_confidence: float | None) -> str:
        if calibrated_confidence is None:
            return "unavailable"
        if calibrated_confidence >= 0.55:
            return "positive_bias"
        if calibrated_confidence <= 0.45:
            return "negative_bias"
        return "neutral_bias"

    def _domain_status(self, reasons: list[str]) -> str:
        if "UNSUPPORTED_DOMAIN" in reasons:
            return "unsupported"
        if reasons and "STALE_INPUT" not in reasons:
            return "not_eligible"
        return "valid"

    def _risk_notes(
        self,
        risk_notes: str | None,
        calibration_status: str,
        economic_verdict: str,
        eligibility_reasons: list[str],
        freshness_status: str,
    ) -> str | None:
        notes: list[str] = []
        if risk_notes and risk_notes.strip():
            notes.append(risk_notes.strip())
        if calibration_status.startswith("warning"):
            notes.append(f"Calibration warning: {calibration_status.removeprefix('warning:')}")
        if self._economic_is_unusable(economic_verdict):
            notes.append(f"Economic warning: {economic_verdict}")
        if freshness_status in {"stale", "expired"}:
            notes.append(f"Freshness warning: {freshness_status}")
        if eligibility_reasons:
            notes.append("Signal reason: " + ",".join(eligibility_reasons))
        return " | ".join(notes) if notes else None

    def _explainability_summary(
        self,
        *,
        model: ModelArtifact,
        inference_input: InferenceInput,
        input_hash: str,
        signal_state: str,
        state_reason: str,
        raw_score: float | None,
        calibrated_confidence: float | None,
        signal_direction: str,
        operating_domain_status: str,
        calibration_status: str,
        economic_verdict: str,
        eligibility_reasons: list[str],
        rationale: str,
        input_staleness_seconds: int,
        signal_validity_seconds: int,
        expires_at,
        freshness_status: str,
    ) -> dict[str, Any]:
        return {
            "model": {
                "model_artifact_id": model.id,
                "model_version": model.version,
                "experiment_id": model.experiment_id,
                "feature_set_version": model.feature_set_version,
            },
            "input": {
                "as_of_time": inference_input.as_of_time.isoformat(),
                "market_class": inference_input.market_class,
                "provider": inference_input.provider,
                "symbol": inference_input.symbol,
                "timeframe": inference_input.timeframe,
                "regime": inference_input.regime,
                "source": inference_input.source,
                "inference_input_hash": input_hash,
            },
            "why": {
                "signal_state": signal_state,
                "state_reason": state_reason,
                "rationale": rationale,
                "eligibility_reasons": eligibility_reasons,
            },
            "confidence": {
                "raw_score_recorded_for_audit": raw_score,
                "calibrated_confidence": calibrated_confidence,
                "calibration_status": calibration_status,
                "confidence_source": "calibration_report_bins_or_base_rate",
            },
            "domain": {"operating_domain_status": operating_domain_status},
            "economic": {"economic_verdict": economic_verdict},
            "freshness": {
                "freshness_status": freshness_status,
                "input_staleness_seconds": input_staleness_seconds,
                "max_input_staleness_seconds": self._guardrails.max_input_staleness_seconds,
                "signal_validity_seconds": signal_validity_seconds,
                "expires_at": expires_at.isoformat() if expires_at else None,
            },
            "classification": {"signal_direction": signal_direction},
            "limitations": [
                "advisory_record_only",
                "no_order_payload",
                "no_automatic_action",
                "human_governed_review_required",
            ],
        }

    def _unique(self, values: list[str]) -> list[str]:
        output: list[str] = []
        for value in values:
            if value and value not in output:
                output.append(value)
        return output
