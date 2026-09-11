"""Persistence API (W1-U01: authenticated, service-layer backed)."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import CurrentOperatorDep
from app.core.dependencies import SettingsDep
from app.db.models.audit import AuditEvent
from app.db.models.candle import Candle
from app.db.session import get_db_session
from app.models.indicators import IndicatorSeriesEnvelope
from app.models.persistence import (
    AuditEventRead,
    CandleCreate,
    CandleRead,
    CandleSeriesEnvelope,
    DatabaseStatsResponse,
)
from app.services.indicator_registry import INDICATOR_REGISTRY
from app.services.persistence_service import PersistenceService
from app.services.timeframes import TIMEFRAME_PATTERN

router = APIRouter(prefix="/persistence", tags=["persistence"])

SessionDep = Annotated[AsyncSession, Depends(get_db_session)]


def _service(session: SessionDep, settings: SettingsDep) -> PersistenceService:
    return PersistenceService(session, settings)


PersistenceServiceDep = Annotated[PersistenceService, Depends(_service)]


@router.post(
    "/candles",
    response_model=CandleRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a sample candle (operator-authenticated)",
)
async def create_candle(
    payload: CandleCreate,
    service: PersistenceServiceDep,
    operator: CurrentOperatorDep,
) -> Candle:
    _ = operator
    return await service.create_candle(payload)


@router.get(
    "/candles",
    response_model=list[CandleRead],
    summary="List candles by symbol (operator-authenticated)",
)
async def list_candles(
    service: PersistenceServiceDep,
    operator: CurrentOperatorDep,
    symbol: str = Query(..., min_length=1),
    timeframe: str | None = None,
    market_class: str | None = None,
    limit: int = Query(default=50, ge=1, le=2000),
    order: str = Query(default="desc", pattern="^(asc|desc)$"),
) -> list[Candle]:
    """List candles. Use order=asc for chart series (oldest → newest, last N bars)."""
    _ = operator
    return await service.list_candles(
        symbol=symbol,
        timeframe=timeframe,
        market_class=market_class,
        limit=limit,
        ascending=(order == "asc"),
    )


@router.get(
    "/candle-series",
    response_model=CandleSeriesEnvelope,
    summary="Typed candle series — native, aggregated, or unavailable (DATA-P02)",
)
async def get_candle_series(
    service: PersistenceServiceDep,
    operator: CurrentOperatorDep,
    symbol: str = Query(..., min_length=1),
    timeframe: str = Query(..., pattern=TIMEFRAME_PATTERN),
    market_class: str | None = None,
    limit: int = Query(default=50, ge=1, le=2000),
    order: str = Query(default="desc", pattern="^(asc|desc)$"),
) -> CandleSeriesEnvelope:
    """M2/M4: aggregation is server work, and the series state is a typed
    discriminant on the response — never inferred by the consumer from bar
    counts or message strings. Same auth pattern as the raw listing
    (CurrentOperatorDep)."""
    _ = operator
    return await service.candle_series(
        symbol=symbol,
        timeframe=timeframe,
        market_class=market_class,
        limit=limit,
        ascending=(order == "asc"),
    )


@router.get(
    "/indicator-series",
    response_model=IndicatorSeriesEnvelope,
    summary="Typed indicator series — server-computed, insufficient-aware (CHART-P01)",
)
async def get_indicator_series(
    service: PersistenceServiceDep,
    operator: CurrentOperatorDep,
    symbol: str = Query(..., min_length=1),
    timeframe: str = Query(..., pattern=TIMEFRAME_PATTERN),
    indicators: str = Query(..., min_length=1, description="Comma-separated registry ids, e.g. SMA20,EMA20"),
) -> IndicatorSeriesEnvelope:
    """M1/M4/M6: derived series are server work. Requested ids must exist in
    the indicator registry (unknown ids are a 422, never silently dropped);
    insufficient history is a typed per-indicator result; an unavailable
    underlying series yields no computation."""
    _ = operator
    ids = [part.strip() for part in indicators.split(",") if part.strip()]
    if not ids:
        raise HTTPException(status_code=422, detail="No indicators requested")
    unknown = [i for i in ids if i not in INDICATOR_REGISTRY]
    if unknown:
        raise HTTPException(
            status_code=422,
            detail=f"Unknown indicator(s): {', '.join(unknown)}",
        )
    return await service.indicator_series(symbol=symbol, timeframe=timeframe, indicator_ids=ids)


@router.get(
    "/candles/{candle_id}",
    response_model=CandleRead,
    summary="Get candle by id (operator-authenticated)",
)
async def get_candle(
    candle_id: str,
    service: PersistenceServiceDep,
    operator: CurrentOperatorDep,
) -> Candle:
    _ = operator
    candle = await service.get_candle(candle_id)
    if candle is None:
        raise HTTPException(status_code=404, detail="Candle not found")
    return candle


@router.get(
    "/audit-events",
    response_model=list[AuditEventRead],
    summary="List recent audit events (operator-authenticated)",
)
async def list_audit_events(
    service: PersistenceServiceDep,
    operator: CurrentOperatorDep,
    category: str | None = None,
    limit: int = Query(default=50, ge=1, le=200),
) -> list[AuditEvent]:
    _ = operator
    return await service.list_audit_events(category=category, limit=limit)


@router.get(
    "/stats",
    response_model=DatabaseStatsResponse,
    summary="Database stats for observability (operator-authenticated)",
)
async def database_stats(
    service: PersistenceServiceDep,
    operator: CurrentOperatorDep,
) -> DatabaseStatsResponse:
    _ = operator
    return await service.database_stats()
