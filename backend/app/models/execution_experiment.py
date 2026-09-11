"""Execution research experiment API schemas (W6-U05)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.time import coerce_external_utc


class ExecutionResearchExperimentCreate(BaseModel):
    experiment_title: str = Field(min_length=1, max_length=200)
    hypothesis: str = Field(min_length=1)
    market_class: str = Field(min_length=1, max_length=64)
    symbol: str = Field(min_length=1, max_length=128)
    timeframe: str = Field(min_length=1, max_length=32)
    as_of_start: datetime
    as_of_time: datetime
    input_artifact_ids: list[str] = Field(min_length=1)
    max_candles: int = Field(default=100, ge=1, le=1000)

    model_config = ConfigDict(extra="forbid")

    @field_validator("as_of_start", "as_of_time")
    @classmethod
    def _datetimes_utc(cls, value: datetime) -> datetime:
        normalized = coerce_external_utc(value, source="execution experiment create")
        assert normalized is not None
        return normalized


class ExecutionResearchExperimentRead(BaseModel):
    experiment_id: str
    created_at: datetime
    simulation_mode: str
    operator_id: str
    experiment_title: str
    pre_registration_plan: dict[str, Any]
    plan_hash: str
    as_of_time: datetime
    as_of_window: dict[str, Any]
    replay_input_lineage: dict[str, Any]
    included_scope_summary: dict[str, Any]
    uncertainty: dict[str, Any]
    limitations: list[Any]
    research_status: str
    simulation_disclaimer: str
    audit_correlation_id: str

    @field_validator("created_at", "as_of_time")
    @classmethod
    def _read_datetimes_utc(cls, value: datetime) -> datetime:
        normalized = coerce_external_utc(value, source="execution experiment read")
        assert normalized is not None
        return normalized

    model_config = ConfigDict(from_attributes=True)
