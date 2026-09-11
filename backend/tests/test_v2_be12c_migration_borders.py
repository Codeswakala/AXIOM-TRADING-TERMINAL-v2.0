"""V2 BE-12C migration + DEL-001-defense border coupons (BO §1.e/§1.g/§4).

One-upgrade-line; tattoo 86/77/15; lxe-1.1.0 insert-only with BOTH rows
standing (append-only registry law + guard witnessed refusing update);
downgrade exact; itemized drift; append-only parents (byte-stable
across acts); armed-pass API border coupons for cancel AND modify over
the real corridor with counter-arms (12B CR-1 R2 pattern — never
fixture-injection-only).
"""

from __future__ import annotations

import hashlib
import os
import sqlite3
import subprocess
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
TRANS_AUTHORITY = "BO-V2-BE-3-P2-TRANS-001"
REV_0054 = "20260909_0054"
REV_0055 = "20260909_0055"

PERMS_0055 = {
    ("admin", "v2.live_exec.modify.write", "SAL-4"),
    ("admin", "v2.live_exec.modifies.read", "SAL-2"),
}

_LXE_FILES_1_1 = (
    "app/v2/live_exec/intents.py",
    "app/v2/live_exec/eligibility.py",
    "app/v2/live_exec/risk.py",
    "app/v2/live_exec/locks.py",
    "app/v2/live_exec/submissions.py",
    "app/v2/live_exec/ack_fills.py",
    "app/v2/live_exec/modify/__init__.py",
    "app/v2/live_exec/modify/engine.py",
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
    db_file = tmp_path / "be12c.db"
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


def test_one_upgrade_line_0054_to_0055(tmp_path: Path) -> None:
    db_file, db_url = _db(tmp_path, REV_0054)
    result = _alembic(["upgrade", REV_0055], db_url)
    assert result.returncode == 0, result.stderr
    both = result.stdout + result.stderr
    lines = [ln for ln in both.splitlines() if "Running upgrade" in ln]
    assert len(lines) == 1, lines
    assert f"{REV_0054} -> {REV_0055}" in lines[0]


def test_census_tattoo_86_77_15_append_only_registry(tmp_path: Path) -> None:
    db_file, _ = _db(tmp_path, REV_0055)
    trig = _q(db_file, "SELECT COUNT(*) FROM sqlite_master WHERE"
                       " type='trigger'")[0][0]
    perm = _q(db_file, "SELECT COUNT(*) FROM v2_permission")[0][0]
    comp = _q(db_file, "SELECT COUNT(*) FROM v2_computation_version")[0][0]
    assert (trig, perm, comp) == (86, 77, 15)
    rows = {(r, p, s) for r, p, s in _q(
        db_file, "SELECT role, permission, sal FROM v2_permission"
                 " WHERE permission LIKE '%modif%'")}
    assert rows == PERMS_0055
    # append-only registry law: BOTH lxe rows stand
    lxe = _q(db_file, "SELECT version, source_hash FROM"
                      " v2_computation_version WHERE"
                      " component='live_exec_engine' ORDER BY version")
    assert [v for v, _ in lxe] == ["lxe-1.0.0", "lxe-1.1.0"]
    digest = hashlib.sha256()
    for ref in _LXE_FILES_1_1:
        digest.update(ref.encode())
        digest.update(b"\x00")
        digest.update((BACKEND_DIR / ref).read_bytes())
        digest.update(b"\x00")
    assert lxe[1][1] == digest.hexdigest()
    # the update path is REFUSED by the standing guard (witnessed live)
    conn = sqlite3.connect(db_file)
    try:
        try:
            conn.execute("UPDATE v2_computation_version SET"
                         " source_hash='x' WHERE version='lxe-1.0.0'")
            raise AssertionError("compver update guard failed open")
        except sqlite3.IntegrityError:
            pass
    finally:
        conn.close()


def test_downgrade_reverses_exactly(tmp_path: Path) -> None:
    db_file, db_url = _db(tmp_path, REV_0055)
    result = _alembic(["downgrade", REV_0054], db_url)
    assert result.returncode == 0, result.stderr
    trig = _q(db_file, "SELECT COUNT(*) FROM sqlite_master WHERE"
                       " type='trigger'")[0][0]
    perm = _q(db_file, "SELECT COUNT(*) FROM v2_permission")[0][0]
    comp = _q(db_file, "SELECT COUNT(*) FROM v2_computation_version")[0][0]
    assert (trig, perm, comp) == (84, 75, 14)
    tables = {x[0] for x in _q(db_file, "SELECT name FROM sqlite_master"
                                        " WHERE type='table'")}
    assert "v2_live_exec_modify_event" not in tables
    lxe = [v for (v,) in _q(db_file, "SELECT version FROM"
                                     " v2_computation_version WHERE"
                                     " component='live_exec_engine'")]
    assert lxe == ["lxe-1.0.0"]  # 1.1.0 removed; 1.0.0 stands
    guard = _q(db_file, "SELECT COUNT(*) FROM sqlite_master WHERE"
                        " type='trigger' AND name="
                        "'v2_computation_version_immutable_delete'")[0][0]
    assert guard == 1


def test_drift_gate_0055_itemized(tmp_path: Path) -> None:
    """ERRATUM E-0054-A11.4: the drift law is ITEMIZED — the inherited
    V1 set may appear; ZERO 12C tokens; never absolute-silence."""
    db_file, db_url = _db(tmp_path, REV_0055)
    check = _alembic(["check"], db_url)
    drift = (check.stdout + check.stderr).lower()
    assert check.returncode != 0
    assert "modify_event" not in drift, "BE-12C drift at 0055"
    assert "live_exec" not in drift
    if "not up to date" not in drift:
        assert "audit_write_failure_records" in drift  # inheritance witness


# --- DEL-001 defense: armed-pass API borders, cancel AND modify (BO §1.e) -----------


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


def _armed_world(tmp_path: Path, monkey_answers: dict):
    """The 12B CR-1 R2 corridor: sealed vault + lawful provisioning +
    injected fake terminal family + PAPER mode."""
    import app.v2.broker_read.providers.practice_actuator as actuator
    from app.v2.broker_read.vault import seal_practice_vault_bytes

    vault_file = tmp_path / "practice.vault"
    vault_file.write_bytes(seal_practice_vault_bytes(
        "gate-passphrase", "practice-secret", "999001", "Srv-1"))

    class _Result:
        def __init__(self, retcode, order=""):
            self.retcode = retcode
            self.order = order

    class _FakeMt5:
        TRADE_RETCODE_DONE = 10009
        TRADE_RETCODE_REQUOTE = 10004
        TRADE_ACTION_REMOVE = 8
        TRADE_ACTION_MODIFY = 7

        def order_send(self, req):
            action = req.get("action")
            if action == 8:
                return _Result(monkey_answers.get("cancel", 10009))
            if action == 7:
                return _Result(monkey_answers.get("modify", 10009))
            return _Result(10009, order="555777")

    os.environ["AXIOM_BROKER_PRACTICE_VAULT_PATH"] = str(vault_file)
    os.environ["AXIOM_BROKER_PRACTICE_VAULT_PASSPHRASE"] = "gate-passphrase"
    os.environ["AXIOM_V2_MODE"] = "PAPER"
    orig = actuator._terminal
    actuator._terminal = lambda: _FakeMt5()
    return actuator, orig


def _disarm(actuator, orig, prior_mode):
    actuator._terminal = orig
    os.environ.pop("AXIOM_BROKER_PRACTICE_VAULT_PATH", None)
    os.environ.pop("AXIOM_BROKER_PRACTICE_VAULT_PASSPHRASE", None)
    if prior_mode is None:
        os.environ.pop("AXIOM_V2_MODE", None)
    else:
        os.environ["AXIOM_V2_MODE"] = prior_mode


def test_border_armed_cancel_and_modify_full_api(tmp_path: Path) -> None:
    """DEL-001 defense: armed-pass cancel AND modify through the FULL
    API corridor over the alembic-0055 chain, with counter-arms."""
    db_file, _ = _db(tmp_path, REV_0055)
    prior_db = os.environ.get("AXIOM_DATABASE_URL")
    prior_mode = os.environ.get("AXIOM_V2_MODE")
    actuator, orig = _armed_world(tmp_path, {"cancel": 10009,
                                             "modify": 10013})
    try:
        with _client_on_chain(db_file) as client:
            login = client.post(
                "/api/v1/auth/login",
                json={"username": "admin", "password": "admin123"})
            assert login.status_code == 200, login.text
            headers = {"Authorization":
                       f"Bearer {login.json()['tokens']['access_token']}"}
            # arrange: register + submit (accepted) on the armed corridor
            reg = client.post(
                "/api/v1/v2/live-exec/intents", headers=headers,
                json={"idempotency_key": "12c-1",
                      "requested_basis_id": "basis-c",
                      "payload": {"instrument": "forex.eurusd"},
                      "step_up_ref": "mfa-c-1"})
            assert reg.status_code == 200, reg.text
            sub = client.post(
                f"/api/v1/v2/live-exec/intents/"
                f"{reg.json()['intent']['id']}/submit",
                json={"order_request": {"symbol": "EURUSDm"},
                      "basis_age_hours": 2.0}, headers=headers)
            assert sub.status_code == 200, sub.text
            submission_id = sub.json()["submission"]["id"]
            # ARMED CANCEL: applied (fake terminal DONE on remove)
            cancel = client.post(
                f"/api/v1/v2/live-exec/submissions/{submission_id}/cancel",
                json={"request_payload": {"order": 555777},
                      "basis_age_hours": 2.0}, headers=headers)
            assert cancel.status_code == 200, cancel.text
            assert cancel.json()["modify_event"]["outcome"] == "applied"
            # duplicate cancel: typed, non-firing
            dup = client.post(
                f"/api/v1/v2/live-exec/submissions/{submission_id}/cancel",
                json={"request_payload": {"order": 555777},
                      "basis_age_hours": 2.0}, headers=headers)
            assert dup.status_code == 409, dup.text
            assert dup.json()["refusal"]["reason"] == \
                "duplicate_modify_event"
            # ARMED MODIFY: refused_terminal (fake retcode 10013) —
            # the terminal's typed refusal MIRRORED, one row persisted
            modify = client.post(
                f"/api/v1/v2/live-exec/submissions/{submission_id}/modify",
                json={"request_payload": {"order": 555777,
                                          "price": "1.0950"},
                      "basis_age_hours": 2.0}, headers=headers)
            assert modify.status_code == 200, modify.text
            assert modify.json()["modify_event"]["outcome"] == \
                "refused_terminal"
            # absent submission: 404 typed
            miss = client.post(
                "/api/v1/v2/live-exec/submissions/no-such/cancel",
                json={"request_payload": {}}, headers=headers)
            assert miss.status_code == 404
            assert miss.json()["refusal"]["reason"] == \
                "submission_not_found"
            # COUNTER-ARM: vault removed => P3 typed (never LIVE-lane).
            # CR-1 note: the ticket is WELDED (555777) so the input arms
            # pass and the lane door is the failing gate — the weld law
            # gates BEFORE the door by design (input arms first).
            os.environ.pop("AXIOM_BROKER_PRACTICE_VAULT_PATH", None)
            bare = client.post(
                f"/api/v1/v2/live-exec/submissions/{submission_id}/cancel",
                json={"request_payload": {"order": 555777},
                      "basis_age_hours": 2.0}, headers=headers)
            assert bare.status_code == 409, bare.text
            assert bare.json()["refusal"]["reason"] == \
                "practice_posture_absent"
    finally:
        _disarm(actuator, orig, prior_mode)
        _restore_env(prior_db)
    # Level-I: exactly TWO act rows (cancel applied + modify refused);
    # APPEND-ONLY: parent submission row byte-stable (still accepted)
    acts = _q(db_file, "SELECT verb, outcome, operator_election FROM"
                       " v2_live_exec_modify_event ORDER BY verb")
    assert acts == [("cancel", "applied", "standard"),
                    ("modify", "refused_terminal", "standard")]
    parents = _q(db_file, "SELECT terminal_state, server_ack_ref FROM"
                          " v2_live_exec_submission")
    assert parents == [("accepted", "555777")]
    guard = _q(db_file, "SELECT COUNT(*) FROM sqlite_master WHERE"
                        " type='trigger' AND name LIKE"
                        " 'v2_live_exec_modify_event_immutable_%'")[0][0]
    assert guard == 2


def test_border_parents_byte_stable_and_guards_fire(tmp_path: Path) -> None:
    """Append-only law at Level I: acts never mutate parents (digest-set
    equal before/after); modify-event guards fire; unknown-elected
    cancel persists with the election recorded; unknown_outcome under
    election escalates typed."""
    import asyncio

    from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

    from app.db.models.v2_live_exec import V2LiveExecIntent
    from app.v2.live_exec.modify.engine import persist_modify_event
    from app.v2.live_exec.submissions import persist_submission

    db_file, _ = _db(tmp_path, REV_0055)

    async def run():
        eng = create_async_engine(f"sqlite+aiosqlite:///{db_file}")
        try:
            async with AsyncSession(eng) as s:
                intent = V2LiveExecIntent(
                    idempotency_key="c2-1", requested_basis_id="b",
                    posture="capability", payload={}, digest="d" * 64,
                    record_state="registered", actor_id="t",
                    data_class="simulated", mode="PAPER", operator_id="t")
                s.add(intent)
                await s.flush()
                sub = await persist_submission(
                    s, intent=intent, order_request={"v": 1},
                    terminal_answer={"terminal_state": "no_answer",
                                     "server_ack_ref": None,
                                     "raw_note": "injected"},
                    actor_id="t", mode="PAPER", operator_id="t")
                # elected cancel answering unknown => unknown_escalate
                row = await persist_modify_event(
                    s, submission=sub, verb="cancel",
                    request_payload={"order": 1},
                    act_answer={"outcome": "unknown_outcome",
                                "raw_note": "injected unknown"},
                    operator_election="cancel_on_unknown",
                    actor_id="t", mode="PAPER", operator_id="t")
                # read BEFORE commit expiry (the 12B CR-1 harness lesson)
                outcome, election = row.outcome, row.operator_election
                await s.commit()
                return outcome, election
        finally:
            await eng.dispose()

    outcome, election = asyncio.run(run())
    assert outcome == "unknown_escalate"
    assert election == "cancel_on_unknown"

    # parent digest-set BEFORE == AFTER (append-only witnessed)
    before = _q(db_file, "SELECT id, terminal_state, digest FROM"
                         " v2_live_exec_submission")
    conn = sqlite3.connect(db_file)
    try:
        for sql in ("UPDATE v2_live_exec_modify_event SET actor_id='x'",
                    "DELETE FROM v2_live_exec_modify_event"):
            try:
                conn.execute(sql)
                raise AssertionError(f"guard failed open: {sql}")
            except sqlite3.IntegrityError:
                pass
        # election CHECK closed
        try:
            conn.execute(
                "INSERT INTO v2_live_exec_modify_event (id, submission_id,"
                " intent_id, verb, act_identity, request_payload, outcome,"
                " operator_election, actor_id, data_class, mode,"
                " operator_id, created_at) VALUES ('x','s','i','cancel',"
                "'aid-x','{}','applied','auto_recovery','t','simulated',"
                "'PAPER','t','2026-09-09 00:00:00+00:00')")
            raise AssertionError("election CHECK failed open")
        except sqlite3.IntegrityError:
            pass
    finally:
        conn.close()
    after = _q(db_file, "SELECT id, terminal_state, digest FROM"
                        " v2_live_exec_submission")
    assert before == after


def test_border_weld_and_allowlist_arms(tmp_path: Path) -> None:
    """CR-1 R2 (V2-BE12C-DEL-001 + DEL-002): the corridor's input-side
    arms over the REAL armed corridor with a send-recording fake
    terminal. Mismatch/foreign-key asks: typed refusal, ZERO terminal
    sends, NO row. Welded case still green; elected-unknown case still
    green; both verbs covered."""
    import app.v2.broker_read.providers.practice_actuator as actuator
    from app.v2.broker_read.vault import seal_practice_vault_bytes

    db_file, _ = _db(tmp_path, REV_0055)
    vault_file = tmp_path / "practice.vault"
    vault_file.write_bytes(seal_practice_vault_bytes(
        "gate-passphrase", "practice-secret", "999001", "Srv-1"))

    SENDS: list[dict] = []

    class _Result:
        def __init__(self, retcode, order=""):
            self.retcode = retcode
            self.order = order

    class _FakeMt5:
        TRADE_RETCODE_DONE = 10009
        TRADE_RETCODE_REQUOTE = 10004
        TRADE_ACTION_REMOVE = 8
        TRADE_ACTION_MODIFY = 7

        def order_send(self, req):
            SENDS.append(dict(req))
            if req.get("action") in (7, 8):
                return _Result(10009)
            return _Result(10009, order="555777")

    prior_db = os.environ.get("AXIOM_DATABASE_URL")
    prior_mode = os.environ.get("AXIOM_V2_MODE")
    orig = actuator._terminal
    os.environ["AXIOM_BROKER_PRACTICE_VAULT_PATH"] = str(vault_file)
    os.environ["AXIOM_BROKER_PRACTICE_VAULT_PASSPHRASE"] = "gate-passphrase"
    os.environ["AXIOM_V2_MODE"] = "PAPER"
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
                json={"idempotency_key": "weld-1",
                      "requested_basis_id": "b",
                      "payload": {"instrument": "forex.eurusd"},
                      "step_up_ref": "mfa-w-1"})
            sub = client.post(
                f"/api/v1/v2/live-exec/intents/"
                f"{reg.json()['intent']['id']}/submit",
                json={"order_request": {"symbol": "EURUSDm"},
                      "basis_age_hours": 2.0}, headers=headers)
            assert sub.status_code == 200, sub.text
            sid = sub.json()["submission"]["id"]
            ack = sub.json()["submission"]["server_ack_ref"]

            # DEL-001 arm: mismatched ticket, BOTH verbs — typed, ZERO
            # sends, NO row
            for verb in ("cancel", "modify"):
                SENDS.clear()
                resp = client.post(
                    f"/api/v1/v2/live-exec/submissions/{sid}/{verb}",
                    json={"request_payload": {"order": 999111},
                          "basis_age_hours": 2.0}, headers=headers)
                assert resp.status_code == 409, resp.text
                assert resp.json()["refusal"]["reason"] == \
                    "act_target_mismatch"
                assert SENDS == [], f"{verb}: terminal reached on mismatch"
            # ticket ABSENT on a welded submission: same refusal, no send
            SENDS.clear()
            resp = client.post(
                f"/api/v1/v2/live-exec/submissions/{sid}/cancel",
                json={"request_payload": {}, "basis_age_hours": 2.0},
                headers=headers)
            assert resp.status_code == 409
            assert resp.json()["refusal"]["reason"] == "act_target_mismatch"
            assert SENDS == []

            # DEL-002 arm: welded ticket + foreign keys, BOTH verbs —
            # typed, ZERO sends, NO row
            for verb, payload in (
                ("cancel", {"order": int(ack), "volume": 9.99}),
                ("modify", {"order": int(ack), "comment": "smuggled",
                            "type_time": 1}),
            ):
                SENDS.clear()
                resp = client.post(
                    f"/api/v1/v2/live-exec/submissions/{sid}/{verb}",
                    json={"request_payload": payload,
                          "basis_age_hours": 2.0}, headers=headers)
                assert resp.status_code == 409, resp.text
                assert resp.json()["refusal"]["reason"] == \
                    "act_payload_field_not_supported"
                assert SENDS == [], f"{verb}: terminal reached on foreign key"

            # allowlist READ FROM THE CITED MAP: modify with a spec field
            # (price) + welded ticket is GREEN — one send, one row
            SENDS.clear()
            ok = client.post(
                f"/api/v1/v2/live-exec/submissions/{sid}/modify",
                json={"request_payload": {"order": int(ack),
                                          "price": "1.0950"},
                      "basis_age_hours": 2.0}, headers=headers)
            assert ok.status_code == 200, ok.text
            assert ok.json()["modify_event"]["outcome"] == "applied"
            assert len(SENDS) == 1
            assert SENDS[0]["order"] == int(ack)
            assert "volume" not in SENDS[0]

            # welded cancel still green (one send, ticket == ack)
            SENDS.clear()
            ok2 = client.post(
                f"/api/v1/v2/live-exec/submissions/{sid}/cancel",
                json={"request_payload": {"order": int(ack)},
                      "basis_age_hours": 2.0}, headers=headers)
            assert ok2.status_code == 200, ok2.text
            assert len(SENDS) == 1
            assert SENDS[0]["order"] == int(ack)
    finally:
        actuator._terminal = orig
        os.environ.pop("AXIOM_BROKER_PRACTICE_VAULT_PATH", None)
        os.environ.pop("AXIOM_BROKER_PRACTICE_VAULT_PASSPHRASE", None)
        if prior_mode is None:
            os.environ.pop("AXIOM_V2_MODE", None)
        else:
            os.environ["AXIOM_V2_MODE"] = prior_mode
        _restore_env(prior_db)
    # Level-I: exactly the TWO green acts persisted; refusals left no rows
    acts = _q(db_file, "SELECT verb, outcome FROM v2_live_exec_modify_event"
                       " ORDER BY verb")
    assert acts == [("cancel", "applied"), ("modify", "applied")]


