"""V2 BE-6 worked-sample annex + boundary tests — BO-V2-BE-6-001 T-9/P-7.

The annex fixtures here are THE published worked sample: every expected
value is hand-computable from the pinned inputs; the ITRGA recomputes
independently (P-7). Plus boundary/edge coverage completing the plan
Part 5 budget.
"""

from __future__ import annotations

import json
import math
import socket

import pytest

from app.v2.portfolio_research.contracts import (
    BASIS_LABELS,
    METRIC_CONTRACT_FIELDS,
    PORTFOLIO_BASES,
    REPORT_STATUSES,
    WEIGHT_SUM_TOLERANCE,
    insufficient_result,
    validate_allocations,
)
from app.v2.portfolio_research.metrics import (
    CONFIDENCE_LEVEL,
    VAR_MIN_OBSERVATIONS,
    _norm_ppf,
    compute_concentration,
    compute_drawdown,
    compute_exposures,
    compute_factor_shares,
    compute_var,
    compute_volatility,
)
from app.v2.portfolio_research.scenarios import apply_scenarios


@pytest.fixture(autouse=True)
def _socket_guard(monkeypatch):
    def _deny(*_a, **_k):
        raise AssertionError("network attempt during BE-6 annex test")

    monkeypatch.setattr(socket, "getaddrinfo", _deny)
    monkeypatch.setattr(socket, "create_connection", _deny)


# =============================================================================
# WORKED-SAMPLE ANNEX (P-7) — Portfolio "ANNEX-A"
#
#   allocations: alpha 0.40 · beta 0.35 · gamma 0.25       (sum = 1.00)
#   classes:     alpha→forex · beta→crypto · gamma→metal
#   value series V = [100, 98, 103, 101, 99, 104, 102, 100, 105, 103]
#
# Hand-computed expected values (to the stated precision):
#   HHI      = 0.40² + 0.35² + 0.25² = 0.16 + 0.1225 + 0.0625 = 0.3450
#   top-2    = 0.40 + 0.35 = 0.7500
#   gross    = net = 1.0000
#   drawdown = worst peak-to-trough = (99-103)/103 = -0.03883495…
#   returns  = ln(V_i/V_{i-1}), 9 obs; stdev per the sample formula
#   VaR hist = -(worst return) at 95% (floor(0.05*9)=0 → order stat 1)
#   scenario "crypto-crash" {crypto: -0.5} → delta = 0.35 × -0.5 = -0.1750
# =============================================================================

ANNEX_ALLOC = [
    {"instrument_id": "alpha", "weight": 0.40},
    {"instrument_id": "beta", "weight": 0.35},
    {"instrument_id": "gamma", "weight": 0.25},
]
ANNEX_CLASSES = {"alpha": "forex", "beta": "crypto", "gamma": "metal"}
ANNEX_VALUES = [100.0, 98.0, 103.0, 101.0, 99.0, 104.0, 102.0, 100.0, 105.0, 103.0]
ANNEX_RETURNS = [math.log(ANNEX_VALUES[i] / ANNEX_VALUES[i - 1])
                 for i in range(1, len(ANNEX_VALUES))]


def test_annex_hhi_exact() -> None:
    m = compute_concentration(ANNEX_ALLOC, top_n=2)
    assert m.value["hhi"] == pytest.approx(0.3450, abs=1e-12)


def test_annex_top2_exact() -> None:
    m = compute_concentration(ANNEX_ALLOC, top_n=2)
    assert m.value["top_n_share"] == pytest.approx(0.7500, abs=1e-12)


def test_annex_exposures_exact() -> None:
    m = compute_exposures(ANNEX_ALLOC)
    assert m.value["gross"] == pytest.approx(1.0, abs=1e-12)
    assert m.value["net"] == pytest.approx(1.0, abs=1e-12)


def test_annex_drawdown_exact() -> None:
    m = compute_drawdown(ANNEX_VALUES)
    assert m.value["max_drawdown"] == pytest.approx((99.0 - 103.0) / 103.0,
                                                    abs=1e-12)


def test_annex_volatility_matches_hand_formula() -> None:
    n = len(ANNEX_RETURNS)
    mean = sum(ANNEX_RETURNS) / n
    sd = math.sqrt(sum((r - mean) ** 2 for r in ANNEX_RETURNS) / (n - 1))
    m = compute_volatility(ANNEX_RETURNS)
    assert m.value["stdev"] == pytest.approx(sd, rel=1e-12)


def test_annex_var_historical_order_statistic() -> None:
    result = compute_var(ANNEX_RETURNS, confidence=0.95)
    assert result["historical"].value["var"] == pytest.approx(
        -sorted(ANNEX_RETURNS)[0], rel=1e-12)


def test_annex_var_parametric_closed_form() -> None:
    n = len(ANNEX_RETURNS)
    mean = sum(ANNEX_RETURNS) / n
    sd = math.sqrt(sum((r - mean) ** 2 for r in ANNEX_RETURNS) / (n - 1))
    z = 1.6448536269514722
    result = compute_var(ANNEX_RETURNS, confidence=0.95)
    assert result["parametric_normal"].value["var"] == pytest.approx(
        -(mean - z * sd), rel=1e-9)


