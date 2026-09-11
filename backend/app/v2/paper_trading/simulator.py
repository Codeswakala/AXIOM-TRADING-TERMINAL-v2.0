"""BE-8 paper execution simulator (design S4; BO T-4/T-6/T-10).

Deterministic single-pass over a pinned snapshot's bars: market orders
fill at the first bar close; limit orders when touched (low <= limit for
buys, high >= limit for sells); partial fills when declared bar liquidity
is below remaining quantity. Costs via the CR-V2-BE-7-001 unit vocabulary
('price'/'fraction'); Decimal throughout (S5 money law). The seam accepts
ONLY PaperOrderIntent (S6.1) — no dict-shaped order can cross. Snapshot
content is re-verified before execution (G-5 lineage; mismatch = typed
refusal, never silent).

Replay contract (S4.3): (intent + snapshot content hash + cost model +
simulator version) -> byte-identical fills, x3-attested in tests.
"""

from __future__ import annotations

import hashlib
import json
from decimal import Decimal

from app.v2.paper_trading.contracts import (
    COST_UNITS_V1,
    PAPER_DISCLAIMER,
    PaperOrderIntent,
    PaperRefused,
)

SIMULATOR_VERSION = "pxs-1.0.0"
ENGINE_VERSIONS = {"paper_execution_simulator": SIMULATOR_VERSION,
                   "paper_risk_gateway": "prg-1.0.0"}


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      default=str)


def engine_versions_hash() -> str:
    return hashlib.sha256(canonical(ENGINE_VERSIONS).encode()).hexdigest()


def snapshot_content_hash(bars: list[dict], snapshot_ref: str) -> str:
    """Content hash over the bar set + ref (S4.1 re-verification law)."""
    payload = canonical({"snapshot_ref": snapshot_ref, "bars": bars})
    return hashlib.sha256(payload.encode()).hexdigest()


def apply_costs(fill_price: Decimal, side: str, cost_model: dict) -> Decimal:
    """Effective price after declared costs (CR-V2-BE-7-001 vocabulary)."""
    price = Decimal(str(fill_price))
    sign = Decimal(1) if side == "buy" else Decimal(-1)
    for key in ("spread", "commission", "slippage"):
        entry = cost_model[key]
        if entry["unit"] not in COST_UNITS_V1:
            raise PaperRefused("paper.cost_unit.unknown", [
                {"failing": f"{key}.unit", "value": entry["unit"],
                 "allowed": list(COST_UNITS_V1)}])
        value = Decimal(str(entry["value"]))
        if entry["unit"] == "price":
            price += sign * value
        else:
            price *= (Decimal(1) + sign * value)
    return price


def run_simulation(
    intent: PaperOrderIntent,
    bars: list[dict],
    *,
    stored_content_hash: str,
) -> dict:
    """Execute the intent deterministically. Typed seam: PaperOrderIntent only.

    Returns {fills, outcome, disclaimer, engine_versions,
    engine_versions_hash, bars_replayed}. outcome: 'filled' |
    'partially_filled' | 'expired'.
    """
    if not isinstance(intent, PaperOrderIntent):  # S6.1 typed seam
        raise PaperRefused("paper.seam.untyped", [
            {"failing": "intent", "note":
             "simulator seam accepts PaperOrderIntent only"}])

    observed = snapshot_content_hash(bars, intent.snapshot_ref)
    if observed != stored_content_hash:
        raise PaperRefused("paper.snapshot.content_mismatch", [
            {"failing": "snapshot_content_hash",
             "stored": stored_content_hash, "observed": observed,
             "note": "G-5 lineage law: refusal, never silent inclusion"}])

    remaining = Decimal(str(intent.quantity))
    fills: list[dict] = []
    fill_index = 0
    for bar in bars:
        if remaining <= 0:
            break
        close = Decimal(str(bar["close"]))
        low = Decimal(str(bar["low"]))
        high = Decimal(str(bar["high"]))
        liquidity = Decimal(str(bar.get("liquidity", remaining)))

        if intent.order_type == "market":
            raw = close
        else:
            limit = Decimal(str(intent.limit_price))
            if intent.side == "buy" and low <= limit:
                raw = limit
            elif intent.side == "sell" and high >= limit:
                raw = limit
            else:
                continue

        qty = min(remaining, liquidity) if liquidity > 0 else remaining
        if qty <= 0:
            continue
        effective = apply_costs(raw, intent.side, intent.cost_model)
        fills.append({
            "fill_index": fill_index,
            "quantity": str(qty),
            "raw_price": str(raw),
            "effective_price": str(effective),
            "fill_class": "paper_simulated",  # N4 — the only value
            "simulator_version": SIMULATOR_VERSION,
            "bar_open_time": str(bar["open_time"]),
        })
        remaining -= qty
        fill_index += 1

    if not fills:
        outcome = "expired"
    elif remaining > 0:
        outcome = "partially_filled"
    else:
        outcome = "filled"

    return {
        "fills": fills,
        "outcome": outcome,
        "unfilled_quantity": str(remaining),
        "bars_replayed": len(bars),
        "disclaimer": PAPER_DISCLAIMER,
        "engine_versions": dict(ENGINE_VERSIONS),
        "engine_versions_hash": engine_versions_hash(),
    }
