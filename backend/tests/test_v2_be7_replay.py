"""V2 BE-7 U-2 tests — BO-V2-BE-7-001 T-9 (leakage G-1…G-5; determinism;
annex values; cost purity). Fail-first for the engine unit.

The ANNEX-R fixtures ARE the worked-sample replay annex: 10 pinned bars,
pinned threshold strategy, pinned cost model with citations, hand-computed
expected fills/summary (comments show the arithmetic).
"""

from __future__ import annotations

import json
import socket
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

from app.v2.research_jobs.contracts import (
    CONSTRUCTIBLE_RESULT_CLASSES,
    RESULT_CLASS_TAXONOMY,
    RJ_DATA_CLASSES,
    ResultClassRefused,
    require_constructible_result_class,
)
from app.v2.research_jobs.leakage import (
    LeakageRefused,
    ReplayWindow,
    content_hash,
    filter_bars_g1,
    validate_decision_ordering_g4,
    validate_horizon_g3,
    verify_content_g5,
)
from app.v2.research_jobs.replay import (
    apply_costs,
    engine_versions_hash,
    run_replay,
)

UTC = timezone.utc
T0 = datetime(2026, 9, 1, tzinfo=UTC)


@pytest.fixture(autouse=True)
def _socket_guard(monkeypatch):
    def _deny(*_a, **_k):
        raise AssertionError("network attempt during BE-7 test")

    monkeypatch.setattr(socket, "getaddrinfo", _deny)
    monkeypatch.setattr(socket, "create_connection", _deny)


def _bar(i: int, close: str) -> dict:
    px = Decimal(close)
    return {"open_time": T0 + timedelta(minutes=15 * i),
            "open": px, "high": px + Decimal("0.5"),
            "low": px - Decimal("0.5"), "close": px, "volume": 100}


# =============================================================================
# WORKED-SAMPLE REPLAY ANNEX "ANNEX-R" — pinned inputs
#   bars (close): 100, 99, 97, 96, 99, 102, 104, 103, 101, 100   (10 bars)
#   strategy: threshold — buy_below=97.5, sell_above=103.5, unit_qty=1,
#             initial_cash=10000
#   cost model: spread 0.10 price · commission 0.05 price · slippage 0.0 price
#               (citations: band-declared, unit price — plan Part 4)
#
# Hand computation:
#   buys  at bars close 97 and 96 (close < 97.5):
#     effective = close + 0.10 + 0.05 = 97.15 and 96.15
#   sell  at bar close 104 (close > 103.5):
#     effective = 104 - 0.15 = 103.85
#   fills = 3; final position = 1 (+1 +1 -1)
#   cash  = 10000 - 97.15 - 96.15 + 103.85 = 9910.55
#   final mark = 100 → equity = 9910.55 + 1×100 = 10010.55
# =============================================================================

ANNEX_CLOSES = ["100", "99", "97", "96", "99", "102", "104", "103", "101", "100"]
ANNEX_BARS = [_bar(i, c) for i, c in enumerate(ANNEX_CLOSES)]
ANNEX_WINDOW = ReplayWindow(
    window_start=T0, window_end=T0 + timedelta(minutes=15 * 9),
    as_of=T0 + timedelta(minutes=15 * 9))
ANNEX_PARAMS = {"buy_below": "97.5", "sell_above": "103.5",
                "unit_qty": "1", "initial_cash": "10000"}
ANNEX_COSTS = {
    "spread": {"value": "0.10", "unit": "price",
               "citation": "band-declared: fixed synthetic spread"},
    "commission": {"value": "0.05", "unit": "price",
                   "citation": "band-declared: flat commission"},
    "slippage": {"value": "0", "unit": "price",
                 "citation": "band-declared: zero in annex scope"},
}
ANNEX_REFS = {"instrument": "annex.synthetic", "timeframe": "M15"}


def _annex_run():
    ch = content_hash(filter_bars_g1(ANNEX_BARS, ANNEX_WINDOW),
                      ANNEX_WINDOW, ANNEX_REFS)
    return run_replay(bars=ANNEX_BARS, window=ANNEX_WINDOW,
                      strategy_rule="threshold", parameters=ANNEX_PARAMS,
                      cost_model=ANNEX_COSTS, stored_content_hash=ch,
                      series_refs=ANNEX_REFS)


# --- Annex correctness (hand-computed values) ----------------------------------


def test_annex_fill_count_and_sides() -> None:
    r = _annex_run()
    assert [f["side"] for f in r.fills] == ["buy", "buy", "sell"]


def test_annex_effective_prices_exact() -> None:
    r = _annex_run()
    assert [f["effective_price"] for f in r.fills] == ["97.15", "96.15", "103.85"]


def test_annex_summary_exact() -> None:
    r = _annex_run()
    assert r.summary["final_position"] == "1"
    assert r.summary["final_cash"] == "9910.55"
    assert r.summary["final_equity"] == "10010.55"
    assert r.summary["fills"] == 3
    assert r.summary["bars_replayed"] == 10
    assert "NOT live or future performance" in r.summary["performance_disclaimer"]


def test_annex_deterministic_byte_identical() -> None:
    # CR-V2-BE-7-001 F-2: BO T-9 pins retry x3 byte-identical.
    s1 = json.dumps(_annex_run().summary, sort_keys=True)
    s2 = json.dumps(_annex_run().summary, sort_keys=True)
    s3 = json.dumps(_annex_run().summary, sort_keys=True)
    assert s1 == s2 == s3


# --- G-1: as-of cutoff ------------------------------------------------------------


