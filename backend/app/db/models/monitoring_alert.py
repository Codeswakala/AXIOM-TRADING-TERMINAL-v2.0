"""Monitoring, drift, and health alert persistence model (W3-U06)."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base, utc_now


class MonitoringAlert(Base):
    """Inert operator alert record.

    Alerts inform a human operator only. The schema intentionally contains no
    order, execution, model-mutation, or remediation payload.
    """

    __tablename__ = "monitoring_alerts"
    __table_args__ = (
        Index("ix_monitoring_alerts_created_at", "created_at"),
        Index("ix_monitoring_alerts_type", "alert_type"),
        Index("ix_monitoring_alerts_severity", "severity"),
        Index("ix_monitoring_alerts_subject", "subject_type", "subject_id"),
        Index("ix_monitoring_alerts_acknowledged", "acknowledged"),
        Index("ix_monitoring_alerts_correlation", "audit_correlation_id"),
    )

    alert_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    alert_type: Mapped[str] = mapped_column(String(96), nullable=False)
    severity: Mapped[str] = mapped_column(String(32), nullable=False)
    subject_type: Mapped[str] = mapped_column(String(64), nullable=False)
    subject_id: Mapped[str] = mapped_column(String(128), nullable=False)
    market_class: Mapped[str | None] = mapped_column(String(64), nullable=True)
    symbol: Mapped[str | None] = mapped_column(String(128), nullable=True)
    timeframe: Mapped[str | None] = mapped_column(String(32), nullable=True)
    model_artifact_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    signal_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    evidence: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    lineage: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    acknowledged: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    acknowledged_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    acknowledged_by: Mapped[str | None] = mapped_column(String(128), nullable=True)
    audit_correlation_id: Mapped[str] = mapped_column(String(64), nullable=False)
