"""Short-lived WebSocket tickets (avoid JWT in query strings) — W0-U08."""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, utc_now


class WsTicket(Base):
    __tablename__ = "ws_tickets"
    __table_args__ = (UniqueConstraint("ticket", name="uq_ws_tickets_ticket"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    ticket: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    operator_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("operators.id", ondelete="CASCADE"),
        nullable=False,
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    used: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )
