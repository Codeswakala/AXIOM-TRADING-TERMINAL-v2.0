"""V2 BE-12B two-lane chokepoint coupons (BO §1.a/§4).

The LIVE lane is the 12A door UNCHANGED; the PRACTICE lane speaks its
own closed vocabulary; THE LANES' REFUSALS NEVER COMMUTE (coupon-pinned
both directions). Practice-lane arms each fire alone and in pinned
order; the full ACTIVE refusal set over both lanes enumerated closed.
"""

from __future__ import annotations

import pytest

from app.v2.live_exec.locks import (
    LOCK_ORDER,
    PRACTICE_LOCK_ORDER,
    ActuationRefused,
    ActuationState,
    PracticeActuationRefused,
    PracticeActuationState,
    require_actuation,
    require_practice_actuation,
)

# A fully-armed practice state (every lock satisfied).
_ARMED = dict(lane="practice", mode="PAPER", credential_state="present",
              boundary_stance="practice_wired", basis_age_hours=2.0)


def _p_state(**overrides) -> PracticeActuationState:
    return PracticeActuationState(**{**_ARMED, **overrides})


def _p_refusal(**overrides) -> PracticeActuationRefused:
    with pytest.raises(PracticeActuationRefused) as exc:
        require_practice_actuation(_p_state(**overrides))
    return exc.value


# --- the closed lane vocabularies (three-layer enumeration law) --------------------


def test_lane_vocabularies_closed_and_disjoint():
    assert PRACTICE_LOCK_ORDER == (
        "actuation_lane_mismatch", "practice_mode_not_armed",
        "practice_posture_absent", "practice_boundary_not_wired",
        "basis_stale")
    # LIVE lane unchanged from 12A — recited exact
    assert LOCK_ORDER == (
        "mode_locked", "posture_mismatch",
        "activation_instrument_not_in_force", "funded_posture_required",
        "killswitch_armed", "sub_contract_failure")
    # the two vocabularies share NO member (basis_stale is practice-lane
    # only at the chokepoint; the LIVE door has no basis arm)
    assert set(PRACTICE_LOCK_ORDER) & set(LOCK_ORDER) == set()


def test_full_active_refusal_set_enumerated_closed():
    """F1 recital: the ACTIVE refuse set over both lanes, closed."""
    live = set(LOCK_ORDER)
    practice = set(PRACTICE_LOCK_ORDER)
    assert len(live | practice) == 11  # 6 + 5, disjoint


# --- practice lane arms, each alone, in order ---------------------------------------


def test_practice_all_armed_passes():
    require_practice_actuation(_p_state())  # no raise


def test_p1_lane_mismatch_alone():
    refused = _p_refusal(lane="live")
    assert refused.reason == "actuation_lane_mismatch"


def test_p2_mode_not_armed_alone():
    refused = _p_refusal(mode="RESEARCH")
    assert refused.reason == "practice_mode_not_armed"


def test_p3_posture_absent_alone():
    refused = _p_refusal(credential_state="absent")
    assert refused.reason == "practice_posture_absent"


def test_p4_boundary_not_wired_alone():
    refused = _p_refusal(boundary_stance="posture_stub")
    assert refused.reason == "practice_boundary_not_wired"


def test_p5_basis_stale_and_absent_arms():
    assert _p_refusal(basis_age_hours=25.0).reason == "basis_stale"
    assert _p_refusal(basis_age_hours=None).reason == "basis_stale"


def test_practice_order_first_failure_wins():
    refused = _p_refusal(mode="RESEARCH", credential_state="absent",
                         boundary_stance="posture_stub")
    assert refused.reason == "practice_mode_not_armed"
    refused = _p_refusal(lane="live", mode="RESEARCH")
    assert refused.reason == "actuation_lane_mismatch"


# --- THE NON-COMMUTATION LAW (BO §1.a: lanes never answer each other) ----------------


def test_lanes_never_commute_practice_side():
    """Every practice-lane refusal is a practice-vocabulary member —
    NEVER a LIVE-lane reason, whatever the degradation mix."""
    for overrides in (
        {"lane": "live"}, {"mode": "RESEARCH"},
        {"credential_state": "absent"},
        {"boundary_stance": "posture_stub"},
        {"basis_age_hours": None},
        {"mode": "LIVE"},  # even a LIVE-mode string answers in practice vocabulary
    ):
        refused = _p_refusal(**overrides)
        assert refused.reason in PRACTICE_LOCK_ORDER, overrides
        assert refused.reason not in LOCK_ORDER, overrides
        assert isinstance(refused, PracticeActuationRefused)


