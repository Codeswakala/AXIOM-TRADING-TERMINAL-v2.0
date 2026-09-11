"""Portfolio/risk research report model (W4-U05)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Float, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base, utc_now


class PortfolioRiskReport(Base):
    """Persisted inert hypothetical market-series risk research artifact."""

    __tablename__ = "portfolio_risk_reports"
    __table_args__ = (
        Index("ix_portfolio_risk_reports_created_at", "created_at"),
        Index("ix_portfolio_risk_reports_series", "market_class", "symbol", "timeframe"),
        Index("ix_portfolio_risk_reports_report_hash", "report_hash"),
        Index("ix_portfolio_risk_reports_correlation_id", "audit_correlation_id"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    artifact_type: Mapped[str] = mapped_column(String(96), nullable=False)
    method_version: Mapped[str] = mapped_column(String(96), nullable=False)
    market_class: Mapped[str] = mapped_column(String(64), nullable=False)
    symbol: Mapped[str] = mapped_column(String(128), nullable=False)
    timeframe: Mapped[str] = mapped_column(String(32), nullable=False)
    as_of_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    as_of_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    sample_count: Mapped[int] = mapped_column(Integer, nullable=False)
    max_drawdown: Mapped[float] = mapped_column(Float, nullable=False)
    realized_volatility: Mapped[float] = mapped_column(Float, nullable=False)
    stress_loss: Mapped[float] = mapped_column(Float, nullable=False)
    metrics: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    uncertainty: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    assumptions: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    economic_usefulness: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    config: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    input_lineage: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    source_artifact_ids: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    market_scope: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    results: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    limitations: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    report_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    research_status: Mapped[str] = mapped_column(
        String(64), nullable=False, default="research_only"
    )
    created_by: Mapped[str] = mapped_column(String(128), nullable=False)
    audit_correlation_id: Mapped[str] = mapped_column(String(64), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
