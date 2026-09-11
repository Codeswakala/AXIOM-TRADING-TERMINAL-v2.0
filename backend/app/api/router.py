"""Aggregate API router."""

from __future__ import annotations

from fastapi import APIRouter

from app.api.routes import (
    advisory_analytics,
    advisory_signals,
    auth,
    collaboration,
    execution_research,
    health,
    ingestion,
    institutional_platform,
    intelligence,
    market,
    monitoring_alerts,
    observability,
    operator,
    persistence,
    system,
    ws,
)
from app.api.routes.v2 import v2_router

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(system.router)
api_router.include_router(ws.router)
api_router.include_router(persistence.router)
api_router.include_router(observability.router)
api_router.include_router(ingestion.router)
api_router.include_router(auth.router)
api_router.include_router(operator.router)
api_router.include_router(market.router)
api_router.include_router(advisory_signals.router)
api_router.include_router(monitoring_alerts.router)
api_router.include_router(advisory_analytics.router)
api_router.include_router(intelligence.router)
api_router.include_router(collaboration.router)
api_router.include_router(execution_research.router)
api_router.include_router(institutional_platform.router)
api_router.include_router(v2_router)
