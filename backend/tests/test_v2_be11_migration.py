"""V2 BE-11 migration coupons — L-10 (BO D-3/exit criteria).

Census tattoo (triggers 78, permissions 69, compver 13); EMPTY-FORCED
seed slots; guard messages verbatim; verdict-iff CHECK; reversible-exact
downgrade; drift gate."""

from __future__ import annotations

import os
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

BACKEND_DIR = Path(__file__).resolve().parents[1]
TRANS_AUTHORITY = "BO-V2-BE-3-P2-TRANS-001"
REV_0050 = "20260908_0050"
REV_0051 = "20260909_0051"

REGIME = "'simulated','PAPER','t',NULL,'2026-09-06 00:00:00+00:00'"

TRIGGERS_0051 = {
    "v2_paper_bridge_drift_run_immutable_update":
        "V2 paper bridge drift runs are immutable; UPDATE prohibited",
    "v2_paper_bridge_drift_run_immutable_delete":
        "V2 paper bridge drift runs are immutable; DELETE prohibited",
}

PERMS_0051 = {
    ("admin", "v2.paper_bridge.intent.write", "SAL-3"),
    ("admin", "v2.paper_bridge.evaluate.write", "SAL-3"),
    ("admin", "v2.paper_bridge.ledger.read", "SAL-2"),
    ("admin", "v2.paper_bridge.drift.read", "SAL-2"),
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
    db_file = tmp_path / "be11.db"
    db_url = f"sqlite+aiosqlite:///{db_file}"
    result = _alembic(["upgrade", rev], db_url)
    assert result.returncode == 0, result.stderr
    return db_file, db_url


def _q(db_file: Path, sql: str):
    conn = sqlite3.connect(db_file)
    try:
        return conn.execute(sql).fetchall()
    finally:
        conn.close()


def test_l10_census_tattoo_and_empty_forced(tmp_path: Path) -> None:
    db_file, _ = _db(tmp_path, REV_0051)
    trig = _q(db_file, "SELECT COUNT(*) FROM sqlite_master WHERE"
                       " type='trigger' AND name LIKE 'v2_%'")[0][0]
    perm = _q(db_file, "SELECT COUNT(*) FROM v2_permission")[0][0]
    comp = _q(db_file, "SELECT COUNT(*) FROM v2_computation_version")[0][0]
    rows = _q(db_file, "SELECT COUNT(*) FROM v2_paper_bridge_drift_run")[0][0]
    assert (trig, perm, comp) == (78, 69, 13)  # exit criteria exactly
    assert rows == 0  # EMPTY-FORCED is the shipped state
    assert PERMS_0051 <= {tuple(r) for r in _q(
        db_file, "SELECT role, permission, sal FROM v2_permission")}
    pbr = _q(db_file, "SELECT component, version, LENGTH(source_hash)"
                      " FROM v2_computation_version"
                      " WHERE component='paper_bridge_engine'")
    assert pbr == [("paper_bridge_engine", "pbr-1.0.0", 64)]


def test_l10_guard_messages_verbatim_and_checks(tmp_path: Path) -> None:
    db_file, _ = _db(tmp_path, REV_0051)
    conn = sqlite3.connect(db_file)
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO v2_paper_bridge_drift_run (id, run_kind,"
            " basis_sync_run_id, paper_side, broker_side,"
            " tolerances_in_force, verdict, digest, seed_name, payload,"
            " actor_id, data_class, mode, operator_id, correlation_id,"
            " created_at)"
            f" VALUES ('d1','drift_run','s1','{{}}','{{}}','{{}}',"
            f" 'within_tolerance','h',NULL,NULL,'t',{REGIME})")
        conn.commit()
        with pytest.raises(sqlite3.IntegrityError) as e_up:
            cur.execute("UPDATE v2_paper_bridge_drift_run"
                        " SET operator_id='x' WHERE id='d1'")
        assert TRIGGERS_0051[
            "v2_paper_bridge_drift_run_immutable_update"] in str(e_up.value)
        with pytest.raises(sqlite3.IntegrityError) as e_del:
            cur.execute("DELETE FROM v2_paper_bridge_drift_run"
                        " WHERE id='d1'")
        assert TRIGGERS_0051[
            "v2_paper_bridge_drift_run_immutable_delete"] in str(e_del.value)
        # verdict-iff CHECK both directions
        with pytest.raises(sqlite3.IntegrityError):
            cur.execute(  # drift_run WITHOUT verdict
                "INSERT INTO v2_paper_bridge_drift_run (id, run_kind,"
                " verdict, seed_name, payload, actor_id, data_class,"
                " mode, operator_id, correlation_id, created_at)"
                f" VALUES ('d2','drift_run',NULL,NULL,NULL,'t',{REGIME})")
        with pytest.raises(sqlite3.IntegrityError):
            cur.execute(  # seed WITH verdict
                "INSERT INTO v2_paper_bridge_drift_run (id, run_kind,"
                " verdict, seed_name, payload, actor_id, data_class,"
                " mode, operator_id, correlation_id, created_at)"
                f" VALUES ('d3','seed','drift_minor','x','{{}}','t',{REGIME})")
        with pytest.raises(sqlite3.IntegrityError):
            cur.execute(  # invented run_kind
                "INSERT INTO v2_paper_bridge_drift_run (id, run_kind,"
                " verdict, seed_name, payload, actor_id, data_class,"
                " mode, operator_id, correlation_id, created_at)"
                f" VALUES ('d4','audit',NULL,NULL,NULL,'t',{REGIME})")
    finally:
        conn.close()


def test_l10_downgrade_reverses_exactly(tmp_path: Path) -> None:
    db_file, db_url = _db(tmp_path, REV_0050)
    pre_perms = sorted(_q(db_file, "SELECT role, permission FROM"
                                   " v2_permission"))
    pre_comp = sorted(_q(db_file, "SELECT component, version FROM"
                                  " v2_computation_version"))
    r = _alembic(["upgrade", REV_0051], db_url)
    assert r.returncode == 0, r.stderr
    r = _alembic(["downgrade", REV_0050], db_url)
    assert r.returncode == 0, r.stderr
    tables = {x[0] for x in _q(db_file, "SELECT name FROM sqlite_master"
                                        " WHERE type='table'")}
    assert "v2_paper_bridge_drift_run" not in tables
    assert sorted(_q(db_file, "SELECT role, permission FROM"
                              " v2_permission")) == pre_perms
    assert sorted(_q(db_file, "SELECT component, version FROM"
                              " v2_computation_version")) == pre_comp
    guard = _q(db_file, "SELECT COUNT(*) FROM sqlite_master WHERE"
                        " type='trigger' AND name="
                        "'v2_computation_version_immutable_delete'")
    assert guard[0][0] == 1


@pytest.mark.parametrize("rev", [REV_0050, REV_0051])
def test_drift_gate_0051(tmp_path: Path, rev: str) -> None:
    db_file, db_url = _db(tmp_path, rev)
    check = _alembic(["check"], db_url)
    drift = (check.stdout + check.stderr).lower()
    assert check.returncode != 0
    assert "paper_bridge" not in drift, f"BE-11 drift at {rev}"
    if "not up to date" not in drift:
        assert "audit_write_failure_records" in drift


def test_no_fill_sim_scaffolding_anywhere() -> None:
    """Exit criterion: fill-sim ABSENT, not dormant (non-revival law)."""
    bridge = BACKEND_DIR / "app/v2/paper_bridge"
    for f in bridge.rglob("*.py"):
        text = f.read_text().lower()
        for token in ("fill_sim", "simulate_fill", "run_simulation(",
                      "bar_replay", "fills ="):
            assert token not in text, f"{token} in {f.name}"
