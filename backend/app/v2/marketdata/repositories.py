"""V2 BE-2 repositories — reference reads, catalog upsert (W-1 only),
fingerprint-deduplicated exception append, verification append (W-2 only).

Append-only tables expose no update/delete methods; DB triggers enforce
immutability. GET paths use only the read methods here (persistence-pure).
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.candle import Candle
from app.db.models.v2_marketdata import (
    V2MdAsOfVerification,
    V2MdInstrument,
    V2MdIntegrityException,
    V2MdSeries,
    V2MdSource,
    V2MdSymbolMap,
)
from app.v2.audit.redaction import redact
from app.v2.identifiers import new_id
from app.v2.marketdata.integrity import IntegrityFinding
from app.v2.temporal.validation import require_utc, utc_now


def _utc_from_store(value: datetime | None) -> datetime | None:
    """Normalize a datetime read from the database to aware UTC.

    SQLite discards timezone info on DateTime(timezone=True) columns and
    returns naive values; PostgreSQL returns aware values. All V1/V2 rows are
    written as UTC, so attaching UTC to a store-read naive value is a
    deterministic dialect normalization — NOT naive-input coercion (external/
    client naive datetimes remain rejected by require_utc()).
    """
    from datetime import timezone as _tz

    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=_tz.utc)
    return value


class V2MdReferenceRepository:
    """Read-only reference data (instruments, mappings, sources)."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_instruments(self) -> list[V2MdInstrument]:
        result = await self._session.execute(
            select(V2MdInstrument).order_by(V2MdInstrument.instrument_id)
        )
        return list(result.scalars().all())

    async def get_instrument(self, instrument_id: str) -> V2MdInstrument | None:
        result = await self._session.execute(
            select(V2MdInstrument).where(V2MdInstrument.instrument_id == instrument_id)
        )
        return result.scalar_one_or_none()

    async def list_sources(self) -> list[V2MdSource]:
        result = await self._session.execute(
            select(V2MdSource).order_by(V2MdSource.source_id)
        )
        return list(result.scalars().all())

    async def get_source(self, source_id: str) -> V2MdSource | None:
        result = await self._session.execute(
            select(V2MdSource).where(V2MdSource.source_id == source_id)
        )
        return result.scalar_one_or_none()

    async def list_mappings(self) -> list[V2MdSymbolMap]:
        result = await self._session.execute(
            select(V2MdSymbolMap).order_by(V2MdSymbolMap.source_id, V2MdSymbolMap.source_symbol)
        )
        return list(result.scalars().all())

    async def resolve_symbol(self, source_id: str, source_symbol: str) -> V2MdSymbolMap | None:
        result = await self._session.execute(
            select(V2MdSymbolMap).where(
                V2MdSymbolMap.source_id == source_id,
                V2MdSymbolMap.source_symbol == source_symbol,
            )
        )
        return result.scalar_one_or_none()


