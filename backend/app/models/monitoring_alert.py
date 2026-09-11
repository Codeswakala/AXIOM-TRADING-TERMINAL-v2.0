"""Monitoring alert API schemas (W3-U06 + BO-B-05 emission inputs)."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator

from app.core.time import coerce_external_utc


class MonitoringAlertRead(BaseModel):
    alert_id: str
    created_at: datetime
    alert_type: str
    severity: str
    subject_type: str
    subject_id: str
    market_class: str | None
    symbol: str | None
    timeframe: str | None
    model_artifact_id: str | None
    signal_id: str | None
    summary: str
    evidence: dict[str, Any]
    lineage: dict[str, Any]
    acknowledged: bool
    acknowledged_at: datetime | None
    acknowledged_by: str | None
    audit_correlation_id: str

    @field_validator("created_at", "acknowledged_at")
    @classmethod
    def _datetimes_utc(cls, value: datetime | None) -> datetime | None:
        return coerce_external_utc(value, source="monitoring alert schema output")

    model_config = {"from_attributes": True}


class InferenceHealthCheckRequest(BaseModel):
    """BO-B-05.2 — explicit inference-health degradation input.

    Only degraded states are accepted: the emission path exists for health
    degradation, not for spurious 'ok' alerts. Status severity mapping lives
    in the service (degraded→warning, down→critical).
    """

    component: str = Field(min_length=1, max_length=128)
    status: Literal["degraded", "down"]
    detail: str = Field(min_length=1, max_length=1024)


class AlertCheckResponse(BaseModel):
    """BO-B-05.1/2/3 — governed check-path result (bounded, honest counts)."""

    stale_alerts_emitted: int
    drift_alerts_emitted: int
    withheld_alerts_emitted: int
    stale_symbols_checked: int
    threshold_seconds: int
    cooldown_seconds: int
    emitted_alert_ids: list[str]
