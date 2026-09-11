"""V2 Audit API — read-only audit event endpoints.

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
from app.v2.models.audit import V2AuditEventResponse, V2AuditListResponse
from app.v2.rbac.dependencies import RequireV2AuditRead, RequireV2AuditReadAll

router = APIRouter(prefix="/audit", tags=["V2 Audit"])


def _to_response(event, user_role: str) -> V2AuditEventResponse:
    """Convert a V2AuditEvent DB model to a response model.

    Applies classification-based detail filtering.
    """
    from app.v2.audit.contract import filter_details_by_classification

    filtered_details = filter_details_by_classification(
        event.details, event.classification, user_role
    )
    return V2AuditEventResponse(
        id=event.id,
        correlation_id=event.correlation_id,
        causation_id=event.causation_id,
        actor_id=event.actor_id,
        actor_type=event.actor_type,
        domain=event.domain,
        action=event.action,
        resource_type=event.resource_type,
        resource_id=event.resource_id,
        mode=event.mode,
        details=filtered_details,
        classification=event.classification,
        operator_id=event.operator_id,
        created_at=event.created_at,
    )


@router.get("", response_model=V2AuditListResponse)
async def list_audit_events(
    request: Request,
    operator: RequireV2AuditRead,
    domain: str | None = None,
    limit: int = 50,
    session: AsyncSession = Depends(get_db_session),
) -> V2AuditListResponse:
    """List V2 audit events. Operator-scoped (own events only)."""
    repo = V2AuditRepository(session)
    events = await repo.read_by_operator(
        operator.id, domain=domain, limit=min(limit, 100)
    )

    # Audit the sensitive read
    await repo.append(V2AuditEventCreate(
        domain="v2.audit",
        action="audit.read_own",
        actor_id=operator.id,
        actor_type="operator",
        mode=request.app.state.v2_mode,
        operator_id=operator.id,
        classification="confidential",
        details={"scope": "operator", "domain_filter": domain, "count": len(events)},
    ))

    return V2AuditListResponse(
        events=[_to_response(e, operator.role) for e in events],
        total=len(events),
        mode=request.app.state.v2_mode,
        scope="operator",
        correlation_id=getattr(request.state, "correlation_id", None),
        timestamp=datetime.now(timezone.utc),
    )


@router.get("/all", response_model=V2AuditListResponse)
async def list_all_audit_events(
    request: Request,
    operator: RequireV2AuditReadAll,
    domain: str | None = None,
    limit: int = 50,
    session: AsyncSession = Depends(get_db_session),
) -> V2AuditListResponse:
    """List all V2 audit events. Admin-only, SAL-4. Sensitive read is audited."""
    repo = V2AuditRepository(session)
    events = await repo.read_all(domain=domain, limit=min(limit, 100))

    # Audit the sensitive admin read
    await repo.append(V2AuditEventCreate(
        domain="v2.audit",
        action="audit.read_all",
        actor_id=operator.id,
        actor_type="operator",
        mode=request.app.state.v2_mode,
        operator_id=operator.id,
        classification="confidential",
        details={"scope": "all", "domain_filter": domain, "count": len(events)},
    ))

    return V2AuditListResponse(
        events=[_to_response(e, operator.role) for e in events],
        total=len(events),
        mode=request.app.state.v2_mode,
        scope="all",
        correlation_id=getattr(request.state, "correlation_id", None),
        timestamp=datetime.now(timezone.utc),
    )
