"""Trade plan note API schemas (W5-U06)."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.time import coerce_external_utc


class TradePlanNoteWrite(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    market_context: str = Field(min_length=1)
    hypothesis: str = Field(min_length=1)
    linked_signal_ids: list[str] = Field(default_factory=list)
    linked_report_ids: list[str] = Field(default_factory=list)
    scenario_notes: str | None = None
    risk_notes: str | None = None
    invalidating_conditions_text: str | None = None
    decision_status: Literal["draft", "archived", "reviewed"] = "draft"

    model_config = ConfigDict(extra="forbid")


class TradePlanNoteRead(BaseModel):
    plan_id: str
    created_at: datetime
    updated_at: datetime
    operator_id: str
    title: str
    market_context: str
    hypothesis: str
    linked_signal_ids: list[Any]
    linked_report_ids: list[Any]
    scenario_notes: str | None
    risk_notes: str | None
    invalidating_conditions_text: str | None
    decision_status: str
    research_disclaimer: str
    research_status: str
    audit_correlation_id: str

    @field_validator("created_at", "updated_at")
    @classmethod
    def _datetimes_utc(cls, value: datetime) -> datetime:
        normalized = coerce_external_utc(value, source="trade plan note schema output")
        assert normalized is not None
        return normalized

    model_config = ConfigDict(from_attributes=True)
