"""BE-8 typed contracts — vocabularies, sealed registry, typed seam.

Design AXIOM-V2-BE-8-DESIGN-001 v1.1.0 (ACCEPTED) S1/S2/S6; BO-V2-BE-8-001
T-2/T-4/T-9. The N2 isolation mechanism lives here: EXECUTION_BACKENDS is a
frozen single-entry literal (no registration function, no plugin path, no
config file — adding a key requires editing this literal, caught by the
source manifest and the import scan). No adapter interface/ABC exists
anywhere in this band BY DESIGN (an abstraction with one paper
implementation is the substitution surface N2 forbids).
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from types import MappingProxyType
from typing import Final

# --- N2: the sealed routing registry (S6.1) -----------------------------------
# BE-12A AM-3 (BO-V2-BE12A-001 SS1.e; adopted REQ S-3): the registry
# extends 1 -> 2 keys BY THIS CITED EDIT. The 'live' entry is
# POSTURE-LOCKED: it names the live_exec adapter boundary (posture-stub
# in 12A) — never a transport; every submission-shaped call through it
# refuses typed until 12B wiring, and actuation itself sits behind the
# lock-order chokepoint (mode_locked first). The single-entry coupon in
# tests/test_v2_be8_boundaries.py is superseded BY CITATION of this BO
# (the file is presence-only-pinned by BE-11 — lawful to edit).
EXECUTION_BACKENDS: Final = MappingProxyType(
    {"paper": "app.v2.paper_trading.simulator",
     "live": "app.v2.live_exec.adapter_boundary"})

# --- Order lifecycle vocabulary (S2.1; closed) ---------------------------------
ORDER_STATES = (
    "draft", "validated", "rejected",
    "risk_passed", "risk_blocked", "risk_hold",
    "executing", "filled", "partially_filled",
    "settled", "cancelled", "expired", "quarantined_unknown",
)
TERMINAL_STATES = ("settled", "rejected", "risk_blocked", "cancelled",
                   "expired", "quarantined_unknown")

# S2.2 exhaustive legal transitions — absence is a typed refusal.
LEGAL_TRANSITIONS = (
    ("draft", "validated"), ("draft", "rejected"), ("draft", "cancelled"),
    ("validated", "risk_passed"), ("validated", "risk_blocked"),
    ("validated", "risk_hold"), ("validated", "cancelled"),
    ("risk_hold", "risk_passed"), ("risk_hold", "cancelled"),
    ("risk_passed", "executing"),
    ("executing", "filled"), ("executing", "partially_filled"),
    ("executing", "expired"), ("executing", "quarantined_unknown"),
    ("filled", "settled"), ("partially_filled", "settled"),
)

# S2.6/C-1c closed event-class vocabulary.
EVENT_CLASSES = (
    "order.drafted", "order.validated", "order.rejected",
    "risk.passed", "risk.blocked", "hold.issued",
    "hold.confirmed", "hold.cancelled",
    "order.cancelled", "execution.started",
    "execution.filled", "execution.partially_filled",
    "execution.expired", "order.settled",
    "order.recovered", "order.quarantined",
)

# S3 decision vocabulary.
RISK_DECISIONS = ("pass", "block", "hold")

# N4: the single-value fill-class law — the schema CHECK admits exactly this.
FILL_CLASSES = ("paper_simulated",)

# S7.2/C-1b confirmation refusal classes (typed; each durably audited).
CONFIRMATION_REFUSALS = (
    "paper.confirmation.already_consumed",
    "paper.confirmation.ref_mismatch",
    "paper.confirmation.cancelled",
    "paper.confirmation.not_confirmable",
)

ACCOUNT_STATES = ("active", "frozen", "closed")
ACCOUNT_ACTIONS = ("create", "freeze", "close")
INTENT_SIDES = ("buy", "sell")
INTENT_TYPES = ("market", "limit")
TIME_IN_FORCE_V1 = ("replay_window",)
BASE_CURRENCIES_V1 = ("USD",)

# Cost-unit vocabulary — CR-V2-BE-7-001 lineage, same law.
COST_UNITS_V1 = ("price", "fraction")

# S3 v1 risk configuration (A-1: DA defaults, Operator resets at will via a
# future governed act; version pinned on every decision row).
RISK_CONFIG_VERSION_V1 = "prc-1"
RISK_CONFIG_V1: Final = MappingProxyType({
    "max_order_quantity": Decimal("10000"),
    "max_order_notional": Decimal("100000"),
    "hold_band_lower_fraction": Decimal("0.80"),
    "max_concentration_fraction": Decimal("0.25"),
    "margin_rate_default": Decimal("0.5"),
    "max_intents_per_session": 100,
})

# The mandatory unconditional disclaimer (N4 surface law).
PAPER_DISCLAIMER = (
    "paper-simulated execution on governed replayable snapshots; "
    "never broker-confirmed; no live or future performance claim"
)

_DOMAIN = "v2.paper_trading"


@dataclass(frozen=True)
class PaperOrderIntent:
    """The ONLY type the simulator seam accepts (S6.1 typed seam).

    Constructed exclusively by the run writer after the S2.6 derived rule
    (`may_execute`) passes. Frozen: no field is assignable post-construction.
    """

    intent_id: str
    account_id: str
    instrument_id: str
    side: str
    order_type: str
    quantity: Decimal
    limit_price: Decimal | None
    snapshot_ref: str
    window_start: str
    window_end: str
    cost_model: dict


@dataclass(frozen=True)
class PaperOutcome:
    """Uniform typed outcome for paper writers."""

    outcome: str
    reasons: list
    record_id: str | None = None
    confirmation_ref: str | None = None

    @property
    def refused(self) -> bool:
        return self.outcome == "refused"


class PaperRefused(Exception):
    """Typed refusal in the paper domain; class + reasons always carried."""

    def __init__(self, refusal_class: str, reasons: list) -> None:
        self.refusal_class = refusal_class
        self.reasons = reasons
        super().__init__(f"{refusal_class}: {reasons}")
