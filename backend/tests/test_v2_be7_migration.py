"""V2 BE-7 migration tests — BO-V2-BE-7-001 T-1…T-7 (12 tests).

0047 on dedicated SQLite chains. Content-based comparisons (PGF-012).
Pins: triggers 32→42; permissions 41→49; compver 6→8.
"""

from __future__ import annotations

import os
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

BACKEND_DIR = Path(__file__).resolve().parents[1]
TRANS_AUTHORITY = "BO-V2-BE-3-P2-TRANS-001"
REV_0046 = "20260903_0046"
REV_0047 = "20260903_0047"

TRIGGERS_0047 = {
    "v2_backtest_input_immutable_update":
        "V2 backtest inputs are immutable; UPDATE prohibited",
    "v2_backtest_input_immutable_delete":
        "V2 backtest inputs are immutable; DELETE prohibited",
    "v2_cost_model_immutable_update":
        "V2 cost models are immutable; UPDATE prohibited",
    "v2_cost_model_immutable_delete":
        "V2 cost models are immutable; DELETE prohibited",
    "v2_strategy_version_immutable_update":
        "V2 strategy versions are immutable; UPDATE prohibited",
    "v2_strategy_version_immutable_delete":
        "V2 strategy versions are immutable; DELETE prohibited",
    "v2_research_job_attempt_immutable_update":
        "V2 research job attempts are immutable; UPDATE prohibited",
    "v2_research_job_attempt_immutable_delete":
        "V2 research job attempts are immutable; DELETE prohibited",
    "v2_research_result_immutable_update":
        "V2 research results are immutable; UPDATE prohibited",
    "v2_research_result_immutable_delete":
        "V2 research results are immutable; DELETE prohibited",
}

PERMS_0047 = {
    ("admin", "v2.research.jobs.read", "SAL-2"),
    ("admin", "v2.research.jobs.submit", "SAL-3"),
    ("admin", "v2.research.jobs.cancel", "SAL-3"),
    ("admin", "v2.research.registry.read", "SAL-2"),
    ("admin", "v2.research.registry.write", "SAL-3"),
    ("admin", "v2.research.results.read", "SAL-2"),
    ("operator", "v2.research.jobs.read", "SAL-2"),
    ("operator", "v2.research.results.read", "SAL-2"),
}


