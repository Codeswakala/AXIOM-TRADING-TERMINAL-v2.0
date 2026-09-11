"""V2 BE-12A engine coupons (BO §1.b/§1.c/§4).

Intent chassis + digest ×3 per-world; idempotency/duplicate refusal;
step-up shape law; eligibility typed refusals (BOP law); pre-trade
risk declines + positive-reason pair; AM-3 registry; AM-4 credential
class hygiene; adapter boundary posture-stub.
"""

from __future__ import annotations

import pytest

from app.v2.live_exec.eligibility import (
    ELIGIBILITY_REFUSALS,
    require_eligibility,
)
from app.v2.live_exec.intents import (
    INTENT_REFUSALS,
    LXE_ENGINE_TUPLE,
    LiveExecRefused,
    intent_digest,
    require_step_up,
)
from app.v2.live_exec.risk import (
    RISK_DECLINES,
    RISK_STATES,
    evaluate_pre_trade_risk,
)

_ELIGIBLE = dict(account_present=True, account_posture_class="practice",
                 instrument_mapped=True, session_open=True,
                 basis_present=True, basis_age_hours=2.0,
                 max_age_hours=48.0)


# --- closed vocabularies (three-layer enumeration law) ----------------------------


def test_closed_enums_exact():
    assert INTENT_REFUSALS == ("duplicate_intent",
                               "step_up_reference_absent")
    assert ELIGIBILITY_REFUSALS == (
        "account_ineligible", "instrument_ineligible",
        "session_ineligible", "basis_stale")
    assert RISK_DECLINES == (
        "notional_exceeds_available_margin", "quantity_not_positive",
        "citation_currency_differs_from_basis")
    assert RISK_STATES == ("risk_evaluated", "risk_declined")
    assert LXE_ENGINE_TUPLE == ("pxs-1.0.0", "lxe-1.0.0")


# --- digest law (N-O13 per-world) --------------------------------------------------


def test_digest_x3_and_moves_on_change():
    payload = {"instrument": "forex.eurusd", "quantity": "100.00"}
    d1 = intent_digest("basis-1", payload)
    d2 = intent_digest("basis-1", payload)
    d3 = intent_digest("basis-1", payload)
    assert d1 == d2 == d3
    assert intent_digest("basis-2", payload) != d1
    assert intent_digest("basis-1", {**payload, "quantity": "101.00"}) != d1


# --- step-up shape law (R-3.4; V2-TD-29 adopted line) ------------------------------


def test_step_up_absent_refuses_typed():
    for absent in (None, "", "   "):
        with pytest.raises(LiveExecRefused) as exc:
            require_step_up(absent)
        assert exc.value.reason == "step_up_reference_absent"
    assert require_step_up("  mfa-ref-1  ") == "mfa-ref-1"


# --- eligibility (BOP law: present, not stale) --------------------------------------


def test_eligibility_passes_when_whole():
    answer = require_eligibility(**_ELIGIBLE)
    assert answer == {"eligibility_state": "eligible"}


def test_eligibility_refusals_typed():
    """All seven refusal arms, loop-form (one coupon: suite-stair law)."""
    cases = [
        ({"account_present": False}, "account_ineligible"),
        ({"account_posture_class": None}, "account_ineligible"),
        ({"instrument_mapped": False}, "instrument_ineligible"),
        ({"session_open": False}, "session_ineligible"),
        ({"basis_present": False}, "basis_stale"),
        ({"basis_age_hours": None}, "basis_stale"),
        ({"basis_age_hours": 49.0}, "basis_stale"),
    ]
    for override, reason in cases:
        with pytest.raises(LiveExecRefused) as exc:
            require_eligibility(**{**_ELIGIBLE, **override})
        assert exc.value.reason == reason, override


# --- pre-trade risk (money-units; BE-11 flat-account law) ---------------------------


def test_risk_evaluated_with_positive_facts():
    answer = evaluate_pre_trade_risk(
        quantity="100", cited_price="1.10", price_currency="USD",
        basis_currency="USD", margin_available="10000.0")
    assert answer["risk_state"] == "risk_evaluated"
    assert answer["declines"] == []
    assert answer["positive_facts"] == {
        "quantity_positive": True, "currency_matched": True,
        "notional_within_available": True}
    assert answer["notional"] == "110.00"


