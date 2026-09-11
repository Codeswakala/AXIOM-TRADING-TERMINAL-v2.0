"""Market series metadata for ML research access layer (W2-U02)."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from sqlalchemy import DateTime, Index, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base, utc_now


class MarketSeriesMetadata(Base):
    """Governance/evaluation metadata for a canonical market series.

    This metadata supports slicing, evaluation, and guardrails. It is not a
    learned predictive feature.
    """

    __tablename__ = "market_series_metadata"
    __table_args__ = (
        UniqueConstraint(
            "market_class",
            "provider",
            "symbol",
            "timeframe",
            name="uq_market_series_metadata_key",
        ),
        Index(
            "ix_market_series_metadata_key",
            "market_class",
            "provider",
            "symbol",
            "timeframe",
        ),
        Index("ix_market_series_metadata_market_provider", "market_class", "provider"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    market_class: Mapped[str] = mapped_column(String(32), nullable=False)
    provider: Mapped[str] = mapped_column(String(64), nullable=False)
    symbol: Mapped[str] = mapped_column(String(64), nullable=False)
    timeframe: Mapped[str] = mapped_column(String(16), nullable=False)
    session_calendar: Mapped[str | None] = mapped_column(String(128), nullable=True)
    tick_size: Mapped[Decimal | None] = mapped_column(Numeric(24, 10), nullable=True)
    price_precision: Mapped[int | None] = mapped_column(nullable=True)
    timezone_assumption: Mapped[str] = mapped_column(String(64), nullable=False, default="UTC")
    source_authority: Mapped[str] = mapped_column(String(32), nullable=False)
    known_limitations: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_role: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        default="governance_evaluation_only",
    )
    extra: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )
