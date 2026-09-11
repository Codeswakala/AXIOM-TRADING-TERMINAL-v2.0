"""BE-6 typed contracts — the risk-metric contract and vocabularies.

Every metric output carries the FULL contract (REQ-1.3): method,
method_citation, inputs, value, uncertainty, limitations, time_basis,
insufficient. A metric that cannot be honestly computed returns a typed
insufficient result — never a fabricated number.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.v2.research_governance.contracts import DATA_CLASSES

# Single taxonomy — shared with BE-5, no fork (REQ-1.7).
PR_DATA_CLASSES = DATA_CLASSES
PR_FIRST_LANDING_DATA_CLASSES = ("synthetic", "simulated")

# Single-value vocabularies (band exclusions made structural — P-6).
PORTFOLIO_BASES = ("hypothetical",)
BASIS_LABELS = ("hypothetical-research",)

REPORT_STATUSES = ("available", "degraded", "unavailable", "stale",
                   "unknown", "denied")

METRIC_CONTRACT_FIELDS = (
    "metric", "method", "method_citation", "inputs", "value",
    "uncertainty", "limitations", "time_basis", "insufficient",
)

WEIGHT_SUM_TOLERANCE = 1e-9


@dataclass(frozen=True)
class MetricResult:
    """One metric outcome carrying the full REQ-1.3 contract."""

    metric: str
    method: str
    method_citation: str
    inputs: dict
    value: dict | None            # None WHEN insufficient — never fabricated
    uncertainty: dict
    limitations: dict
    time_basis: dict
    insufficient: bool = False

    def as_dict(self) -> dict:
        return {
            "metric": self.metric,
            "method": self.method,
            "method_citation": self.method_citation,
            "inputs": self.inputs,
            "value": self.value,
            "uncertainty": self.uncertainty,
            "limitations": self.limitations,
            "time_basis": self.time_basis,
            "insufficient": self.insufficient,
        }


def insufficient_result(metric: str, method: str, citation: str,
                        required: dict, available: dict) -> MetricResult:
    """Typed insufficiency — the honest non-answer (REQ-1.3)."""
    return MetricResult(
        metric=metric, method=method, method_citation=citation,
        inputs=available, value=None,
        uncertainty={"basis": "not-computed"},
        limitations={"outcome": "insufficient_data",
                     **{f"required_{k}": v for k, v in required.items()},
                     **{f"available_{k}": v for k, v in available.items()}},
        time_basis={}, insufficient=True,
    )


def validate_allocations(allocations: list[dict]) -> tuple[bool, list]:
    """Long-only v1 contract: weights each >= 0, sum to 1.0 ± tolerance,
    instrument ids non-empty, no duplicates. Returns (ok, typed reasons)."""
    reasons: list = []
    if not allocations:
        return False, [{"failing": "allocations", "value": "empty"}]
    seen: set[str] = set()
    total = 0.0
    for entry in allocations:
        iid = entry.get("instrument_id")
        weight = entry.get("weight")
        if not iid:
            reasons.append({"failing": "instrument_id", "value": iid})
            continue
        if iid in seen:
            reasons.append({"failing": "duplicate_instrument", "value": iid})
        seen.add(iid)
        if weight is None or float(weight) < 0:
            reasons.append({"failing": "negative_or_missing_weight",
                            "instrument_id": iid, "value": weight,
                            "note": "long-only v1 scope"})
            continue
        total += float(weight)
    if abs(total - 1.0) > WEIGHT_SUM_TOLERANCE:
        reasons.append({"failing": "weight_sum", "value": total,
                        "required": f"1.0 ± {WEIGHT_SUM_TOLERANCE}"})
    return (not reasons), reasons


def validate_assumptions(assumptions: dict) -> tuple[bool, list]:
    """Assumption-visibility law: never silently empty (plan §1.2)."""
    if assumptions:
        return True, []
    return False, [{"failing": "assumptions",
                    "required": "declared assumptions or"
                                " {'none_beyond_defaults': true}"}]
