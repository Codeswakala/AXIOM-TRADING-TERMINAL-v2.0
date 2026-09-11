"""Feature definition and quality report models (W2-U03)."""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Float, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base, utc_now


class FeatureDefinition(Base):
    """Versioned, causal feature definition."""

    __tablename__ = "feature_definitions"
    __table_args__ = (
        UniqueConstraint(
            "feature_name",
            "feature_version",
            name="uq_feature_definition_name_version",
        ),
        Index("ix_feature_definitions_name", "feature_name"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    feature_name: Mapped[str] = mapped_column(String(128), nullable=False)
    feature_version: Mapped[str] = mapped_column(String(64), nullable=False)
    formula_spec: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    input_requirements: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    lookback_window: Mapped[int] = mapped_column(Integer, nullable=False)
    causal: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    market_compatibility_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )


class FeatureQualityReport(Base):
    """Feature quality report artifact metadata."""

    __tablename__ = "feature_quality_reports"
    __table_args__ = (
        Index("ix_feature_quality_reports_version", "feature_set_version"),
        Index("ix_feature_quality_reports_hash", "content_hash"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    feature_set_version: Mapped[str] = mapped_column(String(64), nullable=False)
    source_dataset_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    missing_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    drift_summary: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    leakage_checks: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    stationarity_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    cross_market_compatibility: Mapped[str | None] = mapped_column(Text, nullable=True)
    content_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
