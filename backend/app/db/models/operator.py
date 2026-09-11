"""Operator identity model — foundation auth (W0-U04)."""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class Operator(Base, TimestampMixin):
    """Minimal operator account for institutional terminal access."""

    __tablename__ = "operators"
    __table_args__ = (UniqueConstraint("username", name="uq_operators_username"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    username: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="operator",
        doc="operator | admin (coarse roles only; full RBAC deferred)",
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    display_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
