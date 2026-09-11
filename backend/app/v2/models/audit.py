"""V2 Audit Models — Pydantic models for audit API responses."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class V2AuditEventResponse(BaseModel):
    """Response model for a single V2 audit event."""

    id: str
    correlation_id: str
    causation_id: str | None
    actor_id: str
    actor_type: str
    domain: str
    action: str
    resource_type: str | None
    resource_id: str | None
    mode: str
    details: dict[str, Any] | None
    classification: str
    operator_id: str | None
    created_at: datetime


class V2AuditListResponse(BaseModel):
    """Response model for V2 audit event list."""

    events: list[V2AuditEventResponse]
    total: int
    mode: str
    scope: str  # "operator" or "all"
    correlation_id: str | None = None
    timestamp: datetime
