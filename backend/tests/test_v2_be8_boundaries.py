"""V2 BE-8 boundary/isolation tests — BO-V2-BE-8-001 T-1/T-3/T-4/T-16/T-18.

D-1 marker-exemption both arms + boundary; sealed-registry census;
no-adapter-ABC scan; import scan (N1/N2); PGF-021 source scan; API-surface
census (C3); V1 pin re-hash; prior-band contract regression.
"""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import pytest

BACKEND = Path(__file__).resolve().parents[1]
PAPER_DIR = BACKEND / "app/v2/paper_trading"


# --- T-1: D-1 marker law, both arms + boundary --------------------------------


def test_d1_exemption_scoped_exactly_v2_paper_prefix():
    """Arm 1: v2.paper.* rows pass the guard (would die without D-1)."""
    from app.v2.rbac.permissions import (
        V2_FORBIDDEN_PERMISSION_MARKERS,
        V2_ROLE_PERMISSIONS,
        assert_permission_vocabulary_safe,
    )

    assert_permission_vocabulary_safe()  # must not raise with paper rows in
    paper_rows = {p for perms in V2_ROLE_PERMISSIONS.values()
                  for p in perms if p.startswith("v2.paper.")}
    assert len(paper_rows) == 8
    # the collision is real: without the exemption these WOULD die
    assert any(m in p for p in paper_rows
               for m in V2_FORBIDDEN_PERMISSION_MARKERS)


def test_d1_markers_still_die_elsewhere(monkeypatch):
    """Arm 2 (must-die): v2.research.order.* rejected."""
    import app.v2.rbac.permissions as perms_mod

    forged = dict(perms_mod.V2_ROLE_PERMISSIONS)
    forged["admin"] = forged["admin"] | {"v2.research.order.place"}
    monkeypatch.setattr(perms_mod, "V2_ROLE_PERMISSIONS", forged)
    with pytest.raises(ValueError, match="V2_PERMISSION_FORBIDDEN"):
        perms_mod.assert_permission_vocabulary_safe()


def test_d1_boundary_paperwork_dies(monkeypatch):
    """Boundary arm (must-die): v2.paperwork.* is NOT exempt — the test
    is a literal prefix 'v2.paper.' including the trailing dot."""
    import app.v2.rbac.permissions as perms_mod

    forged = dict(perms_mod.V2_ROLE_PERMISSIONS)
    forged["admin"] = forged["admin"] | {"v2.paperwork.order.forge"}
    monkeypatch.setattr(perms_mod, "V2_ROLE_PERMISSIONS", forged)
    with pytest.raises(ValueError, match="V2_PERMISSION_FORBIDDEN"):
        perms_mod.assert_permission_vocabulary_safe()


# --- T-4: sealed registry + no adapter interface --------------------------------


def test_sealed_registry_two_keys_frozen_live_posture_locked():
    """AM-3 (BE-12A): registry 2 keys; live entry posture-locked.

    SUPERSEDES BY CITATION: test_sealed_registry_single_entry_frozen
    (BE-8 N2 len==1 pin) — superseded under BO-V2-BE12A-001 SS1.e /
    DR-V2-BE-12-001 AM-3 (this file is presence-only-pinned by BE-11's
    wall coupon; the byte-pinned test_v2_be9_boundaries.py is NOT
    touched). The N2 mechanism is UNCHANGED: frozen literal, no
    registration function, no plugin path.
    """
    from types import MappingProxyType

    from app.v2.paper_trading.contracts import EXECUTION_BACKENDS

    assert isinstance(EXECUTION_BACKENDS, MappingProxyType)
    assert dict(EXECUTION_BACKENDS) == {
        "paper": "app.v2.paper_trading.simulator",
        "live": "app.v2.live_exec.adapter_boundary"}
    with pytest.raises(TypeError):
        EXECUTION_BACKENDS["funded"] = "anywhere"  # frozen literal
    # posture-lock arm (12B edition — stance arm superseded BY CITATION
    # under BO-V2-BE12B-001 SS1.b: posture_stub -> practice_wired by
    # cited edit): the live entry names the boundary package whose door
    # STILL refuses without a practice-lane pass — the lock moved from
    # a stub literal to the lane door, and LIVE-lane asks have no path.
    from app.v2.live_exec.adapter_boundary import BOUNDARY_STANCE, submission_doorway
    from app.v2.live_exec.locks import (
        PracticeActuationRefused,
        PracticeActuationState,
    )
    assert BOUNDARY_STANCE == "practice_wired"
    with pytest.raises(PracticeActuationRefused) as exc:
        submission_doorway(PracticeActuationState(
            lane="live", mode="RESEARCH"), {})
    assert exc.value.reason == "actuation_lane_mismatch"


