"""Persisted assistant research responses and refusals (W5-U02)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import Boolean, DateTime, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base, utc_now


class AssistantResearchResponse(Base):
    """Audited assistant response/refusal record.

    The schema intentionally stores only a request hash, never raw request text.
    Rows are inert research artifacts and carry no execution, account, or sizing
    payload fields.
    """

    __tablename__ = "assistant_research_responses"
    __table_args__ = (
        Index("ix_assistant_research_responses_created_at", "created_at"),
        Index("ix_assistant_research_responses_operator", "operator_id"),
        Index("ix_assistant_research_responses_request_hash", "request_text_hash"),
        Index("ix_assistant_research_responses_correlation_id", "audit_correlation_id"),
        Index("ix_assistant_research_responses_refused", "refused"),
    )

    assistant_response_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    request_id: Mapped[str] = mapped_column(String(36), nullable=False)
    request_text_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    assistant_policy_version: Mapped[str] = mapped_column(String(96), nullable=False)
    provider_name: Mapped[str] = mapped_column(String(96), nullable=False)
    provider_version: Mapped[str] = mapped_column(String(96), nullable=False)
    model_or_engine_version: Mapped[str] = mapped_column(String(128), nullable=False)
    source_artifact_ids: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    grounding_summary: Mapped[str] = mapped_column(Text, nullable=False)
    response_text: Mapped[str] = mapped_column(Text, nullable=False)
    refused: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    refusal_reason: Mapped[str | None] = mapped_column(String(96), nullable=True)
    limitations: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    disclaimer: Mapped[str] = mapped_column(Text, nullable=False)
    research_status: Mapped[str] = mapped_column(String(64), nullable=False)
    audit_correlation_id: Mapped[str] = mapped_column(String(64), nullable=False)
    provenance: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
