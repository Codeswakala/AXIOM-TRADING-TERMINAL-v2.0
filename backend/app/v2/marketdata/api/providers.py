"""V2 BE-3 P1 provider status APIs — strictly read-only.

No transition endpoint or write path exists (BO-V2-BE-3-P1-001 §3.4).
Status is read from the seeded registry; the adapter existing does not and
cannot change it.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.v2_provider import V2MdProvider, V2MdProviderStatusHistory
from app.db.session import get_db_session
from app.v2.audit.contract import V2AuditEventCreate
from app.v2.audit.repository import V2AuditRepository
from app.v2.rbac.dependencies import RequireV2ProviderRead, RequireV2ProviderReadHistory

router = APIRouter(prefix="/marketdata/providers", tags=["V2 Providers"])


class V2ProviderModel(BaseModel):
    provider_id: str
    display_name: str
    markets: list[str]
    entitlement_status: str
    persistence_permitted: bool
    source_status: str
    created_at: datetime


class V2ProviderListResponse(BaseModel):
    providers: list[V2ProviderModel]
    total: int
    mode: str
    correlation_id: str | None = None
    timestamp: datetime


class V2ProviderStatusHistoryModel(BaseModel):
    provider_id: str
    from_status: str | None
    to_status: str
    authority_ref: str
    evidence_ref: str | None
    created_at: datetime


class V2ProviderHistoryResponse(BaseModel):
    history: list[V2ProviderStatusHistoryModel]
    total: int
    mode: str
    correlation_id: str | None = None
    timestamp: datetime


def _envelope(request: Request) -> dict[str, Any]:
    return {
        "mode": request.app.state.v2_mode,
        "correlation_id": getattr(request.state, "correlation_id", None),
        "timestamp": datetime.now(timezone.utc),
    }


@router.get("", response_model=V2ProviderListResponse)
async def list_providers(
    request: Request,
    operator: RequireV2ProviderRead,
    session: AsyncSession = Depends(get_db_session),
) -> V2ProviderListResponse:
    """Provider registry (read-only). Truthful ladder status."""
    rows = (
        (await session.execute(select(V2MdProvider).order_by(V2MdProvider.provider_id)))
        .scalars()
        .all()
    )
    return V2ProviderListResponse(
        providers=[
            V2ProviderModel(
                provider_id=r.provider_id,
                display_name=r.display_name,
                markets=r.markets,
                entitlement_status=r.entitlement_status,
                persistence_permitted=r.persistence_permitted,
                source_status=r.source_status,
                created_at=r.created_at,
            )
            for r in rows
        ],
        total=len(rows),
        **_envelope(request),
    )


@router.get("/{provider_id}/history", response_model=V2ProviderHistoryResponse)
async def provider_status_history(
    provider_id: str,
    request: Request,
    operator: RequireV2ProviderReadHistory,
    session: AsyncSession = Depends(get_db_session),
) -> V2ProviderHistoryResponse:
    """Status-ladder history (admin, SAL-4). Sensitive read audited."""
    rows = (
        (
            await session.execute(
                select(V2MdProviderStatusHistory)
                .where(V2MdProviderStatusHistory.provider_id == provider_id)
                .order_by(V2MdProviderStatusHistory.created_at.asc())
            )
        )
        .scalars()
        .all()
    )
    if not rows:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found")

    audit_repo = V2AuditRepository(session)
    await audit_repo.append(
        V2AuditEventCreate(
            domain="v2.marketdata",
            action="provider.history_read",
            actor_id=operator.id,
            actor_type="operator",
            mode=request.app.state.v2_mode,
            operator_id=operator.id,
            resource_type="provider",
            resource_id=provider_id,
            classification="confidential",
            details={"count": len(rows)},
        )
    )
    return V2ProviderHistoryResponse(
        history=[
            V2ProviderStatusHistoryModel(
                provider_id=r.provider_id,
                from_status=r.from_status,
                to_status=r.to_status,
                authority_ref=r.authority_ref,
                evidence_ref=r.evidence_ref,
                created_at=r.created_at,
            )
            for r in rows
        ],
        total=len(rows),
        **_envelope(request),
    )
