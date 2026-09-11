"""V2 BE-10 boundary tests — BO-V2-BE-10-001 L1/L2/L3 (banned imports,
zero-mutation verb census, GET-only)."""

from __future__ import annotations

import ast
import socket
from pathlib import Path

import pytest

BACKEND = Path(__file__).resolve().parents[1]
BAND_DIR = BACKEND / "app/v2/account_context"


@pytest.fixture(autouse=True)
def _socket_guard(monkeypatch):
    def _deny(*_a, **_k):
        raise AssertionError("network attempt during BE-10 test")

    monkeypatch.setattr(socket, "getaddrinfo", _deny)
    monkeypatch.setattr(socket, "create_connection", _deny)


def test_l3_banned_imports_absent():
    """R-1.4: never MetaTrader, never the vault, never network."""
    banned = ("providers.exness_mt5", "broker_read.vault", "MetaTrader5",
              "metatrader", "requests", "httpx", "urllib", "socket",
              "aiohttp", "websocket", "paper_trading")
    for f in BAND_DIR.rglob("*.py"):
        tree = ast.parse(f.read_text())
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module]
            for name in names:
                low = name.lower()
                for token in banned:
                    assert token.lower() not in low, f"{f.name}: {name}"


def test_l2_zero_mutation_verbs_in_band_code():
    """No session.add / .delete / INSERT / UPDATE / DELETE / commit in the
    band's modules — the band reads; it never writes anything anywhere."""
    for f in BAND_DIR.rglob("*.py"):
        text = f.read_text()
        for token in ("session.add", "session.delete", ".commit()",
                      "INSERT INTO", "UPDATE ", "DELETE FROM",
                      "insert()", "update()", "delete()"):
            assert token not in text, f"{token} in {f.name}"


def test_l1_get_only_route_census():
    from app.v2.account_context.api import router

    gets, others = set(), set()
    for route in router.routes:
        methods = route.methods - {"HEAD", "OPTIONS"}
        if "GET" in methods:
            gets.add(route.path)
        for m in methods - {"GET"}:
            others.add((m, route.path))
    assert gets == {"/account-context/alignment",
                    "/account-context/summary"}
    assert others == set()  # L1: zero writers of any verb


def test_permission_prefix_exemption_three_arms(monkeypatch):
    """The third literal-prefix ruling: v2.account_context. exempt;
    markers still die elsewhere; boundary tokens die."""
    import app.v2.rbac.permissions as perms_mod

    perms_mod.assert_permission_vocabulary_safe()  # row in => no raise
    rows = {p for s in perms_mod.V2_ROLE_PERMISSIONS.values()
            for p in s if p.startswith("v2.account_context.")}
    assert rows == {"v2.account_context.read"}

    forged = dict(perms_mod.V2_ROLE_PERMISSIONS)
    forged["admin"] = forged["admin"] | {"v2.research.account.peek"}
    monkeypatch.setattr(perms_mod, "V2_ROLE_PERMISSIONS", forged)
    with pytest.raises(ValueError, match="V2_PERMISSION_FORBIDDEN"):
        perms_mod.assert_permission_vocabulary_safe()


def test_permission_boundary_account_contexts_dies(monkeypatch):
    import app.v2.rbac.permissions as perms_mod

    forged = dict(perms_mod.V2_ROLE_PERMISSIONS)
    forged["admin"] = forged["admin"] | {"v2.account_contexts.order.x"}
    monkeypatch.setattr(perms_mod, "V2_ROLE_PERMISSIONS", forged)
    with pytest.raises(ValueError, match="V2_PERMISSION_FORBIDDEN"):
        perms_mod.assert_permission_vocabulary_safe()


def test_prior_band_contracts_untouched():
    from app.v2.broker_read.contract import CONTRACT_VERBS, REFUSAL_CLASSES
    assert len(CONTRACT_VERBS) == 6
    assert len(REFUSAL_CLASSES) == 10
    from app.v2.mode.contract import DEFERRED_MODES, VALID_MODES
    assert VALID_MODES == ("RESEARCH", "SIMULATION", "PAPER")
    assert DEFERRED_MODES == ("LIVE",)
