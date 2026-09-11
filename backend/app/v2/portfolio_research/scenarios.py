"""BE-6 scenario/stress contracts — declared deterministic shocks (REQ-1.4).

Result = re-valued portfolio delta given the declared shock. Shock realism
is NOT claimed — the limitation field is mandatory on every result.
"""

from __future__ import annotations

from app.v2.portfolio_research.contracts import MetricResult

_SPECREF = "AXIOM-V2-BE-6-DA-PLAN-001 Part 2 (scenario/stress)"


def apply_scenarios(
    allocations: list[dict],
    market_classes: dict[str, str],
    scenarios: list[dict],
) -> list[MetricResult]:
    """Each scenario: {"name": str, "shocks": {market_class: pct_shock}}.
    Delta = Σ weight_i × shock(class_i); unshocked classes contribute 0.
    Typed-empty allowed: [] in ⇒ [] out (the writer records the reason)."""
    results: list[MetricResult] = []
    for scenario in scenarios:
        name = scenario.get("name", "unnamed")
        shocks = scenario.get("shocks", {})
        delta = 0.0
        applied: dict[str, float] = {}
        for a in allocations:
            cls = market_classes.get(a["instrument_id"], "unknown")
            shock = float(shocks.get(cls, 0.0))
            contribution = float(a["weight"]) * shock
            delta += contribution
            if shock != 0.0:
                applied[a["instrument_id"]] = contribution
        results.append(MetricResult(
            metric="scenario", method="declared-deterministic-shock",
            method_citation=f"delta = Σ w_i × shock(class_i) ({_SPECREF})",
            inputs={"scenario": name, "shocks": shocks,
                    "allocation_count": len(allocations)},
            value={"scenario": name, "portfolio_delta": delta,
                   "contributions": applied},
            uncertainty={"basis": "deterministic given the declared shock"},
            limitations={"realism": "shock realism NOT claimed — the"
                                    " scenario is a declared hypothetical"
                                    " input, not a forecast"},
            time_basis={"basis": "instantaneous shock on declared"
                                 " allocations"},
        ))
    return results
