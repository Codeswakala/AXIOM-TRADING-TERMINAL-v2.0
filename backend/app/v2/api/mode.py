"""V2 Mode API — read-only mode status endpoint."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Request

from app.v2.mode.contract import DEFERRED_MODES, VALID_MODES
from app.v2.models.mode import V2ModeResponse
from app.v2.rbac.dependencies import RequireV2ModeRead

router = APIRouter(prefix="/mode", tags=["V2 Mode"])


@router.get("", response_model=V2ModeResponse)
async def get_mode(
    request: Request,
    operator: RequireV2ModeRead,
) -> V2ModeResponse:
    """Get current V2 mode status. Read-only; immutable at runtime."""
    mode = request.app.state.v2_mode
    return V2ModeResponse(
        mode=mode,
        valid_modes=list(VALID_MODES),
        deferred_modes=list(DEFERRED_MODES),
        source="AXIOM_V2_MODE",
        immutable_at_runtime=True,
        correlation_id=getattr(request.state, "correlation_id", None),
        timestamp=datetime.now(timezone.utc),
    )
