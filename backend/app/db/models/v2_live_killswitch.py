"""BE-12D kill-switch table (BO-V2-BE12D-001 §1.c.1).

Singleton sole-row; closed status CHECK armed/pulled/cleared;
`data_class` CHECK = single member 'evidence' (the switch is an
authority/evidence artifact, never trade data — 'simulated' BANNED).
Guard pair prohibits UPDATE/DELETE; the ONLY legal transitions run
through the engine's sanctioned valve (guard-dance).
"""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import CheckConstraint, DateTime, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.v2.temporal.validation import utc_now


class V2LiveKillSwitch(Base):
    """The sole-row switch (persisted, never state-in-memory)."""

    __tablename__ = "v2_live_kill_switch"
    __table_args__ = (
        Index("uq_v2_lks_sole", "sole", unique=True),
        CheckConstraint("sole IN ('SOLE')", name="ck_v2_lks_sole"),
        CheckConstraint("status IN ('armed','pulled','cleared')",
                        name="ck_v2_lks_status"),
        CheckConstraint("data_class IN ('evidence')",
                        name="ck_v2_lks_data_class"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    sole: Mapped[str] = mapped_column(String(4), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    step_up_ref: Mapped[str] = mapped_column(String(128), nullable=False)
    # regime block (standing shape)
    actor_id: Mapped[str] = mapped_column(String(128), nullable=False)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False)
