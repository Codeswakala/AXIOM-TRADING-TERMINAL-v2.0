"""Shared types for ingestion pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Any

from app.core.time import require_utc


@dataclass(slots=True)
class NormalizedCandleRow:
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
    extra: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        normalized = require_utc(self.open_time, boundary="normalized_candle_row.open_time")
        assert normalized is not None
        self.open_time = normalized


@dataclass(slots=True)
class RowValidationError:
    row_number: int
    message: str
    raw: dict[str, Any] | None = None


@dataclass(slots=True)
class IngestionResult:
    run_id: str
    status: str
    source_name: str
    market_class: str
    symbol: str
    timeframe: str
    rows_read: int = 0
    rows_valid: int = 0
    rows_invalid: int = 0
    rows_inserted: int = 0
    rows_updated: int = 0
    rows_unchanged: int = 0
    duration_ms: int = 0
    errors: list[RowValidationError] = field(default_factory=list)
    error_summary: str | None = None
