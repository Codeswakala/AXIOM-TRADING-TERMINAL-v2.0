"""BE-7 U-2 deterministic replay engine (plan Part 2; P-8 G-2).

Pure function of (registered input content, strategy parameters, cost
model, engine versions). No wall clock, no unpinned randomness, no I/O.
The decision cursor is the structural cutoff: at step t the strategy
callback can observe ONLY bars with open_time <= t (G-2).
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal

from app.v2.research_jobs.leakage import (
    ReplayWindow,
    filter_bars_g1,
    verify_content_g5,
)

ENGINE_VERSIONS = {"replay_engine": "rpe-1.0.0",
                   "research_job_engine": "rje-1.0.0"}


def canonical(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      default=str)


def engine_versions_hash() -> str:
    return hashlib.sha256(canonical(ENGINE_VERSIONS).encode()).hexdigest()


# --- Cost application (REQ-1.4: pure and deterministic) -----------------------


def apply_costs(fill_price: Decimal, side: str, cost_model: dict) -> Decimal:
    """Effective price after declared costs. spread/commission/slippage are
    {value, unit, citation} entries; v1 units: 'price' (absolute add) and
    'fraction' (multiplicative). Deterministic; no rounding surprises
    (Decimal throughout)."""
    price = Decimal(str(fill_price))
    sign = Decimal(1) if side == "buy" else Decimal(-1)
    for key in ("spread", "commission", "slippage"):
        entry = cost_model[key]
        value = Decimal(str(entry["value"]))
        if entry["unit"] == "price":
            price += sign * value
        elif entry["unit"] == "fraction":
            price *= (Decimal(1) + sign * value)
        else:  # unknown unit is a typed configuration error upstream
            raise ValueError(f"unknown cost unit: {entry['unit']}")
    return price


# --- Strategy rules (v1 scope: registered deterministic rule functions) --------


@dataclass(frozen=True)
class CursorSlice:
    """G-2: the immutable window slice a strategy sees at one step —
    bars strictly up to and including the cursor; nothing beyond."""

    bars: tuple
    cursor: datetime


def threshold_rule(slice_: CursorSlice, params: dict) -> str | None:
    """v1 rule: buy when close < buy_below; sell when close > sell_above.
    Pure; sees only the slice."""
    last = slice_.bars[-1]
    close = Decimal(str(last["close"]))
    if close < Decimal(str(params["buy_below"])):
        return "buy"
    if close > Decimal(str(params["sell_above"])):
        return "sell"
    return None


def crossover_rule(slice_: CursorSlice, params: dict) -> str | None:
    """v1 rule: fast/slow mean crossover over the visible slice."""
    n_fast, n_slow = int(params["fast"]), int(params["slow"])
    closes = [Decimal(str(b["close"])) for b in slice_.bars]
    if len(closes) < n_slow:
        return None
    fast = sum(closes[-n_fast:]) / n_fast
    slow = sum(closes[-n_slow:]) / n_slow
    prev_closes = closes[:-1]
    if len(prev_closes) < n_slow:
        return None
    pfast = sum(prev_closes[-n_fast:]) / n_fast
    pslow = sum(prev_closes[-n_slow:]) / n_slow
    if pfast <= pslow and fast > slow:
        return "buy"
    if pfast >= pslow and fast < slow:
        return "sell"
    return None


STRATEGY_RULES = {"threshold": threshold_rule, "crossover": crossover_rule}


@dataclass
class ReplayResult:
    fills: list = field(default_factory=list)
    summary: dict = field(default_factory=dict)
    decision_ledger: list = field(default_factory=list)


def run_replay(*, bars: list[dict], window: ReplayWindow,
               strategy_rule: str, parameters: dict, cost_model: dict,
               stored_content_hash: str, series_refs: dict) -> ReplayResult:
    """The deterministic replay. G-5 re-verifies content; G-1 filters;
    G-2 slices at the cursor; every decision is ledgered with its data
    timestamps (G-4 evidence)."""
    from app.v2.research_jobs.leakage import content_hash as _ch

    assembled = filter_bars_g1(bars, window)  # G-1: the only fetch path
    verify_content_g5(
        stored_hash=stored_content_hash,
        recomputed_hash=_ch(assembled, window, series_refs))  # G-5

    if strategy_rule not in STRATEGY_RULES:
        raise ValueError(f"unregistered strategy rule: {strategy_rule}")
    rule = STRATEGY_RULES[strategy_rule]

    result = ReplayResult()
    position = Decimal(0)
    cash = Decimal(str(parameters.get("initial_cash", "10000")))
    for i in range(1, len(assembled) + 1):
        visible = tuple(assembled[:i])          # G-2: cursor slice
        cursor = visible[-1]["open_time"]
        decision = rule(CursorSlice(bars=visible, cursor=cursor), parameters)
        result.decision_ledger.append({
            "decision_ts": cursor,
            "data_ref_ts": [b["open_time"] for b in visible[-3:]],
            "decision": decision,
        })
        if decision in ("buy", "sell"):
            raw = Decimal(str(visible[-1]["close"]))
            effective = apply_costs(raw, decision, cost_model)
            qty = Decimal(str(parameters.get("unit_qty", "1")))
            if decision == "buy":
                position += qty
                cash -= effective * qty
            else:
                position -= qty
                cash += effective * qty
            result.fills.append({
                "ts": cursor.isoformat(), "side": decision,
                "raw_price": str(raw), "effective_price": str(effective),
                "qty": str(qty),
            })
    final_mark = (Decimal(str(assembled[-1]["close"]))
                  if assembled else Decimal(0))
    equity = cash + position * final_mark
    result.summary = {
        "bars_replayed": len(assembled),
        "fills": len(result.fills),
        "final_position": str(position),
        "final_cash": str(cash),
        "final_equity": str(equity),
        "performance_disclaimer": (
            "pipeline-validation tier on labelled synthetic input;"
            " NOT live or future performance; no market conclusion"),
    }
    return result
