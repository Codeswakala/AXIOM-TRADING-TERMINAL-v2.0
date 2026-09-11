"""V2 BE-9 contract/canon/vault tests — BO-V2-BE-9-001 T-1/T-3/T-7/T-8/T-11.

Socket guard on every test (zero network — E1 practice contact is a
separately-authorized act). Fixture vault is in-memory (S2.4 canary law).
"""

from __future__ import annotations

import ast
import socket
from pathlib import Path

import pytest

from app.v2.broker_read.contract import (
    CONTRACT_VERBS,
    DISCREPANCY_CLASSES,
    DISCREPANCY_STATES,
    ENVIRONMENT_BINDING,
    RECONCILE_OUTCOMES,
    REFUSAL_CLASSES,
    SYNC_OUTCOMES,
    BrokerReadContract,
    BrokerRefused,
    assert_environment_binding,
)
from app.v2.broker_read.sync import canonical_digest
from app.v2.broker_read.vault import (
    ABSENT,
    ResolvedBrokerCredential,
    open_vault_bytes,
    seal_vault_bytes,
)

BACKEND = Path(__file__).resolve().parents[1]
BROKER_DIR = BACKEND / "app/v2/broker_read"

CANARY = "canary-investor-pw-3f9d1c"


@pytest.fixture(autouse=True)
def _socket_guard(monkeypatch):
    def _deny(*_a, **_k):
        raise AssertionError("network attempt during BE-9 test")

    monkeypatch.setattr(socket, "getaddrinfo", _deny)
    monkeypatch.setattr(socket, "create_connection", _deny)


# --- T-3: the closed six-verb type census -----------------------------------------


def test_t3_contract_verb_census_exact():
    members = [m for m in vars(BrokerReadContract)
               if not m.startswith("_")]
    assert sorted(members) == sorted(CONTRACT_VERBS)
    assert len(CONTRACT_VERBS) == 6


def test_t3_no_v1_brokerport_import_anywhere():
    """The V1 BrokerPort (carries OrderIntent) must not enter the graph."""
    for f in BROKER_DIR.rglob("*.py"):
        tree = ast.parse(f.read_text())
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module]
            for name in names:
                assert "external_integration" not in name, f"{f.name}: {name}"
                assert "broker.port" not in name, f"{f.name}: {name}"


def test_t4_no_mutation_vocabulary_in_domain_code():
    """No submit/amend/cancel order shapes in the domain (docstrings
    stripped — declarations name the concept to forbid it)."""
    def _code(path: Path) -> str:
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.ClassDef,
                                 ast.FunctionDef, ast.AsyncFunctionDef)):
                body = node.body
                if (body and isinstance(body[0], ast.Expr)
                        and isinstance(body[0].value, ast.Constant)
                        and isinstance(body[0].value.value, str)):
                    body[0].value.value = ""
        return ast.unparse(tree)

    for f in BROKER_DIR.rglob("*.py"):
        if f.name == "practice_actuator.py":
            # AMENDED BY CITATION (BO-V2-BE12B-001 SS1.b): the practice
            # actuator is the ONE sanctioned mutation-speaking file in
            # the provider family (name-literal exception; the READ
            # domain ban stands everywhere else). Its own vocabulary is
            # scanned separately below.
            continue
        text = _code(f).lower()
        for token in ("order_send", "ordersend", "submit_order",
                      "place_order", "cancel_order", "modify_order",
                      "orderintent", "trade_action"):
            assert token not in text, f"{token} in {f.name}"
    # the exception file: exactly the sanctioned actuator verb, and the
    # V1 shapes stay banned even there
    actuator = BROKER_DIR / "providers" / "practice_actuator.py"
    text = _code(actuator).lower()
    assert "order_send" in text  # the sanctioned terminal verb
    for token in ("submit_order", "place_order", "cancel_order",
                  "modify_order", "orderintent"):
        assert token not in text, f"{token} in practice_actuator.py"


