"""Execution risk research report service (W6-U04)."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Sequence
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.time import utc_now
from app.db.models.execution_risk_report import ExecutionRiskResearchReport
from app.db.models.simulated_execution import SimulatedExecutionRun, SimulatedFillEvent
from app.db.models.simulated_paper_ledger import SimulatedPaperLedgerEntry
from app.execution_research.contracts import (
    RESEARCH_STATUS,
    SIMULATED_EXECUTION_RESEARCH_DISCLAIMER,
    SIMULATION_MODE,
)
from app.repositories.audit_repository import AuditRepository


@dataclass(frozen=True, slots=True)
class ExecutionRiskResearchReportDraft:
    """Input references for a simulated execution-risk report."""

    input_artifact_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class _ResolvedInputs:
    runs: tuple[SimulatedExecutionRun, ...]
    fills: tuple[SimulatedFillEvent, ...]
    ledger_entries: tuple[SimulatedPaperLedgerEntry, ...]


class ExecutionRiskResearchReportService:
    """Creates simulated execution-risk research reports without actuation."""

    method_version = "w6-u04.execution_risk_report.v1"

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._audit = AuditRepository(session)

    async def create_report(
        self,
        *,
        draft: ExecutionRiskResearchReportDraft,
        actor: str = "system",
    ) -> ExecutionRiskResearchReport:
        if not draft.input_artifact_ids:
            raise ValueError("EXECUTION_RISK_INPUT_ARTIFACT_REQUIRED")
        resolved = await self._resolve_inputs(draft.input_artifact_ids)
        if not (resolved.runs or resolved.fills or resolved.ledger_entries):
            raise ValueError("EXECUTION_RISK_NO_SUPPORTED_INPUT_ARTIFACTS")
        fill_count = len(resolved.fills)
        ledger_count = len(resolved.ledger_entries)
        slippage_values = [fill.simulated_slippage_bps for fill in resolved.fills]
        return_values = [entry.simulated_return_estimate for entry in resolved.ledger_entries]
        risk_metrics = {
            "simulated_fill_count": {
                "value": fill_count,
                "unit": "count",
                "description": "Number of simulated fill model outputs included.",
            },
            "simulated_average_slippage_bps": {
                "value": self._average(slippage_values),
                "unit": "basis_points",
                "sample_count": fill_count,
            },
            "simulated_max_abs_return_estimate": {
                "value": max((abs(value) for value in return_values), default=0.0),
                "unit": "dimensionless_research_estimate",
                "sample_count": ledger_count,
            },
            "simulated_ledger_entry_count": {
                "value": ledger_count,
                "unit": "count",
            },
        }
        sample_count = max(fill_count, ledger_count, 1)
        uncertainty = {
            "method": "sample_range_or_single_sample_limitation",
            "sample_count": sample_count,
            "metrics": {
                "simulated_average_slippage_bps": self._range(slippage_values),
                "simulated_return_estimate": self._range(return_values),
            },
            "limitations": [
                "uncertainty_is_descriptive_for_simulated_research_inputs",
                "small_samples_remain_low_confidence",
            ],
        }
        report = ExecutionRiskResearchReport(
            report_id=str(uuid4()),
            created_at=utc_now(),
            simulation_mode=SIMULATION_MODE,
            input_artifact_ids=list(draft.input_artifact_ids),
            simulated_request_summary={
                "run_ids": [run.run_id for run in resolved.runs],
                "simulated_fill_ids": [fill.simulated_fill_id for fill in resolved.fills],
                "ledger_entry_ids": [entry.ledger_entry_id for entry in resolved.ledger_entries],
                "method_version": self.method_version,
                "simulation_only": True,
            },
            risk_metrics=risk_metrics,
            uncertainty=uncertainty,
            limitations=[
                "simulated_execution_research_only",
                "not_live_instruction",
                "not_real_p_and_l",
                "not_financial_advice",
                "no_account_or_broker_linkage",
                "no_actuating_sizing_output",
                "economic_usefulness_not_assessed",
            ],
            economic_usefulness={
                "verdict": "not_assessed",
                "reason": (
                    "Structured risk metrics are simulated research measurements and do not "
                    "establish economic success or live execution suitability."
                ),
            },
            research_status=RESEARCH_STATUS,
            simulation_disclaimer=SIMULATED_EXECUTION_RESEARCH_DISCLAIMER,
            audit_correlation_id=str(uuid4()),
        )
        self._session.add(report)
        await self._session.flush()
        await self._append_report_audit(report)
        return report

    async def list_reports(self, *, limit: int = 50) -> Sequence[ExecutionRiskResearchReport]:
        stmt = (
            select(ExecutionRiskResearchReport)
            .order_by(ExecutionRiskResearchReport.created_at.desc())
            .limit(limit)
        )
        return list((await self._session.scalars(stmt)).all())

    async def get_report(self, report_id: str) -> ExecutionRiskResearchReport | None:
        return await self._session.get(ExecutionRiskResearchReport, report_id)

    async def _resolve_inputs(self, ids: Sequence[str]) -> _ResolvedInputs:
        runs: list[SimulatedExecutionRun] = []
        fills: list[SimulatedFillEvent] = []
        ledgers: list[SimulatedPaperLedgerEntry] = []
        unresolved: list[str] = []
        for item in ids:
            run = await self._session.get(SimulatedExecutionRun, item)
            if run is not None:
                runs.append(run)
                fills.extend(await self._fills_for_run(run.run_id))
                continue
            fill = await self._session.get(SimulatedFillEvent, item)
            if fill is not None:
                fills.append(fill)
                run_for_fill = await self._session.get(SimulatedExecutionRun, fill.run_id)
                if run_for_fill is not None and run_for_fill not in runs:
                    runs.append(run_for_fill)
                continue
            ledger = await self._session.get(SimulatedPaperLedgerEntry, item)
            if ledger is not None:
                ledgers.append(ledger)
                fill_for_ledger = await self._session.get(
                    SimulatedFillEvent, ledger.simulated_fill_id
                )
                if fill_for_ledger is not None and fill_for_ledger not in fills:
                    fills.append(fill_for_ledger)
                run_for_ledger = await self._session.get(SimulatedExecutionRun, ledger.run_id)
                if run_for_ledger is not None and run_for_ledger not in runs:
                    runs.append(run_for_ledger)
                continue
            unresolved.append(item)
        if unresolved:
            raise ValueError("EXECUTION_RISK_UNRESOLVED_INPUT_ARTIFACT")
        return _ResolvedInputs(runs=tuple(runs), fills=tuple(fills), ledger_entries=tuple(ledgers))

    async def _fills_for_run(self, run_id: str) -> list[SimulatedFillEvent]:
        stmt = select(SimulatedFillEvent).where(SimulatedFillEvent.run_id == run_id)
        return list((await self._session.scalars(stmt)).all())

    def _average(self, values: Sequence[float]) -> float | None:
        return round(float(mean(values)), 10) if values else None

    def _range(self, values: Sequence[float]) -> dict[str, object]:
        if not values:
            return {
                "method": "insufficient_samples",
                "sample_count": 0,
                "limitation": "No simulated observations available for this metric.",
            }
        if len(values) == 1:
            return {
                "method": "single_sample_no_interval",
                "lower": round(values[0], 10),
                "upper": round(values[0], 10),
                "sample_count": 1,
                "limitation": "Single simulated observation; interval width is not inferred.",
            }
        return {
            "method": "observed_range",
            "lower": round(min(values), 10),
            "upper": round(max(values), 10),
            "sample_count": len(values),
        }

    async def _append_report_audit(self, report: ExecutionRiskResearchReport) -> None:
        event = await self._audit.append(
            category="GOVERNANCE",
            action="execution_risk_research_report.created",
            actor="system",
            resource_type="execution_risk_research_report",
            resource_id=report.report_id,
            message="Execution risk research report created from simulated artifacts",
            details={
                "simulation_mode": report.simulation_mode,
                "research_status": report.research_status,
                "input_artifact_ids": report.input_artifact_ids,
                "method_version": self.method_version,
                "simulation_only": True,
                "economic_usefulness": report.economic_usefulness,
            },
            correlation_id=report.audit_correlation_id,
        )
        if event is None:
            raise RuntimeError("EXECUTION_RISK_RESEARCH_REPORT_AUDIT_FAILED")
