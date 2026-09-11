"""V2 BE-6 migration lifecycle tests — BO-V2-BE-6-001 T-1…T-7.

0046 on dedicated file-based SQLite chains. Content-based comparisons only
(PGF-012). Pinned totals: triggers 28→32; permissions 35→41; compver 5→6.
"""

from __future__ import annotations

import os
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

BACKEND_DIR = Path(__file__).resolve().parents[1]
TRANS_AUTHORITY = "BO-V2-BE-3-P2-TRANS-001"  # 0042 gate (test chains only)
REV_0045 = "20260902_0045"
REV_0046 = "20260903_0046"

TRIGGERS_0046 = {
    "v2_portfolio_definition_immutable_update":
        "V2 portfolio definitions are immutable; UPDATE prohibited",
    "v2_portfolio_definition_immutable_delete":
        "V2 portfolio definitions are immutable; DELETE prohibited",
    "v2_portfolio_risk_report_immutable_update":
        "V2 portfolio risk reports are immutable; UPDATE prohibited",
    "v2_portfolio_risk_report_immutable_delete":
        "V2 portfolio risk reports are immutable; DELETE prohibited",
}

PERMS_0046 = {
    ("admin", "v2.research.portfolio.read", "SAL-2"),
    ("admin", "v2.research.portfolio.define", "SAL-3"),
    ("admin", "v2.research.portfolio_risk.read", "SAL-2"),
    ("admin", "v2.research.portfolio_risk.compute", "SAL-3"),
    ("operator", "v2.research.portfolio.read", "SAL-2"),
    ("operator", "v2.research.portfolio_risk.read", "SAL-2"),
}


def _alembic(args: list[str], db_url: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["AXIOM_DATABASE_URL"] = db_url
    env.setdefault("AXIOM_ENVIRONMENT", "testing")
    env.setdefault("AXIOM_ALLOW_INSECURE_DEV", "true")
    env.setdefault("AXIOM_JWT_SECRET_KEY", "test-secret-key-at-least-32-chars-long!!")
    env.setdefault("AXIOM_V2_MODE", "RESEARCH")
    env["AXIOM_TD_TRANSITION_AUTHORITY_REF"] = TRANS_AUTHORITY
    return subprocess.run(
        [sys.executable, "-m", "alembic", *args],
        cwd=BACKEND_DIR, env=env, capture_output=True, text=True, timeout=600,
    )


def _db(tmp_path: Path, rev: str) -> tuple[Path, str]:
    db_file = tmp_path / "be6.db"
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
        "SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE 'v2_%'")}


def _insert_definition(cur, *, rid="p1", pid="pf-1", seq=1,
                       basis="hypothetical", dc="synthetic"):
    cur.execute(
        "INSERT INTO v2_portfolio_definition"
        " (id, portfolio_id, record_seq, name, basis, allocations,"
        "  base_currency, data_class, assumptions, mode, operator_id,"
        "  created_at)"
        f" VALUES ('{rid}','{pid}',{seq},'W','{basis}','[]','USD','{dc}',"
        " '{}','RESEARCH','t','2026-09-03 00:00:00+00:00')")


# --- T-1/T-2: chain + DDL content --------------------------------------------------


def test_0046_tables_seeds_triggers(tmp_path: Path) -> None:
    db_file, _ = _db(tmp_path, REV_0046)

    tables = {r[0] for r in _q(
        db_file, "SELECT name FROM sqlite_master WHERE type='table'")}
    assert {"v2_portfolio_definition", "v2_portfolio_risk_report"} <= tables

    cols = [r[1] for r in _q(db_file, "PRAGMA table_info(v2_portfolio_definition)")]
    for c in ("record_seq", "supersedes", "basis", "allocations",
              "assumptions", "data_class"):
        assert c in cols
    rcols = [r[1] for r in _q(db_file, "PRAGMA table_info(v2_portfolio_risk_report)")]
    for c in ("time_basis", "input_refs", "inputs_hash", "metrics",
              "scenarios", "basis_label", "engine_versions_hash"):
        assert c in rcols

    trigs = _v2_triggers(db_file)
    assert len(trigs) == 32  # T-3: 28 + 4
    assert set(TRIGGERS_0046) <= trigs

    perms = _q(db_file, "SELECT role, permission, sal FROM v2_permission")
    assert len(perms) == 41  # T-4
    assert len({(r, p) for r, p, _ in perms}) == 41  # no duplicates
    assert PERMS_0046 <= {tuple(r) for r in perms}
    # forbidden vocabulary absent from ALL permissions (T-4)
    for _r, p, _s in perms:
        for banned in ("account", "order", "position", "broker", "execution"):
            assert banned not in p

    compver = _q(db_file,
                 "SELECT component, version, length(source_hash)"
                 " FROM v2_computation_version")
    assert len(compver) == 6  # T-5
    assert ("portfolio_risk_engine", "pre-1.0.0", 64) in compver


