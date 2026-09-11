"""BE-12A live-exec intent ledger (BO-V2-BE12A-001 §1.g; DR-4 floor).

One table this sub-band: v2_live_exec_intent — zero-UPDATE regime,
guard-pair triggers (migration 20260909_0053), surrogate uuid pk,
closed CHECKs. No submission/fill tables here (12B); no activation/
kill-switch tables here (12D).
"""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import JSON, CheckConstraint, DateTime, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.v2.temporal.validation import utc_now


class V2LiveExecIntent(Base):
    """Immutable live-exec intent record (12A: registration only)."""

    __tablename__ = "v2_live_exec_intent"
    __table_args__ = (
        Index("ix_v2_lxintent_created", "created_at"),
        Index("uq_v2_lxintent_idem", "idempotency_key", unique=True),
        CheckConstraint("record_state IN ('registered')",
                        name="ck_v2_lxintent_state"),
        CheckConstraint("data_class IN ('simulated')",
                        name="ck_v2_lxintent_data_class"),
        CheckConstraint("posture IN ('capability','practice','activation')",
                        name="ck_v2_lxintent_posture"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    idempotency_key: Mapped[str] = mapped_column(String(128), nullable=False)
    requested_basis_id: Mapped[str] = mapped_column(String(64), nullable=False)
    posture: Mapped[str] = mapped_column(String(16), nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    digest: Mapped[str] = mapped_column(String(64), nullable=False)
    record_state: Mapped[str] = mapped_column(String(16), nullable=False)
    step_up_ref: Mapped[str | None] = mapped_column(String(128), nullable=True)
    # regime block (standing shape)
    actor_id: Mapped[str] = mapped_column(String(128), nullable=False)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False)
