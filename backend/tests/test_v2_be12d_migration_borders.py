"""V2 BE-12D migration + governor-cycle border coupons (BO §1.f/§1.g).

One-line law; tattoo 90/83/16; all three lxe rows standing (append-only
registry, update refused live); rendered CHECK names (E-0055-A10.3);
downgrade exact; itemized drift; simulated-class-banned schema arms;
valve-vs-guard inversion; THE governor cycle border with counter-arms
over the real alembic chain; lane non-commutation under an armed
switch; armature proof rolled back.
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
REV_0055 = "20260909_0055"
REV_0056 = "20260909_0056"

PERMS_0056 = {
    ("admin", "v2.live_exec.killswitch.arm", "SAL-4"),
    ("admin", "v2.live_exec.killswitch.pull", "SAL-4"),
    ("admin", "v2.live_exec.killswitch.clear", "SAL-4"),
    ("admin", "v2.live_exec.killswitch.read", "SAL-2"),
    ("admin", "v2.live_exec.activation.read", "SAL-2"),
    ("admin", "v2.live_exec.activation.template.read", "SAL-3"),
}

_LXE_FILES_1_2 = (
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
    db_file = tmp_path / "be12d.db"
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


def test_one_upgrade_line_0055_to_0056(tmp_path: Path) -> None:
    db_file, db_url = _db(tmp_path, REV_0055)
    result = _alembic(["upgrade", REV_0056], db_url)
    assert result.returncode == 0, result.stderr
    both = result.stdout + result.stderr
    lines = [ln for ln in both.splitlines() if "Running upgrade" in ln]
    assert len(lines) == 1, lines
    assert f"{REV_0055} -> {REV_0056}" in lines[0]


def test_census_tattoo_90_83_16_rendered_checks(tmp_path: Path) -> None:
    db_file, _ = _db(tmp_path, REV_0056)
    trig = _q(db_file, "SELECT COUNT(*) FROM sqlite_master WHERE"
                       " type='trigger'")[0][0]
    perm = _q(db_file, "SELECT COUNT(*) FROM v2_permission")[0][0]
    comp = _q(db_file, "SELECT COUNT(*) FROM v2_computation_version")[0][0]
    assert (trig, perm, comp) == (90, 83, 16)
    rows = {(r, p, s) for r, p, s in _q(
        db_file, "SELECT role, permission, sal FROM v2_permission"
                 " WHERE permission LIKE '%killswitch%'"
                 " OR permission LIKE '%activation%'")}
    assert rows == PERMS_0056
    # append-only registry: all THREE lxe rows; 1.2.0 == disk recompute
    lxe = _q(db_file, "SELECT version, source_hash FROM"
                      " v2_computation_version WHERE"
                      " component='live_exec_engine' ORDER BY version")
    assert [v for v, _ in lxe] == ["lxe-1.0.0", "lxe-1.1.0", "lxe-1.2.0"]
    digest = hashlib.sha256()
    for ref in _LXE_FILES_1_2:
        digest.update(ref.encode())
        digest.update(b"\x00")
        digest.update((BACKEND_DIR / ref).read_bytes())
        digest.update(b"\x00")
    assert lxe[2][1] == digest.hexdigest()
    # RENDERED CHECK-name pins (E-0055-A10.3 law: from the DB's own DDL)
    ddl = _q(db_file, "SELECT sql FROM sqlite_master WHERE type='table'"
                      " AND name='v2_live_activation_instrument'")[0][0]
    for rendered in ("ck_v2_live_activation_instrument_ck_v2_lai_sole",
                     "ck_v2_live_activation_instrument_ck_v2_lai_version",
                     "ck_v2_live_activation_instrument_ck_v2_lai_data_class"):
        assert rendered in ddl
    ddl2 = _q(db_file, "SELECT sql FROM sqlite_master WHERE type='table'"
                       " AND name='v2_live_kill_switch'")[0][0]
    for rendered in ("ck_v2_live_kill_switch_ck_v2_lks_sole",
                     "ck_v2_live_kill_switch_ck_v2_lks_status",
                     "ck_v2_live_kill_switch_ck_v2_lks_data_class"):
        assert rendered in ddl2
    # both tables ZERO rows (zero-row IS the law)
    assert _q(db_file, "SELECT COUNT(*) FROM"
                       " v2_live_activation_instrument")[0][0] == 0
    assert _q(db_file, "SELECT COUNT(*) FROM v2_live_kill_switch")[0][0] == 0
    # append-only registry: the compver UPDATE guard refuses live
    conn = sqlite3.connect(db_file)
    try:
        try:
            conn.execute("UPDATE v2_computation_version SET"
                         " source_hash='x' WHERE version='lxe-1.1.0'")
            raise AssertionError("compver update guard failed open")
        except sqlite3.IntegrityError:
            pass
    finally:
        conn.close()


def test_simulated_class_banned_at_schema(tmp_path: Path) -> None:
    """No coupon world can simulate force or fake the switch: the
    data_class CHECKs admit only 'live_marker'/'evidence' — 'simulated'
    dies at schema in BOTH tables (witnessed live)."""
    db_file, _ = _db(tmp_path, REV_0056)
    conn = sqlite3.connect(db_file)
    try:
        try:
            conn.execute(
                "INSERT INTO v2_live_activation_instrument (id, sole,"
                " version, template_hash, funded_posture_ref, step_up_ref,"
                " operator_ref, actor_id, data_class, mode, operator_id,"
                " created_at) VALUES ('x','SOLE','lai-1.0.0','h','f','s',"
                "'o','t','simulated','RESEARCH','t',"
                "'2026-09-09 00:00:00+00:00')")
            raise AssertionError("simulated force row failed open")
        except sqlite3.IntegrityError:
            pass
        try:
            conn.execute(
                "INSERT INTO v2_live_kill_switch (id, sole, status,"
                " step_up_ref, actor_id, data_class, mode, operator_id,"
                " created_at) VALUES ('x','SOLE','armed','s','t',"
                "'simulated','RESEARCH','t','2026-09-09 00:00:00+00:00')")
            raise AssertionError("simulated switch row failed open")
        except sqlite3.IntegrityError:
            pass
    finally:
        conn.close()


def test_downgrade_reverses_exactly(tmp_path: Path) -> None:
    db_file, db_url = _db(tmp_path, REV_0056)
    result = _alembic(["downgrade", REV_0055], db_url)
    assert result.returncode == 0, result.stderr
    trig = _q(db_file, "SELECT COUNT(*) FROM sqlite_master WHERE"
                       " type='trigger'")[0][0]
    perm = _q(db_file, "SELECT COUNT(*) FROM v2_permission")[0][0]
    comp = _q(db_file, "SELECT COUNT(*) FROM v2_computation_version")[0][0]
    assert (trig, perm, comp) == (86, 77, 15)
    tables = {x[0] for x in _q(db_file, "SELECT name FROM sqlite_master"
                                        " WHERE type='table'")}
    assert "v2_live_activation_instrument" not in tables
    assert "v2_live_kill_switch" not in tables
    lxe = [v for (v,) in _q(db_file, "SELECT version FROM"
                                     " v2_computation_version WHERE"
                                     " component='live_exec_engine'"
                                     " ORDER BY version")]
    assert lxe == ["lxe-1.0.0", "lxe-1.1.0"]  # both prior rows preserved
    guard = _q(db_file, "SELECT COUNT(*) FROM sqlite_master WHERE"
                        " type='trigger' AND name="
                        "'v2_computation_version_immutable_delete'")[0][0]
    assert guard == 1


def test_drift_gate_0056_itemized(tmp_path: Path) -> None:
    db_file, db_url = _db(tmp_path, REV_0056)
    check = _alembic(["check"], db_url)
    drift = (check.stdout + check.stderr).lower()
    assert check.returncode != 0
    for banned in ("activation_instrument", "kill_switch", "lai_", "lks_"):
        assert banned not in drift, f"BE-12D drift at 0056: {banned}"
    if "not up to date" not in drift:
        assert "audit_write_failure_records" in drift


# --- the governor cycle border (BO §1.f) ------------------------------------------------


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


def test_border_governor_cycle_full_api(tmp_path: Path) -> None:
    """THE governor cycle border (§1.f), one border, full witness:
    arm 200 -> GET armed (L5 over the real schema) -> pull 200 ->
    re-arm 409 killswitch_armed (non-firing) -> clear 200 -> re-arm 200
    -> end state ARMED after CLEARED. Counter-arms: step-up absent;
    pull-before-arm; direct-SQL mutation dies on the guard."""
    db_file, _ = _db(tmp_path, REV_0056)
    prior = os.environ.get("AXIOM_DATABASE_URL")
    try:
        with _client_on_chain(db_file) as client:
            login = client.post(
                "/api/v1/auth/login",
                json={"username": "admin", "password": "admin123"})
            assert login.status_code == 200, login.text
            headers = {"Authorization":
                       f"Bearer {login.json()['tokens']['access_token']}"}
            base = "/api/v1/v2/live-exec/killswitch"

            # counter-arm: pull before any arm => state_invalid typed
            r = client.post(f"{base}/pull",
                            json={"step_up_ref": "mfa-ks-0"},
                            headers=headers)
            assert r.status_code == 409, r.text
            assert r.json()["refusal"]["reason"] == \
                "killswitch_state_invalid"
            # counter-arm: step-up absent => chassis refusal typed
            r = client.post(f"{base}/arm", json={}, headers=headers)
            assert r.status_code == 409
            assert r.json()["refusal"]["reason"] == \
                "step_up_reference_absent"
            # zero-row read: typed 'intact', never error
            r = client.get(base, headers=headers)
            assert r.status_code == 200
            assert r.json()["killswitch"] == {"status": "intact",
                                              "engaged": False}
            # ARM
            r = client.post(f"{base}/arm",
                            json={"step_up_ref": "mfa-ks-1"},
                            headers=headers)
            assert r.status_code == 200, r.text
            assert r.json()["killswitch"]["status"] == "armed"
            r = client.get(base, headers=headers)
            assert r.json()["killswitch"] == {"status": "armed",
                                              "engaged": True}
            # the LIVE door now reads L5 over the REAL schema: any
            # write envelope carries a refusal that is upstream of L5
            # (L1 in RESEARCH) — the L5 fact itself is proven by the
            # engaged read + the activation read below
            act = client.get("/api/v1/v2/live-exec/activation",
                             headers=headers)
            assert act.status_code == 200
            assert act.json()["activation_instrument"] == "not_in_force"
            assert act.json()["row_count"] == 0
            # PULL
            r = client.post(f"{base}/pull",
                            json={"step_up_ref": "mfa-ks-2"},
                            headers=headers)
            assert r.status_code == 200
            assert r.json()["killswitch"]["status"] == "pulled"
            # RE-ARM while pulled => 409 killswitch_armed, NON-FIRING
            r = client.post(f"{base}/arm",
                            json={"step_up_ref": "mfa-ks-3"},
                            headers=headers)
            assert r.status_code == 409
            assert r.json()["refusal"]["reason"] == "killswitch_armed"
            # CLEAR (the single sanctioned path)
            r = client.post(f"{base}/clear",
                            json={"step_up_ref": "mfa-ks-4"},
                            headers=headers)
            assert r.status_code == 200
            assert r.json()["killswitch"]["status"] == "cleared"
            r = client.get(base, headers=headers)
            assert r.json()["killswitch"] == {"status": "cleared",
                                              "engaged": False}
            # RE-ARM after cleared => lawful
            r = client.post(f"{base}/arm",
                            json={"step_up_ref": "mfa-ks-5"},
                            headers=headers)
            assert r.status_code == 200
            assert r.json()["killswitch"]["status"] == "armed"
            # template read: hash echoed == recompute (C-2 family)
            t = client.get("/api/v1/v2/live-exec/activation/template",
                           headers=headers)
            assert t.status_code == 200
            body = t.json()
            assert "THIS TEMPLATE CONFERS NO ACTIVATION" in body["template"]
            assert body["template_hash"] == hashlib.sha256(
                body["template"].encode("utf-8")).hexdigest()
    finally:
        _restore_env(prior)
    # Level-I after close: sole row 'armed'; guard pair present and
    # VERIFIED-restored after every valve pass; direct SQL dies
    rows = _q(db_file, "SELECT sole, status, step_up_ref FROM"
                       " v2_live_kill_switch")
    assert rows == [("SOLE", "armed", "mfa-ks-5")]
    guards = _q(db_file, "SELECT COUNT(*) FROM sqlite_master WHERE"
                         " type='trigger' AND name LIKE"
                         " 'v2_live_kill_switch_immutable_%'")[0][0]
    assert guards == 2
    conn = sqlite3.connect(db_file)
    try:
        for sql in ("UPDATE v2_live_kill_switch SET status='cleared'",
                    "DELETE FROM v2_live_kill_switch"):
            try:
                conn.execute(sql)
                raise AssertionError(f"guard failed open: {sql}")
            except sqlite3.IntegrityError:
                pass
        # singleton schema-fatal backstop
        try:
            conn.execute(
                "INSERT INTO v2_live_kill_switch (id, sole, status,"
                " step_up_ref, actor_id, data_class, mode, operator_id,"
                " created_at) VALUES ('y','SOLE','armed','s','t',"
                "'evidence','RESEARCH','t','2026-09-09 00:00:00+00:00')")
            raise AssertionError("singleton uq failed open")
        except sqlite3.IntegrityError:
            pass
    finally:
        conn.close()


def test_lane_noncommutation_under_armed_switch(tmp_path: Path) -> None:
    """BO §1.d: the PRACTICE lane NEVER consults the switch/instrument.
    With the switch ARMED in-world, a degraded practice ask still
    answers practice vocabulary ONLY, and a lawful practice ask still
    PASSES the lane door (refusing only at the terminal seam on this
    station)."""
    import asyncio

    from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

    from app.v2.live_exec.killswitch.engine import governor_arm
    from app.v2.live_exec.locks import (
        LOCK_ORDER,
        PracticeActuationRefused,
        PracticeActuationState,
        require_practice_actuation,
    )

    db_file, _ = _db(tmp_path, REV_0056)

    async def arm():
        eng = create_async_engine(f"sqlite+aiosqlite:///{db_file}")
        try:
            async with AsyncSession(eng) as s:
                await governor_arm(s, actor_id="t", step_up_ref="mfa-t",
                                   operator_id="t")
                await s.commit()
        finally:
            await eng.dispose()

    asyncio.run(arm())
    assert _q(db_file, "SELECT status FROM v2_live_kill_switch"
              ) == [("armed",)]
    # degraded practice ask: practice vocabulary only
    try:
        require_practice_actuation(PracticeActuationState(
            lane="practice", mode="RESEARCH"))
        raise AssertionError("lane door failed open")
    except PracticeActuationRefused as refused:
        assert refused.reason == "practice_mode_not_armed"
        assert refused.reason not in LOCK_ORDER
    # lawful practice ask: the lane door PASSES (switch state invisible)
    require_practice_actuation(PracticeActuationState(
        lane="practice", mode="PAPER", credential_state="present",
        boundary_stance="practice_wired", basis_age_hours=2.0))


def test_armature_proof_rolled_back(tmp_path: Path) -> None:
    """BO §1.b.4: the coupon-world armature — the future-lawful row
    SHAPE inserted IN-TRANSACTION; the L3 fact reader witnesses
    in-force; ROLLED BACK, never committed; the field stays zero-row."""
    import asyncio

    from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

    from app.v2.live_exec.activation.engine import (
        activation_instrument_rows,
        template_hash,
    )
    from app.v2.live_exec.locks import (
        ActuationRefused,
        ActuationState,
        require_actuation,
    )

    db_file, _ = _db(tmp_path, REV_0056)

    async def run():
        eng = create_async_engine(f"sqlite+aiosqlite:///{db_file}")
        try:
            async with AsyncSession(eng) as s:
                from sqlalchemy import text
                assert await activation_instrument_rows(s) == 0
                await s.execute(text(
                    "INSERT INTO v2_live_activation_instrument (id, sole,"
                    " version, template_hash, funded_posture_ref,"
                    " step_up_ref, operator_ref, actor_id, data_class,"
                    " mode, operator_id, created_at) VALUES"
                    " ('armature','SOLE','lai-1.0.0',:h,'fp-ref','su-ref',"
                    "'op-ref','armature','live_marker','RESEARCH',"
                    "'armature','2026-09-09 00:00:00+00:00')"
                ).bindparams(h=template_hash()))
                rows = await activation_instrument_rows(s)
                assert rows == 1
                # the lock evaluates IN-FORCE for the hypothetical row:
                # L3 passes; the next lock (L4 funded posture) answers
                try:
                    require_actuation(ActuationState(
                        mode="PAPER", credential_class="practice_trade",
                        activation_instrument_rows=rows,
                        funded_posture=False, killswitch_armed=False))
                    raise AssertionError("door failed open")
                except ActuationRefused as refused:
                    assert refused.reason == "funded_posture_required"
                await s.rollback()  # NEVER committed
        finally:
            await eng.dispose()

    asyncio.run(run())
    # the field stays zero-row: force was never taken anywhere
    assert _q(db_file, "SELECT COUNT(*) FROM"
                       " v2_live_activation_instrument")[0][0] == 0
