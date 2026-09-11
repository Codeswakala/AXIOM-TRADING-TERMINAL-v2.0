"""Health and readiness endpoints."""

from __future__ import annotations

from fastapi import APIRouter

from app.core.dependencies import HealthServiceDep
from app.models.health import HealthResponse, ReadinessResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse, summary="Liveness probe")
async def health(service: HealthServiceDep) -> HealthResponse:
    """Return process liveness. Does not validate downstream dependencies."""
    return service.liveness()


@router.get("/ready", response_model=ReadinessResponse, summary="Readiness probe")
async def ready(service: HealthServiceDep) -> ReadinessResponse:
    """Return readiness including live database connectivity (W0-U02)."""
    return await service.readiness()
