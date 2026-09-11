"""V2 BE-12C engine + matrix coupons (BO §1.a–§1.d/§3).

Verb law (adapter-cited capability map); position verbs absent by
charter; unknown-state matrix fully typed (every cell); quarantine-hold
default; election law; act-identity idempotency; closed vocabularies;
two-lane non-commutation extension; 12E-workflow absence-with-pin.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from app.v2.live_exec.intents import LiveExecRefused
from app.v2.live_exec.modify.engine import (
    ACT_OUTCOMES,
    MODIFY_REFUSALS,
    MODIFY_VERBS,
    OPERATOR_ELECTIONS,
    act_identity,
    require_actionable,
    require_verb_capability,
)

BACKEND = Path(__file__).resolve().parents[1]


class _Sub:
    """Minimal submission shape for posture-gate coupons."""

    def __init__(self, terminal_state):
        self.terminal_state = terminal_state
        self.id = "sub-1"
        self.intent_id = "int-1"
        self.server_ack_ref = "ack-1"


# --- closed vocabularies (design-commit enumeration; F1 recital) --------------------


def test_closed_vocabularies_exact():
    assert MODIFY_VERBS == ("cancel", "modify")
    assert ACT_OUTCOMES == ("applied", "refused_terminal",
                            "unknown_outcome", "unknown_escalate")
    assert OPERATOR_ELECTIONS == ("standard", "cancel_on_unknown")
    # CR-1 (V2-BE12C-DEL-001/002): +act_target_mismatch,
    # +act_payload_field_not_supported. LOW-1 re-homed by documentation:
    # the tuple is the VOCABULARY UNION of act-refusal ids and
    # outcome-noun citizens (the three cancel_* outcome nouns are never
    # raised as refusals; documented in the engine).
    assert MODIFY_REFUSALS == (
        "submission_not_found", "modify_not_supported_state",
        "duplicate_modify_event", "cancel_refused_terminal",
        "cancel_on_unknown_applied", "cancel_unknown_outcome",
        "unknown_escalate", "act_target_mismatch",
        "act_payload_field_not_supported")


# --- the verb law: capability by CITED READ (BO §1.a / §4) ---------------------------


def test_capability_map_is_the_landed_adapter_object():
    """The boundary's map is the ADAPTER'S OWN object (cited read:
    app/v2/broker_read/providers/practice_actuator.py ::
    PRACTICE_ORDER_CAPABILITIES) — key-for-key, field-for-field; a
    handwritten copy diverging from the adapter would fail here."""
    from app.v2.broker_read.providers.practice_actuator import (
        PRACTICE_ORDER_CAPABILITIES,
    )
    from app.v2.live_exec.adapter_boundary import adapter_capability_map
    cited = adapter_capability_map()
    assert set(cited) == set(PRACTICE_ORDER_CAPABILITIES)
    for verb in cited:
        assert cited[verb] == dict(PRACTICE_ORDER_CAPABILITIES[verb])
    # the adapter evidences exactly the two order verbs, both scoped to
    # pending orders (the terminal contract's own mechanism)
    assert set(cited) == {"cancel", "modify"}
    for verb in cited:
        assert cited[verb]["applies_to"] == "pending_orders_only"


def test_position_verbs_absent_by_charter():
    """Refusal-pins proving ABSENCE: no position verb exists in the map,
    the engine, or the api surface (a close is a NEW opposite submission
    under 12B law — never a modify)."""
    from app.v2.live_exec.adapter_boundary import adapter_capability_map
    cited = adapter_capability_map()
    for absent in ("close", "close_position", "position_modify",
                   "position_close", "hedge"):
        assert absent not in cited
        with pytest.raises(LiveExecRefused) as exc:
            require_verb_capability(absent, cited)
        assert exc.value.reason == "modify_not_supported_state"
    # static arm: no position-verb tokens in the 12C package
    for f in (BACKEND / "app/v2/live_exec/modify").rglob("*.py"):
        text = f.read_text(encoding="utf-8").lower()
        for token in ("position_modify", "close_position",
                      "position_close("):
            assert token not in text, f"{token} in {f.name}"


def test_unsupported_verb_refuses_typed():
    with pytest.raises(LiveExecRefused) as exc:
        require_verb_capability("cancel", {"cancel": {"supported": False}})
    assert exc.value.reason == "modify_not_supported_state"
    with pytest.raises(LiveExecRefused) as exc:
        require_verb_capability("modify", {})
    assert exc.value.reason == "modify_not_supported_state"


# --- unknown-state matrix (BO §1.c: every cell typed) --------------------------------


def test_matrix_pending_states_admit_both_verbs():
    for state in ("accepted", "requote"):
        for verb in ("cancel", "modify"):
            for election in ("standard", "cancel_on_unknown"):
                assert require_actionable(_Sub(state), verb,
                                          election) == "pending"


def test_matrix_unknown_states_quarantine_hold_default():
    """QUARANTINE-HOLD: unknown posture + standard election refuses BOTH
    verbs; modify refuses even WITH the election (cancel-only recovery)."""
    for state in ("no_answer", "quarantined_unknown"):
        for verb, election in (("cancel", "standard"),
                               ("modify", "standard"),
                               ("modify", "cancel_on_unknown")):
            with pytest.raises(LiveExecRefused) as exc:
                require_actionable(_Sub(state), verb, election)
            assert exc.value.reason == "modify_not_supported_state", (
                state, verb, election)


def test_matrix_cancel_on_unknown_elected_admits():
    for state in ("no_answer", "quarantined_unknown"):
        assert require_actionable(
            _Sub(state), "cancel", "cancel_on_unknown") == "unknown_elected"


def test_matrix_terminal_states_refuse_all_cells():
    for verb in ("cancel", "modify"):
        for election in ("standard", "cancel_on_unknown"):
            with pytest.raises(LiveExecRefused) as exc:
                require_actionable(_Sub("rejected"), verb, election)
            assert exc.value.reason == "modify_not_supported_state"


# --- act identity (idempotency anchor) ------------------------------------------------


def test_act_identity_x3_and_moves():
    a1 = act_identity("sub-1", "cancel", {"order": "7"})
    a2 = act_identity("sub-1", "cancel", {"order": "7"})
    a3 = act_identity("sub-1", "cancel", {"order": "7"})
    assert a1 == a2 == a3
    assert act_identity("sub-2", "cancel", {"order": "7"}) != a1
    assert act_identity("sub-1", "modify", {"order": "7"}) != a1
    assert act_identity("sub-1", "cancel", {"order": "8"}) != a1


# --- actuator act-answer arms (closed; seam law) --------------------------------------


def test_actuator_act_arms_closed_and_seam_absorbs():
    import app.v2.broker_read.providers.practice_actuator as actuator

    class _Result:
        def __init__(self, retcode):
            self.retcode = retcode

    class _NoRetcode:
        pass

    class _FakeMt5:
        TRADE_RETCODE_DONE = 10009
        TRADE_ACTION_REMOVE = 8
        TRADE_ACTION_MODIFY = 7

        def __init__(self, answer):
            self._answer = answer

        def order_send(self, req):
            if isinstance(self._answer, Exception):
                raise self._answer
            return self._answer

    orig = actuator._terminal
    try:
        cases = ((_Result(10009), "applied"),
                 (_Result(10013), "refused_terminal"),
                 (None, "unknown_outcome"),
                 (_NoRetcode(), "unknown_outcome"),
                 (TimeoutError("t"), "unknown_outcome"))
        for answer, want in cases:
            actuator._terminal = lambda a=answer: _FakeMt5(a)
            for act in (actuator.practice_order_cancel,
                        actuator.practice_order_modify):
                record = act({"order": 7})
                assert record["outcome"] == want, (answer, act.__name__)
    finally:
        actuator._terminal = orig


# --- two-lane law extension (BO §1.d) --------------------------------------------------


def test_act_doorways_speak_practice_vocabulary_only():
    """Cancel/modify doorway refusals are practice-lane words — never a
    LIVE-lane reason (the 12B non-commutation corpus extended)."""
    from app.v2.live_exec.adapter_boundary import (
        cancel_doorway,
        modify_doorway,
    )
    from app.v2.live_exec.locks import (
        LOCK_ORDER,
        PracticeActuationRefused,
        PracticeActuationState,
    )
    for doorway in (cancel_doorway, modify_doorway):
        for overrides, want in (
            ({"mode": "RESEARCH"}, "practice_mode_not_armed"),
            ({"credential_state": "absent"}, "practice_posture_absent"),
            ({"lane": "live"}, "actuation_lane_mismatch"),
        ):
            state = PracticeActuationState(**{
                "lane": "practice", "mode": "PAPER",
                "credential_state": "present",
                "boundary_stance": "practice_wired",
                "basis_age_hours": 2.0, **overrides})
            with pytest.raises(PracticeActuationRefused) as exc:
                doorway(state, {})
            assert exc.value.reason == want
            assert exc.value.reason not in LOCK_ORDER


def test_live_door_untouched_by_12c():
    from app.v2.live_exec.locks import (
        LOCK_ORDER,
        ActuationRefused,
        ActuationState,
        require_actuation,
    )
    assert LOCK_ORDER == (
        "mode_locked", "posture_mismatch",
        "activation_instrument_not_in_force", "funded_posture_required",
        "killswitch_armed", "sub_contract_failure")
    with pytest.raises(ActuationRefused) as exc:
        require_actuation(ActuationState(mode="LIVE"))
    assert exc.value.reason == "mode_locked"


# --- 12E absence-with-pin (BO §4) ------------------------------------------------------


def test_12e_workflow_present_by_its_own_order():
    """SUPERSEDES BY CITATION under BO-V2-BE12E-001 (the 12C
    absence-with-pin coupon's absence claim EXPIRED lawfully when 12E's
    own BO built the workflow). The SURVIVING half of the 12C law
    stands: the MODIFY package still never links the workflow — a
    parity_break/unknown_escalate is QUOTED by an operator, never
    linked by the machine (SS1.d.4 evidence-only law)."""
    package = BACKEND / "app/v2/live_exec"
    # the 12E packages now lawfully exist (their own BO)
    assert (package / "incident").exists()
    assert (package / "reconcile").exists()
    # the surviving 12C arm: modify/ never speaks workflow verbs
    for f in (package / "modify").rglob("*.py"):
        text = f.read_text(encoding="utf-8").lower()
        for token in ("incident_workflow", "open_incident(",
                      "recovery_path"):
            assert token not in text, f"{token} in {f.name}"


# --- register line + walls + F1 recitals (BO §3/§5) ----------------------------------


def test_register_line_superseded_pointer():
    """SUPERSEDED BY CITATION under BO-V2-BE12D-001 §2 (prose refreshed
    at 12E CR-1 per REV §6.3): the exact-form pin chain now runs 12C →
    12D pointer (`test_register_line_superseded_pointer_12d`) → the 12E
    corpus (`test_register_line_12e_honesty_pair_exact`, carrying the
    DR-3(i) honesty clause); the structural-invariants pin stands in
    the 12B corpus. This pointer keeps the supersession grep-able
    (LIVE=REGISTERED_LOCKED and the funded-account invariant recited
    here as the standing floor)."""
    from app.v2.live_exec.api import _REGISTER_LINE
    assert "LIVE=REGISTERED_LOCKED" in _REGISTER_LINE
    assert "funded account: NONE" in _REGISTER_LINE


def test_capability_cited_read_names_the_adapter_file():
    """BO §4: the coupon NAMES the adapter file — the map object is
    imported from `app/v2/broker_read/providers/practice_actuator.py`
    and the boundary's reader carries the module path literally (a
    handwritten map elsewhere = defect; scan proves no second map)."""
    boundary = (BACKEND / "app/v2/live_exec/adapter_boundary.py"
                ).read_text(encoding="utf-8")
    assert "PRACTICE_ORDER_CAPABILITIES" in boundary
    assert "broker_read.providers.practice_actuator" in boundary
    # no second capability literal anywhere in live_exec outside the
    # boundary's cited read
    for f in (BACKEND / "app/v2/live_exec").rglob("*.py"):
        if f.name == "adapter_boundary.py":
            continue
        assert "PRACTICE_ORDER_CAPABILITIES" not in f.read_text(
            encoding="utf-8"), f.name


def test_wall_modify_package_no_provider_tokens():
    """The 12B wall law extends over the new package: zero provider/
    terminal tokens in modify/ (the boundary stays the one doorway)."""
    package = BACKEND / "app/v2/live_exec/modify"
    banned = ("broker_read.providers", "MetaTrader5", "mt5",
              "external_integration", "broker_read.sync",
              "broker_read.vault", "paper_trading.simulator",
              "order_send", "TRADE_ACTION")
    offenders = []
    for path in package.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for needle in banned:
            if needle in text:
                offenders.append(f"{path.name}:{needle}")
    assert offenders == []


def test_f1_full_active_refuse_set_all_lanes_and_acts():
    """F1 recital: the complete ACTIVE refuse vocabulary over LIVE lane
    + PRACTICE lane + 12C acts, enumerated closed and disjoint."""
    from app.v2.live_exec.locks import LOCK_ORDER, PRACTICE_LOCK_ORDER
    live, practice = set(LOCK_ORDER), set(PRACTICE_LOCK_ORDER)
    acts = set(MODIFY_REFUSALS)
    assert live & practice == set()
    assert live & acts == set()
    assert practice & acts == set()
    assert len(live | practice | acts) == 6 + 5 + 9  # CR-1: +2
