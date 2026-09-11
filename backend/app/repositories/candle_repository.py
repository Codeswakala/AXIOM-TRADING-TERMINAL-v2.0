"""Candle repository — multi-market OHLCV access patterns + upsert."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.core.time import require_utc
from app.db.models.candle import Candle
from app.repositories.base import BaseRepository

logger = get_logger(__name__, category="DATABASE")


class CandleRepository(BaseRepository[Candle]):
    model = Candle

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get_by_natural_key(
        self,
        *,
        market_class: str,
        symbol: str,
        timeframe: str,
        open_time: datetime,
    ) -> Candle | None:
        normalized_time = require_utc(open_time, boundary="candle_repository.open_time")
        assert normalized_time is not None
        stmt = select(Candle).where(
            Candle.market_class == market_class,
            Candle.symbol == symbol,
            Candle.timeframe == timeframe,
            Candle.open_time == normalized_time,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_for_symbol(
        self,
        *,
        symbol: str,
        timeframe: str | None = None,
        market_class: str | None = None,
        limit: int = 100,
        offset: int = 0,
        ascending: bool = False,
    ) -> Sequence[Candle]:
        stmt = select(Candle).where(Candle.symbol == symbol)
        if timeframe is not None:
            stmt = stmt.where(Candle.timeframe == timeframe)
        if market_class is not None:
            stmt = stmt.where(Candle.market_class == market_class)
        # For charts: take the latest N bars, then return chronological order.
        order = Candle.open_time.asc() if ascending else Candle.open_time.desc()
        if ascending:
            # Subquery-style: fetch newest first then reverse in Python for SQLite simplicity
            stmt_desc = (
                select(Candle)
                .where(Candle.symbol == symbol)
            )
            if timeframe is not None:
                stmt_desc = stmt_desc.where(Candle.timeframe == timeframe)
            if market_class is not None:
                stmt_desc = stmt_desc.where(Candle.market_class == market_class)
            stmt_desc = stmt_desc.order_by(Candle.open_time.desc()).limit(limit).offset(offset)
            result = await self.session.execute(stmt_desc)
            rows = list(result.scalars().all())
            rows.reverse()
            return rows
        stmt = stmt.order_by(order).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def list_all_for_symbol(
        self,
        *,
        symbol: str,
        timeframe: str | None = None,
        market_class: str | None = None,
        ascending: bool = True,
        max_rows: int = 500_000,
    ) -> Sequence[Candle]:
        """Full stored series for one symbol (bounded) — used by DATA-P02
        server-side aggregation, which needs the complete M1 window."""
        stmt = select(Candle).where(Candle.symbol == symbol)
        if timeframe is not None:
            stmt = stmt.where(Candle.timeframe == timeframe)
        if market_class is not None:
            stmt = stmt.where(Candle.market_class == market_class)
        stmt = (
            stmt.order_by(Candle.open_time.asc() if ascending else Candle.open_time.desc())
            .limit(max_rows)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def list_window_as_of(
        self,
        *,
        market_class: str,
        symbol: str,
        timeframe: str,
        as_of_time: datetime,
        limit: int,
        allowed_sources: Sequence[str] | None = None,
    ) -> Sequence[Candle]:
        """Return latest candles at or before as-of time, oldest → newest."""
        normalized_as_of = require_utc(as_of_time, boundary="candle_repository.as_of_time")
        assert normalized_as_of is not None
        stmt = select(Candle).where(
            Candle.market_class == market_class,
            Candle.symbol == symbol,
            Candle.timeframe == timeframe,
            Candle.open_time <= normalized_as_of,
        )
        if allowed_sources:
            stmt = stmt.where(Candle.source.in_(tuple(allowed_sources)))
        stmt = stmt.order_by(Candle.open_time.desc()).limit(limit)
        result = await self.session.execute(stmt)
        rows = list(result.scalars().all())
        rows.reverse()
        return rows

    async def count_after(
        self,
        *,
        market_class: str,
        symbol: str,
        timeframe: str,
        after_time: datetime,
    ) -> int:
        """Count candles after the requested as-of anchor for no-look-ahead evidence."""
        normalized_after = require_utc(after_time, boundary="candle_repository.after_time")
        assert normalized_after is not None
        stmt = (
            select(func.count())
            .select_from(Candle)
            .where(
                Candle.market_class == market_class,
                Candle.symbol == symbol,
                Candle.timeframe == timeframe,
                Candle.open_time > normalized_after,
            )
        )
        result = await self.session.execute(stmt)
        return int(result.scalar_one())

    async def count_by_market(
        self,
        *,
        market_class: str | None = None,
        symbol: str | None = None,
        timeframe: str | None = None,
    ) -> int:
        stmt = select(func.count()).select_from(Candle)
        if market_class is not None:
            stmt = stmt.where(Candle.market_class == market_class)
        if symbol is not None:
            stmt = stmt.where(Candle.symbol == symbol)
        if timeframe is not None:
            stmt = stmt.where(Candle.timeframe == timeframe)
        result = await self.session.execute(stmt)
        return int(result.scalar_one())

    async def upsert_ohlcv(
        self,
        *,
        market_class: str,
        symbol: str,
        timeframe: str,
        open_time: datetime,
        open: Decimal,
        high: Decimal,
        low: Decimal,
        close: Decimal,
        volume: Decimal | None,
        source: str | None,
    ) -> tuple[Candle, str]:
        """Insert or update by natural key.

        Returns (entity, action) where action is inserted | updated | unchanged.
        """
        normalized_time = require_utc(open_time, boundary="candle_repository.open_time")
        assert normalized_time is not None
        existing = await self.get_by_natural_key(
            market_class=market_class,
            symbol=symbol,
            timeframe=timeframe,
            open_time=normalized_time,
        )
        if existing is None:
            entity = Candle(
                market_class=market_class,
                symbol=symbol,
                timeframe=timeframe,
                open_time=normalized_time,
                open=open,
                high=high,
                low=low,
                close=close,
                volume=volume,
                source=source,
            )
            self.session.add(entity)
            await self.session.flush()
            # Avoid refresh() for bulk seed performance and SQLite stability
            return entity, "inserted"

        changed = (
            existing.open != open
            or existing.high != high
            or existing.low != low
            or existing.close != close
            or existing.volume != volume
        )
        if not changed:
            return existing, "unchanged"

        existing.open = open
        existing.high = high
        existing.low = low
        existing.close = close
        existing.volume = volume
        if source is not None:
            existing.source = source
        await self.session.flush()
        await self.session.refresh(existing)
        logger.info("upsert updated candle id=%s", existing.id)
        return existing, "updated"
