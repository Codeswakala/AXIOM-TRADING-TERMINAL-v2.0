"""BE-4 endpoints (BO D-4; plan §7 + R-1).

Four GET endpoints + the SINGLE governed computation writer
``POST /market-context/compute`` — the only non-GET endpoint in the band.
Mounted on the V2 aggregate router (R-3: accepted physical mount; the
Delivery Report pins the final path with Level I evidence).
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.operator import Operator
from app.db.models.v2_research import (
    V2ChartIntelligenceReport,
    V2MarketContextReport,
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
from app.v2.rbac.dependencies import require_v2_permission
from app.v2.research.chart_intelligence import (
    cie_to_json,
    compute_chart_intelligence,
)
from app.v2.research.market_context import (
    compute_market_context,
    input_content_hash,
    observations_to_json,
)
from app.v2.research.repositories import (
    V2ChartIntelligenceReportRepository,
    V2ComputationVersionRepository,
    V2MarketContextReportRepository,
    utc_normalized,
)
from app.v2.research.versioning import (
    COMPONENT_INDICATOR_ENGINE,
    INDICATOR_ENGINE_VERSION,
    ComputationVersionMismatch,
    compute_indicator_engine_hash,
    engine_versions,
    engine_versions_hash,
)
from app.v2.temporal.validation import require_utc, utc_now

router = APIRouter(prefix="/market-context", tags=["V2 Research Read Models"])

RequireV2ResearchMcRead = Annotated[
    Operator, Depends(require_v2_permission("v2.research.market_context.read"))
]
RequireV2ResearchCiRead = Annotated[
    Operator, Depends(require_v2_permission("v2.research.chart_intelligence.read"))
]
RequireV2ResearchCompute = Annotated[
    Operator, Depends(require_v2_permission("v2.research.market_context.compute"))
]

_ALLOWED_MODES = ("RESEARCH", "SIMULATION")


def _envelope(request: Request) -> dict:
    return {
        "mode": request.app.state.v2_mode,
        "correlation_id": getattr(request.state, "correlation_id", None),
        "timestamp": datetime.now(timezone.utc),
    }


# --- Response / request models ------------------------------------------------


class V2McReportSummary(BaseModel):
    id: str
    instrument_id: str
    timeframe_set: list[str]
    as_of: datetime
    mode: str
    status: str
    validation_tier: str
    input_content_hash: str
    engine_versions: dict[str, str]
    created_at: datetime


class V2McReportListResponse(BaseModel):
    reports: list[V2McReportSummary]
    total: int
    mode: str
    correlation_id: str | None
    timestamp: datetime


class V2McReportDetailResponse(BaseModel):
    report: V2McReportSummary
    observations: dict
    input_snapshot_id: str
    engine_versions_hash: str
    mode: str
    correlation_id: str | None
    timestamp: datetime


class V2CiReportResponse(BaseModel):
    id: str
    market_context_report_id: str
    as_of: datetime
    status: str
    annotations: list[dict]
    interpretations: list[dict]
    engine_versions: dict[str, str]
    mode: str
    correlation_id: str | None
    timestamp: datetime


class V2VersionsResponse(BaseModel):
    versions: list[dict]
    mode: str
    correlation_id: str | None
    timestamp: datetime


class V2McComputeRequest(BaseModel):
    instrument_id: str = Field(min_length=1, max_length=96)
    timeframes: list[str] = Field(min_length=1, max_length=6)
    source_id: str = "sim.local"
    as_of: datetime | None = None
    bar_limit: int = Field(default=500, ge=20, le=1000)


class V2McComputeResponse(BaseModel):
    report_id: str | None
    chart_intelligence_report_id: str | None
    status: str
    reused_existing: bool
    families_computed: int
    insufficient_data: list[dict]
    mode: str
    correlation_id: str | None
    timestamp: datetime


# --- GET endpoints (strictly read-only) ----------------------------------------


def _summary(r: V2MarketContextReport) -> V2McReportSummary:
    return V2McReportSummary(
        id=r.id,
        instrument_id=r.instrument_id,
        timeframe_set=list(r.timeframe_set),
        as_of=utc_normalized(r.as_of),
        mode=r.mode,
        status=r.status,
        validation_tier=r.validation_tier,
        input_content_hash=r.input_content_hash,
        engine_versions=dict(r.engine_versions),
        created_at=utc_normalized(r.created_at),
    )


@router.get("/reports", response_model=V2McReportListResponse)
async def list_reports(
    request: Request,
    operator: RequireV2ResearchMcRead,
    instrument_id: str | None = Query(default=None),
    status_filter: str | None = Query(default=None, alias="status"),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_db_session),
) -> V2McReportListResponse:
    repo = V2MarketContextReportRepository(session)
    reports = await repo.list_reports(
        instrument_id=instrument_id, status=status_filter,
        limit=limit, offset=offset,
    )
    return V2McReportListResponse(
        reports=[_summary(r) for r in reports],
        total=len(reports),
        **_envelope(request),
    )


@router.get("/reports/{report_id}", response_model=V2McReportDetailResponse)
async def get_report(
    report_id: str,
    request: Request,
    operator: RequireV2ResearchMcRead,
    session: AsyncSession = Depends(get_db_session),
) -> V2McReportDetailResponse:
    repo = V2MarketContextReportRepository(session)
    report = await repo.get(report_id)
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Report not found")
    return V2McReportDetailResponse(
        report=_summary(report),
        observations=dict(report.observations),
        input_snapshot_id=report.input_snapshot_id,
        engine_versions_hash=report.engine_versions_hash,
        **_envelope(request),
    )


@router.get("/chart-intelligence/{report_id}", response_model=V2CiReportResponse)
async def get_chart_intelligence(
    report_id: str,
    request: Request,
    operator: RequireV2ResearchCiRead,
    session: AsyncSession = Depends(get_db_session),
) -> V2CiReportResponse:
    repo = V2ChartIntelligenceReportRepository(session)
    report = await repo.get(report_id)
    if report is None:
        # allow lookup by parent market-context id as a convenience
        report = await repo.get_by_market_context(report_id)
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Report not found")
    return V2CiReportResponse(
        id=report.id,
        market_context_report_id=report.market_context_report_id,
        as_of=utc_normalized(report.as_of),
        status=report.status,
        annotations=list(report.annotations.get("annotations", [])),
        interpretations=list(report.interpretations.get("interpretations", [])),
        engine_versions=dict(report.engine_versions),
        **_envelope(request),
    )


@router.get("/versions", response_model=V2VersionsResponse)
async def list_versions(
    request: Request,
    operator: RequireV2ResearchMcRead,
    session: AsyncSession = Depends(get_db_session),
) -> V2VersionsResponse:
    repo = V2ComputationVersionRepository(session)
    rows = await repo.list_all()
    return V2VersionsResponse(
        versions=[
            {
                "component": r.component,
                "version": r.version,
                "source_hash": r.source_hash,
                "registered_at": utc_normalized(r.registered_at).isoformat(),
            }
            for r in rows
        ],
        **_envelope(request),
    )


# --- R-1: the single governed computation writer -------------------------------


@router.post("/compute", response_model=V2McComputeResponse)
async def compute(
    body: V2McComputeRequest,
    request: Request,
    operator: RequireV2ResearchCompute,
    session: AsyncSession = Depends(get_db_session),
) -> V2McComputeResponse:
    """R-1 governed writer — the only non-GET endpoint in the band.

    Mode-enforced server-side; fully audited; idempotent by the determinism
    anchor (same input + versions ⇒ the existing report is returned).
    """
    mode = request.app.state.v2_mode
    correlation_id = getattr(request.state, "correlation_id", None) or new_id()
    if mode not in _ALLOWED_MODES:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Computation not permitted in this mode")

    now = utc_now()
    as_of = body.as_of
    if as_of is not None:
        require_utc(as_of, boundary="as_of")
        if as_of > now:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="as_of may not be in the future")
    effective_as_of = as_of or now

    # Version-pin check — registered hash must match the live surface
    # (typed refusal on mismatch, BO D-1).
    ver_repo = V2ComputationVersionRepository(session)
    registered = await ver_repo.get(
        COMPONENT_INDICATOR_ENGINE, INDICATOR_ENGINE_VERSION
    )
    if registered is None:
        # Plan §6: version resolution impossible → typed UNKNOWN — an
        # allowed state, never guessed over. Nothing is persisted.
        await V2AuditRepository(session).append(V2AuditEventCreate(
            domain="v2.research",
            action="research.market_context.compute.unknown",
            actor_id=operator.username,
            actor_type="operator",
            mode=mode,
            details={"reason": "computation version not registered"},
            operator_id=operator.username,
            correlation_id=correlation_id,
        ))
        return V2McComputeResponse(
            report_id=None,
            chart_intelligence_report_id=None,
            status="unknown",
            reused_existing=False,
            families_computed=0,
            insufficient_data=[],
            mode=mode,
            correlation_id=correlation_id,
            timestamp=datetime.now(timezone.utc),
        )
    actual_hash = compute_indicator_engine_hash()
    if registered.source_hash != actual_hash:
        exc = ComputationVersionMismatch(
            COMPONENT_INDICATOR_ENGINE, registered.source_hash, actual_hash
        )
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=str(exc))

    # Resolve instrument + source through the BE-2 reference model.
    ref_repo = V2MdReferenceRepository(session)
    instrument = await ref_repo.get_instrument(body.instrument_id)
    if instrument is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Instrument not found")
    source = await ref_repo.get_source(body.source_id)
    if source is None or not source.active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Source not found or inactive")

    # Read bars per timeframe (as-of bounded; labelled synthetic input).
    boundary = V2MdBarReadBoundary(session)
    bars_by_tf: dict[str, list[dict]] = {}
    for timeframe in body.timeframes:
        rows = await boundary.read_bars(
            market_class=instrument.market_class,
            symbol=instrument.display_symbol,
            timeframe=timeframe.upper(),
            as_of=effective_as_of,
            limit=body.bar_limit,
        )
        # Source filter; the as-of bound is applied by read_bars (no-future
        # is re-proved by the temporal-integrity test group).
        rows = [r for r in rows if r.source == source.authority]
        bars_by_tf[timeframe.upper()] = [
            {
                "open_time": r.open_time,
                "open": r.open,
                "high": r.high,
                "low": r.low,
                "close": r.close,
                "volume": getattr(r, "volume", 0),
            }
            for r in rows
        ]

    versions = engine_versions()
    versions_hash = engine_versions_hash(versions)
    content_hash = input_content_hash(bars_by_tf)
    snapshot_id = (
        f"{body.instrument_id}|{'+'.join(sorted(bars_by_tf))}|{body.source_id}"
        f"|{effective_as_of.isoformat()}|{content_hash[:16]}"
    )

    mc_repo = V2MarketContextReportRepository(session)
    audit_repo = V2AuditRepository(session)

    # R-1 idempotency: determinism anchor lookup first.
    existing = await mc_repo.find_by_anchor(
        body.instrument_id, content_hash, versions_hash
    )
    if existing is not None:
        await audit_repo.append(V2AuditEventCreate(
            domain="v2.research",
            action="research.market_context.compute.reused",
            actor_id=operator.username,
            actor_type="operator",
            mode=mode,
            resource_type="market_context_report",
            resource_id=existing.id,
            details={"reused_existing": True,
                     "input_content_hash": content_hash},
            operator_id=operator.username,
            correlation_id=correlation_id,
        ))
        ci_repo = V2ChartIntelligenceReportRepository(session)
        existing_ci = await ci_repo.get_by_market_context(existing.id)
        return V2McComputeResponse(
            report_id=existing.id,
            chart_intelligence_report_id=existing_ci.id if existing_ci else None,
            status=existing.status,
            reused_existing=True,
            families_computed=len(
                {o["family"] for o in existing.observations.get("observations", [])}
            ),
            insufficient_data=list(
                existing.observations.get("insufficient_data", [])
            ),
            mode=mode,
            correlation_id=correlation_id,
            timestamp=datetime.now(timezone.utc),
        )

    # Compute — deterministic MCE + CIE.
    mc_result = compute_market_context(bars_by_tf)

    # Plan §6: staleness beyond the declared bound (3 timeframe periods
    # before as_of) → typed `stale`, report emitted with disclosure.
    from datetime import timedelta

    from app.v2.marketdata.provenance import timeframe_seconds

    staleness: list[dict] = []
    for tf, tf_bars in bars_by_tf.items():
        if not tf_bars:
            continue
        last_open = tf_bars[-1]["open_time"]
        if last_open.tzinfo is None:
            last_open = last_open.replace(tzinfo=timezone.utc)
        bound = timedelta(seconds=3 * timeframe_seconds(tf))
        if effective_as_of - last_open > bound:
            staleness.append({
                "timeframe": tf,
                "last_open_time": last_open.isoformat(),
                "declared_bound_seconds": 3 * timeframe_seconds(tf),
            })
    final_status = mc_result.status
    if staleness and final_status == "available":
        final_status = "stale"
    observations_json = observations_to_json(
        mc_result.observations, mc_result.insufficient
    )
    if staleness:
        observations_json["staleness_disclosure"] = staleness
    report = V2MarketContextReport(
        instrument_id=body.instrument_id,
        timeframe_set=sorted(bars_by_tf),
        as_of=effective_as_of,
        mode=mode,
        status=final_status,
        validation_tier="pipeline-validation",
        input_snapshot_id=snapshot_id,
        input_content_hash=content_hash,
        observations=observations_json,
        engine_versions=versions,
        engine_versions_hash=versions_hash,
        operator_id=operator.username,
    )
    await mc_repo.append(report)

    ci_result = compute_chart_intelligence(
        observations_json["observations"]
    )
    ci_json = cie_to_json(ci_result)
    ci_report = V2ChartIntelligenceReport(
        market_context_report_id=report.id,
        as_of=effective_as_of,
        mode=mode,
        status=ci_result.status,
        annotations={"annotations": ci_json["annotations"]},
        interpretations={"interpretations": ci_json["interpretations"]},
        engine_versions=versions,
        operator_id=operator.username,
    )
    ci_repo = V2ChartIntelligenceReportRepository(session)
    await ci_repo.append(ci_report)

    # Audit + lineage (BE-1 contracts).
    await audit_repo.append(V2AuditEventCreate(
        domain="v2.research",
        action="research.market_context.computed",
        actor_id=operator.username,
        actor_type="operator",
        mode=mode,
        resource_type="market_context_report",
        resource_id=report.id,
        details={
            "instrument_id": body.instrument_id,
            "timeframes": sorted(bars_by_tf),
            "status": final_status,
            "input_content_hash": content_hash,
            "engine_versions_hash": versions_hash,
            "validation_tier": "pipeline-validation",
        },
        operator_id=operator.username,
        correlation_id=correlation_id,
    ))
    await audit_repo.append(V2AuditEventCreate(
        domain="v2.research",
        action="research.chart_intelligence.computed",
        actor_id=operator.username,
        actor_type="operator",
        mode=mode,
        resource_type="chart_intelligence_report",
        resource_id=ci_report.id,
        details={"market_context_report_id": report.id,
                 "status": ci_result.status},
        operator_id=operator.username,
        correlation_id=correlation_id,
    ))
    lineage_repo = V2LineageRepository(session)
    await lineage_repo.append(V2LineageRecordCreate(
        artifact_type="market_context_report",
        artifact_id=report.id,
        operator_id=operator.username,
        mode=mode,
        source_artifact_ids=[snapshot_id],
        computation_version=versions_hash,
        input_snapshot_id=snapshot_id,
    ))
    await lineage_repo.append(V2LineageRecordCreate(
        artifact_type="chart_intelligence_report",
        artifact_id=ci_report.id,
        operator_id=operator.username,
        mode=mode,
        source_artifact_ids=[report.id],
        computation_version=versions_hash,
        input_snapshot_id=snapshot_id,
    ))

    return V2McComputeResponse(
        report_id=report.id,
        chart_intelligence_report_id=ci_report.id,
        status=final_status,
        reused_existing=False,
        families_computed=mc_result.families_computed,
        insufficient_data=mc_result.insufficient,
        mode=mode,
        correlation_id=correlation_id,
        timestamp=datetime.now(timezone.utc),
    )
