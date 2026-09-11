"""BE-7 U-5 endpoints (BO §1; C3/C4).

GET-only reads + the enumerated governed writers: register-input,
register-cost-model, register-strategy, submit-job, run-job, cancel-job.
NO generic job-update endpoint exists (C3). RESEARCH-mode writers.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.operator import Operator
from app.db.models.v2_research_jobs import (
    V2BacktestInput,
    V2ResearchJob,
    V2ResearchJobAttempt,
    V2ResearchResult,
)
from app.db.session import get_db_session
from app.v2.identifiers import new_id
from app.v2.marketdata.repositories import (
    V2MdBarReadBoundary,
    V2MdReferenceRepository,
)
from app.v2.rbac.dependencies import require_v2_permission
from app.v2.research_jobs.leakage import (
    LeakageRefused,
    ReplayWindow,
    content_hash,
    filter_bars_g1,
)
from app.v2.research_jobs.queue import JobSubmission, cancel_job, submit_job
from app.v2.research_jobs.registry import (
    register_cost_model,
    register_input,
    register_strategy,
)
from app.v2.research_jobs.runner import _utc_from_store, run_job
from app.v2.temporal.validation import require_utc, utc_now

router = APIRouter(prefix="/research-jobs", tags=["V2 Research Jobs"])

RequireJobsRead = Annotated[
    Operator, Depends(require_v2_permission("v2.research.jobs.read"))]
RequireJobsSubmit = Annotated[
    Operator, Depends(require_v2_permission("v2.research.jobs.submit"))]
RequireJobsCancel = Annotated[
    Operator, Depends(require_v2_permission("v2.research.jobs.cancel"))]
RequireRegistryRead = Annotated[
    Operator, Depends(require_v2_permission("v2.research.registry.read"))]
RequireRegistryWrite = Annotated[
    Operator, Depends(require_v2_permission("v2.research.registry.write"))]
RequireResultsRead = Annotated[
    Operator, Depends(require_v2_permission("v2.research.results.read"))]


def _envelope(request: Request) -> dict:
    return {"mode": request.app.state.v2_mode,
            "correlation_id": getattr(request.state, "correlation_id", None),
            "timestamp": datetime.now(timezone.utc)}


def _require_research(request: Request) -> str:
    mode = request.app.state.v2_mode
    if mode != "RESEARCH":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Writer not permitted in this mode")
    return mode


def _cid(request: Request) -> str:
    return getattr(request.state, "correlation_id", None) or new_id()


# --- request models -------------------------------------------------------------


class InputRegistration(BaseModel):
    input_id: str = Field(min_length=1, max_length=64)
    instrument_id: str
    timeframe: str = "M15"
    source_id: str = "sim.local"
    window_start: datetime
    window_end: datetime
    data_class: str = "simulated"
    bar_limit: int = Field(default=500, ge=10, le=1000)


class CostModelRegistration(BaseModel):
    cost_model_id: str = Field(min_length=1, max_length=64)
    spread: dict
    commission: dict
    slippage: dict
    latency_ms: int = Field(ge=0)
    risk_limits: dict = Field(default_factory=dict)
    data_class: str = "simulated"


class StrategyRegistration(BaseModel):
    strategy_id: str = Field(min_length=1, max_length=64)
    name: str
    parameters: dict
    lifecycle_state: str = "registered"
    data_class: str = "simulated"


class JobSubmitRequest(BaseModel):
    authorization_ref: str = Field(min_length=1)
    inputs: dict
    schedule: dict = Field(default_factory=lambda: {"kind": "manual"})
    data_class: str = "simulated"


class JobRunRequest(BaseModel):
    job_id: str


class JobCancelRequest(BaseModel):
    job_id: str
    reason: str = Field(min_length=1)


# --- governed writers -------------------------------------------------------------


@router.post("/registry/inputs")
async def api_register_input(
    body: InputRegistration, request: Request,
    operator: RequireRegistryWrite,
    session: AsyncSession = Depends(get_db_session)) -> dict:
    mode = _require_research(request)
    require_utc(body.window_start, boundary="window_start")
    require_utc(body.window_end, boundary="window_end")
    now = utc_now()
    if body.window_end > now:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="window_end may not be in the future")
    ref_repo = V2MdReferenceRepository(session)
    instrument = await ref_repo.get_instrument(body.instrument_id)
    source = await ref_repo.get_source(body.source_id)
    if instrument is None or source is None or not source.active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Instrument or source not found")
    boundary = V2MdBarReadBoundary(session)
    rows = await boundary.read_bars(
        market_class=instrument.market_class,
        symbol=instrument.display_symbol,
        timeframe=body.timeframe.upper(),
        as_of=body.window_end, limit=body.bar_limit)
    rows = [r for r in rows if r.source == source.authority]
    bars = [{"open_time": _utc_from_store(r.open_time), "open": r.open,
             "high": r.high,
             "low": r.low, "close": r.close,
             "volume": getattr(r, "volume", 0)} for r in rows]
    window = ReplayWindow(window_start=body.window_start,
                          window_end=body.window_end,
                          as_of=body.window_end)
    series_refs = {"instrument_id": body.instrument_id,
                   "timeframe": body.timeframe.upper(),
                   "source_id": body.source_id,
                   "table": "candles via V2MdBarReadBoundary"}
    try:
        assembled = filter_bars_g1(bars, window)
    except LeakageRefused as exc:
        # typed refusal through the registration writer's refusal path
        # (durable audit — C-1 law), never an unhandled 500
        outcome = await register_input(
            session, input_id=body.input_id, content_hash="",
            series_refs={}, window_start=body.window_start,
            window_end=body.window_end, data_class=body.data_class,
            mode=mode, operator_id=operator.username,
            correlation_id=_cid(request))
        return {"outcome": "refused",
                "record_id": None,
                "reasons": exc.reasons + outcome.reasons,
                "content_hash": None, "bars_registered": 0,
                **_envelope(request)}
    ch = content_hash(assembled, window, series_refs)
    outcome = await register_input(
        session, input_id=body.input_id, content_hash=ch,
        series_refs=series_refs, window_start=body.window_start,
        window_end=body.window_end, data_class=body.data_class,
        mode=mode, operator_id=operator.username,
        correlation_id=_cid(request))
    return {"outcome": outcome.outcome, "record_id": outcome.record_id,
            "reasons": outcome.reasons, "content_hash": ch,
            "bars_registered": len(assembled), **_envelope(request)}


@router.post("/registry/cost-models")
async def api_register_cost_model(
    body: CostModelRegistration, request: Request,
    operator: RequireRegistryWrite,
    session: AsyncSession = Depends(get_db_session)) -> dict:
    mode = _require_research(request)
    outcome = await register_cost_model(
        session, cost_model_id=body.cost_model_id, spread=body.spread,
        commission=body.commission, slippage=body.slippage,
        latency_ms=body.latency_ms, risk_limits=body.risk_limits,
        data_class=body.data_class, mode=mode,
        operator_id=operator.username, correlation_id=_cid(request))
    return {"outcome": outcome.outcome, "record_id": outcome.record_id,
            "reasons": outcome.reasons, **_envelope(request)}


@router.post("/registry/strategies")
async def api_register_strategy(
    body: StrategyRegistration, request: Request,
    operator: RequireRegistryWrite,
    session: AsyncSession = Depends(get_db_session)) -> dict:
    mode = _require_research(request)
    outcome = await register_strategy(
        session, strategy_id=body.strategy_id, name=body.name,
        parameters=body.parameters, lifecycle_state=body.lifecycle_state,
        data_class=body.data_class, mode=mode,
        operator_id=operator.username, correlation_id=_cid(request))
    return {"outcome": outcome.outcome, "record_id": outcome.record_id,
            "reasons": outcome.reasons, **_envelope(request)}


@router.post("/jobs/submit")
async def api_submit_job(
    body: JobSubmitRequest, request: Request,
    operator: RequireJobsSubmit,
    session: AsyncSession = Depends(get_db_session)) -> dict:
    mode = _require_research(request)
    outcome = await submit_job(session, JobSubmission(
        owner=operator.username,
        authorization_ref=body.authorization_ref,
        inputs=body.inputs, schedule=body.schedule,
        data_class=body.data_class, mode=mode,
        operator_id=operator.username, correlation_id=_cid(request)))
    return {"outcome": outcome.outcome, "job_id": outcome.record_id,
            "reasons": outcome.reasons, **_envelope(request)}


@router.post("/jobs/run")
async def api_run_job(
    body: JobRunRequest, request: Request,
    operator: RequireJobsSubmit,
    session: AsyncSession = Depends(get_db_session)) -> dict:
    """Manual invocation (v1 scope) — the ONLY execution trigger."""
    _require_research(request)  # mode gate; the job row carries its own mode
    job = (await session.execute(
        select(V2ResearchJob).where(V2ResearchJob.id == body.job_id)
    )).scalar_one_or_none()
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Job not found")
    registry = (await session.execute(
        select(V2BacktestInput).where(
            V2BacktestInput.id == job.inputs.get("input_registry_id"))
    )).scalar_one_or_none()
    bars: list[dict] = []
    if registry is not None:
        ref_repo = V2MdReferenceRepository(session)
        instrument = await ref_repo.get_instrument(
            registry.series_refs["instrument_id"])
        source = await ref_repo.get_source(registry.series_refs["source_id"])
        if instrument is not None and source is not None:
            boundary = V2MdBarReadBoundary(session)
            rows = await boundary.read_bars(
                market_class=instrument.market_class,
                symbol=instrument.display_symbol,
                timeframe=registry.series_refs["timeframe"],
                as_of=_utc_from_store(registry.window_end), limit=1000)
            rows = [r for r in rows if r.source == source.authority]
            bars = [{"open_time": _utc_from_store(r.open_time),
                     "open": r.open,
                     "high": r.high, "low": r.low, "close": r.close,
                     "volume": getattr(r, "volume", 0)} for r in rows]
    result = await run_job(session, job_id=body.job_id,
                           actor_id=operator.username, bars=bars,
                           correlation_id=_cid(request))
    return {**result, **_envelope(request)}


@router.post("/jobs/cancel")
async def api_cancel_job(
    body: JobCancelRequest, request: Request,
    operator: RequireJobsCancel,
    session: AsyncSession = Depends(get_db_session)) -> dict:
    mode = _require_research(request)
    outcome = await cancel_job(session, job_id=body.job_id,
                               actor_id=operator.username,
                               reason=body.reason, mode=mode,
                               correlation_id=_cid(request))
    return {"outcome": outcome.outcome, "reasons": outcome.reasons,
            **_envelope(request)}


# --- reads (GET only) ---------------------------------------------------------------


@router.get("/jobs")
async def list_jobs(
    request: Request, operator: RequireJobsRead,
    job_state: str | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
    session: AsyncSession = Depends(get_db_session)) -> dict:
    stmt = select(V2ResearchJob).order_by(V2ResearchJob.created_at.desc())
    if job_state is not None:
        stmt = stmt.where(V2ResearchJob.job_state == job_state)
    rows = list((await session.execute(stmt.limit(limit))).scalars().all())
    return {"jobs": [{
        "id": r.id, "owner": r.owner,
        "authorization_ref": r.authorization_ref, "inputs": r.inputs,
        "schedule": r.schedule, "job_state": r.job_state,
        "attempt_count": r.attempt_count, "output_ref": r.output_ref,
        "failure": r.failure, "data_class": r.data_class,
    } for r in rows], "total": len(rows), **_envelope(request)}


@router.get("/jobs/{job_id}/attempts")
async def list_attempts(
    job_id: str, request: Request, operator: RequireJobsRead,
    session: AsyncSession = Depends(get_db_session)) -> dict:
    rows = list((await session.execute(
        select(V2ResearchJobAttempt)
        .where(V2ResearchJobAttempt.job_id == job_id)
        .order_by(V2ResearchJobAttempt.attempt_index))).scalars().all())
    return {"attempts": [{
        "attempt_index": r.attempt_index, "outcome": r.outcome,
        "artifact_ref": r.artifact_ref, "reason": r.reason,
        "actor_id": r.actor_id,
    } for r in rows], "total": len(rows), **_envelope(request)}


@router.get("/results")
async def list_results(
    request: Request, operator: RequireResultsRead,
    result_class: str | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
    session: AsyncSession = Depends(get_db_session)) -> dict:
    stmt = select(V2ResearchResult).order_by(
        V2ResearchResult.created_at.desc())
    if result_class is not None:
        stmt = stmt.where(V2ResearchResult.result_class == result_class)
    rows = list((await session.execute(stmt.limit(limit))).scalars().all())
    return {"results": [{
        "id": r.id, "result_class": r.result_class, "job_id": r.job_id,
        "attempt_index": r.attempt_index,
        "strategy_version_id": r.strategy_version_id,
        "input_registry_id": r.input_registry_id,
        "cost_model_id": r.cost_model_id, "inputs_hash": r.inputs_hash,
        "engine_versions": r.engine_versions,
        "summary": r.summary, "time_basis": r.time_basis,
        "data_class": r.data_class,
    } for r in rows], "total": len(rows), **_envelope(request)}
