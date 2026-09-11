"""V2 Permission — read-only seeded permission table.

Seeded during migration. No runtime mutation.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, utc_now


class V2Permission(Base):
    """V2 permission record. Read-only seeded."""

    __tablename__ = "v2_permission"
    __table_args__ = (
        Index("ix_v2_permission_role_permission", "role", "permission", unique=True),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    role: Mapped[str] = mapped_column(String(32), nullable=False)
    permission: Mapped[str] = mapped_column(String(128), nullable=False)
    sal: Mapped[str] = mapped_column(String(16), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