def test_g1_future_bar_excluded_and_summary_unchanged() -> None:
    """Exit item i, G-1: plant a bar after as_of; it must be absent from
    inputs AND the summary must equal the un-planted run."""
    planted = ANNEX_BARS + [_bar(10, "50")]  # would trigger a huge buy
    base = _annex_run().summary
    ch = content_hash(filter_bars_g1(planted, ANNEX_WINDOW),
                      ANNEX_WINDOW, ANNEX_REFS)
    r = run_replay(bars=planted, window=ANNEX_WINDOW,
                   strategy_rule="threshold", parameters=ANNEX_PARAMS,
                   cost_model=ANNEX_COSTS, stored_content_hash=ch,
                   series_refs=ANNEX_REFS)
    assert r.summary == base  # the planted bar had zero effect


def test_g1_window_rule_as_of_before_end_refused() -> None:
    with pytest.raises(LeakageRefused, match="G-1:window"):
        ReplayWindow(window_start=T0,
                     window_end=T0 + timedelta(hours=4),
                     as_of=T0 + timedelta(hours=2)).validate()


# --- G-2: decision-cursor ordering ---------------------------------------------------


def test_g2_cursor_never_sees_future() -> None:
    r = _annex_run()
    for entry in r.decision_ledger:
        for ref in entry["data_ref_ts"]:
            assert ref <= entry["decision_ts"]


# --- G-3: horizon/embargo -------------------------------------------------------------


def test_g3_horizon_past_embargo_refused() -> None:
    with pytest.raises(LeakageRefused, match="G-3:horizon"):
        validate_horizon_g3(
            label_horizon=timedelta(hours=4),
            embargo=timedelta(minutes=30),
            window=ANNEX_WINDOW)  # window is 2h15m long → no legal decision


def test_g3_legal_horizon_passes() -> None:
    validate_horizon_g3(label_horizon=timedelta(minutes=15),
                        embargo=timedelta(minutes=15), window=ANNEX_WINDOW)


# --- G-4: decision-vs-data ordering ----------------------------------------------------


def test_g4_corrupted_ledger_refused() -> None:
    bad = [{"decision_ts": T0,
            "data_ref_ts": [T0 + timedelta(minutes=15)]}]  # data AFTER decision
    with pytest.raises(LeakageRefused, match="G-4:ordering"):
        validate_decision_ordering_g4(bad)


# --- G-5: content immutability ----------------------------------------------------------


def test_g5_tampered_content_refused() -> None:
    with pytest.raises(LeakageRefused, match="G-5:content"):
        verify_content_g5(stored_hash="0" * 64, recomputed_hash="1" * 64)


def test_g5_replay_refuses_on_tamper() -> None:
    tampered = [dict(b) for b in ANNEX_BARS]
    tampered[3]["close"] = Decimal("1")  # post-registration tamper
    good_hash = content_hash(filter_bars_g1(ANNEX_BARS, ANNEX_WINDOW),
                             ANNEX_WINDOW, ANNEX_REFS)
    with pytest.raises(LeakageRefused, match="G-5:content"):
        run_replay(bars=tampered, window=ANNEX_WINDOW,
                   strategy_rule="threshold", parameters=ANNEX_PARAMS,
                   cost_model=ANNEX_COSTS, stored_content_hash=good_hash,
                   series_refs=ANNEX_REFS)


# --- Cost purity + determinism misc -------------------------------------------------------


def test_cost_application_pure_and_sided() -> None:
    cm = ANNEX_COSTS
    assert apply_costs(Decimal("100"), "buy", cm) == Decimal("100.15")
    assert apply_costs(Decimal("100"), "sell", cm) == Decimal("99.85")
    # fraction unit
    cm2 = {"spread": {"value": "0.001", "unit": "fraction", "citation": "x"},
           "commission": {"value": "0", "unit": "price", "citation": "x"},
           "slippage": {"value": "0", "unit": "price", "citation": "x"}}
    assert apply_costs(Decimal("100"), "buy", cm2) == Decimal("100.1")


def test_anchor_inputs_hash_sensitivity() -> None:
    assembled = filter_bars_g1(ANNEX_BARS, ANNEX_WINDOW)
    h1 = content_hash(assembled, ANNEX_WINDOW, ANNEX_REFS)
    changed = [dict(b) for b in assembled]
    changed[0]["close"] = Decimal("100.0001")
    assert content_hash(changed, ANNEX_WINDOW, ANNEX_REFS) != h1


def test_engine_versions_hash_canonical() -> None:
    import hashlib

    from app.v2.research_jobs.replay import ENGINE_VERSIONS

    expected = hashlib.sha256(json.dumps(
        ENGINE_VERSIONS, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    assert engine_versions_hash() == expected


# --- P-9: result-class law -----------------------------------------------------------------


def test_result_class_taxonomy_and_refusals() -> None:
    assert RESULT_CLASS_TAXONOMY == ("backtest", "simulation", "paper", "live")
    assert CONSTRUCTIBLE_RESULT_CLASSES == ("backtest", "simulation")
    assert require_constructible_result_class("backtest") == "backtest"
    assert require_constructible_result_class("simulation") == "simulation"
    for banned in ("paper", "live", "shadow"):
        with pytest.raises(ResultClassRefused):
            require_constructible_result_class(banned)


def test_taxonomy_shared_with_lineage() -> None:
    from app.v2.research_governance.contracts import DATA_CLASSES

    assert RJ_DATA_CLASSES == DATA_CLASSES  # no fork