def test_no_adapter_abc_anywhere_in_domain():
    """S6.1: no ExecutionAdapter interface/ABC exists — the substitution
    surface N2 forbids is structurally absent."""
    for f in PAPER_DIR.glob("*.py"):
        tree = ast.parse(f.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                base_names = {getattr(b, "id", getattr(b, "attr", ""))
                              for b in node.bases}
                assert "ABC" not in base_names, f"ABC in {f.name}"
                assert "adapter" not in node.name.lower(), node.name
        text = f.read_text().lower()
        assert "executionadapter" not in text, f.name
        assert "abstractmethod" not in text, f.name


def test_import_scan_paper_domain_isolated():
    """T-3/N1/N2: no broker/execution/credential/network module reachable
    from the paper domain graph."""
    banned_tokens = ("execution", "broker", "live_service",
                     "trading_intelligence", "market.live", "app.market",
                     "credential", "secret", "vault", "keyring")
    banned_network = ("requests", "httpx", "urllib", "socket", "aiohttp",
                      "websocket")
    for f in PAPER_DIR.glob("*.py"):
        tree = ast.parse(f.read_text())
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module]
            for name in names:
                low = name.lower()
                for token in banned_tokens + banned_network:
                    assert token not in low, f"{f.name} imports {name}"


def test_pgf021_no_filesystem_conditional_behavior():
    """T-18: no Path.exists/is_dir/is_file branching; no env reads.
    (The migration reads files by design — domain modules only.)"""
    for f in PAPER_DIR.glob("*.py"):
        text = f.read_text()
        for marker in (".exists()", ".is_dir()", ".is_file()",
                       "os.environ", "os.getenv"):
            assert marker not in text, f"{marker} in {f.name}"


