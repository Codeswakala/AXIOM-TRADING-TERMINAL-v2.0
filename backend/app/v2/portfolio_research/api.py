"""BE-6 U-3 endpoints (BO-V2-BE-6-001; plan §U-3).

Read-only surface + TWO governed writers (define-portfolio,
compute-risk-report) under ``/portfolio-research`` on the V2 aggregate
router. RESEARCH-mode writers; six BE-1 states; every artifact response
carries `basis_label='hypothetical-research'`. No credential anywhere.
"""

from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.operator import Operator
from app.db.models.v2_portfolio import (
    V2PortfolioDefinition,
    V2PortfolioRiskReport,
)
from app.db.session import get_db_session
from app.v2.audit.contract import V2AuditEventCreate
from app.v2.audit.repository import V2AuditRepository
from app.v2.identifiers import new_id
from app.v2.lineage.contract import V2LineageRecordCreate
from app.v2.lineage.repository import V2LineageRepository
from app.v2.marketdata.repositories import (
    V2MdBarReadBoundary,
    V2MdReferenceRepository,
)
from app.v2.portfolio_research.contracts import (
    PR_DATA_CLASSES,
    PR_FIRST_LANDING_DATA_CLASSES,
    validate_allocations,
    validate_assumptions,
)
from app.v2.portfolio_research.metrics import (
    CONFIDENCE_LEVEL,
    compute_concentration,
    compute_drawdown,
    compute_exposures,
    compute_factor_shares,
    compute_var,
    compute_volatility,
)
from app.v2.portfolio_research.scenarios import apply_scenarios
from app.v2.rbac.dependencies import require_v2_permission
from app.v2.temporal.validation import require_utc, utc_now

router = APIRouter(prefix="/portfolio-research", tags=["V2 Portfolio Research"])

RequirePortfolioRead = Annotated[
    Operator, Depends(require_v2_permission("v2.research.portfolio.read"))
]
RequirePortfolioDefine = Annotated[
    Operator, Depends(require_v2_permission("v2.research.portfolio.define"))
]
RequireRiskRead = Annotated[
    Operator, Depends(require_v2_permission("v2.research.portfolio_risk.read"))
]
RequireRiskCompute = Annotated[
    Operator, Depends(require_v2_permission("v2.research.portfolio_risk.compute"))
]

ENGINE_VERSIONS = {"portfolio_risk_engine": "pre-1.0.0"}


def _canonical(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)


def _engine_versions_hash() -> str:
    return hashlib.sha256(_canonical(ENGINE_VERSIONS).encode()).hexdigest()


def _envelope(request: Request) -> dict:
    return {
        "mode": request.app.state.v2_mode,
        "correlation_id": getattr(request.state, "correlation_id", None),
        "timestamp": datetime.now(timezone.utc),
    }


async def _audit_compute_refusal(
    session: AsyncSession, *, refusal_class: str, details: dict,
    mode: str, operator_id: str, correlation_id: str | None,
    status_code: int, detail: str,
) -> None:
    """C-1 (ITRGA_INT_V2_BE-6_DR_001 §5 route a): every compute-side
    refusal emits the plan-enumerated `portfolio_risk.compute.unknown`
    event with a typed refusal class, COMMITTED before the HTTP error is
    raised (the request dependency rolls back on exception — an uncommitted
    audit would vanish; BE-1 refusal-audit law requires durability)."""
    await V2AuditRepository(session).append(V2AuditEventCreate(
        domain="v2.portfolio_research",
        action="portfolio_risk.compute.unknown",
        actor_id=operator_id, actor_type="operator", mode=mode,
        details={"refusal_class": refusal_class, **details},
        operator_id=operator_id, correlation_id=correlation_id,
    ))
    await session.commit()
    raise HTTPException(status_code=status_code, detail=detail)


def _require_research(request: Request) -> str:
    mode = request.app.state.v2_mode
    if mode != "RESEARCH":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Writer not permitted in this mode")
    return mode


# --- models ------------------------------------------------------------------


class DefineRequest(BaseModel):
    portfolio_id: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=128)
    allocations: list[dict]
    base_currency: str = Field(default="USD", max_length=8)
    data_class: str
    assumptions: dict = Field(default_factory=dict)
    supersede: bool = False


