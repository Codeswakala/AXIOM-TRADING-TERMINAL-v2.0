"""V2 Audit Event — append-only audit event table.

DB triggers enforce immutability (no UPDATE/DELETE).
Operator-scoped reads; admin read_all requires SAL-4 permission.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Index, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base, utc_now


class V2AuditEvent(Base):
    """V2 audit event record. Append-only; immutable after creation."""

    __tablename__ = "v2_audit_event"
    __table_args__ = (
        Index("ix_v2_audit_domain_created", "domain", "created_at"),
        Index("ix_v2_audit_actor", "actor_id"),
        Index("ix_v2_audit_correlation", "correlation_id"),
        Index("ix_v2_audit_mode", "mode"),
        Index("ix_v2_audit_operator", "operator_id"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    correlation_id: Mapped[str] = mapped_column(String(64), nullable=False)
    causation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    actor_id: Mapped[str] = mapped_column(String(128), nullable=False)
    actor_type: Mapped[str] = mapped_column(String(32), nullable=False)
    domain: Mapped[str] = mapped_column(String(64), nullable=False)
    action: Mapped[str] = mapped_column(String(128), nullable=False)
    resource_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    resource_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    details: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    classification: Mapped[str] = mapped_column(String(32), nullable=False, default="internal")
    operator_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
