"""BE-12 sanctioned adapter boundary — PRACTICE-WIRED (BO-V2-BE12B-001 §1.b).

The ONLY doorway through which live_exec writers may ever reach a
provider. 12B moves the stance literal `posture_stub` -> `practice_wired`
BY CITED EDIT (the 12A supersession coupon names the BO). The PRACTICE
submission path reaches the terminal family ONLY via the sanctioned
BE-9 provider leg (`app.v2.broker_read.providers.practice_actuator`) —
NEVER directly: no terminal package import exists in this file or
anywhere in live_exec. This file is the ONE package file permitted to
speak a provider-module token (the amended wall coupon scopes the
exception to this file by name-literal).

The LIVE lane still has no path here: `submission_doorway` demands a
practice-lane pass FIRST (re-checked at this door — belt and braces,
one lane, one vocabulary). Terminal absence answers the typed refusal
`practice_terminal_unavailable` proxied from the provider leg; terminal
timeouts surface as the `no_answer` STATE record, never an exception
from the seam (BE-8 S2.4 preimage law; the caller quarantines).
"""

from __future__ import annotations

from typing import Final

from app.v2.live_exec.locks import (
    PracticeActuationState,
    require_practice_actuation,
)

# Closed stance vocabulary (state nouns — wording law).
BOUNDARY_STANCES: Final = ("posture_stub", "practice_wired", "activation_scoped")

# 12B pin (BO-V2-BE12B-001 SS1.b cited edit; supersedes the 12A
# `posture_stub` literal): the boundary now carries the PRACTICE path.
BOUNDARY_STANCE: Final = "practice_wired"


def practice_credential_state() -> str:
    """State-only vault read for the lane door: 'present' | 'absent'.

    The boundary is the ONE live_exec file permitted to name the vault
    module (amended wall law, name-literal). No material crosses this
    function — it forwards the resolution STATE string only; the sealed
    doorway itself fail-closes every absence arm.
    """
    from app.v2.broker_read.vault import resolve_practice_trade_credential
    return resolve_practice_trade_credential().state


class AdapterBoundaryRefused(Exception):
    """Typed boundary refusal — reason from the closed lane vocabulary."""

    def __init__(self, reason: str, notes: list[dict] | None = None):
        self.reason = reason
        self.notes = notes or []
        super().__init__(reason)


def submission_doorway(practice_state: PracticeActuationState,
                       order_request: dict) -> dict:
    """The PRACTICE submission path (12B). LIVE lane has no path here.

    Contract: (1) the practice-lane door must pass (re-checked here);
    (2) the terminal is reached ONLY through the sanctioned provider
    family's actuator; (3) the answer is a RECORD from the actuator's
    closed state vocabulary (`accepted|rejected|requote|no_answer`).
    """
    require_practice_actuation(practice_state)
    # Deferred import: the provider leg loads only when a lawful
    # practice-lane pass reaches the doorway (E-ENV-1 pattern).
    from app.v2.broker_read.providers.practice_actuator import (
        PracticeTerminalRefused,
        practice_order_send,
    )
    try:
        return practice_order_send(order_request)
    except PracticeTerminalRefused as refused:
        raise AdapterBoundaryRefused(refused.reason, refused.notes) from None


# --- BE-12C act doorways (BO-V2-BE12C-001 SS1.b; same lane law) ------------------


def adapter_capability_map() -> dict:
    """THE CITED READ (BO SS1.a verb law): the capability map is read
    from the LANDED adapter object — never handwritten here. A verb the
    adapter cannot evidence does not exist in 12C."""
    from app.v2.broker_read.providers.practice_actuator import (
        PRACTICE_ORDER_CAPABILITIES,
    )
    return {verb: dict(spec)
            for verb, spec in PRACTICE_ORDER_CAPABILITIES.items()}


def cancel_doorway(practice_state: PracticeActuationState,
                   cancel_request: dict) -> dict:
    """The PRACTICE cancel path. Lane door re-checked; terminal reached
    only via the provider leg; answer = closed act-outcome RECORD."""
    require_practice_actuation(practice_state)
    from app.v2.broker_read.providers.practice_actuator import (
        PracticeTerminalRefused,
        practice_order_cancel,
    )
    try:
        return practice_order_cancel(cancel_request)
    except PracticeTerminalRefused as refused:
        raise AdapterBoundaryRefused(refused.reason, refused.notes) from None


def modify_doorway(practice_state: PracticeActuationState,
                   modify_request: dict) -> dict:
    """The PRACTICE modify path (supported fields only; same laws)."""
    require_practice_actuation(practice_state)
    from app.v2.broker_read.providers.practice_actuator import (
        PracticeTerminalRefused,
        practice_order_modify,
    )
    try:
        return practice_order_modify(modify_request)
    except PracticeTerminalRefused as refused:
        raise AdapterBoundaryRefused(refused.reason, refused.notes) from None
