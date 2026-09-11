"""BE-8 positions/balances/margin/P&L engine (design S5; BO T-11/T-12).

Pure derivation over the immutable fill ledger: positions = signed fill
sums; cash = initial - buys + sells; equity = cash + position x mark
(mark = last close OF THE PINNED SNAPSHOT — never a live read); realized
P&L average-cost (A-3); margin engine COMPUTES ONLY — the risk gateway
decides (Q5). Decimal end-to-end; TEXT-decimal storage; rounding at
presentation only (S5 money law). Reconciliation = genesis recompute +
content comparison (PGF-012); discrepant is a typed alarm, never
auto-corrected.
"""

from __future__ import annotations

import hashlib
import json
from decimal import Decimal

from app.v2.paper_trading.contracts import RISK_CONFIG_V1


def _canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


def derivation_hash(payload: dict) -> str:
    return hashlib.sha256(_canonical(payload).encode()).hexdigest()


def derive_positions(fills: list[dict]) -> dict[str, Decimal]:
    """instrument -> signed quantity (buy +, sell -)."""
    positions: dict[str, Decimal] = {}
    for f in fills:
        qty = Decimal(str(f["quantity"]))
        signed = qty if f["side"] == "buy" else -qty
        key = f["instrument_id"]
        positions[key] = positions.get(key, Decimal(0)) + signed
    return {k: v for k, v in positions.items() if v != 0}


def derive_cash(initial_balance: Decimal, fills: list[dict]) -> Decimal:
    cash = Decimal(str(initial_balance))
    for f in fills:
        qty = Decimal(str(f["quantity"]))
        px = Decimal(str(f["effective_price"]))
        if f["side"] == "buy":
            cash -= qty * px
        else:
            cash += qty * px
    return cash


def derive_realized_pnl(fills: list[dict]) -> Decimal:
    """Average-cost realized P&L (A-3), per instrument, chronological."""
    realized = Decimal(0)
    book: dict[str, dict] = {}
    for f in fills:
        key = f["instrument_id"]
        qty = Decimal(str(f["quantity"]))
        px = Decimal(str(f["effective_price"]))
        entry = book.setdefault(key, {"qty": Decimal(0), "cost": Decimal(0)})
        pos, cost = entry["qty"], entry["cost"]
        signed = qty if f["side"] == "buy" else -qty
        if pos == 0 or (pos > 0) == (signed > 0):
            entry["qty"] = pos + signed
            entry["cost"] = cost + signed * px
        else:
            closing = min(abs(signed), abs(pos))
            avg = cost / pos if pos != 0 else Decimal(0)
            direction = Decimal(1) if pos > 0 else Decimal(-1)
            realized += closing * (px - avg) * direction
            entry["qty"] = pos + signed
            entry["cost"] = avg * entry["qty"]
    return realized


def margin_used(positions: dict[str, Decimal], marks: dict[str, Decimal],
                margin_params: dict) -> Decimal:
    """Computes ONLY (Q5): sum |position notional| x margin_rate."""
    rate = Decimal(str(margin_params.get(
        "margin_rate", RISK_CONFIG_V1["margin_rate_default"])))
    total = Decimal(0)
    for instrument, qty in positions.items():
        mark = marks.get(instrument, Decimal(0))
        total += abs(qty * mark) * rate
    return total


def derive_balance(*, initial_balance: Decimal, fills: list[dict],
                   marks: dict[str, Decimal], margin_params: dict) -> dict:
    positions = derive_positions(fills)
    cash = derive_cash(initial_balance, fills)
    unrealized = Decimal(0)
    equity = cash
    book_cost: dict[str, Decimal] = {}
    for f in fills:
        key = f["instrument_id"]
        qty = Decimal(str(f["quantity"]))
        px = Decimal(str(f["effective_price"]))
        signed = qty if f["side"] == "buy" else -qty
        book_cost[key] = book_cost.get(key, Decimal(0)) + signed * px
    for instrument, qty in positions.items():
        mark = marks.get(instrument, Decimal(0))
        equity += qty * mark
        avg = (book_cost.get(instrument, Decimal(0)) / qty) if qty else Decimal(0)
        unrealized += qty * (mark - avg)
    used = margin_used(positions, marks, margin_params)
    return {
        "positions": {k: str(v) for k, v in positions.items()},
        "cash": str(cash),
        "equity": str(equity),
        "margin_used": str(used),
        "margin_available": str(equity - used),
        "unrealized_pnl": str(unrealized),
        "realized_pnl": str(derive_realized_pnl(fills)),
    }


def reconcile(*, snapshot: dict, recomputed: dict) -> tuple[str, list]:
    """Genesis recompute vs stored snapshot; content comparison (PGF-012).

    Returns (outcome, discrepancies). Never mutates anything.
    """
    discrepancies: list = []
    for field in ("cash", "equity", "margin_used", "margin_available",
                  "unrealized_pnl", "realized_pnl"):
        if Decimal(str(snapshot[field])) != Decimal(str(recomputed[field])):
            discrepancies.append({
                "field": field, "stored": str(snapshot[field]),
                "recomputed": str(recomputed[field])})
    if snapshot.get("positions") != recomputed.get("positions"):
        discrepancies.append({
            "field": "positions", "stored": snapshot.get("positions"),
            "recomputed": recomputed.get("positions")})
    return ("consistent" if not discrepancies else "discrepant",
            discrepancies)


def presentation_round(value: Decimal) -> str:
    """Rounding at presentation ONLY (half-even, 2 dp) — S5 money law."""
    return str(value.quantize(Decimal("0.01")))
