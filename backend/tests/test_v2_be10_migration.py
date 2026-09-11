"""V2 BE-10 migration tests — BO-V2-BE-10-001 L10 (census 76/65/12, seed
idempotency, seed-only law, reversible-exact downgrade, drift)."""

from __future__ import annotations

import os
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

BACKEND_DIR = Path(__file__).resolve().parents[1]
TRANS_AUTHORITY = "BO-V2-BE-3-P2-TRANS-001"
REV_0049 = "20260905_0049"
REV_0050 = "20260908_0050"

SEALED_MAP = {
    "EURUSDm": "forex.eurusd", "GBPUSDm": "forex.gbpusd",
    "USDJPYm": "forex.usdjpy", "AUDUSDm": "forex.audusd",
    "USDCADm": "forex.usdcad", "USDCHFm": "forex.usdchf",
    "NZDUSDm": "forex.nzdusd", "EURGBPm": "forex.eurgbp",
    "BTCUSDm": "crypto.btcusd", "ETHUSDm": "crypto.ethusd",
    "SOLUSDm": "crypto.solusd", "XAUUSDm": "metal.xauusd",
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
    db_file = tmp_path / "be10.db"
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


def test_0050_census_tattoo(tmp_path: Path) -> None:
    db_file, _ = _db(tmp_path, REV_0050)
    trig = _q(db_file, "SELECT COUNT(*) FROM sqlite_master WHERE"
                       " type='trigger' AND name LIKE 'v2_%'")[0][0]
    perm = _q(db_file, "SELECT COUNT(*) FROM v2_permission")[0][0]
    comp = _q(db_file, "SELECT COUNT(*) FROM v2_computation_version")[0][0]
    assert (trig, perm, comp) == (76, 65, 12)  # B-3: no new triggers
    assert ("admin", "v2.account_context.read", "SAL-2") in {
        tuple(r) for r in _q(db_file,
                             "SELECT role, permission, sal FROM"
                             " v2_permission")}
    ace = _q(db_file, "SELECT component, version, LENGTH(source_hash)"
                      " FROM v2_computation_version"
                      " WHERE component='account_context_engine'")
    assert ace == [("account_context_engine", "ace-1.0.0", 64)]


def test_0050_sealed_map_rows_exact(tmp_path: Path) -> None:
    """Exactly the 12 sealed pairs; no invented rows (BO commission law)."""
    db_file, _ = _db(tmp_path, REV_0050)
    rows = dict(_q(db_file,
                   "SELECT source_symbol, instrument_id FROM"
                   " v2_md_symbol_map WHERE source_id='exness_mt5_demo'"))
    assert rows == SEALED_MAP
    src = _q(db_file, "SELECT source_id, kind, authority, active FROM"
                      " v2_md_source WHERE source_id='exness_mt5_demo'")
    assert src == [("exness_mt5_demo", "import", "unknown", 1)]


def test_0050_seed_idempotency(tmp_path: Path) -> None:
    """Down/up cycle re-seeds without duplicates (existing-set filters)."""
    db_file, db_url = _db(tmp_path, REV_0050)
    r = _alembic(["downgrade", REV_0049], db_url)
    assert r.returncode == 0, r.stderr
    r = _alembic(["upgrade", REV_0050], db_url)
    assert r.returncode == 0, r.stderr
    maps = _q(db_file, "SELECT COUNT(*) FROM v2_md_symbol_map"
                       " WHERE source_id='exness_mt5_demo'")[0][0]
    perm = _q(db_file, "SELECT COUNT(*) FROM v2_permission")[0][0]
    comp = _q(db_file, "SELECT COUNT(*) FROM v2_computation_version")[0][0]
    assert (maps, perm, comp) == (12, 65, 12)


def test_0050_downgrade_reverses_exactly(tmp_path: Path) -> None:
    db_file, db_url = _db(tmp_path, REV_0049)
    pre_perms = sorted(_q(db_file, "SELECT role, permission FROM"
                                   " v2_permission"))
    pre_comp = sorted(_q(db_file, "SELECT component, version FROM"
                                  " v2_computation_version"))
    pre_maps = sorted(_q(db_file, "SELECT source_id, source_symbol FROM"
                                  " v2_md_symbol_map"))
    pre_srcs = sorted(_q(db_file, "SELECT source_id FROM v2_md_source"))
    r = _alembic(["upgrade", REV_0050], db_url)
    assert r.returncode == 0, r.stderr
    r = _alembic(["downgrade", REV_0049], db_url)
    assert r.returncode == 0, r.stderr
    assert sorted(_q(db_file, "SELECT role, permission FROM"
                              " v2_permission")) == pre_perms
    assert sorted(_q(db_file, "SELECT component, version FROM"
                              " v2_computation_version")) == pre_comp
    assert sorted(_q(db_file, "SELECT source_id, source_symbol FROM"
                              " v2_md_symbol_map")) == pre_maps
    assert sorted(_q(db_file, "SELECT source_id FROM"
                              " v2_md_source")) == pre_srcs
    guard = _q(db_file, "SELECT COUNT(*) FROM sqlite_master WHERE"
                        " type='trigger' AND name="
                        "'v2_computation_version_immutable_delete'")
    assert guard[0][0] == 1  # compver delete-guard restored


def test_0050_seed_only_no_schema_ops(tmp_path: Path) -> None:
    """L10: zero new tables/columns/triggers across 0050 (content law)."""
    db_file, db_url = _db(tmp_path, REV_0049)
    pre_tables = sorted(_q(db_file, "SELECT name FROM sqlite_master"
                                    " WHERE type='table'"))
    pre_trigs = sorted(_q(db_file, "SELECT name FROM sqlite_master"
                                   " WHERE type='trigger'"))
    r = _alembic(["upgrade", REV_0050], db_url)
    assert r.returncode == 0, r.stderr
    assert sorted(_q(db_file, "SELECT name FROM sqlite_master"
                              " WHERE type='table'")) == pre_tables
    assert sorted(_q(db_file, "SELECT name FROM sqlite_master"
                              " WHERE type='trigger'")) == pre_trigs


@pytest.mark.parametrize("rev", [REV_0049, REV_0050])
def test_drift_gate_0050(tmp_path: Path, rev: str) -> None:
    db_file, db_url = _db(tmp_path, rev)
    check = _alembic(["check"], db_url)
    drift = (check.stdout + check.stderr).lower()
    assert check.returncode != 0
    assert "account_context" not in drift, f"BE-10 drift at {rev}"
    if "not up to date" not in drift:
        assert "audit_write_failure_records" in drift
