"""Persisted inert trade plan research notes (W5-U06)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base, utc_now


class TradePlanNoteRecord(Base):
    """Operator-authored inert trade plan research note.

    A trade plan note is not an order ticket. The schema deliberately contains
    no order, sizing, broker, account, position, stop/target, or execution
    payload columns.
    """

    __tablename__ = "trade_plan_notes"
    __table_args__ = (
        Index("ix_trade_plan_notes_created_at", "created_at"),
        Index("ix_trade_plan_notes_updated_at", "updated_at"),
        Index("ix_trade_plan_notes_operator", "operator_id"),
        Index("ix_trade_plan_notes_decision_status", "decision_status"),
        Index("ix_trade_plan_notes_correlation_id", "audit_correlation_id"),
    )

    plan_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False
    )
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    market_context: Mapped[str] = mapped_column(Text, nullable=False)
    hypothesis: Mapped[str] = mapped_column(Text, nullable=False)
    linked_signal_ids: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    linked_report_ids: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    scenario_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    risk_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    invalidating_conditions_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    decision_status: Mapped[str] = mapped_column(String(32), nullable=False)
    research_disclaimer: Mapped[str] = mapped_column(Text, nullable=False)
    research_status: Mapped[str] = mapped_column(String(64), nullable=False)
    audit_correlation_id: Mapped[str] = mapped_column(String(64), nullable=False)