def test_annex_factor_shares_exact() -> None:
    m = compute_factor_shares(ANNEX_ALLOC, ANNEX_CLASSES)
    assert m.value["shares"] == {
        "forex": pytest.approx(0.40), "crypto": pytest.approx(0.35),
        "metal": pytest.approx(0.25)}


def test_annex_scenario_exact() -> None:
    results = apply_scenarios(
        ANNEX_ALLOC, ANNEX_CLASSES,
        [{"name": "crypto-crash", "shocks": {"crypto": -0.5}}])
    assert results[0].value["portfolio_delta"] == pytest.approx(-0.1750,
                                                                abs=1e-12)


def test_annex_full_bundle_deterministic_json() -> None:
    """The annex bundle serializes identically across runs — the exact
    property the ITRGA recomputation relies on."""
    def bundle() -> str:
        out = {
            "concentration": compute_concentration(ANNEX_ALLOC, top_n=2).as_dict(),
            "exposures": compute_exposures(ANNEX_ALLOC).as_dict(),
            "drawdown": compute_drawdown(ANNEX_VALUES).as_dict(),
            "volatility": compute_volatility(ANNEX_RETURNS).as_dict(),
            "var": {k: v.as_dict() for k, v in
                    compute_var(ANNEX_RETURNS, confidence=0.95).items()},
            "factors": compute_factor_shares(ANNEX_ALLOC, ANNEX_CLASSES).as_dict(),
            "scenario": [s.as_dict() for s in apply_scenarios(
                ANNEX_ALLOC, ANNEX_CLASSES,
                [{"name": "crypto-crash", "shocks": {"crypto": -0.5}}])],
        }
        return json.dumps(out, sort_keys=True)
    assert bundle() == bundle()


# --- boundary/edge coverage (plan Part 5 budget completion) ---------------------


def test_norm_ppf_reference_values() -> None:
    """Acklam approximation against reference quantiles (cited accuracy)."""
    assert _norm_ppf(0.975) == pytest.approx(1.959963985, abs=1e-6)
    assert _norm_ppf(0.95) == pytest.approx(1.644853627, abs=1e-6)
    assert _norm_ppf(0.5) == pytest.approx(0.0, abs=1e-9)
    assert _norm_ppf(0.05) == pytest.approx(-1.644853627, abs=1e-6)


def test_volatility_ci_widens_with_fewer_observations() -> None:
    short = compute_volatility(ANNEX_RETURNS[:4])
    full = compute_volatility(ANNEX_RETURNS)
    width_short = short.uncertainty["interval"][1] - short.uncertainty["interval"][0]
    width_full = full.uncertainty["interval"][1] - full.uncertainty["interval"][0]
    # relative widths: fewer observations ⇒ proportionally wider CI
    assert width_short / short.value["stdev"] > width_full / full.value["stdev"]


def test_var_minimum_observation_boundary() -> None:
    exactly_min = ANNEX_RETURNS[:VAR_MIN_OBSERVATIONS]
    result = compute_var(exactly_min, confidence=0.95)
    assert result["historical"].insufficient is False
    one_short = ANNEX_RETURNS[:VAR_MIN_OBSERVATIONS - 1]
    result = compute_var(one_short, confidence=0.95)
    assert result["historical"].insufficient is True


def test_weight_sum_tolerance_boundary() -> None:
    within = [{"instrument_id": "a", "weight": 1.0 + WEIGHT_SUM_TOLERANCE / 2}]
    ok, _ = validate_allocations(within)
    assert ok
    outside = [{"instrument_id": "a", "weight": 1.0 + WEIGHT_SUM_TOLERANCE * 10}]
    ok, reasons = validate_allocations(outside)
    assert not ok and any(x.get("failing") == "weight_sum" for x in reasons)


def test_duplicate_instrument_refused() -> None:
    ok, reasons = validate_allocations([
        {"instrument_id": "a", "weight": 0.5},
        {"instrument_id": "a", "weight": 0.5}])
    assert not ok
    assert any(x.get("failing") == "duplicate_instrument" for x in reasons)


def test_insufficient_result_contract_complete() -> None:
    r = insufficient_result("m", "meth", "cite", {"observations": 5},
                            {"observations": 1})
    d = r.as_dict()
    assert all(k in d for k in METRIC_CONTRACT_FIELDS)
    assert d["value"] is None and d["insufficient"] is True
    assert d["limitations"]["outcome"] == "insufficient_data"


def test_vocabulary_single_values_and_status_set() -> None:
    """P-6: the band exclusions are single-value vocabularies; the report
    status set is exactly the BE-1 six."""
    assert PORTFOLIO_BASES == ("hypothetical",)
    assert BASIS_LABELS == ("hypothetical-research",)
    assert set(REPORT_STATUSES) == {"available", "degraded", "unavailable",
                                    "stale", "unknown", "denied"}
    assert CONFIDENCE_LEVEL == 0.95  # the cited V1 config value
