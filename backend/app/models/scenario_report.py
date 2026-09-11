"""Scenario report API schemas (W4-U04)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, field_validator

from app.core.time import coerce_external_utc


class ScenarioReportRead(BaseModel):
    id: str
    created_at: datetime
    artifact_type: str
    method_version: str
    market_class: str
    symbol: str
    timeframe: str
    as_of_start: datetime
    as_of_end: datetime
    sample_count: int
    scenario_name: str
    hypothetical_return: float
    scenario_result: dict[str, Any]
    assumptions: dict[str, Any]
    inputs: dict[str, Any]
    uncertainty: dict[str, Any]
    economic_usefulness: dict[str, Any]
    config: dict[str, Any]
    input_lineage: dict[str, Any]
    source_artifact_ids: list[Any]
    market_scope: dict[str, Any]
    results: dict[str, Any]
    limitations: list[Any]
    report_hash: str
    research_status: str
    created_by: str
    audit_correlation_id: str
    notes: str | None

    @field_validator("created_at", "as_of_start", "as_of_end")
    @classmethod
    def _datetimes_utc(cls, value: datetime) -> datetime:
        normalized = coerce_external_utc(value, source="scenario report schema output")
        assert normalized is not None
        return normalized

    model_config = {"from_attributes": True}
