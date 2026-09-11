"""CSV historical OHLCV loader with configurable column mapping."""

from __future__ import annotations

import csv
from collections.abc import Iterator
from pathlib import Path
from typing import Any, Mapping

from app.core.logging import get_logger

logger = get_logger(__name__, category="MARKET")

# Canonical internal field names → accepted CSV header aliases (case-insensitive)
DEFAULT_COLUMN_ALIASES: dict[str, tuple[str, ...]] = {
    "timestamp": ("timestamp", "time", "datetime", "date", "open_time"),
    "open": ("open", "o"),
    "high": ("high", "h"),
    "low": ("low", "l"),
    "close": ("close", "c"),
    "volume": ("volume", "vol", "v"),
}


class CsvLoaderError(ValueError):
    """Raised when a CSV cannot be loaded or mapped."""


def _normalize_header(name: str) -> str:
    return name.strip().lower().replace(" ", "_")


def resolve_column_map(
    headers: list[str],
    aliases: Mapping[str, tuple[str, ...]] | None = None,
) -> dict[str, str]:
    """Map canonical field → actual CSV header name."""
    aliases = aliases or DEFAULT_COLUMN_ALIASES
    normalized = {_normalize_header(h): h for h in headers}
    mapping: dict[str, str] = {}
    for canonical, options in aliases.items():
        for option in options:
            key = _normalize_header(option)
            if key in normalized:
                mapping[canonical] = normalized[key]
                break
    missing = [f for f in ("timestamp", "open", "high", "low", "close") if f not in mapping]
    if missing:
        raise CsvLoaderError(
            f"CSV missing required columns for {missing}. Found headers: {headers}"
        )
    return mapping


def iter_csv_rows(
    path: str | Path,
    *,
    delimiter: str = ",",
    encoding: str = "utf-8",
    aliases: Mapping[str, tuple[str, ...]] | None = None,
) -> Iterator[tuple[int, dict[str, Any]]]:
    """Yield (row_number, canonical_dict) for each data row. Row numbers are 1-based data rows."""
    file_path = Path(path)
    if not file_path.is_file():
        raise CsvLoaderError(f"CSV file not found: {file_path}")

    logger.info("Opening CSV path=%s", file_path)
    with file_path.open("r", encoding=encoding, newline="") as handle:
        reader = csv.DictReader(handle, delimiter=delimiter)
        if not reader.fieldnames:
            raise CsvLoaderError("CSV has no header row")
        column_map = resolve_column_map(list(reader.fieldnames), aliases=aliases)
        for index, raw in enumerate(reader, start=1):
            if raw is None:
                continue
            # Skip completely empty lines
            if all((v is None or str(v).strip() == "") for v in raw.values()):
                continue
            canonical: dict[str, Any] = {}
            for field, header in column_map.items():
                canonical[field] = raw.get(header)
            yield index, canonical
