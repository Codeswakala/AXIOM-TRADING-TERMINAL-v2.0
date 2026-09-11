"""V2 BE-12B migration + LAW-BORDER-01 coupons (BO §1.g/§2/§4).

One-upgrade-line law; census tattoo 84/75/14; lxe compver row DB==disk;
guard fires; downgrade exact (80/72/13 restored); drift gate; the
submission/fill engines Level-I; LAW-BORDER-01 border coupons for BOTH
new gated writers over the alembic-applied chain.
"""

from __future__ import annotations

import os
import sqlite3
import subprocess
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
TRANS_AUTHORITY = "BO-V2-BE-3-P2-TRANS-001"
REV_0053 = "20260909_0053"
REV_0054 = "20260909_0054"

PERMS_0054 = {
    ("admin", "v2.live_exec.submit.write", "SAL-4"),
    ("admin", "v2.live_exec.submissions.read", "SAL-2"),
    ("admin", "v2.live_exec.fills.read", "SAL-2"),
}

TRIGGERS_0054 = {
    "v2_live_exec_submission_immutable_update",
    "v2_live_exec_submission_immutable_delete",
    "v2_live_exec_fill_event_immutable_update",
    "v2_live_exec_fill_event_immutable_delete",
}

_LXE_FILES = (
    "app/v2/live_exec/intents.py",
    "app/v2/live_exec/eligibility.py",
    "app/v2/live_exec/risk.py",
    "app/v2/live_exec/locks.py",
    "app/v2/live_exec/submissions.py",
    "app/v2/live_exec/ack_fills.py",
)


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
    db_file = tmp_path / "be12b.db"
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


def test_one_upgrade_line_0053_to_0054(tmp_path: Path) -> None:
    db_file, db_url = _db(tmp_path, REV_0053)
    result = _alembic(["upgrade", REV_0054], db_url)
    assert result.returncode == 0, result.stderr
    both = result.stdout + result.stderr
    lines = [ln for ln in both.splitlines() if "Running upgrade" in ln]
    assert len(lines) == 1, lines
    assert f"{REV_0053} -> {REV_0054}" in lines[0]


def test_census_tattoo_84_75_14_and_lxe_row(tmp_path: Path) -> None:
    import hashlib
    db_file, _ = _db(tmp_path, REV_0054)
    trig = _q(db_file, "SELECT COUNT(*) FROM sqlite_master WHERE"
                       " type='trigger'")[0][0]
    perm = _q(db_file, "SELECT COUNT(*) FROM v2_permission")[0][0]
    comp = _q(db_file, "SELECT COUNT(*) FROM v2_computation_version")[0][0]
    assert (trig, perm, comp) == (84, 75, 14)
    rows = {(r, p, s) for r, p, s in _q(
        db_file, "SELECT role, permission, sal FROM v2_permission"
                 " WHERE permission LIKE 'v2.live_exec.%'"
                 " AND (permission LIKE '%submit%'"
                 " OR permission LIKE '%submissions%'"
                 " OR permission LIKE '%fills%')")}
    assert rows == PERMS_0054
    names = {x[0] for x in _q(db_file, "SELECT name FROM sqlite_master"
                                       " WHERE type='trigger'")}
    assert TRIGGERS_0054 <= names
    # lxe compver row: DB == fresh disk recompute (naming-of-numbers law)
    row = _q(db_file, "SELECT version, source_hash FROM"
                      " v2_computation_version WHERE"
                      " component='live_exec_engine'")[0]
    digest = hashlib.sha256()
    for ref in _LXE_FILES:
        digest.update(ref.encode())
        digest.update(b"\x00")
        digest.update((BACKEND_DIR / ref).read_bytes())
        digest.update(b"\x00")
    assert row == ("lxe-1.0.0", digest.hexdigest())


def test_downgrade_reverses_exactly(tmp_path: Path) -> None:
    db_file, db_url = _db(tmp_path, REV_0054)
    result = _alembic(["downgrade", REV_0053], db_url)
    assert result.returncode == 0, result.stderr
    trig = _q(db_file, "SELECT COUNT(*) FROM sqlite_master WHERE"
                       " type='trigger'")[0][0]
    perm = _q(db_file, "SELECT COUNT(*) FROM v2_permission")[0][0]
    comp = _q(db_file, "SELECT COUNT(*) FROM v2_computation_version")[0][0]
    assert (trig, perm, comp) == (80, 72, 13)  # the 0053 tattoo restored
    tables = {x[0] for x in _q(db_file, "SELECT name FROM sqlite_master"
                                        " WHERE type='table'")}
    assert "v2_live_exec_submission" not in tables
    assert "v2_live_exec_fill_event" not in tables
    guard = _q(db_file, "SELECT COUNT(*) FROM sqlite_master WHERE"
                        " type='trigger' AND name="
                        "'v2_computation_version_immutable_delete'")[0][0]
    assert guard == 1  # delete-guard dance restored


def test_drift_gate_0054(tmp_path: Path) -> None:
    db_file, db_url = _db(tmp_path, REV_0054)
    check = _alembic(["check"], db_url)
    drift = (check.stdout + check.stderr).lower()
    assert check.returncode != 0
    assert "live_exec" not in drift, "BE-12B drift at 0054"
    if "not up to date" not in drift:
        assert "audit_write_failure_records" in drift


# --- LAW-BORDER-01: both new gated writers over the alembic-applied chain -----------


def _client_on_chain(db_file: Path):
    import importlib

    from fastapi.testclient import TestClient

    from app.core.config import clear_settings_cache
    os.environ["AXIOM_DATABASE_URL"] = f"sqlite+aiosqlite:///{db_file}"
    clear_settings_cache()
    main = importlib.import_module("app.main")
    return TestClient(main.create_app())


def _restore_env(prior):
    from app.core.config import clear_settings_cache
    if prior is None:
        os.environ.pop("AXIOM_DATABASE_URL", None)
    else:
        os.environ["AXIOM_DATABASE_URL"] = prior
    clear_settings_cache()


def test_border_submit_writer_under_alembic_guards(tmp_path: Path) -> None:
    """LAW-BORDER-01 coupon #1: the submit writer through the 0054
    chain (triggers PRESENT). On this station the lawful outcome is the
    typed practice-lane refusal (posture absent — no vault resolves) and
    ZERO rows persisted; the 404 arm and the refusal envelope prove the
    writer's whole path executes against the guarded schema."""
    db_file, _ = _db(tmp_path, REV_0054)
    prior = os.environ.get("AXIOM_DATABASE_URL")
    try:
        with _client_on_chain(db_file) as client:
            login = client.post(
                "/api/v1/auth/login",
                json={"username": "admin", "password": "admin123"})
            assert login.status_code == 200, login.text
            headers = {"Authorization":
                       f"Bearer {login.json()['tokens']['access_token']}"}
            # arm 1: intent absent => typed 404
            miss = client.post(
                "/api/v1/v2/live-exec/intents/no-such-id/submit",
                json={"order_request": {}}, headers=headers)
            assert miss.status_code == 404, miss.text
            assert miss.json()["refusal"]["reason"] == "intent_not_found"
            # arm 2: register an intent, then submit => practice-lane
            # typed refusal (mode RESEARCH on this world), zero rows
            reg = client.post(
                "/api/v1/v2/live-exec/intents", headers=headers,
                json={"idempotency_key": "border-12b-1",
                      "requested_basis_id": "basis-b",
                      "payload": {"instrument": "forex.eurusd"},
                      "step_up_ref": "mfa-b-1"})
            assert reg.status_code == 200, reg.text
            intent_id = reg.json()["intent"]["id"]
            sub = client.post(
                f"/api/v1/v2/live-exec/intents/{intent_id}/submit",
                json={"order_request": {}, "basis_age_hours": 2.0},
                headers=headers)
            assert sub.status_code == 409, sub.text
            assert sub.json()["refusal"]["reason"] == \
                "practice_mode_not_armed"
            # reads live on the same chain
            subs = client.get("/api/v1/v2/live-exec/submissions",
                              headers=headers)
            assert subs.status_code == 200
            assert subs.json()["submissions"] == []
    finally:
        _restore_env(prior)
    # Level-I: refusals persisted NOTHING; guards intact
    assert _q(db_file, "SELECT COUNT(*) FROM v2_live_exec_submission"
              )[0][0] == 0
    assert _q(db_file, "SELECT COUNT(*) FROM v2_live_exec_intent"
              )[0][0] == 1


