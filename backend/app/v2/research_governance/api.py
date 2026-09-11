"""BE-5 U-4/U-5 endpoints (BO-V2-BE-5-001 T-8).

Read-only surface under ``/research-governance`` on the V2 aggregate
router, plus the TWO governed writers: the SAL-3 governance decision
writer and the SAL-3 signal emitter. RESEARCH-mode enforcement
server-side; every response carries the V2 envelope; no credential is
prompted for or used anywhere.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.operator import Operator
from app.db.models.v2_research_governance import (
    V2MlDiagnosticReport,
    V2MlGovernanceRecord,
    V2MlLifecycleEvent,
)
from app.db.models.v2_signal import V2SignalRecord
from app.db.session import get_db_session
from app.v2.audit.contract import V2AuditEventCreate
from app.v2.audit.repository import V2AuditRepository
from app.v2.identifiers import new_id
from app.v2.lineage.contract import V2LineageRecordCreate
from app.v2.lineage.repository import V2LineageRepository
from app.v2.rbac.dependencies import require_v2_permission
from app.v2.research_governance.contracts import (
    DATA_CLASSES,
    SIGNAL_FAMILIES,
)
from app.v2.research_governance.decisions import decide_promotion
from app.v2.research_governance.signals import (
    SignalRequest,
    emit_signal,
    projected_state,
)
from app.v2.temporal.validation import require_utc, utc_now

router = APIRouter(prefix="/research-governance", tags=["V2 Research Governance"])

RequireMlGovRead = Annotated[
    Operator, Depends(require_v2_permission("v2.research.ml_governance.read"))
]
RequireMlGovDecide = Annotated[
    Operator, Depends(require_v2_permission("v2.research.ml_governance.decide"))
]
RequireSignalRead = Annotated[
    Operator, Depends(require_v2_permission("v2.research.signal.read"))
]
RequireSignalEmit = Annotated[
    Operator, Depends(require_v2_permission("v2.research.signal.emit"))
]
RequireDiagRead = Annotated[
    Operator, Depends(require_v2_permission("v2.research.ml_diagnostics.read"))
]


def _envelope(request: Request) -> dict:
    return {
        "mode": request.app.state.v2_mode,
        "correlation_id": getattr(request.state, "correlation_id", None),
        "timestamp": datetime.now(timezone.utc),
    }


def _require_research(request: Request) -> str:
    mode = request.app.state.v2_mode
    if mode != "RESEARCH":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Decision not permitted in this mode")
    return mode


# --- models --------------------------------------------------------------------


class GovernanceRecordModel(BaseModel):
    id: str
    model_artifact_id: str
    record_seq: int
    supersedes: str | None
    model_type: str
    instrument_class: str
    eligibility_status: str
    calibration_status: str
    freshness_status: str
    economic_status: str
    statistical_status: str
    deployment_class: str
    rollback_target_version: str | None
    data_class: str
    created_at: datetime


class GovernanceListResponse(BaseModel):
    records: list[GovernanceRecordModel]
    total: int
    mode: str
    correlation_id: str | None
    timestamp: datetime


class PromotionRequest(BaseModel):
    governance_record_id: str = Field(min_length=1)
    target_class: str


class PromotionResponse(BaseModel):
    decision: str
    reasons: list
    new_record_id: str | None
    mode: str
    correlation_id: str | None
    timestamp: datetime


class SignalEmitRequest(BaseModel):
    family: str
    signal_type: str = Field(min_length=1, max_length=64)
    instrument_id: str = Field(min_length=1, max_length=96)
    timeframe: str = Field(min_length=1, max_length=16)
    payload: dict | None = None
    uncertainty: dict | None = None
    limitations: dict = Field(default_factory=dict)
    source_family_refs: dict = Field(default_factory=dict)
    governance_record_id: str | None = None
    data_class: str
    as_of: datetime | None = None
    expires_at: datetime | None = None


class SignalEmitResponse(BaseModel):
    signal_id: str
    state: str
    reasons: list
    mode: str
    correlation_id: str | None
    timestamp: datetime


class SignalListResponse(BaseModel):
    signals: list[dict]
    total: int
    mode: str
    correlation_id: str | None
    timestamp: datetime


class DiagnosticsListResponse(BaseModel):
    reports: list[dict]
    total: int
    mode: str
    correlation_id: str | None
    timestamp: datetime


# --- reads ----------------------------------------------------------------------


def _record_model(r: V2MlGovernanceRecord) -> GovernanceRecordModel:
    return GovernanceRecordModel(
        id=r.id, model_artifact_id=r.model_artifact_id,
        record_seq=r.record_seq, supersedes=r.supersedes,
        model_type=r.model_type, instrument_class=r.instrument_class,
        eligibility_status=r.eligibility_status,
        calibration_status=r.calibration_status,
        freshness_status=r.freshness_status,
        economic_status=r.economic_status,
        statistical_status=r.statistical_status,
        deployment_class=r.deployment_class,
        rollback_target_version=r.rollback_target_version,
        data_class=r.data_class,
        created_at=r.created_at,
    )


@router.get("/governance", response_model=GovernanceListResponse)
async def list_governance(
    request: Request,
    operator: RequireMlGovRead,
    model_artifact_id: str | None = Query(default=None),
    current_only: bool = Query(default=True),
    limit: int = Query(default=100, ge=1, le=500),
    session: AsyncSession = Depends(get_db_session),
) -> GovernanceListResponse:
    stmt = select(V2MlGovernanceRecord).order_by(
        V2MlGovernanceRecord.model_artifact_id,
        V2MlGovernanceRecord.record_seq.desc(),
    )
    if model_artifact_id is not None:
        stmt = stmt.where(
            V2MlGovernanceRecord.model_artifact_id == model_artifact_id)
    if current_only:
        # currency = greatest record_seq per artifact (P-1 projection);
        # with the C-1 forward link, `supersedes IS NULL` selects only
        # genesis rows — wrong. Subquery projection instead.
        from sqlalchemy import func

        latest = (
            select(V2MlGovernanceRecord.model_artifact_id,
                   func.max(V2MlGovernanceRecord.record_seq).label("max_seq"))
            .group_by(V2MlGovernanceRecord.model_artifact_id)
            .subquery()
        )
        stmt = stmt.join(
            latest,
            (V2MlGovernanceRecord.model_artifact_id == latest.c.model_artifact_id)
            & (V2MlGovernanceRecord.record_seq == latest.c.max_seq),
        )
    rows = list((await session.execute(stmt.limit(limit))).scalars().all())
    return GovernanceListResponse(
        records=[_record_model(r) for r in rows], total=len(rows),
        **_envelope(request))


@router.get("/signals", response_model=SignalListResponse)
async def list_signals(
    request: Request,
    operator: RequireSignalRead,
    family: str | None = Query(default=None),
    state: str | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
    session: AsyncSession = Depends(get_db_session),
) -> SignalListResponse:
    stmt = select(V2SignalRecord).order_by(V2SignalRecord.created_at.desc())
    if family is not None:
        stmt = stmt.where(V2SignalRecord.family == family)
    if state is not None:
        stmt = stmt.where(V2SignalRecord.state == state)
    rows = list((await session.execute(stmt.limit(limit))).scalars().all())
    signals = []
    for r in rows:
        projected = await projected_state(session, r.id)
        signals.append({
            "id": r.id, "family": r.family, "signal_type": r.signal_type,
            "instrument_id": r.instrument_id, "timeframe": r.timeframe,
            "state": r.state, "projected_state": projected or r.state,
            "state_reason": r.state_reason, "payload": r.payload,
            "uncertainty": r.uncertainty, "limitations": r.limitations,
            "source_family_refs": r.source_family_refs,
            "governance_record_id": r.governance_record_id,
            "data_class": r.data_class,
            "as_of": r.as_of.isoformat() if r.as_of else None,
        })
    return SignalListResponse(signals=signals, total=len(signals),
                              **_envelope(request))


@router.get("/diagnostics", response_model=DiagnosticsListResponse)
async def list_diagnostics(
    request: Request,
    operator: RequireDiagRead,
    model_artifact_id: str | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
    session: AsyncSession = Depends(get_db_session),
) -> DiagnosticsListResponse:
    stmt = select(V2MlDiagnosticReport).order_by(
        V2MlDiagnosticReport.created_at.desc())
    if model_artifact_id is not None:
        stmt = stmt.where(
            V2MlDiagnosticReport.model_artifact_id == model_artifact_id)
    rows = list((await session.execute(stmt.limit(limit))).scalars().all())
    return DiagnosticsListResponse(
        reports=[{
            "id": r.id, "model_artifact_id": r.model_artifact_id,
            "diagnostics": r.diagnostics, "input_refs": r.input_refs,
            "inputs_hash": r.inputs_hash,
            "engine_versions": r.engine_versions,
            "engine_versions_hash": r.engine_versions_hash,
            "data_class": r.data_class,
        } for r in rows],
        total=len(rows), **_envelope(request))


# --- governed writer 1: promotion decision (SAL-3) --------------------------------


@router.post("/governance/promote", response_model=PromotionResponse)
async def promote(
    body: PromotionRequest,
    request: Request,
    operator: RequireMlGovDecide,
    session: AsyncSession = Depends(get_db_session),
) -> PromotionResponse:
    """P-1 row-versioning writer: an allowed promotion creates a NEW
    governance row (record_seq + 1); the prior row is never mutated.
    The successor's `supersedes` column holds the predecessor's id
    (C-1 forward-reading vocabulary: this row SUPERSEDES that one).
    Currency = greatest record_seq per artifact.
    """
    mode = _require_research(request)
    correlation_id = getattr(request.state, "correlation_id", None) or new_id()

    current = (await session.execute(
        select(V2MlGovernanceRecord).where(
            V2MlGovernanceRecord.id == body.governance_record_id)
    )).scalar_one_or_none()
    if current is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Governance record not found")
    # currency check: is this the greatest record_seq for the artifact?
    newest = (await session.execute(
        select(V2MlGovernanceRecord)
        .where(V2MlGovernanceRecord.model_artifact_id
               == current.model_artifact_id)
        .order_by(V2MlGovernanceRecord.record_seq.desc())
    )).scalars().first()
    audit_repo = V2AuditRepository(session)

    outcome = decide_promotion(
        statuses={
            "eligibility_status": current.eligibility_status,
            "calibration_status": current.calibration_status,
            "freshness_status": current.freshness_status,
            "economic_status": current.economic_status,
            "statistical_status": current.statistical_status,
        },
        current_class=current.deployment_class,
        target_class=body.target_class,
        rollback_target_version=current.rollback_target_version,
        mode=mode,
    )
    reasons = list(outcome.reasons)
    if newest is not None and newest.id != current.id:
        reasons.append({"failing": "record_currency",
                        "value": f"seq {current.record_seq} < {newest.record_seq}"})

    # champion-scope rule (P-3): at most one champion per
    # (model_type, instrument_class) on the current projection
    if body.target_class == "champion" and not reasons:
        rows = (await session.execute(
            select(V2MlGovernanceRecord)
            .where(V2MlGovernanceRecord.model_type == current.model_type,
                   V2MlGovernanceRecord.instrument_class
                   == current.instrument_class)
            .order_by(V2MlGovernanceRecord.model_artifact_id,
                      V2MlGovernanceRecord.record_seq.desc())
        )).scalars().all()
        seen: set[str] = set()
        for row in rows:
            if row.model_artifact_id in seen:
                continue
            seen.add(row.model_artifact_id)
            if (row.deployment_class == "champion"
                    and row.model_artifact_id != current.model_artifact_id):
                reasons.append({
                    "failing": "champion_scope",
                    "value": f"champion exists for ({current.model_type},"
                             f" {current.instrument_class})"})
                break

    decision = "allowed" if not reasons else "refused"
    new_record_id: str | None = None

    if decision == "allowed":
        successor = V2MlGovernanceRecord(
            model_artifact_id=current.model_artifact_id,
            record_seq=current.record_seq + 1,
            supersedes=current.id,  # this row supersedes `current` (C-1)
            registry_version=current.registry_version,
            model_type=current.model_type,
            instrument_class=current.instrument_class,
            eligibility_status=current.eligibility_status,
            calibration_status=current.calibration_status,
            freshness_status=current.freshness_status,
            economic_status=current.economic_status,
            statistical_status=current.statistical_status,
            deployment_class=body.target_class,
            rollback_target_version=current.rollback_target_version,
            data_class=current.data_class,
            evidence_refs=current.evidence_refs,
            mode=mode,
            operator_id=operator.username,
            correlation_id=correlation_id,
        )
        session.add(successor)
        await session.flush()
        new_record_id = successor.id
        session.add(V2MlLifecycleEvent(
            governance_record_id=successor.id,
            event_type="promoted",
            from_value=current.deployment_class,
            to_value=body.target_class,
            decision_basis=outcome.as_decision_basis(),
            mode=mode, actor_id=operator.username,
            operator_id=operator.username, correlation_id=correlation_id,
        ))
        await V2LineageRepository(session).append(V2LineageRecordCreate(
            artifact_type="ml_governance_record",
            artifact_id=successor.id,
            operator_id=operator.username,
            mode=mode,
            source_artifact_ids=[current.id, current.model_artifact_id],
            computation_version=current.registry_version,
            input_snapshot_id=None,
        ))
        await audit_repo.append(V2AuditEventCreate(
            domain="v2.research_governance",
            action="ml.promotion.decided",
            actor_id=operator.username, actor_type="operator", mode=mode,
            resource_type="ml_governance_record", resource_id=successor.id,
            details={"from": current.deployment_class,
                     "to": body.target_class,
                     "predecessor": current.id},
            operator_id=operator.username, correlation_id=correlation_id,
        ))
    else:
        session.add(V2MlLifecycleEvent(
            governance_record_id=current.id,
            event_type="refused",
            from_value=current.deployment_class,
            to_value=body.target_class,
            decision_basis={"contract": "promotion", "status": "refused",
                            "reasons": reasons,
                            "spec_citation": outcome.citation},
            mode=mode, actor_id=operator.username,
            operator_id=operator.username, correlation_id=correlation_id,
        ))
        await audit_repo.append(V2AuditEventCreate(
            domain="v2.research_governance",
            action="ml.promotion.refused",
            actor_id=operator.username, actor_type="operator", mode=mode,
            resource_type="ml_governance_record", resource_id=current.id,
            details={"to": body.target_class, "reasons": reasons},
            operator_id=operator.username, correlation_id=correlation_id,
        ))

    return PromotionResponse(decision=decision, reasons=reasons,
                             new_record_id=new_record_id,
                             **_envelope(request))


# --- governed writer 2: signal emission (SAL-3) -----------------------------------


@router.post("/signals/emit", response_model=SignalEmitResponse)
async def emit(
    body: SignalEmitRequest,
    request: Request,
    operator: RequireSignalEmit,
    session: AsyncSession = Depends(get_db_session),
) -> SignalEmitResponse:
    mode = _require_research(request)
    correlation_id = getattr(request.state, "correlation_id", None) or new_id()
    now = utc_now()
    as_of = body.as_of or now
    require_utc(as_of, boundary="as_of")
    if as_of > now:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="as_of may not be in the future")
    if body.family not in SIGNAL_FAMILIES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Unknown signal family")
    if body.data_class not in DATA_CLASSES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Unknown data class")

    result = await emit_signal(session, SignalRequest(
        family=body.family, signal_type=body.signal_type,
        instrument_id=body.instrument_id, timeframe=body.timeframe,
        payload=body.payload, uncertainty=body.uncertainty,
        limitations=body.limitations or {"declared": "none"},
        source_family_refs=body.source_family_refs,
        governance_record_id=body.governance_record_id,
        data_class=body.data_class, as_of=as_of,
        expires_at=body.expires_at, mode=mode,
        operator_id=operator.username, correlation_id=correlation_id,
    ))

    audit_repo = V2AuditRepository(session)
    await audit_repo.append(V2AuditEventCreate(
        domain="v2.research_governance",
        action=f"signal.{result.state}",
        actor_id=operator.username, actor_type="operator", mode=mode,
        resource_type="signal_record", resource_id=result.record.id,
        details={"family": body.family, "signal_type": body.signal_type,
                 "state": result.state,
                 "reasons": result.reasons[:5]},
        operator_id=operator.username, correlation_id=correlation_id,
    ))
    await V2LineageRepository(session).append(V2LineageRecordCreate(
        artifact_type="signal_record",
        artifact_id=result.record.id,
        operator_id=operator.username,
        mode=mode,
        source_artifact_ids=(
            list(body.source_family_refs.get("ids", []))
            + ([body.governance_record_id] if body.governance_record_id else [])
        ),
        computation_version="sge-1.0.0",
        input_snapshot_id=None,
    ))
    return SignalEmitResponse(
        signal_id=result.record.id, state=result.state,
        reasons=result.reasons, **_envelope(request))
