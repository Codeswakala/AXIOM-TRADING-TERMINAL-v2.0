"""V2 Mode Contract — single source of truth for V2 environment mode.

Mode is determined by AXIOM_V2_MODE environment variable ONLY.
No database table. No API mutation. No client input accepted.

Supported modes: RESEARCH, SIMULATION, PAPER
Deferred modes: LIVE (BE-10)

PAPER authorized by BO-V2-BE-8-001 D-3 under ITRGA ruling D-2
(ITRGA-REV-V2-BE-8-DESIGN-001 §6): narrowest extension; LIVE remains
refused; paper writers require mode == "PAPER" explicitly.
"""

from __future__ import annotations

import os

from app.core.logging import get_logger

logger = get_logger(__name__, category="SYSTEM")

VALID_MODES = ("RESEARCH", "SIMULATION", "PAPER")

# Deferred modes — recognized but never authorized until their band
DEFERRED_MODES = ("LIVE",)

# BE-12A AM-2 (BO-V2-BE12A-001 SS1.e; DR-F1 law): LIVE becomes the THIRD
# STATE — REGISTERED_LOCKED: constructible for typing/wiring/wall/refusal
# proofs, behaviorally locked at every actuation seam (the live_exec
# lock-order chokepoint refuses `mode_locked`). VALID_MODES and
# DEFERRED_MODES stay BYTE-IDENTICAL by that law: LIVE's BEHAVIOR remains
# deferred — the standing boundary-file tuple pins stay true, and the
# BE-11 byte pin on tests/test_v2_be9_boundaries.py never moves.
REGISTERED_LOCKED_MODES = ("LIVE",)


def get_mode() -> str:
    """Return the configured V2 mode. Immutable at runtime.

    Source: AXIOM_V2_MODE environment variable.
    Default: RESEARCH (if not set).

    AM-2 (BE-12A): LIVE constructs and is tagged registered-locked
    (`is_registered_locked()` answers True); every actuation seam
    refuses it as `mode_locked` at the live_exec chokepoint. All other
    non-member values still refuse here.
    """
    mode = os.environ.get("AXIOM_V2_MODE", "RESEARCH").upper()
    if mode in REGISTERED_LOCKED_MODES:
        logger.warning(
            "V2 mode %s is REGISTERED_LOCKED (BE-12A AM-2): constructible, "
            "behaviorally locked at every actuation seam (mode_locked).",
            mode,
        )
        return mode
    if mode not in VALID_MODES:
        raise ValueError(
            f"AXIOM_V2_MODE must be one of {VALID_MODES}, got: {mode}. "
            f"LIVE mode is deferred to a future band."
        )
    return mode


def is_registered_locked(mode: str) -> bool:
    """AM-2 third-state tag: recognized, typed, behaviorally locked."""
    return mode in REGISTERED_LOCKED_MODES


def is_research(mode: str) -> bool:
    """Check if mode is RESEARCH."""
    return mode == "RESEARCH"


def is_simulation(mode: str) -> bool:
    """Check if mode is SIMULATION."""
    return mode == "SIMULATION"


def validate_mode_value(mode: str) -> str:
    """Validate a mode string. Returns the mode if valid."""
    if mode not in VALID_MODES:

        raise ValueError(
            f"Invalid mode: {mode}. Must be one of {VALID_MODES}"
        )
    return mode
