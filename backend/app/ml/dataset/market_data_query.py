"""Market-agnostic data access contract for ML Research System (W2-U02)."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Protocol, Sequence

from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.time import coerce_external_utc, require_utc
from app.db.models.candle import Candle
from app.db.models.market_metadata import MarketSeriesMetadata
from app.ml.dataset.chronology_guard import SourceAuthority


class CanonicalMarketClass(StrEnum):
    SYNTHETIC = "synthetic"
    FOREX = "forex"
    CRYPTO = "crypto"
    STOCKS = "stocks"
    INDICES = "indices"
    ETFS = "etfs"
    COMMODITIES = "commodities"
    FUTURES = "futures"


CANONICAL_MARKET_CLASSES = {item.value for item in CanonicalMarketClass}


class MarketSeriesKey(BaseModel):
    """Uniform market series address tuple for ML access."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    market_class: str
    provider: str
    symbol: str
    timeframe: str

    @field_validator("market_class")
    @classmethod
    def _canonical_market_class(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized not in CANONICAL_MARKET_CLASSES:
            raise ValueError(f"unsupported market_class={value!r}")
        return normalized

    @field_validator("provider", "symbol", "timeframe")
    @classmethod
    def _not_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("series key fields must not be empty")
        return normalized.upper() if value == value.upper() else normalized


class MarketSeriesMetadataRead(BaseModel):
    """Governance/evaluation metadata only — never a learned feature."""

    model_config = ConfigDict(extra="forbid")

    series_key: MarketSeriesKey
    session_calendar: str | None = None
    tick_size: Decimal | None = None
    price_precision: int | None = Field(default=None, ge=0)
    timezone_assumption: str = "UTC"
    source_authority: SourceAuthority
    known_limitations: str | None = None
    metadata_role: str = "governance_evaluation_only"


class SourceMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source: str
    authority: SourceAuthority
    provider: str


class CanonicalOHLCVRecord(BaseModel):
    """Broker/provider-neutral OHLCV boundary record."""

    model_config = ConfigDict(extra="forbid")

    series_key: MarketSeriesKey
    open_time: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal | None = None
    source: str
    ingestion_run_id: str | None = None
    authority_classification: SourceAuthority
    source_record_id: str | None = None

    @field_validator("open_time")
    @classmethod
    def _open_time_utc(cls, value: datetime) -> datetime:
        normalized = require_utc(value, boundary="canonical_ohlcv.open_time")
        assert normalized is not None
        return normalized

    @property
    def natural_key(self) -> tuple[str, str, str, str, datetime, str]:
        return (
            self.series_key.market_class,
            self.series_key.provider,
            self.series_key.symbol,
            self.series_key.timeframe,
            self.open_time,
            self.source,
        )


def authority_from_source(source: str) -> SourceAuthority:
    """Single source-label → authority classification (BO-B-DATA Part A).

    AUTHORITATIVE is granted ONLY through an explicit, declared real-data
    label — ``historical:real``. No other string acquires authority:

      - ``historical:real``   → AUTHORITATIVE (explicit declaration)
      - ``synthetic``         → SYNTHETIC   (BO-B-01 additive label)
      - ``seed:synthetic``    → SYNTHETIC
      - ``live:simulated``    → SIMULATED
      - ``sample:*`` / ``csv:*`` / ``test`` → UNKNOWN (legacy fixture
        convention, hardened by BO-B-DATA A2: no silent authority — real data
        ingested without an explicit label is quarantined from authoritative
        snapshots)
      - anything else         → UNKNOWN
    """
    if source == "seed:synthetic":
        return SourceAuthority.SYNTHETIC
    if source == "live:simulated":
        return SourceAuthority.SIMULATED
    if source == "synthetic":
        return SourceAuthority.SYNTHETIC
    if source == "historical:real":
        return SourceAuthority.AUTHORITATIVE
    return SourceAuthority.UNKNOWN


class MarketDataQueryPort(Protocol):
    async def list_series(self) -> Sequence[MarketSeriesKey]: ...

    async def get_candles(
        self,
        *,
        series_key: MarketSeriesKey,
        start: datetime | None = None,
        end: datetime | None = None,
        source_filter: str | None = None,
    ) -> Sequence[CanonicalOHLCVRecord]: ...

    async def get_source_metadata(self, *, source: str) -> SourceMetadata: ...

    async def get_series_metadata(
        self, *, series_key: MarketSeriesKey
    ) -> MarketSeriesMetadataRead | None: ...


class CandleMarketDataQueryAdapter:
    """Market data query adapter backed by existing candle table.

    This is the only ML dataset module allowed to import candle ORM details.
    """

    def __init__(self, session: AsyncSession, *, provider: str = "internal") -> None:
        self._session = session
        self._provider = provider

    async def list_series(self) -> Sequence[MarketSeriesKey]:
        stmt = (
            select(Candle.market_class, Candle.symbol, Candle.timeframe)
            .group_by(Candle.market_class, Candle.symbol, Candle.timeframe)
            .order_by(Candle.market_class, Candle.symbol, Candle.timeframe)
        )
        result = await self._session.execute(stmt)
        return [
            MarketSeriesKey(
                market_class=row.market_class,
                provider=self._provider,
                symbol=row.symbol,
                timeframe=row.timeframe,
            )
            for row in result.all()
        ]

    async def get_candles(
        self,
        *,
        series_key: MarketSeriesKey,
        start: datetime | None = None,
        end: datetime | None = None,
        source_filter: str | None = None,
    ) -> Sequence[CanonicalOHLCVRecord]:
        stmt = select(Candle).where(
            Candle.market_class == series_key.market_class,
            Candle.symbol == series_key.symbol,
            Candle.timeframe == series_key.timeframe,
        )
        if start is not None:
            stmt = stmt.where(Candle.open_time >= start)
        if end is not None:
            stmt = stmt.where(Candle.open_time <= end)
        if source_filter is not None:
            stmt = stmt.where(Candle.source == source_filter)
        stmt = stmt.order_by(Candle.open_time.asc(), Candle.id.asc())
        result = await self._session.execute(stmt)
        return [self._to_canonical(row, series_key=series_key) for row in result.scalars().all()]

    async def get_source_metadata(self, *, source: str) -> SourceMetadata:
        return SourceMetadata(
            source=source,
            authority=authority_from_source(source),
            provider=self._provider,
        )

    async def get_series_metadata(
        self, *, series_key: MarketSeriesKey
    ) -> MarketSeriesMetadataRead | None:
        stmt = select(MarketSeriesMetadata).where(
            MarketSeriesMetadata.market_class == series_key.market_class,
            MarketSeriesMetadata.provider == series_key.provider,
            MarketSeriesMetadata.symbol == series_key.symbol,
            MarketSeriesMetadata.timeframe == series_key.timeframe,
        )
        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        if row is None:
            return None
        return MarketSeriesMetadataRead(
            series_key=series_key,
            session_calendar=row.session_calendar,
            tick_size=row.tick_size,
            price_precision=row.price_precision,
            timezone_assumption=row.timezone_assumption,
            source_authority=SourceAuthority(row.source_authority),
            known_limitations=row.known_limitations,
            metadata_role=row.metadata_role,
        )

    def _to_canonical(
        self, candle: Candle, *, series_key: MarketSeriesKey
    ) -> CanonicalOHLCVRecord:
        source = candle.source or "unknown"
        return CanonicalOHLCVRecord(
            series_key=series_key,
            open_time=coerce_external_utc(
                candle.open_time,
                source="candle market data query adapter",
            ),
            open=candle.open,
            high=candle.high,
            low=candle.low,
            close=candle.close,
            volume=candle.volume,
            source=source,
            ingestion_run_id=None,
            authority_classification=self._authority_from_source(source),
            source_record_id=candle.id,
        )

    def _authority_from_source(self, source: str) -> SourceAuthority:
        return authority_from_source(source)