def _alembic(args: list[str], db_url: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["AXIOM_DATABASE_URL"] = db_url
    env.setdefault("AXIOM_ENVIRONMENT", "testing")
    env.setdefault("AXIOM_ALLOW_INSECURE_DEV", "true")
    env.setdefault("AXIOM_JWT_SECRET_KEY",
                   "test-secret-key-at-least-32-chars-long!!")
    env.setdefault("AXIOM_V2_MODE", "RESEARCH")
    env["AXIOM_TD_TRANSITION_AUTHORITY_REF"] = TRANS_AUTHORITY
    return subprocess.run(
        [sys.executable, "-m", "alembic", *args],
        cwd=BACKEND_DIR, env=env, capture_output=True, text=True, timeout=600)


def _db(tmp_path: Path, rev: str) -> tuple[Path, str]:
    db_file = tmp_path / "be7.db"
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


def _v2_triggers(db_file: Path) -> set[str]:
    return {r[0] for r in _q(
        db_file,
        "SELECT name FROM sqlite_master WHERE type='trigger'"
        " AND name LIKE 'v2_%'")}


BE1 = ("'simulated','RESEARCH','t',NULL,'2026-09-03 00:00:00+00:00'")


def _insert_input(cur, rid="i1", iid="in-1", seq=1, ch="h1"):
    cur.execute(
        "INSERT INTO v2_backtest_input (id, input_id, record_seq,"
        " content_hash, series_refs, window_start, window_end,"
        " registration_outcome, data_class, mode, operator_id,"
        " correlation_id, created_at)"
        f" VALUES ('{rid}','{iid}',{seq},'{ch}','{{}}',"
        " '2026-09-01 00:00:00+00:00','2026-09-02 00:00:00+00:00',"
        f" 'registered',{BE1})")


# --- T-1/T-2: chain + DDL (4 tests) -------------------------------------------


def test_0047_tables_and_columns(tmp_path: Path) -> None:
    db_file, _ = _db(tmp_path, REV_0047)
    tables = {r[0] for r in _q(
        db_file, "SELECT name FROM sqlite_master WHERE type='table'")}
    for t in ("v2_backtest_input", "v2_cost_model", "v2_strategy_version",
              "v2_research_job", "v2_research_job_attempt",
              "v2_research_result"):
        assert t in tables
    job_cols = [r[1] for r in _q(db_file, "PRAGMA table_info(v2_research_job)")]
    for c in ("owner", "authorization_ref", "inputs", "schedule",
              "output_ref", "failure", "job_state", "attempt_count"):
        assert c in job_cols
    result_cols = [r[1] for r in _q(
        db_file, "PRAGMA table_info(v2_research_result)")]
    for c in ("result_class", "inputs_hash", "engine_versions_hash",
              "summary", "replay_of", "time_basis"):
        assert c in result_cols


def test_0047_seeds_and_totals(tmp_path: Path) -> None:
    db_file, _ = _db(tmp_path, REV_0047)
    trigs = _v2_triggers(db_file)
    assert len(trigs) == 42          # T-3: 32 + 10
    assert set(TRIGGERS_0047) <= trigs
    perms = _q(db_file, "SELECT role, permission, sal FROM v2_permission")
    assert len(perms) == 49          # T-4
    assert len({(r, p) for r, p, _ in perms}) == 49
    assert PERMS_0047 <= {tuple(r) for r in perms}
    compver = _q(db_file,
                 "SELECT component, version, length(source_hash)"
                 " FROM v2_computation_version")
    assert len(compver) == 8         # T-5
    assert ("replay_engine", "rpe-1.0.0", 64) in compver
    assert ("research_job_engine", "rje-1.0.0", 64) in compver


def test_0047_result_class_check_refuses_paper_live(tmp_path: Path) -> None:
    """T-2/P-9: `paper`/`live` are schema-impossible."""
    db_file, _ = _db(tmp_path, REV_0047)
    conn = sqlite3.connect(db_file)
    try:
        for banned in ("paper", "live"):
            with pytest.raises(sqlite3.IntegrityError):
                conn.execute(
                    "INSERT INTO v2_research_result (id, result_class,"
                    " job_id, attempt_index, strategy_version_id,"
                    " input_registry_id, cost_model_id, inputs_hash,"
                    " engine_versions, engine_versions_hash, summary,"
                    " time_basis, data_class, mode, operator_id,"
                    " correlation_id, created_at)"
                    f" VALUES ('r-{banned}','{banned}','j',1,'s','i','c',"
                    f" 'h','{{}}','h2','{{}}','{{}}',{BE1})")
        # constructible classes insert fine
        conn.execute(
            "INSERT INTO v2_research_result (id, result_class, job_id,"
            " attempt_index, strategy_version_id, input_registry_id,"
            " cost_model_id, inputs_hash, engine_versions,"
            " engine_versions_hash, summary, time_basis, data_class,"
            " mode, operator_id, correlation_id, created_at)"
            f" VALUES ('r-ok','backtest','j',1,'s','i','c','h','{{}}','h2',"
            f" '{{}}','{{}}',{BE1})")
        conn.commit()
    finally:
        conn.close()


def test_0047_uniqueness_anchors_behavioral(tmp_path: Path) -> None:
    db_file, _ = _db(tmp_path, REV_0047)
    conn = sqlite3.connect(db_file)
    try:
        cur = conn.cursor()
        _insert_input(cur, rid="i1", iid="in-1", seq=1, ch="h1")
        conn.commit()
        with pytest.raises(sqlite3.IntegrityError):
            _insert_input(cur, rid="i2", iid="in-1", seq=1, ch="h2")  # dup seq
        with pytest.raises(sqlite3.IntegrityError):
            _insert_input(cur, rid="i3", iid="in-2", seq=1, ch="h1")  # dup content
        _insert_input(cur, rid="i4", iid="in-1", seq=2, ch="h3")      # next gen ok
        conn.commit()
        # attempt-ledger anchor
        cur.execute(
            "INSERT INTO v2_research_job_attempt (id, job_id,"
            " attempt_index, outcome, reason, actor_id, mode, operator_id,"
            " correlation_id, created_at)"
            " VALUES ('a1','j1',1,'failed','{}','t','RESEARCH','t',NULL,"
            " '2026-09-03 00:00:00+00:00')")
        conn.commit()
        with pytest.raises(sqlite3.IntegrityError):
            cur.execute(
                "INSERT INTO v2_research_job_attempt (id, job_id,"
                " attempt_index, outcome, reason, actor_id, mode,"
                " operator_id, correlation_id, created_at)"
                " VALUES ('a2','j1',1,'succeeded','{}','t','RESEARCH','t',"
                " NULL,'2026-09-03 00:00:00+00:00')")  # P-10 anchor
    finally:
        conn.close()


# --- T-3: guard messages verbatim (2 tests) --------------------------------------


def test_0047_guard_messages_verbatim_registries(tmp_path: Path) -> None:
    db_file, _ = _db(tmp_path, REV_0047)
    conn = sqlite3.connect(db_file)
    try:
        cur = conn.cursor()
        _insert_input(cur)
        cur.execute(
            "INSERT INTO v2_cost_model (id, cost_model_id, record_seq,"
            " spread, commission, slippage, latency_ms, risk_limits,"
            " citations, data_class, mode, operator_id, correlation_id,"
            " created_at)"
            f" VALUES ('c1','cm-1',1,'{{}}','{{}}','{{}}',0,'{{}}','{{}}',{BE1})")
        cur.execute(
            "INSERT INTO v2_strategy_version (id, strategy_id, record_seq,"
            " name, parameters, lifecycle_state, data_class, mode,"
            " operator_id, correlation_id, created_at)"
            f" VALUES ('s1','st-1',1,'S','{{}}','draft',{BE1})")
        conn.commit()
        for sql, trig in (
            ("UPDATE v2_backtest_input SET input_id='x'",
             "v2_backtest_input_immutable_update"),
            ("DELETE FROM v2_backtest_input",
             "v2_backtest_input_immutable_delete"),
            ("UPDATE v2_cost_model SET latency_ms=1",
             "v2_cost_model_immutable_update"),
            ("DELETE FROM v2_cost_model",
             "v2_cost_model_immutable_delete"),
            ("UPDATE v2_strategy_version SET name='x'",
             "v2_strategy_version_immutable_update"),
            ("DELETE FROM v2_strategy_version",
             "v2_strategy_version_immutable_delete"),
        ):
            with pytest.raises(sqlite3.DatabaseError) as excinfo:
                cur.execute(sql)
            assert str(excinfo.value) == TRIGGERS_0047[trig]
    finally:
        conn.close()


def test_0047_guard_messages_verbatim_ledger_results(tmp_path: Path) -> None:
    db_file, _ = _db(tmp_path, REV_0047)
    conn = sqlite3.connect(db_file)
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO v2_research_job_attempt (id, job_id, attempt_index,"
            " outcome, reason, actor_id, mode, operator_id, correlation_id,"
            " created_at)"
            " VALUES ('a1','j1',1,'succeeded','{}','t','RESEARCH','t',NULL,"
            " '2026-09-03 00:00:00+00:00')")
        cur.execute(
            "INSERT INTO v2_research_result (id, result_class, job_id,"
            " attempt_index, strategy_version_id, input_registry_id,"
            " cost_model_id, inputs_hash, engine_versions,"
            " engine_versions_hash, summary, time_basis, data_class, mode,"
            " operator_id, correlation_id, created_at)"
            f" VALUES ('r1','simulation','j1',1,'s','i','c','h','{{}}','h2',"
            f" '{{}}','{{}}',{BE1})")
        conn.commit()
        for sql, trig in (
            ("UPDATE v2_research_job_attempt SET outcome='failed'",
             "v2_research_job_attempt_immutable_update"),
            ("DELETE FROM v2_research_job_attempt",
             "v2_research_job_attempt_immutable_delete"),
            ("UPDATE v2_research_result SET result_class='backtest'",
             "v2_research_result_immutable_update"),
            ("DELETE FROM v2_research_result",
             "v2_research_result_immutable_delete"),
        ):
            with pytest.raises(sqlite3.DatabaseError) as excinfo:
                cur.execute(sql)
            assert str(excinfo.value) == TRIGGERS_0047[trig]
        # the job table is UNGUARDED by design (FP-1)
        cur.execute(
            "INSERT INTO v2_research_job (id, owner, authorization_ref,"
            " inputs, schedule, job_state, attempt_count, data_class, mode,"
            " operator_id, correlation_id, created_at)"
            f" VALUES ('j1','o','BO-V2-BE-7-001','{{}}','{{}}','queued',0,{BE1})")
        cur.execute("UPDATE v2_research_job SET job_state='running'")
        conn.commit()
    finally:
        conn.close()


# --- T-7: no-touch (1) + downgrade (1) + drift (2) + checks (2) --------------------


def test_no_touch_protected_state(tmp_path: Path) -> None:
    db_file, db_url = _db(tmp_path, REV_0046)
    provider = _q(db_file,
                  "SELECT provider_id, source_status FROM v2_md_provider")
    compver_before = _q(db_file,
                        "SELECT component, version, source_hash"
                        " FROM v2_computation_version ORDER BY component")
    triggers_before = _v2_triggers(db_file)
    assert len(triggers_before) == 32
    result = _alembic(["upgrade", REV_0047], db_url)
    assert result.returncode == 0, result.stderr
    assert _q(db_file,
              "SELECT provider_id, source_status"
              " FROM v2_md_provider") == provider
    after_prior = _q(db_file,
                     "SELECT component, version, source_hash"
                     " FROM v2_computation_version"
                     " WHERE component NOT IN ('replay_engine',"
                     " 'research_job_engine') ORDER BY component")
    assert after_prior == compver_before
    after = _v2_triggers(db_file)
    assert after - triggers_before == set(TRIGGERS_0047)


def test_downgrade_cycle_content_based(tmp_path: Path) -> None:
    db_file, db_url = _db(tmp_path, REV_0047)
    down = _alembic(["downgrade", REV_0046], db_url)
    assert down.returncode == 0, down.stderr
    tables = {r[0] for r in _q(
        db_file, "SELECT name FROM sqlite_master WHERE type='table'")}
    for t in ("v2_backtest_input", "v2_research_result", "v2_research_job"):
        assert t not in tables
    assert len(_v2_triggers(db_file)) == 32
    assert _q(db_file, "SELECT COUNT(*) FROM v2_permission")[0][0] == 41
    assert _q(db_file,
              "SELECT COUNT(*) FROM v2_computation_version")[0][0] == 6
    assert "v2_computation_version_immutable_delete" in _v2_triggers(db_file)
    up = _alembic(["upgrade", REV_0047], db_url)
    assert up.returncode == 0, up.stderr
    assert len(_q(db_file, "SELECT role, permission FROM v2_permission")) == 49


@pytest.mark.parametrize("rev", [REV_0046, REV_0047])
def test_drift_gate(tmp_path: Path, rev: str) -> None:
    """Format-independent (PGF-014): zero BE-7 tokens in either form."""
    db_file, db_url = _db(tmp_path, rev)
    check = _alembic(["check"], db_url)
    drift = (check.stdout + check.stderr).lower()
    assert check.returncode != 0
    for marker in ("v2_backtest_input", "v2_cost_model",
                   "v2_strategy_version", "v2_research_job",
                   "v2_research_result", "v2_md_", "v2_permission",
                   "v2_computation_version"):
        assert marker not in drift, f"BE-7 drift at {rev}: {marker}"
    if "not up to date" not in drift:
        assert "audit_write_failure_records" in drift


def test_job_state_and_outcome_checks(tmp_path: Path) -> None:
    db_file, _ = _db(tmp_path, REV_0047)
    conn = sqlite3.connect(db_file)
    try:
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO v2_research_job (id, owner, authorization_ref,"
                " inputs, schedule, job_state, attempt_count, data_class,"
                " mode, operator_id, correlation_id, created_at)"
                f" VALUES ('jx','o','x','{{}}','{{}}','executing',0,{BE1})")
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO v2_strategy_version (id, strategy_id,"
                " record_seq, name, parameters, lifecycle_state, data_class,"
                " mode, operator_id, correlation_id, created_at)"
                f" VALUES ('sx','st-x',1,'S','{{}}','live',{BE1})")
    finally:
        conn.close()
