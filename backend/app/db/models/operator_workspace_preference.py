"""Operator workspace preferences (W7-U02)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base, utc_now


class OperatorWorkspacePreference(Base):
    """Per-operator presentation-only workspace preferences."""

    __tablename__ = "operator_workspace_preferences"
    __table_args__ = (
        UniqueConstraint(
            "operator_id",
            "workspace_key",
            name="uq_operator_workspace_preferences_operator_workspace",
        ),
        Index("ix_operator_workspace_preferences_operator", "operator_id"),
        Index("ix_operator_workspace_preferences_workspace_key", "workspace_key"),
        Index("ix_operator_workspace_preferences_correlation_id", "audit_correlation_id"),
    )

    preference_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False
    )
    operator_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("operators.id", ondelete="RESTRICT"), nullable=False
    )
    workspace_key: Mapped[str] = mapped_column(String(96), nullable=False)
    layout_config: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    visible_modules: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    theme_config: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    research_status: Mapped[str] = mapped_column(String(64), nullable=False)
    metadata_json: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, nullable=False)
    audit_correlation_id: Mapped[str] = mapped_column(String(64), nullable=False)
