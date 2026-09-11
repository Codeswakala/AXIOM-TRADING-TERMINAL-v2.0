"""Read-only advisory analytics API (W3-U07)."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import CurrentOperatorDep
from app.db.session import get_db_session
from app.models.advisory_analytics import AdvisoryAnalyticsResponse
from app.trading_intelligence.analytics import AdvisoryAnalyticsService

router = APIRouter(prefix="/analytics", tags=["advisory-analytics"])

SessionDep = Annotated[AsyncSession, Depends(get_db_session)]


def _service(session: SessionDep) -> AdvisoryAnalyticsService:
    return AdvisoryAnalyticsService(session)


AdvisoryAnalyticsServiceDep = Annotated[AdvisoryAnalyticsService, Depends(_service)]


@router.get(
    "/advisory-performance",
    response_model=AdvisoryAnalyticsResponse,
    summary="Read-only advisory analytics with uncertainty (operator-authenticated)",
)
async def advisory_performance(
    service: AdvisoryAnalyticsServiceDep,
    operator: CurrentOperatorDep,
    limit: int = Query(default=500, ge=1, le=2000),
) -> AdvisoryAnalyticsResponse:
    _ = operator
    snapshot = await service.snapshot(limit=limit)
    return AdvisoryAnalyticsResponse.model_validate(service.to_dict(snapshot))
