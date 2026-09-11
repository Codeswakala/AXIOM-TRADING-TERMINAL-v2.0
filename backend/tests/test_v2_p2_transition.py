"""V2 BE-3 P2 status-transition tests — BO-V2-BE-3-P2-TRANS-001 (b).

Full plan Part 8 matrix: precondition matrix (durable refusal audits, zero
side effects), happy path, idempotence (TR-001 pinned no-op), post-transition
immutability, downgrade reversal-append, P-5 re-upgrade refusal, refusal-audit
fallback (TR-003), interruption/consistency detection, and regression.

All tests run migrations on dedicated file-based SQLite databases via the
alembic CLI (fresh chain per test as needed). No network, no credential,
no runtime source involvement (the migration is the only subject).
"""

from __future__ import annotations

import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

BACKEND_DIR = Path(__file__).resolve().parents[1]
MIGRATION = BACKEND_DIR / "alembic" / "versions" / "20260829_0042_v2_be3_p2_transition.py"
AUTHORITY = "BO-V2-BE-3-P2-TRANS-001"
P1_REV = "20260825_0041"
TRANS_REV = "20260829_0042"

SQLITE_UPDATE_MSG = "V2 provider registry is immutable in P1; UPDATE prohibited"
SQLITE_DELETE_MSG = "V2 provider registry is immutable in P1; DELETE prohibited"


