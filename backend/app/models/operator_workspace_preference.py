"""Operator workspace preference API schemas (W7-U02)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.time import coerce_external_utc


class OperatorWorkspacePreferenceWrite(BaseModel):
    workspace_key: str = Field(default="default", min_length=1, max_length=96)
    layout_config: dict[str, Any] = Field(default_factory=dict)
    visible_modules: list[str] = Field(default_factory=list)
    theme_config: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(extra="forbid")


class OperatorWorkspacePreferenceRead(BaseModel):
    preference_id: str
    created_at: datetime
    updated_at: datetime
    operator_id: str
    workspace_key: str
    layout_config: dict[str, Any]
    visible_modules: list[Any]
    theme_config: dict[str, Any]
    research_status: str
    metadata_json: dict[str, Any] = Field(serialization_alias="metadata")
    audit_correlation_id: str

    @field_validator("created_at", "updated_at")
    @classmethod
    def _datetimes_utc(cls, value: datetime) -> datetime:
        normalized = coerce_external_utc(value, source="workspace preference read")
        assert normalized is not None
        return normalized

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
