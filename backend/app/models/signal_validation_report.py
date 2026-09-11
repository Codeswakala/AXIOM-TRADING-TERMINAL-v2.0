"""Signal validation report API schemas (W4-U06)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, field_validator

from app.core.time import coerce_external_utc


class SignalValidationReportRead(BaseModel):
    id: str
    created_at: datetime
    artifact_type: str
    method_version: str
    scope_start: datetime
    scope_end: datetime
    sample_count: int
    metrics: dict[str, Any]
    uncertainty: dict[str, Any]
    validation_scope: dict[str, Any]
    outcome_data_status: dict[str, Any]
    economic_usefulness: dict[str, Any]
    config: dict[str, Any]
    input_lineage: dict[str, Any]
    source_signal_ids: list[Any]
    market_scope: dict[str, Any]
    results: dict[str, Any]
    limitations: list[Any]
    report_hash: str
    research_status: str
    created_by: str
    audit_correlation_id: str
    notes: str | None

    @field_validator("created_at", "scope_start", "scope_end")
    @classmethod
    def _datetimes_utc(cls, value: datetime) -> datetime:
        normalized = coerce_external_utc(value, source="signal validation report schema output")
        assert normalized is not None
        return normalized

    model_config = {"from_attributes": True}
