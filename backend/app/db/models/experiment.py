"""Experiment registry models (W2-U05)."""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base, TimestampMixin


class Experiment(Base, TimestampMixin):
    """Immutable/versioned pre-registered ML research experiment plan."""

    __tablename__ = "experiments"
    __table_args__ = (
        UniqueConstraint("experiment_id", "version", name="uq_experiments_experiment_version"),
        Index("ix_experiments_status", "status"),
        Index("ix_experiments_experiment_id", "experiment_id"),
        Index("ix_experiments_plan_hash", "plan_hash"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    experiment_id: Mapped[str] = mapped_column(String(96), nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="draft",
        doc="draft | pre_registered | approved | superseded",
    )

    # 07_ML_SPEC Experiment Governance mandatory fields.
    purpose: Mapped[str] = mapped_column(Text, nullable=False)
    hypothesis: Mapped[str] = mapped_column(Text, nullable=False)
    dataset_snapshot_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("dataset_snapshots.id", ondelete="RESTRICT"), nullable=False
    )
    dataset_content_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    split_manifest_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("dataset_split_manifests.id", ondelete="RESTRICT"), nullable=False
    )
    split_manifest_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    feature_set_version: Mapped[str] = mapped_column(String(64), nullable=False)
    model_family: Mapped[str] = mapped_column(String(128), nullable=False)
    model_spec: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    evaluation_plan: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    approval_timestamp: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    approver: Mapped[str | None] = mapped_column(String(128), nullable=True)

    plan_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    previous_experiment_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