class V2MdSeriesRepository:
    """Series catalog. Upsert is W-1-only; reads are pure."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_series(self) -> list[V2MdSeries]:
        result = await self._session.execute(
            select(V2MdSeries).order_by(V2MdSeries.instrument_id, V2MdSeries.timeframe)
        )
        rows = list(result.scalars().all())
        for row in rows:
            row.first_open_time = _utc_from_store(row.first_open_time)
            row.last_open_time = _utc_from_store(row.last_open_time)
        return rows

    async def get_series(
        self, instrument_id: str, timeframe: str, source_id: str
    ) -> V2MdSeries | None:
        result = await self._session.execute(
            select(V2MdSeries).where(
                V2MdSeries.instrument_id == instrument_id,
                V2MdSeries.timeframe == timeframe,
                V2MdSeries.source_id == source_id,
            )
        )
        return result.scalar_one_or_none()

    async def upsert_series(
        self,
        *,
        instrument_id: str,
        timeframe: str,
        source_id: str,
        first_open_time: datetime | None,
        last_open_time: datetime | None,
        bar_count: int,
    ) -> tuple[V2MdSeries, str]:
        """W-1 only. Returns (row, 'created'|'updated'|'unchanged')."""
        if first_open_time is not None:
            require_utc(first_open_time, boundary="first_open_time")
        if last_open_time is not None:
            require_utc(last_open_time, boundary="last_open_time")
        existing = await self.get_series(instrument_id, timeframe, source_id)
        if existing is not None:
            existing.first_open_time = _utc_from_store(existing.first_open_time)
            existing.last_open_time = _utc_from_store(existing.last_open_time)
        if existing is None:
            row = V2MdSeries(
                id=new_id(),
                instrument_id=instrument_id,
                timeframe=timeframe,
                source_id=source_id,
                first_open_time=first_open_time,
                last_open_time=last_open_time,
                bar_count=bar_count,
                updated_at=utc_now(),
                created_at=utc_now(),
            )
            self._session.add(row)
            await self._session.flush()
            return row, "created"
        if (
            existing.first_open_time == first_open_time
            and existing.last_open_time == last_open_time
            and existing.bar_count == bar_count
        ):
            return existing, "unchanged"
        existing.first_open_time = first_open_time
        existing.last_open_time = last_open_time
        existing.bar_count = bar_count
        existing.updated_at = utc_now()
        await self._session.flush()
        return existing, "updated"


class V2MdIntegrityRepository:
    """Append-only, fingerprint-deduplicated exception store (W-1/W-2 only)."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def append_finding(
        self,
        finding: IntegrityFinding,
        *,
        operator_id: str,
        mode: str,
        correlation_id: str | None,
    ) -> V2MdIntegrityException | None:
        """Insert one finding owned by the W-1/W-2 actor (DEL-002);
        fingerprint collision → no-op (returns None)."""
        existing = await self._session.execute(
            select(V2MdIntegrityException.id).where(
                V2MdIntegrityException.fingerprint == finding.fingerprint
            )
        )
        if existing.scalar_one_or_none() is not None:
            return None
        row = V2MdIntegrityException(
            id=new_id(),
            series_ref=finding.series_ref,
            operator_id=operator_id,
            exception_type=finding.exception_type,
            fingerprint=finding.fingerprint,
            detail=redact(finding.detail),
            observed_at=finding.observed_at,
            mode=mode,
            correlation_id=correlation_id,
            created_at=utc_now(),
        )
        self._session.add(row)
        await self._session.flush()
        return row

    async def list_exceptions(
        self,
        *,
        mode: str,
        operator_id: str,
        series_ref: str | None = None,
        limit: int = 100,
    ) -> list[V2MdIntegrityException]:
        """Operator-scoped read (SAL-3, DEL-002): own records only."""
        stmt = (
            select(V2MdIntegrityException)
            .where(
                V2MdIntegrityException.mode == mode,
                V2MdIntegrityException.operator_id == operator_id,
            )
            .order_by(V2MdIntegrityException.observed_at.desc())
            .limit(limit)
        )
        if series_ref:
            stmt = stmt.where(V2MdIntegrityException.series_ref == series_ref)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def list_all_exceptions(
        self, *, mode: str, series_ref: str | None = None, limit: int = 100
    ) -> list[V2MdIntegrityException]:
        """Admin-only cross-operator read (SAL-4); caller must audit."""
        stmt = (
            select(V2MdIntegrityException)
            .where(V2MdIntegrityException.mode == mode)
            .order_by(V2MdIntegrityException.observed_at.desc())
            .limit(limit)
        )
        if series_ref:
            stmt = stmt.where(V2MdIntegrityException.series_ref == series_ref)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def exists_for_series(self, *, mode: str, series_ref: str) -> dict[str, bool]:
        """Non-disclosing existence flags for availability labelling only.

        Returns which exception classes exist for a series without exposing
        any record detail — availability labels stay honest for every
        operator while SAL-3 record contents remain owner-scoped.
        """
        stmt = select(V2MdIntegrityException.exception_type).where(
            V2MdIntegrityException.mode == mode,
            V2MdIntegrityException.series_ref == series_ref,
        )
        result = await self._session.execute(stmt)
        types = {row[0] for row in result.all()}
        return {
            "quarantine": bool(types & {"out_of_order", "duplicate", "future_data"}),
            "partial": bool(types),
        }

    async def count_all(self) -> int:
        result = await self._session.execute(
            select(func.count()).select_from(V2MdIntegrityException)
        )
        return int(result.scalar_one())


