"""V2 BE-2 read APIs — persistence-pure GET endpoints (plan D.0 Rule 1).

The ONLY GET with a persistence side effect is /verification/all, whose
sensitive-read audit follows the established BE-1 pattern. Every data-bearing
response carries the mandatory provenance block.
"""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.v2.audit.contract import V2AuditEventCreate
from app.v2.audit.repository import V2AuditRepository
from app.v2.marketdata.models import (
    V2MdBarModel,
    V2MdBarsResponse,
    V2MdExceptionListResponse,
    V2MdExceptionModel,
    V2MdInstrumentDetailResponse,
    V2MdInstrumentListResponse,
    V2MdInstrumentModel,
    V2MdSeriesListResponse,
    V2MdSeriesModel,
    V2MdSourceListResponse,
    V2MdSourceModel,
    V2MdSymbolMapModel,
    V2MdVerificationDetailResponse,
    V2MdVerificationListResponse,
    V2MdVerificationModel,
    V2ProvenanceModel,
)
from app.v2.marketdata.provenance import (
    ACTIVE_AUTHORITY_VALUES,
    AUTHORITY_DISPLAY_LABELS,
    AUTHORITY_UNKNOWN,
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_EMPTY,
    AVAILABILITY_PARTIAL,
    AVAILABILITY_QUARANTINED,
    build_provenance,
    compute_freshness,
    timeframe_seconds,
)
from app.v2.marketdata.repositories import (
    V2MdBarReadBoundary,
    V2MdIntegrityRepository,
    V2MdReferenceRepository,
    V2MdSeriesRepository,
    V2MdVerificationRepository,
)
from app.v2.rbac.dependencies import (
    RequireV2MarketDataRead,
    RequireV2MarketDataReadAll,
)
from app.v2.temporal.validation import require_utc, utc_now

router = APIRouter(prefix="/marketdata", tags=["V2 Market Data"])


def _envelope(request: Request) -> dict:
    return {
        "mode": request.app.state.v2_mode,
        "correlation_id": getattr(request.state, "correlation_id", None),
        "timestamp": datetime.now(timezone.utc),
    }


def _provenance_for_source(source, as_of, verification_id=None) -> V2ProvenanceModel:
    prov = build_provenance(
        source_kind=source.kind if source else "reserved",
        authority=source.authority if source and source.active else AUTHORITY_UNKNOWN,
        source_id=source.source_id if source else "unregistered",
        as_of=as_of,
        verification_id=verification_id,
    )
    return V2ProvenanceModel(
        source_kind=prov.source_kind,
        authority=prov.authority,
        source_id=prov.source_id,
        as_of=prov.as_of,
        display_label=prov.display_label,
        verification_id=prov.verification_id,
    )


@router.get("/instruments", response_model=V2MdInstrumentListResponse)
async def list_instruments(
    request: Request,
    operator: RequireV2MarketDataRead,
    session: AsyncSession = Depends(get_db_session),
) -> V2MdInstrumentListResponse:
    repo = V2MdReferenceRepository(session)
    instruments = await repo.list_instruments()
    mappings = await repo.list_mappings()
    return V2MdInstrumentListResponse(
        instruments=[
            V2MdInstrumentModel(
                instrument_id=i.instrument_id,
                market_class=i.market_class,
                display_symbol=i.display_symbol,
                precision=i.precision,
                created_at=i.created_at,
            )
            for i in instruments
        ],
        mappings=[
            V2MdSymbolMapModel(
                source_id=m.source_id,
                source_symbol=m.source_symbol,
                instrument_id=m.instrument_id,
            )
            for m in mappings
        ],
        total=len(instruments),
        **_envelope(request),
    )


