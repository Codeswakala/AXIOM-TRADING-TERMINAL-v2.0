"""BE-12E incident record (BO-V2-BE12E-001 §1.d.1; DR-1 shape).

Zero-UPDATE regime, guard pair; THE single sanctioned close = the
engine's valve dance. Severity/status CHECKs closed; data_class CHECK
single member 'evidence'; instruments_pinned non-empty enforced at the
app edge (typed `incident_instruments_absent`); closed_at/closed_by
NULL iff open.
"""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import JSON, CheckConstraint, DateTime, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.v2.temporal.validation import utc_now


class V2LiveExecIncident(Base):
    """Operator-opened incident evidence record."""

    __tablename__ = "v2_live_exec_incident"
    __table_args__ = (
        Index("ix_v2_lxinc_created", "created_at"),
        CheckConstraint(
            "severity IN ('SEV-1','SEV-2','SEV-3','SEV-4')",
            name="ck_v2_lxinc_severity"),
        CheckConstraint("status IN ('open','closed')",
                        name="ck_v2_lxinc_status"),
        CheckConstraint("data_class IN ('evidence')",
                        name="ck_v2_lxinc_data_class"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    opened_by: Mapped[str] = mapped_column(String(128), nullable=False)
    severity: Mapped[str] = mapped_column(String(8), nullable=False)
    instruments_pinned: Mapped[list] = mapped_column(JSON, nullable=False)
    recovery_path: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(8), nullable=False)
    closed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True)
    closed_by: Mapped[str | None] = mapped_column(String(128), nullable=True)
    digest: Mapped[str] = mapped_column(String(64), nullable=False)
    step_up_ref: Mapped[str | None] = mapped_column(String(128), nullable=True)
    # regime block (standing shape)
    actor_id: Mapped[str] = mapped_column(String(128), nullable=False)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False)
