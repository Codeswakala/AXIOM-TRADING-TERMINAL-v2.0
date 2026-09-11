"""Unit tests for CSV loader column mapping."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.ingestion.csv_loader import CsvLoaderError, iter_csv_rows, resolve_column_map

FIXTURES = Path(__file__).resolve().parent / "fixtures"
SAMPLES = Path(__file__).resolve().parents[1] / "sample_data"


def test_resolve_column_map_standard() -> None:
    mapping = resolve_column_map(["timestamp", "open", "high", "low", "close", "volume"])
    assert mapping["timestamp"] == "timestamp"
    assert mapping["volume"] == "volume"


def test_resolve_column_map_aliases() -> None:
    mapping = resolve_column_map(["time", "o", "h", "l", "c", "vol"])
    assert mapping["timestamp"] == "time"
    assert mapping["open"] == "o"
    assert mapping["volume"] == "vol"


def test_resolve_column_map_missing_raises() -> None:
    with pytest.raises(CsvLoaderError):
        resolve_column_map(["open", "high", "low"])


def test_iter_csv_rows_sample() -> None:
    rows = list(iter_csv_rows(SAMPLES / "eurusd_h1_sample.csv"))
    assert len(rows) == 5
    assert rows[0][0] == 1
    assert "open" in rows[0][1]


def test_iter_csv_rows_missing_file() -> None:
    with pytest.raises(CsvLoaderError):
        list(iter_csv_rows(SAMPLES / "does_not_exist.csv"))
