"""Market data ingestion verification API (historical CSV only).

W1-U01: ingestion endpoints are operator-authenticated operational APIs.
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import CurrentOperatorDep
from app.db.models.ingestion_run import IngestionRun
from app.db.session import get_db_session
from app.ingestion.service import IngestionService
from app.ingestion.types import IngestionResult
from app.models.ingestion import (
    IngestCsvRequest,
    IngestionResultRead,
    IngestionRunRead,
    IngestionStatsResponse,
    IngestSampleRequest,
    RowErrorRead,
)

router = APIRouter(prefix="/ingestion", tags=["ingestion"])

SessionDep = Annotated[AsyncSession, Depends(get_db_session)]

# Allowed roots for path-based ingestion (path traversal protection)
BACKEND_ROOT = Path(__file__).resolve().parents[3]
ALLOWED_ROOTS = (
    BACKEND_ROOT / "sample_data",
    BACKEND_ROOT / "tests" / "fixtures",
)


def _resolve_allowed_path(path_str: str) -> Path:
    candidate = Path(path_str).expanduser()
    if not candidate.is_absolute():
        candidate = (BACKEND_ROOT / candidate).resolve()
    else:
        candidate = candidate.resolve()
    for root in ALLOWED_ROOTS:
        root_resolved = root.resolve()
        try:
            candidate.relative_to(root_resolved)
            return candidate
        except ValueError:
            continue
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=(
            "Path not allowed. Use files under backend/sample_data/ "
            "or backend/tests/fixtures/ (or sample_name endpoint)."
        ),
    )


def _to_result_read(result: IngestionResult) -> IngestionResultRead:
    return IngestionResultRead(
        run_id=result.run_id,
        status=result.status,
        source_name=result.source_name,
        market_class=result.market_class,
        symbol=result.symbol,
        timeframe=result.timeframe,
        rows_read=result.rows_read,
        rows_valid=result.rows_valid,
        rows_invalid=result.rows_invalid,
        rows_inserted=result.rows_inserted,
        rows_updated=result.rows_updated,
        rows_unchanged=result.rows_unchanged,
        duration_ms=result.duration_ms,
        error_summary=result.error_summary,
        errors=[RowErrorRead(row_number=e.row_number, message=e.message) for e in result.errors],
    )


@router.post(
    "/csv",
    response_model=IngestionResultRead,
    summary="Ingest historical CSV from an allowed path (operator-authenticated)",
)
async def ingest_csv(
    payload: IngestCsvRequest,
    session: SessionDep,
    operator: CurrentOperatorDep,
) -> IngestionResultRead:
    _ = operator
    path = _resolve_allowed_path(payload.path)
    service = IngestionService(session)
    result = await service.ingest_csv(
        path=path,
        market_class=payload.market_class,
        symbol=payload.symbol,
        timeframe=payload.timeframe,
        source=payload.source,
    )
    return _to_result_read(result)


@router.post(
    "/sample",
    response_model=IngestionResultRead,
    summary="Ingest a built-in sample CSV by filename (operator-authenticated)",
)
async def ingest_sample(
    payload: IngestSampleRequest,
    session: SessionDep,
    operator: CurrentOperatorDep,
) -> IngestionResultRead:
    _ = operator
    sample_path = (BACKEND_ROOT / "sample_data" / Path(payload.sample_name).name).resolve()
    if not sample_path.is_file():
        raise HTTPException(status_code=404, detail=f"Sample not found: {payload.sample_name}")
    service = IngestionService(session)
    # BO-B-DATA A3: the default sample label is NON-authoritative (classifies
    # UNKNOWN under the Part-A rule) — it cannot manufacture authority for
    # data that was never declared real.
    result = await service.ingest_csv(
        path=sample_path,
        market_class=payload.market_class,
        symbol=payload.symbol,
        timeframe=payload.timeframe,
        source=payload.source or f"sample:{payload.sample_name}",
    )
    return _to_result_read(result)


@router.get(
    "/runs",
    response_model=list[IngestionRunRead],
    summary="List recent ingestion runs (operator-authenticated)",
)
async def list_runs(
    session: SessionDep,
    operator: CurrentOperatorDep,
    limit: int = Query(default=20, ge=1, le=100),
) -> list[IngestionRun]:
    _ = operator
    service = IngestionService(session)
    return await service.list_runs(limit=limit)


@router.get(
    "/runs/{run_id}",
    response_model=IngestionRunRead,
    summary="Get ingestion run by id (operator-authenticated)",
)
async def get_run(
    run_id: str,
    session: SessionDep,
    operator: CurrentOperatorDep,
) -> IngestionRun:
    _ = operator
    service = IngestionService(session)
    run = await service.get_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Ingestion run not found")
    return run


@router.get(
    "/stats",
    response_model=IngestionStatsResponse,
    summary="Ingestion and candle statistics (operator-authenticated)",
)
async def ingestion_stats(
    session: SessionDep,
    operator: CurrentOperatorDep,
    market_class: str | None = None,
    symbol: str | None = None,
    timeframe: str | None = None,
) -> IngestionStatsResponse:
    """Protected endpoint for ingestion stats."""
    _ = operator
    service = IngestionService(session)
    runs = await service.list_runs(limit=1)
    total_runs = int(
        (await session.execute(select(func.count()).select_from(IngestionRun))).scalar_one()
    )
    total_candles = await service.candle_counts()
    filtered = await service.candle_counts(
        market_class=market_class,
        symbol=symbol,
        timeframe=timeframe,
    )
    return IngestionStatsResponse(
        total_runs=total_runs,
        last_run=IngestionRunRead.model_validate(runs[0]) if runs else None,
        candle_count_total=total_candles,
        candle_counts_by_filter={
            "market_class": market_class or "*",
            "symbol": symbol or "*",
            "timeframe": timeframe or "*",
            "count": filtered,
        },
    )


@router.get(
    "/candle-counts",
    summary="Candle counts by optional market filters (operator-authenticated)",
)
async def candle_counts(
    session: SessionDep,
    operator: CurrentOperatorDep,
    market_class: str | None = None,
    symbol: str | None = None,
    timeframe: str | None = None,
) -> dict[str, int | str | None]:
    _ = operator
    service = IngestionService(session)
    count = await service.candle_counts(
        market_class=market_class,
        symbol=symbol,
        timeframe=timeframe,
    )
    return {
        "market_class": market_class,
        "symbol": symbol,
        "timeframe": timeframe,
        "count": count,
    }