@router.get("/instruments/{instrument_id}", response_model=V2MdInstrumentDetailResponse)
async def get_instrument(
    instrument_id: str,
    request: Request,
    operator: RequireV2MarketDataRead,
    session: AsyncSession = Depends(get_db_session),
) -> V2MdInstrumentDetailResponse:
    repo = V2MdReferenceRepository(session)
    instrument = await repo.get_instrument(instrument_id)
    if instrument is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instrument not found")
    mappings = [m for m in await repo.list_mappings() if m.instrument_id == instrument_id]
    return V2MdInstrumentDetailResponse(
        instrument=V2MdInstrumentModel(
            instrument_id=instrument.instrument_id,
            market_class=instrument.market_class,
            display_symbol=instrument.display_symbol,
            precision=instrument.precision,
            created_at=instrument.created_at,
        ),
        mappings=[
            V2MdSymbolMapModel(
                source_id=m.source_id,
                source_symbol=m.source_symbol,
                instrument_id=m.instrument_id,
            )
            for m in mappings
        ],
        **_envelope(request),
    )


@router.get("/sources", response_model=V2MdSourceListResponse)
async def list_sources(
    request: Request,
    operator: RequireV2MarketDataRead,
    session: AsyncSession = Depends(get_db_session),
) -> V2MdSourceListResponse:
    """Source registry. DEL-001: serialization passes the active-authority
    guard — an active row may only emit approved vocabulary; a defective or
    inactive/reserved row is emitted with authority='unknown', never with
    reserved/imported/real vocabulary."""
    repo = V2MdReferenceRepository(session)
    sources = await repo.list_sources()
    items: list[V2MdSourceModel] = []
    for src in sources:
        if src.active and src.authority in ACTIVE_AUTHORITY_VALUES:
            emitted_authority = src.authority
        else:
            # inactive or non-approved vocabulary: honest unknown, no leak
            emitted_authority = AUTHORITY_UNKNOWN
        # Guard invariant (raises on any non-active value; defence in depth)
        build_provenance(
            source_kind=src.kind,
            authority=emitted_authority,
            source_id=src.source_id,
            as_of=None,
        )
        items.append(
            V2MdSourceModel(
                source_id=src.source_id,
                kind=src.kind,
                authority=emitted_authority,
                mode_scope=src.mode_scope,
                active=src.active,
                display_label=AUTHORITY_DISPLAY_LABELS[emitted_authority],
            )
        )
    return V2MdSourceListResponse(
        sources=items,
        total=len(items),
        **_envelope(request),
    )


@router.get("/series", response_model=V2MdSeriesListResponse)
async def list_series(
    request: Request,
    operator: RequireV2MarketDataRead,
    session: AsyncSession = Depends(get_db_session),
) -> V2MdSeriesListResponse:
    series_repo = V2MdSeriesRepository(session)
    ref_repo = V2MdReferenceRepository(session)
    integrity_repo = V2MdIntegrityRepository(session)
    rows = await series_repo.list_series()
    mode = request.app.state.v2_mode

    items: list[V2MdSeriesModel] = []
    for row in rows:
        source = await ref_repo.get_source(row.source_id)
        freshness = compute_freshness(row.last_open_time, row.timeframe)
        flags = await integrity_repo.exists_for_series(
            mode=mode,
            series_ref=f"{row.instrument_id}:{row.timeframe}:{row.source_id}",
        )
        if row.bar_count == 0:
            availability = AVAILABILITY_EMPTY
        elif flags["quarantine"]:
            availability = AVAILABILITY_QUARANTINED
        elif flags["partial"]:
            availability = AVAILABILITY_PARTIAL
        else:
            availability = AVAILABILITY_AVAILABLE
        items.append(
            V2MdSeriesModel(
                instrument_id=row.instrument_id,
                timeframe=row.timeframe,
                source_id=row.source_id,
                first_open_time=row.first_open_time,
                last_open_time=row.last_open_time,
                bar_count=row.bar_count,
                freshness=freshness,
                availability=availability,
                provenance=_provenance_for_source(source, row.last_open_time),
            )
        )
    return V2MdSeriesListResponse(series=items, total=len(items), **_envelope(request))


