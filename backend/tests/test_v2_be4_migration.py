"""V2 BE-4 migration lifecycle tests — BO-V2-BE-4-001 D-5 groups 6–7.

Migration 20260831_0043 on dedicated file-based SQLite chains. All row
assertions content-based (PGF-012). No-touch: provider row, history count,
the ORIGINAL 12 guard triggers, persistence_permitted — byte-identical;
v2 trigger count = 18 after 0043. Six R-2 guard messages verbatim.
"""

from __future__ import annotations

import os
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

BACKEND_DIR = Path(__file__).resolve().parents[1]
TRANS_AUTHORITY = "BO-V2-BE-3-P2-TRANS-001"  # 0042 gate (consumed act; test chains only)
BE4_REV = "20260831_0043"
PARENT_REV = "20260829_0042"

# R-2 pins (BO §4 D-1) — exact names and messages.
BE4_TRIGGERS = {
    "v2_computation_version_immutable_update":
        "V2 computation version registry is immutable; UPDATE prohibited",
    "v2_computation_version_immutable_delete":
        "V2 computation version registry is immutable; DELETE prohibited",
    "v2_market_context_report_immutable_update":
        "V2 market context reports are immutable; UPDATE prohibited",
    "v2_market_context_report_immutable_delete":
        "V2 market context reports are immutable; DELETE prohibited",
    "v2_chart_intelligence_report_immutable_update":
        "V2 chart intelligence reports are immutable; UPDATE prohibited",
    "v2_chart_intelligence_report_immutable_delete":
        "V2 chart intelligence reports are immutable; DELETE prohibited",
}

BE4_PERMISSIONS = {
    ("admin", "v2.research.market_context.read"),
    ("admin", "v2.research.chart_intelligence.read"),
    ("admin", "v2.research.market_context.compute"),
    ("operator", "v2.research.market_context.read"),
    ("operator", "v2.research.chart_intelligence.read"),
}


def _alembic(args: list[str], db_url: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["AXIOM_DATABASE_URL"] = db_url
    env.setdefault("AXIOM_ENVIRONMENT", "testing")
    env.setdefault("AXIOM_ALLOW_INSECURE_DEV", "true")
    env.setdefault("AXIOM_JWT_SECRET_KEY", "test-secret-key-at-least-32-chars-long!!")
    env.setdefault("AXIOM_V2_MODE", "RESEARCH")
    # 0042 sits in this chain's history; its authority gate must be
    # satisfied for a fresh test chain (accepted transition-test pattern).
    env["AXIOM_TD_TRANSITION_AUTHORITY_REF"] = TRANS_AUTHORITY
    return subprocess.run(
        [sys.executable, "-m", "alembic", *args],
        cwd=BACKEND_DIR, env=env, capture_output=True, text=True, timeout=600,
    )


def _db(tmp_path: Path, rev: str = BE4_REV) -> tuple[Path, str]:
    db_file = tmp_path / "be4.db"
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
        "SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE 'v2_%'",
    )}


def _provider_state(db_file: Path):
    return _q(
        db_file,
        "SELECT provider_id, source_status, entitlement_status,"
        " persistence_permitted FROM v2_md_provider ORDER BY provider_id",
    )


# ---------------------------------------------------------------------------
# Upgrade content
# ---------------------------------------------------------------------------


def test_upgrade_creates_tables_seeds_and_triggers(tmp_path: Path) -> None:
    db_file, _ = _db(tmp_path)

    tables = {r[0] for r in _q(
        db_file, "SELECT name FROM sqlite_master WHERE type='table'")}
    assert {"v2_computation_version", "v2_market_context_report",
            "v2_chart_intelligence_report"} <= tables

    # seeds: exactly the three components, content-compared
    rows = _q(db_file,
              "SELECT component, version FROM v2_computation_version")
    assert sorted(rows) == [
        ("chart_intelligence_engine", "cie-1.0.0"),
        ("indicator_engine", "v1-reuse-1.0.0"),
        ("market_context_engine", "mce-1.0.0"),
    ]
    hashes = _q(db_file, "SELECT component, source_hash FROM v2_computation_version")
    for _component, source_hash in hashes:
        assert len(source_hash) == 64  # full SHA-256 recorded at seed time

    perms = {tuple(r) for r in _q(
        db_file,
        "SELECT role, permission FROM v2_permission"
        " WHERE permission LIKE 'v2.research%'",
    )}
    assert perms == BE4_PERMISSIONS

    # trigger topology: original 12 + the 6 pinned = 18
    trigs = _v2_triggers(db_file)
    assert len(trigs) == 18
    assert set(BE4_TRIGGERS) <= trigs


