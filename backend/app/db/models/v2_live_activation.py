"""BE-12D activation-instrument table (BO-V2-BE12D-001 §1.b.1).

THE TABLE IS THE FORCE SWITCH: zero-row == L3
`activation_instrument_not_in_force`. At most one row may ever exist
(sole discriminator CHECK + unique index). **`data_class` CHECK =
single member 'live_marker'** — the coupon worlds' own 'simulated'
class is structurally BANNED: no test fixture can ever simulate force.
NO code path in this band INSERTs here (absence coupon-pinned); the
row, if it ever exists, arrives by a future operator register act
under a future build order.
"""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import CheckConstraint, DateTime, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.v2.temporal.validation import utc_now


class V2LiveActivationInstrument(Base):
    """The force row (zero-row state IS the lock)."""

    __tablename__ = "v2_live_activation_instrument"
    __table_args__ = (
        Index("uq_v2_lai_sole", "sole", unique=True),
        CheckConstraint("sole IN ('SOLE')", name="ck_v2_lai_sole"),
        CheckConstraint("version IN ('lai-1.0.0')",
                        name="ck_v2_lai_version"),
        CheckConstraint("data_class IN ('live_marker')",
                        name="ck_v2_lai_data_class"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    sole: Mapped[str] = mapped_column(String(4), nullable=False)
    version: Mapped[str] = mapped_column(String(16), nullable=False)
    template_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    funded_posture_ref: Mapped[str] = mapped_column(String(128), nullable=False)
    step_up_ref: Mapped[str] = mapped_column(String(128), nullable=False)
    operator_ref: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_ref: Mapped[str | None] = mapped_column(String(64), nullable=True)
    # regime block (standing shape)
    actor_id: Mapped[str] = mapped_column(String(128), nullable=False)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False)
