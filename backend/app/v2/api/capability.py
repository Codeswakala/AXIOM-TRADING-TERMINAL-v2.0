"""V2 Capability API — read-only capability registry endpoints."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.v2_capability_record import V2CapabilityRecord
from app.db.session import get_db_session
from app.v2.models.capability import (
    V2CapabilityDetailResponse,
    V2CapabilityListResponse,
    V2CapabilityResponse,
)
from app.v2.rbac.dependencies import RequireV2CapabilityRead

router = APIRouter(prefix="/capabilities", tags=["V2 Capabilities"])


@router.get("", response_model=V2CapabilityListResponse)
async def list_capabilities(
    request: Request,
    operator: RequireV2CapabilityRead,
    session: AsyncSession = Depends(get_db_session),
) -> V2CapabilityListResponse:
    """List all V2 capabilities. Read-only seeded registry."""
    stmt = select(V2CapabilityRecord).order_by(
        V2CapabilityRecord.band, V2CapabilityRecord.capability_id
    )
    result = await session.execute(stmt)
    records = list(result.scalars().all())

    capabilities = [
        V2CapabilityResponse(
            id=r.id,
            capability_id=r.capability_id,
            domain=r.domain,
            band=r.band,
            maturity=r.maturity,
            artifact_status=r.artifact_status,
            version=r.version,
            created_at=r.created_at,
        )
        for r in records
    ]

    return V2CapabilityListResponse(
        capabilities=capabilities,
        total=len(capabilities),
        mode=request.app.state.v2_mode,
        correlation_id=getattr(request.state, "correlation_id", None),
        timestamp=datetime.now(timezone.utc),
    )


@router.get("/{capability_id}", response_model=V2CapabilityDetailResponse)
async def get_capability(
    capability_id: str,
    request: Request,
    operator: RequireV2CapabilityRead,
    session: AsyncSession = Depends(get_db_session),
) -> V2CapabilityDetailResponse:
    """Get a single V2 capability by ID. Typed envelope with mode/correlation/timestamp."""
    stmt = select(V2CapabilityRecord).where(V2CapabilityRecord.capability_id == capability_id)
    result = await session.execute(stmt)
    record = result.scalar_one_or_none()

    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Capability not found: {capability_id}",
        )

    return V2CapabilityDetailResponse(
        capability=V2CapabilityResponse(
            id=record.id,
            capability_id=record.capability_id,
            domain=record.domain,
            band=record.band,
            maturity=record.maturity,
            artifact_status=record.artifact_status,
            version=record.version,
            created_at=record.created_at,
        ),
        mode=request.app.state.v2_mode,
        correlation_id=getattr(request.state, "correlation_id", None),
        timestamp=datetime.now(timezone.utc),
    )