def test_n3_paper_wall_from_broker_side():
    """T-6: the broker domain's import graph never reaches the paper
    domain (both-sides wall; `paper` in the banned set for THIS domain)."""
    for f in BROKER_DIR.rglob("*.py"):
        tree = ast.parse(f.read_text())
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module]
            for name in names:
                assert "paper" not in name.lower(), f"{f.name}: {name}"


# --- T-11: the S4.1 digest canon (three pinned tests) -------------------------------


def _payload(balance="10000.00"):
    return {
        "accounts": [{"broker_account_ext_id": "111", "alias": "demo",
                      "currency": "USD", "environment": "practice",
                      "request_id": "VOLATILE-1"}],
        "balances": [{"broker_account_ext_id": "111", "balance": balance,
                      "margin_used": "0", "margin_available": balance,
                      "unrealized_pl": "0", "currency": "USD",
                      "fetched_at": "VOLATILE-2"}],
        "positions": [
            {"broker_account_ext_id": "111", "instrument_ext_id": "EURUSD",
             "units_long": "1", "units_short": "0",
             "avg_price_long": "1.1", "avg_price_short": "0"},
            {"broker_account_ext_id": "111", "instrument_ext_id": "GBPUSD",
             "units_long": "2", "units_short": "0",
             "avg_price_long": "1.3", "avg_price_short": "0"},
        ],
        "orders": [], "fills": [], "instrument_permissions": [],
    }


def test_canon_shuffle_invariance():
    a = _payload()
    b = _payload()
    b["positions"] = list(reversed(b["positions"]))  # retrieval re-order
    assert canonical_digest(a) == canonical_digest(b)


def test_canon_single_value_sensitivity():
    assert canonical_digest(_payload("10000.00")) != \
        canonical_digest(_payload("10000.01"))


def test_canon_volatile_invariance():
    a = _payload()
    b = _payload()
    b["accounts"][0]["request_id"] = "DIFFERENT-VOLATILE"
    b["balances"][0]["fetched_at"] = "ANOTHER-TIME"
    b["balances"][0]["server_ping_ms"] = "999"  # unknown field: excluded
    assert canonical_digest(a) == canonical_digest(b)


def test_canon_order_payload_volatile_invariance():
    """N-O1 refinement (INT review §3): a provider-smuggled volatile
    field inside the order payload blob cannot flip the run digest —
    only the substantive projection is hashed. A substantive change
    (price) still moves it."""
    def _orders(price="1.10", volatile=None):
        payload = {"type": "limit", "volume": "1", "price": price,
                   "symbol": "EURUSD"}
        if volatile:
            payload["server_echo_ts"] = volatile  # volatile-class field
        p = _payload()
        p["orders"] = [{"order_ext_id": "1", "broker_account_ext_id": "111",
                        "order_state_ext": "placed", "payload": payload}]
        return p

    assert canonical_digest(_orders()) == \
        canonical_digest(_orders(volatile="2026-09-05T23:59:59Z"))
    assert canonical_digest(_orders(price="1.10")) != \
        canonical_digest(_orders(price="1.11"))


# --- T-7: vault cryptography ---------------------------------------------------------


def test_vault_roundtrip_and_wrong_passphrase():
    payload = seal_vault_bytes("correct-horse", CANARY, "111",
                               "Exness-MT5Trial")
    ok = open_vault_bytes("correct-horse", payload)
    assert ok.state == "present"
    assert ok.investor_password == CANARY
    bad = open_vault_bytes("wrong-passphrase", payload)
    assert bad is ABSENT or bad.state == "absent"


def test_vault_tamper_absent():
    payload = bytearray(seal_vault_bytes("p", CANARY, "111", "S"))
    payload[-1] ^= 0xFF
    assert open_vault_bytes("p", bytes(payload)).state == "absent"


def test_vault_repr_blindness():
    cred = ResolvedBrokerCredential(
        state="present", investor_password=CANARY,
        account_number="111", server_hostname="S")
    assert CANARY not in repr(cred)
    assert CANARY not in str(cred)
    assert "111" not in repr(cred)