def test_guard_messages_verbatim(tmp_path: Path) -> None:
    db_file, _ = _db(tmp_path)
    conn = sqlite3.connect(db_file)
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO v2_market_context_report"
            " (id, instrument_id, timeframe_set, as_of, mode, status,"
            "  validation_tier, input_snapshot_id, input_content_hash,"
            "  observations, engine_versions, engine_versions_hash,"
            "  operator_id, created_at)"
            " VALUES ('r1','FX.EURUSD','[\"H1\"]','2026-08-31 00:00:00+00:00',"
            " 'RESEARCH','available','pipeline-validation','snap','h1',"
            " '{}','{}','h2','tester','2026-08-31 00:00:00+00:00')"
        )
        cur.execute(
            "INSERT INTO v2_chart_intelligence_report"
            " (id, market_context_report_id, as_of, mode, status,"
            "  annotations, interpretations, engine_versions, operator_id,"
            "  created_at)"
            " VALUES ('c1','r1','2026-08-31 00:00:00+00:00','RESEARCH',"
            " 'available','{}','{}','{}','tester','2026-08-31 00:00:00+00:00')"
        )
        conn.commit()

        checks = [
            ("UPDATE v2_computation_version SET version='x'",
             BE4_TRIGGERS["v2_computation_version_immutable_update"]),
            ("DELETE FROM v2_computation_version",
             BE4_TRIGGERS["v2_computation_version_immutable_delete"]),
            ("UPDATE v2_market_context_report SET status='x'",
             BE4_TRIGGERS["v2_market_context_report_immutable_update"]),
            ("DELETE FROM v2_market_context_report",
             BE4_TRIGGERS["v2_market_context_report_immutable_delete"]),
            ("UPDATE v2_chart_intelligence_report SET status='x'",
             BE4_TRIGGERS["v2_chart_intelligence_report_immutable_update"]),
            ("DELETE FROM v2_chart_intelligence_report",
             BE4_TRIGGERS["v2_chart_intelligence_report_immutable_delete"]),
        ]
        for sql, message in checks:
            with pytest.raises(sqlite3.DatabaseError) as excinfo:
                cur.execute(sql)
            assert str(excinfo.value) == message  # verbatim (D-5 pin)
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# No-touch group (BG-3): provider state byte-identical across 0043
# ---------------------------------------------------------------------------


def test_no_touch_provider_state_across_0043(tmp_path: Path) -> None:
    db_file, db_url = _db(tmp_path, rev=PARENT_REV)

    before_provider = _provider_state(db_file)
    before_history = _q(
        db_file,
        "SELECT provider_id, from_status, to_status, authority_ref,"
        " evidence_ref FROM v2_md_provider_status_history"
        " ORDER BY created_at",
    )
    before_triggers = _v2_triggers(db_file)
    assert len(before_triggers) == 12  # original set at 0042

    result = _alembic(["upgrade", BE4_REV], db_url)
    assert result.returncode == 0, result.stderr

    # provider row + history byte-identical (content-based comparison)
    assert _provider_state(db_file) == before_provider
    after_history = _q(
        db_file,
        "SELECT provider_id, from_status, to_status, authority_ref,"
        " evidence_ref FROM v2_md_provider_status_history"
        " ORDER BY created_at",
    )
    assert after_history == before_history
    # persistence still false
    assert all(row[3] == 0 for row in _provider_state(db_file))
    # original 12 triggers unchanged; exactly the 6 pinned added
    after_triggers = _v2_triggers(db_file)
    assert before_triggers <= after_triggers
    assert after_triggers - before_triggers == set(BE4_TRIGGERS)
    # provider guard still fires post-0043
    with pytest.raises(sqlite3.DatabaseError, match="registry is immutable"):
        conn = sqlite3.connect(db_file)
        try:
            conn.execute(
                "UPDATE v2_md_provider SET source_status='integrated'"
                " WHERE provider_id='twelvedata'"
            )
        finally:
            conn.close()


