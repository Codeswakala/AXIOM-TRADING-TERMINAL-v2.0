"""Model registry metadata placeholder — no binary blobs in foundation unit."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import DateTime, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base, TimestampMixin, utc_now


class ModelArtifact(Base, TimestampMixin):
    """Metadata for trained model artifacts (registry foundation).

    Artifact binaries/paths are referenced, not stored inline, to keep the
    relational store lean and replaceable with object storage later.
    """

    __tablename__ = "model_artifacts"
    __table_args__ = (
        Index("ix_model_artifacts_name_version", "name", "version"),
        Index("ix_model_artifacts_status", "status"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    version: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="registered",
        doc="registered | validated | approved | deployed | retired",
    )
    framework: Mapped[str | None] = mapped_column(String(64), nullable=True)
    feature_set_version: Mapped[str | None] = mapped_column(String(64), nullable=True)
    supported_markets: Mapped[list[Any] | None] = mapped_column(JSON, nullable=True)
    metrics: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    artifact_uri: Mapped[str | None] = mapped_column(String(512), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    experiment_id: Mapped[str | None] = mapped_column(String(96), nullable=True)
    dataset_snapshot_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    dataset_content_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    split_manifest_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    hyperparameters: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    artifact_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    research_status: Mapped[str | None] = mapped_column(String(64), nullable=True)
    statistical_report_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    calibration_report_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    economic_report_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    operating_domain: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    unsupported_domains: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    approval_history: Mapped[list[Any] | None] = mapped_column(JSON, nullable=True)
    rollback_version: Mapped[str | None] = mapped_column(String(64), nullable=True)
    advisory_status: Mapped[str | None] = mapped_column(String(64), nullable=True)
    advisory_approved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    advisory_approved_by: Mapped[str | None] = mapped_column(String(128), nullable=True)
    registered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )
