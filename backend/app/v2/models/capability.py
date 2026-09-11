"""V2 Capability Models — Pydantic models for capability API responses."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class V2CapabilityResponse(BaseModel):
    """Response model for a single V2 capability."""

    id: str
    capability_id: str
    domain: str
    band: str
    maturity: str
    artifact_status: str
    version: str
    created_at: datetime


class V2CapabilityDetailResponse(BaseModel):
    """Typed envelope for the single-capability endpoint (DEF-BE1-06).

    Every V2 response carries mode, correlation ID, and timestamp context.
    """

    capability: V2CapabilityResponse
    mode: str
    correlation_id: str | None = None
    timestamp: datetime


class V2CapabilityListResponse(BaseModel):
    """Response model for V2 capability list."""

    capabilities: list[V2CapabilityResponse]
    total: int
    mode: str
    correlation_id: str | None = None
    timestamp: datetime
