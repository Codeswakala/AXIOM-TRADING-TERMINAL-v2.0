"""V2 BE-12E engine coupons (BO §1.a/§1.b/§1.c/§1.d/§1.e partial).

DR-F2 four pins (locus, direction, ROUND_HALF_EVEN delegated, canonical
form, float ban); mode-stamp laws (§a.4 both halves); closed
vocabularies + F1 final recital; evidence-only scans; lane law final
form; template-literal closure; counterfeit-witness scan.
"""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pytest

from app.v2.live_exec.incident.engine import (
    INCIDENT_REFUSALS,
    INCIDENT_SEVERITIES,
    INCIDENT_STATUSES,
)
from app.v2.live_exec.reconcile.engine import (
    DRIFT_FACT_KINDS,
    RECON_OUTCOMES,
)
from app.v2.live_exec.reconcile.money import (
    MoneyNotCanonicalizable,
    money_parity,
    to_canonical_money,
)

BACKEND = Path(__file__).resolve().parents[1]


# --- DR-F2: the four pins (BO §1.b.3) -------------------------------------------------


def test_drf2_canonical_form_pins():
    """Fixed-point 2dp; no exponent; no '+'; single leading zero for
    |x|<1; sign only when negative; -0 normalized."""
    cases = [("100", "100.00"), ("100.5", "100.50"),
             ("0.005", "0.00"), ("0.015", "0.02"),  # HALF_EVEN at the edge
             (".5", "0.50"), ("-3.14159", "-3.14"),
             ("1e2", "100.00"), (Decimal("2.675"), "2.68"),
             ("-0.001", "0.00"), (0, "0.00"), (7, "7.00")]
    for raw, want in cases:
        got = to_canonical_money(raw)
        assert got == want, (raw, got, want)
        assert "e" not in got and "E" not in got and "+" not in got


def test_drf2_round_half_even_delegated_not_reimplemented():
    """The locus DELEGATES to the fielded bridge convention: HALF_EVEN
    witnessed at the tie cells (0.125 -> 0.12, 0.135 -> 0.14), and the
    locus body carries the IMPORT, not a quantize of its own."""
    assert to_canonical_money("0.125") == "0.12"  # ties-to-even down
    assert to_canonical_money("0.135") == "0.14"  # ties-to-even up
    body = (BACKEND / "app/v2/live_exec/reconcile/money.py").read_text(
        encoding="utf-8")
    assert "from app.v2.paper_bridge.engine import quantize_2dp" in body
    # the locus never re-implements: no rounding-mode token in its code
    import ast
    tree = ast.parse(body)
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute):
            assert node.attr != "quantize", "locus re-implements quantize"


def test_drf2_float_banned_typed():
    with pytest.raises(MoneyNotCanonicalizable) as exc:
        to_canonical_money(1.23)
    assert exc.value.reason == "money_float_banned"
    with pytest.raises(MoneyNotCanonicalizable) as exc:
        to_canonical_money("not-money")
    assert exc.value.reason == "money_not_decimal"


def test_drf2_float_token_scan_positive_pin():
    """`float(` banned over both new packages (positive-pin: the corpus
    is enumerated and asserted non-empty)."""
    corpus = []
    for package in ("app/v2/live_exec/reconcile",
                    "app/v2/live_exec/incident"):
        for path in (BACKEND / package).rglob("*.py"):
            corpus.append(path)
            assert "float(" not in path.read_text(encoding="utf-8"), path
    assert len(corpus) >= 5  # positive pin: all five 12E modules seen


def test_drf2_one_locus_scan():
    """The entry-point token appears ONLY in the locus and call sites
    (engine + this coupon corpus); no other converter exists."""
    hits = []
    for path in (BACKEND / "app").rglob("*.py"):
        if "to_canonical_money" in path.read_text(encoding="utf-8"):
            hits.append(path.name)
    assert sorted(hits) == ["engine.py", "money.py"]  # reconcile engine + locus


def test_drf2_parity_is_string_equality():
    assert money_parity("100", "100.000")
    assert money_parity("0.1", Decimal("0.10"))
    assert not money_parity("100.00", "100.01")


# --- closed vocabularies + F1 FINAL recital (BO §1.f.1) --------------------------------