def test_border_persistence_paths_under_guards(tmp_path: Path) -> None:
    """LAW-BORDER-01 coupon #2: the persistence engines write through
    the guarded schema directly (async session on the 0054 chain):
    submission row born complete (incl. quarantine transition);
    duplicate_submission typed; fill event + dedupe anchor typed AND
    schema-fatal on bypass; UPDATE/DELETE guards fire on both tables."""
    import asyncio

    from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

    from app.db.models.v2_live_exec import V2LiveExecIntent
    from app.v2.live_exec.ack_fills import persist_fill_event
    from app.v2.live_exec.intents import LiveExecRefused
    from app.v2.live_exec.submissions import persist_submission

    db_file, _ = _db(tmp_path, REV_0054)

    async def run():
        eng = create_async_engine(f"sqlite+aiosqlite:///{db_file}")
        outcomes = {}
        try:
            async with AsyncSession(eng) as s:
                intent = V2LiveExecIntent(
                    idempotency_key="b2-1", requested_basis_id="basis",
                    posture="capability", payload={}, digest="d" * 64,
                    record_state="registered", actor_id="t",
                    data_class="simulated", mode="PAPER", operator_id="t")
                s.add(intent)
                await s.flush()
                sub = await persist_submission(
                    s, intent=intent, order_request={"v": 1},
                    terminal_answer={"terminal_state": "no_answer",
                                     "server_ack_ref": None,
                                     "raw_note": "injected timeout"},
                    actor_id="t", mode="PAPER", operator_id="t")
                outcomes["quarantine"] = sub.terminal_state
                try:
                    await persist_submission(
                        s, intent=intent, order_request={"v": 2},
                        terminal_answer={"terminal_state": "accepted"},
                        actor_id="t", mode="PAPER", operator_id="t")
                except LiveExecRefused as refused:
                    outcomes["dup_submission"] = refused.reason
                fill = await persist_fill_event(
                    s, submission=sub, correlation_basis="server_ack_ref",
                    correlation_ref="ack-1",
                    fill_payload={"deal_id": "D1", "volume": "0.01",
                                  "price": "1.1", "time": "t1"},
                    actor_id="t", mode="PAPER", operator_id="t")
                outcomes["fill_id"] = fill.fill_event_identity
                try:
                    await persist_fill_event(
                        s, submission=sub,
                        correlation_basis="server_ack_ref",
                        correlation_ref="ack-1",
                        fill_payload={"deal_id": "D1", "volume": "0.01",
                                      "price": "1.1", "time": "t1"},
                        actor_id="t", mode="PAPER", operator_id="t")
                except LiveExecRefused as refused:
                    outcomes["dup_fill"] = refused.reason
                await s.commit()
        finally:
            await eng.dispose()
        return outcomes

    outcomes = asyncio.run(run())
    assert outcomes["quarantine"] == "quarantined_unknown"
    assert outcomes["dup_submission"] == "duplicate_submission"
    assert outcomes["dup_fill"] == "duplicate_fill_event"
    # Level-I + guard fires on the file
    conn = sqlite3.connect(db_file)
    try:
        assert conn.execute("SELECT COUNT(*) FROM"
                            " v2_live_exec_submission").fetchone()[0] == 1
        assert conn.execute("SELECT COUNT(*) FROM"
                            " v2_live_exec_fill_event").fetchone()[0] == 1
        for sql in ("UPDATE v2_live_exec_submission SET actor_id='x'",
                    "DELETE FROM v2_live_exec_submission",
                    "UPDATE v2_live_exec_fill_event SET actor_id='x'",
                    "DELETE FROM v2_live_exec_fill_event"):
            try:
                conn.execute(sql)
                raise AssertionError(f"guard failed open: {sql}")
            except sqlite3.IntegrityError:
                pass
        # dedupe anchor is schema-fatal even on engine bypass
        try:
            conn.execute(
                "INSERT INTO v2_live_exec_fill_event (id, submission_id,"
                " fill_event_identity, correlation_basis, correlation_ref,"
                " fill_payload, actor_id, data_class, mode, operator_id,"
                " created_at) SELECT 'x-1', submission_id,"
                " fill_event_identity, correlation_basis, correlation_ref,"
                " fill_payload, actor_id, data_class, mode, operator_id,"
                " created_at FROM v2_live_exec_fill_event")
            raise AssertionError("identity uq failed open")
        except sqlite3.IntegrityError:
            pass
    finally:
        conn.close()


