"""V2 Lineage API — read-only lineage record endpoints.

Operator-scoped reads; admin read_all requires SAL-4 permission.
Sensitive reads are audited.
"""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.v2.audit.contract import V2AuditEventCreate
from app.v2.audit.repository import V2AuditRepository
from app.v2.lineage.repository import V2LineageRepository
from app.v2.models.lineage import V2LineageListResponse, V2LineageRecordResponse
from app.v2.rbac.dependencies import RequireV2LineageRead, RequireV2LineageReadAll

router = APIRouter(prefix="/lineage", tags=["V2 Lineage"])


def _to_response(record) -> V2LineageRecordResponse:
    """Convert a V2LineageRecord DB model to a response model."""
    return V2LineageRecordResponse(
        id=record.id,
        artifact_type=record.artifact_type,
        artifact_id=record.artifact_id,
        operator_id=record.operator_id,
        mode=record.mode,
        source_artifact_ids=record.source_artifact_ids,
        computation_version=record.computation_version,
        input_snapshot_id=record.input_snapshot_id,
        created_at=record.created_at,
    )


@router.get("", response_model=V2LineageListResponse)
async def list_lineage_records(
    request: Request,
    operator: RequireV2LineageRead,
    artifact_type: str | None = None,
    limit: int = 50,
    session: AsyncSession = Depends(get_db_session),
) -> V2LineageListResponse:
    """List V2 lineage records. Operator-scoped (own records only)."""
    repo = V2LineageRepository(session)
    records = await repo.read_by_operator(
        operator.id, artifact_type=artifact_type, limit=min(limit, 100)
    )

    # Audit the sensitive read
    audit_repo = V2AuditRepository(session)
    await audit_repo.append(V2AuditEventCreate(
        domain="v2.lineage",
        action="lineage.read_own",
        actor_id=operator.id,
        actor_type="operator",
        mode=request.app.state.v2_mode,
        operator_id=operator.id,
        classification="confidential",
        details={"scope": "operator", "artifact_type_filter": artifact_type, "count": len(records)},
    ))

    return V2LineageListResponse(
        records=[_to_response(r) for r in records],
        total=len(records),
        mode=request.app.state.v2_mode,
        scope="operator",
        correlation_id=getattr(request.state, "correlation_id", None),
        timestamp=datetime.now(timezone.utc),
    )


@router.get("/all", response_model=V2LineageListResponse)
async def list_all_lineage_records(
    request: Request,
    operator: RequireV2LineageReadAll,
    artifact_type: str | None = None,
    limit: int = 50,
    session: AsyncSession = Depends(get_db_session),
) -> V2LineageListResponse:
    """List all V2 lineage records. Admin-only, SAL-4. Sensitive read is audited."""
    repo = V2LineageRepository(session)
    records = await repo.read_all(artifact_type=artifact_type, limit=min(limit, 100))

    # Audit the sensitive admin read
    audit_repo = V2AuditRepository(session)
    await audit_repo.append(V2AuditEventCreate(
        domain="v2.lineage",
        action="lineage.read_all",
        actor_id=operator.id,
        actor_type="operator",
        mode=request.app.state.v2_mode,
        operator_id=operator.id,
        classification="confidential",
        details={"scope": "all", "artifact_type_filter": artifact_type, "count": len(records)},
    ))

    return V2LineageListResponse(
        records=[_to_response(r) for r in records],
        total=len(records),
        mode=request.app.state.v2_mode,
        scope="all",
        correlation_id=getattr(request.state, "correlation_id", None),
        timestamp=datetime.now(timezone.utc),
    )


@router.get("/{artifact_type}/{artifact_id}", response_model=V2LineageListResponse)
async def get_artifact_lineage(
    artifact_type: str,
    artifact_id: str,
    request: Request,
    operator: RequireV2LineageRead,
    session: AsyncSession = Depends(get_db_session),
) -> V2LineageListResponse:
    """Get lineage records for a specific artifact. Operator-scoped."""
    repo = V2LineageRepository(session)
    records = await repo.read_by_artifact(artifact_type, artifact_id, operator_id=operator.id)

    # Audit the read
    audit_repo = V2AuditRepository(session)
    await audit_repo.append(V2AuditEventCreate(
        domain="v2.lineage",
        action="lineage.read_artifact",
        actor_id=operator.id,
        actor_type="operator",
        mode=request.app.state.v2_mode,
        operator_id=operator.id,
        resource_type=artifact_type,
        resource_id=artifact_id,
        classification="confidential",
        details={"count": len(records)},
    ))

    return V2LineageListResponse(
        records=[_to_response(r) for r in records],
        total=len(records),
        mode=request.app.state.v2_mode,
        scope="operator",
        correlation_id=getattr(request.state, "correlation_id", None),
        timestamp=datetime.now(timezone.utc),
    )
