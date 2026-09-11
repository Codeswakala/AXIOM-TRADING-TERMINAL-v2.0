"""Application service for candle persistence demos and future market data."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.core.time import require_utc
from app.db.models.candle import Candle
from app.repositories.audit_repository import AuditRepository
from app.repositories.candle_repository import CandleRepository

logger = get_logger(__name__, category="MARKET")


class CandleService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._candles = CandleRepository(session)
        self._audit = AuditRepository(session)

    async def create_candle(
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
        volume: Decimal | None = None,
        source: str | None = "manual",
    ) -> Candle:
        normalized_open_time = require_utc(open_time, boundary="candle_service.open_time")
        assert normalized_open_time is not None
        existing = await self._candles.get_by_natural_key(
            market_class=market_class,
            symbol=symbol,
            timeframe=timeframe,
            open_time=normalized_open_time,
        )
        if existing is not None:
            logger.info("Candle already exists id=%s", existing.id)
            return existing

        candle = Candle(
            market_class=market_class,
            symbol=symbol,
            timeframe=timeframe,
            open_time=normalized_open_time,
            open=open,
            high=high,
            low=low,
            close=close,
            volume=volume,
            source=source,
        )
        created = await self._candles.add(candle, refresh=False)
        await self._audit.append(
            category="DATABASE",
            action="candle.create",
            message=f"Created candle {symbol} {timeframe}",
            resource_type="candle",
            resource_id=created.id,
            details={
                "market_class": market_class,
                "symbol": symbol,
                "timeframe": timeframe,
            },
        )
        return created

    async def list_candles(
        self,
        *,
        symbol: str,
        timeframe: str | None = None,
        market_class: str | None = None,
        limit: int = 100,
        ascending: bool = False,
    ) -> list[Candle]:
        rows = await self._candles.list_for_symbol(
            symbol=symbol,
            timeframe=timeframe,
            market_class=market_class,
            limit=limit,
            ascending=ascending,
        )
        return list(rows)

    async def list_all_for_symbol(
        self,
        *,
        symbol: str,
        timeframe: str | None = None,
        market_class: str | None = None,
        ascending: bool = True,
        max_rows: int = 500_000,
    ) -> list[Candle]:
        """Full stored series (bounded) — DATA-P02 aggregation needs the
        complete M1 window, not the latest N rows."""
        rows = await self._candles.list_all_for_symbol(
            symbol=symbol,
            timeframe=timeframe,
            market_class=market_class,
            ascending=ascending,
            max_rows=max_rows,
        )
        return list(rows)

    async def get(self, candle_id: str) -> Candle | None:
        return await self._candles.get_by_id(candle_id)
