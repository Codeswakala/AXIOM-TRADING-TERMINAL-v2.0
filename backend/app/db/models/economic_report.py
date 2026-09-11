"""Economic validation report model (W2-U09)."""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base, utc_now


class EconomicReport(Base):
    """Research-only economic validation report for hypothetical P&L after costs."""

    __tablename__ = "economic_reports"
    __table_args__ = (
        Index("ix_economic_reports_experiment_id", "experiment_id"),
        Index("ix_economic_reports_model_artifact_id", "model_artifact_id"),
        Index("ix_economic_reports_report_hash", "report_hash"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    experiment_id: Mapped[str] = mapped_column(String(96), nullable=False)
    model_artifact_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("model_artifacts.id", ondelete="RESTRICT"), nullable=False
    )
    validation_report_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("validation_reports.id", ondelete="RESTRICT"), nullable=True
    )
    calibration_report_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("calibration_reports.id", ondelete="RESTRICT"), nullable=True
    )
    cost_model: Mapped[dict] = mapped_column(JSON, nullable=False)
    scenario_results: Mapped[dict] = mapped_column(JSON, nullable=False)
    statistical_conclusion: Mapped[dict] = mapped_column(JSON, nullable=False)
    economic_conclusion: Mapped[dict] = mapped_column(JSON, nullable=False)
    sensitivity_summary: Mapped[dict] = mapped_column(JSON, nullable=False)
    per_slice: Mapped[dict] = mapped_column(JSON, nullable=False)
    report_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    research_status: Mapped[str] = mapped_column(
        String(64), nullable=False, default="research_only"
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
