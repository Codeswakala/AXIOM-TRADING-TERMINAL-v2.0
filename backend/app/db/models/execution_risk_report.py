"""Execution risk research report persistence model (W6-U04)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base, utc_now


class ExecutionRiskResearchReport(Base):
    """Persisted simulated execution-risk research report.

    The report is advisory research only. It contains structured risk metrics,
    uncertainty, limitations, and an economic-usefulness statement. It contains
    no order, sizing directive, account, broker, margin, capital, position, or
    live execution payload.
    """

    __tablename__ = "execution_risk_research_reports"
    __table_args__ = (
        Index("ix_execution_risk_reports_created_at", "created_at"),
        Index("ix_execution_risk_reports_correlation_id", "audit_correlation_id"),
        Index("ix_execution_risk_reports_simulation_mode", "simulation_mode"),
    )

    report_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    simulation_mode: Mapped[str] = mapped_column(String(32), nullable=False)
    input_artifact_ids: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    simulated_request_summary: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    risk_metrics: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    uncertainty: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    limitations: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    economic_usefulness: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    research_status: Mapped[str] = mapped_column(String(64), nullable=False)
    simulation_disclaimer: Mapped[str] = mapped_column(Text, nullable=False)
    audit_correlation_id: Mapped[str] = mapped_column(String(64), nullable=False)