def test_lanes_never_commute_live_side():
    """The LIVE door still answers ONLY its 12A vocabulary — practice-
    flavored degradations cannot make it speak practice words."""
    with pytest.raises(ActuationRefused) as exc:
        require_actuation(ActuationState(mode="LIVE",
                                         credential_class="practice_trade"))
    assert exc.value.reason == "mode_locked"
    assert exc.value.reason not in PRACTICE_LOCK_ORDER
    with pytest.raises(ActuationRefused) as exc:
        require_actuation(ActuationState(mode="PAPER", credential_class=None))
    assert exc.value.reason == "posture_mismatch"
    assert exc.value.reason not in PRACTICE_LOCK_ORDER


def test_live_lane_byte_posture_unchanged_from_12a():
    """The LIVE door's answers are exactly the 12A battery (recital):
    all-six-failing still answers L1; kill still beats sub_*."""
    with pytest.raises(ActuationRefused) as exc:
        require_actuation(ActuationState(
            mode="LIVE", credential_class=None,
            activation_instrument_rows=0, funded_posture=False,
            killswitch_armed=True, sub_failures=("sub_signing_failure",)))
    assert exc.value.reason == "mode_locked"


# --- digest + register-line + F1 coupons (BO §3/§5) ---------------------------------


def test_submission_digest_x3_and_moves():
    """N-O13 per-world: submission digest deterministic ×3; moves on
    intent, request, and terminal-state change."""
    from app.v2.live_exec.submissions import submission_digest
    d1 = submission_digest("i-1", {"v": 1}, "accepted")
    d2 = submission_digest("i-1", {"v": 1}, "accepted")
    d3 = submission_digest("i-1", {"v": 1}, "accepted")
    assert d1 == d2 == d3
    assert submission_digest("i-2", {"v": 1}, "accepted") != d1
    assert submission_digest("i-1", {"v": 2}, "accepted") != d1
    assert submission_digest("i-1", {"v": 1}, "rejected") != d1


def test_fill_identity_anchor_substantive_projection():
    """The dedupe anchor hashes the SUBSTANTIVE facts (N-O1 lesson:
    volatile-in-blob cannot flip identities; same facts => same
    identity even when noise fields differ)."""
    from app.v2.live_exec.ack_fills import fill_event_identity
    facts = {"deal_id": "D1", "order_id": "O1", "volume": "0.01",
             "price": "1.1", "time": "t1"}
    a = fill_event_identity("server_ack_ref", "ack-1", facts)
    b = fill_event_identity("server_ack_ref", "ack-1",
                            {**facts, "noise": "volatile-comment"})
    assert a == b
    assert fill_event_identity("server_ack_ref", "ack-1",
                               {**facts, "volume": "0.02"}) != a
    assert fill_event_identity("terminal_order_id", "ack-1", facts) != a


def test_register_line_current_form_on_envelopes():
    """SUPERSEDES BY CITATION the 12B-form pin (BO-V2-BE12C-001 SS5) and
    AMENDED BY CITATION at 12D (BO-V2-BE12D-001 SS5: the ordered line
    carries the activation posture, not the practice token). The
    LINE invariants: LIVE=REGISTERED_LOCKED + funded account: NONE.
    The PRACTICE=WIRED fact moves to its STRUCTURAL home — the boundary
    stance literal — which this coupon pins directly (the fact stands;
    only its carriage moved, per the BO's ordered text)."""
    from app.v2.live_exec.adapter_boundary import BOUNDARY_STANCE
    from app.v2.live_exec.api import _REGISTER_LINE
    for invariant in ("LIVE=REGISTERED_LOCKED", "funded account: NONE"):
        assert invariant in _REGISTER_LINE
    assert _REGISTER_LINE.startswith("BE-12")
    assert BOUNDARY_STANCE == "practice_wired"  # the fact, structurally


def test_f1_all_12b_refusals_register_recoverable():
    """F1 recital: every 12B refusal id is a closed-tuple member —
    CWS-recoverable from the register, no free-text reasons."""
    from app.v2.live_exec.ack_fills import FILL_REFUSALS
    from app.v2.live_exec.submissions import SUBMISSION_REFUSALS
    assert SUBMISSION_REFUSALS == ("intent_not_found",
                                   "duplicate_submission")
    assert FILL_REFUSALS == ("duplicate_fill_event",)
    # boundary + lane citizens
    assert "practice_terminal_unavailable" not in PRACTICE_LOCK_ORDER
    # (it is a BOUNDARY refusal, not a lane lock — separable by design)


def test_no_live_lane_path_into_boundary():
    """The boundary's doorway signature demands a PracticeActuationState;
    a LIVE-lane ActuationState is not accepted anywhere in the package
    (static arm: the boundary file never names the LIVE-door types)."""
    from pathlib import Path
    text = (Path(__file__).resolve().parents[1] /
            "app/v2/live_exec/adapter_boundary.py").read_text(
        encoding="utf-8")
    for live_token in ("require_actuation(", "ActuationState(",
                       " ActuationRefused"):
        assert live_token not in text.replace(
            "PracticeActuationState", "").replace(
            "PracticeActuationRefused", "").replace(
            "require_practice_actuation", "")
