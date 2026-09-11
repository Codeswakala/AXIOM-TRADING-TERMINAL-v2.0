"""BE-12E reconciliation evidence ledger (BO-V2-BE12E-001 §1.c.5).

Zero-UPDATE regime, guard pair, NO VALVE — a report never transitions;
correction = a new run. Outcome CHECK closed (clean/parity_break);
data_class CHECK single member 'evidence'; mode = REQUEST WORLD per the
§1.a.4 forward law (threaded from the chassis, never a literal).
"""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import JSON, CheckConstraint, DateTime, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.v2.temporal.validation import utc_now


class V2LiveExecReconciliation(Base):
    """One immutable evidence row per operator-initiated run (C-2 law)."""

    __tablename__ = "v2_live_exec_reconciliation"
    __table_args__ = (
        Index("ix_v2_lxrecon_created", "created_at"),
        CheckConstraint("outcome IN ('clean','parity_break')",
                        name="ck_v2_lxrecon_outcome"),
        CheckConstraint("data_class IN ('evidence')",
                        name="ck_v2_lxrecon_data_class"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    scope: Mapped[dict] = mapped_column(JSON, nullable=False)
    outcome: Mapped[str] = mapped_column(String(16), nullable=False)
    drift_facts: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # NULL iff clean
    digest: Mapped[str] = mapped_column(String(64), nullable=False)
    # regime block (standing shape)
    actor_id: Mapped[str] = mapped_column(String(128), nullable=False)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False)
