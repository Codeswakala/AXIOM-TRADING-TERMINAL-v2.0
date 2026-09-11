"""V2 BE-2 Market Data models — six additive tables (BO-V2-BE-2-001).

All timestamps timezone-aware UTC. `v2_md_integrity_exception` and
`v2_md_asof_verification` are append-only (DB triggers, both dialects).
Reference tables (instrument/symbol_map/source) are read-only seeded from the
versioned seed manifest (app.v2.marketdata.seed).
"""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import JSON, CheckConstraint, DateTime, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.v2.temporal.validation import utc_now

_MARKET_CLASSES = "'forex','crypto','index','equity','commodity','metal','future','etf','synthetic'"


class V2MdInstrument(Base):
    """Canonical instrument registry (read-only seeded in BE-2)."""

    __tablename__ = "v2_md_instrument"
    __table_args__ = (
        UniqueConstraint("instrument_id", name="uq_v2_md_instrument_id"),
        CheckConstraint(f"market_class IN ({_MARKET_CLASSES})", name="ck_v2_md_instrument_class"),
        Index("ix_v2_md_instrument_class", "market_class"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    instrument_id: Mapped[str] = mapped_column(String(96), nullable=False)
    market_class: Mapped[str] = mapped_column(String(32), nullable=False)
    display_symbol: Mapped[str] = mapped_column(String(64), nullable=False)
    precision: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    meta: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )


class V2MdSymbolMap(Base):
    """Source symbol → canonical instrument (read-only seeded, exact match)."""

    __tablename__ = "v2_md_symbol_map"
    __table_args__ = (
        UniqueConstraint("source_id", "source_symbol", name="uq_v2_md_symbol_map"),
        Index("ix_v2_md_symbol_map_instrument", "instrument_id"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    source_id: Mapped[str] = mapped_column(String(64), nullable=False)
    source_symbol: Mapped[str] = mapped_column(String(64), nullable=False)
    instrument_id: Mapped[str] = mapped_column(String(96), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )


class V2MdSource(Base):
    """Data-source registry (read-only seeded).

    Active authority is constitutionally bounded: only seed:synthetic and
    live:simulated rows may be active (emission guard + CHECK constraints).
    """

    __tablename__ = "v2_md_source"
    __table_args__ = (
        UniqueConstraint("source_id", name="uq_v2_md_source_id"),
        CheckConstraint(
            "kind IN ('simulator','seed','import','reserved')", name="ck_v2_md_source_kind"
        ),
        CheckConstraint(
            "authority IN ('seed:synthetic','live:simulated','historical:imported','unknown')",
            name="ck_v2_md_source_authority",
        ),
        # DEL-001: an ACTIVE source may never carry reserved/unapproved
        # authority vocabulary. Activation of historical:imported requires a
        # V2 Amendment Register entry — not a data change.
        CheckConstraint(
            "active = false OR authority IN ('seed:synthetic','live:simulated','unknown')",
            name="ck_v2_md_source_active_authority",
        ),
        CheckConstraint(
            "mode_scope IN ('RESEARCH','SIMULATION')", name="ck_v2_md_source_mode"
        ),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    source_id: Mapped[str] = mapped_column(String(64), nullable=False)
    kind: Mapped[str] = mapped_column(String(16), nullable=False)
    authority: Mapped[str] = mapped_column(String(32), nullable=False)
    mode_scope: Mapped[str] = mapped_column(String(16), nullable=False)
    active: Mapped[bool] = mapped_column(nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )


class V2MdSeries(Base):
    """Series catalog — written only by W-1 catalog refresh.

    Freshness is NOT stored; it is computed at read time (plan D.0 Rule 2).
    """

    __tablename__ = "v2_md_series"
    __table_args__ = (
        UniqueConstraint(
            "instrument_id", "timeframe", "source_id", name="uq_v2_md_series_triple"
        ),
        Index("ix_v2_md_series_instrument", "instrument_id"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    instrument_id: Mapped[str] = mapped_column(String(96), nullable=False)
    timeframe: Mapped[str] = mapped_column(String(16), nullable=False)
    source_id: Mapped[str] = mapped_column(String(64), nullable=False)
    first_open_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_open_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    bar_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )


class V2MdIntegrityException(Base):
    """Integrity/quarantine records — append-only, fingerprint-deduplicated.

    Written only by W-1/W-2. UNIQUE fingerprint enforces idempotency
    (plan D.0 Rule 3). SAL-3: operator-owned (DEL-002) — the W-1/W-2 actor —
    with separate audited admin read-all access.
    """

    __tablename__ = "v2_md_integrity_exception"
    __table_args__ = (
        UniqueConstraint("fingerprint", name="uq_v2_md_integrity_fingerprint"),
        CheckConstraint(
            "exception_type IN ('out_of_order','duplicate','future_data',"
            "'unmapped_symbol','gap','stale','verification_mismatch')",
            name="ck_v2_md_integrity_type",
        ),
        Index("ix_v2_md_integrity_series", "series_ref", "observed_at"),
        Index("ix_v2_md_integrity_operator", "operator_id"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    series_ref: Mapped[str] = mapped_column(String(192), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    exception_type: Mapped[str] = mapped_column(String(32), nullable=False)
    fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    detail: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )


class V2MdAsOfVerification(Base):
    """As-Of Verification Record — tamper-evidence ONLY (append-only).

    Per ITRGA-DET-V2-BE-2-PLAN-001: verification-only semantics; NOT a
    reproducible snapshot; cannot reconstruct original rows if the underlying
    V1 store changes. API responses carry reconstructive=false.
    """

    __tablename__ = "v2_md_asof_verification"
    __table_args__ = (
        UniqueConstraint("verification_id", name="uq_v2_md_asof_verification_id"),
        Index("ix_v2_md_asof_verification_operator", "created_by_operator_id"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    verification_id: Mapped[str] = mapped_column(String(64), nullable=False)
    scope: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    as_of: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    row_count: Mapped[int] = mapped_column(Integer, nullable=False)
    source_ids: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    created_by_operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
