"""Persisted inert manual research journal entries (W5-U07)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base, utc_now


class ManualTradeJournalEntryRecord(Base):
    """Operator-authored inert manual research journal entry.

    A journal entry is a research reflection, not a broker/account/execution
    record. The schema deliberately contains no account, broker, fill, order,
    sizing, position, execution, P&L, or realized-return columns.
    """

    __tablename__ = "manual_trade_journal_entries"
    __table_args__ = (
        Index("ix_manual_trade_journal_entries_created_at", "created_at"),
        Index("ix_manual_trade_journal_entries_operator", "operator_id"),
        Index("ix_manual_trade_journal_entries_linked_plan", "linked_plan_id"),
        Index("ix_manual_trade_journal_entries_correlation_id", "audit_correlation_id"),
    )

    journal_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    reflection_text: Mapped[str] = mapped_column(Text, nullable=False)
    linked_plan_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    linked_signal_ids: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    linked_report_ids: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    emotion_tags: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    process_tags: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    lesson_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    research_disclaimer: Mapped[str] = mapped_column(Text, nullable=False)
    research_status: Mapped[str] = mapped_column(String(64), nullable=False)
    audit_correlation_id: Mapped[str] = mapped_column(String(64), nullable=False)
