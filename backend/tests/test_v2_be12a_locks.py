"""V2 BE-12A lock-order chokepoint coupons (BO §4; DR-2; DA §2 law).

Order-fixture battery (L1-vs-L3, L2-vs-L6, kill-vs-all); mode_locked
computed ONLY from the mode contract (promenade: posture inputs cannot
manufacture mode answers); every lock's typed reason first-class;
AM-2 third-state pins; boundary-file tuples byte-identical recital.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from app.v2.live_exec.locks import (
    ACTUATION_CREDENTIAL_CLASSES,
    LOCK_ORDER,
    ActuationRefused,
    ActuationState,
    require_actuation,
)

BACKEND = Path(__file__).resolve().parents[1]

# The healthy-state fixture: every lock satisfied (test-only promenade —
# no such state is REACHABLE in fielded 12A; the coupon proves the door
# itself, not a fielded pathway).
_OPEN = dict(mode="PAPER", credential_class="practice_trade",
             activation_instrument_rows=1, funded_posture=True,
             killswitch_armed=False, sub_failures=())


def _state(**overrides) -> ActuationState:
    return ActuationState(**{**_OPEN, **overrides})


def _refusal(**overrides) -> ActuationRefused:
    with pytest.raises(ActuationRefused) as exc:
        require_actuation(_state(**overrides))
    return exc.value


# --- the pinned order itself ----------------------------------------------------


def test_lock_order_pinned_exactly():
    assert LOCK_ORDER == (
        "mode_locked", "posture_mismatch",
        "activation_instrument_not_in_force", "funded_posture_required",
        "killswitch_armed", "sub_contract_failure")


def test_all_locks_satisfied_passes():
    require_actuation(_state())  # no raise: the door opens only here


# --- each lock alone, typed -----------------------------------------------------


def test_l1_mode_locked_alone():
    refused = _refusal(mode="LIVE")
    assert refused.reason == "mode_locked"
    assert refused.lock == "mode_locked"


def test_l2_posture_mismatch_alone():
    refused = _refusal(credential_class=None)
    assert refused.reason == "posture_mismatch"


def test_l3_activation_absent_alone():
    refused = _refusal(activation_instrument_rows=0)
    assert refused.reason == "activation_instrument_not_in_force"


def test_l4_funded_posture_alone():
    refused = _refusal(funded_posture=False)
    assert refused.reason == "funded_posture_required"


def test_l5_killswitch_alone():
    refused = _refusal(killswitch_armed=True)
    assert refused.reason == "killswitch_armed"


def test_l6_sub_failure_alone_proxies_first_class():
    refused = _refusal(sub_failures=("sub_signing_failure",))
    assert refused.reason == "sub_signing_failure"
    assert refused.lock == "sub_contract_failure"
    assert refused.notes[0]["sub_classes"] == ["sub_signing_failure"]


# --- order fixtures (BO §4: fail L1 AND L3 -> mode_locked, etc.) -----------------


def test_order_l1_beats_l3():
    refused = _refusal(mode="LIVE", activation_instrument_rows=0)
    assert refused.reason == "mode_locked"


def test_order_l2_beats_l6():
    refused = _refusal(credential_class=None,
                       sub_failures=("sub_signing_failure",))
    assert refused.reason == "posture_mismatch"


def test_order_kill_vs_all_downstream():
    # L5 vs L6: kill beats sub-failures; everything upstream open.
    refused = _refusal(killswitch_armed=True,
                       sub_failures=("sub_signing_failure",))
    assert refused.reason == "killswitch_armed"


def test_order_all_locks_failing_answers_l1():
    refused = _refusal(mode="LIVE", credential_class=None,
                       activation_instrument_rows=0, funded_posture=False,
                       killswitch_armed=True,
                       sub_failures=("sub_signing_failure",))
    assert refused.reason == "mode_locked"


# --- the promenade: posture inputs cannot manufacture mode answers ---------------


def test_promenade_posture_cannot_make_mode_locked():
    """Every posture-flavored degradation with a lawful mode NEVER
    answers mode_locked — L1 truth comes ONLY from the mode contract."""
    for overrides in (
        {"credential_class": None},
        {"credential_class": "investor_read_only"},
        {"activation_instrument_rows": 0},
        {"funded_posture": False},
        {"killswitch_armed": True},
        {"sub_failures": ("sub_signing_failure",)},
    ):
        refused = _refusal(**overrides)
        assert refused.reason != "mode_locked", overrides


def test_promenade_mode_locked_regardless_of_perfect_posture():
    # perfect posture + LIVE = mode_locked (posture cannot unlock mode)
    refused = _refusal(mode="LIVE")
    assert refused.reason == "mode_locked"


# --- AM-2 third-state pins --------------------------------------------------------


def test_am2_third_state_tuples_byte_identical():
    """DR-F1 law recital: VALID_MODES / DEFERRED_MODES untouched;
    REGISTERED_LOCKED_MODES added; the credential classes closed."""
    from app.v2.mode.contract import (
        DEFERRED_MODES,
        REGISTERED_LOCKED_MODES,
        VALID_MODES,
    )
    assert VALID_MODES == ("RESEARCH", "SIMULATION", "PAPER")
    assert DEFERRED_MODES == ("LIVE",)
    assert REGISTERED_LOCKED_MODES == ("LIVE",)
    assert ACTUATION_CREDENTIAL_CLASSES == ("practice_trade",)


def test_am2_byte_pinned_wall_file_untouched():
    """BO §4 AM-2 closure: the BE-11 byte pin on
    tests/test_v2_be9_boundaries.py names the SAME sha — the file was
    not touched by this band (drift check by bytes, not by git)."""
    sha = hashlib.sha256(
        (BACKEND / "tests/test_v2_be9_boundaries.py").read_bytes()
    ).hexdigest()
    assert sha == ("9ba9fd8290d5861911582a5286752c7ed5aee71c06e"
                   "56acb9f4ac4337355f91f")


def test_am2_superseded_coupon_nowhere():
    """`test_mode_rejects_live` NOWHERE in the suite (BO §4: superseded
    by citation; the citation text is grep-able in test_v2_mode.py)."""
    needle = "def " + "test_mode_rejects_live" + "("  # split: the scan
    # must never carry its own needle (the BE-11 orderintent lesson)
    hits = []
    for path in (BACKEND / "tests").rglob("*.py"):
        if path.name == "test_v2_be12a_locks.py":
            continue  # this scanner
        text = path.read_text(encoding="utf-8")
        if needle in text:
            hits.append(path.name)
    assert hits == []
    mode_tests = (BACKEND / "tests/test_v2_mode.py").read_text(
        encoding="utf-8")
    assert "SUPERSEDES BY CITATION" in mode_tests
    assert "BO-V2-BE12A-001" in mode_tests
