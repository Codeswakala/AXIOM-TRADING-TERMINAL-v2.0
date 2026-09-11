"""Operator-scoped research management metadata (W7-U03)."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, utc_now


class ResearchCollection(Base):
    """Per-operator research collection metadata.

    Collections organize existing governed artifacts by reference only. They do not
    own, copy, cascade to, or mutate source artifacts.
    """

    __tablename__ = "research_collections"
    __table_args__ = (
        UniqueConstraint(
            "operator_id",
            "name",
            name="uq_research_collections_operator_name",
        ),
        Index("ix_research_collections_operator", "operator_id"),
        Index("ix_research_collections_correlation_id", "audit_correlation_id"),
    )

    collection_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False
    )
    operator_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("operators.id", ondelete="RESTRICT"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    research_status: Mapped[str] = mapped_column(String(64), nullable=False)
    audit_correlation_id: Mapped[str] = mapped_column(String(64), nullable=False)


class ResearchCollectionMember(Base):
    """Reference-only collection membership for a governed artifact."""

    __tablename__ = "research_collection_members"
    __table_args__ = (
        UniqueConstraint(
            "collection_id",
            "artifact_type",
            "artifact_id",
            name="uq_research_collection_members_collection_artifact",
        ),
        Index("ix_research_collection_members_operator", "operator_id"),
        Index("ix_research_collection_members_collection", "collection_id"),
        Index(
            "ix_research_collection_members_artifact",
            "artifact_type",
            "artifact_id",
        ),
        Index("ix_research_collection_members_correlation_id", "audit_correlation_id"),
    )

    member_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    operator_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("operators.id", ondelete="RESTRICT"), nullable=False
    )
    collection_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("research_collections.collection_id", ondelete="RESTRICT"),
        nullable=False,
    )
    artifact_type: Mapped[str] = mapped_column(String(96), nullable=False)
    artifact_id: Mapped[str] = mapped_column(String(96), nullable=False)
    audit_correlation_id: Mapped[str] = mapped_column(String(64), nullable=False)


class ResearchTag(Base):
    """Per-operator tag metadata over an existing governed artifact."""

    __tablename__ = "research_tags"
    __table_args__ = (
        UniqueConstraint(
            "operator_id",
            "artifact_type",
            "artifact_id",
            "tag",
            name="uq_research_tags_operator_artifact_tag",
        ),
        Index("ix_research_tags_operator", "operator_id"),
        Index("ix_research_tags_artifact", "artifact_type", "artifact_id"),
        Index("ix_research_tags_tag", "tag"),
        Index("ix_research_tags_correlation_id", "audit_correlation_id"),
    )

    tag_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    operator_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("operators.id", ondelete="RESTRICT"), nullable=False
    )
    artifact_type: Mapped[str] = mapped_column(String(96), nullable=False)
    artifact_id: Mapped[str] = mapped_column(String(96), nullable=False)
    tag: Mapped[str] = mapped_column(String(96), nullable=False)
    audit_correlation_id: Mapped[str] = mapped_column(String(64), nullable=False)
