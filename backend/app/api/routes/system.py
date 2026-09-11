"""System metadata endpoints."""

from __future__ import annotations

from fastapi import APIRouter

from app.auth.dependencies import CurrentOperatorDep
from app.core.dependencies import SystemServiceDep
from app.models.system import SystemInfoResponse

router = APIRouter(tags=["system"])


@router.get("/system/info", response_model=SystemInfoResponse, summary="Platform identity")
async def system_info(
    service: SystemServiceDep,
    operator: CurrentOperatorDep,
) -> SystemInfoResponse:
    """Return platform identity for authenticated operator terminal shell."""
    _ = operator
    return service.get_info()
