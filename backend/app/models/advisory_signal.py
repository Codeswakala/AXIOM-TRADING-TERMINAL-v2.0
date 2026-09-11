"""Advisory signal API schemas (W3-U02)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, field_validator

from app.core.time import coerce_external_utc


class AdvisorySignalRead(BaseModel):
    signal_id: str
    created_at: datetime
    as_of_time: datetime
    market_class: str
    provider: str
    symbol: str
    timeframe: str
    model_artifact_id: str
    model_version: str
    feature_set_version: str
    experiment_id: str
    statistical_report_id: str | None
    calibration_report_id: str | None
    economic_report_id: str | None
    generalization_report_id: str | None
    inference_input_hash: str
    raw_score: float | None
    calibrated_confidence: float | None
    input_staleness_seconds: int | None
    signal_validity_seconds: int | None
    expires_at: datetime | None
    freshness_status: str | None
    signal_direction: str
    signal_state: str
    state_reason: str
    eligibility_reasons: list[Any]
    operating_domain_status: str
    calibration_status: str
    economic_verdict: str
    risk_notes: str | None
    rationale: str
    explainability_summary: dict[str, Any]
    state_transition_history: list[Any]
    audit_correlation_id: str

    @field_validator("created_at", "as_of_time", "expires_at")
    @classmethod
    def _datetimes_utc(cls, value: datetime | None) -> datetime | None:
        normalized = coerce_external_utc(value, source="advisory signal schema output")
        return normalized

    model_config = {"from_attributes": True}
