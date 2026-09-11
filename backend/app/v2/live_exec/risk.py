"""BE-12A pre-trade risk engine (BO-V2-BE12A-001 §1.c).

Money-units sizing inherited from the BE-11 flat-account law; decline
verbs typed; positive-reason pair carried on the evaluated record
(BO §4). No live submission exists in this sub-band (12B scope).
"""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Final

from app.v2.live_exec.intents import LiveExecRefused

# Closed decline vocabulary (wording law; CWS-recoverable ids).
RISK_DECLINES: Final = (
    "notional_exceeds_available_margin",
    "quantity_not_positive",
    "citation_currency_differs_from_basis",
)

# Closed risk answer states.
RISK_STATES: Final = ("risk_evaluated", "risk_declined")


def evaluate_pre_trade_risk(
    *, quantity: str, cited_price: str, price_currency: str,
    basis_currency: str, margin_available: str,
) -> dict:
    """Money-units sizing (BE-11 flat-account law); typed declines.

    Positive reasons pair (BO §4): the evaluated record carries the
    passing facts, not only absence-of-decline.
    """
    try:
        qty = Decimal(quantity)
        price = Decimal(cited_price)
        available = Decimal(margin_available)
    except (InvalidOperation, TypeError) as exc:
        raise LiveExecRefused("quantity_not_positive", [
            {"failing": "numeric_inputs", "note": "non-decimal input"},
        ]) from exc

    declines: list[str] = []
    if qty <= 0:
        declines.append("quantity_not_positive")
    if price_currency != basis_currency:
        declines.append("citation_currency_differs_from_basis")
    notional = qty * price
    if notional > available:
        declines.append("notional_exceeds_available_margin")

    if declines:
        return {"risk_state": "risk_declined", "declines": declines,
                "notional": str(notional), "available": str(available)}
    return {"risk_state": "risk_evaluated", "declines": [],
            "notional": str(notional), "available": str(available),
            "positive_facts": {
                "quantity_positive": True,
                "currency_matched": True,
                "notional_within_available": True}}
