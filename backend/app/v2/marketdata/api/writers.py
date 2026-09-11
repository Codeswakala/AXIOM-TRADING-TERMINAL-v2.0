"""V2 BE-2 writers — W-1 catalog refresh and W-2 verification (plan D.0 Rule 2).

The ONLY BE-2 mutation paths. Both are authenticated, mode-gated, audited,
transaction-bounded, and idempotent (fingerprint dedup / manifest-stable
upsert). No bar payload is ever written.
"""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.v2.audit.contract import V2AuditEventCreate
from app.v2.audit.repository import V2AuditRepository
from app.v2.identifiers import new_id
from app.v2.lineage.contract import V2LineageRecordCreate
from app.v2.lineage.repository import V2LineageRepository
from app.v2.marketdata.api.reads import _envelope, _verification_model
from app.v2.marketdata.integrity import (
    check_future_data,
    check_gaps,
    check_ordering,
    verification_mismatch_finding,
)
from app.v2.marketdata.models import (
    V2MdCatalogRefreshResponse,
    V2MdVerificationCreateRequest,
    V2MdVerificationDetailResponse,
    V2MdVerifyResultResponse,
)
from app.v2.marketdata.provenance import map_v1_source_marker
from app.v2.marketdata.repositories import (
    V2MdBarReadBoundary,
    V2MdIntegrityRepository,
    V2MdReferenceRepository,
    V2MdSeriesRepository,
    V2MdVerificationRepository,
)
from app.v2.marketdata.verification import (
    VerificationScopeItem,
    compute_content_hash,
    validate_scope,
)
from app.v2.rbac.dependencies import (
    RequireV2MarketDataCatalogRefresh,
    RequireV2MarketDataVerify,
)
from app.v2.temporal.validation import require_utc, utc_now

router = APIRouter(prefix="/marketdata", tags=["V2 Market Data Writers"])


