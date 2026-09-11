"""Immutable-oriented audit event store for governance traceability."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import DateTime, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base, utc_now


class AuditEvent(Base):
    """Governance audit log entry.

    Updates are discouraged at the service layer; append-only usage is preferred.
    """

    __tablename__ = "audit_events"
    __table_args__ = (
        Index("ix_audit_events_category_created", "category", "created_at"),
        Index("ix_audit_events_actor", "actor"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    category: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        doc="SYSTEM | API | DATABASE | ML | MARKET | BROKER | SECURITY | GOVERNANCE | AUDIT",
    )
    action: Mapped[str] = mapped_column(String(128), nullable=False)
    actor: Mapped[str] = mapped_column(String(128), nullable=False, default="system")
    resource_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    resource_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    details: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )


class AuditWriteFailureRecord(Base):
    """BO-B-AUDIT — durable marker for an audit append that could not land.

    When `AuditRepository.append` exhausts its retry budget, it persists one
    of these rows (via a short-lived dedicated session) so the loss is a
    queryable record — never silent. No foreign keys by design: the marker
    must be writable even when the referenced business rows no longer exist.
    """

    __tablename__ = "audit_write_failure_records"
    __table_args__ = (
        Index("ix_audit_write_failures_created", "created_at"),
        Index("ix_audit_write_failures_category_action", "category", "action"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    category: Mapped[str] = mapped_column(String(64), nullable=False)
    action: Mapped[str] = mapped_column(String(96), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    actor: Mapped[str] = mapped_column(String(128), nullable=False, default="system")
    resource_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    resource_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    details: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    failure_reason: Mapped[str] = mapped_column(Text, nullable=False)
    attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )
