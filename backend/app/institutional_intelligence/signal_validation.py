"""Professional signal validation reports (W4-U06)."""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.time import coerce_external_utc, require_utc, utc_now
from app.db.models.advisory_signal import AdvisorySignal
from app.db.models.model_artifact import ModelArtifact
from app.db.models.signal_validation_report import SignalValidationReport
from app.institutional_intelligence.contracts import (
    IntelligenceArtifactDraft,
    IntelligenceArtifactFactory,
)
from app.repositories.audit_repository import AuditRepository


@dataclass(frozen=True, slots=True)
class SignalValidationScope:
    scope_start: datetime
    scope_end: datetime
    market_class: str | None = None
    symbol: str | None = None
    timeframe: str | None = None
    include_states: tuple[str, ...] = ("emitted", "warning", "withheld", "expired")


@dataclass(frozen=True, slots=True)
class SignalValidationComputationResult:
    report: SignalValidationReport
    excluded_future_signal_count: int


class SignalValidationReportService:
    """Creates persisted, audited professional signal-validation reports."""

    method_version = "w4-u06.signal_validation.v1"

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._audit = AuditRepository(session)
        self._factory = IntelligenceArtifactFactory()

    async def create_report(
        self,
        *,
        scope: SignalValidationScope,
        actor: str = "system",
    ) -> SignalValidationComputationResult:
        start = require_utc(scope.scope_start, boundary="signal_validation.scope_start")
        end = require_utc(scope.scope_end, boundary="signal_validation.scope_end")
        assert start is not None and end is not None
        if start > end:
            raise ValueError("SIGNAL_VALIDATION_SCOPE_INVALID")
        if end > utc_now():
            raise ValueError("SIGNAL_VALIDATION_FUTURE_SCOPE_REFUSED")
        signals = await self._signals(scope, start, end)
        if not signals:
            raise ValueError("SIGNAL_VALIDATION_EMPTY_SCOPE")
        future_count = await self._future_count(scope, end)
        metrics = self._metrics(signals)
        uncertainty = {
            "method": "wilson_score_intervals",
            "confidence_level": 0.95,
            "sample_count": len(signals),
            "metrics": {key: value["uncertainty"] for key, value in metrics.items()},
        }
        outcome_data_status = {
            "status": "not_available",
            "reason": (
                "Governed forward outcome labels are not present in W4-U06; validation is limited "
                "to persisted advisory state, guardrail, freshness, "
                "and calibrated-confidence coverage."
            ),
        }
        economic_usefulness = {
            "verdict": "not_assessed",
            "reason": (
                "Signal quality validation is research context and not an "
                "economic/trading claim."
            ),
        }
        source_signal_ids = [signal.signal_id for signal in signals]
        results = {
            "metrics": metrics,
            "outcome_data_status": outcome_data_status,
            "economic_usefulness": economic_usefulness,
            "excluded_future_signal_count": future_count,
        }
        validation_scope = self._scope_payload(scope, start, end)
        draft = IntelligenceArtifactDraft(
            artifact_type="signal_validation_report",
            method_version=self.method_version,
            config={
                "scope": validation_scope,
                "metric_policy": "full_declared_scope_no_cherry_picking",
                "model_score_policy": "uncalibrated_score_excluded_from_validation_output",
            },
            input_lineage={
                "source": "advisory_signals",
                "scope": validation_scope,
                "source_signal_ids": source_signal_ids,
                "excluded_future_signal_count": future_count,
                "uncalibrated_model_score_excluded": True,
            },
            source_artifact_ids=source_signal_ids,
            market_scope={
                "market_class": scope.market_class,
                "symbol": scope.symbol,
                "timeframe": scope.timeframe,
            },
            as_of_start=start,
            as_of_end=end,
            sample_count=len(signals),
            uncertainty=uncertainty,
            results=results,
            limitations=[
                "historical_research_only",
                "not_a_guarantee",
                "not_a_prediction",
                "not_financial_advice",
                "uncalibrated_model_score_excluded",
                "no_governed_forward_outcomes_available",
                "economic_usefulness_not_assessed",
            ],
            created_by=actor,
        )
        artifact = self._factory.build(draft)
        report = SignalValidationReport(
            id=artifact.artifact_id,
            created_at=artifact.created_at,
            artifact_type=artifact.artifact_type,
            method_version=artifact.method_version,
            scope_start=start,
            scope_end=end,
            sample_count=artifact.sample_count,
            metrics=metrics,
            uncertainty=artifact.uncertainty,
            validation_scope=validation_scope,
            outcome_data_status=outcome_data_status,
            economic_usefulness=economic_usefulness,
            config=artifact.config,
            input_lineage=artifact.input_lineage,
            source_signal_ids=source_signal_ids,
            market_scope=artifact.market_scope,
            results=artifact.results,
            limitations=list(artifact.limitations),
            report_hash=artifact.report_hash,
            research_status=artifact.research_status,
            created_by=artifact.created_by,
            audit_correlation_id=artifact.audit_correlation_id,
            notes=(
                "Historical advisory signal validation; uncalibrated score excluded; "
                "no forward outcomes fabricated."
            ),
        )
        self._session.add(report)
        await self._session.flush()
        await self._audit.append(
            category="GOVERNANCE",
            action="signal_validation_report.created",
            actor=actor,
            resource_type="signal_validation_report",
            resource_id=report.id,
            message=f"Signal validation report created sample_count={report.sample_count}",
            details=artifact.to_audit_details(),
            correlation_id=report.audit_correlation_id,
        )
        return SignalValidationComputationResult(
            report=report, excluded_future_signal_count=future_count
        )

    async def list_reports(self, *, limit: int = 50) -> list[SignalValidationReport]:
        result = await self._session.scalars(
            select(SignalValidationReport).order_by(SignalValidationReport.created_at.desc()).limit(limit)
        )
        return list(result.all())

    async def get_report(self, report_id: str) -> SignalValidationReport | None:
        return await self._session.get(SignalValidationReport, report_id)

    async def assert_no_side_effects(
        self, *, model_statuses: dict[str, str], signal_count: int
    ) -> None:
        signals = list((await self._session.scalars(select(AdvisorySignal))).all())
        if len(signals) != signal_count:
            raise AssertionError("SIGNAL_VALIDATION_SIGNAL_SIDE_EFFECT")
        for model_id, status in model_statuses.items():
            model = await self._session.get(ModelArtifact, model_id)
            if model is not None and model.status != status:
                raise AssertionError("SIGNAL_VALIDATION_MODEL_MUTATION")

    async def _signals(
        self,
        scope: SignalValidationScope,
        start: datetime,
        end: datetime,
    ) -> list[AdvisorySignal]:
        stmt = select(AdvisorySignal).where(
            AdvisorySignal.as_of_time >= start,
            AdvisorySignal.as_of_time <= end,
        )
        if scope.market_class:
            stmt = stmt.where(AdvisorySignal.market_class == scope.market_class)
        if scope.symbol:
            stmt = stmt.where(AdvisorySignal.symbol == scope.symbol)
        if scope.timeframe:
            stmt = stmt.where(AdvisorySignal.timeframe == scope.timeframe)
        if scope.include_states:
            stmt = stmt.where(AdvisorySignal.signal_state.in_(scope.include_states))
        stmt = stmt.order_by(AdvisorySignal.as_of_time.asc(), AdvisorySignal.created_at.asc())
        return list((await self._session.scalars(stmt)).all())

    async def _future_count(self, scope: SignalValidationScope, end: datetime) -> int:
        from sqlalchemy import func

        stmt = (
            select(func.count())
            .select_from(AdvisorySignal)
            .where(AdvisorySignal.as_of_time > end)
        )
        if scope.market_class:
            stmt = stmt.where(AdvisorySignal.market_class == scope.market_class)
        if scope.symbol:
            stmt = stmt.where(AdvisorySignal.symbol == scope.symbol)
        if scope.timeframe:
            stmt = stmt.where(AdvisorySignal.timeframe == scope.timeframe)
        return int((await self._session.execute(stmt)).scalar_one())

    def _metrics(self, signals: Sequence[AdvisorySignal]) -> dict[str, dict[str, object]]:
        total = len(signals)
        emitted = sum(1 for signal in signals if signal.signal_state == "emitted")
        guardrailed = sum(
            1
            for signal in signals
            if signal.signal_state in {"warning", "withheld", "expired"}
        )
        with_calibrated_confidence = sum(
            1 for signal in signals if signal.calibrated_confidence is not None
        )
        return {
            "clean_advisory_rate": self._rate(emitted, total),
            "guardrail_intervention_rate": self._rate(guardrailed, total),
            "calibrated_confidence_coverage": self._rate(with_calibrated_confidence, total),
        }

    def _rate(self, numerator: int, denominator: int) -> dict[str, object]:
        value = numerator / denominator if denominator else 0.0
        return {
            "value": value,
            "sample_count": denominator,
            "uncertainty": self._wilson(numerator, denominator),
        }

    def _wilson(self, numerator: int, denominator: int) -> dict[str, object]:
        if denominator <= 0:
            return {
                "method": "wilson_score_interval",
                "lower": 0.0,
                "upper": 0.0,
                "confidence_level": 0.95,
                "sample_count": 0,
            }
        z = 1.96
        n = float(denominator)
        p = numerator / n
        denom = 1.0 + (z * z / n)
        centre = p + (z * z / (2.0 * n))
        margin = z * math.sqrt((p * (1.0 - p) / n) + (z * z / (4.0 * n * n)))
        return {
            "method": "wilson_score_interval",
            "lower": max(0.0, (centre - margin) / denom),
            "upper": min(1.0, (centre + margin) / denom),
            "confidence_level": 0.95,
            "sample_count": denominator,
        }

    def _scope_payload(
        self,
        scope: SignalValidationScope,
        start: datetime,
        end: datetime,
    ) -> dict[str, object]:
        return {
            "scope_start": start.isoformat(),
            "scope_end": end.isoformat(),
            "market_class": scope.market_class,
            "symbol": scope.symbol,
            "timeframe": scope.timeframe,
            "include_states": list(scope.include_states),
        }

    def normalize_signal_time(self, signal: AdvisorySignal) -> datetime:
        value = coerce_external_utc(signal.as_of_time, source="signal_validation.as_of_time")
        assert value is not None
        return value
