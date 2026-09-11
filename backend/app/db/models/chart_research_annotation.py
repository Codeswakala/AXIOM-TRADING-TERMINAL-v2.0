"""Persisted inert chart research annotations (W5-U03)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base, utc_now


class ChartResearchAnnotation(Base):
    """Operator-authored inert chart research markup.

    Rows are research notes/drawings on chart context only. The schema
    deliberately contains no order, sizing, execution, account, position, or
    signal-emission payload columns.
    """

    __tablename__ = "chart_research_annotations"
    __table_args__ = (
        Index("ix_chart_research_annotations_created_at", "created_at"),
        Index("ix_chart_research_annotations_operator", "operator_id"),
        Index("ix_chart_research_annotations_artifact_type", "artifact_type"),
        Index("ix_chart_research_annotations_research_status", "research_status"),
        Index("ix_chart_research_annotations_correlation_id", "audit_correlation_id"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    artifact_type: Mapped[str] = mapped_column(String(96), nullable=False)
    chart_context: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    content: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    source_artifact_ids: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    provenance: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    uncertainty: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    disclaimer: Mapped[str] = mapped_column(Text, nullable=False)
    research_status: Mapped[str] = mapped_column(String(64), nullable=False)
    audit_correlation_id: Mapped[str] = mapped_column(String(64), nullable=False)