def test_12e_vocabularies_closed():
    assert RECON_OUTCOMES == ("clean", "parity_break")
    assert DRIFT_FACT_KINDS == ("fill_price_mismatch", "fill_unprojected",
                                "position_money_uncanonical",
                                "ledger_orphan")
    assert INCIDENT_SEVERITIES == ("SEV-1", "SEV-2", "SEV-3", "SEV-4")
    assert INCIDENT_STATUSES == ("open", "closed")
    # CR-1 (DEL-001): the 4-member form — the wire's severity refusal
    # is now an enumerated citizen of the closed law.
    assert INCIDENT_REFUSALS == ("incident_not_open",
                                 "incident_already_closed",
                                 "incident_instruments_absent",
                                 "incident_severity_invalid")


def test_f1_final_full_active_set():
    """The ladder's FINAL F1 recital: LIVE(6) + PRACTICE(5) + ACTS(9) +
    GOVERNOR(2) + 12E(3); the ONLY overlap = the declared lock token."""
    from app.v2.live_exec.killswitch.engine import GOVERNOR_REFUSALS
    from app.v2.live_exec.locks import LOCK_ORDER, PRACTICE_LOCK_ORDER
    from app.v2.live_exec.modify.engine import MODIFY_REFUSALS
    live, practice = set(LOCK_ORDER), set(PRACTICE_LOCK_ORDER)
    acts, governor = set(MODIFY_REFUSALS), set(GOVERNOR_REFUSALS)
    twelve_e = set(INCIDENT_REFUSALS)
    assert twelve_e & (live | practice | acts | governor) == set()
    assert live & governor == {"killswitch_armed"}
    # CR-1 (DEL-001): the F1 FINAL recital re-stated at 25 — the FULL
    # active set is now true ON THE WIRE, not only in the tuples.
    assert len(live | practice | acts | governor | twelve_e) == \
        6 + 5 + 9 + 2 + 4 - 1


# --- evidence-only law (§a.1) + lane law final form (§a.3) -----------------------------


def test_evidence_only_no_self_activity_tokens():
    """Positive-pin scans over both packages + the API wedge: no
    timer/scheduler/self-trigger tokens; parity_break never side-acts
    (no incident construction in the reconcile package, both ways)."""
    scanned = 0
    for package in ("app/v2/live_exec/reconcile",
                    "app/v2/live_exec/incident"):
        for path in (BACKEND / package).rglob("*.py"):
            scanned += 1
            text = path.read_text(encoding="utf-8").lower()
            for token in ("asyncio.create_task", "threading.",
                          "schedule", "cron", "background", "timer(",
                          "signal."):
                assert token not in text, f"{token} in {path.name}"
    assert scanned >= 5
    # cross-table no-writer both directions (§f.2)
    recon = (BACKEND / "app/v2/live_exec/reconcile/engine.py").read_text(
        encoding="utf-8")
    assert "V2LiveExecIncident" not in recon
    incident = (BACKEND / "app/v2/live_exec/incident/engine.py").read_text(
        encoding="utf-8")
    assert "V2LiveExecReconciliation" not in incident


def test_lane_law_final_form():
    """PRACTICE_LOCK_ORDER stays five members; practice pass/refusal
    vocabulary untouched by the evidence plane (pure-lock arms)."""
    from app.v2.live_exec.locks import (
        PRACTICE_LOCK_ORDER,
        PracticeActuationRefused,
        PracticeActuationState,
        require_practice_actuation,
    )
    assert len(PRACTICE_LOCK_ORDER) == 5
    require_practice_actuation(PracticeActuationState(
        lane="practice", mode="PAPER", credential_state="present",
        boundary_stance="practice_wired", basis_age_hours=2.0))
    with pytest.raises(PracticeActuationRefused) as exc:
        require_practice_actuation(PracticeActuationState(
            lane="practice", mode="RESEARCH"))
    assert exc.value.reason == "practice_mode_not_armed"
    assert exc.value.reason not in INCIDENT_REFUSALS


# --- §a.4 mode-stamp laws (both halves) -----------------------------------------------


def test_killswitch_mode_stamp_fixed_constant():
    """LOW-1 / V2-BE12D-DEL-001 CLOSURE COUPON (§a.4): on the
    kill-switch, `mode` is a HOUSE GOVERNANCE STAMP fixed at
    'RESEARCH' — arm-insert carries the constant, and the valve
    transitions never touch the column (the constant is LAW; silent
    drift fails here). ZERO 12D byte moves: the engine body is
    asserted to carry the literal at the insert site only."""
    body = (BACKEND / "app/v2/live_exec/killswitch/engine.py").read_text(
        encoding="utf-8")
    assert 'mode="RESEARCH"' in body           # the arm-insert stamp
    # the valve UPDATE statement does not touch mode
    valve_start = body.index("async def _valve")
    valve_end = body.index("async def governor_arm")
    valve_body = body[valve_start:valve_end]
    assert "mode" not in valve_body.split('"""')[2]  # code after docstring


