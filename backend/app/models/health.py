"""Health and readiness response schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator

from app.core.time import coerce_external_utc


class ServiceStatus(BaseModel):
    """Status of an individual subsystem check."""

    name: str
    status: Literal["up", "down", "degraded", "stub"]
    detail: str | None = None
    latency_ms: float | None = None


class HealthResponse(BaseModel):
    """Liveness response — process is running."""

    status: Literal["ok", "error"] = "ok"
    service: str
    version: str
    environment: str
    timestamp: datetime
    message: str = Field(default="AXIOM backend is alive")
    latency_ms: float | None = None

    @field_validator("timestamp")
    @classmethod
    def _timestamp_utc(cls, value: datetime) -> datetime:
        normalized = coerce_external_utc(value, source="health schema output")
        assert normalized is not None
        return normalized


class ReadinessResponse(BaseModel):
    """Readiness response — process can accept traffic for foundation scope."""

    status: Literal["ready", "not_ready"]
    service: str
    version: str
    environment: str
    timestamp: datetime
    checks: list[ServiceStatus]

    @field_validator("timestamp")
    @classmethod
    def _timestamp_utc(cls, value: datetime) -> datetime:
        normalized = coerce_external_utc(value, source="health schema output")
        assert normalized is not None
        return normalized
