"""Research management API schemas (W7-U03)."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.time import coerce_external_utc


class ResearchCollectionRead(BaseModel):
    collection_id: str
    created_at: datetime
    updated_at: datetime
    operator_id: str
    name: str
    description: str | None
    research_status: str
    audit_correlation_id: str

    @field_validator("created_at", "updated_at")
    @classmethod
    def _datetimes_utc(cls, value: datetime) -> datetime:
        normalized = coerce_external_utc(value, source="research collection read")
        assert normalized is not None
        return normalized

    model_config = ConfigDict(from_attributes=True)


class ResearchCollectionMemberRead(BaseModel):
    member_id: str
    created_at: datetime
    operator_id: str
    collection_id: str
    artifact_type: str
    artifact_id: str
    audit_correlation_id: str

    @field_validator("created_at")
    @classmethod
    def _created_at_utc(cls, value: datetime) -> datetime:
        normalized = coerce_external_utc(value, source="research collection member read")
        assert normalized is not None
        return normalized

    model_config = ConfigDict(from_attributes=True)


class ResearchTagRead(BaseModel):
    tag_id: str
    created_at: datetime
    operator_id: str
    artifact_type: str
    artifact_id: str
    tag: str
    audit_correlation_id: str

    @field_validator("created_at")
    @classmethod
    def _created_at_utc(cls, value: datetime) -> datetime:
        normalized = coerce_external_utc(value, source="research tag read")
        assert normalized is not None
        return normalized

    model_config = ConfigDict(from_attributes=True)


class ResearchCollectionDetail(ResearchCollectionRead):
    members: list[ResearchCollectionMemberRead] = Field(default_factory=list)


class ResearchManagementBundle(BaseModel):
    collections: list[ResearchCollectionRead]
    members: list[ResearchCollectionMemberRead]
    tags: list[ResearchTagRead]
    supported_artifact_types: list[str]
    posture: str = "reference_only_research_management"
