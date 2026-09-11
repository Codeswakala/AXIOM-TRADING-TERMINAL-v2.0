"""Simulated execution research persistence models (W6-U02)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Float, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base, utc_now


class SimulatedExecutionRun(Base):
    """Persisted simulated execution research run.

    This is a research artifact only. It is never a live venue, account, order,
    capital, margin, or position record.
    """

    __tablename__ = "simulated_execution_runs"
    __table_args__ = (
        Index("ix_simulated_execution_runs_created_at", "created_at"),
        Index("ix_simulated_execution_runs_operator", "operator_id"),
        Index("ix_simulated_execution_runs_policy", "simulation_policy_version"),
        Index("ix_simulated_execution_runs_fill_model", "fill_model_name", "fill_model_version"),
        Index("ix_simulated_execution_runs_correlation_id", "audit_correlation_id"),
    )

    run_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    operator_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("operators.id", ondelete="RESTRICT"), nullable=False
    )
    simulation_mode: Mapped[str] = mapped_column(String(32), nullable=False)
    simulation_policy_version: Mapped[str] = mapped_column(String(96), nullable=False)
    input_artifact_ids: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    replay_scope: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    fill_model_name: Mapped[str] = mapped_column(String(96), nullable=False)
    fill_model_version: Mapped[str] = mapped_column(String(96), nullable=False)
    assumptions: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    limitations: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    research_status: Mapped[str] = mapped_column(String(64), nullable=False)
    simulation_disclaimer: Mapped[str] = mapped_column(Text, nullable=False)
    audit_correlation_id: Mapped[str] = mapped_column(String(64), nullable=False)


class SimulatedFillEvent(Base):
    """Persisted simulated fill-model output.

    This is a deterministic model output over replayed data, not a broker fill.
    """

    __tablename__ = "simulated_fill_events"
    __table_args__ = (
        Index("ix_simulated_fill_events_created_at", "created_at"),
        Index("ix_simulated_fill_events_run", "run_id"),
        Index("ix_simulated_fill_events_series", "market_class", "symbol", "timeframe"),
        Index("ix_simulated_fill_events_as_of", "as_of_time"),
        Index("ix_simulated_fill_events_fill_model", "fill_model_name", "fill_model_version"),
        Index("ix_simulated_fill_events_correlation_id", "audit_correlation_id"),
    )

    simulated_fill_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    run_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("simulated_execution_runs.run_id", ondelete="CASCADE"),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    simulation_mode: Mapped[str] = mapped_column(String(32), nullable=False)
    market_class: Mapped[str] = mapped_column(String(64), nullable=False)
    symbol: Mapped[str] = mapped_column(String(128), nullable=False)
    timeframe: Mapped[str] = mapped_column(String(32), nullable=False)
    as_of_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    simulated_research_direction: Mapped[str] = mapped_column(String(32), nullable=False)
    simulated_units: Mapped[float] = mapped_column(Float, nullable=False)
    requested_reference_price: Mapped[float] = mapped_column(Float, nullable=False)
    simulated_fill_price: Mapped[float] = mapped_column(Float, nullable=False)
    simulated_slippage_bps: Mapped[float] = mapped_column(Float, nullable=False)
    source_candle_ids: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    fill_model_name: Mapped[str] = mapped_column(String(96), nullable=False)
    fill_model_version: Mapped[str] = mapped_column(String(96), nullable=False)
    research_status: Mapped[str] = mapped_column(String(64), nullable=False)
    simulation_disclaimer: Mapped[str] = mapped_column(Text, nullable=False)
    audit_correlation_id: Mapped[str] = mapped_column(String(64), nullable=False)
