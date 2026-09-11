"""BE-11 typed contracts (BO D-1; DR Q3 vocabularies; wording law).

Closed enums — STATE NOUNS ONLY. Gateway decisions are RECORDS OF STATE
with reason codes, never executions (R-3.3): no broker-order verb may
appear in any vocabulary member, field name, or DDL identifier
(D-B11-NAMING + D-B10-SCAN, both scan-armed).

Seed-slot law (BO §0, fail-closed posture): drift tolerances and the
generation-staleness threshold are SEEDS, not constants. They are read
at compute time from the seeded drift-run configuration rows landed by a
future operator overlay migration; until seeded, the drift arm answers
`uncomputable` (refuse-to-compare) and intent GENERATION refuses typed
`basis_staleness_threshold_unseeded`. Nothing in this module carries a
default value for either — absence IS the shipped state.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final

# Gateway decisions (closed; R-3.3).
GATEWAY_DECISIONS: Final = (
    "accept_with_notes",
    "deferred",
    "refused_under_policy",
)

# Refusal reasons (closed sub-enum; BO D-1 set exactly).
REFUSAL_REASONS: Final = (
    "basis_unavailable",
    "basis_stale",
    "reference_price_uncited",
    "duplicate_intent",
    "basis_staleness_threshold_unseeded",
)

# Drift verdicts (closed; R-3.4).
DRIFT_VERDICTS: Final = (
    "within_tolerance",
    "drift_minor",
    "drift_major",
    "uncomputable",
)

# Staleness triple (D-B02-COMP law carried verbatim).
STALENESS_STATES: Final = ("fresh", "stale", "unavailable")

ENGINE_VERSION: Final = "pbr-1.0.0"

# 2dp decimal quantization law (mirrors D-B10-2DP): presentation-boundary
# rounding only; internal math full-precision Decimal.
PRESENTATION_DECIMALS: Final = 2

# The citation shape D-B11-CITE demands on every intent (all four keys).
CITATION_KEYS: Final = ("value", "currency_unit", "cited_source",
                        "cited_at")

_DOMAIN = "v2.paper_bridge"


@dataclass(frozen=True)
class CitedReferencePrice:
    """Operator-cited price — INPUT, never platform truth (D-B11-CITE)."""

    value: str
    currency_unit: str
    cited_source: str
    cited_at: str


@dataclass(frozen=True)
class BridgeBasis:
    """The pinned basis (consistency ARM): read ONCE at entry."""

    sync_run_id: str
    balance: str
    margin_used: str
    margin_available: str
    unrealized_pl: str
    currency: str
    basis_age_hours: float
    staleness: str          # STALENESS_STATES member
    positions_present: bool


@dataclass(frozen=True)
class GatewayRecord:
    """A record of STATE with reason codes — never an execution."""

    decision: str            # GATEWAY_DECISIONS member
    reasons: tuple = ()
    notes: tuple = ()        # e.g. instrument-exposure check deferred
    digest: str = ""
    basis_sync_run_id: str = ""
    engine_versions: dict = field(default_factory=dict)


class BridgeRefused(Exception):
    """Typed refusal; reason from the closed sub-enum; never improvised."""

    def __init__(self, reason: str, details: list) -> None:
        assert reason in REFUSAL_REASONS
        self.reason = reason
        self.details = details
        super().__init__(f"{reason}: {details}")
