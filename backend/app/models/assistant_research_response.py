"""Assistant research response API schemas (W5-U02)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, field_validator

from app.core.time import coerce_external_utc


class AssistantResearchResponseRead(BaseModel):
    assistant_response_id: str
    created_at: datetime
    operator_id: str
    request_id: str
    request_text_hash: str
    assistant_policy_version: str
    provider_name: str
    provider_version: str
    model_or_engine_version: str
    source_artifact_ids: list[str]
    grounding_summary: str
    response_text: str
    refused: bool
    refusal_reason: str | None
    limitations: list[str]
    disclaimer: str
    research_status: str
    audit_correlation_id: str
    provenance: dict[str, Any]

    @field_validator("created_at")
    @classmethod
    def _created_at_utc(cls, value: datetime) -> datetime:
        normalized = coerce_external_utc(value, source="assistant response schema output")
        assert normalized is not None
        return normalized

    model_config = {"from_attributes": True}
