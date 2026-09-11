"""Execution research experiment pre-registration model (W6-U05)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base, utc_now


class ExecutionResearchExperiment(Base):
    """Immutable pre-registered simulated execution research experiment.

    This record declares a replay scope before results and stores only simulated,
    research-only outputs. It is not a live feed, broker, order, account, or P&L
    record.
    """

    __tablename__ = "execution_research_experiments"
    __table_args__ = (
        Index("ix_execution_research_experiments_created_at", "created_at"),
        Index("ix_execution_research_experiments_operator", "operator_id"),
        Index("ix_execution_research_experiments_plan_hash", "plan_hash"),
        Index("ix_execution_research_experiments_as_of_time", "as_of_time"),
        Index("ix_execution_research_experiments_correlation_id", "audit_correlation_id"),
    )

    experiment_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    simulation_mode: Mapped[str] = mapped_column(String(32), nullable=False)
    operator_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("operators.id", ondelete="RESTRICT"), nullable=False
    )
    experiment_title: Mapped[str] = mapped_column(String(200), nullable=False)
    pre_registration_plan: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    plan_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    as_of_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    as_of_window: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    replay_input_lineage: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    included_scope_summary: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    uncertainty: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    limitations: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    research_status: Mapped[str] = mapped_column(String(64), nullable=False)
    simulation_disclaimer: Mapped[str] = mapped_column(Text, nullable=False)
    audit_correlation_id: Mapped[str] = mapped_column(String(64), nullable=False)
