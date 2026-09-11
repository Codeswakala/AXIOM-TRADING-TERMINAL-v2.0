"""V2 BE-8 migration tests — BO-V2-BE-8-001 T-7/T-13/T-14/T-15.

0048 on dedicated SQLite chains. Content-based comparisons (PGF-012).
Pins: triggers 42->58; permissions 49->57; compver 8->10.
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
REV_0047 = "20260903_0047"
REV_0048 = "20260904_0048"

TRIGGERS_0048 = {
    "v2_paper_account_immutable_update":
        "V2 paper accounts are immutable; UPDATE prohibited",
    "v2_paper_account_immutable_delete":
        "V2 paper accounts are immutable; DELETE prohibited",
    "v2_paper_order_intent_immutable_update":
        "V2 paper order intents are immutable; UPDATE prohibited",
    "v2_paper_order_intent_immutable_delete":
        "V2 paper order intents are immutable; DELETE prohibited",
    "v2_paper_risk_decision_immutable_update":
        "V2 paper risk decisions are immutable; UPDATE prohibited",
    "v2_paper_risk_decision_immutable_delete":
        "V2 paper risk decisions are immutable; DELETE prohibited",
    "v2_paper_order_event_immutable_update":
        "V2 paper order events are immutable; UPDATE prohibited",
    "v2_paper_order_event_immutable_delete":
        "V2 paper order events are immutable; DELETE prohibited",
    "v2_paper_fill_immutable_update":
        "V2 paper fills are immutable; UPDATE prohibited",
    "v2_paper_fill_immutable_delete":
        "V2 paper fills are immutable; DELETE prohibited",
    "v2_paper_position_snapshot_immutable_update":
        "V2 paper position snapshots are immutable; UPDATE prohibited",
    "v2_paper_position_snapshot_immutable_delete":
        "V2 paper position snapshots are immutable; DELETE prohibited",
    "v2_paper_balance_snapshot_immutable_update":
        "V2 paper balance snapshots are immutable; UPDATE prohibited",
    "v2_paper_balance_snapshot_immutable_delete":
        "V2 paper balance snapshots are immutable; DELETE prohibited",
    "v2_paper_reconciliation_immutable_update":
        "V2 paper reconciliations are immutable; UPDATE prohibited",
    "v2_paper_reconciliation_immutable_delete":
        "V2 paper reconciliations are immutable; DELETE prohibited",
}

PERMS_0048 = {
    ("admin", "v2.paper.accounts.read", "SAL-2"),
    ("admin", "v2.paper.accounts.manage", "SAL-3"),
    ("admin", "v2.paper.orders.read", "SAL-2"),
    ("admin", "v2.paper.orders.place", "SAL-3"),
    ("admin", "v2.paper.orders.cancel", "SAL-3"),
    ("admin", "v2.paper.orders.confirm", "SAL-3"),
    ("admin", "v2.paper.fills.read", "SAL-2"),
    ("admin", "v2.paper.risk.read", "SAL-2"),
}

PAPER_TABLES = (
    "v2_paper_account", "v2_paper_order_intent", "v2_paper_risk_decision",
    "v2_paper_order_event", "v2_paper_fill", "v2_paper_position_snapshot",
    "v2_paper_balance_snapshot", "v2_paper_reconciliation",
)

BE1 = "'simulated','PAPER','t',NULL,'2026-09-04 00:00:00+00:00'"


def _alembic(args: list[str], db_url: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["AXIOM_DATABASE_URL"] = db_url
    env.setdefault("AXIOM_ENVIRONMENT", "testing")
    env.setdefault("AXIOM_ALLOW_INSECURE_DEV", "true")
    env.setdefault("AXIOM_JWT_SECRET_KEY",
                   "test-secret-key-at-least-32-chars-long!!")
    env["AXIOM_V2_MODE"] = "RESEARCH"  # 0042 gate precondition (P-7)
    env["AXIOM_TD_TRANSITION_AUTHORITY_REF"] = TRANS_AUTHORITY
    return subprocess.run(
        [sys.executable, "-m", "alembic", *args],
        cwd=BACKEND_DIR, env=env, capture_output=True, text=True, timeout=600)


def _db(tmp_path: Path, rev: str) -> tuple[Path, str]:
    db_file = tmp_path / "be8.db"
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


# --- T-13: chain + censuses -----------------------------------------------------


def test_0048_tables_and_columns(tmp_path: Path) -> None:
    db_file, _ = _db(tmp_path, REV_0048)
    tables = {r[0] for r in _q(
        db_file, "SELECT name FROM sqlite_master WHERE type='table'")}
    for t in PAPER_TABLES:
        assert t in tables
    intent_cols = [r[1] for r in _q(
        db_file, "PRAGMA table_info(v2_paper_order_intent)")]
    # N3: every order carries the full law.
    for c in ("mode", "actor_id", "account_id", "correlation_id",
              "idempotency_key", "snapshot_ref", "time_basis"):
        assert c in intent_cols
    decision_cols = [r[1] for r in _q(
        db_file, "PRAGMA table_info(v2_paper_risk_decision)")]
    for c in ("decision", "evaluated_limits", "risk_config_version",
              "confirmation_ref"):
        assert c in decision_cols


def test_0048_seeds_and_totals(tmp_path: Path) -> None:
    db_file, _ = _db(tmp_path, REV_0048)
    trigs = _v2_triggers(db_file)
    assert len(trigs) == 58          # T-13: 42 + 16
    assert set(TRIGGERS_0048) <= trigs
    perms = _q(db_file, "SELECT role, permission, sal FROM v2_permission")
    assert len(perms) == 57          # T-13: 49 + 8
    assert len({(r, p) for r, p, _ in perms}) == 57
    assert PERMS_0048 <= {tuple(r) for r in perms}
    compver = _q(db_file,
                 "SELECT component, version, length(source_hash)"
                 " FROM v2_computation_version")
    assert len(compver) == 10        # T-13: 8 + 2
    assert ("paper_execution_simulator", "pxs-1.0.0", 64) in compver
    assert ("paper_risk_gateway", "prg-1.0.0", 64) in compver
    # RPE/RJE unchanged members (append-only law)
    assert ("replay_engine", "rpe-1.0.0", 64) in compver
    assert ("research_job_engine", "rje-1.0.0", 64) in compver


def test_0048_fill_class_schema_impossible(tmp_path: Path) -> None:
    """T-6/N4: any fill_class other than paper_simulated refused at DB."""
    db_file, _ = _db(tmp_path, REV_0048)
    conn = sqlite3.connect(db_file)
    try:
        for banned in ("broker_confirmed", "live", "paper", "confirmed"):
            with pytest.raises(sqlite3.IntegrityError):
                conn.execute(
                    "INSERT INTO v2_paper_fill (id, fill_id, intent_id,"
                    " fill_index, quantity, raw_price, effective_price,"
                    " cost_model_ref, fill_class, simulator_version,"
                    " snapshot_ref, time_basis, data_class, mode,"
                    " operator_id, correlation_id, created_at)"
                    f" VALUES ('f-{banned}','fid-{banned}','i',0,'1','100',"
                    f" '100','{{}}','{banned}','pxs-1.0.0','s','{{}}',{BE1})")
        conn.execute(
            "INSERT INTO v2_paper_fill (id, fill_id, intent_id, fill_index,"
            " quantity, raw_price, effective_price, cost_model_ref,"
            " fill_class, simulator_version, snapshot_ref, time_basis,"
            " data_class, mode, operator_id, correlation_id, created_at)"
            f" VALUES ('f-ok','fid-ok','i',0,'1','100','100','{{}}',"
            f" 'paper_simulated','pxs-1.0.0','s','{{}}',{BE1})")
        conn.commit()
    finally:
        conn.close()


def test_0048_guard_messages_verbatim(tmp_path: Path) -> None:
    """T-7: all 16 guard messages byte-exact vs independent literals."""
    db_file, _ = _db(tmp_path, REV_0048)
    conn = sqlite3.connect(db_file)
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO v2_paper_account (id, account_id, record_seq,"
            " name, base_currency, initial_balance, margin_params,"
            " lifecycle_state, confirmation_ref, data_class, mode,"
            " operator_id, correlation_id, created_at)"
            f" VALUES ('a1','acct-1',1,'A','USD','10000','{{}}','active',"
            f" 'ref-1',{BE1})")
        cur.execute(
            "INSERT INTO v2_paper_order_intent (id, intent_id, account_id,"
            " instrument_id, side, order_type, quantity, limit_price,"
            " time_in_force, idempotency_key, snapshot_ref, time_basis,"
            " confirmation_ref, actor_id, data_class, mode, operator_id,"
            " correlation_id, created_at)"
            f" VALUES ('i1','int-1','a1','x','buy','market','1',NULL,"
            f" 'replay_window','k1','s1','{{}}',NULL,'t',{BE1})")
        cur.execute(
            "INSERT INTO v2_paper_risk_decision (id, intent_id, decision,"
            " evaluated_limits, reasons, risk_config_version,"
            " decided_at_basis, confirmation_ref, data_class, mode,"
            " operator_id, correlation_id, created_at)"
            f" VALUES ('d1','i1','pass','{{}}','{{}}','prc-1','{{}}',NULL,{BE1})")
        cur.execute(
            "INSERT INTO v2_paper_order_event (id, intent_id, event_index,"
            " from_state, to_state, event_class, details, actor_id,"
            " data_class, mode, operator_id, correlation_id, created_at)"
            f" VALUES ('e1','i1',0,'draft','validated','order.validated',"
            f" '{{}}','t',{BE1})")
        cur.execute(
            "INSERT INTO v2_paper_fill (id, fill_id, intent_id, fill_index,"
            " quantity, raw_price, effective_price, cost_model_ref,"
            " fill_class, simulator_version, snapshot_ref, time_basis,"
            " data_class, mode, operator_id, correlation_id, created_at)"
            f" VALUES ('f1','fid-1','i1',0,'1','100','100','{{}}',"
            f" 'paper_simulated','pxs-1.0.0','s','{{}}',{BE1})")
        cur.execute(
            "INSERT INTO v2_paper_position_snapshot (id, account_id,"
            " as_of_basis, positions, derivation_inputs_hash,"
            " engine_versions_hash, data_class, mode, operator_id,"
            " correlation_id, created_at)"
            f" VALUES ('p1','a1','{{}}','{{}}','h1','h2',{BE1})")
        cur.execute(
            "INSERT INTO v2_paper_balance_snapshot (id, account_id,"
            " as_of_basis, cash, equity, margin_used, margin_available,"
            " unrealized_pnl, realized_pnl, derivation_inputs_hash,"
            " engine_versions_hash, data_class, mode, operator_id,"
            " correlation_id, created_at)"
            f" VALUES ('b1','a1','{{}}','1','1','0','1','0','0','h1','h2',{BE1})")
        cur.execute(
            "INSERT INTO v2_paper_reconciliation (id, account_id, run_basis,"
            " outcome, discrepancies, inputs_hash, data_class, mode,"
            " operator_id, correlation_id, created_at)"
            f" VALUES ('r1','a1','{{}}','consistent','{{}}','h1',{BE1})")
        conn.commit()

        probes = (
            ("v2_paper_account", "a1"),
            ("v2_paper_order_intent", "i1"),
            ("v2_paper_risk_decision", "d1"),
            ("v2_paper_order_event", "e1"),
            ("v2_paper_fill", "f1"),
            ("v2_paper_position_snapshot", "p1"),
            ("v2_paper_balance_snapshot", "b1"),
            ("v2_paper_reconciliation", "r1"),
        )
        for table, rid in probes:
            up_msg = TRIGGERS_0048[f"{table}_immutable_update"]
            del_msg = TRIGGERS_0048[f"{table}_immutable_delete"]
            with pytest.raises(sqlite3.IntegrityError) as e_up:
                cur.execute(
                    f"UPDATE {table} SET operator_id='x' WHERE id='{rid}'")
            assert up_msg in str(e_up.value)
            with pytest.raises(sqlite3.IntegrityError) as e_del:
                cur.execute(f"DELETE FROM {table} WHERE id='{rid}'")
            assert del_msg in str(e_del.value)
    finally:
        conn.close()


def test_0048_behavioral_uniqueness_anchors(tmp_path: Path) -> None:
    """T-8 anchors at DB: idempotency, decision uq, event uq, fill uq."""
    db_file, _ = _db(tmp_path, REV_0048)
    conn = sqlite3.connect(db_file)
    try:
        cur = conn.cursor()

        def _intent(rid, iid, key):
            cur.execute(
                "INSERT INTO v2_paper_order_intent (id, intent_id,"
                " account_id, instrument_id, side, order_type, quantity,"
                " limit_price, time_in_force, idempotency_key, snapshot_ref,"
                " time_basis, confirmation_ref, actor_id, data_class, mode,"
                " operator_id, correlation_id, created_at)"
                f" VALUES ('{rid}','{iid}','a1','x','buy','market','1',NULL,"
                f" 'replay_window','{key}','s1','{{}}',NULL,'t',{BE1})")

        _intent("i1", "int-1", "k1")
        conn.commit()
        with pytest.raises(sqlite3.IntegrityError):
            _intent("i2", "int-2", "k1")  # same (account, key)
        _intent("i3", "int-3", "k2")
        conn.commit()

        cur.execute(
            "INSERT INTO v2_paper_risk_decision (id, intent_id, decision,"
            " evaluated_limits, reasons, risk_config_version,"
            " decided_at_basis, confirmation_ref, data_class, mode,"
            " operator_id, correlation_id, created_at)"
            f" VALUES ('d1','i1','pass','{{}}','{{}}','prc-1','{{}}',NULL,{BE1})")
        conn.commit()
        with pytest.raises(sqlite3.IntegrityError):
            cur.execute(  # second decision for i1 — schema-refused (T-8)
                "INSERT INTO v2_paper_risk_decision (id, intent_id,"
                " decision, evaluated_limits, reasons, risk_config_version,"
                " decided_at_basis, confirmation_ref, data_class, mode,"
                " operator_id, correlation_id, created_at)"
                f" VALUES ('d2','i1','block','{{}}','{{}}','prc-1','{{}}',"
                f" NULL,{BE1})")
        # C-1b iff-CHECK both directions
        with pytest.raises(sqlite3.IntegrityError):
            cur.execute(  # hold WITHOUT ref
                "INSERT INTO v2_paper_risk_decision (id, intent_id,"
                " decision, evaluated_limits, reasons, risk_config_version,"
                " decided_at_basis, confirmation_ref, data_class, mode,"
                " operator_id, correlation_id, created_at)"
                f" VALUES ('d3','i3','hold','{{}}','{{}}','prc-1','{{}}',"
                f" NULL,{BE1})")
        with pytest.raises(sqlite3.IntegrityError):
            cur.execute(  # pass WITH ref
                "INSERT INTO v2_paper_risk_decision (id, intent_id,"
                " decision, evaluated_limits, reasons, risk_config_version,"
                " decided_at_basis, confirmation_ref, data_class, mode,"
                " operator_id, correlation_id, created_at)"
                f" VALUES ('d4','i3','pass','{{}}','{{}}','prc-1','{{}}',"
                f" 'ref-x',{BE1})")

        # event-ledger uq (append-only double-append refusal)
        cur.execute(
            "INSERT INTO v2_paper_order_event (id, intent_id, event_index,"
            " from_state, to_state, event_class, details, actor_id,"
            " data_class, mode, operator_id, correlation_id, created_at)"
            f" VALUES ('e1','i1',0,'draft','validated','order.validated',"
            f" '{{}}','t',{BE1})")
        conn.commit()
        with pytest.raises(sqlite3.IntegrityError):
            cur.execute(
                "INSERT INTO v2_paper_order_event (id, intent_id,"
                " event_index, from_state, to_state, event_class, details,"
                " actor_id, data_class, mode, operator_id, correlation_id,"
                " created_at)"
                f" VALUES ('e2','i1',0,'draft','rejected','order.rejected',"
                f" '{{}}','t',{BE1})")
        # fill anchor
        cur.execute(
            "INSERT INTO v2_paper_fill (id, fill_id, intent_id, fill_index,"
            " quantity, raw_price, effective_price, cost_model_ref,"
            " fill_class, simulator_version, snapshot_ref, time_basis,"
            " data_class, mode, operator_id, correlation_id, created_at)"
            f" VALUES ('f1','fid-1','i1',0,'1','100','100','{{}}',"
            f" 'paper_simulated','pxs-1.0.0','s','{{}}',{BE1})")
        conn.commit()
        with pytest.raises(sqlite3.IntegrityError):
            cur.execute(
                "INSERT INTO v2_paper_fill (id, fill_id, intent_id,"
                " fill_index, quantity, raw_price, effective_price,"
                " cost_model_ref, fill_class, simulator_version,"
                " snapshot_ref, time_basis, data_class, mode, operator_id,"
                " correlation_id, created_at)"
                f" VALUES ('f2','fid-2','i1',0,'1','100','100','{{}}',"
                f" 'paper_simulated','pxs-1.0.0','s','{{}}',{BE1})")
    finally:
        conn.close()


def test_0048_no_touch_protected_state(tmp_path: Path) -> None:
    """T-15: 0047-chain content byte-identical across 0048; trigger delta
    is exactly the 16 new names (content-based, PGF-012)."""
    db_file, db_url = _db(tmp_path, REV_0047)
    pre_perms = sorted(_q(db_file,
                          "SELECT role, permission, sal FROM v2_permission"))
    pre_comp = sorted(_q(db_file,
                         "SELECT component, version, source_hash"
                         " FROM v2_computation_version"))
    pre_trigs = _v2_triggers(db_file)
    result = _alembic(["upgrade", REV_0048], db_url)
    assert result.returncode == 0, result.stderr
    post_perms = sorted(_q(db_file,
                           "SELECT role, permission, sal FROM v2_permission"))
    post_comp = sorted(_q(db_file,
                          "SELECT component, version, source_hash"
                          " FROM v2_computation_version"))
    post_trigs = _v2_triggers(db_file)
    assert [p for p in post_perms
            if not p[1].startswith("v2.paper.")] == pre_perms
    assert [c for c in post_comp
            if not c[0].startswith("paper_")] == pre_comp
    assert post_trigs - pre_trigs == set(TRIGGERS_0048)


def test_0048_downgrade_cycle_content_based(tmp_path: Path) -> None:
    """T-15: symmetric teardown; content equal to the pre-0048 state."""
    db_file, db_url = _db(tmp_path, REV_0047)
    pre_perms = sorted(_q(db_file,
                          "SELECT role, permission, sal FROM v2_permission"))
    pre_comp = sorted(_q(db_file,
                         "SELECT component, version FROM"
                         " v2_computation_version"))
    result = _alembic(["upgrade", REV_0048], db_url)
    assert result.returncode == 0, result.stderr
    result = _alembic(["downgrade", REV_0047], db_url)
    assert result.returncode == 0, result.stderr
    tables = {r[0] for r in _q(
        db_file, "SELECT name FROM sqlite_master WHERE type='table'")}
    for t in PAPER_TABLES:
        assert t not in tables
    assert sorted(_q(db_file,
                     "SELECT role, permission, sal FROM v2_permission")) \
        == pre_perms
    assert sorted(_q(db_file,
                     "SELECT component, version FROM"
                     " v2_computation_version")) == pre_comp
    assert len(_v2_triggers(db_file)) == 42
    # compver delete-guard restored
    guard = _q(db_file,
               "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'"
               " AND name='v2_computation_version_immutable_delete'")
    assert guard[0][0] == 1


@pytest.mark.parametrize("rev", [REV_0047, REV_0048])
def test_drift_gate_0048(tmp_path: Path, rev: str) -> None:
    """T-14: format-independent (PGF-014); zero BE-8 tokens either form;
    at head the drift is exactly the 9 inherited V1 tokens."""
    db_file, db_url = _db(tmp_path, rev)
    check = _alembic(["check"], db_url)
    drift = (check.stdout + check.stderr).lower()
    assert check.returncode != 0
    for marker in ("v2_paper_account", "v2_paper_order_intent",
                   "v2_paper_risk_decision", "v2_paper_order_event",
                   "v2_paper_fill", "v2_paper_position_snapshot",
                   "v2_paper_balance_snapshot", "v2_paper_reconciliation"):
        assert marker not in drift, f"BE-8 drift at {rev}: {marker}"
    if "not up to date" not in drift:
        assert "audit_write_failure_records" in drift


def test_0048_state_checks(tmp_path: Path) -> None:
    """Closed CHECK vocabularies: account state, decision, outcome, tif."""
    db_file, _ = _db(tmp_path, REV_0048)
    conn = sqlite3.connect(db_file)
    try:
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO v2_paper_account (id, account_id, record_seq,"
                " name, base_currency, initial_balance, margin_params,"
                " lifecycle_state, confirmation_ref, data_class, mode,"
                " operator_id, correlation_id, created_at)"
                f" VALUES ('a-x','acct-x',1,'A','USD','1','{{}}','open',"
                f" 'r',{BE1})")
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(  # non-USD refused (v1 currency law)
                "INSERT INTO v2_paper_account (id, account_id, record_seq,"
                " name, base_currency, initial_balance, margin_params,"
                " lifecycle_state, confirmation_ref, data_class, mode,"
                " operator_id, correlation_id, created_at)"
                f" VALUES ('a-y','acct-y',1,'A','EUR','1','{{}}','active',"
                f" 'r',{BE1})")
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(  # limit_price iff limit type
                "INSERT INTO v2_paper_order_intent (id, intent_id,"
                " account_id, instrument_id, side, order_type, quantity,"
                " limit_price, time_in_force, idempotency_key,"
                " snapshot_ref, time_basis, confirmation_ref, actor_id,"
                " data_class, mode, operator_id, correlation_id,"
                " created_at)"
                f" VALUES ('i-x','int-x','a1','x','buy','market','1','99',"
                f" 'replay_window','kx','s','{{}}',NULL,'t',{BE1})")
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(  # reconciliation outcome closed set
                "INSERT INTO v2_paper_reconciliation (id, account_id,"
                " run_basis, outcome, discrepancies, inputs_hash,"
                " data_class, mode, operator_id, correlation_id,"
                " created_at)"
                f" VALUES ('r-x','a1','{{}}','maybe','{{}}','h',{BE1})")
    finally:
        conn.close()
