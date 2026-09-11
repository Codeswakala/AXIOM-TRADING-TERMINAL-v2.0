"""Pydantic schemas for ingestion API (verification surface)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator

from app.core.time import coerce_external_utc


class IngestCsvRequest(BaseModel):
    """Trigger historical CSV ingestion from a server-side path (foundation only)."""

    path: str = Field(
        description="Absolute or backend-relative path to CSV under allowed sample dirs",
    )
    market_class: str = Field(examples=["forex"])
    symbol: str = Field(examples=["EURUSD"])
    timeframe: str = Field(examples=["H1"])
    source: str | None = Field(default=None, description="Optional source label")


class IngestSampleRequest(BaseModel):
    """Ingest a built-in sample fixture by name."""

    sample_name: str = Field(
        examples=["eurusd_h1_sample.csv", "btcusd_h1_sample.csv"],
        description="Filename under backend/sample_data/",
    )
    market_class: str
    symbol: str
    timeframe: str
    source: str | None = None


class RowErrorRead(BaseModel):
    row_number: int
    message: str


class IngestionResultRead(BaseModel):
    run_id: str
    status: str
    source_name: str
    market_class: str
    symbol: str
    timeframe: str
    rows_read: int
    rows_valid: int
    rows_invalid: int
    rows_inserted: int
    rows_updated: int
    rows_unchanged: int
    duration_ms: int
    error_summary: str | None = None
    errors: list[RowErrorRead] = Field(default_factory=list)


class IngestionRunRead(BaseModel):
    id: str
    source_type: str
    source_name: str
    market_class: str
    symbol: str
    timeframe: str
    status: str
    rows_read: int
    rows_valid: int
    rows_invalid: int
    rows_inserted: int
    rows_updated: int
    rows_unchanged: int
    duration_ms: int | None
    error_summary: str | None
    details: dict[str, Any] | None
    started_at: datetime
    finished_at: datetime | None

    @field_validator("started_at", "finished_at")
    @classmethod
    def _datetimes_utc(cls, value: datetime | None) -> datetime | None:
        return coerce_external_utc(value, source="ingestion schema output")

    model_config = {"from_attributes": True}


class IngestionStatsResponse(BaseModel):
    total_runs: int
    last_run: IngestionRunRead | None
    candle_count_total: int
    candle_counts_by_filter: dict[str, str | int]
