"""Calibration report model (W2-U08)."""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base, utc_now


class CalibrationReport(Base):
    """Research-only calibration/probability-quality report."""

    __tablename__ = "calibration_reports"
    __table_args__ = (
        Index("ix_calibration_reports_experiment_id", "experiment_id"),
        Index("ix_calibration_reports_model_artifact_id", "model_artifact_id"),
        Index("ix_calibration_reports_validation_report_id", "validation_report_id"),
        Index("ix_calibration_reports_report_hash", "report_hash"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    experiment_id: Mapped[str] = mapped_column(String(96), nullable=False)
    model_artifact_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("model_artifacts.id", ondelete="RESTRICT"), nullable=False
    )
    validation_report_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("validation_reports.id", ondelete="RESTRICT"), nullable=False
    )
    brier_score: Mapped[str] = mapped_column(String(64), nullable=False)
    expected_calibration_error: Mapped[str] = mapped_column(String(64), nullable=False)
    bin_scheme: Mapped[dict] = mapped_column(JSON, nullable=False)
    bins: Mapped[list] = mapped_column(JSON, nullable=False)
    per_slice: Mapped[dict] = mapped_column(JSON, nullable=False)
    warnings: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    base_rate: Mapped[str] = mapped_column(String(64), nullable=False)
    base_rate_significance: Mapped[dict] = mapped_column(JSON, nullable=False)
    config: Mapped[dict] = mapped_column(JSON, nullable=False)
    report_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    research_status: Mapped[str] = mapped_column(
        String(64), nullable=False, default="research_only"
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
