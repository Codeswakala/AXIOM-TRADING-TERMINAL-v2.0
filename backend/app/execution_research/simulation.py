"""Deterministic simulated execution run and fill services (W6-U02)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Sequence
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.time import coerce_external_utc, require_utc, utc_now
from app.db.models.candle import Candle
from app.db.models.simulated_execution import SimulatedExecutionRun, SimulatedFillEvent
from app.execution_research.contracts import (
    EXECUTION_RESEARCH_POLICY_VERSION,
    RESEARCH_STATUS,
    SIMULATED_EXECUTION_RESEARCH_DISCLAIMER,
    SIMULATION_MODE,
)
from app.repositories.audit_repository import AuditRepository

FILL_MODEL_NAME = "deterministic_mid_close_slippage"
FILL_MODEL_VERSION = "w6-u02.fill_model.v1"


@dataclass(frozen=True, slots=True)
class SimulatedExecutionRunSpec:
    """Research-only simulated execution run request."""

    market_class: str
    symbol: str
    timeframe: str
    as_of_start: datetime
    as_of_end: datetime
    simulated_research_direction: str = "long_bias"
    simulated_units: float = 1.0
    simulated_slippage_bps: float = 0.0
    max_fill_events: int = 5
    input_artifact_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class SimulatedFillPreview:
    """Deterministic fill-model output before persistence."""

    market_class: str
    symbol: str
    timeframe: str
    as_of_time: datetime
    simulated_research_direction: str
    simulated_units: float
    requested_reference_price: float
    simulated_fill_price: float
    simulated_slippage_bps: float
    source_candle_ids: tuple[str, ...]
    fill_model_name: str
    fill_model_version: str


@dataclass(frozen=True, slots=True)
class SimulatedExecutionCreationResult:
    run: SimulatedExecutionRun
    fills: tuple[SimulatedFillEvent, ...]


class DeterministicSimulatedFillModel:
    """Deterministic fill model over persisted replay candles."""

    name = FILL_MODEL_NAME
    version = FILL_MODEL_VERSION

    def preview(
        self,
        *,
        spec: SimulatedExecutionRunSpec,
        candles: Sequence[Candle],
    ) -> tuple[SimulatedFillPreview, ...]:
        direction = self._direction(spec.simulated_research_direction)
        units = self._units(spec.simulated_units)
        slippage_bps = float(spec.simulated_slippage_bps)
        output: list[SimulatedFillPreview] = []
        for candle in candles[: spec.max_fill_events]:
            as_of_time = coerce_external_utc(candle.open_time, source="simulated_fill.as_of_time")
            assert as_of_time is not None
            reference = float(candle.close)
            slip = reference * (slippage_bps / 10_000.0)
            fill_price = reference + slip if direction == "long_bias" else reference - slip
            output.append(
                SimulatedFillPreview(
                    market_class=candle.market_class,
                    symbol=candle.symbol,
                    timeframe=candle.timeframe,
                    as_of_time=as_of_time,
                    simulated_research_direction=direction,
                    simulated_units=units,
                    requested_reference_price=round(reference, 10),
                    simulated_fill_price=round(fill_price, 10),
                    simulated_slippage_bps=slippage_bps,
                    source_candle_ids=(candle.id,),
                    fill_model_name=self.name,
                    fill_model_version=self.version,
                )
            )
        return tuple(output)

    def _direction(self, value: str) -> str:
        if value not in {"long_bias", "short_bias", "neutral_research"}:
            raise ValueError("SIMULATED_DIRECTION_INVALID")
        return value

    def _units(self, value: float) -> float:
        units = float(value)
        if units <= 0:
            raise ValueError("SIMULATED_UNITS_MUST_BE_POSITIVE")
        return units


class SimulatedExecutionService:
    """Creates and reads simulated execution research artifacts."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._audit = AuditRepository(session)
        self._fill_model = DeterministicSimulatedFillModel()

    async def create_run(
        self,
        *,
        spec: SimulatedExecutionRunSpec,
        operator_id: str,
    ) -> SimulatedExecutionCreationResult:
        start = require_utc(spec.as_of_start, boundary="simulated_execution.as_of_start")
        end = require_utc(spec.as_of_end, boundary="simulated_execution.as_of_end")
        assert start is not None and end is not None
        if start > end:
            raise ValueError("SIMULATED_REPLAY_SCOPE_INVALID")
        if spec.max_fill_events < 1:
            raise ValueError("SIMULATED_MAX_FILL_EVENTS_INVALID")
        candles = await self._candles(spec, start, end)
        if not candles:
            raise ValueError("SIMULATED_REPLAY_REQUIRES_CANDLES")
        previews = self._fill_model.preview(spec=spec, candles=candles)
        if not previews:
            raise ValueError("SIMULATED_FILL_PREVIEW_EMPTY")
        correlation_id = str(uuid4())
        now = utc_now()
        run = SimulatedExecutionRun(
            run_id=str(uuid4()),
            created_at=now,
            operator_id=operator_id,
            simulation_mode=SIMULATION_MODE,
            simulation_policy_version=EXECUTION_RESEARCH_POLICY_VERSION,
            input_artifact_ids=list(spec.input_artifact_ids),
            replay_scope={
                "market_class": spec.market_class,
                "symbol": spec.symbol,
                "timeframe": spec.timeframe,
                "as_of_start": start.isoformat(),
                "as_of_end": end.isoformat(),
                "included_candle_ids": [candle.id for candle in candles[: spec.max_fill_events]],
            },
            fill_model_name=self._fill_model.name,
            fill_model_version=self._fill_model.version,
            assumptions={
                "simulated_research_direction": spec.simulated_research_direction,
                "simulated_units_dimensionless": float(spec.simulated_units),
                "simulated_slippage_bps": float(spec.simulated_slippage_bps),
                "max_fill_events": spec.max_fill_events,
                "deterministic": True,
            },
            limitations=[
                "simulated_research_only",
                "not_live_instruction",
                "not_real_profit_loss",
                "not_financial_advice",
                "no_broker_or_account_linkage",
            ],
            research_status=RESEARCH_STATUS,
            simulation_disclaimer=SIMULATED_EXECUTION_RESEARCH_DISCLAIMER,
            audit_correlation_id=correlation_id,
        )
        self._session.add(run)
        await self._session.flush()
        await self._append_run_audit(run)

        fills: list[SimulatedFillEvent] = []
        for preview in previews:
            fill = SimulatedFillEvent(
                simulated_fill_id=str(uuid4()),
                run_id=run.run_id,
                created_at=now,
                simulation_mode=SIMULATION_MODE,
                market_class=preview.market_class,
                symbol=preview.symbol,
                timeframe=preview.timeframe,
                as_of_time=preview.as_of_time,
                simulated_research_direction=preview.simulated_research_direction,
                simulated_units=preview.simulated_units,
                requested_reference_price=preview.requested_reference_price,
                simulated_fill_price=preview.simulated_fill_price,
                simulated_slippage_bps=preview.simulated_slippage_bps,
                source_candle_ids=list(preview.source_candle_ids),
                fill_model_name=preview.fill_model_name,
                fill_model_version=preview.fill_model_version,
                research_status=RESEARCH_STATUS,
                simulation_disclaimer=SIMULATED_EXECUTION_RESEARCH_DISCLAIMER,
                audit_correlation_id=str(uuid4()),
            )
            self._session.add(fill)
            fills.append(fill)
        await self._session.flush()
        for fill in fills:
            await self._append_fill_audit(fill)
        return SimulatedExecutionCreationResult(run=run, fills=tuple(fills))

    async def list_runs(self, *, limit: int = 50) -> list[SimulatedExecutionRun]:
        stmt = (
            select(SimulatedExecutionRun)
            .order_by(SimulatedExecutionRun.created_at.desc())
            .limit(limit)
        )
        return list((await self._session.scalars(stmt)).all())

    async def get_run(self, run_id: str) -> SimulatedExecutionRun | None:
        return await self._session.get(SimulatedExecutionRun, run_id)

    async def list_fills(
        self, *, run_id: str | None = None, limit: int = 100
    ) -> list[SimulatedFillEvent]:
        stmt = select(SimulatedFillEvent)
        if run_id is not None:
            stmt = stmt.where(SimulatedFillEvent.run_id == run_id)
        stmt = stmt.order_by(SimulatedFillEvent.as_of_time.asc()).limit(limit)
        return list((await self._session.scalars(stmt)).all())

    async def get_fill(self, fill_id: str) -> SimulatedFillEvent | None:
        return await self._session.get(SimulatedFillEvent, fill_id)

    async def _candles(
        self,
        spec: SimulatedExecutionRunSpec,
        start: datetime,
        end: datetime,
    ) -> list[Candle]:
        stmt = (
            select(Candle)
            .where(
                Candle.market_class == spec.market_class,
                Candle.symbol == spec.symbol,
                Candle.timeframe == spec.timeframe,
                Candle.open_time >= start,
                Candle.open_time <= end,
            )
            .order_by(Candle.open_time.asc())
        )
        return list((await self._session.scalars(stmt)).all())

    async def _append_run_audit(self, run: SimulatedExecutionRun) -> None:
        event = await self._audit.append(
            category="GOVERNANCE",
            action="simulated_execution_run.created",
            actor=run.operator_id,
            resource_type="simulated_execution_run",
            resource_id=run.run_id,
            message="Simulated execution research run created",
            details={
                "simulation_mode": run.simulation_mode,
                "research_status": run.research_status,
                "simulation_policy_version": run.simulation_policy_version,
                "fill_model_name": run.fill_model_name,
                "fill_model_version": run.fill_model_version,
                "operator_id": run.operator_id,
                "simulation_only": True,
            },
            correlation_id=run.audit_correlation_id,
        )
        if event is None:
            raise RuntimeError("SIMULATED_EXECUTION_RUN_AUDIT_FAILED")

    async def _append_fill_audit(self, fill: SimulatedFillEvent) -> None:
        event = await self._audit.append(
            category="GOVERNANCE",
            action="simulated_fill_event.created",
            actor="system",
            resource_type="simulated_fill_event",
            resource_id=fill.simulated_fill_id,
            message="Simulated fill event created by deterministic research model",
            details={
                "run_id": fill.run_id,
                "simulation_mode": fill.simulation_mode,
                "research_status": fill.research_status,
                "fill_model_name": fill.fill_model_name,
                "fill_model_version": fill.fill_model_version,
                "simulated_units_dimensionless": fill.simulated_units,
                "simulation_only": True,
            },
            correlation_id=fill.audit_correlation_id,
        )
        if event is None:
            raise RuntimeError("SIMULATED_FILL_EVENT_AUDIT_FAILED")
