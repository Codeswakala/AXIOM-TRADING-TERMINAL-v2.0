"""Simulated execution analytics and performance-comparison reports (W6-U06)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Sequence
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.time import utc_now
from app.db.models.execution_experiment import ExecutionResearchExperiment
from app.db.models.simulated_execution import SimulatedFillEvent
from app.db.models.simulated_execution_analytics_report import SimulatedExecutionAnalyticsReport
from app.db.models.simulated_paper_ledger import SimulatedPaperLedgerEntry
from app.execution_research.contracts import (
    RESEARCH_STATUS,
    SIMULATED_EXECUTION_RESEARCH_DISCLAIMER,
    SIMULATION_MODE,
)
from app.repositories.audit_repository import AuditRepository


@dataclass(frozen=True, slots=True)
class SimulatedExecutionAnalyticsReportDraft:
    """Declared full scope for a simulated analytics report."""

    source_artifact_ids: tuple[str, ...]
    analytics_type: str = "return_estimate"


@dataclass(frozen=True, slots=True)
class _ResolvedAnalyticsInputs:
    fills: tuple[SimulatedFillEvent, ...]
    ledger_entries: tuple[SimulatedPaperLedgerEntry, ...]
    experiments: tuple[ExecutionResearchExperiment, ...]


class SimulatedExecutionAnalyticsReportService:
    """Creates simulated execution analytics reports without actuation."""

    method_version = "w6-u06.simulated_execution_analytics.v1"
    allowed_analytics_types = {
        "slippage_distribution",
        "return_estimate",
        "fill_model_comparison",
        "replay_scope_comparison",
    }

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._audit = AuditRepository(session)

    async def create_report(
        self,
        *,
        draft: SimulatedExecutionAnalyticsReportDraft,
        actor: str = "system",
    ) -> SimulatedExecutionAnalyticsReport:
        if draft.analytics_type not in self.allowed_analytics_types:
            raise ValueError("SIMULATED_ANALYTICS_TYPE_INVALID")
        declared_ids = self._dedupe(draft.source_artifact_ids)
        if not declared_ids:
            raise ValueError("SIMULATED_ANALYTICS_SOURCE_ARTIFACT_REQUIRED")
        resolved = await self._resolve_inputs(declared_ids)
        analyzed_ids = self._analyzed_ids(resolved)
        if set(analyzed_ids) != set(declared_ids):
            raise ValueError("SIMULATED_ANALYTICS_SCOPE_MISMATCH")
        slippage_values = [fill.simulated_slippage_bps for fill in resolved.fills]
        return_values = [entry.simulated_return_estimate for entry in resolved.ledger_entries]
        experiment_count = len(resolved.experiments)
        metrics = {
            "simulated_fill_count": {
                "value": len(resolved.fills),
                "unit": "count",
                "sample_count": len(resolved.fills),
            },
            "simulated_average_slippage_bps": {
                "value": self._average(slippage_values),
                "unit": "basis_points",
                "sample_count": len(slippage_values),
            },
            "simulated_average_return_estimate": {
                "value": self._average(return_values),
                "unit": "dimensionless_research_estimate",
                "sample_count": len(return_values),
            },
            "simulated_experiment_count": {
                "value": experiment_count,
                "unit": "count",
                "sample_count": experiment_count,
            },
        }
        uncertainty = {
            "method": "per_metric_interval_or_insufficient_sample_limitation",
            "metrics": {
                "simulated_fill_count": self._uncertainty_count(len(resolved.fills)),
                "simulated_average_slippage_bps": self._uncertainty_range(slippage_values),
                "simulated_average_return_estimate": self._uncertainty_range(return_values),
                "simulated_experiment_count": self._uncertainty_count(experiment_count),
            },
        }
        included_scope = {
            "declared_source_artifact_ids": list(declared_ids),
            "analyzed_source_artifact_ids": list(analyzed_ids),
            "simulated_fill_ids": [fill.simulated_fill_id for fill in resolved.fills],
            "simulated_ledger_entry_ids": [
                entry.ledger_entry_id for entry in resolved.ledger_entries
            ],
            "execution_experiment_ids": [
                exp.experiment_id for exp in resolved.experiments
            ],
            "comparison_groups": self._comparison_groups(resolved),
            "full_scope_included": True,
        }
        report_hash = self.compute_report_hash(
            analytics_type=draft.analytics_type,
            included_scope=included_scope,
            source_artifact_ids=tuple(declared_ids),
        )
        report = SimulatedExecutionAnalyticsReport(
            report_id=str(uuid4()),
            created_at=utc_now(),
            simulation_mode=SIMULATION_MODE,
            analytics_type=draft.analytics_type,
            included_scope=included_scope,
            sample_count=len(declared_ids),
            metrics=metrics,
            uncertainty=uncertainty,
            limitations=[
                "simulated_execution_research_only",
                "not_live_instruction",
                "not_real_p_and_l",
                "not_financial_advice",
                "full_declared_scope_included",
                "economic_usefulness_not_assessed",
            ],
            economic_usefulness={
                "verdict": "not_assessed",
                "reason": (
                    "Simulated analytics are statistical research summaries and do not establish "
                    "economic usefulness or live execution suitability."
                ),
            },
            report_hash=report_hash,
            source_artifact_ids=list(declared_ids),
            research_status=RESEARCH_STATUS,
            simulation_disclaimer=SIMULATED_EXECUTION_RESEARCH_DISCLAIMER,
            audit_correlation_id=str(uuid4()),
        )
        self._session.add(report)
        await self._session.flush()
        await self._append_report_audit(report)
        return report

    def compute_report_hash(
        self,
        *,
        analytics_type: str,
        included_scope: dict[str, object],
        source_artifact_ids: tuple[str, ...],
    ) -> str:
        payload = {
            "analytics_type": analytics_type,
            "included_scope": included_scope,
            "method_version": self.method_version,
            "source_artifact_ids": list(source_artifact_ids),
        }
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
        return hashlib.sha256(encoded.encode("utf-8")).hexdigest()

    async def list_reports(self, *, limit: int = 50) -> Sequence[SimulatedExecutionAnalyticsReport]:
        stmt = (
            select(SimulatedExecutionAnalyticsReport)
            .order_by(SimulatedExecutionAnalyticsReport.created_at.desc())
            .limit(limit)
        )
        return list((await self._session.scalars(stmt)).all())

    async def get_report(self, report_id: str) -> SimulatedExecutionAnalyticsReport | None:
        return await self._session.get(SimulatedExecutionAnalyticsReport, report_id)

    async def _resolve_inputs(self, ids: Sequence[str]) -> _ResolvedAnalyticsInputs:
        fills: list[SimulatedFillEvent] = []
        ledgers: list[SimulatedPaperLedgerEntry] = []
        experiments: list[ExecutionResearchExperiment] = []
        unresolved: list[str] = []
        for item in ids:
            fill = await self._session.get(SimulatedFillEvent, item)
            if fill is not None:
                fills.append(fill)
                continue
            ledger = await self._session.get(SimulatedPaperLedgerEntry, item)
            if ledger is not None:
                ledgers.append(ledger)
                continue
            experiment = await self._session.get(ExecutionResearchExperiment, item)
            if experiment is not None:
                experiments.append(experiment)
                continue
            unresolved.append(item)
        if unresolved:
            raise ValueError("SIMULATED_ANALYTICS_UNRESOLVED_SOURCE_ARTIFACT")
        return _ResolvedAnalyticsInputs(
            fills=tuple(fills),
            ledger_entries=tuple(ledgers),
            experiments=tuple(experiments),
        )

    def _analyzed_ids(self, resolved: _ResolvedAnalyticsInputs) -> tuple[str, ...]:
        return tuple(
            sorted(
                [fill.simulated_fill_id for fill in resolved.fills]
                + [entry.ledger_entry_id for entry in resolved.ledger_entries]
                + [experiment.experiment_id for experiment in resolved.experiments]
            )
        )

    def _comparison_groups(self, resolved: _ResolvedAnalyticsInputs) -> dict[str, list[str]]:
        return {
            "simulated_fills": [fill.simulated_fill_id for fill in resolved.fills],
            "simulated_ledger_entries": [
                entry.ledger_entry_id for entry in resolved.ledger_entries
            ],
            "execution_experiments": [
                experiment.experiment_id for experiment in resolved.experiments
            ],
        }

    def _dedupe(self, values: Sequence[str]) -> tuple[str, ...]:
        return tuple(sorted({value for value in values if value}))

    def _average(self, values: Sequence[float]) -> float | None:
        return round(float(sum(values) / len(values)), 10) if values else None

    def _uncertainty_count(self, count: int) -> dict[str, object]:
        if count <= 1:
            return {
                "method": "insufficient_sample_limitation",
                "sample_count": count,
                "limitation": "Count metric has insufficient sample size for interval estimation.",
            }
        return {"method": "observed_count", "sample_count": count, "lower": count, "upper": count}

    def _uncertainty_range(self, values: Sequence[float]) -> dict[str, object]:
        if not values:
            return {
                "method": "insufficient_samples",
                "sample_count": 0,
                "limitation": "No simulated observations available for this metric.",
            }
        if len(values) == 1:
            return {
                "method": "insufficient_sample_limitation",
                "lower": round(values[0], 10),
                "upper": round(values[0], 10),
                "sample_count": 1,
                "limitation": "Single simulated observation; no confidence interval inferred.",
            }
        return {
            "method": "observed_range",
            "lower": round(min(values), 10),
            "upper": round(max(values), 10),
            "sample_count": len(values),
        }

    async def _append_report_audit(self, report: SimulatedExecutionAnalyticsReport) -> None:
        event = await self._audit.append(
            category="GOVERNANCE",
            action="simulated_execution_analytics_report.created",
            actor="system",
            resource_type="simulated_execution_analytics_report",
            resource_id=report.report_id,
            message="Simulated execution analytics report created from full declared scope",
            details={
                "simulation_mode": report.simulation_mode,
                "analytics_type": report.analytics_type,
                "research_status": report.research_status,
                "report_hash": report.report_hash,
                "sample_count": report.sample_count,
                "method_version": self.method_version,
                "simulation_only": True,
            },
            correlation_id=report.audit_correlation_id,
        )
        if event is None:
            raise RuntimeError("SIMULATED_EXECUTION_ANALYTICS_REPORT_AUDIT_FAILED")