def test_template_artifact_hash_literal():
    """§e.3 template-literal closure: the disclosed artifact hash is
    pinned as a full literal against the template's final bytes —
    intra-band text drift is formally closed."""
    from app.v2.live_exec.activation.template import template_hash
    assert template_hash() == (
        "142f87723a63420f3ddd9b0250a9a215"
        "f8c7bee690eca4d65fc74103019d8c0b")


# --- §e.2 counterfeit-witness scan ----------------------------------------------------


def test_counterfeit_witness_scan():
    """PGF-022 applied to CLAIMS: no evidence artifact in the band
    family claims live-network proof. Corpus POSITIVE-PINNED (every
    path asserted to exist); this coupon's own body is EXCLUDED by
    recited law; the honest phraseology family is allow-listed."""
    from app.v2.live_exec.activation.template import (
        ACTIVATION_INSTRUMENT_TEMPLATE,
    )
    from app.v2.live_exec.api import _REGISTER_LINE
    repo = BACKEND.parent
    corpus_paths = [
        repo / "DELIVERY_REPORT_V2_BE-12A.md",
        repo / "DELIVERY_REPORT_V2_BE-12B.md",
        repo / "DELIVERY_REPORT_V2_BE-12C.md",
        repo / "DELIVERY_REPORT_V2_BE-12D.md",
        repo / "docs/evidence/V2_BE-12A_FAILFIRST_WITNESS.txt",
        repo / "docs/evidence/V2_BE-12B_FAILFIRST_WITNESS.txt",
        repo / "docs/evidence/V2_BE-12C_FAILFIRST_WITNESS.txt",
        repo / "docs/evidence/V2_BE-12D_FAILFIRST_WITNESS.txt",
    ]
    banned = ("live-network-proven", "live network proven",
              "proven on the live network", "real-network-proven",
              "live-wire-proven")
    texts = [ACTIVATION_INSTRUMENT_TEMPLATE, _REGISTER_LINE]
    for path in corpus_paths:
        assert path.exists(), f"corpus positive-pin: {path} absent"
        texts.append(path.read_text(encoding="utf-8"))
    for text in texts:
        lowered = text.lower()
        for token in banned:
            assert token not in lowered, token
    # the honest phraseology stands (allow-listed, present by law)
    assert "NOT PROVEN" in _REGISTER_LINE


def test_register_line_12e_honesty_pair_exact():
    """§e.1 exact-form pin (SUPERSEDES BY CITATION the 12D-era pin —
    grep-able pointer: the 12D exact form moved here per BO §2)."""
    from app.v2.live_exec.api import _REGISTER_LINE
    assert _REGISTER_LINE == (
        "BE-12E RECONCILIATION+INCIDENT |"
        " LIVE=REGISTERED_LOCKED | funded account: NONE |"
        " activation instrument: NOT IN FORCE |"
        " LIVE real-network behavior: NOT PROVEN (\\u2260 FALSE)"
        .encode().decode("unicode_escape"))
    # floor law stands
    assert _REGISTER_LINE.startswith("BE-12")
    for invariant in ("LIVE=REGISTERED_LOCKED", "funded account: NONE"):
        assert invariant in _REGISTER_LINE


def test_wire_literal_enrollment():
    """CR-1 (DEL-002 rider): every refusal-reason STRING LITERAL fired
    from api.py is enrolled — pinned == exactly the two lookup-idiom
    ids (12B-lineage `submission_not_found`, recited; this band's
    `reconciliation_not_found`). Every OTHER reason on the wire arrives
    from an engine constant or a raised LiveExecRefused — the closed
    law and the wire are one surface. A new inline literal fails here."""
    import re
    body = (BACKEND / "app/v2/live_exec/api.py").read_text(
        encoding="utf-8")
    literals = set(re.findall(r'_refusal\(request, "([a-z_]+)"', body))
    assert literals == {"submission_not_found",
                        "reconciliation_not_found"}
