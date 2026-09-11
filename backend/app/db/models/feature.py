"""Feature store record placeholder — versioned feature payload foundation."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import DateTime, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base, TimestampMixin, utc_now


class FeatureRecord(Base, TimestampMixin):
    """Placeholder feature matrix row for future ML feature store integration.

    Stores a versioned feature payload keyed by market context and as-of time.
    Does not implement feature engineering (Wave 2+).
    """

    __tablename__ = "feature_records"
    __table_args__ = (
        UniqueConstraint(
            "feature_set_version",
            "market_class",
            "symbol",
            "timeframe",
            "as_of",
            name="uq_feature_records_version_context_asof",
        ),
        Index("ix_feature_records_symbol_as_of", "symbol", "as_of"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    feature_set_version: Mapped[str] = mapped_column(String(64), nullable=False)
    market_class: Mapped[str] = mapped_column(String(32), nullable=False)
    provider: Mapped[str] = mapped_column(String(64), nullable=False, default="internal")
    symbol: Mapped[str] = mapped_column(String(64), nullable=False)
    timeframe: Mapped[str] = mapped_column(String(16), nullable=False)
    as_of: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    features: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    quality_score: Mapped[str | None] = mapped_column(String(32), nullable=True)
    source: Mapped[str | None] = mapped_column(String(64), nullable=True)
    source_dataset_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )
