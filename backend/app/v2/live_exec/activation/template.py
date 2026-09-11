"""BE-12D activation-instrument TEMPLATE artifact (BO-V2-BE12D-001 §1.b.2).

READ-ONLY data. The template is the instrument's extant form: versioned,
hash-pinned (the artifact hash is recomputed from these final bytes by
coupon — C-2-family discipline), and NOT-IN-FORCE ON ITS FACE. No code
in this band writes the instrument table; no force-verb exists.
"""

from __future__ import annotations

import hashlib
from typing import Final

TEMPLATE_VERSION: Final = "lai-1.0.0"

# The instrument's face. Its OWN opening clause declares non-force.
ACTIVATION_INSTRUMENT_TEMPLATE: Final = """\
AXIOM V2 — LIVE ACTIVATION INSTRUMENT (TEMPLATE, lai-1.0.0)
STATUS ON ITS FACE: NOT IN FORCE.

THIS TEMPLATE CONFERS NO ACTIVATION. It is the drafted, versioned,
hash-pinned FORM of the instrument only. Taking force is a FUTURE
OPERATOR REGISTER ACT — its own build order, its own evidence arms —
requiring, at minimum, ALL of:
  (1) a funded-posture witness (funded_posture_ref) — no funded account
      exists at this drafting; the reference class itself is
      NONEXISTENT until that act;
  (2) an operator step-up confirmation (step_up_ref) — second FACTOR,
      never second actor;
  (3) a kill-switch check — the switch must exist and not be pulled at
      the moment of force.
Until such an act, the instrument table's ZERO-ROW state IS the lock:
every LIVE-lane actuation ask answers the typed refusal
`activation_instrument_not_in_force` at lock position L3. The machine
never takes force on its own initiative (activate-nothing law;
N4/N-O11). The capability being complete is not, and may never be
cited as, evidence toward production certification (REQ R-1.4 adopted
wording).
"""


def template_hash() -> str:
    """The artifact hash, recomputed from the final bytes at every ask
    (never a stored literal — the naming-of-numbers law)."""
    return hashlib.sha256(
        ACTIVATION_INSTRUMENT_TEMPLATE.encode("utf-8")).hexdigest()
