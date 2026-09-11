"""V2 BE-6 portfolio-research tables (BO-V2-BE-6-001 T-2).

Both tables fully immutable at the DB level; definition edits = successor
rows (P-1 versioning, C-1 `supersedes` vocabulary). PKs uuid4 TEXT(36).
"""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    JSON,
    CheckConstraint,
    DateTime,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.v2.temporal.validation import utc_now

_DATA_CLASS_CHECK = (
    "data_class IN ('synthetic','simulated','historical_real','live',"
    "'stale_cached','unavailable')"
)


class V2PortfolioDefinition(Base):
    """Hypothetical portfolio definition — versioned-immutable (P-1)."""

    __tablename__ = "v2_portfolio_definition"
    __table_args__ = (
        UniqueConstraint("portfolio_id", "record_seq",
                         name="uq_v2_pfdef_id_seq"),
        Index("ix_v2_pfdef_portfolio", "portfolio_id"),
        CheckConstraint("basis IN ('hypothetical')",
                        name="ck_v2_pfdef_basis"),
        CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_pfdef_data_class"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    portfolio_id: Mapped[str] = mapped_column(String(64), nullable=False)
    record_seq: Mapped[int] = mapped_column(Integer, nullable=False)
    # C-1 vocabulary: this row SUPERSEDES the predecessor whose id it holds.
    supersedes: Mapped[str | None] = mapped_column(String(36), nullable=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    basis: Mapped[str] = mapped_column(String(16), nullable=False)
    allocations: Mapped[list] = mapped_column(JSON, nullable=False)
    base_currency: Mapped[str] = mapped_column(String(8), nullable=False)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    assumptions: Mapped[dict] = mapped_column(JSON, nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )


class V2PortfolioRiskReport(Base):
    """Immutable portfolio risk-report artifact (P-2 / 0043 pattern)."""

    __tablename__ = "v2_portfolio_risk_report"
    __table_args__ = (
        UniqueConstraint("portfolio_definition_id", "inputs_hash",
                         "engine_versions_hash",
                         name="uq_v2_pfrisk_determinism_anchor"),
        Index("ix_v2_pfrisk_def", "portfolio_definition_id"),
        CheckConstraint(
            "status IN ('available','degraded','unavailable','stale',"
            "'unknown','denied')",
            name="ck_v2_pfrisk_status"),
        CheckConstraint("basis_label IN ('hypothetical-research')",
                        name="ck_v2_pfrisk_basis_label"),
        CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_pfrisk_data_class"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    portfolio_definition_id: Mapped[str] = mapped_column(String(36), nullable=False)
    as_of: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    time_basis: Mapped[dict] = mapped_column(JSON, nullable=False)
    input_refs: Mapped[dict] = mapped_column(JSON, nullable=False)
    inputs_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    metrics: Mapped[list] = mapped_column(JSON, nullable=False)
    scenarios: Mapped[list] = mapped_column(JSON, nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    basis_label: Mapped[str] = mapped_column(String(32), nullable=False)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    engine_versions: Mapped[dict] = mapped_column(JSON, nullable=False)
    engine_versions_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
