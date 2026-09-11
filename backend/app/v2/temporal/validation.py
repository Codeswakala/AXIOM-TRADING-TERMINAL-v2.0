"""V2 Temporal Validation — timezone-aware clock and validation.

V2 paths use require_utc() ONLY. No coerce_external_utc() on V2 paths.
Naive datetimes are rejected, not coerced.
"""

from __future__ import annotations

from datetime import datetime, timezone

from app.v2.errors.contract import TemporalError

UTC = timezone.utc


def utc_now() -> datetime:
    """Return the current time as timezone-aware UTC."""
    return datetime.now(UTC)


def is_naive(value: datetime) -> bool:
    """Check if a datetime is naive (no timezone info)."""
    return value.tzinfo is None or value.tzinfo.utcoffset(value) is None


def require_utc(value: datetime | None, *, boundary: str) -> datetime | None:
    """Normalize an aware datetime to UTC. Reject naive values.

    This is the V2 temporal validation function. It does NOT coerce
    naive datetimes — it raises TemporalError.
    """
    if value is None:
        return None
    if is_naive(value):
        raise TemporalError(
            f"Naive datetime rejected at V2 boundary: {boundary}. "
            f"V2 requires timezone-aware UTC datetimes."
        )
    return value.astimezone(UTC)


def utc_iso(value: datetime | None) -> str | None:
    """Return ISO-8601 string for a UTC-normalized datetime."""
    if value is None:
        return None
    normalized = require_utc(value, boundary="iso serialization")
    return normalized.isoformat()
