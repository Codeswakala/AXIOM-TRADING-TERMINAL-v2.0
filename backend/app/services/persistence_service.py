"""Persistence application service boundary (W1-U01).

Routers delegate persistence workflows here so HTTP controllers remain thin and
ORM/database details stay behind repositories and services.
"""

from __future__ import annotations

from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.db.models.audit import AuditEvent
from app.db.models.candle import Candle
from app.models.indicators import (
    BandIndicatorRead,
    BandPointRead,
    IndicatorSeriesEnvelope,
    InsufficientIndicatorRead,
    LineIndicatorRead,
    LinePointRead,
    MacdIndicatorRead,
    MacdPointRead,
    MultiIndicatorRead,
)
from app.models.persistence import (
    CandleCreate,
    CandleRead,
    CandleSeriesEnvelope,
    DatabaseStatsResponse,
)
from app.repositories.audit_repository import AuditRepository
from app.services.candle_service import CandleService
from app.services.database_health import check_database
from app.services.indicator_registry import INDICATOR_REGISTRY
from app.services.indicators import BandPoint, LinePoint, MacdPoint
from app.services.ohlcv_aggregation import aggregate_m1_to_target
from app.services.timeframes import TIMEFRAME_MINUTES


class PersistenceService:
    """Application service for persistence API workflows."""

    # CHART-P02: computation window for indicator series (2 days of M1 bars —
    # enough for a full prior-day derivation plus margin).
    COMPUTE_WINDOW_LIMIT = 2880

    def __init__(self, session: AsyncSession, settings: Settings) -> None:
        self._session = session
        self._settings = settings
        self._candles = CandleService(session)
        self._audit = AuditRepository(session)

    async def create_candle(self, payload: CandleCreate) -> Candle:
        return await self._candles.create_candle(**payload.model_dump())

    async def list_candles(
        self,
        *,
        symbol: str,
        timeframe: str | None = None,
        market_class: str | None = None,
        limit: int = 100,
        ascending: bool = False,
    ) -> list[Candle]:
        return await self._candles.list_candles(
            symbol=symbol,
            timeframe=timeframe,
            market_class=market_class,
            limit=limit,
            ascending=ascending,
        )

    async def get_candle(self, candle_id: str) -> Candle | None:
        return await self._candles.get(candle_id)

    async def indicator_series(
        self,
        *,
        symbol: str,
        timeframe: str,
        indicator_ids: list[str],
        limit: int = 100,
    ) -> IndicatorSeriesEnvelope:
        """CHART-P01 M1/M6 + CHART-P02 window extension, stated:
        indicators are server work; the underlying series kind travels on the
        envelope (native/aggregated); an unavailable series yields NO
        indicator computation — detail states why. Insufficient history is a
        typed per-indicator result, never a padded value.

        CHART-P02 adds day/session-derived LEVEL indicators whose
        full-definition requirement (one prior UTC day: 1440 M1 bars) exceeds
        the displayed chart window. The endpoint therefore computes over a
        longer window (up to COMPUTE_WINDOW_LIMIT bars, reusing the existing
        native/aggregated series path) and TRIMS every output to the last
        `limit` points — the displayed window. Computation-window extension
        only; the chart still receives exactly its displayed series length."""
        # Extended compute window ONLY when a level indicator is requested
        # (their full-definition needs a prior UTC day of bars); otherwise the
        # standard displayed window serves, keeping the common path cheap.
        needs_extended = any(
            INDICATOR_REGISTRY[i].required_bars_fn is not None for i in indicator_ids
        )
        compute_limit = self.COMPUTE_WINDOW_LIMIT if needs_extended else limit
        series = await self.candle_series(
            symbol=symbol,
            timeframe=timeframe,
            limit=compute_limit,
            ascending=True,
        )
        if series.kind == "unavailable":
            return IndicatorSeriesEnvelope(
                symbol=symbol,
                timeframe=timeframe,
                seriesKind="unavailable",
                detail=series.detail,
                indicators={},
            )

        bars = series.bars
        tf_minutes = TIMEFRAME_MINUTES[timeframe]
        indicators: dict = {}
        for indicator_id in indicator_ids:
            definition = INDICATOR_REGISTRY[indicator_id]
            if definition.required_bars_fn is not None:
                required = definition.required_bars_fn(tf_minutes)
                if required is None:
                    indicators[indicator_id] = InsufficientIndicatorRead(
                        required=0,
                        available=len(bars),
                        detail=f"not resolvable at this timeframe ({timeframe} bars span multiple sessions)",
                    )
                    continue
            else:
                required = definition.required_bars
            if required is not None and len(bars) < required:
                indicators[indicator_id] = InsufficientIndicatorRead(
                    required=required,
                    available=len(bars),
                )
                continue
            if definition.required_bars_fn is not None:
                outcome = definition.compute(bars, tf_minutes)
            else:
                outcome = definition.compute(bars)
            if outcome.kind == "insufficient":
                indicators[indicator_id] = InsufficientIndicatorRead(
                    required=outcome.required if outcome.required is not None else (required or 0),
                    available=outcome.available if outcome.available is not None else len(bars),
                )
                continue
            if outcome.lines is not None:
                indicators[indicator_id] = MultiIndicatorRead(
                    shape="multi",
                    kind="computed",
                    lines={
                        name: (
                            [LinePointRead(time=p.time, value=p.value) for p in pts][-limit:]
                            if needs_extended
                            else [LinePointRead(time=p.time, value=p.value) for p in pts]
                        )
                        for name, pts in outcome.lines.items()
                    },
                )
            else:
                trimmed = outcome.points[-limit:] if needs_extended else outcome.points
                indicators[indicator_id] = _read_for_points(trimmed)

        return IndicatorSeriesEnvelope(
            symbol=symbol,
            timeframe=timeframe,
            seriesKind=series.kind,
            sourceTimeframe=series.sourceTimeframe,
            excludedPartialBuckets=series.excludedPartialBuckets,
            indicators=indicators,
        )

    async def candle_series(
        self,
        *,
        symbol: str,
        timeframe: str,
        market_class: str | None = None,
        limit: int = 100,
        ascending: bool = False,
    ) -> CandleSeriesEnvelope:
        """DATA-P02 M4: typed series result.

        kind=native      — bars stored at the requested timeframe (M1 today;
                           higher timeframes if ever stored natively).
        kind=aggregated  — bars computed from M1 at request time, wall-clock
                           aligned; partial buckets excluded and disclosed via
                           excludedPartialBuckets.
        kind=unavailable — insufficient M1 coverage to form one complete
                           bucket; the chart must render absence, not an
                           improvised series.
        """
        if timeframe == "M1":
            rows = await self._candles.list_candles(
                symbol=symbol,
                timeframe="M1",
                market_class=market_class,
                limit=limit,
                ascending=ascending,
            )
            if not rows:
                return CandleSeriesEnvelope(
                    kind="unavailable",
                    timeframe="M1",
                    detail=f"No M1 bars stored for symbol {symbol}",
                    bars=[],
                )
            return CandleSeriesEnvelope(
                kind="native",
                timeframe="M1",
                bars=[CandleRead.model_validate(row) for row in rows],
            )

        # Forward-compatible native path: rows stored at the higher timeframe.
        stored = await self._candles.list_candles(
            symbol=symbol,
            timeframe=timeframe,
            market_class=market_class,
            limit=1,
            ascending=False,
        )
        if stored:
            rows = await self._candles.list_candles(
                symbol=symbol,
                timeframe=timeframe,
                market_class=market_class,
                limit=limit,
                ascending=ascending,
            )
            return CandleSeriesEnvelope(
                kind="native",
                timeframe=timeframe,
                bars=[CandleRead.model_validate(row) for row in rows],
            )

        minutes = TIMEFRAME_MINUTES[timeframe]
        m1_rows = await self._candles.list_all_for_symbol(
            symbol=symbol,
            timeframe="M1",
            market_class=market_class,
            ascending=True,
        )
        outcome = aggregate_m1_to_target(
            m1_rows,
            target_minutes=minutes,
            target_timeframe=timeframe,
        )
        if not outcome.bars:
            detail = (
                f"insufficient M1 coverage to form a complete {timeframe} bucket: "
                f"stored M1 bars {outcome.unaggregated_total}, "
                f"partial buckets excluded {outcome.excluded_partial}"
            )
            return CandleSeriesEnvelope(
                kind="unavailable",
                timeframe=timeframe,
                detail=detail,
                bars=[],
            )

        bars = list(outcome.bars)[-limit:]
        if not ascending:
            bars = list(reversed(bars))
        reads = [
            CandleRead(
                id=bar.id,
                market_class=bar.market_class,
                symbol=bar.symbol,
                timeframe=bar.timeframe,
                open_time=bar.open_time,
                open=bar.open,
                high=bar.high,
                low=bar.low,
                close=bar.close,
                volume=bar.volume if bar.volume != Decimal("0") else None,
                source=bar.source,
                created_at=bar.open_time,
                complete=True,
                constituents=bar.constituents,
            )
            for bar in bars
        ]
        return CandleSeriesEnvelope(
            kind="aggregated",
            timeframe=timeframe,
            sourceTimeframe="M1",
            excludedPartialBuckets=outcome.excluded_partial,
            bars=reads,
        )

    async def list_audit_events(
        self,
        *,
        category: str | None = None,
        limit: int = 50,
    ) -> list[AuditEvent]:
        return list(await self._audit.list_recent(category=category, limit=limit))

    async def database_stats(self) -> DatabaseStatsResponse:
        db = await check_database(self._settings)
        candle_count = int(
            (await self._session.execute(select(func.count()).select_from(Candle))).scalar_one()
        )
        audit_count = int(
            (await self._session.execute(select(func.count()).select_from(AuditEvent))).scalar_one()
        )
        scheme = self._settings.database_url.split("://", 1)[0]
        return DatabaseStatsResponse(
            backend=db.backend,
            database_url_scheme=scheme,
            pool=db.pool,
            candle_count=candle_count,
            audit_count=audit_count,
        )


def _read_for_points(points: list) -> object:
    """Convert computed indicator points into their read-model shape.

    The shape is decided by the point type (LinePoint/BandPoint/MacdPoint) —
    a typed mapping, never inferred from values."""
    if not points:
        return LineIndicatorRead(shape="line", kind="computed", points=[])
    if isinstance(points[0], BandPoint):
        return BandIndicatorRead(
            shape="band",
            kind="computed",
            points=[
                BandPointRead(time=p.time, upper=p.upper, middle=p.middle, lower=p.lower)
                for p in points
                if isinstance(p, BandPoint)
            ],
        )
    if isinstance(points[0], MacdPoint):
        return MacdIndicatorRead(
            shape="macd",
            kind="computed",
            points=[
                MacdPointRead(time=p.time, macd=p.macd, signal=p.signal, histogram=p.histogram)
                for p in points
                if isinstance(p, MacdPoint)
            ],
        )
    return LineIndicatorRead(
        shape="line",
        kind="computed",
        points=[
            LinePointRead(time=p.time, value=p.value) for p in points if isinstance(p, LinePoint)
        ],
    )
