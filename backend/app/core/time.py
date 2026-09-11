"""Timezone utilities for AXIOM.

AXIOM stores and exposes timestamps as timezone-aware UTC. Internal/trusted
boundaries reject naive datetimes so timezone defects are not hidden. External
operator inputs may be interpreted as UTC only at explicit ingress validators,
where the compatibility assumption is logged.
"""

from __future__ import annotations

from datetime import datetime, timezone

from app.core.logging import get_logger

UTC = timezone.utc
logger = get_logger(__name__, category="SYSTEM")


def utc_now() -> datetime:
    """Return the current time as timezone-aware UTC."""
    return datetime.now(UTC)


def is_naive(value: datetime) -> bool:
    return value.tzinfo is None or value.tzinfo.utcoffset(value) is None


def require_utc(value: datetime | None, *, boundary: str) -> datetime | None:
    """Normalize an aware datetime to UTC, rejecting naive trusted values."""
    if value is None:
        return None
    if is_naive(value):
        raise ValueError(f"Naive datetime rejected at trusted boundary: {boundary}")
    return value.astimezone(UTC)


def coerce_external_utc(value: datetime | None, *, source: str) -> datetime | None:
    """Normalize external/driver values to UTC, logging any naive assumption.

    This function is for external API inputs and database-driver serialization
    compatibility only. Trusted internal storage/ingestion boundaries should use
    ``require_utc`` so naive timestamps fail loudly.
    """
    if value is None:
        return None
    if is_naive(value):
        logger.warning("Naive datetime assumed UTC at external boundary: %s", source)
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


# Backward-compatible name for API/schema serialization boundaries.
def ensure_utc(value: datetime | None) -> datetime | None:
    return coerce_external_utc(value, source="schema serialization")


def utc_iso(value: datetime | None) -> str | None:
    """Return ISO-8601 string for a UTC-normalized datetime."""
    normalized = coerce_external_utc(value, source="iso serialization")
    return normalized.isoformat() if normalized is not None else None
