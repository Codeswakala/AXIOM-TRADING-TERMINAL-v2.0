"""V2 BE-9 migration tests — BO-V2-BE-9-001 T-6/T-9/T-17/T-18/T-19.

0049 on dedicated SQLite chains. Content-based comparisons (PGF-012).
Pins: triggers 58->76; permissions 57->64; compver 10->11.
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
REV_0048 = "20260904_0048"
REV_0049 = "20260905_0049"

TRIGGERS_0049 = {
    "v2_broker_account_immutable_update":
        "V2 broker accounts are immutable; UPDATE prohibited",
    "v2_broker_account_immutable_delete":
        "V2 broker accounts are immutable; DELETE prohibited",
    "v2_broker_balance_immutable_update":
        "V2 broker balances are immutable; UPDATE prohibited",
    "v2_broker_balance_immutable_delete":
        "V2 broker balances are immutable; DELETE prohibited",
    "v2_broker_position_immutable_update":
        "V2 broker positions are immutable; UPDATE prohibited",
    "v2_broker_position_immutable_delete":
        "V2 broker positions are immutable; DELETE prohibited",
    "v2_broker_order_immutable_update":
        "V2 broker orders are immutable; UPDATE prohibited",
    "v2_broker_order_immutable_delete":
        "V2 broker orders are immutable; DELETE prohibited",
    "v2_broker_fill_immutable_update":
        "V2 broker fills are immutable; UPDATE prohibited",
    "v2_broker_fill_immutable_delete":
        "V2 broker fills are immutable; DELETE prohibited",
    "v2_broker_instrument_permission_immutable_update":
        "V2 broker instrument permissions are immutable; UPDATE prohibited",
    "v2_broker_instrument_permission_immutable_delete":
        "V2 broker instrument permissions are immutable; DELETE prohibited",
    "v2_broker_sync_run_immutable_update":
        "V2 broker sync runs are immutable; UPDATE prohibited",
    "v2_broker_sync_run_immutable_delete":
        "V2 broker sync runs are immutable; DELETE prohibited",
    "v2_broker_reconcile_run_immutable_update":
        "V2 broker reconcile runs are immutable; UPDATE prohibited",
    "v2_broker_reconcile_run_immutable_delete":
        "V2 broker reconcile runs are immutable; DELETE prohibited",
    "v2_broker_discrepancy_immutable_update":
        "V2 broker discrepancies are immutable; UPDATE prohibited",
    "v2_broker_discrepancy_immutable_delete":
        "V2 broker discrepancies are immutable; DELETE prohibited",
}

PERMS_0049 = {
    ("admin", "v2.broker.accounts.read", "SAL-2"),
    ("admin", "v2.broker.balances.read", "SAL-2"),
    ("admin", "v2.broker.positions.read", "SAL-2"),
    ("admin", "v2.broker.orders_fills.read", "SAL-2"),
    ("admin", "v2.broker.sync.run", "SAL-3"),
    ("admin", "v2.broker.discrepancy.manage", "SAL-3"),
    ("admin", "v2.broker.vault.manage", "SAL-4"),
}

BROKER_TABLES = (
    "v2_broker_account", "v2_broker_balance", "v2_broker_position",
    "v2_broker_order", "v2_broker_fill",
    "v2_broker_instrument_permission", "v2_broker_sync_run",
    "v2_broker_reconcile_run", "v2_broker_discrepancy",
)

REGIME = "'simulated','RESEARCH','t',NULL,'2026-09-05 00:00:00+00:00'"


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
    db_file = tmp_path / "be9.db"
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


def test_0049_tables_and_columns(tmp_path: Path) -> None:
    db_file, _ = _db(tmp_path, REV_0049)
    tables = {r[0] for r in _q(
        db_file, "SELECT name FROM sqlite_master WHERE type='table'")}
    for t in BROKER_TABLES:
        assert t in tables
    # N3 provenance pins present + NOT NULL on a projection table
    cols = {r[1]: r[3] for r in _q(
        db_file, "PRAGMA table_info(v2_broker_fill)")}
    for pin in ("provider_id", "sync_run_id", "server_hostname",
                "fetched_at_basis", "data_class"):
        assert pin in cols and cols[pin] == 1, f"{pin} not NOT NULL"
    rec_cols = [r[1] for r in _q(
        db_file, "PRAGMA table_info(v2_broker_reconcile_run)")]
    for c in ("broker_side_digest", "projection_side_digest",
              "compared_counts", "discrepancy_count", "outcome"):
        assert c in rec_cols


def test_0049_seeds_and_totals(tmp_path: Path) -> None:
    db_file, _ = _db(tmp_path, REV_0049)
    trigs = _v2_triggers(db_file)
    assert len(trigs) == 76          # T-17: 58 + 18
    assert set(TRIGGERS_0049) <= trigs
    perms = _q(db_file, "SELECT role, permission, sal FROM v2_permission")
    assert len(perms) == 64          # T-17: 57 + 7
    assert len({(r, p) for r, p, _ in perms}) == 64
    assert PERMS_0049 <= {tuple(r) for r in perms}
    compver = _q(db_file,
                 "SELECT component, version, length(source_hash)"
                 " FROM v2_computation_version")
    assert len(compver) == 11        # T-17: 10 + 1
    assert ("broker_read_engine", "bre-1.0.0", 64) in compver
    # append-only law: prior engine rows all present
    for row in (("replay_engine", "rpe-1.0.0", 64),
                ("research_job_engine", "rje-1.0.0", 64),
                ("paper_execution_simulator", "pxs-1.0.0", 64),
                ("paper_risk_gateway", "prg-1.0.0", 64)):
        assert row in compver


def test_0049_data_class_schema_impossible(tmp_path: Path) -> None:
    """T-6: any data_class other than 'simulated' refused at DB."""
    db_file, _ = _db(tmp_path, REV_0049)
    conn = sqlite3.connect(db_file)
    try:
        for banned in ("live", "historical_real", "synthetic"):
            with pytest.raises(sqlite3.IntegrityError):
                conn.execute(
                    "INSERT INTO v2_broker_fill (id, provider_id,"
                    " broker_account_ext_id, transaction_ext_id,"
                    " tx_type_ext, instrument_ext_id, units, price,"
                    " tx_time_ext, sync_run_id, server_hostname,"
                    " fetched_at_basis, data_class, mode, operator_id,"
                    " correlation_id, created_at)"
                    f" VALUES ('f-{banned}','p','a','t-{banned}','buy',"
                    f" 'EURUSD','1','1.1','x','s','h','b','{banned}',"
                    " 'RESEARCH','t',NULL,'2026-09-05 00:00:00+00:00')")
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(  # environment CHECK 'practice'
                "INSERT INTO v2_broker_account (id, provider_id,"
                " broker_account_ext_id, record_seq, supersedes, alias,"
                " currency, environment, read_only_login, sync_run_id,"
                " server_hostname, fetched_at_basis, data_class, mode,"
                " operator_id, correlation_id, created_at)"
                f" VALUES ('a-x','p','111',1,NULL,'x','USD','live',1,'s',"
                f" 'h','b',{REGIME})")
    finally:
        conn.close()


def test_0049_guard_messages_verbatim(tmp_path: Path) -> None:
    """T-9: all 18 guard messages byte-exact vs independent literals."""
    db_file, _ = _db(tmp_path, REV_0049)
    conn = sqlite3.connect(db_file)
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO v2_broker_account (id, provider_id,"
            " broker_account_ext_id, record_seq, supersedes, alias,"
            " currency, environment, read_only_login, sync_run_id,"
            " server_hostname, fetched_at_basis, data_class, mode,"
            " operator_id, correlation_id, created_at)"
            f" VALUES ('a1','p','111',1,NULL,'x','USD','practice',1,'s',"
            f" 'h','b',{REGIME})")
        cur.execute(
            "INSERT INTO v2_broker_balance (id, provider_id,"
            " broker_account_ext_id, balance, margin_used,"
            " margin_available, unrealized_pl, currency, sync_run_id,"
            " server_hostname, fetched_at_basis, data_class, mode,"
            " operator_id, correlation_id, created_at)"
            f" VALUES ('b1','p','111','1','0','1','0','USD','s','h','b',{REGIME})")
        cur.execute(
            "INSERT INTO v2_broker_position (id, provider_id,"
            " broker_account_ext_id, instrument_ext_id, units_long,"
            " units_short, avg_price_long, avg_price_short, sync_run_id,"
            " server_hostname, fetched_at_basis, data_class, mode,"
            " operator_id, correlation_id, created_at)"
            f" VALUES ('p1','p','111','EURUSD','1','0','1.1','0','s','h',"
            f" 'b',{REGIME})")
        cur.execute(
            "INSERT INTO v2_broker_order (id, provider_id, order_ext_id,"
            " broker_account_ext_id, order_state_ext, payload,"
            " sync_run_id, server_hostname, fetched_at_basis, data_class,"
            " mode, operator_id, correlation_id, created_at)"
            f" VALUES ('o1','p','ord-1','111','placed','{{}}','s','h','b',{REGIME})")
        cur.execute(
            "INSERT INTO v2_broker_fill (id, provider_id,"
            " broker_account_ext_id, transaction_ext_id, tx_type_ext,"
            " instrument_ext_id, units, price, tx_time_ext, sync_run_id,"
            " server_hostname, fetched_at_basis, data_class, mode,"
            " operator_id, correlation_id, created_at)"
            f" VALUES ('f1','p','111','tx-1','buy','EURUSD','1','1.1','x',"
            f" 's','h','b',{REGIME})")
        cur.execute(
            "INSERT INTO v2_broker_instrument_permission (id, provider_id,"
            " broker_account_ext_id, instrument_ext_id, visibility,"
            " display_name, sync_run_id, server_hostname,"
            " fetched_at_basis, data_class, mode, operator_id,"
            " correlation_id, created_at)"
            f" VALUES ('i1','p','111','EURUSD','{{}}','Euro','s','h','b',{REGIME})")
        cur.execute(
            "INSERT INTO v2_broker_sync_run (id, provider_id, scope,"
            " outcome, page_counts, origin_basis, inputs_hash,"
            " result_digest, refusal, actor_id, data_class, mode,"
            " operator_id, correlation_id, created_at)"
            f" VALUES ('s1','p','{{}}','complete','{{}}','o','h1','d1',NULL,"
            f" 't',{REGIME})")
        cur.execute(
            "INSERT INTO v2_broker_reconcile_run (id, provider_id,"
            " sync_run_id, compare_scope, broker_side_digest,"
            " projection_side_digest, compared_counts, discrepancy_count,"
            " outcome, actor_id, data_class, mode, operator_id,"
            " correlation_id, created_at)"
            f" VALUES ('r1','p','s1','{{}}','d1','d2','{{}}',0,'clean','t',{REGIME})")
        cur.execute(
            "INSERT INTO v2_broker_discrepancy (id, discrepancy_id,"
            " record_seq, supersedes, reconcile_run_id, discrepancy_class,"
            " state, broker_side, projection_side, owned_by,"
            " dismiss_reason, provider_id, data_class, mode, operator_id,"
            " correlation_id, created_at)"
            f" VALUES ('d1','disc-1',1,NULL,'r1','amount_mismatch',"
            f" 'detected','{{}}','{{}}',NULL,NULL,'p',{REGIME})")
        conn.commit()

        probes = (
            ("v2_broker_account", "a1"), ("v2_broker_balance", "b1"),
            ("v2_broker_position", "p1"), ("v2_broker_order", "o1"),
            ("v2_broker_fill", "f1"),
            ("v2_broker_instrument_permission", "i1"),
            ("v2_broker_sync_run", "s1"),
            ("v2_broker_reconcile_run", "r1"),
            ("v2_broker_discrepancy", "d1"),
        )
        for table, rid in probes:
            up_msg = TRIGGERS_0049[f"{table}_immutable_update"]
            del_msg = TRIGGERS_0049[f"{table}_immutable_delete"]
            with pytest.raises(sqlite3.IntegrityError) as e_up:
                cur.execute(
                    f"UPDATE {table} SET operator_id='x' WHERE id='{rid}'")
            assert up_msg in str(e_up.value)
            with pytest.raises(sqlite3.IntegrityError) as e_del:
                cur.execute(f"DELETE FROM {table} WHERE id='{rid}'")
            assert del_msg in str(e_del.value)
    finally:
        conn.close()


def test_0049_anchors_and_reason_iff(tmp_path: Path) -> None:
    db_file, _ = _db(tmp_path, REV_0049)
    conn = sqlite3.connect(db_file)
    try:
        cur = conn.cursor()

        def _fill(rid, tx):
            cur.execute(
                "INSERT INTO v2_broker_fill (id, provider_id,"
                " broker_account_ext_id, transaction_ext_id, tx_type_ext,"
                " instrument_ext_id, units, price, tx_time_ext,"
                " sync_run_id, server_hostname, fetched_at_basis,"
                " data_class, mode, operator_id, correlation_id,"
                " created_at)"
                f" VALUES ('{rid}','p','111','{tx}','buy','EURUSD','1',"
                f" '1.1','x','s','h','b',{REGIME})")

        _fill("f1", "tx-1")
        conn.commit()
        with pytest.raises(sqlite3.IntegrityError):
            _fill("f2", "tx-1")  # T-10 anchor: same provider/account/tx
        # discrepancy reason-iff CHECK both directions
        cur.execute(
            "INSERT INTO v2_broker_reconcile_run (id, provider_id,"
            " sync_run_id, compare_scope, broker_side_digest,"
            " projection_side_digest, compared_counts,"
            " discrepancy_count, outcome, actor_id, data_class, mode,"
            " operator_id, correlation_id, created_at)"
            f" VALUES ('r1','p','s1','{{}}','d1','d2','{{}}',0,'clean','t',{REGIME})")
        conn.commit()
        with pytest.raises(sqlite3.IntegrityError):
            cur.execute(  # dismissed WITHOUT reason
                "INSERT INTO v2_broker_discrepancy (id, discrepancy_id,"
                " record_seq, supersedes, reconcile_run_id,"
                " discrepancy_class, state, broker_side, projection_side,"
                " owned_by, dismiss_reason, provider_id, data_class,"
                " mode, operator_id, correlation_id, created_at)"
                f" VALUES ('d-x','disc-x',1,NULL,'r1','amount_mismatch',"
                f" 'dismissed_with_reason','{{}}','{{}}',NULL,NULL,'p',{REGIME})")
        with pytest.raises(sqlite3.IntegrityError):
            cur.execute(  # detected WITH a reason
                "INSERT INTO v2_broker_discrepancy (id, discrepancy_id,"
                " record_seq, supersedes, reconcile_run_id,"
                " discrepancy_class, state, broker_side, projection_side,"
                " owned_by, dismiss_reason, provider_id, data_class,"
                " mode, operator_id, correlation_id, created_at)"
                f" VALUES ('d-y','disc-y',1,NULL,'r1','amount_mismatch',"
                f" 'detected','{{}}','{{}}',NULL,'why','p',{REGIME})")
    finally:
        conn.close()


def test_0049_no_touch_protected_state(tmp_path: Path) -> None:
    """T-19: 0048-chain content byte-identical across 0049; trigger delta
    exactly the 18 names (content-based, PGF-012)."""
    db_file, db_url = _db(tmp_path, REV_0048)
    pre_perms = sorted(_q(db_file,
                          "SELECT role, permission, sal FROM v2_permission"))
    pre_comp = sorted(_q(db_file,
                         "SELECT component, version, source_hash"
                         " FROM v2_computation_version"))
    pre_trigs = _v2_triggers(db_file)
    result = _alembic(["upgrade", REV_0049], db_url)
    assert result.returncode == 0, result.stderr
    post_perms = sorted(_q(db_file,
                           "SELECT role, permission, sal FROM v2_permission"))
    post_comp = sorted(_q(db_file,
                          "SELECT component, version, source_hash"
                          " FROM v2_computation_version"))
    post_trigs = _v2_triggers(db_file)
    assert [p for p in post_perms
            if not p[1].startswith("v2.broker.")] == pre_perms
    assert [c for c in post_comp if c[0] != "broker_read_engine"] == pre_comp
    assert post_trigs - pre_trigs == set(TRIGGERS_0049)


def test_0049_downgrade_cycle_content_based(tmp_path: Path) -> None:
    db_file, db_url = _db(tmp_path, REV_0048)
    pre_perms = sorted(_q(db_file,
                          "SELECT role, permission, sal FROM v2_permission"))
    pre_comp = sorted(_q(db_file,
                         "SELECT component, version FROM"
                         " v2_computation_version"))
    result = _alembic(["upgrade", REV_0049], db_url)
    assert result.returncode == 0, result.stderr
    result = _alembic(["downgrade", REV_0048], db_url)
    assert result.returncode == 0, result.stderr
    tables = {r[0] for r in _q(
        db_file, "SELECT name FROM sqlite_master WHERE type='table'")}
    for t in BROKER_TABLES:
        assert t not in tables
    assert sorted(_q(db_file,
                     "SELECT role, permission, sal FROM v2_permission")) \
        == pre_perms
    assert sorted(_q(db_file,
                     "SELECT component, version FROM"
                     " v2_computation_version")) == pre_comp
    assert len(_v2_triggers(db_file)) == 58
    guard = _q(db_file,
               "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'"
               " AND name='v2_computation_version_immutable_delete'")
    assert guard[0][0] == 1


@pytest.mark.parametrize("rev", [REV_0048, REV_0049])
def test_drift_gate_0049(tmp_path: Path, rev: str) -> None:
    """T-18: format-independent (PGF-014); zero BE-9 tokens either form."""
    db_file, db_url = _db(tmp_path, rev)
    check = _alembic(["check"], db_url)
    drift = (check.stdout + check.stderr).lower()
    assert check.returncode != 0
    for marker in BROKER_TABLES:
        assert marker not in drift, f"BE-9 drift at {rev}: {marker}"
    if "not up to date" not in drift:
        assert "audit_write_failure_records" in drift
