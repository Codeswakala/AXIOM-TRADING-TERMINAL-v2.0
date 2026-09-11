"""BE-8 pre-trade risk gateway (design S3; BO T-8/T-9).

Default-deny: an intent with no decision row cannot reach `executing`
(orders.py enforces the S2.6 derived rule). Exactly-once evaluation is a
SCHEMA fact (uq(intent_id) on v2_paper_risk_decision). Every limit is
measured and recorded: {observed, threshold, verdict} per limit — never
asserted. The margin engine (ledger.py) computes; ONLY this gateway
decides (Q5 single-decision-authority law).
"""

from __future__ import annotations

from decimal import Decimal

from app.v2.paper_trading.contracts import (
    RISK_CONFIG_V1,
    RISK_CONFIG_VERSION_V1,
)

SIMULATOR_VERSION = "pxs-1.0.0"
GATEWAY_VERSION = "prg-1.0.0"


def evaluate_intent(
    *,
    quantity: Decimal,
    reference_price: Decimal,
    account_state: str,
    instrument_known: bool,
    margin_available: Decimal,
    margin_required: Decimal,
    concentration_fraction: Decimal,
    session_intent_count: int,
) -> tuple[str, dict, list]:
    """Pure decision function. Returns (decision, evaluated_limits, reasons).

    decision: 'pass' | 'block' | 'hold' (S3 semantics: block terminal with
    no confirmation path; hold when a limit is inside its declared
    confirmation band; pass otherwise).
    """
    cfg = RISK_CONFIG_V1
    notional = quantity * reference_price
    limits: dict = {}
    reasons: list = []
    hold_reasons: list = []

    def _check(name: str, observed, threshold, ok: bool) -> None:
        limits[name] = {"observed": str(observed), "threshold": str(threshold),
                        "verdict": "pass" if ok else "fail"}
        if not ok:
            reasons.append({"failing": name, "observed": str(observed),
                            "threshold": str(threshold)})

    _check("max_order_quantity", quantity, cfg["max_order_quantity"],
           quantity <= cfg["max_order_quantity"])
    _check("max_order_notional", notional, cfg["max_order_notional"],
           notional <= cfg["max_order_notional"])
    _check("instrument_allowed", instrument_known, True, instrument_known)
    _check("account_active", account_state, "active",
           account_state == "active")
    _check("sufficient_margin", margin_required, margin_available,
           margin_required <= margin_available)
    _check("concentration", concentration_fraction,
           cfg["max_concentration_fraction"],
           concentration_fraction <= cfg["max_concentration_fraction"])
    _check("session_rate", session_intent_count,
           cfg["max_intents_per_session"],
           session_intent_count < cfg["max_intents_per_session"])

    if reasons:
        return "block", limits, reasons

    # Hold band: notional within [band_lower * max, max] (S3).
    band_floor = cfg["max_order_notional"] * cfg["hold_band_lower_fraction"]
    if notional >= band_floor:
        hold_reasons.append({
            "holding": "max_order_notional_band",
            "observed": str(notional),
            "band": [str(band_floor), str(cfg["max_order_notional"])],
            "note": "confirmation band - human confirmation required (S7.2)",
        })
        limits["max_order_notional_band"] = {
            "observed": str(notional),
            "threshold": str(band_floor), "verdict": "hold"}
        return "hold", limits, hold_reasons

    return "pass", limits, []


def config_version() -> str:
    """The version pinned on every decision row (S3 governance)."""
    return RISK_CONFIG_VERSION_V1
