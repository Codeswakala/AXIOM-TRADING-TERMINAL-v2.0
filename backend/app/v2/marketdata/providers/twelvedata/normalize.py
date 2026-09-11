"""Twelve Data response normalization → BE-2 contracts (pure functions, P1).

Input shapes come from workspace-reviewed static fixtures (unverified
candidate documentation samples). Every output is validated by the BE-2
quality rules; timestamps become aware-UTC; symbol echo is verified against
the requested canonical id (misdelivery refusal). No provenance is emitted
here — provider authority remains reserved/unemittable in P1.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any

from app.v2.errors.contract import V2Error, V2ErrorCode
from app.v2.marketdata.providers.twelvedata.symbols import to_canonical


@dataclass(frozen=True, slots=True)
class NormalizedBar:
    """Provider-neutral bar (pre-provenance; P1 fixture output only)."""

    instrument_id: str
    timeframe: str
    open_time: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal | None


def _fail(detail: str) -> V2Error:
    return V2Error(code=V2ErrorCode.VALIDATION_FAILED, detail=detail, status_code=422)


def _dec(raw: Any, field_name: str) -> Decimal:
    try:
        return Decimal(str(raw))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise _fail(f"Malformed numeric field: {field_name}") from exc


def _utc(raw: str) -> datetime:
    """TD 'datetime' strings ('YYYY-MM-DD HH:MM:SS') are declared UTC in the
    candidate documentation for this endpoint family; parsed and made aware.
    A malformed value is a refusal, not a guess."""
    try:
        parsed = datetime.fromisoformat(raw)
    except ValueError as exc:
        raise _fail("Malformed datetime field") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def normalize_time_series(
    payload: dict[str, Any],
    *,
    requested_instrument_id: str,
    requested_timeframe: str,
) -> list[NormalizedBar]:
    """Normalize a TD `time_series`-shaped payload.

    Refusals: provider error shape, missing meta/values, symbol-echo
    mismatch (misdelivery), malformed numerics/timestamps, OHLC insanity,
    negative volume.
    """
    if payload.get("status") == "error" or "code" in payload and "message" in payload:
        raise V2Error(
            code=V2ErrorCode.DATA_UNAVAILABLE,
            detail="Provider fixture reports an error state",
            status_code=502,
        )
    meta = payload.get("meta")
    values = payload.get("values")
    if not isinstance(meta, dict) or not isinstance(values, list):
        raise _fail("Fixture missing meta/values")

    echoed = to_canonical(str(meta.get("symbol", "")))
    if echoed is None or echoed != requested_instrument_id:
        raise _fail("Symbol echo mismatch: refusing misdelivered data")

    bars: list[NormalizedBar] = []
    for row in values:
        if not isinstance(row, dict):
            raise _fail("Malformed value row")
        open_ = _dec(row.get("open"), "open")
        high = _dec(row.get("high"), "high")
        low = _dec(row.get("low"), "low")
        close = _dec(row.get("close"), "close")
        volume = (
            _dec(row.get("volume"), "volume") if row.get("volume") is not None else None
        )
        if not (low <= open_ <= high and low <= close <= high and low <= high):
            raise _fail("OHLC sanity violation")
        if volume is not None and volume < 0:
            raise _fail("Negative volume")
        bars.append(
            NormalizedBar(
                instrument_id=requested_instrument_id,
                timeframe=requested_timeframe,
                open_time=_utc(str(row.get("datetime"))),
                open=open_,
                high=high,
                low=low,
                close=close,
                volume=volume,
            )
        )
    # ascending chronological order for downstream validators
    bars.sort(key=lambda b: b.open_time)
    return bars


def normalize_quote(
    payload: dict[str, Any], *, requested_instrument_id: str
) -> dict[str, Any]:
    """Normalize a TD `quote`-shaped payload to a neutral dict (P1 test use)."""
    echoed = to_canonical(str(payload.get("symbol", "")))
    if echoed is None or echoed != requested_instrument_id:
        raise _fail("Symbol echo mismatch: refusing misdelivered data")
    return {
        "instrument_id": requested_instrument_id,
        "close": str(_dec(payload.get("close"), "close")),
        "as_of": _utc(str(payload.get("datetime"))).isoformat(),
    }
