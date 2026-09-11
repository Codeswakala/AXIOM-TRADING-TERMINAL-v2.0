"""V2 Lineage Models — Pydantic models for lineage API responses."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class V2LineageRecordResponse(BaseModel):
    """Response model for a single V2 lineage record."""

    id: str
    artifact_type: str
    artifact_id: str
    operator_id: str
    mode: str
    source_artifact_ids: list[str] | None
    computation_version: str | None
    input_snapshot_id: str | None
    created_at: datetime


class V2LineageListResponse(BaseModel):
    """Response model for V2 lineage record list."""

    records: list[V2LineageRecordResponse]
    total: int
    mode: str
    scope: str  # "operator" or "all"
    correlation_id: str | None = None
    timestamp: datetime
