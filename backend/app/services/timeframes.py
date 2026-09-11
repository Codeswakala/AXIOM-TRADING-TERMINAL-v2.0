"""Canonical timeframe vocabulary — the single source of truth for DATA-P02.

F-DATA2-1 repair: the UI offered 1m/5m/15m/1h/4h/1d while the database stored
M1 only, and the client mapped labels to codes ad hoc. From this phase the
backend owns one vocabulary; every aggregation, validation and response
metadata path imports it from here. The frontend mirrors the identical golden
table (frontend/src/api/timeframes.ts) and both sides pin it with tests — a
divergence fails loudly: the API timeframe pattern rejects codes outside this
vocabulary with 422, never silently.

Wall-clock note: all buckets are UTC-aligned (see ohlcv_aggregation.bucket_start_for).
"""

from __future__ import annotations

TIMEFRAME_MINUTES: dict[str, int] = {
    "M1": 1,
    "M5": 5,
    "M15": 15,
    "H1": 60,
    "H4": 240,
    "D1": 1440,
}

TIMEFRAME_LABELS: dict[str, str] = {
    "M1": "1m",
    "M5": "5m",
    "M15": "15m",
    "H1": "1h",
    "H4": "4h",
    "D1": "1d",
}

VALID_TIMEFRAMES: tuple[str, ...] = tuple(TIMEFRAME_MINUTES)

TIMEFRAME_PATTERN = "^(M1|M5|M15|H1|H4|D1)$"

AGGREGATED_TIMEFRAMES: frozenset[str] = frozenset(("M5", "M15", "H1", "H4", "D1"))