def _alembic(args: list[str], db_url: str, *, authority: str | None = None,
             extra_env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["AXIOM_DATABASE_URL"] = db_url
    env.setdefault("AXIOM_ENVIRONMENT", "testing")
    env.setdefault("AXIOM_ALLOW_INSECURE_DEV", "true")
    env.setdefault("AXIOM_JWT_SECRET_KEY", "test-secret-key-at-least-32-chars-long!!")
    env.setdefault("AXIOM_V2_MODE", "RESEARCH")
    env.pop("AXIOM_TD_TRANSITION_AUTHORITY_REF", None)
    if authority is not None:
        env["AXIOM_TD_TRANSITION_AUTHORITY_REF"] = authority
    if extra_env:
        env.update(extra_env)
    return subprocess.run(
        [sys.executable, "-m", "alembic", *args],
        cwd=BACKEND_DIR, env=env, capture_output=True, text=True, timeout=600,
    )


def _prepare_p1_db(tmp_path: Path, name: str = "trans.db") -> tuple[Path, str]:
    """Fresh chain to the P2 head (0041): verified entitlement, genesis history."""
    db_file = tmp_path / name
    db_url = f"sqlite+aiosqlite:///{db_file}"
    result = _alembic(["upgrade", P1_REV], db_url)
    assert result.returncode == 0, result.stderr
    return db_file, db_url


def _q(db_file: Path, sql: str, params: tuple = ()):
    conn = sqlite3.connect(db_file)
    try:
        return conn.execute(sql, params).fetchall()
    finally:
        conn.close()


def _provider_state(db_file: Path):
    return _q(
        db_file,
        "SELECT source_status, entitlement_status, persistence_permitted"
        " FROM v2_md_provider WHERE provider_id='twelvedata'",
    )[0]


def _history_rows(db_file: Path):
    return _q(
        db_file,
        "SELECT from_status, to_status, authority_ref, evidence_ref"
        " FROM v2_md_provider_status_history WHERE provider_id='twelvedata'"
        " ORDER BY created_at",
    )


def _audit_actions(db_file: Path):
    return [r[0] for r in _q(
        db_file,
        "SELECT action FROM v2_audit_event"
        " WHERE action LIKE 'provider.status_transition%' ORDER BY created_at",
    )]


def _exec_sql(db_file: Path, sql: str):
    conn = sqlite3.connect(db_file)
    try:
        conn.execute(sql)
        conn.commit()
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------


def test_happy_path_transition(tmp_path: Path) -> None:
    db_file, db_url = _prepare_p1_db(tmp_path)
    result = _alembic(["upgrade", TRANS_REV], db_url, authority=AUTHORITY)
    assert result.returncode == 0, result.stderr

    status, ent, persist = _provider_state(db_file)
    assert status == "contract_tested"
    assert ent == "verified"          # entitlement unchanged
    assert persist == 0               # persistence still false

    history = _history_rows(db_file)
    assert len(history) == 2
    genesis, transition = history
    assert genesis[1] == "architecture_candidate"
    assert transition[0] == "architecture_candidate"
    assert transition[1] == "contract_tested"
    assert transition[2] == AUTHORITY
    assert "ITRGA-DET-V2-BE-3-P2-FINAL-001" in transition[3]
    assert "a246607c-f0c5-42e9-8f3b-a1e1bd75fa83" in transition[3]

    actions = _audit_actions(db_file)
    assert actions == [
        "provider.status_transition.start",
        "provider.status_transition.complete",
    ]

    # invariants: reserved authority still inactive; no other provider touched
    active = _q(db_file, "SELECT active FROM v2_md_source WHERE source_id='twelvedata'")[0][0]
    assert active == 0


# ---------------------------------------------------------------------------
# Precondition matrix — each failure: refusal audit + zero side effects
# ---------------------------------------------------------------------------


def _assert_refused(
    db_file: Path, result, precondition: str,
    expected_status: str = "architecture_candidate",
) -> None:
    assert result.returncode != 0
    assert f"precondition {precondition} failed" in (result.stdout + result.stderr)
    # zero side effects (status unchanged from the pre-run fixture value)
    status, _, _ = _provider_state(db_file)
    assert status == expected_status
    assert len(_history_rows(db_file)) == 1
    # durable refusal audit exists (independent connection survived rollback)
    refusals = _q(
        db_file,
        "SELECT details FROM v2_audit_event"
        " WHERE action='provider.status_transition.refused'",
    )
    assert refusals, "refusal audit row missing"
    assert precondition in refusals[-1][0]


def test_p1_authority_ref_missing_refused(tmp_path: Path) -> None:
    db_file, db_url = _prepare_p1_db(tmp_path)
    result = _alembic(["upgrade", TRANS_REV], db_url, authority=None)
    _assert_refused(db_file, result, "P-1:authority_ref")


def test_p1_authority_ref_wrong_refused(tmp_path: Path) -> None:
    db_file, db_url = _prepare_p1_db(tmp_path)
    result = _alembic(["upgrade", TRANS_REV], db_url, authority="WRONG-REF")
    _assert_refused(db_file, result, "P-1:authority_ref")


def test_p2_other_status_refused(tmp_path: Path) -> None:
    """P-2 refuse branch (TRD-002): a third source_status value — neither
    FROM (proceed) nor TO (no-op) — must refuse, not proceed and not no-op."""
    db_file, db_url = _prepare_p1_db(tmp_path)
    # simulate a foreign status value (guard dropped only for test setup)
    _exec_sql(db_file, "DROP TRIGGER v2_md_provider_immutable_update")
    _exec_sql(db_file, "UPDATE v2_md_provider SET source_status='integrated'"
                        " WHERE provider_id='twelvedata'")
    result = _alembic(["upgrade", TRANS_REV], db_url, authority=AUTHORITY)
    _assert_refused(db_file, result, "P-2:source_status",
                    expected_status="integrated")


def test_p3_unverified_entitlement_refused(tmp_path: Path) -> None:
    db_file, db_url = _prepare_p1_db(tmp_path)
    # simulate unverified entitlement (guard dropped only for test setup)
    _exec_sql(db_file, "DROP TRIGGER v2_md_provider_immutable_update")
    _exec_sql(db_file, "UPDATE v2_md_provider SET entitlement_status='unverified'"
                        " WHERE provider_id='twelvedata'")
    result = _alembic(["upgrade", TRANS_REV], db_url, authority=AUTHORITY)
    assert result.returncode != 0
    assert "P-3:entitlement_status" in (result.stdout + result.stderr)
    assert len(_history_rows(db_file)) == 1


def test_p4_persistence_permitted_refused(tmp_path: Path) -> None:
    """P-4 (TRD-002): persistence_permitted = true must refuse — the
    transition never grants or tolerates persistence."""
    db_file, db_url = _prepare_p1_db(tmp_path)
    _exec_sql(db_file, "DROP TRIGGER v2_md_provider_immutable_update")
    _exec_sql(db_file, "UPDATE v2_md_provider SET persistence_permitted=1"
                        " WHERE provider_id='twelvedata'")
    result = _alembic(["upgrade", TRANS_REV], db_url, authority=AUTHORITY)
    _assert_refused(db_file, result, "P-4:persistence_permitted")
    # the flag itself is untouched by the refusal
    _, _, persist = _provider_state(db_file)
    assert persist == 1


def test_p5_history_count_refused(tmp_path: Path) -> None:
    db_file, db_url = _prepare_p1_db(tmp_path)
    _exec_sql(
        db_file,
        "INSERT INTO v2_md_provider_status_history"
        " (id, provider_id, from_status, to_status, authority_ref, created_at)"
        " VALUES ('extra', 'twelvedata', NULL, 'architecture_candidate',"
        " 'test-fixture', '2026-08-29 00:00:00+00:00')",
    )
    result = _alembic(["upgrade", TRANS_REV], db_url, authority=AUTHORITY)
    _assert_refused_partial = result.returncode != 0
    assert _assert_refused_partial
    assert "P-5:history_count" in (result.stdout + result.stderr)
    status, _, _ = _provider_state(db_file)
    assert status == "architecture_candidate"


def test_p7_invalid_mode_refused(tmp_path: Path) -> None:
    db_file, db_url = _prepare_p1_db(tmp_path)
    result = _alembic(
        ["upgrade", TRANS_REV], db_url, authority=AUTHORITY,
        extra_env={"AXIOM_V2_MODE": "LIVE"},
    )
    _assert_refused(db_file, result, "P-7:mode")


def test_p8_active_reserved_authority_refused(tmp_path: Path) -> None:
    db_file, db_url = _prepare_p1_db(tmp_path)
    # activate the reserved source (allowed vocabulary: authority stays 'unknown')
    _exec_sql(db_file, "UPDATE v2_md_source SET active=1 WHERE source_id='twelvedata'")
    result = _alembic(["upgrade", TRANS_REV], db_url, authority=AUTHORITY)
    _assert_refused(db_file, result, "P-8:reserved_authority_active")


# ---------------------------------------------------------------------------
# Idempotence (TR-001 pinned no-op)
# ---------------------------------------------------------------------------


def test_rerun_is_clean_audited_no_op(tmp_path: Path) -> None:
    db_file, db_url = _prepare_p1_db(tmp_path)
    assert _alembic(["upgrade", TRANS_REV], db_url, authority=AUTHORITY).returncode == 0

    # roll the version back WITHOUT reversing state, then re-run upgrade:
    # simulates re-application on an already-transitioned database
    _exec_sql(db_file, f"UPDATE alembic_version SET version_num='{P1_REV}'")
    rerun = _alembic(["upgrade", TRANS_REV], db_url, authority=AUTHORITY)
    assert rerun.returncode == 0  # exit 0 — not a refusal

    # still exactly one transition row
    assert len(_history_rows(db_file)) == 2
    actions = _audit_actions(db_file)
    # first run: start+complete; rerun: start+complete with no_op marker
    assert actions.count("provider.status_transition.start") == 2
    assert actions.count("provider.status_transition.complete") == 2
    assert "provider.status_transition.refused" not in actions
    noop_details = _q(
        db_file,
        "SELECT details FROM v2_audit_event"
        " WHERE action='provider.status_transition.start'"
        " ORDER BY created_at DESC LIMIT 1",
    )[0][0]
    assert json.loads(noop_details)["no_op"] == "already-applied"


# ---------------------------------------------------------------------------
# Post-transition immutability (exact dialect messages)
# ---------------------------------------------------------------------------


def test_post_transition_immutability(tmp_path: Path) -> None:
    db_file, db_url = _prepare_p1_db(tmp_path)
    assert _alembic(["upgrade", TRANS_REV], db_url, authority=AUTHORITY).returncode == 0

    conn = sqlite3.connect(db_file)
    try:
        cur = conn.cursor()
        # seed another-provider fixture row (guard blocks INSERT? No — guard is
        # UPDATE/DELETE only; INSERT allowed for fixture)
        cur.execute(
            "INSERT INTO v2_md_provider (id, provider_id, display_name, markets,"
            " entitlement_status, persistence_permitted, source_status, created_at)"
            " VALUES ('fx1', 'otherprov', 'Other', '[]', 'unverified', 0,"
            " 'architecture_candidate', '2026-08-29 00:00:00+00:00')"
        )
        conn.commit()

        for sql in (
            "UPDATE v2_md_provider SET source_status='integrated' WHERE provider_id='twelvedata'",
            "UPDATE v2_md_provider SET entitlement_status='expired' WHERE provider_id='twelvedata'",
            "UPDATE v2_md_provider SET persistence_permitted=1 WHERE provider_id='twelvedata'",
            "UPDATE v2_md_provider SET display_name='x' WHERE provider_id='otherprov'",
        ):
            with pytest.raises(sqlite3.DatabaseError, match=SQLITE_UPDATE_MSG):
                cur.execute(sql)
        for sql in (
            "DELETE FROM v2_md_provider WHERE provider_id='twelvedata'",
            "DELETE FROM v2_md_provider WHERE provider_id='otherprov'",
        ):
            with pytest.raises(sqlite3.DatabaseError, match=SQLITE_DELETE_MSG):
                cur.execute(sql)
        # history triggers intact (never dropped by 0042)
        with pytest.raises(sqlite3.DatabaseError, match="immutable"):
            cur.execute(
                "UPDATE v2_md_provider_status_history SET to_status='integrated'"
            )
        with pytest.raises(sqlite3.DatabaseError, match="immutable"):
            cur.execute("DELETE FROM v2_md_provider_status_history")
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Downgrade (reversal append) + P-5 re-upgrade refusal
# ---------------------------------------------------------------------------


def test_downgrade_reversal_and_p5_reupgrade_refusal(tmp_path: Path) -> None:
    db_file, db_url = _prepare_p1_db(tmp_path)
    assert _alembic(["upgrade", TRANS_REV], db_url, authority=AUTHORITY).returncode == 0

    down = _alembic(["downgrade", P1_REV], db_url)  # no authority required
    assert down.returncode == 0, down.stderr

    status, _, _ = _provider_state(db_file)
    assert status == "architecture_candidate"
    history = _history_rows(db_file)
    assert len(history) == 3  # genesis + transition + reversal (never deleted)
    reversal = history[2]
    assert reversal[0] == "contract_tested"
    assert reversal[1] == "architecture_candidate"
    assert "provider.status_transition.downgraded" in _audit_actions(db_file)

    # immutability re-proven post-downgrade
    with pytest.raises(sqlite3.DatabaseError, match=SQLITE_UPDATE_MSG):
        _exec_sql(
            db_file,
            "UPDATE v2_md_provider SET source_status='contract_tested'"
            " WHERE provider_id='twelvedata'",
        )

    # re-upgrade attempt (authority STILL SET) → documented P-5 refusal
    reup = _alembic(["upgrade", TRANS_REV], db_url, authority=AUTHORITY)
    assert reup.returncode != 0
    assert "P-5:history_count" in (reup.stdout + reup.stderr)
    refusals = _q(
        db_file,
        "SELECT details FROM v2_audit_event"
        " WHERE action='provider.status_transition.refused'",
    )
    assert refusals and "P-5:history_count" in refusals[-1][0]


def test_downgrade_refuses_over_guard_absent_state(tmp_path: Path) -> None:
    """TRD-001: an interrupted prior downgrade (guard dropped, status
    reverted, reversal append missing — SQLite per-statement DDL) must NOT
    be maskable by a re-run: the early return is preceded by
    _verify_guard_present, so the re-run raises 'NOT restored' loudly."""
    db_file, db_url = _prepare_p1_db(tmp_path)
    assert _alembic(["upgrade", TRANS_REV], db_url, authority=AUTHORITY).returncode == 0

    # fault injection — manufacture the interrupted-downgrade state:
    # guard absent, status reverted, history still 2, version still 0042
    _exec_sql(db_file, "DROP TRIGGER v2_md_provider_immutable_update")
    _exec_sql(db_file, "DROP TRIGGER v2_md_provider_immutable_delete")
    _exec_sql(db_file, "UPDATE v2_md_provider SET source_status='architecture_candidate'"
                        " WHERE provider_id='twelvedata'")
    assert len(_history_rows(db_file)) == 2
    assert _q(db_file, "SELECT version_num FROM alembic_version")[0][0] == TRANS_REV

    rerun = _alembic(["downgrade", P1_REV], db_url)
    assert rerun.returncode != 0  # NOT a silent exit-0 completion
    assert "NOT restored" in (rerun.stdout + rerun.stderr)
    # nothing further mutated by the refused re-run
    assert len(_history_rows(db_file)) == 2
    status, _, _ = _provider_state(db_file)
    assert status == "architecture_candidate"


# ---------------------------------------------------------------------------
# TR-003 refusal-audit fallback + consistency detection
# ---------------------------------------------------------------------------


def test_refusal_audit_fallback_distinct_error(tmp_path: Path) -> None:
    """If the refusal-audit insert cannot succeed, the migration raises the
    distinct TR-003 error preserving the precondition name. Simulated by
    dropping the audit table so the independent insert must fail."""
    db_file, db_url = _prepare_p1_db(tmp_path)
    _exec_sql(db_file, "ALTER TABLE v2_audit_event RENAME TO v2_audit_event_hidden")
    result = _alembic(["upgrade", TRANS_REV], db_url, authority=None)  # P-1 fails
    assert result.returncode != 0
    output = result.stdout + result.stderr
    assert "REFUSAL AUDIT WRITE FAILED: P-1:authority_ref" in output
    # zero side effects
    assert len(_history_rows(db_file)) == 1


def test_consistency_check_detects_partial_state(tmp_path: Path) -> None:
    """_verify_transition_consistent raises on status/history mismatch."""
    db_file, db_url = _prepare_p1_db(tmp_path)
    assert _alembic(["upgrade", TRANS_REV], db_url, authority=AUTHORITY).returncode == 0

    # manufacture inconsistency: status transitioned but history forced to 1
    conn = sqlite3.connect(db_file)
    conn.execute("DROP TRIGGER v2_md_provider_hist_immutable_delete")
    conn.execute(
        "DELETE FROM v2_md_provider_status_history WHERE from_status IS NOT NULL"
    )
    conn.commit()
    conn.close()

    import importlib.util

    spec = importlib.util.spec_from_file_location("transmig", MIGRATION)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    from sqlalchemy import create_engine

    engine = create_engine(f"sqlite:///{db_file}")
    with engine.connect() as bind:
        with pytest.raises(RuntimeError, match="INCONSISTENT"):
            module._verify_transition_consistent(bind)


def test_guard_absence_detected(tmp_path: Path) -> None:
    db_file, db_url = _prepare_p1_db(tmp_path)
    assert _alembic(["upgrade", TRANS_REV], db_url, authority=AUTHORITY).returncode == 0
    _exec_sql(db_file, "DROP TRIGGER v2_md_provider_immutable_update")

    import importlib.util

    spec = importlib.util.spec_from_file_location("transmig2", MIGRATION)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    from sqlalchemy import create_engine

    engine = create_engine(f"sqlite:///{db_file}")
    with engine.connect() as bind:
        with pytest.raises(RuntimeError, match="NOT restored"):
            module._verify_guard_present(bind)


# ---------------------------------------------------------------------------
# Drift gate
# ---------------------------------------------------------------------------


def test_no_transition_drift(tmp_path: Path) -> None:
    db_file, db_url = _prepare_p1_db(tmp_path)
    assert _alembic(["upgrade", TRANS_REV], db_url, authority=AUTHORITY).returncode == 0
    check = _alembic(["check"], db_url)
    drift = (check.stdout + check.stderr).lower()
    for marker in ("v2_md_provider", "v2_md_", "v2_audit_event", "v2_permission"):
        assert marker not in drift, f"transition drift detected: {marker}"
