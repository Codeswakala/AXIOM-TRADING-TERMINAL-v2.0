"""Advisory analytics API schemas (W3-U07)."""

from __future__ import annotations

from pydantic import BaseModel


class AnalyticsUncertainty(BaseModel):
    method: str
    lower: float
    upper: float
    confidence_level: float
    sample_count: int


class AdvisoryAnalyticsMetric(BaseModel):
    key: str
    label: str
    value: float
    unit: str
    sample_count: int
    uncertainty: AnalyticsUncertainty
    interpretation: str


class ConfidenceBandRead(BaseModel):
    label: str
    lower: float
    upper: float
    sample_count: int
    average_calibrated_confidence: float | None
    calibration_status: str
    uncertainty: AnalyticsUncertainty
    unreliable: bool
    economic_context: str


class AdvisoryAnalyticsResponse(BaseModel):
    generated_from: str
    disclaimer: str
    metrics: list[AdvisoryAnalyticsMetric]
    confidence_bands: list[ConfidenceBandRead]
    notes: list[str]