def test_risk_declines_typed():
    """All three decline arms, loop-form (one coupon: suite-stair law)."""
    cases = [
        (dict(quantity="0", cited_price="1.10", price_currency="USD",
              basis_currency="USD", margin_available="10000.0"),
         "quantity_not_positive"),
        (dict(quantity="100", cited_price="1.10", price_currency="EUR",
              basis_currency="USD", margin_available="10000.0"),
         "citation_currency_differs_from_basis"),
        (dict(quantity="100000", cited_price="1.10", price_currency="USD",
              basis_currency="USD", margin_available="10000.0"),
         "notional_exceeds_available_margin"),
    ]
    for kwargs, decline in cases:
        answer = evaluate_pre_trade_risk(**kwargs)
        assert answer["risk_state"] == "risk_declined"
        assert decline in answer["declines"]


def test_risk_nondecimal_refuses_typed():
    with pytest.raises(LiveExecRefused) as exc:
        evaluate_pre_trade_risk(
            quantity="not-a-number", cited_price="1.10",
            price_currency="USD", basis_currency="USD",
            margin_available="10000.0")
    assert exc.value.reason == "quantity_not_positive"


# --- AM-3 / AM-4 / boundary stubs ---------------------------------------------------


def test_am4_practice_trade_class_registered_and_absent():
    """AM-4: class registered; 12A resolution fail-closes ABSENT;
    investor class intact; funded class NOWHERE in the tuple."""
    from app.v2.broker_read.vault import (
        CREDENTIAL_CLASSES,
        resolve_practice_trade_credential,
    )
    assert CREDENTIAL_CLASSES == ("investor_read_only", "practice_trade")
    assert "funded" not in " ".join(CREDENTIAL_CLASSES)
    resolved = resolve_practice_trade_credential()
    assert resolved.state == "absent"
    # repr-blind law holds on the returned type
    assert "password" not in repr(resolved)


def test_am4_doorway_hygiene_12b():
    """AM-4 doorway hygiene (12B edition).

    SUPERSEDES BY CITATION: the 12A no-env/no-file stub coupon —
    superseded under BO-V2-BE12B-001 SS1.e (the ABSENT stub moved to the
    real sealed doorway BY CITED EDIT). The hygiene law now reads:
    fail-closed on every absence arm; env names ONLY the practice path
    var; no provider import; the investor AAD is structurally disjoint.
    """
    import inspect

    from app.v2.broker_read import vault
    body = inspect.getsource(vault.resolve_practice_trade_credential)
    # the ONLY env surface is the practice path var
    assert "AXIOM_BROKER_PRACTICE_VAULT_PATH" in body
    assert "AXIOM_BROKER_VAULT_PATH\"" not in body  # investor var untouched here
    for token in ("MetaTrader5", "mt5", "import requests"):
        assert token not in body
    # fail-closed arms: no passphrase / no env / no file => ABSENT
    assert vault.resolve_practice_trade_credential().state == "absent"
    assert vault.resolve_practice_trade_credential("pw").state == "absent"


def test_adapter_boundary_practice_wired_still_gated():
    """12B stance (SUPERSEDES BY CITATION the 12A posture-stub coupon —
    BO-V2-BE12B-001 SS1.b cited edit). The boundary is practice_wired
    but every doorway call STILL demands a practice-lane pass; a
    lane-less/mode-less ask refuses in practice vocabulary, and the
    LIVE lane has no path here at all."""
    from app.v2.live_exec.adapter_boundary import (
        BOUNDARY_STANCE,
        BOUNDARY_STANCES,
        submission_doorway,
    )
    from app.v2.live_exec.locks import (
        PracticeActuationRefused,
        PracticeActuationState,
    )
    assert BOUNDARY_STANCES == ("posture_stub", "practice_wired",
                                "activation_scoped")
    assert BOUNDARY_STANCE == "practice_wired"
    with pytest.raises(PracticeActuationRefused) as exc:
        submission_doorway(PracticeActuationState(
            lane="practice", mode="RESEARCH"), {})
    assert exc.value.reason == "practice_mode_not_armed"


def test_am3_registry_two_keys_live_names_boundary():
    from app.v2.paper_trading.contracts import EXECUTION_BACKENDS
    assert dict(EXECUTION_BACKENDS) == {
        "paper": "app.v2.paper_trading.simulator",
        "live": "app.v2.live_exec.adapter_boundary"}
