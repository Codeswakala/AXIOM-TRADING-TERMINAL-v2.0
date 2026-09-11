"""Chart research annotation API schemas (W5-U03)."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator

from app.core.time import coerce_external_utc


class ChartResearchAnnotationCreate(BaseModel):
    artifact_type: Literal["chart_research_annotation", "chart_research_drawing"] = (
        "chart_research_annotation"
    )
    chart_context: dict[str, Any]
    content: dict[str, Any]
    source_artifact_ids: list[str] = Field(min_length=1)
    provenance: dict[str, Any] = Field(default_factory=dict)
    uncertainty: dict[str, Any] = Field(default_factory=dict)
    research_status: Literal["research_only"] = "research_only"


class ChartResearchAnnotationUpdate(BaseModel):
    """CHART-P03: content-only update (drawing reposition) — the other
    fields are immutable once audited; geometry travels in content."""

    content: dict[str, Any]


class ChartResearchAnnotationRead(BaseModel):
    id: str
    created_at: datetime
    operator_id: str
    artifact_type: str
    chart_context: dict[str, Any]
    content: dict[str, Any]
    source_artifact_ids: list[str]
    provenance: dict[str, Any]
    uncertainty: dict[str, Any]
    disclaimer: str
    research_status: str
    audit_correlation_id: str

    @field_validator("created_at")
    @classmethod
    def _created_at_utc(cls, value: datetime) -> datetime:
        normalized = coerce_external_utc(value, source="chart annotation schema output")
        assert normalized is not None
        return normalized

    model_config = {"from_attributes": True}
