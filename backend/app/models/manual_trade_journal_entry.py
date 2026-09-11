"""Manual research journal API schemas (W5-U07)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.time import coerce_external_utc


class ManualTradeJournalEntryWrite(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    reflection_text: str = Field(min_length=1)
    linked_plan_id: str | None = None
    linked_signal_ids: list[str] = Field(default_factory=list)
    linked_report_ids: list[str] = Field(default_factory=list)
    emotion_tags: list[str] = Field(default_factory=list)
    process_tags: list[str] = Field(default_factory=list)
    lesson_notes: str | None = None

    model_config = ConfigDict(extra="forbid")


class ManualTradeJournalEntryRead(BaseModel):
    journal_id: str
    created_at: datetime
    operator_id: str
    title: str
    reflection_text: str
    linked_plan_id: str | None
    linked_signal_ids: list[Any]
    linked_report_ids: list[Any]
    emotion_tags: list[Any]
    process_tags: list[Any]
    lesson_notes: str | None
    research_disclaimer: str
    research_status: str
    audit_correlation_id: str

    @field_validator("created_at")
    @classmethod
    def _created_at_utc(cls, value: datetime) -> datetime:
        normalized = coerce_external_utc(value, source="manual journal schema output")
        assert normalized is not None
        return normalized

    model_config = ConfigDict(from_attributes=True)
