"""V2 BE-11 seed overlay coupons — OV-V2-BE-11-002 §2.

Gate pair (one upgrade line 0051->0052); seed census 5 with exact
names/payloads/units/citations (values quoted from the spec, never
retyped); armed flips (comparison_state armed, tolerance census 4);
generation staleness arms (23h passes, 49h -> basis_stale); drift
three-ways plus both exact boundaries under the 125/250 structural 2x
law; EMPTY-FORCE for everything else; content-keyed count-asserted
downgrade with guard-pair restoration."""

from __future__ import annotations

import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
TRANS_AUTHORITY = "BO-V2-BE-3-P2-TRANS-001"
REV_0051 = "20260909_0051"
REV_0052 = "20260909_0052"

# OV-V2-BE-11-002 §1, quoted verbatim.
EXPECTED_TOLERANCES = {
    "balance": ("125.00", "USD", "operator seed"),
    "margin_used": ("125.00", "USD", "operator seed"),
    "margin_available": ("125.00", "USD", "operator seed"),
    "unrealized_pl": ("125.00", "USD", "operator seed"),
}
EXPECTED_STALENESS = (48, "operator seed")


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
    db_file = tmp_path / "be11ov.db"
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


def test_ov_one_upgrade_line_0051_to_0052(tmp_path: Path) -> None:
    """Exactly ONE upgrade line 0051->0052, BOTH streams parsed (N-O8)."""
    db_file, db_url = _db(tmp_path, REV_0051)
    result = _alembic(["upgrade", REV_0052], db_url)
    assert result.returncode == 0, result.stderr
    both = result.stdout + result.stderr
    lines = [ln for ln in both.splitlines() if "Running upgrade" in ln]
    assert len(lines) == 1, lines
    assert f"{REV_0051} -> {REV_0052}" in lines[0]


def test_ov_seed_census_exact(tmp_path: Path) -> None:
    """Five rows; names/payloads/units/citations exact; census unchanged."""
    db_file, _ = _db(tmp_path, REV_0052)
    rows = _q(db_file,
              "SELECT seed_name, payload FROM v2_paper_bridge_drift_run"
              " WHERE run_kind = 'seed'")
    assert len(rows) == 5
    tolerances = {}
    staleness = None
    for seed_name, raw in rows:
        payload = json.loads(raw)
        if seed_name == "drift_tolerance":
            tolerances[payload["name"]] = (
                payload["value"], payload["unit"], payload["citation"])
        elif seed_name == "generation_staleness":
            staleness = (payload["max_age_hours"], payload["citation"])
        else:
            raise AssertionError(f"unexpected seed_name {seed_name}")
    assert tolerances == EXPECTED_TOLERANCES
    assert staleness == EXPECTED_STALENESS
    # census tattoo unchanged: the overlay is data-only
    trig = _q(db_file, "SELECT COUNT(*) FROM sqlite_master WHERE"
                       " type='trigger'")[0][0]
    perm = _q(db_file, "SELECT COUNT(*) FROM v2_permission")[0][0]
    comp = _q(db_file, "SELECT COUNT(*) FROM v2_computation_version")[0][0]
    assert (trig, perm, comp) == (78, 69, 13)
    # EMPTY-FORCE for everything else: zero drift_run rows, zero other kinds
    other = _q(db_file, "SELECT COUNT(*) FROM v2_paper_bridge_drift_run"
                        " WHERE run_kind != 'seed'")[0][0]
    assert other == 0


def test_ov_armed_flip_and_tolerance_census(tmp_path: Path) -> None:
    """comparison_state armed; tolerance census 4; staleness 48.0."""
    import asyncio

    from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

    from app.v2.paper_bridge.engine import (
        read_staleness_seed,
        read_tolerance_seeds,
    )

    db_file, _ = _db(tmp_path, REV_0052)

    async def read():
        eng = create_async_engine(f"sqlite+aiosqlite:///{db_file}")
        try:
            async with AsyncSession(eng) as s:
                return (await read_tolerance_seeds(s),
                        await read_staleness_seed(s))
        finally:
            await eng.dispose()

    seeds, max_age = asyncio.run(read())
    assert len(seeds) == 4
    assert {s["name"] for s in seeds} == set(EXPECTED_TOLERANCES)
    assert max_age == 48.0
    armed = bool(seeds) and max_age is not None
    assert armed, "comparison_state must be armed post-overlay"


