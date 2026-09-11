"""System information schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from app.core.time import coerce_external_utc


class SystemInfoResponse(BaseModel):
    """High-level platform identity for operators and frontend shell."""

    name: str
    version: str
    environment: str
    wave: str = Field(default="7 — Institutional Platform")
    unit: str = Field(default="W7-U08")
    architecture_version: str = Field(default="2.0.0")
    description: str = Field(
        default=(
            "Institutional multi-market AI research and trading intelligence platform "
            "(Wave-7 Closeout & Whole-Project Completion Checkpoint)"
        )
    )
    timestamp: datetime

    @field_validator("timestamp")
    @classmethod
    def _timestamp_utc(cls, value: datetime) -> datetime:
        normalized = coerce_external_utc(value, source="system schema output")
        assert normalized is not None
        return normalized
