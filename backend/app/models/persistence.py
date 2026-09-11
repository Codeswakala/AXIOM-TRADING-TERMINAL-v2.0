"""Pydantic schemas for persistence-facing APIs (W0-U02 evidence surface)."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator

from app.core.time import coerce_external_utc


class CandleCreate(BaseModel):
    market_class: str = Field(examples=["forex"])
    symbol: str = Field(examples=["EURUSD"])
    timeframe: str = Field(examples=["H1"])
    open_time: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal | None = None
    source: str | None = "api"

    @field_validator("open_time")
    @classmethod
    def _open_time_utc(cls, value: datetime) -> datetime:
        normalized = coerce_external_utc(value, source="persistence schema boundary")
        assert normalized is not None
        return normalized


class CandleRead(BaseModel):
    id: str
    market_class: str
    symbol: str
    timeframe: str
    open_time: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal | None
    source: str | None
    created_at: datetime
    # DATA-P02: populated only on aggregated bars — every emitted bar is a
    # complete bucket (partial buckets are excluded and disclosed by the
    # envelope, never padded); constituents states the bucket's minute count.
    complete: bool | None = None
    constituents: int | None = None

    @field_validator("open_time", "created_at")
    @classmethod
    def _datetimes_utc(cls, value: datetime) -> datetime:
        normalized = coerce_external_utc(value, source="persistence schema boundary")
        assert normalized is not None
        return normalized

    model_config = {"from_attributes": True}


class CandleSeriesEnvelope(BaseModel):
    """DATA-P02 M4: typed series result — the discriminant is carried on the
    response; consumers must never infer the state from message strings or
    bar counts."""

    kind: Literal["native", "aggregated", "unavailable"]
    timeframe: str
    sourceTimeframe: str | None = None
    excludedPartialBuckets: int | None = None
    detail: str | None = None
    bars: list[CandleRead] = Field(default_factory=list)


class AuditEventRead(BaseModel):
    id: str
    category: str
    action: str
    actor: str
    message: str
    resource_type: str | None
    resource_id: str | None
    details: dict[str, Any] | None
    created_at: datetime

    @field_validator("created_at")
    @classmethod
    def _created_at_utc(cls, value: datetime) -> datetime:
        normalized = coerce_external_utc(value, source="persistence schema boundary")
        assert normalized is not None
        return normalized

    model_config = {"from_attributes": True}


class DatabaseStatsResponse(BaseModel):
    backend: str
    database_url_scheme: str
    pool: dict[str, Any]
    candle_count: int
    audit_count: int
