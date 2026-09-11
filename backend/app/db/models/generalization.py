"""Generalization and drift monitoring models (W2-U10)."""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base, utc_now


class GeneralizationReport(Base):
    """Research-only trained-on-X / evaluated-on-Y generalization report."""

    __tablename__ = "generalization_reports"
    __table_args__ = (
        Index("ix_generalization_reports_experiment_id", "experiment_id"),
        Index("ix_generalization_reports_model_artifact_id", "model_artifact_id"),
        Index("ix_generalization_reports_report_hash", "report_hash"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    experiment_id: Mapped[str] = mapped_column(String(96), nullable=False)
    model_artifact_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("model_artifacts.id", ondelete="RESTRICT"), nullable=False
    )
    trained_on: Mapped[dict] = mapped_column(JSON, nullable=False)
    evaluated_on: Mapped[dict] = mapped_column(JSON, nullable=False)
    holdout_results: Mapped[dict] = mapped_column(JSON, nullable=False)
    operating_domain: Mapped[dict] = mapped_column(JSON, nullable=False)
    unsupported_domain_warnings: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    report_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    research_status: Mapped[str] = mapped_column(
        String(64), nullable=False, default="research_only"
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )


class DriftMonitoringRecord(Base):
    """Research-only drift monitoring design record.

    Drift records surface evidence; they never trigger retraining automatically.
    """

    __tablename__ = "drift_monitoring_records"
    __table_args__ = (
        Index("ix_drift_records_model_artifact_id", "model_artifact_id"),
        Index("ix_drift_records_drift_kind", "drift_kind"),
        Index("ix_drift_records_record_hash", "record_hash"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    model_artifact_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("model_artifacts.id", ondelete="RESTRICT"), nullable=False
    )
    drift_kind: Mapped[str] = mapped_column(String(64), nullable=False)
    window_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    window_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    signals: Mapped[dict] = mapped_column(JSON, nullable=False)
    drift_detected: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    auto_retrain_requested: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    retrain_triggered: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    governance_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    evidence_summary: Mapped[str] = mapped_column(Text, nullable=False)
    record_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    research_status: Mapped[str] = mapped_column(
        String(64), nullable=False, default="research_only"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
