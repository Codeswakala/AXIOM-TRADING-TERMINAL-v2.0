"""Simulated execution analytics report persistence model (W6-U06)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base, utc_now


class SimulatedExecutionAnalyticsReport(Base):
    """Persisted analytics report over simulated execution research artifacts.

    This is a research artifact only. It is not a real performance statement,
    not a broker/account report, and not an execution instruction.
    """

    __tablename__ = "simulated_execution_analytics_reports"
    __table_args__ = (
        Index("ix_simulated_execution_analytics_reports_created_at", "created_at"),
        Index("ix_simulated_execution_analytics_reports_type", "analytics_type"),
        Index("ix_simulated_execution_analytics_reports_hash", "report_hash"),
        Index(
            "ix_simulated_execution_analytics_reports_correlation_id",
            "audit_correlation_id",
        ),
    )

    report_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    simulation_mode: Mapped[str] = mapped_column(String(32), nullable=False)
    analytics_type: Mapped[str] = mapped_column(String(96), nullable=False)
    included_scope: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    sample_count: Mapped[int] = mapped_column(Integer, nullable=False)
    metrics: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    uncertainty: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    limitations: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    economic_usefulness: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    report_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    source_artifact_ids: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    research_status: Mapped[str] = mapped_column(String(64), nullable=False)
    simulation_disclaimer: Mapped[str] = mapped_column(Text, nullable=False)
    audit_correlation_id: Mapped[str] = mapped_column(String(64), nullable=False)
