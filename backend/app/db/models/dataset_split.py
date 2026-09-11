"""Dataset split manifest model (W2-U04)."""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base, utc_now


class DatasetSplitManifest(Base):
    """Deterministic temporal split manifest for a frozen dataset snapshot."""

    __tablename__ = "dataset_split_manifests"
    __table_args__ = (
        UniqueConstraint(
            "dataset_snapshot_id",
            "split_id",
            name="uq_dataset_split_snapshot_split_id",
        ),
        Index("ix_dataset_split_snapshot", "dataset_snapshot_id"),
        Index("ix_dataset_split_hash", "split_hash"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    dataset_snapshot_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("dataset_snapshots.id", ondelete="CASCADE"), nullable=False
    )
    split_id: Mapped[str] = mapped_column(String(96), nullable=False)
    split_strategy: Mapped[str] = mapped_column(String(32), nullable=False, default="temporal")
    label_horizon_bars: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    embargo_bars: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    train_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    train_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    validation_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    validation_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    test_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    test_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    train_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    validation_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    test_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    split_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    manifest: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    quality_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