@router.get(
    "/series/{instrument_id}/{timeframe}/bars", response_model=V2MdBarsResponse
)
async def get_bars(
    instrument_id: str,
    timeframe: str,
    request: Request,
    operator: RequireV2MarketDataRead,
    source_id: str = Query(default="sim.local"),
    as_of: datetime | None = Query(default=None),
    limit: int = Query(default=500, ge=1, le=1000),
    session: AsyncSession = Depends(get_db_session),
) -> V2MdBarsResponse:
    """Bars read through the V1 wrap boundary with mandatory provenance.

    Persistence-pure: no catalog/exception/verification state is created.
    `as_of` is bounded by the no-future rule; gaps are disclosed, never filled.
    """
    timeframe = timeframe.upper()
    timeframe_seconds(timeframe)  # validates
    now = utc_now()
    if as_of is not None:
        require_utc(as_of, boundary="as_of")
        if as_of > now:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="as_of may not be in the future",
            )

    ref_repo = V2MdReferenceRepository(session)
    instrument = await ref_repo.get_instrument(instrument_id)
    if instrument is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instrument not found")
    source = await ref_repo.get_source(source_id)
    if source is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source not found")

    boundary = V2MdBarReadBoundary(session)
    source_marker = source.authority  # V1 rows carry the marker string
    all_rows = await boundary.read_bars(
        market_class=instrument.market_class,
        symbol=instrument.display_symbol,
        timeframe=timeframe,
        as_of=as_of,
        limit=limit,
    )
    # Filter to this source's marker; disclose non-matching rows as absent.
    rows = [r for r in all_rows if r.source == source_marker]
    # No-future guard on served rows (defence in depth).
    rows = [r for r in rows if r.open_time <= now]

    # Read-time gap disclosure inside the returned window (never filled).
    gaps: list[str] = []
    if len(rows) >= 2:
        from datetime import timedelta

        period = timedelta(seconds=timeframe_seconds(timeframe))
        for earlier, later in zip(rows, rows[1:]):
            expected = earlier.open_time + period
            while expected < later.open_time:
                gaps.append(expected.isoformat())
                expected += period

    last_open = rows[-1].open_time if rows else None
    freshness = compute_freshness(last_open, timeframe, now=now)
    if not rows:
        availability = AVAILABILITY_EMPTY
    elif gaps:
        availability = AVAILABILITY_PARTIAL
    else:
        availability = AVAILABILITY_AVAILABLE

    def dec(value) -> str:
        return str(Decimal(str(value)).normalize()) if value is not None else None

    return V2MdBarsResponse(
        instrument_id=instrument_id,
        timeframe=timeframe,
        bars=[
            V2MdBarModel(
                open_time=r.open_time,
                open=dec(r.open),
                high=dec(r.high),
                low=dec(r.low),
                close=dec(r.close),
                volume=dec(r.volume),
            )
            for r in rows
        ],
        total=len(rows),
        provenance=_provenance_for_source(source, last_open),
        freshness=freshness,
        availability=availability,
        gaps_disclosed=gaps[:50],
        **_envelope(request),
    )


@router.get("/integrity/exceptions", response_model=V2MdExceptionListResponse)
async def list_integrity_exceptions(
    request: Request,
    operator: RequireV2MarketDataRead,
    series_ref: str | None = None,
    limit: int = Query(default=100, ge=1, le=500),
    session: AsyncSession = Depends(get_db_session),
) -> V2MdExceptionListResponse:
    """Operator-scoped (SAL-3, DEL-002): own exception records only."""
    repo = V2MdIntegrityRepository(session)
    rows = await repo.list_exceptions(
        mode=request.app.state.v2_mode,
        operator_id=operator.id,
        series_ref=series_ref,
        limit=limit,
    )
    return V2MdExceptionListResponse(
        exceptions=[_exception_model(r) for r in rows],
        total=len(rows),
        **_envelope(request),
    )


def _exception_model(r) -> V2MdExceptionModel:
    return V2MdExceptionModel(
        id=r.id,
        series_ref=r.series_ref,
        operator_id=r.operator_id,
        exception_type=r.exception_type,
        fingerprint=r.fingerprint,
        detail=r.detail,
        observed_at=r.observed_at,
        mode=r.mode,
        correlation_id=r.correlation_id,
    )


