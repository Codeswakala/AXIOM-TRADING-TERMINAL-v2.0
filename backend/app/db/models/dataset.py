"""ML dataset governance models (W2-U01)."""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base, utc_now


class DatasetSnapshot(Base):
    """Immutable/versioned ML dataset snapshot metadata."""

    __tablename__ = "dataset_snapshots"
    __table_args__ = (
        UniqueConstraint("dataset_id", "version", name="uq_dataset_snapshots_dataset_version"),
        Index("ix_dataset_snapshots_status", "status"),
        Index("ix_dataset_snapshots_dataset_id", "dataset_id"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    dataset_id: Mapped[str] = mapped_column(String(96), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    # 07_ML_SPEC mandatory dataset governance fields.
    market: Mapped[str] = mapped_column(String(64), nullable=False)
    timeframe: Mapped[str] = mapped_column(String(32), nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    source: Mapped[str] = mapped_column(String(128), nullable=False)
    feature_version: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    quality_score: Mapped[str] = mapped_column(String(32), nullable=False)

    status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="draft",
        doc="draft | frozen | quarantined | deprecated",
    )
    content_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    market_scope: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    source_policy: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    frozen_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_by: Mapped[str | None] = mapped_column(String(128), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class DatasetSeriesMember(Base):
    """Series-level membership summary for a dataset snapshot."""

    __tablename__ = "dataset_series_members"
    __table_args__ = (
        Index("ix_dataset_series_snapshot", "dataset_snapshot_id"),
        Index("ix_dataset_series_key", "market_class", "provider", "symbol", "timeframe"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    dataset_snapshot_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("dataset_snapshots.id", ondelete="CASCADE"), nullable=False
    )
    market_class: Mapped[str] = mapped_column(String(32), nullable=False)
    provider: Mapped[str] = mapped_column(String(64), nullable=False, default="internal")
    symbol: Mapped[str] = mapped_column(String(64), nullable=False)
    timeframe: Mapped[str] = mapped_column(String(16), nullable=False)
    source: Mapped[str] = mapped_column(String(64), nullable=False)
    authoritative: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    record_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    first_open_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    last_open_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    series_hash: Mapped[str] = mapped_column(String(128), nullable=False)


class DatasetLineageRecord(Base):
    """Trace source candle membership into dataset snapshots."""

    __tablename__ = "dataset_lineage_records"
    __table_args__ = (
        Index("ix_dataset_lineage_snapshot", "dataset_snapshot_id"),
        Index("ix_dataset_lineage_source", "source_candle_id"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    dataset_snapshot_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("dataset_snapshots.id", ondelete="CASCADE"), nullable=False
    )
    source_candle_id: Mapped[str] = mapped_column(String(36), nullable=False)
    normalized_record_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    feature_record_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    lineage_stage: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )


class DatasetQuarantineRecord(Base):
    """Quarantine record for data-integrity guard refusals."""

    __tablename__ = "dataset_quarantine_records"
    __table_args__ = (
        Index("ix_dataset_quarantine_reason", "reason_code"),
        Index("ix_dataset_quarantine_series", "market_class", "provider", "symbol", "timeframe"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    dataset_snapshot_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("dataset_snapshots.id", ondelete="SET NULL"), nullable=True
    )
    source_record_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    market_class: Mapped[str] = mapped_column(String(32), nullable=False)
    provider: Mapped[str] = mapped_column(String(64), nullable=False, default="internal")
    symbol: Mapped[str] = mapped_column(String(64), nullable=False)
    timeframe: Mapped[str] = mapped_column(String(16), nullable=False)
    open_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    source: Mapped[str] = mapped_column(String(64), nullable=False)
    reason_code: Mapped[str] = mapped_column(String(64), nullable=False)
    detected_stage: Mapped[str] = mapped_column(String(64), nullable=False)
    detail: Mapped[str] = mapped_column(Text, nullable=False)
    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
