"""Simulated paper research ledger service (W6-U03)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.time import utc_now
from app.db.models.simulated_execution import SimulatedExecutionRun, SimulatedFillEvent
from app.db.models.simulated_paper_ledger import SimulatedPaperLedgerEntry
from app.execution_research.contracts import (
    RESEARCH_STATUS,
    SIMULATED_EXECUTION_RESEARCH_DISCLAIMER,
    SIMULATION_MODE,
)
from app.repositories.audit_repository import AuditRepository


@dataclass(frozen=True, slots=True)
class SimulatedPaperLedgerEntryDraft:
    """Research-only ledger draft over an existing simulated fill."""

    run_id: str
    simulated_fill_id: str
    simulated_exit_value: float
    ledger_event_type: str = "simulated_close_estimate"
    uncertainty_width: float = 0.0001


class SimulatedPaperLedgerService:
    """Creates and reads simulated paper research ledger entries."""

    method_version = "w6-u03.simulated_paper_ledger.v1"

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._audit = AuditRepository(session)

    async def create_entry(
        self,
        *,
        draft: SimulatedPaperLedgerEntryDraft,
        operator_id: str,
    ) -> SimulatedPaperLedgerEntry:
        if draft.ledger_event_type not in {"simulated_close_estimate", "simulated_review_mark"}:
            raise ValueError("SIMULATED_LEDGER_EVENT_TYPE_INVALID")
        run = await self._session.get(SimulatedExecutionRun, draft.run_id)
        if run is None or run.simulation_mode != SIMULATION_MODE:
            raise ValueError("SIMULATED_LEDGER_RUN_REQUIRED")
        fill = await self._session.get(SimulatedFillEvent, draft.simulated_fill_id)
        if fill is None or fill.simulation_mode != SIMULATION_MODE:
            raise ValueError("SIMULATED_LEDGER_FILL_REQUIRED")
        if fill.run_id != run.run_id:
            raise ValueError("SIMULATED_LEDGER_FILL_RUN_MISMATCH")
        entry_value = float(fill.simulated_fill_price)
        exit_value = float(draft.simulated_exit_value)
        if entry_value <= 0 or exit_value <= 0:
            raise ValueError("SIMULATED_LEDGER_VALUES_MUST_BE_POSITIVE")
        estimate = (exit_value - entry_value) / entry_value
        width = abs(float(draft.uncertainty_width))
        if width <= 0:
            width = max(abs(estimate) * 0.1, 0.0001)
        entry = SimulatedPaperLedgerEntry(
            ledger_entry_id=str(uuid4()),
            created_at=utc_now(),
            simulation_mode=SIMULATION_MODE,
            run_id=run.run_id,
            simulated_fill_id=fill.simulated_fill_id,
            operator_id=operator_id,
            ledger_event_type=draft.ledger_event_type,
            simulated_research_direction=fill.simulated_research_direction,
            simulated_units=fill.simulated_units,
            simulated_entry_value=round(entry_value, 10),
            simulated_exit_value=round(exit_value, 10),
            simulated_return_estimate=round(estimate, 10),
            uncertainty={
                "method": "fixed_simulated_estimate_band",
                "lower": round(estimate - width, 10),
                "upper": round(estimate + width, 10),
                "sample_count": 1,
                "basis": "single_simulated_fill_research_estimate",
            },
            limitations=[
                "simulated_research_only",
                "not_live_instruction",
                "not_real_profit_loss",
                "not_financial_advice",
                "single_fill_estimate_with_uncertainty",
            ],
            research_status=RESEARCH_STATUS,
            simulation_disclaimer=SIMULATED_EXECUTION_RESEARCH_DISCLAIMER,
            audit_correlation_id=str(uuid4()),
        )
        self._session.add(entry)
        await self._session.flush()
        await self._append_entry_audit(entry)
        return entry

    async def list_entries(self, *, limit: int = 50) -> Sequence[SimulatedPaperLedgerEntry]:
        stmt = (
            select(SimulatedPaperLedgerEntry)
            .order_by(SimulatedPaperLedgerEntry.created_at.desc())
            .limit(limit)
        )
        return list((await self._session.scalars(stmt)).all())

    async def get_entry(self, ledger_entry_id: str) -> SimulatedPaperLedgerEntry | None:
        return await self._session.get(SimulatedPaperLedgerEntry, ledger_entry_id)

    async def _append_entry_audit(self, entry: SimulatedPaperLedgerEntry) -> None:
        event = await self._audit.append(
            category="GOVERNANCE",
            action="simulated_paper_ledger_entry.created",
            actor=entry.operator_id,
            resource_type="simulated_paper_ledger_entry",
            resource_id=entry.ledger_entry_id,
            message="Simulated paper research ledger entry created",
            details={
                "simulation_mode": entry.simulation_mode,
                "research_status": entry.research_status,
                "run_id": entry.run_id,
                "simulated_fill_id": entry.simulated_fill_id,
                "simulated_return_estimate": entry.simulated_return_estimate,
                "uncertainty": entry.uncertainty,
                "method_version": self.method_version,
                "simulation_only": True,
            },
            correlation_id=entry.audit_correlation_id,
        )
        if event is None:
            raise RuntimeError("SIMULATED_PAPER_LEDGER_AUDIT_FAILED")