def test_vault_sole_resolution_import_boundary():
    """No module outside vault.py imports the crypto backends."""
    for f in BROKER_DIR.rglob("*.py"):
        if f.name == "vault.py":
            continue
        text = f.read_text()
        assert "argon2" not in text, f.name
        assert "AESGCM" not in text, f.name
        assert "cryptography" not in text, f.name


def test_vault_path_never_under_repo():
    """§4 prohibition: no operator-vault directory in the repo tree; the
    path variable is read only inside vault.py."""
    assert not (BACKEND.parent / "operator-vault").exists()
    for f in BROKER_DIR.rglob("*.py"):
        if f.name == "vault.py":
            continue
        assert "AXIOM_BROKER_VAULT_PATH" not in f.read_text(), f.name


# --- T-1: DECISION-1 arms -------------------------------------------------------------


def test_decision1_broker_prefix_exempt():
    from app.v2.rbac.permissions import (
        V2_ROLE_PERMISSIONS,
        assert_permission_vocabulary_safe,
    )

    assert_permission_vocabulary_safe()  # broker rows in => must not raise
    broker_rows = {p for s in V2_ROLE_PERMISSIONS.values()
                   for p in s if p.startswith("v2.broker.")}
    assert len(broker_rows) == 7


def test_decision1_markers_still_die_elsewhere(monkeypatch):
    import app.v2.rbac.permissions as perms_mod

    forged = dict(perms_mod.V2_ROLE_PERMISSIONS)
    forged["admin"] = forged["admin"] | {"v2.research.broker.reach"}
    monkeypatch.setattr(perms_mod, "V2_ROLE_PERMISSIONS", forged)
    with pytest.raises(ValueError, match="V2_PERMISSION_FORBIDDEN"):
        perms_mod.assert_permission_vocabulary_safe()


def test_decision1_boundary_brokerage_dies(monkeypatch):
    import app.v2.rbac.permissions as perms_mod

    forged = dict(perms_mod.V2_ROLE_PERMISSIONS)
    forged["admin"] = forged["admin"] | {"v2.brokerage.order.forge"}
    monkeypatch.setattr(perms_mod, "V2_ROLE_PERMISSIONS", forged)
    with pytest.raises(ValueError, match="V2_PERMISSION_FORBIDDEN"):
        perms_mod.assert_permission_vocabulary_safe()


# --- Q9 successor binding + vocabulary integrity ---------------------------------------


def test_binding_pinned_and_mismatch_refuses():
    """Operator pinning act of 2026-09-05 landed the literals; the
    mismatch arm still refuses typed (Q9 successor law). The pre-pin
    fail-closed arm is superseded by this pinned state — disclosed."""
    assert ENVIRONMENT_BINDING["server_hostname"] == "ExnessKE-MT5Trial9"
    assert ENVIRONMENT_BINDING["account_number"] == "476910140"
    assert ENVIRONMENT_BINDING["environment"] == "practice"
    # exact match passes
    assert_environment_binding("ExnessKE-MT5Trial9", "476910140",
                               "practice")
    # any deviation = typed refusal (a config error cannot repoint reads)
    with pytest.raises(BrokerRefused) as exc:
        assert_environment_binding("Exness-LIVE1", "476910140", "practice")
    assert exc.value.refusal_class == "broker.binding.mismatch"
    with pytest.raises(BrokerRefused):
        assert_environment_binding("ExnessKE-MT5Trial9", "999999999",
                                   "practice")


def test_vocabulary_integrity():
    assert len(REFUSAL_CLASSES) == 10
    assert "broker.terminal.unavailable" in REFUSAL_CLASSES  # E-ENV-1
    assert "broker.unavailable" in REFUSAL_CLASSES           # distinct
    assert SYNC_OUTCOMES == ("complete", "partial_refused", "failed")
    assert RECONCILE_OUTCOMES == ("clean", "discrepant")
    assert len(DISCREPANCY_CLASSES) == 7
    assert DISCREPANCY_STATES == ("detected", "triaged", "owned",
                                  "resolved", "dismissed_with_reason")
