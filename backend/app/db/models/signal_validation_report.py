"""Professional signal validation report model (W4-U06)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base, utc_now


class SignalValidationReport(Base):
    """Persisted research report validating advisory-signal records.

    The report intentionally excludes raw score and contains no order/execution
    or signal-emission payload.
    """

    __tablename__ = "signal_validation_reports"
    __table_args__ = (
        Index("ix_signal_validation_reports_created_at", "created_at"),
        Index("ix_signal_validation_reports_scope", "scope_start", "scope_end"),
        Index("ix_signal_validation_reports_report_hash", "report_hash"),
        Index("ix_signal_validation_reports_correlation_id", "audit_correlation_id"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    artifact_type: Mapped[str] = mapped_column(String(96), nullable=False)
    method_version: Mapped[str] = mapped_column(String(96), nullable=False)
    scope_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    scope_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    sample_count: Mapped[int] = mapped_column(Integer, nullable=False)
    metrics: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    uncertainty: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    validation_scope: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    outcome_data_status: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    economic_usefulness: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    config: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    input_lineage: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    source_signal_ids: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    market_scope: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    results: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    limitations: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    report_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    research_status: Mapped[str] = mapped_column(
        String(64), nullable=False, default="research_only"
    )
    created_by: Mapped[str] = mapped_column(String(128), nullable=False)
    audit_correlation_id: Mapped[str] = mapped_column(String(64), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
