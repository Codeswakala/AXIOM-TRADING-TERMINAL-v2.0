"""V2 BE-5 signal tables (BO-V2-BE-5-001 T-6; migration 0045).

Structural vs predictive as separately-typed families; withheld/expired/
refused as permanent typed states. Rows fully immutable (DB guards);
state progression = appended state events.
"""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import JSON, CheckConstraint, DateTime, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.v2.temporal.validation import utc_now


class V2SignalRecord(Base):
    """One immutable signal record (emitted OR permanently typed non-emission)."""

    __tablename__ = "v2_signal_record"
    __table_args__ = (
        Index("ix_v2_signal_instrument", "instrument_id"),
        Index("ix_v2_signal_family_state", "family", "state"),
        CheckConstraint("family IN ('structural','predictive')",
                        name="ck_v2_signal_family"),
        CheckConstraint(
            "state IN ('emitted','withheld','expired','refused')",
            name="ck_v2_signal_state"),
        CheckConstraint(
            "data_class IN ('synthetic','simulated','historical_real','live',"
            "'stale_cached','unavailable')",
            name="ck_v2_signal_data_class"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    family: Mapped[str] = mapped_column(String(16), nullable=False)
    signal_type: Mapped[str] = mapped_column(String(64), nullable=False)
    instrument_id: Mapped[str] = mapped_column(String(96), nullable=False)
    timeframe: Mapped[str] = mapped_column(String(16), nullable=False)
    state: Mapped[str] = mapped_column(String(16), nullable=False)
    state_reason: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    uncertainty: Mapped[dict] = mapped_column(JSON, nullable=False)
    limitations: Mapped[dict] = mapped_column(JSON, nullable=False)
    source_family_refs: Mapped[dict] = mapped_column(JSON, nullable=False)
    governance_record_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    as_of: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )


class V2SignalStateEvent(Base):
    """Append-only signal state transitions (immutable — DB guards)."""

    __tablename__ = "v2_signal_state_event"
    __table_args__ = (
        Index("ix_v2_sigev_signal", "signal_record_id"),
        CheckConstraint(
            "event_type IN ('emitted','withheld','refused','expired')",
            name="ck_v2_sigev_type"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    signal_record_id: Mapped[str] = mapped_column(String(36), nullable=False)
    event_type: Mapped[str] = mapped_column(String(16), nullable=False)
    from_state: Mapped[str] = mapped_column(String(16), nullable=False)
    to_state: Mapped[str] = mapped_column(String(16), nullable=False)
    reason: Mapped[dict] = mapped_column(JSON, nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    actor_id: Mapped[str] = mapped_column(String(128), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
