"""Statistical validation report model (W2-U07)."""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base, utc_now


class ValidationReport(Base):
    """Research-only statistical validation report with mandatory uncertainty."""

    __tablename__ = "validation_reports"
    __table_args__ = (
        Index("ix_validation_reports_experiment_id", "experiment_id"),
        Index("ix_validation_reports_model_artifact_id", "model_artifact_id"),
        Index("ix_validation_reports_report_hash", "report_hash"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    experiment_id: Mapped[str] = mapped_column(String(96), nullable=False)
    model_artifact_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("model_artifacts.id", ondelete="RESTRICT"), nullable=False
    )
    validation_kind: Mapped[str] = mapped_column(String(64), nullable=False)
    metrics: Mapped[dict] = mapped_column(JSON, nullable=False)
    uncertainty: Mapped[dict] = mapped_column(JSON, nullable=False)
    fold_results: Mapped[list] = mapped_column(JSON, nullable=False)
    effect_size: Mapped[dict] = mapped_column(JSON, nullable=False)
    significance: Mapped[dict] = mapped_column(JSON, nullable=False)
    config: Mapped[dict] = mapped_column(JSON, nullable=False)
    report_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    research_status: Mapped[str] = mapped_column(
        String(64), nullable=False, default="research_only"
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