class DefineResponse(BaseModel):
    definition_id: str | None
    portfolio_id: str
    record_seq: int | None
    accepted: bool
    reasons: list
    basis: str | None
    mode: str
    correlation_id: str | None
    timestamp: datetime


class ComputeRequest(BaseModel):
    portfolio_definition_id: str
    source_id: str = "sim.local"
    timeframe: str = "M15"
    bar_limit: int = Field(default=500, ge=10, le=1000)
    as_of: datetime | None = None
    scenarios: list[dict] = Field(default_factory=list)
    var_confidence: float | None = None  # defaults to the cited level


class ComputeResponse(BaseModel):
    report_id: str | None
    status: str
    basis_label: str | None
    reused_existing: bool
    insufficient_metrics: list
    mode: str
    correlation_id: str | None
    timestamp: datetime


# --- reads ---------------------------------------------------------------------


@router.get("/portfolios")
async def list_portfolios(
    request: Request,
    operator: RequirePortfolioRead,
    portfolio_id: str | None = Query(default=None),
    current_only: bool = Query(default=True),
    limit: int = Query(default=100, ge=1, le=500),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    stmt = select(V2PortfolioDefinition).order_by(
        V2PortfolioDefinition.portfolio_id,
        V2PortfolioDefinition.record_seq.desc())
    if portfolio_id is not None:
        stmt = stmt.where(V2PortfolioDefinition.portfolio_id == portfolio_id)
    if current_only:
        from sqlalchemy import func

        latest = (
            select(V2PortfolioDefinition.portfolio_id,
                   func.max(V2PortfolioDefinition.record_seq).label("max_seq"))
            .group_by(V2PortfolioDefinition.portfolio_id)
            .subquery()
        )
        stmt = stmt.join(
            latest,
            (V2PortfolioDefinition.portfolio_id == latest.c.portfolio_id)
            & (V2PortfolioDefinition.record_seq == latest.c.max_seq),
        )
    rows = list((await session.execute(stmt.limit(limit))).scalars().all())
    return {
        "portfolios": [{
            "id": r.id, "portfolio_id": r.portfolio_id,
            "record_seq": r.record_seq, "supersedes": r.supersedes,
            "name": r.name, "basis": r.basis,
            "allocations": r.allocations, "base_currency": r.base_currency,
            "data_class": r.data_class, "assumptions": r.assumptions,
        } for r in rows],
        "total": len(rows),
        **_envelope(request),
    }


@router.get("/risk-reports/{report_id}")
async def get_risk_report(
    report_id: str,
    request: Request,
    operator: RequireRiskRead,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    report = (await session.execute(
        select(V2PortfolioRiskReport).where(
            V2PortfolioRiskReport.id == report_id)
    )).scalar_one_or_none()
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Report not found")
    return {
        "id": report.id,
        "portfolio_definition_id": report.portfolio_definition_id,
        "as_of": report.as_of,
        "time_basis": report.time_basis,
        "input_refs": report.input_refs,
        "inputs_hash": report.inputs_hash,
        "metrics": report.metrics,
        "scenarios": report.scenarios,
        "status": report.status,
        "basis_label": report.basis_label,   # hypothetical-vs-account proof
        "data_class": report.data_class,
        "engine_versions": report.engine_versions,
        "engine_versions_hash": report.engine_versions_hash,
        **_envelope(request),
    }


@router.get("/risk-reports")
async def list_risk_reports(
    request: Request,
    operator: RequireRiskRead,
    portfolio_definition_id: str | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    stmt = select(V2PortfolioRiskReport).order_by(
        V2PortfolioRiskReport.created_at.desc())
    if portfolio_definition_id is not None:
        stmt = stmt.where(V2PortfolioRiskReport.portfolio_definition_id
                          == portfolio_definition_id)
    rows = list((await session.execute(stmt.limit(limit))).scalars().all())
    return {
        "reports": [{
            "id": r.id, "portfolio_definition_id": r.portfolio_definition_id,
            "status": r.status, "basis_label": r.basis_label,
            "data_class": r.data_class, "inputs_hash": r.inputs_hash,
        } for r in rows],
        "total": len(rows),
        **_envelope(request),
    }


# --- governed writer 1: define / supersede portfolio ------------------------------


@router.post("/portfolios/define", response_model=DefineResponse)
async def define_portfolio(
    body: DefineRequest,
    request: Request,
    operator: RequirePortfolioDefine,
    session: AsyncSession = Depends(get_db_session),
) -> DefineResponse:
    mode = _require_research(request)
    correlation_id = getattr(request.state, "correlation_id", None) or new_id()

    reasons: list = []
    ok_alloc, r1 = validate_allocations(body.allocations)
    reasons += r1
    ok_assume, r2 = validate_assumptions(body.assumptions)
    reasons += r2
    if body.data_class not in PR_DATA_CLASSES:
        reasons.append({"failing": "data_class", "value": body.data_class})
    elif body.data_class not in PR_FIRST_LANDING_DATA_CLASSES:
        reasons.append({
            "failing": "data_class", "value": body.data_class,
            "required": list(PR_FIRST_LANDING_DATA_CLASSES),
            "note": "corpus-gated (V2-TD-18 continuity)"})

    # instrument existence via the BE-2 registry (typed refusal, not 500)
    ref_repo = V2MdReferenceRepository(session)
    for a in body.allocations:
        iid = a.get("instrument_id")
        if iid and await ref_repo.get_instrument(iid) is None:
            reasons.append({"failing": "unknown_instrument", "value": iid})

    # versioning: existing generations?
    newest = (await session.execute(
        select(V2PortfolioDefinition)
        .where(V2PortfolioDefinition.portfolio_id == body.portfolio_id)
        .order_by(V2PortfolioDefinition.record_seq.desc())
    )).scalars().first()
    if newest is not None and not body.supersede:
        reasons.append({"failing": "portfolio_exists",
                        "required": "supersede=true to version"})

    if reasons:
        await V2AuditRepository(session).append(V2AuditEventCreate(
            domain="v2.portfolio_research", action="portfolio.define.refused",
            actor_id=operator.username, actor_type="operator", mode=mode,
            details={"portfolio_id": body.portfolio_id,
                     "reasons": reasons[:8]},
            operator_id=operator.username, correlation_id=correlation_id,
        ))
        return DefineResponse(
            definition_id=None, portfolio_id=body.portfolio_id,
            record_seq=None, accepted=False, reasons=reasons, basis=None,
            **_envelope(request))

    seq = 1 if newest is None else newest.record_seq + 1
    definition = V2PortfolioDefinition(
        portfolio_id=body.portfolio_id,
        record_seq=seq,
        supersedes=newest.id if newest is not None else None,
        name=body.name,
        basis="hypothetical",
        allocations=body.allocations,
        base_currency=body.base_currency,
        data_class=body.data_class,
        assumptions=body.assumptions,
        mode=mode,
        operator_id=operator.username,
        correlation_id=correlation_id,
    )
    session.add(definition)
    await session.flush()

    action = "portfolio.superseded" if newest is not None else "portfolio.defined"
    await V2AuditRepository(session).append(V2AuditEventCreate(
        domain="v2.portfolio_research", action=action,
        actor_id=operator.username, actor_type="operator", mode=mode,
        resource_type="portfolio_definition", resource_id=definition.id,
        details={"portfolio_id": body.portfolio_id, "record_seq": seq},
        operator_id=operator.username, correlation_id=correlation_id,
    ))
    await V2LineageRepository(session).append(V2LineageRecordCreate(
        artifact_type="portfolio_definition",
        artifact_id=definition.id,
        operator_id=operator.username,
        mode=mode,
        source_artifact_ids=[newest.id] if newest is not None else [],
        computation_version=None,
        input_snapshot_id=None,
    ))
    return DefineResponse(
        definition_id=definition.id, portfolio_id=body.portfolio_id,
        record_seq=seq, accepted=True, reasons=[], basis="hypothetical",
        **_envelope(request))


# --- governed writer 2: compute risk report ------------------------------------------


@router.post("/risk-reports/compute", response_model=ComputeResponse)
async def compute_risk_report(
    body: ComputeRequest,
    request: Request,
    operator: RequireRiskCompute,
    session: AsyncSession = Depends(get_db_session),
) -> ComputeResponse:
    mode = _require_research(request)
    correlation_id = getattr(request.state, "correlation_id", None) or new_id()
    now = utc_now()
    as_of = body.as_of or now
    require_utc(as_of, boundary="as_of")
    if as_of > now:
        await _audit_compute_refusal(
            session, refusal_class="as_of_in_future",
            details={"as_of": as_of.isoformat()},
            mode=mode, operator_id=operator.username,
            correlation_id=correlation_id,
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="as_of may not be in the future")
    confidence = body.var_confidence or CONFIDENCE_LEVEL

    definition = (await session.execute(
        select(V2PortfolioDefinition).where(
            V2PortfolioDefinition.id == body.portfolio_definition_id)
    )).scalar_one_or_none()
    if definition is None:
        await _audit_compute_refusal(
            session, refusal_class="definition_not_found",
            details={"portfolio_definition_id": body.portfolio_definition_id},
            mode=mode, operator_id=operator.username,
            correlation_id=correlation_id,
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio definition not found")
    # currency: greatest record_seq only
    newest = (await session.execute(
        select(V2PortfolioDefinition)
        .where(V2PortfolioDefinition.portfolio_id == definition.portfolio_id)
        .order_by(V2PortfolioDefinition.record_seq.desc())
    )).scalars().first()
    if newest is not None and newest.id != definition.id:
        await _audit_compute_refusal(
            session, refusal_class="definition_superseded",
            details={"portfolio_definition_id": definition.id,
                     "current_generation_id": newest.id},
            mode=mode, operator_id=operator.username,
            correlation_id=correlation_id,
            status_code=status.HTTP_409_CONFLICT,
            detail="Definition superseded — compute against"
                   " the current generation")

    # inputs: weighted portfolio value series from BE-2 bars (labelled synthetic)
    ref_repo = V2MdReferenceRepository(session)
    boundary = V2MdBarReadBoundary(session)
    source = await ref_repo.get_source(body.source_id)
    if source is None or not source.active:
        await _audit_compute_refusal(
            session, refusal_class="source_unknown_or_inactive",
            details={"source_id": body.source_id},
            mode=mode, operator_id=operator.username,
            correlation_id=correlation_id,
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Source not found or inactive")

    series: dict[str, list] = {}
    market_classes: dict[str, str] = {}
    for a in definition.allocations:
        instrument = await ref_repo.get_instrument(a["instrument_id"])
        if instrument is None:
            # C-1 cluster 2: dropped credited weight may NEVER be silent —
            # an instrument resolvable at definition time but not now is a
            # registry drift; typed refusal + durable audit, never a value
            # series that silently omits credited weight.
            await _audit_compute_refusal(
                session, refusal_class="unknown_instrument",
                details={"instrument_id": a["instrument_id"],
                         "credited_weight": a.get("weight"),
                         "portfolio_definition_id": definition.id},
                mode=mode, operator_id=operator.username,
                correlation_id=correlation_id,
                status_code=status.HTTP_409_CONFLICT,
                detail="Allocated instrument no longer resolvable —"
                       " supersede the definition")
        market_classes[a["instrument_id"]] = instrument.market_class
        rows = await boundary.read_bars(
            market_class=instrument.market_class,
            symbol=instrument.display_symbol,
            timeframe=body.timeframe.upper(),
            as_of=as_of, limit=body.bar_limit)
        rows = [r for r in rows if r.source == source.authority]
        series[a["instrument_id"]] = [(r.open_time, float(r.close)) for r in rows]

    # portfolio value series on the common timestamp intersection
    common: list = []
    if series and all(v for v in series.values()):
        ts_sets = [set(t for t, _ in v) for v in series.values()]
        common_ts = sorted(set.intersection(*ts_sets))
        closes = {iid: dict(v) for iid, v in series.items()}
        for ts in common_ts:
            value = sum(float(a["weight"]) * closes[a["instrument_id"]][ts]
                        / closes[a["instrument_id"]][common_ts[0]]
                        for a in definition.allocations
                        if a["instrument_id"] in closes)
            common.append((ts, value * 100.0))
    values = [v for _, v in common]
    returns = [math.log(values[i] / values[i - 1])
               for i in range(1, len(values))] if len(values) >= 2 else []

    input_refs = {
        "definition_id": definition.id,
        "source_id": body.source_id,
        "timeframe": body.timeframe.upper(),
        "series_lengths": {k: len(v) for k, v in series.items()},
        "common_observations": len(common),
    }
    inputs_hash = hashlib.sha256(_canonical({
        "allocations": definition.allocations,
        "values": [(t.isoformat(), v) for t, v in common],
        "scenarios": body.scenarios,
        "confidence": confidence,
    }).encode()).hexdigest()
    versions_hash = _engine_versions_hash()

    # idempotency via the determinism anchor
    existing = (await session.execute(
        select(V2PortfolioRiskReport).where(
            V2PortfolioRiskReport.portfolio_definition_id == definition.id,
            V2PortfolioRiskReport.inputs_hash == inputs_hash,
            V2PortfolioRiskReport.engine_versions_hash == versions_hash)
    )).scalar_one_or_none()
    if existing is not None:
        await V2AuditRepository(session).append(V2AuditEventCreate(
            domain="v2.portfolio_research",
            action="portfolio_risk.compute.reused",
            actor_id=operator.username, actor_type="operator", mode=mode,
            resource_type="portfolio_risk_report", resource_id=existing.id,
            details={"inputs_hash": inputs_hash},
            operator_id=operator.username, correlation_id=correlation_id,
        ))
        return ComputeResponse(
            report_id=existing.id, status=existing.status,
            basis_label=existing.basis_label, reused_existing=True,
            insufficient_metrics=[m["metric"] for m in existing.metrics
                                  if m.get("insufficient")],
            **_envelope(request))

    # compute all metrics (pure functions; typed insufficiency inside)
    metric_results = [
        compute_exposures(definition.allocations),
        compute_concentration(definition.allocations, top_n=3),
        compute_volatility(returns),
        compute_drawdown(values),
        compute_factor_shares(definition.allocations, market_classes),
    ]
    var_pair = compute_var(returns, confidence=confidence)
    metric_results += [var_pair["historical"], var_pair["parametric_normal"]]
    scenario_results = apply_scenarios(
        definition.allocations, market_classes, body.scenarios)

    metrics_json = [m.as_dict() for m in metric_results]
    scenarios_json = [s.as_dict() for s in scenario_results]
    insufficient = [m.metric for m in metric_results if m.insufficient]

    if not values:
        report_status = "unavailable"
    elif insufficient:
        report_status = "degraded"
    else:
        report_status = "available"

    report = V2PortfolioRiskReport(
        portfolio_definition_id=definition.id,
        as_of=as_of,
        time_basis={"timeframe": body.timeframe.upper(),
                    "observations": len(common),
                    "window_start": common[0][0].isoformat() if common else None,
                    "window_end": common[-1][0].isoformat() if common else None},
        input_refs=input_refs,
        inputs_hash=inputs_hash,
        metrics=metrics_json,
        scenarios=scenarios_json,
        status=report_status,
        basis_label="hypothetical-research",
        data_class=definition.data_class,
        engine_versions=ENGINE_VERSIONS,
        engine_versions_hash=versions_hash,
        mode=mode,
        operator_id=operator.username,
        correlation_id=correlation_id,
    )
    session.add(report)
    await session.flush()

    await V2AuditRepository(session).append(V2AuditEventCreate(
        domain="v2.portfolio_research", action="portfolio_risk.computed",
        actor_id=operator.username, actor_type="operator", mode=mode,
        resource_type="portfolio_risk_report", resource_id=report.id,
        details={"status": report_status, "inputs_hash": inputs_hash,
                 "insufficient": insufficient},
        operator_id=operator.username, correlation_id=correlation_id,
    ))
    await V2LineageRepository(session).append(V2LineageRecordCreate(
        artifact_type="portfolio_risk_report",
        artifact_id=report.id,
        operator_id=operator.username,
        mode=mode,
        source_artifact_ids=[definition.id],
        computation_version=versions_hash,
        input_snapshot_id=inputs_hash,
    ))
    return ComputeResponse(
        report_id=report.id, status=report_status,
        basis_label="hypothetical-research", reused_existing=False,
        insufficient_metrics=insufficient,
        **_envelope(request))
