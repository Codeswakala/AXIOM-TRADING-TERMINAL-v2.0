"""V2 Error Models — Pydantic models for error API responses."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class V2ErrorResponse(BaseModel):
    """Response model for V2 error responses."""

    error_code: str
    detail: str
    correlation_id: str | None = None
    timestamp: datetime


class V2ErrorTaxonomyResponse(BaseModel):
    """Response model for V2 error taxonomy reference."""

    error_codes: list[dict[str, str]]
    domain_statuses: list[str]
    mode: str
    correlation_id: str | None = None
    timestamp: datetime