@router.get("/integrity/exceptions/all", response_model=V2MdExceptionListResponse)
async def list_all_integrity_exceptions(
    request: Request,
    operator: RequireV2MarketDataReadAll,
    series_ref: str | None = None,
    limit: int = Query(default=100, ge=1, le=500),
    session: AsyncSession = Depends(get_db_session),
) -> V2MdExceptionListResponse:
    """Admin-only SAL-4 cross-operator read; sensitive read audited
    (BE-1 pattern)."""
    repo = V2MdIntegrityRepository(session)
    rows = await repo.list_all_exceptions(
        mode=request.app.state.v2_mode, series_ref=series_ref, limit=limit
    )
    audit_repo = V2AuditRepository(session)
    await audit_repo.append(
        V2AuditEventCreate(
            domain="v2.marketdata",
            action="integrity.read_all",
            actor_id=operator.id,
            actor_type="operator",
            mode=request.app.state.v2_mode,
            operator_id=operator.id,
            classification="confidential",
            details={"scope": "all", "count": len(rows)},
        )
    )
    return V2MdExceptionListResponse(
        exceptions=[_exception_model(r) for r in rows],
        total=len(rows),
        **_envelope(request),
    )


def _verification_model(row) -> V2MdVerificationModel:
    return V2MdVerificationModel(
        verification_id=row.verification_id,
        scope=row.scope,
        as_of=row.as_of,
        content_hash=row.content_hash,
        row_count=row.row_count,
        source_ids=row.source_ids,
        created_by_operator_id=row.created_by_operator_id,
        created_at=row.created_at,
    )


@router.get("/verification", response_model=V2MdVerificationListResponse)
async def list_verifications(
    request: Request,
    operator: RequireV2MarketDataRead,
    limit: int = Query(default=50, ge=1, le=100),
    session: AsyncSession = Depends(get_db_session),
) -> V2MdVerificationListResponse:
    repo = V2MdVerificationRepository(session)
    rows = await repo.read_by_operator(operator.id, limit=limit)
    return V2MdVerificationListResponse(
        records=[_verification_model(r) for r in rows],
        total=len(rows),
        scope="operator",
        **_envelope(request),
    )


@router.get("/verification/all", response_model=V2MdVerificationListResponse)
async def list_all_verifications(
    request: Request,
    operator: RequireV2MarketDataReadAll,
    limit: int = Query(default=50, ge=1, le=100),
    session: AsyncSession = Depends(get_db_session),
) -> V2MdVerificationListResponse:
    """Admin-only SAL-4. Sensitive read audited (established BE-1 pattern —
    the sole GET persistence side effect in BE-2)."""
    repo = V2MdVerificationRepository(session)
    rows = await repo.read_all(limit=limit)
    audit_repo = V2AuditRepository(session)
    await audit_repo.append(
        V2AuditEventCreate(
            domain="v2.marketdata",
            action="verification.read_all",
            actor_id=operator.id,
            actor_type="operator",
            mode=request.app.state.v2_mode,
            operator_id=operator.id,
            classification="confidential",
            details={"scope": "all", "count": len(rows)},
        )
    )
    return V2MdVerificationListResponse(
        records=[_verification_model(r) for r in rows],
        total=len(rows),
        scope="all",
        **_envelope(request),
    )


@router.get("/verification/{verification_id}", response_model=V2MdVerificationDetailResponse)
async def get_verification(
    verification_id: str,
    request: Request,
    operator: RequireV2MarketDataRead,
    session: AsyncSession = Depends(get_db_session),
) -> V2MdVerificationDetailResponse:
    repo = V2MdVerificationRepository(session)
    row = await repo.get(verification_id, operator_id=operator.id)
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Verification record not found"
        )
    return V2MdVerificationDetailResponse(
        record=_verification_model(row), **_envelope(request)
    )
