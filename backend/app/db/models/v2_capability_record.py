"""V2 Capability Record — read-only seeded capability registry.

No enabled column. No runtime mutation. Seeded during migration.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, utc_now


class V2CapabilityRecord(Base):
    """V2 capability registry record. Read-only seeded."""

    __tablename__ = "v2_capability_record"
    __table_args__ = (
        Index("ix_v2_capability_id", "capability_id", unique=True),
        Index("ix_v2_capability_domain", "domain"),
        Index("ix_v2_capability_band", "band"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    capability_id: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    domain: Mapped[str] = mapped_column(String(64), nullable=False)
    band: Mapped[str] = mapped_column(String(16), nullable=False)
    maturity: Mapped[str] = mapped_column(String(32), nullable=False)
    artifact_status: Mapped[str] = mapped_column(String(32), nullable=False)
    version: Mapped[str] = mapped_column(String(16), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
