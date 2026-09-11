"""V2 BE-12E migration + border coupons (BO §1.c/§1.d/§1.f.2/§1.g).

One-line law; tattoo 94/88/17; all four lxe rows (last names the last
build); rendered CHECK names; downgrade exact; itemized drift;
C-2 clean-runs-evidenced BOTH arms over the real chain; the incident
cycle border with counter-arms; reconcile border; mode = REQUEST WORLD
forward law; guards + no-valve law on reconciliation.
"""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
TRANS_AUTHORITY = "BO-V2-BE-3-P2-TRANS-001"
REV_0056 = "20260909_0056"
REV_0057 = "20260909_0057"

PERMS_0057 = {
    ("admin", "v2.live_exec.reconcile.run", "SAL-4"),
    ("admin", "v2.live_exec.reconcile.read", "SAL-2"),
    ("admin", "v2.live_exec.incident.open", "SAL-4"),
    ("admin", "v2.live_exec.incident.close", "SAL-4"),
    ("admin", "v2.live_exec.incident.read", "SAL-2"),
}

_LXE_FILES_1_3 = (
    "app/v2/live_exec/intents.py",
    "app/v2/live_exec/eligibility.py",
    "app/v2/live_exec/risk.py",
    "app/v2/live_exec/locks.py",
    "app/v2/live_exec/submissions.py",
    "app/v2/live_exec/ack_fills.py",
    "app/v2/live_exec/modify/__init__.py",
    "app/v2/live_exec/modify/engine.py",
    "app/v2/live_exec/activation/__init__.py",
    "app/v2/live_exec/activation/engine.py",
    "app/v2/live_exec/activation/template.py",
    "app/v2/live_exec/killswitch/__init__.py",
    "app/v2/live_exec/killswitch/engine.py",
    "app/v2/live_exec/reconcile/__init__.py",
    "app/v2/live_exec/reconcile/money.py",
    "app/v2/live_exec/reconcile/engine.py",
    "app/v2/live_exec/incident/__init__.py",
    "app/v2/live_exec/incident/engine.py",
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
    db_file = tmp_path / "be12e.db"
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


def test_one_upgrade_line_0056_to_0057(tmp_path: Path) -> None:
    db_file, db_url = _db(tmp_path, REV_0056)
    result = _alembic(["upgrade", REV_0057], db_url)
    assert result.returncode == 0, result.stderr
    both = result.stdout + result.stderr
    lines = [ln for ln in both.splitlines() if "Running upgrade" in ln]
    assert len(lines) == 1, lines
    assert f"{REV_0056} -> {REV_0057}" in lines[0]


def test_census_tattoo_94_88_17_and_registry(tmp_path: Path) -> None:
    db_file, _ = _db(tmp_path, REV_0057)
    trig = _q(db_file, "SELECT COUNT(*) FROM sqlite_master WHERE"
                       " type='trigger'")[0][0]
    perm = _q(db_file, "SELECT COUNT(*) FROM v2_permission")[0][0]
    comp = _q(db_file, "SELECT COUNT(*) FROM v2_computation_version")[0][0]
    assert (trig, perm, comp) == (94, 88, 17)
    rows = {(r, p, s) for r, p, s in _q(
        db_file, "SELECT role, permission, sal FROM v2_permission"
                 " WHERE permission LIKE '%reconcile%'"
                 " OR permission LIKE '%incident%'")}
    assert rows == PERMS_0057
    # append-only registry: all FOUR rows; the LAST names the LAST build
    lxe = _q(db_file, "SELECT version, source_hash, evidence_ref FROM"
                      " v2_computation_version WHERE"
                      " component='live_exec_engine' ORDER BY version")
    assert [v for v, _, _ in lxe] == ["lxe-1.0.0", "lxe-1.1.0",
                                      "lxe-1.2.0", "lxe-1.3.0"]
    assert lxe[3][2] == "BO-V2-BE12E-001"  # the carry item closes here
    digest = hashlib.sha256()
    for ref in _LXE_FILES_1_3:
        digest.update(ref.encode())
        digest.update(b"\x00")
        digest.update((BACKEND_DIR / ref).read_bytes())
        digest.update(b"\x00")
    assert lxe[3][1] == digest.hexdigest()
    # rendered CHECK names (E-0055-A10.3, from the DB's own DDL)
    ddl = _q(db_file, "SELECT sql FROM sqlite_master WHERE type='table'"
                      " AND name='v2_live_exec_reconciliation'")[0][0]
    for rendered in ("ck_v2_live_exec_reconciliation_ck_v2_lxrecon_outcome",
                     "ck_v2_live_exec_reconciliation_ck_v2_lxrecon_data_class"):
        assert rendered in ddl
    ddl2 = _q(db_file, "SELECT sql FROM sqlite_master WHERE type='table'"
                       " AND name='v2_live_exec_incident'")[0][0]
    for rendered in ("ck_v2_live_exec_incident_ck_v2_lxinc_severity",
                     "ck_v2_live_exec_incident_ck_v2_lxinc_status",
                     "ck_v2_live_exec_incident_ck_v2_lxinc_data_class"):
        assert rendered in ddl2
    # both ledgers born empty
    assert _q(db_file, "SELECT COUNT(*) FROM"
                       " v2_live_exec_reconciliation")[0][0] == 0
    assert _q(db_file, "SELECT COUNT(*) FROM v2_live_exec_incident")[0][0] == 0


def test_downgrade_reverses_exactly(tmp_path: Path) -> None:
    db_file, db_url = _db(tmp_path, REV_0057)
    result = _alembic(["downgrade", REV_0056], db_url)
    assert result.returncode == 0, result.stderr
    trig = _q(db_file, "SELECT COUNT(*) FROM sqlite_master WHERE"
                       " type='trigger'")[0][0]
    perm = _q(db_file, "SELECT COUNT(*) FROM v2_permission")[0][0]
    comp = _q(db_file, "SELECT COUNT(*) FROM v2_computation_version")[0][0]
    assert (trig, perm, comp) == (90, 83, 16)
    lxe = [v for (v,) in _q(db_file, "SELECT version FROM"
                                     " v2_computation_version WHERE"
                                     " component='live_exec_engine'"
                                     " ORDER BY version")]
    assert lxe == ["lxe-1.0.0", "lxe-1.1.0", "lxe-1.2.0"]


def test_drift_gate_0057_itemized(tmp_path: Path) -> None:
    db_file, db_url = _db(tmp_path, REV_0057)
    check = _alembic(["check"], db_url)
    drift = (check.stdout + check.stderr).lower()
    assert check.returncode != 0
    for banned in ("reconciliation", "lxrecon", "lxinc", "incident"):
        assert banned not in drift, f"BE-12E drift at 0057: {banned}"
    if "not up to date" not in drift:
        assert "audit_write_failure_records" in drift


# --- borders (§1.f.2) over the real chain ---------------------------------------------


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


def test_border_reconcile_c2_both_arms(tmp_path: Path) -> None:
    """C-2 clean-runs-evidenced, BOTH arms over the real chain:
    empty-ledger world => run 200 writes EXACTLY ONE row, outcome
    clean, drift_facts NULL; seeded-drift world (orphan fill) =>
    exactly one MORE row, parity_break, drift facts serialized. Mode
    stamp == REQUEST WORLD (§a.4 forward law). Latest reflects. NO
    VALVE: UPDATE/DELETE die on the guards."""
    db_file, _ = _db(tmp_path, REV_0057)
    prior = os.environ.get("AXIOM_DATABASE_URL")
    try:
        with _client_on_chain(db_file) as client:
            login = client.post(
                "/api/v1/auth/login",
                json={"username": "admin", "password": "admin123"})
            assert login.status_code == 200, login.text
            headers = {"Authorization":
                       f"Bearer {login.json()['tokens']['access_token']}"}
            base = "/api/v1/v2/live-exec/reconcile"
            # zero-row GET shape typed
            r = client.get(f"{base}/latest", headers=headers)
            assert r.status_code == 200
            assert r.json()["reconciliation"] == "no_runs_recorded"
            # CR-1 rider (DEL-002): the lookup idiom's 404 arm —
            # unknown id answers the enrolled wire literal, typed
            r = client.get(f"{base}/no-such-id", headers=headers)
            assert r.status_code == 404
            assert r.json()["refusal"]["reason"] == \
                "reconciliation_not_found"
            # ARM 1: clean world
            r = client.post(f"{base}/run", headers=headers)
            assert r.status_code == 200, r.text
            body = r.json()["reconciliation"]
            assert body["outcome"] == "clean"
            assert body["drift_facts"] is None
            assert body["mode"] == "RESEARCH"  # the REQUEST world
            first_id = body["id"]
            r = client.get(f"{base}/latest", headers=headers)
            assert r.json()["reconciliation"]["id"] == first_id
            # digest recompute over the real chain (R-3.1)
            row = _q(db_file, "SELECT scope, outcome, drift_facts,"
                              " actor_id, mode, operator_id, digest FROM"
                              " v2_live_exec_reconciliation WHERE id = ?",
                     (first_id,))[0]
            facts = {"scope": json.loads(row[0]), "outcome": row[1],
                     "drift_facts": (json.loads(row[2]) if row[2]
                                     else None),
                     "actor_id": row[3], "mode": row[4],
                     "operator_id": row[5]}
            recomputed = hashlib.sha256(json.dumps(
                facts, sort_keys=True, separators=(",", ":"),
                default=str).encode()).hexdigest()
            assert recomputed == row[6]
    finally:
        _restore_env(prior)
    # exactly ONE row after the clean run (C-2 arm 1)
    assert _q(db_file, "SELECT COUNT(*) FROM"
                       " v2_live_exec_reconciliation")[0][0] == 1

    # ARM 2: seed a drift world (orphan fill event, engine-level)
    import asyncio

    from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

    from app.v2.live_exec.reconcile.engine import run_reconciliation

    async def seed_and_run():
        eng = create_async_engine(f"sqlite+aiosqlite:///{db_file}")
        try:
            async with AsyncSession(eng) as s:
                from sqlalchemy import text
                await s.execute(text(
                    "INSERT INTO v2_live_exec_fill_event (id,"
                    " submission_id, fill_event_identity,"
                    " correlation_basis, correlation_ref, fill_payload,"
                    " actor_id, data_class, mode, operator_id,"
                    " created_at) VALUES ('orphan-1', 'no-such-sub',"
                    " 'fid-1', 'server_ack_ref', 'ack-x',"
                    " '{\"deal_id\": \"D9\", \"price\": \"1.10\"}',"
                    " 't', 'simulated', 'PAPER', 't',"
                    " '2026-09-09 00:00:00+00:00')"))
                row = await run_reconciliation(
                    s, actor_id="t", mode="PAPER", operator_id="t")
                outcome = row.outcome
                kinds = sorted({f["kind"] for f in row.drift_facts})
                mode = row.mode
                await s.commit()
                return outcome, kinds, mode
        finally:
            await eng.dispose()

    outcome, kinds, mode = asyncio.run(seed_and_run())
    assert outcome == "parity_break"
    assert "fill_unprojected" in kinds and "ledger_orphan" in kinds
    assert mode == "PAPER"  # request world threaded, never a literal
    # exactly TWO rows total (one per run — C-2 arm 2)
    assert _q(db_file, "SELECT COUNT(*) FROM"
                       " v2_live_exec_reconciliation")[0][0] == 2
    # NO VALVE: guards fire on the report ledger
    conn = sqlite3.connect(db_file)
    try:
        for sql in ("UPDATE v2_live_exec_reconciliation SET"
                    " outcome='clean'",
                    "DELETE FROM v2_live_exec_reconciliation"):
            try:
                conn.execute(sql)
                raise AssertionError(f"guard failed open: {sql}")
            except sqlite3.IntegrityError:
                pass
    finally:
        conn.close()


def test_border_incident_cycle_with_counter_arms(tmp_path: Path) -> None:
    """The incident cycle border (§1.f.2): step-up absent on BOTH
    confirm verbs => sealed chassis refusal; empty instruments =>
    typed; open 200 => close 200 => re-close => already_closed;
    close-of-unknown => not_open; direct-SQL UPDATE => guard refusal;
    digest recomputed on open AND close over the real chain."""
    db_file, _ = _db(tmp_path, REV_0057)
    prior = os.environ.get("AXIOM_DATABASE_URL")
    try:
        with _client_on_chain(db_file) as client:
            login = client.post(
                "/api/v1/auth/login",
                json={"username": "admin", "password": "admin123"})
            assert login.status_code == 200, login.text
            headers = {"Authorization":
                       f"Bearer {login.json()['tokens']['access_token']}"}
            base = "/api/v1/v2/live-exec/incident"
            # counter-arm: step-up absent on OPEN
            r = client.post(f"{base}/open", headers=headers,
                            json={"severity": "SEV-2",
                                  "instruments_pinned": ["forex.eurusd"],
                                  "recovery_path": "manual review"})
            assert r.status_code == 409
            assert r.json()["refusal"]["reason"] == \
                "step_up_reference_absent"
            # counter-arm: empty instruments => typed
            r = client.post(f"{base}/open", headers=headers,
                            json={"severity": "SEV-2",
                                  "instruments_pinned": [],
                                  "recovery_path": "manual review",
                                  "step_up_ref": "mfa-i-0"})
            assert r.status_code == 409
            assert r.json()["refusal"]["reason"] == \
                "incident_instruments_absent"
            # counter-arm: close-of-unknown => not_open
            r = client.post(f"{base}/no-such/close", headers=headers,
                            json={"step_up_ref": "mfa-i-1"})
            assert r.status_code == 409
            assert r.json()["refusal"]["reason"] == "incident_not_open"
            # CR-1 counter-arm (DEL-001): invalid severity => 422 with
            # the reason read from the ENGINE CONSTANT (never a wire
            # literal) — the closed vocabulary IS the wire
            from app.v2.live_exec.incident.engine import (
                INCIDENT_SEVERITY_INVALID,
            )
            r = client.post(f"{base}/open", headers=headers,
                            json={"severity": "SEV-9",
                                  "instruments_pinned": ["forex.eurusd"],
                                  "recovery_path": "manual review",
                                  "step_up_ref": "mfa-i-1b"})
            assert r.status_code == 422, r.text
            assert r.json()["refusal"]["reason"] == \
                INCIDENT_SEVERITY_INVALID
            # OPEN
            r = client.post(f"{base}/open", headers=headers,
                            json={"severity": "SEV-2",
                                  "instruments_pinned": ["forex.eurusd"],
                                  "recovery_path": "manual review",
                                  "step_up_ref": "mfa-i-2"})
            assert r.status_code == 200, r.text
            incident = r.json()["incident"]
            incident_id = incident["id"]
            assert incident["status"] == "open"
            assert incident["mode"] == "RESEARCH"  # request world
            open_digest = incident["digest"]
            # counter-arm: step-up absent on CLOSE
            r = client.post(f"{base}/{incident_id}/close",
                            headers=headers, json={})
            assert r.status_code == 409
            assert r.json()["refusal"]["reason"] == \
                "step_up_reference_absent"
            # CLOSE (the single sanctioned path)
            r = client.post(f"{base}/{incident_id}/close",
                            headers=headers,
                            json={"step_up_ref": "mfa-i-3"})
            assert r.status_code == 200, r.text
            close_digest = r.json()["incident"]["digest"]
            assert close_digest != open_digest  # digest moved on close
            # RE-CLOSE => already_closed, non-firing
            r = client.post(f"{base}/{incident_id}/close",
                            headers=headers,
                            json={"step_up_ref": "mfa-i-4"})
            assert r.status_code == 409
            assert r.json()["refusal"]["reason"] == \
                "incident_already_closed"
            # reads
            r = client.get(f"{base}/{incident_id}", headers=headers)
            assert r.json()["incident"]["status"] == "closed"
            assert r.json()["incident"]["closed_by"] == "admin"
            r = client.get("/api/v1/v2/live-exec/incidents",
                           headers=headers)
            assert len(r.json()["incidents"]) == 1
    finally:
        _restore_env(prior)
    # Level-I: one row, closed, digest recompute on the close stamps
    rows = _q(db_file, "SELECT severity, instruments_pinned,"
                       " recovery_path, status, opened_by, closed_at,"
                       " closed_by, mode, digest FROM"
                       " v2_live_exec_incident")
    assert len(rows) == 1
    (severity, instruments, recovery, status, opened_by, closed_at,
     closed_by, mode, digest) = rows[0]
    assert status == "closed" and closed_by == "admin"
    # the engine digests the tz-aware str() of its own utc_now(); the
    # sqlite driver stores the naive text — re-derive the engine's
    # representation (facts as the WRITER held them, not as the driver
    # rendered them; the 12B/12C harness-law family)
    from datetime import datetime, timezone
    closed_at_engine = str(
        datetime.fromisoformat(closed_at).replace(tzinfo=timezone.utc))
    facts = {"severity": severity,
             "instruments_pinned": json.loads(instruments),
             "recovery_path": recovery, "status": status,
             "opened_by": opened_by, "closed_at": closed_at_engine,
             "closed_by": closed_by, "mode": mode}
    # digest recompute: the engine's canonical serialization
    recomputed = hashlib.sha256(json.dumps(
        facts, sort_keys=True, separators=(",", ":"),
        default=str).encode()).hexdigest()
    assert recomputed == digest
    # direct-SQL UPDATE dies (the valve untouched)
    conn = sqlite3.connect(db_file)
    try:
        try:
            conn.execute("UPDATE v2_live_exec_incident SET status='open'")
            raise AssertionError("incident guard failed open")
        except sqlite3.IntegrityError:
            pass
        # guard pair restored after the valve close
        guards = conn.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'"
            " AND name LIKE 'v2_live_exec_incident_immutable_%'"
        ).fetchone()[0]
        assert guards == 2
    finally:
        conn.close()
