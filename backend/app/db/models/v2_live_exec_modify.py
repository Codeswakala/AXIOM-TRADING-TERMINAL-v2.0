"""BE-12C modify-event ledger (BO-V2-BE12C-001 §1.b; append-only law).

One table: v2_live_exec_modify_event — zero-UPDATE regime, guard-pair
triggers (migration 20260909_0055), surrogate uuid pk, closed CHECK
vocabularies (verb; outcome; election; data-class). Parent submission/
fill rows are NEVER mutated by 12C (coupon-pinned byte-stable).
"""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import JSON, CheckConstraint, DateTime, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.v2.temporal.validation import utc_now


class V2LiveExecModifyEvent(Base):
    """Immutable cancel/modify act record (one row per act)."""

    __tablename__ = "v2_live_exec_modify_event"
    __table_args__ = (
        Index("ix_v2_lxmod_created", "created_at"),
        Index("uq_v2_lxmod_identity", "act_identity", unique=True),
        CheckConstraint("verb IN ('cancel','modify')",
                        name="ck_v2_lxmod_verb"),
        CheckConstraint(
            "outcome IN ('applied','refused_terminal','unknown_outcome',"
            "'unknown_escalate')",
            name="ck_v2_lxmod_outcome"),
        CheckConstraint(
            "operator_election IN ('standard','cancel_on_unknown')",
            name="ck_v2_lxmod_election"),
        CheckConstraint("data_class IN ('simulated')",
                        name="ck_v2_lxmod_data_class"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    submission_id: Mapped[str] = mapped_column(String(36), nullable=False)
    intent_id: Mapped[str] = mapped_column(String(36), nullable=False)
    verb: Mapped[str] = mapped_column(String(16), nullable=False)
    act_identity: Mapped[str] = mapped_column(String(128), nullable=False)
    request_payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    outcome: Mapped[str] = mapped_column(String(24), nullable=False)
    raw_note: Mapped[str | None] = mapped_column(String(256), nullable=True)
    correlation_ref: Mapped[str | None] = mapped_column(String(64), nullable=True)
    operator_election: Mapped[str] = mapped_column(String(24), nullable=False)
    # regime block (standing shape)
    actor_id: Mapped[str] = mapped_column(String(128), nullable=False)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False)
