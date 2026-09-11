"""V2 BE-12A migration + wall coupons (BO §1.g/§4).

Census tattoo (80/72/13); one-upgrade-line law (N-O8 both streams);
permission rows exact under the AM-1 family; NO compver row; guard
pair verbatim + live fire; downgrade exact; drift gate; wall law
(no domain imports live_exec; live_exec imports read-only surfaces
only; zero provider tokens in the package); intent ledger Level-I
(idempotency at schema; zero-UPDATE regime).
"""

from __future__ import annotations

import os
import sqlite3
import subprocess
import sys
import uuid
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
TRANS_AUTHORITY = "BO-V2-BE-3-P2-TRANS-001"
REV_0052 = "20260909_0052"
REV_0053 = "20260909_0053"

TRIGGERS_0053 = {
    "v2_live_exec_intent_immutable_update":
        "V2 live exec intents are immutable; UPDATE prohibited",
    "v2_live_exec_intent_immutable_delete":
        "V2 live exec intents are immutable; DELETE prohibited",
}

PERMS_0053 = {
    ("admin", "v2.live_exec.intent.write", "SAL-4"),
    ("admin", "v2.live_exec.evaluate.write", "SAL-4"),
    ("admin", "v2.live_exec.intents.read", "SAL-2"),
}


def _alembic(args: list[str], db_url: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["AXIOM_DATABASE_URL"] = db_url
    env.setdefault("AXIOM_ENVIRONMENT", "testing")
    env.setdefault("AXIOM_ALLOW_INSECURE_DEV", "true")
    env.setdefault("AXIOM_JWT_SECRET_KEY",
                   "test-secret-key-at-least-32-chars-long!!")
    env["AXIOM_V2_MODE"] = "RESEARCH"
    env["AXIOM_TD_TRANSITION_AUTHORITY_REF"] = TRANS_AUTHORITY
    return subprocess.run(
        [sys.executable, "-m", "alembic", *args],
        cwd=BACKEND_DIR, env=env, capture_output=True, text=True, timeout=600)


def _db(tmp_path: Path, rev: str) -> tuple[Path, str]:
    db_file = tmp_path / "be12a.db"
    db_url = f"sqlite+aiosqlite:///{db_file}"
    result = _alembic(["upgrade", rev], db_url)
    assert result.returncode == 0, result.stderr
    return db_file, db_url


def _q(db_file: Path, sql: str, params: tuple = ()):
    conn = sqlite3.connect(db_file)
    try:
        return conn.execute(sql, params).fetchall()
    finally:
        conn.close()


def test_one_upgrade_line_0052_to_0053(tmp_path: Path) -> None:
    db_file, db_url = _db(tmp_path, REV_0052)
    result = _alembic(["upgrade", REV_0053], db_url)
    assert result.returncode == 0, result.stderr
    both = result.stdout + result.stderr
    lines = [ln for ln in both.splitlines() if "Running upgrade" in ln]
    assert len(lines) == 1, lines
    assert f"{REV_0052} -> {REV_0053}" in lines[0]


def test_census_tattoo_80_72_13(tmp_path: Path) -> None:
    db_file, _ = _db(tmp_path, REV_0053)
    trig = _q(db_file, "SELECT COUNT(*) FROM sqlite_master WHERE"
                       " type='trigger'")[0][0]
    perm = _q(db_file, "SELECT COUNT(*) FROM v2_permission")[0][0]
    comp = _q(db_file, "SELECT COUNT(*) FROM v2_computation_version")[0][0]
    assert (trig, perm, comp) == (80, 72, 13)
    rows = {(r, p, s) for r, p, s in _q(
        db_file, "SELECT role, permission, sal FROM v2_permission"
                 " WHERE permission LIKE 'v2.live_exec.%'")}
    assert rows == PERMS_0053
    # NO compver row for live_exec (BO §1.g)
    lx_compver = _q(db_file, "SELECT COUNT(*) FROM v2_computation_version"
                             " WHERE component LIKE '%live%'")[0][0]
    assert lx_compver == 0
    # guard messages verbatim
    guards = dict(_q(db_file, "SELECT name, sql FROM sqlite_master WHERE"
                              " type='trigger' AND name LIKE"
                              " 'v2_live_exec_intent_immutable_%'"))
    assert set(guards) == set(TRIGGERS_0053)
    for name, message in TRIGGERS_0053.items():
        assert message in guards[name]


def test_intent_ledger_level_one(tmp_path: Path) -> None:
    """Zero-UPDATE regime + idempotency-at-schema, live-fired."""
    db_file, _ = _db(tmp_path, REV_0053)
    conn = sqlite3.connect(db_file)
    try:
        row = ("id-1", "idem-1", "basis-1", "capability", "{}", "d" * 64,
               "registered", None, "t", "simulated", "RESEARCH", "t",
               None, "2026-09-08 00:00:00+00:00")
        cols = ("id, idempotency_key, requested_basis_id, posture,"
                " payload, digest, record_state, step_up_ref, actor_id,"
                " data_class, mode, operator_id, correlation_id,"
                " created_at")
        marks = ",".join("?" * 14)
        conn.execute(
            f"INSERT INTO v2_live_exec_intent ({cols}) VALUES ({marks})",
            row)
        conn.commit()
        # duplicate idempotency_key dies at schema
        try:
            conn.execute(
                f"INSERT INTO v2_live_exec_intent ({cols}) VALUES ({marks})",
                ("id-2",) + row[1:])
            raise AssertionError("idempotency uq failed open")
        except sqlite3.IntegrityError:
            pass
        # UPDATE / DELETE guards fire verbatim
        for sql in ("UPDATE v2_live_exec_intent SET actor_id='x'",
                    "DELETE FROM v2_live_exec_intent"):
            try:
                conn.execute(sql)
                raise AssertionError(f"guard failed open: {sql}")
            except sqlite3.IntegrityError:
                pass
        # posture CHECK closed
        try:
            conn.execute(
                f"INSERT INTO v2_live_exec_intent ({cols}) VALUES ({marks})",
                (str(uuid.uuid4()), "idem-3", "basis-1", "funded", "{}",
                 "d" * 64, "registered", None, "t", "simulated",
                 "RESEARCH", "t", None, "2026-09-08 00:00:00+00:00"))
            raise AssertionError("posture CHECK failed open")
        except sqlite3.IntegrityError:
            pass
    finally:
        conn.close()


def test_downgrade_reverses_exactly(tmp_path: Path) -> None:
    db_file, db_url = _db(tmp_path, REV_0053)
    result = _alembic(["downgrade", REV_0052], db_url)
    assert result.returncode == 0, result.stderr
    tables = {x[0] for x in _q(db_file, "SELECT name FROM sqlite_master"
                                        " WHERE type='table'")}
    assert "v2_live_exec_intent" not in tables
    perm = _q(db_file, "SELECT COUNT(*) FROM v2_permission WHERE"
                       " permission LIKE 'v2.live_exec.%'")[0][0]
    assert perm == 0
    trig = _q(db_file, "SELECT COUNT(*) FROM sqlite_master WHERE"
                       " type='trigger'")[0][0]
    assert trig == 78  # the 0052 tattoo restored


def test_drift_gate_0053(tmp_path: Path) -> None:
    db_file, db_url = _db(tmp_path, REV_0053)
    check = _alembic(["check"], db_url)
    drift = (check.stdout + check.stderr).lower()
    assert check.returncode != 0
    assert "live_exec" not in drift, "BE-12A drift at 0053"
    if "not up to date" not in drift:
        assert "audit_write_failure_records" in drift


# --- wall law (BO §1.a) -------------------------------------------------------------


def test_wall_no_domain_imports_live_exec() -> None:
    """No standing domain IMPORTS live_exec (one direction of the wall).

    The law is an import wall, not a string wall: the AM-1/AM-2/AM-3
    amendment surfaces name the package in BO-cited comments/values
    (permissions enum, mode contract comment, registry value string) and
    the BE-1-era capability id `v2.live_execution` predates the band —
    none of those are imports. The needles are the import forms.
    """
    app_root = BACKEND_DIR / "app"
    needles = ("from app.v2.live_exec", "import app.v2.live_exec")
    offenders = []
    for path in app_root.rglob("*.py"):
        rel = path.relative_to(app_root).as_posix()
        if rel.startswith("v2/live_exec/") or rel.startswith("v2/api/"):
            continue
        if rel == "db/models/__init__.py":
            continue  # PG-002 registration unit (models are chassis, not domain)
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle in text:
                offenders.append(f"{rel}:{needle}")
    assert offenders == []


def test_wall_live_exec_imports_read_only_surfaces() -> None:
    """live_exec imports models/engines/contracts read-only; no writers,
    no providers, no terminal, no vault-secret surface.

    AMENDED BY CITATION (BO-V2-BE12B-001 SS1.b): the provider-token ban
    now reads banned everywhere in the package EXCEPT inside
    `adapter_boundary.py` (name-literal, the ONE sanctioned doorway,
    which reaches the terminal family ONLY via the BE-9 provider leg).
    Both directions still scanned; every other file keeps the full ban;
    the boundary file itself may speak ONLY the provider-module path —
    never a terminal package token directly."""
    package = BACKEND_DIR / "app/v2/live_exec"
    banned = ("broker_read.providers", "MetaTrader5", "mt5",
              "external_integration", "broker_read.sync",
              "broker_read.vault", "paper_trading.simulator")
    boundary_banned = ("MetaTrader5", "mt5", "external_integration",
                       "broker_read.sync", "paper_trading.simulator")
    # (BO SS1.b one-doorway law: `broker_read.vault` is lawful ONLY in
    # adapter_boundary.py, as the state-only credential reader; the
    # full ban stands in every other live_exec file via `banned`.)
    offenders = []
    for path in package.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        needles = boundary_banned if path.name == "adapter_boundary.py" \
            else banned
        for needle in needles:
            if needle in text:
                offenders.append(f"{path.name}:{needle}")
    assert offenders == []
    # the exception is not vacuous: the boundary file DOES carry the
    # sanctioned provider-leg import (and only the actuator module)
    boundary = (package / "adapter_boundary.py").read_text(encoding="utf-8")
    assert "broker_read.providers.practice_actuator" in boundary
    # the vault surface in the boundary is the STATE-ONLY reader
    assert "resolve_practice_trade_credential().state" in boundary


def test_wall_pair_byte_pins_stand() -> None:
    """The BE-9 wall file byte pin + BE-8 presence (BE-11 law recited
    unchanged by this band)."""
    import hashlib
    sha = hashlib.sha256(
        (BACKEND_DIR / "tests/test_v2_be9_boundaries.py").read_bytes()
    ).hexdigest()
    assert sha == ("9ba9fd8290d5861911582a5286752c7ed5aee71c06e"
                   "56acb9f4ac4337355f91f")
    assert (BACKEND_DIR / "tests/test_v2_be8_boundaries.py").exists()


def test_no_submission_verbs_outside_boundary() -> None:
    """AMENDED BY CITATION (BO-V2-BE12B-001 SS1.b; supersedes the 12A
    package-wide form): order-transport verbs stay banned in every
    live_exec file EXCEPT `adapter_boundary.py` (name-literal — the one
    doorway, which itself speaks only the provider-leg actuator name,
    `practice_order_send`, never a raw terminal verb)."""
    package = BACKEND_DIR / "app/v2/live_exec"
    banned = ("order_send", "OrderSend", "TRADE_ACTION", "ORDER_TYPE",
              "position_open", "market_order(")
    offenders = []
    for path in package.rglob("*.py"):
        if path.name == "adapter_boundary.py":
            continue  # scoped exception (BO SS1.b); scanned separately
        text = path.read_text(encoding="utf-8")
        for needle in banned:
            if needle in text:
                offenders.append(f"{path.name}:{needle}")
    assert offenders == []
    # boundary file: the ONLY transport token is the actuator name
    boundary = (package / "adapter_boundary.py").read_text(encoding="utf-8")
    for needle in ("OrderSend", "TRADE_ACTION", "ORDER_TYPE",
                   "position_open", "market_order("):
        assert needle not in boundary
    assert "practice_order_send" in boundary


# --- R2 border coupon (ITRGA-REV-V2-BE12A-001 §14; V2-BE12A-DEL-001) ---------------


def test_api_writer_persists_under_alembic_guards(tmp_path: Path) -> None:
    """THE border coupon: the fielded write path against the
    alembic-0053-applied chain (triggers PRESENT — not a create_all
    world). POST /live-exec/intents must answer 200 with the row
    persisted (born complete, no UPDATE), and the duplicate arm must
    answer the typed refusal. This is the witness whose absence was
    V2-BE12A-DEL-001's cover."""
    import importlib

    from fastapi.testclient import TestClient

    db_file, _ = _db(tmp_path, REV_0053)

    from app.core.config import clear_settings_cache
    prior = os.environ.get("AXIOM_DATABASE_URL")
    os.environ["AXIOM_DATABASE_URL"] = f"sqlite+aiosqlite:///{db_file}"
    try:
        clear_settings_cache()
        main = importlib.import_module("app.main")
        with TestClient(main.create_app()) as client:
            login = client.post(
                "/api/v1/auth/login",
                json={"username": "admin", "password": "admin123"})
            assert login.status_code == 200, login.text
            headers = {"Authorization":
                       f"Bearer {login.json()['tokens']['access_token']}"}
            body = {"idempotency_key": "border-1",
                    "requested_basis_id": "basis-border",
                    "payload": {"instrument": "forex.eurusd"},
                    "step_up_ref": "mfa-border-1"}
            first = client.post("/api/v1/v2/live-exec/intents",
                                json=body, headers=headers)
            assert first.status_code == 200, first.text
            intent = first.json()["intent"]
            assert intent["record_state"] == "registered"
            # actuation door refusal carried on the envelope (12A truth)
            assert "actuation_refusal" in first.json()
            # duplicate arm: typed, never a 500, never a second row
            dup = client.post("/api/v1/v2/live-exec/intents",
                              json=body, headers=headers)
            assert dup.status_code == 409, dup.text
            assert dup.json()["refusal"]["reason"] == "duplicate_intent"
    finally:
        if prior is None:
            os.environ.pop("AXIOM_DATABASE_URL", None)
        else:
            os.environ["AXIOM_DATABASE_URL"] = prior
        clear_settings_cache()

    # Level-I re-proof on the file AFTER the app closed: exactly one row,
    # step_up_ref present from BIRTH (no UPDATE ever ran - guards intact)
    rows = _q(db_file, "SELECT idempotency_key, step_up_ref, record_state"
                       " FROM v2_live_exec_intent")
    assert rows == [("border-1", "mfa-border-1", "registered")]
    guard = _q(db_file, "SELECT COUNT(*) FROM sqlite_master WHERE"
                        " type='trigger' AND name LIKE"
                        " 'v2_live_exec_intent_immutable_%'")[0][0]
    assert guard == 2
