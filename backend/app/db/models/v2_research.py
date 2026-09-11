"""V2 BE-4 research read-model tables (BO-V2-BE-4-001 D-1; plan §5.1).

Append-only: DB-level guard triggers (R-2) + no repository UPDATE surface.
PKs: uuid4 TEXT(36) (BG-8).
"""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import JSON, DateTime, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.v2.temporal.validation import utc_now


class V2ComputationVersion(Base):
    """Registered component versions (plan §1.2; spec §53). Immutable."""

    __tablename__ = "v2_computation_version"
    __table_args__ = (
        UniqueConstraint("component", "version", name="uq_v2_compver_component_version"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    component: Mapped[str] = mapped_column(String(64), nullable=False)
    version: Mapped[str] = mapped_column(String(64), nullable=False)
    source_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    evidence_ref: Mapped[str | None] = mapped_column(String(256), nullable=True)
    registered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )


class V2MarketContextReport(Base):
    """Immutable market-context report artifacts (plan §5.1)."""

    __tablename__ = "v2_market_context_report"
    __table_args__ = (
        UniqueConstraint(
            "instrument_id", "input_content_hash", "engine_versions_hash",
            name="uq_v2_mcr_determinism_anchor",
        ),
        Index("ix_v2_mcr_instrument", "instrument_id"),
        Index("ix_v2_mcr_mode", "mode"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    instrument_id: Mapped[str] = mapped_column(String(96), nullable=False)
    timeframe_set: Mapped[list] = mapped_column(JSON, nullable=False)
    as_of: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    validation_tier: Mapped[str] = mapped_column(
        String(32), nullable=False, default="pipeline-validation"
    )
    input_snapshot_id: Mapped[str] = mapped_column(String(256), nullable=False)
    input_content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    observations: Mapped[dict] = mapped_column(JSON, nullable=False)
    engine_versions: Mapped[dict] = mapped_column(JSON, nullable=False)
    engine_versions_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )


class V2ChartIntelligenceReport(Base):
    """Immutable chart-intelligence artifacts (plan §5.1)."""

    __tablename__ = "v2_chart_intelligence_report"
    __table_args__ = (
        Index("ix_v2_cir_mcr", "market_context_report_id"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    market_context_report_id: Mapped[str] = mapped_column(String(36), nullable=False)
    as_of: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    annotations: Mapped[dict] = mapped_column(JSON, nullable=False)
    interpretations: Mapped[dict] = mapped_column(JSON, nullable=False)
    engine_versions: Mapped[dict] = mapped_column(JSON, nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