class V2MdVerificationRepository:
    """Append-only As-Of Verification Records (W-2 only)."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def append(
        self,
        *,
        verification_id: str,
        scope: dict[str, Any],
        as_of: datetime,
        content_hash: str,
        row_count: int,
        source_ids: list[str],
        mode: str,
        created_by_operator_id: str,
    ) -> V2MdAsOfVerification:
        require_utc(as_of, boundary="as_of")
        row = V2MdAsOfVerification(
            id=new_id(),
            verification_id=verification_id,
            scope=scope,
            as_of=as_of,
            content_hash=content_hash,
            row_count=row_count,
            source_ids=source_ids,
            mode=mode,
            created_by_operator_id=created_by_operator_id,
            created_at=utc_now(),
        )
        self._session.add(row)
        await self._session.flush()
        return row

    async def read_by_operator(
        self, operator_id: str, *, limit: int = 50
    ) -> list[V2MdAsOfVerification]:
        result = await self._session.execute(
            select(V2MdAsOfVerification)
            .where(V2MdAsOfVerification.created_by_operator_id == operator_id)
            .order_by(V2MdAsOfVerification.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def read_all(self, *, limit: int = 50) -> list[V2MdAsOfVerification]:
        result = await self._session.execute(
            select(V2MdAsOfVerification)
            .order_by(V2MdAsOfVerification.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get(
        self, verification_id: str, *, operator_id: str | None = None
    ) -> V2MdAsOfVerification | None:
        stmt = select(V2MdAsOfVerification).where(
            V2MdAsOfVerification.verification_id == verification_id
        )
        if operator_id is not None:
            stmt = stmt.where(V2MdAsOfVerification.created_by_operator_id == operator_id)
        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        if row is not None:
            row.as_of = _utc_from_store(row.as_of)
        return row


class V2MdBarReadBoundary:
    """Read-only boundary over the V1 `candles` store (D-1 wrap model).

    Never writes; never copies. Attaches nothing itself — provenance is
    attached by the service layer from the source registry.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def read_bars(
        self,
        *,
        market_class: str,
        symbol: str,
        timeframe: str,
        as_of: datetime | None = None,
        limit: int = 500,
    ) -> list[Candle]:
        stmt = (
            select(Candle)
            .where(
                Candle.market_class == market_class,
                Candle.symbol == symbol,
                Candle.timeframe == timeframe,
            )
            .order_by(Candle.open_time.desc())
            .limit(min(limit, 1000))
        )
        if as_of is not None:
            require_utc(as_of, boundary="as_of")
            stmt = stmt.where(Candle.open_time <= as_of)
        result = await self._session.execute(stmt)
        rows = list(result.scalars().all())
        rows.reverse()  # ascending for presentation
        for row in rows:
            row.open_time = _utc_from_store(row.open_time)
        return rows

    async def series_summary(
        self, *, market_class: str, symbol: str, timeframe: str, source_marker: str
    ) -> tuple[datetime | None, datetime | None, int]:
        stmt = select(
            func.min(Candle.open_time),
            func.max(Candle.open_time),
            func.count(),
        ).where(
            Candle.market_class == market_class,
            Candle.symbol == symbol,
            Candle.timeframe == timeframe,
            Candle.source == source_marker,
        )
        result = await self._session.execute(stmt)
        first, last, count = result.one()
        return _utc_from_store(first), _utc_from_store(last), int(count)

    async def distinct_series_keys(self) -> list[tuple[str, str, str, str | None]]:
        """(market_class, symbol, timeframe, source) present in the V1 store."""
        stmt = select(
            Candle.market_class, Candle.symbol, Candle.timeframe, Candle.source
        ).distinct()
        result = await self._session.execute(stmt)
        return [tuple(row) for row in result.all()]
