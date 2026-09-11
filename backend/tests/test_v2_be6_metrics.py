"""V2 BE-6 U-2 metric tests — BO-V2-BE-6-001 T-8/T-11 (fail-first).

Per-metric: >=1 correctness test against hand-computed values (the
worked-sample annex fixtures) + typed-insufficient tests. Pure functions;
no DB, no network, no clock. Expected values below are computed BY HAND
in the comments — the same values ship in the worked-sample annex (P-7).
"""

from __future__ import annotations

import math

import pytest

from app.v2.portfolio_research.contracts import (
    METRIC_CONTRACT_FIELDS,
    MetricResult,
)
from app.v2.portfolio_research.metrics import (
    CONFIDENCE_LEVEL,
    compute_concentration,
    compute_drawdown,
    compute_exposures,
    compute_factor_shares,
    compute_var,
    compute_volatility,
)
from app.v2.portfolio_research.scenarios import apply_scenarios
from app.v2.research_governance.contracts import DATA_CLASSES  # taxonomy reuse

# --- Worked-sample fixtures (annex-pinned; hand-computable) -------------------

# Portfolio W: three instruments, long-only, weights sum to 1.
ALLOCATIONS = [
    {"instrument_id": "forex.eurusd", "weight": 0.5},
    {"instrument_id": "crypto.btcusd", "weight": 0.3},
    {"instrument_id": "metal.xauusd", "weight": 0.2},
]
MARKET_CLASSES = {
    "forex.eurusd": "forex", "crypto.btcusd": "crypto",
    "metal.xauusd": "metal",
}

# Deterministic portfolio value series V (10 points, hand-checkable):
VALUES = [100.0, 102.0, 101.0, 104.0, 103.0, 106.0, 102.0, 105.0, 107.0, 106.0]
# log returns r_i = ln(V_i / V_{i-1}), 9 observations.
RETURNS = [math.log(VALUES[i] / VALUES[i - 1]) for i in range(1, len(VALUES))]


def _contract_complete(m: MetricResult) -> bool:
    d = m.as_dict()
    return all(k in d for k in METRIC_CONTRACT_FIELDS)


# --- Exposures -----------------------------------------------------------------


def test_exposures_hand_values() -> None:
    m = compute_exposures(ALLOCATIONS)
    assert m.insufficient is False
    # gross = sum |w| = 1.0; net = sum w = 1.0 (long-only ⇒ equal)
    assert m.value["gross"] == pytest.approx(1.0)
    assert m.value["net"] == pytest.approx(1.0)
    assert m.value["per_instrument"]["forex.eurusd"] == pytest.approx(0.5)
    assert m.uncertainty == {"basis": "deterministic"}
    assert _contract_complete(m)
    assert m.method_citation


def test_exposures_insufficient_on_empty() -> None:
    m = compute_exposures([])
    assert m.insufficient is True
    assert m.value is None  # never fabricated


# --- Concentration (HHI + top-N) --------------------------------------------------


def test_concentration_hand_values() -> None:
    # HHI = 0.5² + 0.3² + 0.2² = 0.25 + 0.09 + 0.04 = 0.38
    # top-1 share = 0.5 ; top-2 share = 0.8
    m = compute_concentration(ALLOCATIONS, top_n=2)
    assert m.value["hhi"] == pytest.approx(0.38)
    assert m.value["top_n_share"] == pytest.approx(0.8)
    assert m.value["top_n"] == 2
    assert _contract_complete(m)


# --- Volatility (sample stdev of log returns; chi-square CI) ----------------------


def test_volatility_hand_values() -> None:
    n = len(RETURNS)
    mean = sum(RETURNS) / n
    var = sum((r - mean) ** 2 for r in RETURNS) / (n - 1)
    expected_sd = math.sqrt(var)
    m = compute_volatility(RETURNS)
    assert m.value["stdev"] == pytest.approx(expected_sd, rel=1e-12)
    assert m.value["observations"] == n
    # chi-square CI at the cited level brackets the point estimate
    lo, hi = m.uncertainty["interval"]
    assert lo < expected_sd < hi
    assert m.uncertainty["confidence"] == CONFIDENCE_LEVEL
    assert "chi-square" in m.method_citation.lower()
    assert _contract_complete(m)


def test_volatility_insufficient_below_two_returns() -> None:
    m = compute_volatility([0.01])
    assert m.insufficient is True
    assert m.value is None
    assert m.limitations["required_observations"] == 2


# --- Drawdown ---------------------------------------------------------------------


def test_drawdown_hand_values() -> None:
    # peaks: 100,102,102,104,104,106,106,106,107,107
    # troughs after peaks: worst is 102 after 106 → (102-106)/106 = -0.0377358…
    m = compute_drawdown(VALUES)
    assert m.value["max_drawdown"] == pytest.approx((102.0 - 106.0) / 106.0)
    assert m.value["peak_value"] == pytest.approx(106.0)
    assert m.value["trough_value"] == pytest.approx(102.0)
    assert "window-dependence" in str(m.limitations)
    assert _contract_complete(m)


def test_drawdown_insufficient_on_short_series() -> None:
    assert compute_drawdown([100.0]).insufficient is True


# --- VaR (historical AND parametric, reported separately) ---------------------------


