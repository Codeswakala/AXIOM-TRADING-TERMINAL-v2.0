"""Simulated paper research ledger persistence model (W6-U03)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Float, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base, utc_now


class SimulatedPaperLedgerEntry(Base):
    """Persisted simulated paper research ledger entry.

    This is a simulated research estimate over simulated fills only. It is not a
    broker/account/position ledger and does not represent real P&L.
    """

    __tablename__ = "simulated_paper_ledger_entries"
    __table_args__ = (
        Index("ix_simulated_paper_ledger_entries_created_at", "created_at"),
        Index("ix_simulated_paper_ledger_entries_operator", "operator_id"),
        Index("ix_simulated_paper_ledger_entries_run", "run_id"),
        Index("ix_simulated_paper_ledger_entries_fill", "simulated_fill_id"),
        Index("ix_simulated_paper_ledger_entries_correlation_id", "audit_correlation_id"),
    )

    ledger_entry_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    simulation_mode: Mapped[str] = mapped_column(String(32), nullable=False)
    run_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("simulated_execution_runs.run_id", ondelete="RESTRICT"),
        nullable=False,
    )
    simulated_fill_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("simulated_fill_events.simulated_fill_id", ondelete="RESTRICT"),
        nullable=False,
    )
    operator_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("operators.id", ondelete="RESTRICT"), nullable=False
    )
    ledger_event_type: Mapped[str] = mapped_column(String(64), nullable=False)
    simulated_research_direction: Mapped[str] = mapped_column(String(32), nullable=False)
    simulated_units: Mapped[float] = mapped_column(Float, nullable=False)
    simulated_entry_value: Mapped[float] = mapped_column(Float, nullable=False)
    simulated_exit_value: Mapped[float] = mapped_column(Float, nullable=False)
    simulated_return_estimate: Mapped[float] = mapped_column(Float, nullable=False)
    uncertainty: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    limitations: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    research_status: Mapped[str] = mapped_column(String(64), nullable=False)
    simulation_disclaimer: Mapped[str] = mapped_column(Text, nullable=False)
    audit_correlation_id: Mapped[str] = mapped_column(String(64), nullable=False)