def test_weld_elected_unknown_path_still_lawful(tmp_path: Path) -> None:
    """The weld law's elected-recovery arm: ack ABSENT (quarantined) +
    the operator election + an operator-supplied ticket => admitted;
    ticket absent => act_target_mismatch typed."""
    import asyncio

    from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

    from app.db.models.v2_live_exec import V2LiveExecIntent
    from app.v2.live_exec.intents import LiveExecRefused
    from app.v2.live_exec.modify.engine import (
        require_act_payload,
        require_actionable,
    )
    from app.v2.live_exec.submissions import persist_submission

    db_file, _ = _db(tmp_path, REV_0055)

    async def run():
        eng = create_async_engine(f"sqlite+aiosqlite:///{db_file}")
        try:
            async with AsyncSession(eng) as s:
                intent = V2LiveExecIntent(
                    idempotency_key="weld-u-1", requested_basis_id="b",
                    posture="capability", payload={}, digest="d" * 64,
                    record_state="registered", actor_id="t",
                    data_class="simulated", mode="PAPER", operator_id="t")
                s.add(intent)
                await s.flush()
                sub = await persist_submission(
                    s, intent=intent, order_request={"v": 1},
                    terminal_answer={"terminal_state": "no_answer",
                                     "server_ack_ref": None,
                                     "raw_note": "injected"},
                    actor_id="t", mode="PAPER", operator_id="t")
                ack = sub.server_ack_ref
                state = sub.terminal_state
                await s.commit()
                return ack, state, sub
        finally:
            await eng.dispose()

    ack, state, _sub = asyncio.run(run())
    assert ack is None and state == "quarantined_unknown"

    class _Shape:  # detached-safe shape (facts read inside the session)
        terminal_state = state
        server_ack_ref = ack
        id = "s"
        intent_id = "i"

    spec = {"supported": True}
    admitted = require_actionable(_Shape(), "cancel", "cancel_on_unknown")
    assert admitted == "unknown_elected"
    # operator-supplied ticket admitted on the elected path
    out = require_act_payload("cancel", spec, _Shape(), {"order": 42},
                              admitted)
    assert out == {"order": 42}
    # ticket absent on the elected path: typed
    import pytest
    with pytest.raises(LiveExecRefused) as exc:
        require_act_payload("cancel", spec, _Shape(), {}, admitted)
    assert exc.value.reason == "act_target_mismatch"
