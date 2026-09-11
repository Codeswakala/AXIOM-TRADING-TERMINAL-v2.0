"""V2 BE-8 simulator + ledger engine tests — BO-V2-BE-8-001 T-6/T-10/T-11.

ANNEX-P hand-computed values (docs/evidence/V2_BE-8_ANNEX_P_WORKED_SAMPLE.md)
asserted against independent test-local literals; determinism x3; cost
purity; typed seam; content re-verification; money law.
Socket guard on every test.
"""

from __future__ import annotations

import json
import socket
from decimal import Decimal

import pytest

from app.v2.paper_trading.contracts import (
    COST_UNITS_V1,
    FILL_CLASSES,
    PAPER_DISCLAIMER,
    PaperOrderIntent,
    PaperRefused,
)
from app.v2.paper_trading.ledger import (
    derive_balance,
    derive_cash,
    derive_positions,
    derive_realized_pnl,
    presentation_round,
    reconcile,
)
from app.v2.paper_trading.simulator import (
    SIMULATOR_VERSION,
    apply_costs,
    run_simulation,
    snapshot_content_hash,
)


@pytest.fixture(autouse=True)
def _socket_guard(monkeypatch):
    def _deny(*_a, **_k):
        raise AssertionError("network attempt during BE-8 test")

    monkeypatch.setattr(socket, "getaddrinfo", _deny)
    monkeypatch.setattr(socket, "create_connection", _deny)


# --- ANNEX-P pins (independent literals; the doc is the law) --------------------

ANNEX_CLOSES = ["100", "99", "97", "96", "99", "102", "104", "103", "101",
                "100"]
ANNEX_COSTS = {
    "spread": {"value": "0.10", "unit": "price", "citation": "band-declared"},
    "commission": {"value": "0.05", "unit": "price",
                   "citation": "band-declared"},
    "slippage": {"value": "0", "unit": "price", "citation": "band-declared"},
}


def _bars(liquidity: str = "2") -> list[dict]:
    out = []
    for i, close in enumerate(ANNEX_CLOSES):
        c = Decimal(close)
        out.append({"open_time": f"2026-09-01T{i:02d}:00:00+00:00",
                    "open": str(c), "high": str(c + 1), "low": str(c - 1),
                    "close": str(c), "liquidity": liquidity})
    return out


def _intent(order_type: str = "limit", quantity: str = "5",
            limit_price: str | None = "97.5") -> PaperOrderIntent:
    return PaperOrderIntent(
        intent_id="annex-p", account_id="acct-1",
        instrument_id="forex.eurusd", side="buy", order_type=order_type,
        quantity=Decimal(quantity),
        limit_price=Decimal(limit_price) if limit_price else None,
        snapshot_ref="snap-annex-p", window_start="2026-09-01T00:00:00+00:00",
        window_end="2026-09-01T10:00:00+00:00", cost_model=ANNEX_COSTS)


def _run(intent: PaperOrderIntent, bars: list[dict]) -> dict:
    return run_simulation(
        intent, bars,
        stored_content_hash=snapshot_content_hash(bars, intent.snapshot_ref))


# --- ANNEX-P Case A: limit buy partial ------------------------------------------


def test_annex_p_case_a_fill_count_and_prices():
    result = _run(_intent(), _bars())
    assert len(result["fills"]) == 2
    for f in result["fills"]:
        assert f["quantity"] == "2"
        assert f["raw_price"] == "97.5"
        assert f["effective_price"] == "97.65"  # 97.5 + 0.10 + 0.05


def test_annex_p_case_a_partial_and_remainder():
    result = _run(_intent(), _bars())
    assert result["outcome"] == "partially_filled"
    assert Decimal(result["unfilled_quantity"]) == Decimal("1")


def test_annex_p_case_b_market_first_close():
    result = _run(_intent(order_type="market", quantity="1",
                          limit_price=None), _bars())
    assert result["outcome"] == "filled"
    assert len(result["fills"]) == 1
    assert result["fills"][0]["raw_price"] == "100"
    assert result["fills"][0]["effective_price"] == "100.15"


def test_annex_p_ledger_derivation_exact():
    """ANNEX-P §2 account numbers: cash 9609.40, equity 10009.40,
    unrealized 9.40, margin 200/9809.40 — all hand-computed."""
    result = _run(_intent(), _bars())
    fills = [{"instrument_id": "forex.eurusd", "side": "buy",
              "quantity": f["quantity"],
              "effective_price": f["effective_price"]}
             for f in result["fills"]]
    balance = derive_balance(
        initial_balance=Decimal("10000"), fills=fills,
        marks={"forex.eurusd": Decimal("100")},
        margin_params={"margin_rate": "0.5"})
    assert Decimal(balance["cash"]) == Decimal("9609.40")
    assert Decimal(balance["equity"]) == Decimal("10009.40")
    assert Decimal(balance["unrealized_pnl"]) == Decimal("9.40")
    assert Decimal(balance["realized_pnl"]) == Decimal("0")
    assert Decimal(balance["margin_used"]) == Decimal("200")
    assert Decimal(balance["margin_available"]) == Decimal("9809.40")
    assert balance["positions"] == {"forex.eurusd": "4"}


