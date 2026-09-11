"""V2 Mode Models — Pydantic models for mode API responses."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class V2ModeResponse(BaseModel):
    """Response model for V2 mode status."""

    mode: str
    valid_modes: list[str]
    deferred_modes: list[str]
    source: str = "AXIOM_V2_MODE"
    immutable_at_runtime: bool = True
    correlation_id: str | None = None
    timestamp: datetime