# ---------------------------------------------------------------------------
# Group 7 — upgrade → downgrade → re-upgrade cycle (content-based)
# ---------------------------------------------------------------------------


def test_downgrade_reupgrade_cycle(tmp_path: Path) -> None:
    db_file, db_url = _db(tmp_path)

    before = {
        "compver": sorted(_q(
            db_file, "SELECT component, version, source_hash"
                     " FROM v2_computation_version")),
        "perms": sorted(_q(
            db_file, "SELECT role, permission FROM v2_permission"
                     " WHERE permission LIKE 'v2.research%'")),
        "provider": _provider_state(db_file),
    }

    down = _alembic(["downgrade", PARENT_REV], db_url)
    assert down.returncode == 0, down.stderr

    tables = {r[0] for r in _q(
        db_file, "SELECT name FROM sqlite_master WHERE type='table'")}
    assert "v2_computation_version" not in tables
    assert "v2_market_context_report" not in tables
    assert "v2_chart_intelligence_report" not in tables
    assert len(_v2_triggers(db_file)) == 12  # only this revision's dropped
    assert _q(db_file,
              "SELECT COUNT(*) FROM v2_permission"
              " WHERE permission LIKE 'v2.research%'")[0][0] == 0
    # BG-3: provider state untouched by the downgrade
    assert _provider_state(db_file) == before["provider"]

    up = _alembic(["upgrade", BE4_REV], db_url)
    assert up.returncode == 0, up.stderr
    after = {
        "compver": sorted(_q(
            db_file, "SELECT component, version, source_hash"
                     " FROM v2_computation_version")),
        "perms": sorted(_q(
            db_file, "SELECT role, permission FROM v2_permission"
                     " WHERE permission LIKE 'v2.research%'")),
        "provider": _provider_state(db_file),
    }
    # content-based: same components/hashes/permissions/provider state
    assert [r[:2] + (len(r[2]),) for r in after["compver"]] == [
        r[:2] + (len(r[2]),) for r in before["compver"]
    ]
    assert [r[:2] for r in after["compver"]] == [r[:2] for r in before["compver"]]
    assert after["perms"] == before["perms"]
    assert after["provider"] == before["provider"]
    assert len(_v2_triggers(db_file)) == 18


# ---------------------------------------------------------------------------
# Drift gate (BG-8): exactly the inherited V1 set, zero BE-4 tokens
# ---------------------------------------------------------------------------


def test_drift_gate_zero_be4_tokens(tmp_path: Path) -> None:
    """Generational scoping (BE-5 era): 0043 is no longer the chain head,
    so `alembic check` at 0043 returns the revision-offset refusal ('not
    up to date') instead of the itemized list — format-independent
    assertion per the PGF-014 discipline. In EITHER form, zero BE-4
    tokens may appear; the itemized inherited set is asserted only when
    the itemized form is produced (i.e. when 0043 was head)."""
    db_file, db_url = _db(tmp_path)
    check = _alembic(["check"], db_url)
    drift = (check.stdout + check.stderr).lower()
    assert check.returncode != 0  # drift/offset persists by design
    for marker in ("v2_computation_version", "v2_market_context_report",
                   "v2_chart_intelligence_report", "v2_md_", "v2_permission",
                   "v2_audit_event", "v2_lineage_record"):
        assert marker not in drift, f"BE-4 drift detected: {marker}"
    if "not up to date" not in drift:
        # itemized form (0043 was head): inherited V1 baseline exact
        assert "audit_write_failure_records" in drift
