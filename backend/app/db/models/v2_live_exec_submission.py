"""BE-12B submission + fill-event ledgers (BO-V2-BE12B-001 §1.d; DR-4).

Two tables: v2_live_exec_submission, v2_live_exec_fill_event — both
zero-UPDATE regime, guard-pair triggers (migration 20260909_0054),
surrogate uuid pks, closed CHECK vocabularies. Submission states carry
the terminal-answer vocabulary + the quarantine state (BE-8 S2.4
preimage: a timeout is a state transition, never an exception).
Fill events are DE-DUPE anchored on fill-event identity (BE-9
election-derived law: fills are never double-attributed).
"""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import JSON, CheckConstraint, DateTime, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.v2.temporal.validation import utc_now


class V2LiveExecSubmission(Base):
    """Immutable practice-lane submission record."""

    __tablename__ = "v2_live_exec_submission"
    __table_args__ = (
        Index("ix_v2_lxsub_created", "created_at"),
        Index("uq_v2_lxsub_intent", "intent_id", unique=True),
        CheckConstraint(
            "terminal_state IN ('accepted','rejected','requote',"
            "'no_answer','quarantined_unknown')",
            name="ck_v2_lxsub_terminal_state"),
        CheckConstraint("lane IN ('practice')",
                        name="ck_v2_lxsub_lane"),
        CheckConstraint("data_class IN ('simulated')",
                        name="ck_v2_lxsub_data_class"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    intent_id: Mapped[str] = mapped_column(String(36), nullable=False)
    lane: Mapped[str] = mapped_column(String(16), nullable=False)
    terminal_state: Mapped[str] = mapped_column(String(24), nullable=False)
    server_ack_ref: Mapped[str | None] = mapped_column(String(64), nullable=True)
    raw_note: Mapped[str | None] = mapped_column(String(256), nullable=True)
    order_request: Mapped[dict] = mapped_column(JSON, nullable=False)
    digest: Mapped[str] = mapped_column(String(64), nullable=False)
    # regime block (standing shape)
    actor_id: Mapped[str] = mapped_column(String(128), nullable=False)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False)


class V2LiveExecFillEvent(Base):
    """Immutable fill-event record; identity-anchored dedupe at schema."""

    __tablename__ = "v2_live_exec_fill_event"
    __table_args__ = (
        Index("ix_v2_lxfill_created", "created_at"),
        Index("uq_v2_lxfill_identity", "fill_event_identity", unique=True),
        CheckConstraint("data_class IN ('simulated')",
                        name="ck_v2_lxfill_data_class"),
        CheckConstraint(
            "correlation_basis IN ('server_ack_ref','terminal_order_id')",
            name="ck_v2_lxfill_corr_basis"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    submission_id: Mapped[str] = mapped_column(String(36), nullable=False)
    fill_event_identity: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_basis: Mapped[str] = mapped_column(String(32), nullable=False)
    correlation_ref: Mapped[str] = mapped_column(String(64), nullable=False)
    fill_payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    # regime block (standing shape)
    actor_id: Mapped[str] = mapped_column(String(128), nullable=False)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False)
