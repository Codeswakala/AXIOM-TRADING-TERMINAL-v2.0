"""V2 BE-2 integrity validators and exception fingerprinting (plan D.0/D.2).

Pure functions — no I/O. Fingerprints implement the UNIQUE-deduplication
rule: fingerprint = SHA-256(series_ref | exception_type | affected_natural_key
| state_basis). Repeated identical detection is a persistence no-op.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

from app.v2.marketdata.provenance import timeframe_seconds
from app.v2.temporal.validation import require_utc, utc_now

EXCEPTION_TYPES = frozenset(
    {
        "out_of_order",
        "duplicate",
        "future_data",
        "unmapped_symbol",
        "gap",
        "stale",
        "verification_mismatch",
    }
)


def compute_fingerprint(
    series_ref: str,
    exception_type: str,
    affected_natural_key: str,
    state_basis: str = "constant",
) -> str:
    if exception_type not in EXCEPTION_TYPES:
        raise ValueError(f"unknown exception type: {exception_type}")
    payload = "|".join((series_ref, exception_type, affected_natural_key, state_basis))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class IntegrityFinding:
    """A validator result destined for the exception table (via W-1/W-2)."""

    series_ref: str
    exception_type: str
    fingerprint: str
    detail: dict[str, Any]
    observed_at: datetime


def _finding(
    series_ref: str,
    exception_type: str,
    natural_key: str,
    detail: dict[str, Any],
    *,
    state_basis: str = "constant",
    observed_at: datetime | None = None,
) -> IntegrityFinding:
    return IntegrityFinding(
        series_ref=series_ref,
        exception_type=exception_type,
        fingerprint=compute_fingerprint(series_ref, exception_type, natural_key, state_basis),
        detail=detail,
        observed_at=observed_at if observed_at is not None else utc_now(),
    )


def check_future_data(
    series_ref: str, open_time: datetime, *, now: datetime | None = None
) -> IntegrityFinding | None:
    """No served/verification-scoped datum may be in the future (plan D.1)."""
    require_utc(open_time, boundary="open_time")
    reference = now if now is not None else utc_now()
    if open_time > reference:
        return _finding(
            series_ref,
            "future_data",
            open_time.isoformat(),
            {"open_time": open_time.isoformat(), "server_now": reference.isoformat()},
        )
    return None


def check_ordering(
    series_ref: str, open_times: list[datetime]
) -> list[IntegrityFinding]:
    """Strictly increasing open_time per series; duplicates surface separately."""
    findings: list[IntegrityFinding] = []
    seen: set[datetime] = set()
    previous: datetime | None = None
    for ot in open_times:
        require_utc(ot, boundary="open_time")
        if ot in seen:
            findings.append(
                _finding(
                    series_ref,
                    "duplicate",
                    ot.isoformat(),
                    {"open_time": ot.isoformat()},
                )
            )
            continue
        if previous is not None and ot < previous:
            findings.append(
                _finding(
                    series_ref,
                    "out_of_order",
                    ot.isoformat(),
                    {"open_time": ot.isoformat(), "previous": previous.isoformat()},
                )
            )
        seen.add(ot)
        previous = max(previous, ot) if previous is not None else ot
    return findings


def check_gaps(
    series_ref: str,
    timeframe: str,
    open_times: list[datetime],
) -> list[IntegrityFinding]:
    """Missing expected periods on the 24x7 simulator grid.

    Approved state-basis rule (plan D.0 Rule 3, corrected per DEL-003):
    gap fingerprint natural key = missing-period start; **state_basis =
    coverage-window end at detection** (isoformat of the latest open_time).
    Consequences:
    - re-detecting a known gap while coverage is unchanged → identical
      fingerprint → persistence no-op;
    - when coverage advances (new bars arrive) the same missing period
      produces a NEW fingerprint, making the gap's persistence across
      coverage states an explicit recorded transition.
    """
    if len(open_times) < 2:
        return []
    period = timedelta(seconds=timeframe_seconds(timeframe))
    ordered = sorted(set(open_times))
    coverage_end = ordered[-1].isoformat()
    findings: list[IntegrityFinding] = []
    for earlier, later in zip(ordered, ordered[1:]):
        expected = earlier + period
        while expected < later:
            findings.append(
                _finding(
                    series_ref,
                    "gap",
                    expected.isoformat(),
                    {
                        "missing_period_start": expected.isoformat(),
                        "coverage_end": coverage_end,
                    },
                    state_basis=coverage_end,
                )
            )
            expected = expected + period
    return findings


def check_stale_transition(
    series_ref: str,
    previous_freshness: str,
    current_freshness: str,
    *,
    episode_boundary: str,
) -> IntegrityFinding | None:
    """Record only on transition edges fresh→stale / stale→expired.

    ``episode_boundary`` (e.g. last_open_time isoformat at detection) is the
    state_basis: recovery to fresh closes the episode; the next stale episode
    has a new boundary and therefore a new fingerprint.
    """
    edges = {("fresh", "stale"), ("stale", "expired"), ("fresh", "expired")}
    if (previous_freshness, current_freshness) not in edges:
        return None
    return _finding(
        series_ref,
        "stale",
        current_freshness,
        {
            "transition": f"{previous_freshness}->{current_freshness}",
            "episode_boundary": episode_boundary,
        },
        state_basis=episode_boundary,
    )


def unmapped_symbol_finding(source_id: str, source_symbol: str) -> IntegrityFinding:
    series_ref = f"{source_id}:{source_symbol}"
    return _finding(
        series_ref,
        "unmapped_symbol",
        f"{source_id}|{source_symbol}",
        {"source_id": source_id, "source_symbol": source_symbol},
    )


def verification_mismatch_finding(
    verification_id: str, expected_hash: str, actual_hash: str
) -> IntegrityFinding:
    """Once per record per mismatch transition (first-detection edge)."""
    return _finding(
        f"verification:{verification_id}",
        "verification_mismatch",
        verification_id,
        {"expected_hash": expected_hash, "actual_hash": actual_hash},
        state_basis="first-detection",
    )