def test_0046_guard_messages_verbatim(tmp_path: Path) -> None:
    db_file, _ = _db(tmp_path, REV_0046)
    conn = sqlite3.connect(db_file)
    try:
        cur = conn.cursor()
        _insert_definition(cur)
        cur.execute(
            "INSERT INTO v2_portfolio_risk_report"
            " (id, portfolio_definition_id, as_of, time_basis, input_refs,"
            "  inputs_hash, metrics, scenarios, status, basis_label,"
            "  data_class, engine_versions, engine_versions_hash, mode,"
            "  operator_id, created_at)"
            " VALUES ('r1','p1','2026-09-03 00:00:00+00:00','{}','{}','h1',"
            " '[]','[]','available','hypothetical-research','synthetic',"
            " '{}','h2','RESEARCH','t','2026-09-03 00:00:00+00:00')")
        conn.commit()
        for sql, trig in (
            ("UPDATE v2_portfolio_definition SET name='x'",
             "v2_portfolio_definition_immutable_update"),
            ("DELETE FROM v2_portfolio_definition",
             "v2_portfolio_definition_immutable_delete"),
            ("UPDATE v2_portfolio_risk_report SET status='stale'",
             "v2_portfolio_risk_report_immutable_update"),
            ("DELETE FROM v2_portfolio_risk_report",
             "v2_portfolio_risk_report_immutable_delete"),
        ):
            with pytest.raises(sqlite3.DatabaseError) as excinfo:
                cur.execute(sql)
            assert str(excinfo.value) == TRIGGERS_0046[trig]  # verbatim
    finally:
        conn.close()


def test_0046_single_value_checks_refuse(tmp_path: Path) -> None:
    """P-6: the band exclusions are structural — `basis` refuses any
    non-hypothetical value; `basis_label` refuses any non-research label."""
    db_file, _ = _db(tmp_path, REV_0046)
    conn = sqlite3.connect(db_file)
    try:
        cur = conn.cursor()
        with pytest.raises(sqlite3.IntegrityError):
            _insert_definition(cur, rid="p2", pid="pf-2", basis="real")
        with pytest.raises(sqlite3.IntegrityError):
            _insert_definition(cur, rid="p3", pid="pf-3", basis="live_account")
        _insert_definition(cur, rid="p4", pid="pf-4")
        conn.commit()
        with pytest.raises(sqlite3.IntegrityError):
            cur.execute(
                "INSERT INTO v2_portfolio_risk_report"
                " (id, portfolio_definition_id, as_of, time_basis, input_refs,"
                "  inputs_hash, metrics, scenarios, status, basis_label,"
                "  data_class, engine_versions, engine_versions_hash, mode,"
                "  operator_id, created_at)"
                " VALUES ('r2','p4','2026-09-03 00:00:00+00:00','{}','{}','hx',"
                " '[]','[]','available','account-state','synthetic',"
                " '{}','h2','RESEARCH','t','2026-09-03 00:00:00+00:00')")
    finally:
        conn.close()


def test_0046_versioned_uniqueness_behavioral(tmp_path: Path) -> None:
    """P-1: same (portfolio_id, record_seq) refused; next seq allowed."""
    db_file, _ = _db(tmp_path, REV_0046)
    conn = sqlite3.connect(db_file)
    try:
        cur = conn.cursor()
        _insert_definition(cur, rid="u1", pid="pf-u", seq=1)
        conn.commit()
        with pytest.raises(sqlite3.IntegrityError):
            _insert_definition(cur, rid="u2", pid="pf-u", seq=1)
        _insert_definition(cur, rid="u3", pid="pf-u", seq=2)
        conn.commit()
    finally:
        conn.close()