def test_border_armed_pass_full_api_submit(tmp_path: Path) -> None:
    """R2 (ITRGA-REV-V2-BE12B-001 §14; closes V2-BE12B-DEL-001's missing
    witness): THE ARMED-PASS BORDER COUPON — sealed practice vault +
    lawful R1 provisioning (both env names) + injected fake terminal
    answering `accepted` => the FULL API submit path persists ONE
    accepted row on the alembic-0054 chain, guards intact. Then the
    counter-arm: WITHOUT the vault, the same ask types P3
    `practice_posture_absent` (the pre-patch constant, now reachable
    ONLY when the posture is truly absent)."""
    import app.v2.broker_read.providers.practice_actuator as actuator
    from app.v2.broker_read.vault import seal_practice_vault_bytes

    db_file, _ = _db(tmp_path, REV_0054)

    # lawful provisioning: sealed vault + both env names (console-act shape)
    vault_file = tmp_path / "practice.vault"
    vault_file.write_bytes(seal_practice_vault_bytes(
        "gate-passphrase", "practice-secret", "999001", "Srv-1"))

    class _Result:
        retcode = 10009
        order = "777123"

    class _FakeMt5:
        TRADE_RETCODE_DONE = 10009
        TRADE_RETCODE_REQUOTE = 10004

        def order_send(self, req):
            return _Result()

    prior_db = os.environ.get("AXIOM_DATABASE_URL")
    prior_mode = os.environ.get("AXIOM_V2_MODE")
    orig_terminal = actuator._terminal
    os.environ["AXIOM_BROKER_PRACTICE_VAULT_PATH"] = str(vault_file)
    os.environ["AXIOM_BROKER_PRACTICE_VAULT_PASSPHRASE"] = "gate-passphrase"
    os.environ["AXIOM_V2_MODE"] = "PAPER"  # D-2 law: practice lane arms in PAPER
    actuator._terminal = lambda: _FakeMt5()
    try:
        with _client_on_chain(db_file) as client:
            login = client.post(
                "/api/v1/auth/login",
                json={"username": "admin", "password": "admin123"})
            assert login.status_code == 200, login.text
            headers = {"Authorization":
                       f"Bearer {login.json()['tokens']['access_token']}"}
            reg = client.post(
                "/api/v1/v2/live-exec/intents", headers=headers,
                json={"idempotency_key": "armed-1",
                      "requested_basis_id": "basis-armed",
                      "payload": {"instrument": "forex.eurusd"},
                      "step_up_ref": "mfa-armed-1"})
            assert reg.status_code == 200, reg.text
            intent_id = reg.json()["intent"]["id"]
            sub = client.post(
                f"/api/v1/v2/live-exec/intents/{intent_id}/submit",
                json={"order_request": {"symbol": "EURUSDm",
                                        "volume": 0.01},
                      "basis_age_hours": 2.0},
                headers=headers)
            assert sub.status_code == 200, sub.text
            record = sub.json()["submission"]
            assert record["terminal_state"] == "accepted"
            assert record["server_ack_ref"] == "777123"
            # duplicate arm on the SAME armed world: typed, one row stays
            dup = client.post(
                f"/api/v1/v2/live-exec/intents/{intent_id}/submit",
                json={"order_request": {"symbol": "EURUSDm",
                                        "volume": 0.01},
                      "basis_age_hours": 2.0},
                headers=headers)
            assert dup.status_code == 409, dup.text
            assert dup.json()["refusal"]["reason"] == "duplicate_submission"
            # counter-arm: WITHOUT the vault, P3 types (not a 500, not
            # a LIVE-lane word) — the constant-ABSENT behavior is now
            # lawful ONLY when the posture is truly absent
            os.environ.pop("AXIOM_BROKER_PRACTICE_VAULT_PATH", None)
            reg2 = client.post(
                "/api/v1/v2/live-exec/intents", headers=headers,
                json={"idempotency_key": "armed-2",
                      "requested_basis_id": "basis-armed",
                      "payload": {"instrument": "forex.eurusd"},
                      "step_up_ref": "mfa-armed-2"})
            assert reg2.status_code == 200
            bare = client.post(
                f"/api/v1/v2/live-exec/intents/"
                f"{reg2.json()['intent']['id']}/submit",
                json={"order_request": {}, "basis_age_hours": 2.0},
                headers=headers)
            assert bare.status_code == 409, bare.text
            assert bare.json()["refusal"]["reason"] == \
                "practice_posture_absent"
    finally:
        actuator._terminal = orig_terminal
        os.environ.pop("AXIOM_BROKER_PRACTICE_VAULT_PATH", None)
        os.environ.pop("AXIOM_BROKER_PRACTICE_VAULT_PASSPHRASE", None)
        if prior_mode is None:
            os.environ.pop("AXIOM_V2_MODE", None)
        else:
            os.environ["AXIOM_V2_MODE"] = prior_mode
        _restore_env(prior_db)
    # Level-I on the file after close: EXACTLY ONE submission row, born
    # accepted with the ack ref; guards intact
    rows = _q(db_file, "SELECT intent_id, lane, terminal_state,"
                       " server_ack_ref FROM v2_live_exec_submission")
    assert len(rows) == 1
    assert rows[0][1:] == ("practice", "accepted", "777123")
    guard = _q(db_file, "SELECT COUNT(*) FROM sqlite_master WHERE"
                        " type='trigger' AND name LIKE"
                        " 'v2_live_exec_submission_immutable_%'")[0][0]
    assert guard == 2