def test_ov_generation_staleness_arms(tmp_path: Path) -> None:
    """Basis 23h -> armed path (accept); 49h -> typed basis_stale."""
    import asyncio

    from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

    from app.v2.paper_bridge.contract import BridgeRefused
    from app.v2.paper_bridge.engine import (
        evaluate_intent,
        read_staleness_seed,
        require_citation,
    )

    db_file, _ = _db(tmp_path, REV_0052)

    async def read():
        eng = create_async_engine(f"sqlite+aiosqlite:///{db_file}")
        try:
            async with AsyncSession(eng) as s:
                return await read_staleness_seed(s)
        finally:
            await eng.dispose()

    max_age = asyncio.run(read())
    assert max_age == 48.0

    class _Basis:
        basis_age_hours = 23.0
        staleness = "fresh"
        positions_present = True
        sync_run_id = "ov-coupon"
        balance = "10000.0"
        margin_used = "0.0"
        margin_available = "10000.0"
        unrealized_pl = "0.0"
        currency = "USD"

    citation = require_citation({
        "value": "1.10", "currency_unit": "USD",
        "cited_source": "ov-coupon", "cited_at": "2026-09-07T00:00:00Z"})
    record = evaluate_intent(_Basis(), {"quantity": "100"}, citation, max_age)
    assert record.decision == "accept_with_notes"

    stale = _Basis()
    stale.basis_age_hours = 49.0
    try:
        evaluate_intent(stale, {"quantity": "100"}, citation, max_age)
        raise AssertionError("49h basis must refuse")
    except BridgeRefused as refusal:
        assert refusal.reason == "basis_stale"


def test_ov_drift_three_ways_and_boundaries(tmp_path: Path) -> None:
    """125/250 structural 2x law: within / minor / major + BOTH exact
    boundaries tol-inclusive (0.00 and 125.00 within; 250.00 minor)."""
    import asyncio

    from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

    from app.v2.paper_bridge.engine import compute_drift, read_tolerance_seeds

    db_file, _ = _db(tmp_path, REV_0052)

    async def read():
        eng = create_async_engine(f"sqlite+aiosqlite:///{db_file}")
        try:
            async with AsyncSession(eng) as s:
                return await read_tolerance_seeds(s)
        finally:
            await eng.dispose()

    seeds = asyncio.run(read())
    cases = (
        ("0.00", "within_tolerance"),
        ("125.00", "within_tolerance"),
        ("125.01", "drift_minor"),
        ("250.00", "drift_minor"),
        ("250.01", "drift_major"),
    )
    for delta, expected in cases:
        verdict, findings = compute_drift(
            {"balance": "1000.00"},
            {"balance": str(1000.00 + float(delta))}, seeds)
        assert verdict == expected, (delta, verdict, expected)
    # every seeded field individually resolvable
    for field in EXPECTED_TOLERANCES:
        verdict, _ = compute_drift(
            {field: "100.00"}, {field: "150.00"}, seeds)
        assert verdict == "within_tolerance", (field, verdict)


def test_ov_downgrade_reverses_exactly(tmp_path: Path) -> None:
    """Content-keyed delete of exactly 5 rows; guard pair restored;
    post-downgrade table returns to EMPTY-FORCED."""
    db_file, db_url = _db(tmp_path, REV_0052)
    pre = _q(db_file, "SELECT COUNT(*) FROM v2_paper_bridge_drift_run")[0][0]
    assert pre == 5
    result = _alembic(["downgrade", REV_0051], db_url)
    assert result.returncode == 0, result.stderr
    post = _q(db_file, "SELECT COUNT(*) FROM v2_paper_bridge_drift_run")[0][0]
    assert post == 0
    guard = _q(db_file, "SELECT COUNT(*) FROM sqlite_master WHERE"
                        " type='trigger' AND name LIKE"
                        " 'v2_paper_bridge_drift_run_immutable_%'")[0][0]
    assert guard == 2
    head = _q(db_file, "SELECT version_num FROM alembic_version")[0][0]
    assert head == REV_0051


def test_ov_guard_pair_live_after_overlay(tmp_path: Path) -> None:
    """The immutable pair still fires on the seeded rows post-overlay."""
    db_file, _ = _db(tmp_path, REV_0052)
    conn = sqlite3.connect(db_file)
    try:
        for sql in (
            "UPDATE v2_paper_bridge_drift_run SET actor_id = 'x'",
            "DELETE FROM v2_paper_bridge_drift_run",
        ):
            try:
                conn.execute(sql)
                raise AssertionError(f"guard failed open: {sql}")
            except sqlite3.IntegrityError:
                pass
    finally:
        conn.close()


def test_ov_drift_gate_0052(tmp_path: Path) -> None:
    """Drift law at the new head: zero band tokens, inheritance witness."""
    db_file, db_url = _db(tmp_path, REV_0052)
    check = _alembic(["check"], db_url)
    drift = (check.stdout + check.stderr).lower()
    assert check.returncode != 0
    assert "paper_bridge" not in drift, "BE-11 drift at 0052"
    if "not up to date" not in drift:
        assert "audit_write_failure_records" in drift
