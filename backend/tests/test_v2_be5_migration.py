"""V2 BE-5 migration lifecycle tests — BO-V2-BE-5-001 T-1…T-6, T-9…T-11.

0044/0045 on dedicated file-based SQLite chains. Content-based row
comparison only (PGF-012). No-touch group proves BE-3 + BE-4 state
byte-identical across both migrations. P-5 pinned totals asserted:
triggers 18→24→28; permissions 27→34→35; compver 3→4→5.
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
REV_0043 = "20260831_0043"
REV_0044 = "20260902_0044"
REV_0045 = "20260902_0045"

TRIGGERS_0044 = {
    "v2_ml_governance_record_immutable_update":
        "V2 ML governance records are immutable; UPDATE prohibited",
    "v2_ml_governance_record_immutable_delete":
        "V2 ML governance records are immutable; DELETE prohibited",
    "v2_ml_lifecycle_event_immutable_update":
        "V2 ML lifecycle events are immutable; UPDATE prohibited",
    "v2_ml_lifecycle_event_immutable_delete":
        "V2 ML lifecycle events are immutable; DELETE prohibited",
    "v2_ml_diagnostic_report_immutable_update":
        "V2 ML diagnostic reports are immutable; UPDATE prohibited",
    "v2_ml_diagnostic_report_immutable_delete":
        "V2 ML diagnostic reports are immutable; DELETE prohibited",
}
TRIGGERS_0045 = {
    "v2_signal_record_immutable_update":
        "V2 signal records are immutable; UPDATE prohibited",
    "v2_signal_record_immutable_delete":
        "V2 signal records are immutable; DELETE prohibited",
    "v2_signal_state_event_immutable_update":
        "V2 signal state events are immutable; UPDATE prohibited",
    "v2_signal_state_event_immutable_delete":
        "V2 signal state events are immutable; DELETE prohibited",
}

PERMS_0044 = {
    ("admin", "v2.research.ml_governance.read", "SAL-2"),
    ("admin", "v2.research.ml_governance.decide", "SAL-3"),
    ("admin", "v2.research.signal.read", "SAL-2"),
    ("admin", "v2.research.ml_diagnostics.read", "SAL-2"),
    ("operator", "v2.research.ml_governance.read", "SAL-2"),
    ("operator", "v2.research.signal.read", "SAL-2"),
    ("operator", "v2.research.ml_diagnostics.read", "SAL-2"),
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
    db_file = tmp_path / "be5.db"
    db_url = f"sqlite+aiosqlite:///{db_file}"
    result = _alembic(["upgrade", rev], db_url)  # literal revision, never head
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


# --- T-2…T-5: 0044 content -------------------------------------------------------


def test_0044_tables_seeds_triggers(tmp_path: Path) -> None:
    db_file, _ = _db(tmp_path, REV_0044)

    tables = {r[0] for r in _q(
        db_file, "SELECT name FROM sqlite_master WHERE type='table'")}
    assert {"v2_ml_governance_record", "v2_ml_lifecycle_event",
            "v2_ml_diagnostic_report"} <= tables

    # P-1: versioned unique constraint present; no updated_at_event_id column
    cols = [r[1] for r in _q(db_file, "PRAGMA table_info(v2_ml_governance_record)")]
    assert "record_seq" in cols and "supersedes" in cols
    assert "model_type" in cols and "instrument_class" in cols  # P-3
    assert "updated_at_event_id" not in cols  # P-1
    # P-1 versioned uniqueness proven behaviorally (SQLite renders
    # table-level UNIQUE as an autoindex; behavior over name):
    conn = sqlite3.connect(db_file)
    try:
        conn.execute(
            "INSERT INTO v2_ml_governance_record (id, model_artifact_id,"
            " record_seq, registry_version, model_type, instrument_class,"
            " eligibility_status, calibration_status, freshness_status,"
            " economic_status, statistical_status, deployment_class,"
            " data_class, evidence_refs, mode, operator_id, created_at)"
            " VALUES ('u1','m-uq',1,'1.0','c','fx','unevaluated',"
            "'unevaluated','unknown','unevaluated','unevaluated',"
            "'research','synthetic','{}','RESEARCH','t',"
            "'2026-09-02 00:00:00+00:00')")
        conn.commit()
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO v2_ml_governance_record (id, model_artifact_id,"
                " record_seq, registry_version, model_type, instrument_class,"
                " eligibility_status, calibration_status, freshness_status,"
                " economic_status, statistical_status, deployment_class,"
                " data_class, evidence_refs, mode, operator_id, created_at)"
                " VALUES ('u2','m-uq',1,'1.0','c','fx','unevaluated',"
                "'unevaluated','unknown','unevaluated','unevaluated',"
                "'research','synthetic','{}','RESEARCH','t',"
                "'2026-09-02 00:00:00+00:00')")  # same (artifact, seq) refused
        # same artifact, next seq allowed (row versioning)
        conn.execute(
            "INSERT INTO v2_ml_governance_record (id, model_artifact_id,"
            " record_seq, registry_version, model_type, instrument_class,"
            " eligibility_status, calibration_status, freshness_status,"
            " economic_status, statistical_status, deployment_class,"
            " data_class, evidence_refs, mode, operator_id, created_at)"
            " VALUES ('u3','m-uq',2,'1.0','c','fx','unevaluated',"
            "'unevaluated','unknown','unevaluated','unevaluated',"
            "'research','synthetic','{}','RESEARCH','t',"
            "'2026-09-02 00:00:00+00:00')")
        conn.commit()
    finally:
        conn.close()

    # P-2: diagnostic-report determinism anchor — a UNIQUE autoindex exists
    # over (model_artifact_id, inputs_hash, engine_versions_hash); proven
    # behaviorally like the P-1 constraint (SQLite autoindex naming).
    diag_uniques = _q(db_file, "PRAGMA index_list(v2_ml_diagnostic_report)")
    assert any(u[2] == 1 and u[3] == "u" for u in diag_uniques)

    # T-3: 24 triggers = 18 + the 6 pinned
    trigs = _v2_triggers(db_file)
    assert len(trigs) == 24
    assert set(TRIGGERS_0044) <= trigs

    # T-4: 34 permissions = 27 + 7, content-exact, no duplicates
    perms = _q(db_file, "SELECT role, permission, sal FROM v2_permission")
    assert len(perms) == 34
    assert len(set((r, p) for r, p, _s in perms)) == 34  # no duplicates
    assert PERMS_0044 <= {tuple(r) for r in perms}

    # T-5: compver 4 rows; mge hash is a real sha256
    compver = _q(db_file,
                 "SELECT component, version, length(source_hash)"
                 " FROM v2_computation_version ORDER BY component")
    assert len(compver) == 4
    assert ("ml_governance_engine", "mge-1.0.0", 64) in compver


def test_0044_guard_messages_verbatim(tmp_path: Path) -> None:
    db_file, _ = _db(tmp_path, REV_0044)
    conn = sqlite3.connect(db_file)
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO v2_ml_governance_record"
            " (id, model_artifact_id, record_seq, registry_version,"
            "  model_type, instrument_class, eligibility_status,"
            "  calibration_status, freshness_status, economic_status,"
            "  statistical_status, deployment_class, data_class,"
            "  evidence_refs, mode, operator_id, created_at)"
            " VALUES ('g1','m1',1,'1.0','classifier','forex','unevaluated',"
            " 'unevaluated','unknown','unevaluated','unevaluated','research',"
            " 'synthetic','{}','RESEARCH','t','2026-09-02 00:00:00+00:00')")
        cur.execute(
            "INSERT INTO v2_ml_lifecycle_event"
            " (id, governance_record_id, event_type, from_value, to_value,"
            "  decision_basis, mode, actor_id, operator_id, created_at)"
            " VALUES ('e1','g1','registered','none','research','{}',"
            " 'RESEARCH','t','t','2026-09-02 00:00:00+00:00')")
        cur.execute(
            "INSERT INTO v2_ml_diagnostic_report"
            " (id, model_artifact_id, diagnostics, input_refs, inputs_hash,"
            "  engine_versions, engine_versions_hash, data_class, mode,"
            "  operator_id, created_at)"
            " VALUES ('d1','m1','{}','{}','h1','{}','h2','synthetic',"
            " 'RESEARCH','t','2026-09-02 00:00:00+00:00')")
        conn.commit()
        for sql, trigger in (
            ("UPDATE v2_ml_governance_record SET deployment_class='champion'",
             "v2_ml_governance_record_immutable_update"),
            ("DELETE FROM v2_ml_governance_record",
             "v2_ml_governance_record_immutable_delete"),
            ("UPDATE v2_ml_lifecycle_event SET to_value='x'",
             "v2_ml_lifecycle_event_immutable_update"),
            ("DELETE FROM v2_ml_lifecycle_event",
             "v2_ml_lifecycle_event_immutable_delete"),
            ("UPDATE v2_ml_diagnostic_report SET data_class='live'",
             "v2_ml_diagnostic_report_immutable_update"),
            ("DELETE FROM v2_ml_diagnostic_report",
             "v2_ml_diagnostic_report_immutable_delete"),
        ):
            with pytest.raises(sqlite3.DatabaseError) as excinfo:
                cur.execute(sql)
            assert str(excinfo.value) == TRIGGERS_0044[trigger]
    finally:
        conn.close()


def test_0044_check_vocabularies(tmp_path: Path) -> None:
    db_file, _ = _db(tmp_path, REV_0044)
    conn = sqlite3.connect(db_file)
    try:
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO v2_ml_governance_record"
                " (id, model_artifact_id, record_seq, registry_version,"
                "  model_type, instrument_class, eligibility_status,"
                "  calibration_status, freshness_status, economic_status,"
                "  statistical_status, deployment_class, data_class,"
                "  evidence_refs, mode, operator_id, created_at)"
                " VALUES ('g2','m2',1,'1.0','c','fx','unevaluated',"
                " 'unevaluated','unknown','unevaluated','unevaluated',"
                " 'LIVE_SERVING','synthetic','{}','RESEARCH','t',"
                " '2026-09-02 00:00:00+00:00')")
    finally:
        conn.close()


# --- T-6: 0045 content -------------------------------------------------------------


def test_0045_tables_seeds_triggers(tmp_path: Path) -> None:
    db_file, _ = _db(tmp_path, REV_0045)
    tables = {r[0] for r in _q(
        db_file, "SELECT name FROM sqlite_master WHERE type='table'")}
    assert {"v2_signal_record", "v2_signal_state_event"} <= tables

    trigs = _v2_triggers(db_file)
    assert len(trigs) == 28  # 24 + 4
    assert set(TRIGGERS_0045) <= trigs

    perms = _q(db_file, "SELECT role, permission, sal FROM v2_permission")
    assert len(perms) == 35
    assert ("admin", "v2.research.signal.emit", "SAL-3") in {
        tuple(r) for r in perms}

    compver = _q(db_file, "SELECT component, version FROM v2_computation_version")
    assert len(compver) == 5
    assert ("signal_engine", "sge-1.0.0") in compver


def test_0045_guard_messages_and_checks(tmp_path: Path) -> None:
    db_file, _ = _db(tmp_path, REV_0045)
    conn = sqlite3.connect(db_file)
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO v2_signal_record"
            " (id, family, signal_type, instrument_id, timeframe, state,"
            "  uncertainty, limitations, source_family_refs, data_class,"
            "  as_of, mode, operator_id, created_at)"
            " VALUES ('s1','structural','bos','forex.eurusd','M15','emitted',"
            " '{}','{}','{}','synthetic','2026-09-02 00:00:00+00:00',"
            " 'RESEARCH','t','2026-09-02 00:00:00+00:00')")
        conn.commit()
        for sql, trigger in (
            ("UPDATE v2_signal_record SET state='refused'",
             "v2_signal_record_immutable_update"),
            ("DELETE FROM v2_signal_record",
             "v2_signal_record_immutable_delete"),
        ):
            with pytest.raises(sqlite3.DatabaseError) as excinfo:
                cur.execute(sql)
            assert str(excinfo.value) == TRIGGERS_0045[trigger]
        # family/state CHECK vocabularies exact
        with pytest.raises(sqlite3.IntegrityError):
            cur.execute(
                "INSERT INTO v2_signal_record"
                " (id, family, signal_type, instrument_id, timeframe, state,"
                "  uncertainty, limitations, source_family_refs, data_class,"
                "  as_of, mode, operator_id, created_at)"
                " VALUES ('s2','hybrid','x','i','M15','emitted','{}','{}',"
                " '{}','synthetic','2026-09-02 00:00:00+00:00','RESEARCH',"
                " 't','2026-09-02 00:00:00+00:00')")
        with pytest.raises(sqlite3.IntegrityError):
            cur.execute(
                "INSERT INTO v2_signal_record"
                " (id, family, signal_type, instrument_id, timeframe, state,"
                "  uncertainty, limitations, source_family_refs, data_class,"
                "  as_of, mode, operator_id, created_at)"
                " VALUES ('s3','structural','x','i','M15','active','{}','{}',"
                " '{}','synthetic','2026-09-02 00:00:00+00:00','RESEARCH',"
                " 't','2026-09-02 00:00:00+00:00')")
    finally:
        conn.close()


# --- T-11: no-touch across 0044/0045 ------------------------------------------------


def test_no_touch_be3_be4_state(tmp_path: Path) -> None:
    db_file, db_url = _db(tmp_path, REV_0043)

    provider_before = _q(
        db_file,
        "SELECT provider_id, source_status, entitlement_status,"
        " persistence_permitted FROM v2_md_provider ORDER BY provider_id")
    history_before = _q(
        db_file,
        "SELECT provider_id, from_status, to_status, authority_ref"
        " FROM v2_md_provider_status_history ORDER BY created_at")
    compver_be4_before = _q(
        db_file,
        "SELECT component, version, source_hash FROM v2_computation_version"
        " WHERE component IN ('indicator_engine','market_context_engine',"
        " 'chart_intelligence_engine') ORDER BY component")
    triggers_before = _v2_triggers(db_file)
    assert len(triggers_before) == 18

    result = _alembic(["upgrade", REV_0045], db_url)
    assert result.returncode == 0, result.stderr

    assert _q(db_file,
              "SELECT provider_id, source_status, entitlement_status,"
              " persistence_permitted FROM v2_md_provider"
              " ORDER BY provider_id") == provider_before
    assert _q(db_file,
              "SELECT provider_id, from_status, to_status, authority_ref"
              " FROM v2_md_provider_status_history"
              " ORDER BY created_at") == history_before
    assert _q(db_file,
              "SELECT component, version, source_hash"
              " FROM v2_computation_version WHERE component IN"
              " ('indicator_engine','market_context_engine',"
              " 'chart_intelligence_engine')"
              " ORDER BY component") == compver_be4_before
    after = _v2_triggers(db_file)
    assert triggers_before <= after
    assert after - triggers_before == set(TRIGGERS_0044) | set(TRIGGERS_0045)


# --- Downgrade cycle (content-based) -------------------------------------------------


def test_downgrade_cycle_content_based(tmp_path: Path) -> None:
    db_file, db_url = _db(tmp_path, REV_0045)

    before = {
        "perms": sorted(_q(db_file,
                           "SELECT role, permission, sal FROM v2_permission"
                           " WHERE permission LIKE 'v2.research.ml%'"
                           " OR permission LIKE 'v2.research.signal%'")),
        "compver": sorted(_q(db_file,
                             "SELECT component, version"
                             " FROM v2_computation_version")),
    }
    down = _alembic(["downgrade", REV_0043], db_url)
    assert down.returncode == 0, down.stderr
    tables = {r[0] for r in _q(
        db_file, "SELECT name FROM sqlite_master WHERE type='table'")}
    for t in ("v2_ml_governance_record", "v2_ml_lifecycle_event",
              "v2_ml_diagnostic_report", "v2_signal_record",
              "v2_signal_state_event"):
        assert t not in tables
    assert len(_v2_triggers(db_file)) == 18
    assert _q(db_file,
              "SELECT COUNT(*) FROM v2_permission")[0][0] == 27
    assert _q(db_file,
              "SELECT COUNT(*) FROM v2_computation_version")[0][0] == 3

    up = _alembic(["upgrade", REV_0045], db_url)
    assert up.returncode == 0, up.stderr
    after = {
        "perms": sorted(_q(db_file,
                           "SELECT role, permission, sal FROM v2_permission"
                           " WHERE permission LIKE 'v2.research.ml%'"
                           " OR permission LIKE 'v2.research.signal%'")),
        "compver": sorted(_q(db_file,
                             "SELECT component, version"
                             " FROM v2_computation_version")),
    }
    assert after == before  # content-identical (ids may differ; content compared)


# --- T-10: drift gates at both heads --------------------------------------------------


@pytest.mark.parametrize("rev", [REV_0044, REV_0045])
def test_drift_gate(tmp_path: Path, rev: str) -> None:
    """Format-independent (PGF-014 discipline): at a non-head revision
    alembic 'check' refuses with 'not up to date' and prints no drift
    list; at the head it prints the itemized inherited V1 set. In BOTH
    forms, zero BE-5/V2 tokens may appear."""
    db_file, db_url = _db(tmp_path, rev)
    check = _alembic(["check"], db_url)
    drift = (check.stdout + check.stderr).lower()
    assert check.returncode != 0  # inherited V1 drift persists by design
    for marker in ("v2_ml_governance_record", "v2_ml_lifecycle_event",
                   "v2_ml_diagnostic_report", "v2_signal_record",
                   "v2_signal_state_event", "v2_md_", "v2_permission",
                   "v2_computation_version", "v2_market_context",
                   "v2_chart_intelligence"):
        assert marker not in drift, f"BE-5 drift detected at {rev}: {marker}"
    # GENERATIONAL SCOPING (BE-6 era): 0045 is no longer the chain head,
    # so both revisions now produce the revision-offset form. When the
    # itemized form appears (a revision at head), the inherited set must
    # be exact. Format-independent per the PGF-014 discipline.
    if "not up to date" not in drift:
        assert "audit_write_failure_records" in drift  # inherited set exact