def _code_without_docstrings(path: Path) -> str:
    """Source with docstrings stripped: the scan targets CODE vocabulary;
    the N1 declaration sentences in module docstrings are not code."""
    tree = ast.parse(path.read_text())
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef,
                             ast.AsyncFunctionDef)):
            body = node.body
            if (body and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                body[0].value.value = ""
    return ast.unparse(tree)


def test_no_secret_or_credential_vocabulary():
    """N1: zero credential/secret access vocabulary in domain CODE
    (docstrings stripped — the isolation declarations name the concept
    to forbid it; the code may not carry it)."""
    for f in PAPER_DIR.glob("*.py"):
        text = _code_without_docstrings(f).lower()
        for token in ("api_key", "password", "credential", "keyring",
                      "private_key", "auth_token"):
            assert token not in text, f"{token} in {f.name}"


# --- T-16: API census (C3) -------------------------------------------------------


def test_api_surface_census_exact():
    """POST = exactly the 6 governed writers; zero PUT/PATCH/DELETE."""
    from app.v2.paper_trading.api import router

    posts, gets, others = set(), set(), set()
    for route in router.routes:
        methods = route.methods - {"HEAD", "OPTIONS"}
        if "POST" in methods:
            posts.add(route.path)
        if "GET" in methods:
            gets.add(route.path)
        for m in methods - {"POST", "GET"}:
            others.add((m, route.path))
    assert posts == {
        "/paper/accounts", "/paper/accounts/confirm", "/paper/orders",
        "/paper/orders/confirm", "/paper/orders/cancel",
        "/paper/orders/{order_id}/run"}
    assert gets == {
        "/paper/accounts", "/paper/orders",
        "/paper/orders/{order_id}/events", "/paper/fills",
        "/paper/positions", "/paper/balances", "/paper/risk-decisions",
        "/paper/reconciliations"}
    assert others == set()  # C3: no PUT/PATCH/DELETE


# --- vocabulary integrity ---------------------------------------------------------


def test_vocabulary_integrity():
    from app.v2.paper_trading.contracts import (
        CONFIRMATION_REFUSALS,
        FILL_CLASSES,
        LEGAL_TRANSITIONS,
        ORDER_STATES,
        RISK_DECISIONS,
        TERMINAL_STATES,
        TIME_IN_FORCE_V1,
    )

    assert FILL_CLASSES == ("paper_simulated",)
    assert RISK_DECISIONS == ("pass", "block", "hold")
    assert TIME_IN_FORCE_V1 == ("replay_window",)
    assert set(TERMINAL_STATES) <= set(ORDER_STATES)
    assert len(CONFIRMATION_REFUSALS) == 4
    for frm, to in LEGAL_TRANSITIONS:
        assert frm in ORDER_STATES and to in ORDER_STATES
    # no transition leaves a terminal state
    for frm, _to in LEGAL_TRANSITIONS:
        assert frm not in TERMINAL_STATES


def test_mode_law_t2():
    from app.v2.mode.contract import DEFERRED_MODES, VALID_MODES

    assert VALID_MODES == ("RESEARCH", "SIMULATION", "PAPER")
    assert DEFERRED_MODES == ("LIVE",)


# --- regression: V1 pins + prior bands ---------------------------------------------


def test_regression_v1_reuse_pins_unchanged():
    """The six V1 pins re-hash unchanged (T-7 lineage; V1 paper-ledger
    surface byte-frozen per Q1 supersede-with-frozen-boundary)."""
    pins = {
        "app/ml/dataset/chronology_guard.py": "7dbc665dc4b43f31",
        "app/ml/dataset/split_engine.py": "e893b92c6ccce188",
        "app/ml/dataset/snapshot_builder.py": "b08ef4b1dec07567",
        "app/ml/dataset/service.py": "6c5d72a8942050b4",
        "app/execution_research/simulation.py": "f163e610ba1a6215",
        "app/ml/economic/service.py": "c49527ed12f4d2ca",
    }
    for rel, pin in pins.items():
        actual = hashlib.sha256(
            (BACKEND / rel).read_bytes()).hexdigest()[:16]
        assert actual == pin, f"{rel}: {actual} != {pin}"


def test_regression_prior_band_contracts_untouched():
    """BE-4..BE-7 contract vocabularies unchanged by the BE-8 package."""
    from app.v2.portfolio_research.contracts import (
        BASIS_LABELS,
        PORTFOLIO_BASES,
    )
    from app.v2.research.typing import FAMILIES
    from app.v2.research_governance.contracts import (
        DEPLOYMENT_CLASSES,
        SIGNAL_FAMILIES,
        SIGNAL_STATES,
    )
    from app.v2.research_jobs.contracts import (
        CONSTRUCTIBLE_RESULT_CLASSES,
        COST_UNITS_V1,
        RESULT_CLASS_TAXONOMY,
    )

    assert PORTFOLIO_BASES == ("hypothetical",)
    assert BASIS_LABELS == ("hypothetical-research",)
    assert SIGNAL_FAMILIES == ("structural", "predictive")
    assert SIGNAL_STATES == ("emitted", "withheld", "expired", "refused")
    assert DEPLOYMENT_CLASSES == ("research", "shadow", "champion",
                                  "challenger", "retired")
    assert len(FAMILIES) == 10
    assert RESULT_CLASS_TAXONOMY == ("backtest", "simulation", "paper",
                                     "live")
    assert CONSTRUCTIBLE_RESULT_CLASSES == ("backtest", "simulation")
    assert COST_UNITS_V1 == ("price", "fraction")
