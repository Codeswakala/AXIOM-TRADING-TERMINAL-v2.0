"""Unit tests for OHLCV normalization and validation."""

from __future__ import annotations

from datetime import timezone
from decimal import Decimal

import pytest

from app.ingestion.normalize import (
    normalize_row,
    normalize_symbol,
    parse_timestamp,
    validate_ohlc,
)


def test_parse_timestamp_iso_z() -> None:
    dt = parse_timestamp("2024-01-02T00:00:00Z")
    assert dt.tzinfo is not None
    assert dt.astimezone(timezone.utc).hour == 0


def test_parse_timestamp_naive_assumes_utc() -> None:
    dt = parse_timestamp("2024-02-01 01:00:00")
    assert dt.tzinfo is not None


def test_normalize_symbol() -> None:
    assert normalize_symbol(" eurusd ") == "EURUSD"


def test_validate_ohlc_rejects_high_lt_low() -> None:
    with pytest.raises(ValueError):
        validate_ohlc(Decimal("1"), Decimal("0.9"), Decimal("1.1"), Decimal("1"))


def test_normalize_row_success() -> None:
    row, err = normalize_row(
        {
            "timestamp": "2024-01-02T00:00:00Z",
            "open": "1.10",
            "high": "1.12",
            "low": "1.09",
            "close": "1.11",
            "volume": "10",
        },
        row_number=1,
        market_class="Forex",
        symbol="eurusd",
        timeframe="h1",
        source="test",
    )
    assert err is None
    assert row is not None
    assert row.symbol == "EURUSD"
    assert row.market_class == "forex"
    assert row.timeframe == "H1"
    assert row.close == Decimal("1.11")


def test_normalize_row_missing_field() -> None:
    row, err = normalize_row(
        {"timestamp": "2024-01-02T00:00:00Z", "open": "1"},
        row_number=2,
        market_class="forex",
        symbol="EURUSD",
        timeframe="H1",
        source=None,
    )
    assert row is None
    assert err is not None
    assert err.row_number == 2


def test_normalize_row_bad_ohlc() -> None:
    row, err = normalize_row(
        {
            "timestamp": "2024-01-02T00:00:00Z",
            "open": "1.10",
            "high": "1.05",
            "low": "1.09",
            "close": "1.11",
        },
        row_number=3,
        market_class="forex",
        symbol="EURUSD",
        timeframe="H1",
        source=None,
    )
    assert row is None
    assert err is not None
