"""V2 BE-12B boundary-wiring + vault-doorway coupons (BO §1.b/§1.e/§4).

Stance practice_wired by cited edit; amended walls hold with the
one-file exception pinned; the doorway demands the lane pass; terminal
absence answers typed `practice_terminal_unavailable`; refusal-
injection battery (DR-3); vault doorway real-resolution arms + investor
law untouched (investor payload cannot manufacture practice
resolution).
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from app.v2.live_exec.adapter_boundary import (
    BOUNDARY_STANCE,
    BOUNDARY_STANCES,
    AdapterBoundaryRefused,
    submission_doorway,
)
from app.v2.live_exec.locks import (
    PracticeActuationRefused,
    PracticeActuationState,
)

BACKEND = Path(__file__).resolve().parents[1]

_ARMED = dict(lane="practice", mode="PAPER", credential_state="present",
              boundary_stance="practice_wired", basis_age_hours=2.0)


# --- stance + wiring shape -----------------------------------------------------------


def test_stance_practice_wired_by_cited_edit():
    assert BOUNDARY_STANCES == ("posture_stub", "practice_wired",
                                "activation_scoped")
    assert BOUNDARY_STANCE == "practice_wired"


def test_boundary_reaches_terminal_only_via_provider_leg():
    """No terminal package token in the boundary file; the ONLY
    provider-shaped token is the sanctioned actuator module path."""
    text = (BACKEND / "app/v2/live_exec/adapter_boundary.py").read_text(
        encoding="utf-8")
    assert "broker_read.providers.practice_actuator" in text
    for banned in ("MetaTrader5", "import mt5", "mt5.order_send"):
        assert banned not in text
    # actuator lives INSIDE the sanctioned provider family
    assert (BACKEND / "app/v2/broker_read/providers/"
                      "practice_actuator.py").exists()


# --- refusal-injection battery (DR-3 law; BO §1.f arms) --------------------------------


def test_injection_no_credential():
    with pytest.raises(PracticeActuationRefused) as exc:
        submission_doorway(PracticeActuationState(
            **{**_ARMED, "credential_state": "absent"}), {})
    assert exc.value.reason == "practice_posture_absent"


def test_injection_boundary_not_wired():
    with pytest.raises(PracticeActuationRefused) as exc:
        submission_doorway(PracticeActuationState(
            **{**_ARMED, "boundary_stance": "posture_stub"}), {})
    assert exc.value.reason == "practice_boundary_not_wired"


def test_injection_mode_not_armed():
    with pytest.raises(PracticeActuationRefused) as exc:
        submission_doorway(PracticeActuationState(
            **{**_ARMED, "mode": "RESEARCH"}), {})
    assert exc.value.reason == "practice_mode_not_armed"


def test_injection_stale_basis():
    with pytest.raises(PracticeActuationRefused) as exc:
        submission_doorway(PracticeActuationState(
            **{**_ARMED, "basis_age_hours": 30.0}), {})
    assert exc.value.reason == "basis_stale"


def test_injection_terminal_unreachable_typed():
    """Full lane pass on THIS station (no MT5 package) => the doorway
    answers the typed practice_terminal_unavailable — E-ENV-1 law,
    practice vocabulary, never an exception from the seam."""
    with pytest.raises(AdapterBoundaryRefused) as exc:
        submission_doorway(PracticeActuationState(**_ARMED), {})
    assert exc.value.reason == "practice_terminal_unavailable"


def test_injection_retcode_absent_is_a_state():
    """The actuator's seam law: absent retcode / None result / transport
    exception all return the `no_answer` STATE record (quarantine is the
    caller's transition; no exception crosses the seam)."""
    import app.v2.broker_read.providers.practice_actuator as actuator

    class _NoRetcode:
        pass

    class _FakeMt5:
        TRADE_RETCODE_DONE = 10009
        TRADE_RETCODE_REQUOTE = 10004

        def __init__(self, answer):
            self._answer = answer

        def order_send(self, req):
            if isinstance(self._answer, Exception):
                raise self._answer
            return self._answer

    orig = actuator._terminal
    try:
        for answer, want in ((None, "no_answer"),
                             (_NoRetcode(), "no_answer"),
                             (TimeoutError("t"), "no_answer")):
            actuator._terminal = lambda a=answer: _FakeMt5(a)
            record = actuator.practice_order_send({})
            assert record["terminal_state"] == want, answer
    finally:
        actuator._terminal = orig


def test_actuator_retcode_arms_closed():
    """accepted / requote / rejected arms from the closed vocabulary."""
    import app.v2.broker_read.providers.practice_actuator as actuator

    class _Result:
        def __init__(self, retcode, order=""):
            self.retcode = retcode
            self.order = order

    class _FakeMt5:
        TRADE_RETCODE_DONE = 10009
        TRADE_RETCODE_REQUOTE = 10004

        def __init__(self, result):
            self._result = result

        def order_send(self, req):
            return self._result

    orig = actuator._terminal
    try:
        for retcode, want in ((10009, "accepted"), (10004, "requote"),
                              (10013, "rejected")):
            actuator._terminal = (
                lambda r=retcode: _FakeMt5(_Result(r, order="7")))
            record = actuator.practice_order_send({})
            assert record["terminal_state"] == want
            if want == "accepted":
                assert record["server_ack_ref"] == "7"
    finally:
        actuator._terminal = orig


# --- AM-4 vault doorway (BO §1.e/§4) ---------------------------------------------------


def test_vault_doorway_seals_and_resolves(tmp_path):
    from app.v2.broker_read.vault import (
        resolve_practice_trade_credential,
        seal_practice_vault_bytes,
    )
    payload = seal_practice_vault_bytes(
        "gate-passphrase", "practice-trade-secret-1", "999001",
        "PracticeServer-1")
    vault_file = tmp_path / "practice.vault"
    vault_file.write_bytes(payload)
    prior = os.environ.get("AXIOM_BROKER_PRACTICE_VAULT_PATH")
    os.environ["AXIOM_BROKER_PRACTICE_VAULT_PATH"] = str(vault_file)
    try:
        resolved = resolve_practice_trade_credential("gate-passphrase")
        assert resolved.state == "present"
        assert resolved.account_number == "999001"
        # repr-blind law holds on the doorway's return
        assert "practice-trade-secret-1" not in repr(resolved)
        assert "practice-trade-secret-1" not in str(resolved)
        # wrong passphrase => ABSENT (never an exception with material)
        assert resolve_practice_trade_credential("wrong").state == "absent"
        # tamper => ABSENT
        vault_file.write_bytes(payload[:-1] + bytes([payload[-1] ^ 1]))
        assert resolve_practice_trade_credential(
            "gate-passphrase").state == "absent"
    finally:
        if prior is None:
            os.environ.pop("AXIOM_BROKER_PRACTICE_VAULT_PATH", None)
        else:
            os.environ["AXIOM_BROKER_PRACTICE_VAULT_PATH"] = prior


def test_vault_fail_closed_arms():
    from app.v2.broker_read.vault import resolve_practice_trade_credential
    prior = os.environ.pop("AXIOM_BROKER_PRACTICE_VAULT_PATH", None)
    try:
        assert resolve_practice_trade_credential().state == "absent"
        assert resolve_practice_trade_credential("pw").state == "absent"
        os.environ["AXIOM_BROKER_PRACTICE_VAULT_PATH"] = "/nonexistent/x"
        assert resolve_practice_trade_credential("pw").state == "absent"
    finally:
        os.environ.pop("AXIOM_BROKER_PRACTICE_VAULT_PATH", None)
        if prior is not None:
            os.environ["AXIOM_BROKER_PRACTICE_VAULT_PATH"] = prior


def test_investor_payload_cannot_manufacture_practice(tmp_path):
    """Coupon-pinned investor law: an INVESTOR-sealed payload presented
    at the practice doorway resolves ABSENT (AAD disjoint) — reading
    the investor payload cannot manufacture practice resolution."""
    from app.v2.broker_read.vault import (
        resolve_practice_trade_credential,
        seal_vault_bytes,
    )
    investor_payload = seal_vault_bytes(
        "gate-passphrase", "investor-read-only-secret", "476910140",
        "ExnessKE-MT5Trial9")
    vault_file = tmp_path / "masquerade.vault"
    vault_file.write_bytes(investor_payload)
    prior = os.environ.get("AXIOM_BROKER_PRACTICE_VAULT_PATH")
    os.environ["AXIOM_BROKER_PRACTICE_VAULT_PATH"] = str(vault_file)
    try:
        assert resolve_practice_trade_credential(
            "gate-passphrase").state == "absent"
    finally:
        if prior is None:
            os.environ.pop("AXIOM_BROKER_PRACTICE_VAULT_PATH", None)
        else:
            os.environ["AXIOM_BROKER_PRACTICE_VAULT_PATH"] = prior


def test_practice_payload_cannot_open_as_investor(tmp_path):
    """The other direction: a practice payload at the INVESTOR opener
    resolves ABSENT (AAD disjoint both ways)."""
    from app.v2.broker_read.vault import (
        open_vault_bytes,
        seal_practice_vault_bytes,
    )
    payload = seal_practice_vault_bytes(
        "gate-passphrase", "practice-trade-secret-2", "999002", "S")
    assert open_vault_bytes("gate-passphrase", payload).state == "absent"


def test_no_credential_api_surface():
    """Registration stays console-act posture: no live_exec API model
    carries a passphrase/password field."""
    text = (BACKEND / "app/v2/live_exec/api.py").read_text(encoding="utf-8")
    for token in ("passphrase: str", "password", "trade_password"):
        assert token not in text
