"""Authenticated live market data endpoints (W0-U05)."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import CurrentOperatorDep
from app.core.config import get_settings
from app.db.session import get_db_session
from app.market.live_service import get_live_market_service
from app.models.market import (
    LiveMarketControlResponse,
    LiveMarketStatsResponse,
    LiveSubscribeResponse,
)
from app.services.chart_seed_service import seed_chart_history

SessionDep = Annotated[AsyncSession, Depends(get_db_session)]

router = APIRouter(prefix="/market/live", tags=["market-live"])


def _stats_model() -> LiveMarketStatsResponse:
    raw = get_live_market_service().stats()
    return LiveMarketStatsResponse(**raw)


@router.get("/status", response_model=LiveMarketStatsResponse, summary="Live feed status")
async def live_status(operator: CurrentOperatorDep) -> LiveMarketStatsResponse:
    _ = operator
    return _stats_model()


@router.get("/stats", response_model=LiveMarketStatsResponse, summary="Live feed statistics")
async def live_stats(operator: CurrentOperatorDep) -> LiveMarketStatsResponse:
    _ = operator
    return _stats_model()


@router.post(
    "/start",
    response_model=LiveMarketControlResponse,
    summary="Start live market adapter (simulated by default)",
)
async def live_start(operator: CurrentOperatorDep) -> LiveMarketControlResponse:
    _ = operator
    stats = await get_live_market_service().start()
    status = "started" if stats["running"] else "unknown"
    return LiveMarketControlResponse(status=status, stats=stats)


@router.post(
    "/stop",
    response_model=LiveMarketControlResponse,
    summary="Stop live market adapter",
)
async def live_stop(operator: CurrentOperatorDep) -> LiveMarketControlResponse:
    _ = operator
    stats = await get_live_market_service().stop()
    return LiveMarketControlResponse(status="stopped", stats=stats)


@router.get(
    "/subscribe",
    response_model=LiveSubscribeResponse,
    summary="WebSocket subscription instructions",
)
async def live_subscribe(operator: CurrentOperatorDep) -> LiveSubscribeResponse:
    _ = operator
    svc = get_live_market_service().stats()
    return LiveSubscribeResponse(
        symbol=str(svc["symbol"]),
        symbols=list(svc.get("symbols") or []),
        timeframe=str(svc["timeframe"]),
        websocket_path="/ws/market",
    )


@router.post(
    "/seed-history",
    summary="Seed synthetic OHLC history for chart context (auth)",
)
async def seed_history(operator: CurrentOperatorDep, session: SessionDep) -> dict:
    """Insert seed:synthetic bars when series are sparse. Chart presentation enablement only."""
    _ = operator
    settings = get_settings()
    counts = await seed_chart_history(
        session,
        symbols=settings.live_market_symbols_list,
        timeframe=settings.live_market_timeframe,
        bars=80,
    )
    return {"status": "ok", "seeded": counts, "timeframe": settings.live_market_timeframe}
