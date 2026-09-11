"""Simulated execution analytics report API schemas (W6-U06)."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.time import coerce_external_utc


class SimulatedExecutionAnalyticsReportCreate(BaseModel):
    source_artifact_ids: list[str] = Field(min_length=1)
    analytics_type: Literal[
        "slippage_distribution",
        "return_estimate",
        "fill_model_comparison",
        "replay_scope_comparison",
    ] = "return_estimate"

    model_config = ConfigDict(extra="forbid")


class SimulatedExecutionAnalyticsReportRead(BaseModel):
    report_id: str
    created_at: datetime
    simulation_mode: str
    analytics_type: str
    included_scope: dict[str, Any]
    sample_count: int
    metrics: dict[str, Any]
    uncertainty: dict[str, Any]
    limitations: list[Any]
    economic_usefulness: dict[str, Any]
    report_hash: str
    source_artifact_ids: list[Any]
    research_status: str
    simulation_disclaimer: str
    audit_correlation_id: str

    @field_validator("created_at")
    @classmethod
    def _created_at_utc(cls, value: datetime) -> datetime:
        normalized = coerce_external_utc(value, source="simulated analytics report read")
        assert normalized is not None
        return normalized

    model_config = ConfigDict(from_attributes=True)
