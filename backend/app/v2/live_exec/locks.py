"""BE-12A LOCK-ORDER chokepoint (BO §1.d; DR-2 lock-stack; DA §2 law).

ONE door for every actuating verb: `require_actuation(...)` evaluates
the locks in PINNED ORDER L1 -> L6 and refuses with the FIRST failing
lock's typed reason. Nothing else in live_exec may answer an actuation
question — the BE-8 `may_execute`-owned-once law at six-lock scale.

Separation of truths (DR-2 adopted):
- L1 `mode_locked` is computed ONLY from the mode contract
  (REGISTERED_LOCKED_MODES membership) — posture inputs cannot
  manufacture a mode answer (promenade-coupon-proven).
- L2 `posture_mismatch` is computed only from credential-class facts.
- L3 `activation_instrument_not_in_force` is the zero-row schema lock
  (table arrives 12D; in 12A the state input carries the standing
  truth: the instrument DOES NOT EXIST — the caller may not invent it).
- L4 `funded_posture_required`, L5 `killswitch_armed`,
  L6 downstream `sub_*` classes: state inputs with the same law.

In 12A the actuating verbs ARE evaluation/registration only (no
submission — 12B), so this door is exercised by test-only promenades
and the ledger-verified refusal arms, per the BO.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final

from app.v2.mode.contract import REGISTERED_LOCKED_MODES

# The pinned order IS the law (order-fixture coupons assert it).
LOCK_ORDER: Final = (
    "mode_locked",                          # L1
    "posture_mismatch",                     # L2
    "activation_instrument_not_in_force",   # L3
    "funded_posture_required",              # L4
    "killswitch_armed",                     # L5
    "sub_contract_failure",                 # L6 (downstream sub_* family)
)

# Credential classes the posture lock recognizes (AM-4 vocabulary).
ACTUATION_CREDENTIAL_CLASSES: Final = ("practice_trade",)


class ActuationRefused(Exception):
    """Typed lock refusal; reason is a LOCK_ORDER member (or sub_* class)."""

    def __init__(self, reason: str, lock: str, notes: list[dict] | None = None):
        self.reason = reason
        self.lock = lock
        self.notes = notes or []
        super().__init__(reason)


@dataclass(frozen=True)
class ActuationState:
    """The lock inputs, one reading, at the door (consistency ARM)."""

    mode: str
    credential_class: str | None = None       # vault-resolved class name only
    activation_instrument_rows: int = 0        # zero-row lock (12D table; 0 = standing truth)
    funded_posture: bool = False               # R-6.3: no funded account exists
    killswitch_armed: bool = False             # 12D persisted table; False until it exists
    sub_failures: tuple[str, ...] = field(default_factory=tuple)  # L6 injected classes


def _l1_mode_locked(state: ActuationState) -> bool:
    # ONLY the mode contract answers (never posture inputs).
    return state.mode in REGISTERED_LOCKED_MODES


def _l2_posture_mismatch(state: ActuationState) -> bool:
    return state.credential_class not in ACTUATION_CREDENTIAL_CLASSES


def _l3_activation_absent(state: ActuationState) -> bool:
    return state.activation_instrument_rows == 0


def _l4_funded_required(state: ActuationState) -> bool:
    return not state.funded_posture


def _l5_killswitch(state: ActuationState) -> bool:
    return state.killswitch_armed


def _l6_sub_failures(state: ActuationState) -> bool:
    return bool(state.sub_failures)


_LOCK_PREDICATES = (
    ("mode_locked", _l1_mode_locked),
    ("posture_mismatch", _l2_posture_mismatch),
    ("activation_instrument_not_in_force", _l3_activation_absent),
    ("funded_posture_required", _l4_funded_required),
    ("killswitch_armed", _l5_killswitch),
    ("sub_contract_failure", _l6_sub_failures),
)


def require_actuation(state: ActuationState) -> None:
    """The single LIVE-lane door. First failing lock refuses, in pinned order."""
    for lock_name, predicate in _LOCK_PREDICATES:
        if predicate(state):
            reason = lock_name
            notes = [{"lock": lock_name,
                      "order_position": LOCK_ORDER.index(lock_name) + 1}]
            if lock_name == "sub_contract_failure":
                # L6 proxies downstream sub_* classes first-class.
                reason = state.sub_failures[0]
                notes[0]["sub_classes"] = list(state.sub_failures)
            raise ActuationRefused(reason, lock_name, notes)


# --- PRACTICE lane (BE-12B; BO-V2-BE12B-001 SS1.a two-lane law) -------------------
#
# The chokepoint speaks TWO LANES from 12B. The LIVE lane above is the
# 12A door UNCHANGED (six locks; nothing reaches it). The PRACTICE lane
# below carries its own closed `practice_*` vocabulary. THE LANES'
# REFUSALS MAY NEVER COMMUTE: a practice-lane ask answered by a
# LIVE-lane reason (or vice versa) is a defect, coupon-pinned.

PRACTICE_LOCK_ORDER: Final = (
    "actuation_lane_mismatch",       # P1: the ask itself names the wrong lane
    "practice_mode_not_armed",       # P2: mode is not PAPER
    "practice_posture_absent",       # P3: no resolved practice_trade credential
    "practice_boundary_not_wired",   # P4: adapter boundary stance not wired
    "basis_stale",                   # P5: BOP law (present AND fresh)
)

# REGISTER CITATION (ITRGA-REV-V2-BE12B-001 §9 LOW observation,
# discharged in the CR delta): 24.0 mirrors the BE-11 basis-staleness
# presentation law (paper_bridge.engine.pin_basis: stale if age > 24h,
# fielded at 0051) — ONE staleness vocabulary across the paper bridge
# and the practice lane. A different practice threshold is an operator
# seed-class input (BE-11 SS0 precedent), arriving by its own cited
# act, never by editing this literal silently.
PRACTICE_BASIS_MAX_AGE_HOURS: Final = 24.0


class PracticeActuationRefused(Exception):
    """Typed practice-lane refusal; reason is a PRACTICE_LOCK_ORDER member."""

    def __init__(self, reason: str, lock: str, notes: list[dict] | None = None):
        self.reason = reason
        self.lock = lock
        self.notes = notes or []
        super().__init__(reason)


@dataclass(frozen=True)
class PracticeActuationState:
    """Practice-lane lock inputs, one reading at the door."""

    lane: str                                # must be 'practice'
    mode: str                                # must be 'PAPER' (armed)
    credential_state: str = "absent"         # vault class resolution STATE only
    boundary_stance: str = "posture_stub"    # adapter boundary stance literal
    basis_age_hours: float | None = None     # None = basis absent (refuses)


def _p1_lane_mismatch(state: PracticeActuationState) -> bool:
    return state.lane != "practice"


def _p2_mode_not_armed(state: PracticeActuationState) -> bool:
    return state.mode != "PAPER"


def _p3_posture_absent(state: PracticeActuationState) -> bool:
    return state.credential_state != "present"


def _p4_boundary_not_wired(state: PracticeActuationState) -> bool:
    return state.boundary_stance != "practice_wired"


def _p5_basis_stale(state: PracticeActuationState) -> bool:
    return (state.basis_age_hours is None
            or state.basis_age_hours > PRACTICE_BASIS_MAX_AGE_HOURS)


_PRACTICE_PREDICATES = (
    ("actuation_lane_mismatch", _p1_lane_mismatch),
    ("practice_mode_not_armed", _p2_mode_not_armed),
    ("practice_posture_absent", _p3_posture_absent),
    ("practice_boundary_not_wired", _p4_boundary_not_wired),
    ("basis_stale", _p5_basis_stale),
)


def require_practice_actuation(state: PracticeActuationState) -> None:
    """The single PRACTICE-lane door. First failing lock refuses, in
    pinned order. Speaks ONLY practice_* vocabulary (+ basis_stale) —
    never a LIVE-lane reason."""
    for lock_name, predicate in _PRACTICE_PREDICATES:
        if predicate(state):
            raise PracticeActuationRefused(lock_name, lock_name, [
                {"lock": lock_name, "lane": "practice",
                 "order_position":
                     PRACTICE_LOCK_ORDER.index(lock_name) + 1}])
