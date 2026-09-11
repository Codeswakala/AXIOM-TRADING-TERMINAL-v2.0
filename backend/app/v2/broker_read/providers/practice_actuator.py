"""BE-12B practice actuator — the terminal-speaking submission body
(BO-V2-BE12B-001 §1.b).

Lives INSIDE the sanctioned provider family (`v2/broker_read/providers/`)
because that is the ONLY location where terminal vocabulary is lawful
under the V1 containment allowlist (extended at BE-9 by BO citation;
NOT re-extended here — this file rides the standing prefix). The
live_exec adapter boundary imports THIS module and nothing else
provider-shaped; no other live_exec file may.

Contract: every terminal answer returns as a RECORD
{terminal_state, server_ack_ref, raw_note} from the closed
PRACTICE_TERMINAL_STATES; timeouts/absent retcodes surface as
`no_answer` — a STATE, never an exception from the seam (BE-8 S2.4
preimage law; the caller quarantines). Terminal absence answers the
typed refusal `practice_terminal_unavailable` (the practice-lane mirror
of broker.terminal.unavailable; E-ENV-1 first-class law).
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Final

# Closed terminal-answer vocabulary (state nouns — wording law).
PRACTICE_TERMINAL_STATES: Final = (
    "accepted", "rejected", "requote", "no_answer")

# --- BE-12C (BO-V2-BE12C-001 SS1.a): THE LANDED CAPABILITY MAP -------------------
# The verb law: cancel/modify verbs exist ONLY where THIS adapter can
# evidence them. 12C reads THIS object by cited read (identity import
# through the boundary) — never a handwritten copy. Mechanisms are the
# terminal contract's own: order remove/modify actions apply to PENDING
# orders only. POSITION verbs are ABSENT from this map BY CHARTER
# (no position modify; a close is a NEW opposite submission under 12B
# law). The supported modify fields are exactly the pending-order
# fields the terminal contract carries.
PRACTICE_ORDER_CAPABILITIES: Final = MappingProxyType({
    "cancel": MappingProxyType({
        "supported": True,
        "mechanism": "terminal order-remove action",
        "applies_to": "pending_orders_only",
    }),
    "modify": MappingProxyType({
        "supported": True,
        "mechanism": "terminal order-modify action",
        "applies_to": "pending_orders_only",
        "fields": ("price", "stop_loss", "take_profit", "expiration"),
    }),
})

# Closed act-outcome vocabulary for cancel/modify terminal answers.
PRACTICE_ACT_OUTCOMES: Final = ("applied", "refused_terminal",
                                "unknown_outcome")


class PracticeTerminalRefused(Exception):
    """Typed practice-terminal refusal (practice-lane vocabulary)."""

    def __init__(self, reason: str, notes: list[dict] | None = None):
        self.reason = reason
        self.notes = notes or []
        super().__init__(reason)


def _terminal():
    """Deferred guarded import (the BE-9 provider-leg pattern verbatim)."""
    try:
        import MetaTrader5 as mt5  # noqa: N813 - provider package name
        return mt5
    except ImportError:
        raise PracticeTerminalRefused("practice_terminal_unavailable", [
            {"failing": "terminal",
             "note": "MetaTrader5 package not importable on this station"
                     " (practice leg requires the sealed BE-9 terminal"
                     " family)"}]) from None


def practice_order_send(order_request: dict) -> dict:
    """Submit ONE practice-world order request; answer is a RECORD."""
    mt5 = _terminal()
    try:
        result = mt5.order_send(order_request)
        if result is None:
            return {"terminal_state": "no_answer", "server_ack_ref": None,
                    "raw_note": "terminal returned no result object"}
        retcode = getattr(result, "retcode", None)
        if retcode is None:
            return {"terminal_state": "no_answer", "server_ack_ref": None,
                    "raw_note": "result carried no retcode"}
        if retcode == getattr(mt5, "TRADE_RETCODE_DONE", 10009):
            return {"terminal_state": "accepted",
                    "server_ack_ref": str(getattr(result, "order", "")),
                    "raw_note": f"retcode={retcode}"}
        if retcode == getattr(mt5, "TRADE_RETCODE_REQUOTE", 10004):
            return {"terminal_state": "requote", "server_ack_ref": None,
                    "raw_note": f"retcode={retcode}"}
        return {"terminal_state": "rejected", "server_ack_ref": None,
                "raw_note": f"retcode={retcode}"}
    except PracticeTerminalRefused:
        raise
    except Exception as exc:  # timeout/transport: a state, not an exception
        return {"terminal_state": "no_answer", "server_ack_ref": None,
                "raw_note": f"seam absorbed {type(exc).__name__}"}


def _act_answer(mt5, result) -> dict:
    """Map a cancel/modify terminal result onto the closed act-outcome
    vocabulary. Absent result/retcode/exception => unknown_outcome — a
    STATE, never an exception from the seam (BE-8 S2.4 preimage)."""
    if result is None:
        return {"outcome": "unknown_outcome", "raw_note":
                "terminal returned no result object"}
    retcode = getattr(result, "retcode", None)
    if retcode is None:
        return {"outcome": "unknown_outcome",
                "raw_note": "result carried no retcode"}
    if retcode == getattr(mt5, "TRADE_RETCODE_DONE", 10009):
        return {"outcome": "applied", "raw_note": f"retcode={retcode}"}
    return {"outcome": "refused_terminal",
            "raw_note": f"retcode={retcode}"}


def practice_order_cancel(cancel_request: dict) -> dict:
    """Cancel ONE pending practice-world order; answer is a RECORD from
    PRACTICE_ACT_OUTCOMES (BO-V2-BE12C-001 SS1.a/SS1.c)."""
    mt5 = _terminal()
    request = {"action": getattr(mt5, "TRADE_ACTION_REMOVE", 8),
               **cancel_request}
    try:
        return _act_answer(mt5, mt5.order_send(request))
    except PracticeTerminalRefused:
        raise
    except Exception as exc:  # timeout/transport: a state, not an exception
        return {"outcome": "unknown_outcome",
                "raw_note": f"seam absorbed {type(exc).__name__}"}


def practice_order_modify(modify_request: dict) -> dict:
    """Modify ONE pending practice-world order (supported fields only);
    answer is a RECORD from PRACTICE_ACT_OUTCOMES."""
    mt5 = _terminal()
    request = {"action": getattr(mt5, "TRADE_ACTION_MODIFY", 7),
               **modify_request}
    try:
        return _act_answer(mt5, mt5.order_send(request))
    except PracticeTerminalRefused:
        raise
    except Exception as exc:  # timeout/transport: a state, not an exception
        return {"outcome": "unknown_outcome",
                "raw_note": f"seam absorbed {type(exc).__name__}"}