# --- T-7: no-touch across 0046 ----------------------------------------------------


def test_no_touch_protected_state(tmp_path: Path) -> None:
    db_file, db_url = _db(tmp_path, REV_0045)

    provider = _q(db_file,
                  "SELECT provider_id, source_status, entitlement_status,"
                  " persistence_permitted FROM v2_md_provider"
                  " ORDER BY provider_id")
    compver_before = _q(db_file,
                        "SELECT component, version, source_hash"
                        " FROM v2_computation_version ORDER BY component")
    triggers_before = _v2_triggers(db_file)
    assert len(triggers_before) == 28

    result = _alembic(["upgrade", REV_0046], db_url)
    assert result.returncode == 0, result.stderr

    assert _q(db_file,
              "SELECT provider_id, source_status, entitlement_status,"
              " persistence_permitted FROM v2_md_provider"
              " ORDER BY provider_id") == provider
    compver_after = _q(db_file,
                       "SELECT component, version, source_hash"
                       " FROM v2_computation_version"
                       " WHERE component != 'portfolio_risk_engine'"
                       " ORDER BY component")
    assert compver_after == compver_before  # BE-4/BE-5 rows untouched
    after = _v2_triggers(db_file)
    assert triggers_before <= after
    assert after - triggers_before == set(TRIGGERS_0046)


# --- Downgrade cycle (content-based; O-2 obligation) --------------------------------


def test_downgrade_cycle_content_based(tmp_path: Path) -> None:
    db_file, db_url = _db(tmp_path, REV_0046)
    before = {
        "perms": sorted(_q(db_file,
                           "SELECT role, permission, sal FROM v2_permission"
                           " WHERE permission LIKE 'v2.research.portfolio%'")),
        "compver": sorted(_q(db_file,
                             "SELECT component, version"
                             " FROM v2_computation_version")),
    }
    down = _alembic(["downgrade", REV_0045], db_url)
    assert down.returncode == 0, down.stderr
    tables = {r[0] for r in _q(
        db_file, "SELECT name FROM sqlite_master WHERE type='table'")}
    assert "v2_portfolio_definition" not in tables
    assert "v2_portfolio_risk_report" not in tables
    assert len(_v2_triggers(db_file)) == 28
    assert _q(db_file, "SELECT COUNT(*) FROM v2_permission")[0][0] == 35
    assert _q(db_file,
              "SELECT COUNT(*) FROM v2_computation_version")[0][0] == 5
    # compver delete guard restored (drop/recreate/verify pattern)
    assert "v2_computation_version_immutable_delete" in _v2_triggers(db_file)

    up = _alembic(["upgrade", REV_0046], db_url)
    assert up.returncode == 0, up.stderr
    after = {
        "perms": sorted(_q(db_file,
                           "SELECT role, permission, sal FROM v2_permission"
                           " WHERE permission LIKE 'v2.research.portfolio%'")),
        "compver": sorted(_q(db_file,
                             "SELECT component, version"
                             " FROM v2_computation_version")),
    }
    assert after == before


# --- T-6: drift at the 0046 head ------------------------------------------------------


def test_drift_gate_head(tmp_path: Path) -> None:
    db_file, db_url = _db(tmp_path, REV_0046)
    check = _alembic(["check"], db_url)
    drift = (check.stdout + check.stderr).lower()
    assert check.returncode != 0  # inherited V1 drift persists by design
    for marker in ("v2_portfolio_definition", "v2_portfolio_risk_report",
                   "v2_ml_", "v2_signal", "v2_md_", "v2_permission",
                   "v2_computation_version", "v2_market_context",
                   "v2_chart_intelligence"):
        assert marker not in drift, f"BE-6 drift detected: {marker}"
    if "not up to date" not in drift:
        assert "audit_write_failure_records" in drift  # inherited set
