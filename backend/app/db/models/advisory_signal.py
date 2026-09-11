"""Advisory signal persistence model (W3-U02)."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import DateTime, Float, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base, utc_now


class AdvisorySignal(Base):
    """Inert, audited advisory signal record.

    A signal record is research/advisory evidence only. It intentionally contains
    no executable order payload and no broker dispatch metadata.
    """

    __tablename__ = "advisory_signals"
    __table_args__ = (
        Index("ix_advisory_signals_created_at", "created_at"),
        Index("ix_advisory_signals_state", "signal_state"),
        Index("ix_advisory_signals_model_artifact", "model_artifact_id"),
        Index("ix_advisory_signals_market_symbol", "market_class", "symbol", "timeframe"),
        Index("ix_advisory_signals_correlation", "audit_correlation_id"),
    )

    signal_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    as_of_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    market_class: Mapped[str] = mapped_column(String(64), nullable=False)
    provider: Mapped[str] = mapped_column(String(128), nullable=False)
    symbol: Mapped[str] = mapped_column(String(128), nullable=False)
    timeframe: Mapped[str] = mapped_column(String(32), nullable=False)
    model_artifact_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("model_artifacts.id", ondelete="RESTRICT"), nullable=False
    )
    model_version: Mapped[str] = mapped_column(String(64), nullable=False)
    feature_set_version: Mapped[str] = mapped_column(String(64), nullable=False)
    experiment_id: Mapped[str] = mapped_column(String(96), nullable=False)
    statistical_report_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("validation_reports.id", ondelete="RESTRICT"), nullable=True
    )
    calibration_report_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("calibration_reports.id", ondelete="RESTRICT"), nullable=True
    )
    economic_report_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("economic_reports.id", ondelete="RESTRICT"), nullable=True
    )
    generalization_report_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("generalization_reports.id", ondelete="RESTRICT"), nullable=True
    )
    inference_input_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    raw_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    calibrated_confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    input_staleness_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    signal_validity_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    freshness_status: Mapped[str | None] = mapped_column(String(64), nullable=True)
    signal_direction: Mapped[str] = mapped_column(String(64), nullable=False)
    signal_state: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        doc="emitted | withheld | warning | expired | superseded",
    )
    state_reason: Mapped[str] = mapped_column(String(256), nullable=False)
    eligibility_reasons: Mapped[list[Any]] = mapped_column(JSON, nullable=False, default=list)
    operating_domain_status: Mapped[str] = mapped_column(String(64), nullable=False)
    calibration_status: Mapped[str] = mapped_column(String(128), nullable=False)
    economic_verdict: Mapped[str] = mapped_column(String(128), nullable=False)
    risk_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    rationale: Mapped[str] = mapped_column(Text, nullable=False)
    explainability_summary: Mapped[dict[str, Any]] = mapped_column(
        JSON, nullable=False, default=dict
    )
    state_transition_history: Mapped[list[Any]] = mapped_column(JSON, nullable=False, default=list)
    audit_correlation_id: Mapped[str] = mapped_column(String(64), nullable=False)
