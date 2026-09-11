"""Read-only advisory signal history API (W3-U02)."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import CurrentOperatorDep
from app.db.models.advisory_signal import AdvisorySignal
from app.db.session import get_db_session
from app.models.advisory_signal import AdvisorySignalRead
from app.trading_intelligence.signals import AdvisorySignalHistoryFilter, AdvisorySignalService

router = APIRouter(prefix="/signals", tags=["advisory-signals"])

SessionDep = Annotated[AsyncSession, Depends(get_db_session)]


def _service(session: SessionDep) -> AdvisorySignalService:
    return AdvisorySignalService(session)


AdvisorySignalServiceDep = Annotated[AdvisorySignalService, Depends(_service)]


@router.get(
    "/history",
    response_model=list[AdvisorySignalRead],
    summary="List persisted advisory signal history (operator-authenticated)",
)
async def list_signal_history(
    service: AdvisorySignalServiceDep,
    operator: CurrentOperatorDep,
    signal_id: str | None = None,
    model_artifact_id: str | None = None,
    market_class: str | None = None,
    symbol: str | None = None,
    timeframe: str | None = None,
    signal_state: str | None = Query(
        default=None, pattern="^(emitted|withheld|warning|expired|superseded)$"
    ),
    current_only: bool = False,
    limit: int = Query(default=50, ge=1, le=200),
) -> list[AdvisorySignal]:
    _ = operator
    return await service.list_history(
        AdvisorySignalHistoryFilter(
            signal_id=signal_id,
            model_artifact_id=model_artifact_id,
            market_class=market_class,
            symbol=symbol,
            timeframe=timeframe,
            signal_state=signal_state,
            current_only=current_only,
            limit=limit,
        )
    )


@router.get(
    "/history/{signal_id}",
    response_model=AdvisorySignalRead,
    summary="Get one persisted advisory signal by id (operator-authenticated)",
)
async def get_signal_history(
    signal_id: str,
    service: AdvisorySignalServiceDep,
    operator: CurrentOperatorDep,
) -> AdvisorySignal:
    _ = operator
    signal = await service.get_signal(signal_id)
    if signal is None:
        raise HTTPException(status_code=404, detail="Advisory signal not found")
    return signal
