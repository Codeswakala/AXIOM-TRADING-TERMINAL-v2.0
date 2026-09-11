"""Trade replay and execution experiment pre-registration (W6-U05)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from typing import Sequence
from uuid import uuid4

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.time import require_utc, utc_now
from app.db.models.candle import Candle
from app.db.models.execution_experiment import ExecutionResearchExperiment
from app.db.models.simulated_execution import SimulatedExecutionRun, SimulatedFillEvent
from app.db.models.simulated_paper_ledger import SimulatedPaperLedgerEntry
from app.execution_research.contracts import (
    RESEARCH_STATUS,
    SIMULATED_EXECUTION_RESEARCH_DISCLAIMER,
    SIMULATION_MODE,
)
from app.repositories.audit_repository import AuditRepository


@dataclass(frozen=True, slots=True)
class ExecutionResearchExperimentDraft:
    """Pre-registered simulated replay experiment draft."""

    experiment_title: str
    hypothesis: str
    market_class: str
    symbol: str
    timeframe: str
    as_of_start: datetime
    as_of_time: datetime
    input_artifact_ids: tuple[str, ...]
    max_candles: int = 100


class ExecutionResearchExperimentService:
    """Registers immutable simulated execution experiments and replays frozen inputs."""

    method_version = "w6-u05.execution_experiment.v1"

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._audit = AuditRepository(session)

    async def register_and_replay(
        self,
        *,
        draft: ExecutionResearchExperimentDraft,
        operator_id: str,
    ) -> ExecutionResearchExperiment:
        title = draft.experiment_title.strip()
        hypothesis = draft.hypothesis.strip()
        if not title:
            raise ValueError("EXECUTION_EXPERIMENT_TITLE_REQUIRED")
        if not hypothesis:
            raise ValueError("EXECUTION_EXPERIMENT_HYPOTHESIS_REQUIRED")
        start = require_utc(draft.as_of_start, boundary="execution_experiment.as_of_start")
        as_of = require_utc(draft.as_of_time, boundary="execution_experiment.as_of_time")
        assert start is not None and as_of is not None
        if start > as_of:
            raise ValueError("EXECUTION_EXPERIMENT_AS_OF_WINDOW_INVALID")
        if draft.max_candles < 1:
            raise ValueError("EXECUTION_EXPERIMENT_MAX_CANDLES_INVALID")
        if not draft.input_artifact_ids:
            raise ValueError("EXECUTION_EXPERIMENT_INPUT_ARTIFACT_REQUIRED")

        resolved = await self._resolve_artifacts(draft.input_artifact_ids)
        candles = await self._bounded_candles(draft, start, as_of)
        if not candles:
            raise ValueError("EXECUTION_EXPERIMENT_REPLAY_REQUIRES_CANDLES")
        future_count = await self._future_count(draft, as_of)
        replay_scope = {
            "market_class": draft.market_class,
            "symbol": draft.symbol,
            "timeframe": draft.timeframe,
            "as_of_start": start.isoformat(),
            "as_of_time": as_of.isoformat(),
            "max_candles": draft.max_candles,
        }
        pre_registration_plan = {
            "experiment_title": title,
            "hypothesis": hypothesis,
            "replay_scope": replay_scope,
            "input_artifact_ids": list(draft.input_artifact_ids),
            "method_version": self.method_version,
            "simulation_mode": SIMULATION_MODE,
        }
        plan_hash = self.compute_plan_hash(pre_registration_plan)
        included_candle_ids = [candle.id for candle in candles]
        included_times = [candle.open_time.isoformat() for candle in candles]
        lineage = {
            "included_candle_ids": included_candle_ids,
            "included_candle_open_times": included_times,
            "excluded_future_candle_count": future_count,
            "simulated_run_ids": resolved["run_ids"],
            "simulated_fill_ids": resolved["fill_ids"],
            "simulated_ledger_entry_ids": resolved["ledger_ids"],
            "source_policy": "as_of_bounded_frozen_replay_inputs",
        }
        uncertainty = {
            "method": "replay_scope_count_limitation",
            "sample_count": len(candles),
            "limitations": [
                "uncertainty_is_scope_descriptive_for_pre_registered_replay",
                "no_statistical_interval_in_safety_unit",
            ],
        }
        experiment = ExecutionResearchExperiment(
            experiment_id=str(uuid4()),
            created_at=utc_now(),
            simulation_mode=SIMULATION_MODE,
            operator_id=operator_id,
            experiment_title=title,
            pre_registration_plan=pre_registration_plan,
            plan_hash=plan_hash,
            as_of_time=as_of,
            as_of_window={
                "as_of_start": start.isoformat(),
                "as_of_time": as_of.isoformat(),
            },
            replay_input_lineage=lineage,
            included_scope_summary={
                "declared_replay_scope": replay_scope,
                "executed_replay_scope": replay_scope,
                "included_candle_count": len(candles),
                "input_artifact_count": len(draft.input_artifact_ids),
            },
            uncertainty=uncertainty,
            limitations=[
                "simulated_execution_research_only",
                "not_live_instruction",
                "not_real_profit_loss",
                "not_financial_advice",
                "pre_registered_scope_not_cherry_picked",
                "as_of_bounded_no_future_rows",
            ],
            research_status=RESEARCH_STATUS,
            simulation_disclaimer=SIMULATED_EXECUTION_RESEARCH_DISCLAIMER,
            audit_correlation_id=str(uuid4()),
        )
        self._session.add(experiment)
        await self._session.flush()
        await self._append_experiment_audit(experiment)
        return experiment

    def compute_plan_hash(self, plan: dict[str, object]) -> str:
        encoded = json.dumps(plan, sort_keys=True, separators=(",", ":"), default=str)
        return hashlib.sha256(encoded.encode("utf-8")).hexdigest()

    async def list_experiments(self, *, limit: int = 50) -> Sequence[ExecutionResearchExperiment]:
        stmt = (
            select(ExecutionResearchExperiment)
            .order_by(ExecutionResearchExperiment.created_at.desc())
            .limit(limit)
        )
        return list((await self._session.scalars(stmt)).all())

    async def get_experiment(self, experiment_id: str) -> ExecutionResearchExperiment | None:
        return await self._session.get(ExecutionResearchExperiment, experiment_id)

    async def _bounded_candles(
        self,
        draft: ExecutionResearchExperimentDraft,
        start: datetime,
        as_of: datetime,
    ) -> list[Candle]:
        stmt = (
            select(Candle)
            .where(
                Candle.market_class == draft.market_class,
                Candle.symbol == draft.symbol,
                Candle.timeframe == draft.timeframe,
                Candle.open_time >= start,
                Candle.open_time <= as_of,
            )
            .order_by(Candle.open_time.asc())
            .limit(draft.max_candles)
        )
        return list((await self._session.scalars(stmt)).all())

    async def _future_count(self, draft: ExecutionResearchExperimentDraft, as_of: datetime) -> int:
        stmt = (
            select(func.count())
            .select_from(Candle)
            .where(
                Candle.market_class == draft.market_class,
                Candle.symbol == draft.symbol,
                Candle.timeframe == draft.timeframe,
                Candle.open_time > as_of,
            )
        )
        return int((await self._session.execute(stmt)).scalar_one())

    async def _resolve_artifacts(self, ids: Sequence[str]) -> dict[str, list[str]]:
        run_ids: list[str] = []
        fill_ids: list[str] = []
        ledger_ids: list[str] = []
        unresolved: list[str] = []
        for item in ids:
            run = await self._session.get(SimulatedExecutionRun, item)
            if run is not None:
                run_ids.append(run.run_id)
                continue
            fill = await self._session.get(SimulatedFillEvent, item)
            if fill is not None:
                fill_ids.append(fill.simulated_fill_id)
                if fill.run_id not in run_ids:
                    run_ids.append(fill.run_id)
                continue
            ledger = await self._session.get(SimulatedPaperLedgerEntry, item)
            if ledger is not None:
                ledger_ids.append(ledger.ledger_entry_id)
                if ledger.run_id not in run_ids:
                    run_ids.append(ledger.run_id)
                if ledger.simulated_fill_id not in fill_ids:
                    fill_ids.append(ledger.simulated_fill_id)
                continue
            unresolved.append(item)
        if unresolved:
            raise ValueError("EXECUTION_EXPERIMENT_UNRESOLVED_INPUT_ARTIFACT")
        return {"run_ids": run_ids, "fill_ids": fill_ids, "ledger_ids": ledger_ids}

    async def _append_experiment_audit(self, experiment: ExecutionResearchExperiment) -> None:
        event = await self._audit.append(
            category="GOVERNANCE",
            action="execution_research_experiment.created",
            actor=experiment.operator_id,
            resource_type="execution_research_experiment",
            resource_id=experiment.experiment_id,
            message="Pre-registered simulated execution research experiment created",
            details={
                "simulation_mode": experiment.simulation_mode,
                "research_status": experiment.research_status,
                "plan_hash": experiment.plan_hash,
                "as_of_time": experiment.as_of_time.isoformat(),
                "method_version": self.method_version,
                "simulation_only": True,
            },
            correlation_id=experiment.audit_correlation_id,
        )
        if event is None:
            raise RuntimeError("EXECUTION_RESEARCH_EXPERIMENT_AUDIT_FAILED")