def test_deterministic_x3_byte_identical():
    """T-10: replay contract x3 (the 0047-era F-2 lesson, designed in)."""
    s1 = json.dumps(_run(_intent(), _bars())["fills"], sort_keys=True)
    s2 = json.dumps(_run(_intent(), _bars())["fills"], sort_keys=True)
    s3 = json.dumps(_run(_intent(), _bars())["fills"], sort_keys=True)
    assert s1 == s2 == s3


def test_fill_class_single_value_on_every_fill():
    result = _run(_intent(), _bars())
    assert FILL_CLASSES == ("paper_simulated",)
    for f in result["fills"]:
        assert f["fill_class"] == "paper_simulated"
    assert result["disclaimer"] == PAPER_DISCLAIMER


def test_snapshot_content_mismatch_typed_refusal():
    """S4.1/G-5 law: tamper => typed refusal, never silent inclusion."""
    bars = _bars()
    good_hash = snapshot_content_hash(bars, "snap-annex-p")
    bars[3]["close"] = "50"  # tamper after hashing
    with pytest.raises(PaperRefused) as exc:
        run_simulation(_intent(), bars, stored_content_hash=good_hash)
    assert exc.value.refusal_class == "paper.snapshot.content_mismatch"


def test_untyped_seam_refused():
    """S6.1: the seam accepts PaperOrderIntent ONLY."""
    with pytest.raises(PaperRefused) as exc:
        run_simulation({"side": "buy"}, _bars(), stored_content_hash="x")
    assert exc.value.refusal_class == "paper.seam.untyped"


def test_cost_application_pure_and_sided():
    buy = apply_costs(Decimal("100"), "buy", ANNEX_COSTS)
    sell = apply_costs(Decimal("100"), "sell", ANNEX_COSTS)
    assert buy == Decimal("100.15")
    assert sell == Decimal("99.85")


def test_cost_unknown_unit_typed():
    """CR-V2-BE-7-001 vocabulary law carried: unknown unit refused typed."""
    bad = dict(ANNEX_COSTS)
    bad["spread"] = {"value": "0.1", "unit": "bogus", "citation": "x"}
    with pytest.raises(PaperRefused) as exc:
        apply_costs(Decimal("100"), "buy", bad)
    assert exc.value.refusal_class == "paper.cost_unit.unknown"
    assert COST_UNITS_V1 == ("price", "fraction")


def test_expired_when_never_touched():
    result = _run(_intent(limit_price="50"), _bars())
    assert result["outcome"] == "expired"
    assert result["fills"] == []


def test_realized_pnl_average_cost():
    """S5/A-3: buy 2 @ 100, sell 1 @ 110 => realized +10."""
    fills = [
        {"instrument_id": "x", "side": "buy", "quantity": "2",
         "effective_price": "100"},
        {"instrument_id": "x", "side": "sell", "quantity": "1",
         "effective_price": "110"},
    ]
    assert derive_realized_pnl(fills) == Decimal("10")
    assert derive_positions(fills) == {"x": Decimal("1")}
    assert derive_cash(Decimal("1000"), fills) == Decimal("910")


def test_reconcile_content_based_and_alarm():
    """T-12: PGF-012 content comparison; discrepant typed, not corrected."""
    balance = {"positions": {"x": "1"}, "cash": "910", "equity": "1010",
               "margin_used": "50", "margin_available": "960",
               "unrealized_pnl": "0", "realized_pnl": "10"}
    ok, items = reconcile(snapshot=balance, recomputed=dict(balance))
    assert (ok, items) == ("consistent", [])
    tampered = dict(balance)
    tampered["cash"] = "999"
    outcome, discrepancies = reconcile(snapshot=tampered,
                                       recomputed=balance)
    assert outcome == "discrepant"
    assert discrepancies[0]["field"] == "cash"


def test_money_law_decimal_and_presentation_rounding():
    """T-11: TEXT-decimal internal precision; rounding presentation-only."""
    v = Decimal("9609.4000000")
    assert presentation_round(v) == "9609.40"
    assert presentation_round(Decimal("0.125")) == "0.12"  # half-even
    assert str(Decimal("97.5") + Decimal("0.15")) == "97.65"  # no float drift


def test_simulator_version_pinned():
    assert SIMULATOR_VERSION == "pxs-1.0.0"
    result = _run(_intent(order_type="market", quantity="1",
                          limit_price=None), _bars())
    assert result["engine_versions"]["paper_execution_simulator"] == "pxs-1.0.0"
    assert result["engine_versions"]["paper_risk_gateway"] == "prg-1.0.0"
    assert len(result["engine_versions_hash"]) == 64
