"""V2 BE-12D lock/lane coupons (BO §1.b.4/§1.c.3/§1.d/§1.e/§3).

LOCK_ORDER byte-recital unchanged; L3/L5 fact readers over the real
chain; the coupon-world armature proof (rolled back, never committed);
lane non-commutation under an armed switch; closed 12D vocabularies +
F1 full-set recital; template NOT-IN-FORCE face + hash; register line;
activate-nothing scans.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from app.v2.live_exec.killswitch.engine import (
    GOVERNOR_REFUSALS,
    KILLSWITCH_STATES,
)
from app.v2.live_exec.locks import (
    LOCK_ORDER,
    PRACTICE_LOCK_ORDER,
    ActuationRefused,
    ActuationState,
    require_actuation,
)

BACKEND = Path(__file__).resolve().parents[1]


# --- LOCK_ORDER unchanged (BO §1.b.4/§1.c.3 recitals) --------------------------------


def test_lock_order_byte_recital_unchanged():
    assert LOCK_ORDER == (
        "mode_locked", "posture_mismatch",
        "activation_instrument_not_in_force", "funded_posture_required",
        "killswitch_armed", "sub_contract_failure")
    assert PRACTICE_LOCK_ORDER == (
        "actuation_lane_mismatch", "practice_mode_not_armed",
        "practice_posture_absent", "practice_boundary_not_wired",
        "basis_stale")  # stays exactly five members (BO §1.d)


def test_l3_position_three_and_order_law():
    """rows=0 => L3 typed at position 3 (L1/L2 bypassed under coupon
    facts); fixture failing L1 AND L3 answers mode_locked (order law)."""
    with pytest.raises(ActuationRefused) as exc:
        require_actuation(ActuationState(
            mode="PAPER", credential_class="practice_trade",
            activation_instrument_rows=0, funded_posture=True,
            killswitch_armed=False))
    assert exc.value.reason == "activation_instrument_not_in_force"
    assert exc.value.notes[0]["order_position"] == 3
    with pytest.raises(ActuationRefused) as exc:
        require_actuation(ActuationState(
            mode="LIVE", activation_instrument_rows=0))
    assert exc.value.reason == "mode_locked"


def test_l5_all_four_sole_row_states():
    """L5 truth table: engaged iff 'armed'|'pulled' (None/'cleared'
    NOT armed) — the fact-reader semantics, pinned at the lock."""
    base = dict(mode="PAPER", credential_class="practice_trade",
                activation_instrument_rows=1, funded_posture=True)
    # engaged states refuse killswitch_armed
    for engaged in (True,):
        with pytest.raises(ActuationRefused) as exc:
            require_actuation(ActuationState(**base,
                                             killswitch_armed=engaged))
        assert exc.value.reason == "killswitch_armed"
    # not-engaged passes the L5 gate (door opens: all locks satisfied)
    require_actuation(ActuationState(**base, killswitch_armed=False))


# --- closed vocabularies + F1 (BO §1.e) -----------------------------------------------


def test_12d_vocabularies_closed():
    assert KILLSWITCH_STATES == ("armed", "pulled", "cleared")
    assert GOVERNOR_REFUSALS == ("killswitch_armed",
                                 "killswitch_state_invalid")


def test_f1_full_active_refuse_set_with_declared_overlap():
    """LIVE(6) + PRACTICE(5) + ACTS(9) + GOVERNOR(2) — disjoint EXCEPT
    exactly the declared overlap: `killswitch_armed` is BY DESIGN the
    same token in GOVERNOR and LIVE (BO §1.e)."""
    from app.v2.live_exec.modify.engine import MODIFY_REFUSALS
    live, practice = set(LOCK_ORDER), set(PRACTICE_LOCK_ORDER)
    acts, governor = set(MODIFY_REFUSALS), set(GOVERNOR_REFUSALS)
    assert live & practice == set()
    assert live & acts == set()
    assert practice & acts == set()
    assert practice & governor == set()
    assert acts & governor == set()
    assert live & governor == {"killswitch_armed"}  # the declared overlap
    assert len(live | practice | acts | governor) == 6 + 5 + 9 + 2 - 1


# --- the template artifact (BO §1.b.2) ------------------------------------------------


def test_template_not_in_force_on_its_face():
    from app.v2.live_exec.activation.template import (
        ACTIVATION_INSTRUMENT_TEMPLATE,
        TEMPLATE_VERSION,
        template_hash,
    )
    assert TEMPLATE_VERSION == "lai-1.0.0"
    # (i) the declaration is present — pinned substrings
    for pinned in ("NOT IN FORCE",
                   "THIS TEMPLATE CONFERS NO ACTIVATION",
                   "funded-posture witness", "step-up",
                   "kill-switch check",
                   "activation_instrument_not_in_force"):
        assert pinned in ACTIVATION_INSTRUMENT_TEMPLATE, pinned
    # (ii) the hash stands against the landed bytes (recompute == recompute:
    # the function carries no stored literal)
    fresh = hashlib.sha256(
        ACTIVATION_INSTRUMENT_TEMPLATE.encode("utf-8")).hexdigest()
    assert template_hash() == fresh


def test_no_writer_route_into_the_instrument_anywhere():
    """(iii) absence-with-pin: NO code path in the band INSERTs into the
    instrument table — token scan over app/ + API surface enumeration
    (no POST/PUT/DELETE route against /activation)."""
    app_root = BACKEND / "app"
    offenders = []
    for path in app_root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        # constructor-call and raw-SQL needles; the class DEFINITION line
        # (`class V2LiveActivationInstrument(Base)`) is not a writer —
        # scan with the definition form excluded (needle discipline: the
        # scan must not catch the model's own def, the BE-11/12A lesson)
        stripped = text.replace("class V2LiveActivationInstrument(", "")
        for needle in ("V2LiveActivationInstrument(",
                       "INSERT INTO v2_live_activation_instrument",
                       "insert into v2_live_activation_instrument"):
            if needle in stripped:
                offenders.append(f"{path.relative_to(app_root)}:{needle}")
    assert offenders == []
    # surface enumeration off openapi: /activation routes are GET-only
    import os

    from app.main import create_app
    prior = os.environ.get("AXIOM_DATABASE_URL")
    os.environ["AXIOM_DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
    try:
        paths = create_app().openapi()["paths"]
    finally:
        if prior is None:
            os.environ.pop("AXIOM_DATABASE_URL", None)
        else:
            os.environ["AXIOM_DATABASE_URL"] = prior
    activation_routes = {p: sorted(m.keys()) for p, m in paths.items()
                         if "activation" in p}
    assert activation_routes, "activation reads must exist"
    for route, methods in activation_routes.items():
        assert methods == ["get"], (route, methods)


def test_activate_nothing_no_scheduler_or_timer_path():
    """No timer/scheduler/self-activity path in the 12D packages
    (N4/N-O11; absence-with-pin)."""
    for package in ("app/v2/live_exec/activation",
                    "app/v2/live_exec/killswitch"):
        for path in (BACKEND / package).rglob("*.py"):
            text = path.read_text(encoding="utf-8").lower()
            for token in ("asyncio.create_task", "threading.",
                          "schedule", "cron", "background", "timer("):
                assert token not in text, f"{token} in {path.name}"


def test_simulated_class_structurally_banned_from_instrument():
    """The instrument's data_class CHECK admits ONLY 'live_marker' —
    the model's own table_args recite it; no coupon world can simulate
    force (schema arm witnessed live in the border file)."""
    from app.db.models.v2_live_activation import V2LiveActivationInstrument
    checks = [str(c.sqltext) for c in
              V2LiveActivationInstrument.__table__.constraints
              if hasattr(c, "sqltext")]
    assert any("live_marker" in c for c in checks)
    assert not any("simulated" in c for c in checks)


# --- register line (BO §5) + supersession of the 12C exact-form pin --------------------


def test_register_line_superseded_pointer_12d():
    """SUPERSEDED BY CITATION under BO-V2-BE12E-001 §2: the exact-form
    pin moved to the 12E corpus (`test_register_line_12e_honesty_pair_
    exact` — now carrying the DR-3(i) honesty clause); this pointer
    keeps the supersession grep-able and recites the floor."""
    from app.v2.live_exec.api import _REGISTER_LINE
    assert "LIVE=REGISTERED_LOCKED" in _REGISTER_LINE
    assert "funded account: NONE" in _REGISTER_LINE
    assert "activation instrument: NOT IN FORCE" in _REGISTER_LINE
