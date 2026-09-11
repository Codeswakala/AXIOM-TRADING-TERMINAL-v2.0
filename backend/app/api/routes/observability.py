"""Authenticated observability and metrics endpoints (W1-U02)."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from app.auth.dependencies import CurrentOperatorDep
from app.core.config import Settings, get_settings
from app.market.live_service import get_live_market_service
from app.services.database_health import check_database
from app.services.observability_service import get_observability_service, redact

router = APIRouter(tags=["observability"])


@router.get("/metrics", summary="Read-only platform metrics (operator-authenticated)")
async def metrics(operator: CurrentOperatorDep) -> dict[str, Any]:
    """Return read-only metrics without secrets or business decisions."""
    _ = operator
    settings: Settings = get_settings()
    db = await check_database(settings)
    live = get_live_market_service().stats()
    snapshot = get_observability_service().snapshot()
    payload = {
        "service": settings.app_name,
        "version": settings.version,
        "environment": settings.environment,
        "observability": snapshot,
        "database": {
            "status": db.status,
            "latency_ms": db.latency_ms,
            "backend": db.backend,
            "pool": db.pool,
        },
        "live_market": {
            "running": live.get("running"),
            "connected": live.get("connected"),
            "messages_received": live.get("messages_received"),
            "persist_count": live.get("persist_count"),
            "persist_errors": live.get("persist_errors"),
            "lag_ms": live.get("lag_ms"),
            "subscribers": live.get("subscribers"),
        },
    }
    return redact(payload)
