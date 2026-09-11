"""V2 Lineage Record — append-only lineage metadata table.

DB triggers enforce immutability (no UPDATE/DELETE).
Operator-scoped reads; admin read_all requires SAL-4 permission.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Index, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base, utc_now


class V2LineageRecord(Base):
    """V2 lineage record. Append-only; immutable after creation."""

    __tablename__ = "v2_lineage_record"
    __table_args__ = (
        Index("ix_v2_lineage_artifact", "artifact_type", "artifact_id"),
        Index("ix_v2_lineage_operator", "operator_id"),
        Index("ix_v2_lineage_mode", "mode"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    artifact_type: Mapped[str] = mapped_column(String(64), nullable=False)
    artifact_id: Mapped[str] = mapped_column(String(128), nullable=False)
    source_artifact_ids: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    computation_version: Mapped[str | None] = mapped_column(String(64), nullable=True)
    input_snapshot_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
