"""V2 BE-2 provenance / freshness / availability taxonomy and guards.

Constitutional boundary (ITRGA-DET-V2-BE-2-PLAN-001 §1.3 / BO-V2-BE-2-001 §3.2):
BE-2 active API responses may emit ONLY `seed:synthetic`, `live:simulated`,
and honest `unknown`. `historical:imported` is reserved vocabulary — defined
for taxonomy stability but unconstructible in any active emission path.
Activation requires a future explicit V2 Amendment Register entry.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.v2.errors.contract import V2Error, V2ErrorCode
from app.v2.temporal.validation import require_utc, utc_now

# --- authority vocabulary ---------------------------------------------------

AUTHORITY_SEED_SYNTHETIC = "seed:synthetic"
AUTHORITY_LIVE_SIMULATED = "live:simulated"
AUTHORITY_UNKNOWN = "unknown"
AUTHORITY_HISTORICAL_IMPORTED = "historical:imported"  # RESERVED — inactive

#: The only authority values an active BE-2 response may carry.
ACTIVE_AUTHORITY_VALUES: frozenset[str] = frozenset(
    {AUTHORITY_SEED_SYNTHETIC, AUTHORITY_LIVE_SIMULATED, AUTHORITY_UNKNOWN}
)

#: Full stable taxonomy (includes reserved values for schema CHECKs only).
ALL_AUTHORITY_VALUES: frozenset[str] = ACTIVE_AUTHORITY_VALUES | {
    AUTHORITY_HISTORICAL_IMPORTED
}

#: Mandatory display labels — the API returns the label so no consumer can
#: mislabel data authority.
AUTHORITY_DISPLAY_LABELS: dict[str, str] = {
    AUTHORITY_SEED_SYNTHETIC: "SYNTHETIC SEED",
    AUTHORITY_LIVE_SIMULATED: "SIMULATED",
    AUTHORITY_UNKNOWN: "UNKNOWN SOURCE",
}

# --- freshness / availability ------------------------------------------------

FRESHNESS_FRESH = "fresh"
FRESHNESS_STALE = "stale"
FRESHNESS_EXPIRED = "expired"
FRESHNESS_UNKNOWN = "unknown"

AVAILABILITY_AVAILABLE = "available"
AVAILABILITY_PARTIAL = "partial"
AVAILABILITY_EMPTY = "empty"
AVAILABILITY_QUARANTINED = "quarantined"
AVAILABILITY_UNAVAILABLE = "unavailable"
AVAILABILITY_UNKNOWN = "unknown"

#: Per-timeframe staleness budgets (seconds): stale after 2 periods,
#: expired after 10 periods. Simulator grid is 24x7.
_TIMEFRAME_SECONDS: dict[str, int] = {
    "M1": 60,
    "M5": 300,
    "M15": 900,
    "M30": 1800,
    "H1": 3600,
    "H4": 14400,
    "D1": 86400,
}


def timeframe_seconds(timeframe: str) -> int:
    tf = timeframe.upper()
    if tf not in _TIMEFRAME_SECONDS:
        raise V2Error(
            code=V2ErrorCode.VALIDATION_FAILED,
            detail=f"Unsupported timeframe: {tf}",
            status_code=400,
        )
    return _TIMEFRAME_SECONDS[tf]


def compute_freshness(
    last_open_time: datetime | None, timeframe: str, *, now: datetime | None = None
) -> str:
    """Read-time freshness. Never persisted (plan D.0 Rule 2)."""
    if last_open_time is None:
        return FRESHNESS_UNKNOWN
    require_utc(last_open_time, boundary="last_open_time")
    period = timeframe_seconds(timeframe)
    reference = now if now is not None else utc_now()
    age = (reference - last_open_time).total_seconds()
    if age <= 2 * period:
        return FRESHNESS_FRESH
    if age <= 10 * period:
        return FRESHNESS_STALE
    return FRESHNESS_EXPIRED


@dataclass(frozen=True, slots=True)
class Provenance:
    """Mandatory provenance block for every data-bearing response."""

    source_kind: str
    authority: str
    source_id: str
    as_of: datetime | None
    display_label: str
    verification_id: str | None = None


def build_provenance(
    *,
    source_kind: str,
    authority: str,
    source_id: str,
    as_of: datetime | None,
    verification_id: str | None = None,
) -> Provenance:
    """Construct a provenance block, enforcing the active-vocabulary guard.

    Raises V2Error(VALIDATION_FAILED) for any authority outside the active
    set — including the reserved `historical:imported`.
    """
    if authority not in ACTIVE_AUTHORITY_VALUES:
        raise V2Error(
            code=V2ErrorCode.VALIDATION_FAILED,
            detail="Authority value not active in BE-2",
            status_code=500,
        )
    if as_of is not None:
        require_utc(as_of, boundary="as_of")
    return Provenance(
        source_kind=source_kind,
        authority=authority,
        source_id=source_id,
        as_of=as_of,
        display_label=AUTHORITY_DISPLAY_LABELS[authority],
        verification_id=verification_id,
    )


def map_v1_source_marker(marker: str | None) -> tuple[str, str, str]:
    """Map a V1 `candles.source` marker → (source_id, kind, authority).

    Unrecognized markers surface as unknown — never guessed, never
    auto-registered (plan C.4).
    """
    if marker == "live:simulated":
        return ("sim.local", "simulator", AUTHORITY_LIVE_SIMULATED)
    if marker == "seed:synthetic":
        return ("seed.local", "seed", AUTHORITY_SEED_SYNTHETIC)
    return ("unregistered", "reserved", AUTHORITY_UNKNOWN)