@router.post("/catalog/refresh", response_model=V2MdCatalogRefreshResponse)
async def catalog_refresh(
    request: Request,
    operator: RequireV2MarketDataCatalogRefresh,
    session: AsyncSession = Depends(get_db_session),
) -> V2MdCatalogRefreshResponse:
    """W-1 — the sole catalog/exception writer for scans (admin, SAL-3).

    Idempotent: unchanged series upserts are no-ops; integrity findings are
    fingerprint-deduplicated; re-running against unchanged data appends
    nothing. Audited with correlation ID.
    """
    mode = request.app.state.v2_mode
    correlation_id = getattr(request.state, "correlation_id", None) or new_id()

    ref_repo = V2MdReferenceRepository(session)
    series_repo = V2MdSeriesRepository(session)
    integrity_repo = V2MdIntegrityRepository(session)
    boundary = V2MdBarReadBoundary(session)

    created = updated = unchanged = appended = deduplicated = 0
    unmapped_sources: set[str] = set()
    now = utc_now()

    for market_class, symbol, timeframe, marker in await boundary.distinct_series_keys():
        source_id, _, authority = map_v1_source_marker(marker)
        source = await ref_repo.get_source(source_id)
        if source is None or authority == "unknown":
            # Unrecognized marker: disclosed, never auto-registered (plan C.4).
            unmapped_sources.add(str(marker))
            continue
        mapping = await ref_repo.resolve_symbol(source_id, symbol)
        if mapping is None:
            from app.v2.marketdata.integrity import unmapped_symbol_finding

            row = await integrity_repo.append_finding(
                unmapped_symbol_finding(source_id, symbol),
                operator_id=operator.id,
                mode=mode,
                correlation_id=correlation_id,
            )
            if row is None:
                deduplicated += 1
            else:
                appended += 1
            continue

        first, last, count = await boundary.series_summary(
            market_class=market_class,
            symbol=symbol,
            timeframe=timeframe,
            source_marker=marker,
        )
        _, state = await series_repo.upsert_series(
            instrument_id=mapping.instrument_id,
            timeframe=timeframe,
            source_id=source_id,
            first_open_time=first,
            last_open_time=last,
            bar_count=count,
        )
        if state == "created":
            created += 1
        elif state == "updated":
            updated += 1
        else:
            unchanged += 1

        # Integrity scan over the series' recent window
        series_ref = f"{mapping.instrument_id}:{timeframe}:{source_id}"
        bars = await boundary.read_bars(
            market_class=market_class, symbol=symbol, timeframe=timeframe, limit=1000
        )
        bars = [b for b in bars if b.source == marker]
        open_times = [b.open_time for b in bars]
        findings = []
        findings.extend(check_ordering(series_ref, open_times))
        findings.extend(check_gaps(series_ref, timeframe, open_times))
        for ot in open_times:
            f = check_future_data(series_ref, ot, now=now)
            if f is not None:
                findings.append(f)
        for finding in findings:
            row = await integrity_repo.append_finding(
                finding, operator_id=operator.id, mode=mode, correlation_id=correlation_id
            )
            if row is None:
                deduplicated += 1
            else:
                appended += 1

    audit_repo = V2AuditRepository(session)
    await audit_repo.append(
        V2AuditEventCreate(
            domain="v2.marketdata",
            action="catalog.refresh",
            actor_id=operator.id,
            actor_type="operator",
            mode=mode,
            operator_id=operator.id,
            classification="internal",
            correlation_id=correlation_id,
            details={
                "series_created": created,
                "series_updated": updated,
                "series_unchanged": unchanged,
                "exceptions_appended": appended,
                "exceptions_deduplicated": deduplicated,
                "unmapped_sources": sorted(unmapped_sources),
            },
        )
    )

    return V2MdCatalogRefreshResponse(
        series_created=created,
        series_updated=updated,
        series_unchanged=unchanged,
        exceptions_appended=appended,
        exceptions_deduplicated=deduplicated,
        unmapped_sources=sorted(unmapped_sources),
        **_envelope(request),
    )


async def _load_scope_rows(
    session: AsyncSession,
    scope_items: list[VerificationScopeItem],
    as_of: datetime,
) -> tuple[list, list[str]]:
    ref_repo = V2MdReferenceRepository(session)
    boundary = V2MdBarReadBoundary(session)
    rows: list = []
    source_ids: set[str] = set()
    for item in scope_items:
        instrument = await ref_repo.get_instrument(item.instrument_id)
        source = await ref_repo.get_source(item.source_id)
        if instrument is None or source is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Instrument or source not found",
            )
        bars = await boundary.read_bars(
            market_class=instrument.market_class,
            symbol=instrument.display_symbol,
            timeframe=item.timeframe.upper(),
            as_of=as_of,
            limit=1000,
        )
        rows.extend(b for b in bars if b.source == source.authority)
        source_ids.add(item.source_id)
    return rows, sorted(source_ids)


