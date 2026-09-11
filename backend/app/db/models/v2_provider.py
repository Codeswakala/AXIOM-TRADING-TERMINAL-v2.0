"""V2 BE-3 P1 provider models (BO-V2-BE-3-P1-001).

`v2_md_provider` — read-only seeded registry (no application write path).
`v2_md_provider_status_history` — append-only ladder history; P1 contains
only the seeded genesis row; DB triggers prevent UPDATE/DELETE; no
application write path exists (no transition writer in P1).
"""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import JSON, Boolean, CheckConstraint, DateTime, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.v2.temporal.validation import utc_now

_STATUSES = (
    "'architecture_candidate','contract_tested','integrated',"
    "'authorized','production_certified'"
)


class V2MdProvider(Base):
    """Provider registry — read-only seeded AND database-immutable in P1.

    DEL-001: UPDATE/DELETE are refused by DB triggers on both dialects;
    status/entitlement/persistence fields cannot change without a future
    separately authorized transition design shipping its own governed
    migration.
    """

    __tablename__ = "v2_md_provider"
    __table_args__ = (
        UniqueConstraint("provider_id", name="uq_v2_md_provider_id"),
        CheckConstraint(f"source_status IN ({_STATUSES})", name="ck_v2_md_provider_status"),
        CheckConstraint(
            "entitlement_status IN ('unverified','verified','expired','revoked')",
            name="ck_v2_md_provider_entitlement",
        ),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    provider_id: Mapped[str] = mapped_column(String(64), nullable=False)
    display_name: Mapped[str] = mapped_column(String(128), nullable=False)
    markets: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    entitlement: Mapped[dict[str, Any] | None] = mapped_column(
        JSON, nullable=True, doc="Verified entitlement data only; P1: None (unverified)"
    )
    entitlement_status: Mapped[str] = mapped_column(
        String(16), nullable=False, default="unverified"
    )
    persistence_permitted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    source_status: Mapped[str] = mapped_column(
        String(32), nullable=False, default="architecture_candidate"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )


class V2MdProviderStatusHistory(Base):
    """Append-only status-ladder history. P1: genesis row only."""

    __tablename__ = "v2_md_provider_status_history"
    __table_args__ = (
        CheckConstraint(f"to_status IN ({_STATUSES})", name="ck_v2_md_provider_hist_to"),
        Index("ix_v2_md_provider_hist_provider", "provider_id", "created_at"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    provider_id: Mapped[str] = mapped_column(String(64), nullable=False)
    from_status: Mapped[str | None] = mapped_column(String(32), nullable=True)
    to_status: Mapped[str] = mapped_column(String(32), nullable=False)
    authority_ref: Mapped[str] = mapped_column(
        String(128), nullable=False, doc="Build Order / determination / Operator decision id"
    )
    evidence_ref: Mapped[str | None] = mapped_column(String(256), nullable=True)
    operator_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