def test_var_both_methods_reported_separately() -> None:
    result = compute_var(RETURNS, confidence=0.95)
    hist, para = result["historical"], result["parametric_normal"]
    assert isinstance(hist, MetricResult) and isinstance(para, MetricResult)
    # historical: empirical 5% quantile of returns (loss = -quantile)
    sorted_r = sorted(RETURNS)
    # index = floor(0.05 * 9) = 0 → worst return
    assert hist.value["var"] == pytest.approx(-sorted_r[0])
    # parametric: -(mean - z*sd), z(0.95) ≈ 1.6448536269514722
    n = len(RETURNS)
    mean = sum(RETURNS) / n
    sd = math.sqrt(sum((r - mean) ** 2 for r in RETURNS) / (n - 1))
    z = 1.6448536269514722
    assert para.value["var"] == pytest.approx(-(mean - z * sd), rel=1e-9)
    # never merged: two distinct contract objects, distinct methods
    assert hist.method != para.method
    assert "normal" in str(para.limitations).lower()  # assumption declared
    assert _contract_complete(hist) and _contract_complete(para)


def test_var_insufficient() -> None:
    result = compute_var([0.01, -0.02], confidence=0.95)
    assert result["historical"].insufficient is True  # < required obs
    assert result["parametric_normal"].insufficient is True


# --- Factor shares (grouping, not regression) ----------------------------------------


def test_factor_shares_hand_values() -> None:
    m = compute_factor_shares(ALLOCATIONS, MARKET_CLASSES)
    assert m.value["shares"] == {
        "forex": pytest.approx(0.5),
        "crypto": pytest.approx(0.3),
        "metal": pytest.approx(0.2),
    }
    assert "grouping" in m.method.lower()
    assert "not regression" in str(m.limitations).lower() or \
           "grouping, not regression" in m.method_citation.lower()
    assert _contract_complete(m)


def test_factor_shares_unknown_class_typed() -> None:
    m = compute_factor_shares([{"instrument_id": "x.y", "weight": 1.0}], {})
    assert m.value["shares"] == {"unknown": pytest.approx(1.0)}
    assert "unknown" in str(m.limitations)


# --- Scenarios ------------------------------------------------------------------------


def test_scenario_hand_values() -> None:
    # shock: forex -10%, crypto -30% → delta = 0.5*(-0.10) + 0.3*(-0.30)
    #        = -0.05 - 0.09 = -0.14 ; metal untouched
    shocks = [{"name": "risk-off", "shocks": {"forex": -0.10, "crypto": -0.30}}]
    results = apply_scenarios(ALLOCATIONS, MARKET_CLASSES, shocks)
    assert len(results) == 1
    s = results[0]
    assert s.value["portfolio_delta"] == pytest.approx(-0.14)
    assert s.value["scenario"] == "risk-off"
    assert "realism" in str(s.limitations).lower()  # mandatory limitation
    assert _contract_complete(s)


def test_scenarios_empty_typed() -> None:
    results = apply_scenarios(ALLOCATIONS, MARKET_CLASSES, [])
    assert results == []  # typed-empty allowed (writer records the reason)


# --- Determinism + construction bans ---------------------------------------------------


def test_byte_identical_recomputation() -> None:
    import json

    def run():
        out = {
            "expo": compute_exposures(ALLOCATIONS).as_dict(),
            "conc": compute_concentration(ALLOCATIONS, top_n=2).as_dict(),
            "vol": compute_volatility(RETURNS).as_dict(),
            "dd": compute_drawdown(VALUES).as_dict(),
            "var": {k: v.as_dict() for k, v in
                    compute_var(RETURNS, confidence=0.95).items()},
            "fac": compute_factor_shares(ALLOCATIONS, MARKET_CLASSES).as_dict(),
        }
        return json.dumps(out, sort_keys=True)

    assert run() == run()


def test_no_wallclock_randomness_or_recommendation_tokens() -> None:
    """T-11 construction-token scan: deterministic core is clock/random-free
    and the band contains no action vocabulary."""
    from pathlib import Path

    base = Path(__file__).resolve().parents[1] / "app/v2/portfolio_research"
    for f in base.glob("*.py"):
        text = f.read_text()
        for token in ("datetime.now(", "utcnow(", "time.time(", "random.",
                      "uuid4("):
            if f.name in ("api.py",):  # api layer may mint ids/timestamps
                break
            assert token not in text, f"{token} in {f.name}"
        for banned in ("recommendation", "rebalance", "hedge_now",
                       '"action"', "'action'"):
            assert banned not in text.lower(), f"{banned} in {f.name}"


def test_weights_validation_contract() -> None:
    from app.v2.portfolio_research.contracts import validate_allocations

    ok, reasons = validate_allocations(ALLOCATIONS)
    assert ok and reasons == []
    bad_sum, r1 = validate_allocations(
        [{"instrument_id": "a", "weight": 0.9}])
    assert not bad_sum and any("sum" in str(x) for x in r1)
    negative, r2 = validate_allocations(
        [{"instrument_id": "a", "weight": 1.5},
         {"instrument_id": "b", "weight": -0.5}])
    assert not negative and any("negative" in str(x) for x in r2)


def test_data_class_taxonomy_shared_with_be5() -> None:
    from app.v2.portfolio_research.contracts import PR_DATA_CLASSES

    assert PR_DATA_CLASSES == DATA_CLASSES  # single taxonomy, no fork
