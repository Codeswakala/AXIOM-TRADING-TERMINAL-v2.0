"""Execution risk research report API schemas (W6-U04)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.time import coerce_external_utc


class ExecutionRiskResearchReportCreate(BaseModel):
    input_artifact_ids: list[str] = Field(min_length=1)

    model_config = ConfigDict(extra="forbid")


class ExecutionRiskResearchReportRead(BaseModel):
    report_id: str
    created_at: datetime
    simulation_mode: str
    input_artifact_ids: list[Any]
    simulated_request_summary: dict[str, Any]
    risk_metrics: dict[str, Any]
    uncertainty: dict[str, Any]
    limitations: list[Any]
    economic_usefulness: dict[str, Any]
    research_status: str
    simulation_disclaimer: str
    audit_correlation_id: str

    @field_validator("created_at")
    @classmethod
    def _created_at_utc(cls, value: datetime) -> datetime:
        normalized = coerce_external_utc(value, source="execution risk report read")
        assert normalized is not None
        return normalized

    model_config = ConfigDict(from_attributes=True)
