"""BE-5 typed contracts — vocabularies and decision-outcome shape.

Every CHECK vocabulary in migrations 0044/0045 mirrors a constant here
(single source, asserted equal by test). No execution vocabulary exists
in this module by construction (BG posture; forbidden-marker law).
"""

from __future__ import annotations

from dataclasses import dataclass, field

# --- 0044 governance-record vocabularies (BO T-2) ----------------------------
ELIGIBILITY_STATUSES = ("unevaluated", "eligible", "ineligible", "expired")
CALIBRATION_STATUSES = ("unevaluated", "calibrated", "miscalibrated", "stale")
FRESHNESS_STATUSES = ("fresh", "stale", "expired", "unknown")
ECONOMIC_STATUSES = ("unevaluated", "viable", "unviable")
STATISTICAL_STATUSES = ("unevaluated", "significant", "not_significant")

# Promotion ladder — order is the ladder; skipping is refused.
PROMOTION_LADDER = ("research", "shadow", "champion", "challenger", "retired")
DEPLOYMENT_CLASSES = PROMOTION_LADDER

# §0.2 data-honesty taxonomy (BO T-2; first-landing restriction in writers)
DATA_CLASSES = (
    "synthetic", "simulated", "historical_real", "live",
    "stale_cached", "unavailable",
)
FIRST_LANDING_DATA_CLASSES = ("synthetic", "simulated")

# --- 0044 lifecycle-event vocabulary -----------------------------------------
LIFECYCLE_EVENT_TYPES = (
    "registered", "eligibility_evaluated", "calibration_evaluated",
    "freshness_evaluated", "economic_evaluated", "statistical_evaluated",
    "promoted", "demoted", "refused", "rolled_back", "retired",
)

# --- 0045 signal vocabularies (BO T-6) ----------------------------------------
SIGNAL_FAMILIES = ("structural", "predictive")
SIGNAL_STATES = ("emitted", "withheld", "expired", "refused")
SIGNAL_EVENT_TYPES = ("emitted", "withheld", "refused", "expired")


@dataclass(frozen=True)
class DecisionOutcome:
    """Outcome of one pure decision function (BO T-7).

    ``citation`` names the governing 07_ML_SPEC section; ``thresholds``
    carries the V1-config-cited constants applied; ``reasons`` is the
    typed refusal basis (empty on pass). The whole outcome lands in
    ``decision_basis`` on the lifecycle event — report existence is
    necessary, never sufficient; this object is the sufficiency record.
    """

    contract: str
    status: str
    citation: str
    thresholds: dict = field(default_factory=dict)
    reasons: list = field(default_factory=list)
    inputs_ref: dict = field(default_factory=dict)

    def as_decision_basis(self) -> dict:
        return {
            "contract": self.contract,
            "status": self.status,
            "spec_citation": self.citation,
            "thresholds": self.thresholds,
            "reasons": self.reasons,
            "inputs_ref": self.inputs_ref,
        }