@router.post("/verification", response_model=V2MdVerificationDetailResponse)
async def create_verification(
    payload: V2MdVerificationCreateRequest,
    request: Request,
    operator: RequireV2MarketDataVerify,
    session: AsyncSession = Depends(get_db_session),
) -> V2MdVerificationDetailResponse:
    """W-2 — append one As-Of Verification Record (tamper-evidence only).

    NOT a snapshot: reconstructive=false in the response contract. Audited;
    lineage-linked.
    """
    mode = request.app.state.v2_mode
    correlation_id = getattr(request.state, "correlation_id", None) or new_id()
    now = utc_now()
    require_utc(payload.as_of, boundary="as_of")
    if payload.as_of > now:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="as_of may not be in the future",
        )
    scope_items = [
        VerificationScopeItem(
            instrument_id=i.instrument_id,
            timeframe=i.timeframe.upper(),
            source_id=i.source_id,
        )
        for i in payload.scope
    ]
    validate_scope(scope_items, payload.as_of)

    rows, source_ids = await _load_scope_rows(session, scope_items, payload.as_of)
    content_hash = compute_content_hash(rows)
    verification_id = f"mdv-{new_id()[:24]}"

    repo = V2MdVerificationRepository(session)
    record = await repo.append(
        verification_id=verification_id,
        scope={
            "items": [
                {
                    "instrument_id": s.instrument_id,
                    "timeframe": s.timeframe,
                    "source_id": s.source_id,
                }
                for s in scope_items
            ],
            "window": "as_of-bounded",
        },
        as_of=payload.as_of,
        content_hash=content_hash,
        row_count=len(rows),
        source_ids=source_ids,
        mode=mode,
        created_by_operator_id=operator.id,
    )

    lineage_repo = V2LineageRepository(session)
    await lineage_repo.append(
        V2LineageRecordCreate(
            artifact_type="md_asof_verification",
            artifact_id=verification_id,
            source_artifact_ids=source_ids,
            computation_version="be2-v1",
            input_snapshot_id=None,
            operator_id=operator.id,
            mode=mode,
        )
    )
    audit_repo = V2AuditRepository(session)
    await audit_repo.append(
        V2AuditEventCreate(
            domain="v2.marketdata",
            action="verification.create",
            actor_id=operator.id,
            actor_type="operator",
            mode=mode,
            operator_id=operator.id,
            resource_type="md_asof_verification",
            resource_id=verification_id,
            classification="internal",
            correlation_id=correlation_id,
            details={"row_count": len(rows), "content_hash": content_hash},
        )
    )

    return V2MdVerificationDetailResponse(
        record=_verification_model(record), **_envelope(request)
    )


@router.post(
    "/verification/{verification_id}/verify", response_model=V2MdVerifyResultResponse
)
async def reverify(
    verification_id: str,
    request: Request,
    operator: RequireV2MarketDataVerify,
    session: AsyncSession = Depends(get_db_session),
) -> V2MdVerifyResultResponse:
    """W-2 — recompute the hash over the same scope/as_of.

    Match → pure comparison, no state written beyond the audit event.
    Mismatch → one fingerprint-deduplicated `verification_mismatch` exception
    (first-detection edge; repeated re-verification of the same mismatch is a
    no-op).
    """
    mode = request.app.state.v2_mode
    correlation_id = getattr(request.state, "correlation_id", None) or new_id()

    repo = V2MdVerificationRepository(session)
    record = await repo.get(verification_id, operator_id=operator.id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Verification record not found"
        )

    scope_items = [
        VerificationScopeItem(
            instrument_id=i["instrument_id"],
            timeframe=i["timeframe"],
            source_id=i["source_id"],
        )
        for i in record.scope["items"]
    ]
    rows, _ = await _load_scope_rows(session, scope_items, record.as_of)
    actual_hash = compute_content_hash(rows)
    match = actual_hash == record.content_hash

    if not match:
        integrity_repo = V2MdIntegrityRepository(session)
        await integrity_repo.append_finding(
            verification_mismatch_finding(verification_id, record.content_hash, actual_hash),
            operator_id=operator.id,
            mode=mode,
            correlation_id=correlation_id,
        )

    audit_repo = V2AuditRepository(session)
    await audit_repo.append(
        V2AuditEventCreate(
            domain="v2.marketdata",
            action="verification.reverify",
            actor_id=operator.id,
            actor_type="operator",
            mode=mode,
            operator_id=operator.id,
            resource_type="md_asof_verification",
            resource_id=verification_id,
            classification="internal",
            correlation_id=correlation_id,
            details={"match": match},
        )
    )

    return V2MdVerifyResultResponse(
        verification_id=verification_id,
        match=match,
        expected_hash=record.content_hash,
        actual_hash=actual_hash,
        row_count_now=len(rows),
        **_envelope(request),
    )
