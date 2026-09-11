"""OHLCV candle persistence model — multi-market ready foundation."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import uuid4

from sqlalchemy import DateTime, Index, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base, TimestampMixin, utc_now


class Candle(Base, TimestampMixin):
    """Basic OHLCV bar for any market/instrument/timeframe.

    Designed for future multi-market ingestion without schema redesign:
    market_class + symbol + timeframe + open_time form the natural key.
    """

    __tablename__ = "candles"
    __table_args__ = (
        UniqueConstraint(
            "market_class",
            "symbol",
            "timeframe",
            "open_time",
            name="uq_candles_market_symbol_tf_time",
        ),
        Index("ix_candles_symbol_timeframe_open_time", "symbol", "timeframe", "open_time"),
        Index("ix_candles_market_class_symbol", "market_class", "symbol"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    market_class: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        doc="forex | crypto | index | equity | commodity | metal | future | etf | synthetic",
    )
    symbol: Mapped[str] = mapped_column(String(64), nullable=False)
    timeframe: Mapped[str] = mapped_column(String(16), nullable=False, doc="e.g. M1, M5, H1, D1")
    open_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    open: Mapped[Decimal] = mapped_column(Numeric(24, 10), nullable=False)
    high: Mapped[Decimal] = mapped_column(Numeric(24, 10), nullable=False)
    low: Mapped[Decimal] = mapped_column(Numeric(24, 10), nullable=False)
    close: Mapped[Decimal] = mapped_column(Numeric(24, 10), nullable=False)
    volume: Mapped[Decimal | None] = mapped_column(Numeric(24, 10), nullable=True)
    source: Mapped[str | None] = mapped_column(String(64), nullable=True)
    extra: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    ingested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )
