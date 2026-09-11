"""Normalization and basic quality checks for OHLCV rows."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any

from app.core.time import coerce_external_utc
from app.ingestion.types import NormalizedCandleRow, RowValidationError

REQUIRED_FIELDS = ("timestamp", "open", "high", "low", "close")


def parse_timestamp(value: Any) -> datetime:
    """Parse timestamps to timezone-aware UTC."""
    if value is None or value == "":
        raise ValueError("timestamp is required")
    if isinstance(value, datetime):
        dt = value
    else:
        text = str(value).strip()
        # Support trailing Z
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        try:
            dt = datetime.fromisoformat(text)
        except ValueError as exc:
            # Fallback common format YYYY-MM-DD HH:MM:SS
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
                try:
                    dt = datetime.strptime(text, fmt)
                    break
                except ValueError:
                    continue
            else:
                raise ValueError(f"unrecognized timestamp: {value!r}") from exc
    # CSV rows are external operator/data-vendor input. Naive values are accepted
    # for Wave-0 compatibility but explicitly logged as an assumed-UTC boundary.
    normalized = coerce_external_utc(dt, source="csv timestamp input")
    assert normalized is not None
    return normalized


def parse_decimal(value: Any, *, field_name: str) -> Decimal:
    if value is None or value == "":
        raise ValueError(f"{field_name} is required")
    try:
        return Decimal(str(value).strip())
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"invalid decimal for {field_name}: {value!r}") from exc


def parse_optional_decimal(value: Any) -> Decimal | None:
    if value is None or value == "":
        return None
    return parse_decimal(value, field_name="volume")


def normalize_symbol(symbol: str) -> str:
    return symbol.strip().upper().replace(" ", "")


def normalize_market_class(market_class: str) -> str:
    return market_class.strip().lower()


def normalize_timeframe(timeframe: str) -> str:
    return timeframe.strip().upper()


def validate_ohlc(open_: Decimal, high: Decimal, low: Decimal, close: Decimal) -> None:
    if high < low:
        raise ValueError("high must be >= low")
    if high < open_ or high < close:
        raise ValueError("high must be >= open and close")
    if low > open_ or low > close:
        raise ValueError("low must be <= open and close")
    if any(v < 0 for v in (open_, high, low, close)):
        raise ValueError("prices must be non-negative")


def normalize_row(
    raw: dict[str, Any],
    *,
    row_number: int,
    market_class: str,
    symbol: str,
    timeframe: str,
    source: str | None,
) -> tuple[NormalizedCandleRow | None, RowValidationError | None]:
    try:
        for field in REQUIRED_FIELDS:
            if field not in raw or raw[field] in (None, ""):
                raise ValueError(f"missing required field: {field}")

        open_ = parse_decimal(raw["open"], field_name="open")
        high = parse_decimal(raw["high"], field_name="high")
        low = parse_decimal(raw["low"], field_name="low")
        close = parse_decimal(raw["close"], field_name="close")
        volume = parse_optional_decimal(raw.get("volume"))
        open_time = parse_timestamp(raw["timestamp"])
        validate_ohlc(open_, high, low, close)
        if volume is not None and volume < 0:
            raise ValueError("volume must be non-negative")

        row = NormalizedCandleRow(
            market_class=normalize_market_class(market_class),
            symbol=normalize_symbol(symbol),
            timeframe=normalize_timeframe(timeframe),
            open_time=open_time,
            open=open_,
            high=high,
            low=low,
            close=close,
            volume=volume,
            source=source,
            extra=None,
        )
        return row, None
    except Exception as exc:  # noqa: BLE001 — row-level isolation
        return None, RowValidationError(
            row_number=row_number,
            message=str(exc),
            raw={k: str(v) for k, v in raw.items()},
        )
