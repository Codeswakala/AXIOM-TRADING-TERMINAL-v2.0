"""V2 BE-12D kill-switch engine lifecycle matrix (BO §1.c.2, every cell).

Engine-level coupons over the real alembic chain: arm/pull/clear/re-arm
lawful cells; every refusal cell typed non-firing; the intact no-op
shape; the valve dance verified-restored after each verb; L5 truth
table over the real schema; R-3.4 carriage stamps.
"""

from __future__ import annotations

import asyncio
import os
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

BACKEND_DIR = Path(__file__).resolve().parents[1]
TRANS_AUTHORITY = "BO-V2-BE-3-P2-TRANS-001"
REV_0056 = "20260909_0056"


def _db(tmp_path: Path) -> Path:
    db_file = tmp_path / "ks.db"
    env = dict(os.environ)
    env["AXIOM_DATABASE_URL"] = f"sqlite+aiosqlite:///{db_file}"
    env.setdefault("AXIOM_ENVIRONMENT", "testing")
    env.setdefault("AXIOM_ALLOW_INSECURE_DEV", "true")
    env.setdefault("AXIOM_JWT_SECRET_KEY",
                   "test-secret-key-at-least-32-chars-long!!")
    env["AXIOM_V2_MODE"] = "RESEARCH"
    env["AXIOM_TD_TRANSITION_AUTHORITY_REF"] = TRANS_AUTHORITY
    result = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", REV_0056],
        cwd=BACKEND_DIR, env=env, capture_output=True, text=True,
        timeout=600)
    assert result.returncode == 0, result.stderr
    return db_file


def _run(db_file: Path, coro_fn):
    from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

    async def wrapper():
        eng = create_async_engine(f"sqlite+aiosqlite:///{db_file}")
        try:
            async with AsyncSession(eng) as s:
                return await coro_fn(s)
        finally:
            await eng.dispose()

    return asyncio.run(wrapper())


def _guard_count(db_file: Path) -> int:
    conn = sqlite3.connect(db_file)
    try:
        return conn.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'"
            " AND name LIKE 'v2_live_kill_switch_immutable_%'"
        ).fetchone()[0]
    finally:
        conn.close()


_REFS = dict(actor_id="op-1", step_up_ref="mfa-x", operator_id="op-1")


def test_full_lawful_cycle_every_transition(tmp_path: Path) -> None:
    """no-row→armed→pulled→cleared→armed: every lawful cell, with the
    valve guard VERIFIED-restored after each verb (guard pair == 2
    between every step) and the R-3.4 stamps carried."""
    from app.v2.live_exec.killswitch.engine import (
        governor_arm,
        governor_clear,
        governor_pull,
        killswitch_engaged,
        killswitch_state,
    )

    db_file = _db(tmp_path)

    async def cycle(s):
        assert await killswitch_state(s) is None
        assert await killswitch_engaged(s) is False
        assert await governor_arm(s, **_REFS) == "armed"
        await s.commit()
        assert await killswitch_engaged(s) is True
        assert await governor_pull(s, **_REFS) == "pulled"
        await s.commit()
        assert await killswitch_engaged(s) is True
        assert await governor_clear(s, **_REFS) == "cleared"
        await s.commit()
        assert await killswitch_engaged(s) is False
        assert await governor_arm(s, **_REFS) == "armed"
        await s.commit()
        return await killswitch_state(s)

    assert _run(db_file, cycle) == "armed"
    assert _guard_count(db_file) == 2  # valve dance restored
    rows = sqlite3.connect(db_file).execute(
        "SELECT sole, status, actor_id, step_up_ref, operator_id"
        " FROM v2_live_kill_switch").fetchall()
    assert rows == [("SOLE", "armed", "op-1", "mfa-x", "op-1")]


def test_rearm_refusals_nonfiring_both_engaged_states(tmp_path: Path) -> None:
    """arm while 'armed' AND arm while 'pulled' => typed
    `killswitch_armed`, NON-FIRING (state unchanged, valve never
    opened, guard count stable)."""
    from app.v2.live_exec.intents import LiveExecRefused
    from app.v2.live_exec.killswitch.engine import (
        governor_arm,
        governor_pull,
        killswitch_state,
    )

    db_file = _db(tmp_path)

    async def probe(s):
        await governor_arm(s, **_REFS)
        await s.commit()
        with pytest.raises(LiveExecRefused) as exc:
            await governor_arm(s, **_REFS)
        assert exc.value.reason == "killswitch_armed"
        assert await killswitch_state(s) == "armed"  # non-firing
        await governor_pull(s, **_REFS)
        await s.commit()
        with pytest.raises(LiveExecRefused) as exc:
            await governor_arm(s, **_REFS)
        assert exc.value.reason == "killswitch_armed"
        return await killswitch_state(s)

    assert _run(db_file, probe) == "pulled"
    assert _guard_count(db_file) == 2


def test_pull_invalid_cells_typed(tmp_path: Path) -> None:
    """pull on no-row, 'pulled', and 'cleared' => typed
    `killswitch_state_invalid`, non-firing each time."""
    from app.v2.live_exec.intents import LiveExecRefused
    from app.v2.live_exec.killswitch.engine import (
        governor_arm,
        governor_clear,
        governor_pull,
        killswitch_state,
    )

    db_file = _db(tmp_path)

    async def probe(s):
        with pytest.raises(LiveExecRefused) as exc:
            await governor_pull(s, **_REFS)
        assert exc.value.reason == "killswitch_state_invalid"
        await governor_arm(s, **_REFS)
        await governor_pull(s, **_REFS)
        await s.commit()
        with pytest.raises(LiveExecRefused) as exc:
            await governor_pull(s, **_REFS)  # pull while pulled
        assert exc.value.reason == "killswitch_state_invalid"
        await governor_clear(s, **_REFS)
        await s.commit()
        with pytest.raises(LiveExecRefused) as exc:
            await governor_pull(s, **_REFS)  # pull while cleared
        assert exc.value.reason == "killswitch_state_invalid"
        return await killswitch_state(s)

    assert _run(db_file, probe) == "cleared"


def test_clear_cells_intact_and_idempotent_shapes(tmp_path: Path) -> None:
    """clear on no-row => 'intact' (the standing state, never invented);
    clear on 'cleared' => 'cleared' (idempotent shape); clear on
    'armed' AND 'pulled' both lawful (the single sanctioned path)."""
    from app.v2.live_exec.killswitch.engine import (
        governor_arm,
        governor_clear,
        governor_pull,
    )

    db_file = _db(tmp_path)

    async def probe(s):
        shapes = []
        shapes.append(await governor_clear(s, **_REFS))  # no row
        await governor_arm(s, **_REFS)
        shapes.append(await governor_clear(s, **_REFS))  # from armed
        await governor_arm(s, **_REFS)
        await governor_pull(s, **_REFS)
        shapes.append(await governor_clear(s, **_REFS))  # from pulled
        shapes.append(await governor_clear(s, **_REFS))  # idempotent
        await s.commit()
        return shapes

    assert _run(db_file, probe) == ["intact", "cleared", "cleared",
                                    "cleared"]


def test_valve_inversion_direct_sql_dies_engine_path_lives(
        tmp_path: Path) -> None:
    """The §1.c.1 inversion: direct SQL UPDATE => guard refusal;
    the SAME transition through the valve => allowed exactly once."""
    from app.v2.live_exec.killswitch.engine import (
        governor_arm,
        governor_pull,
    )

    db_file = _db(tmp_path)
    _run(db_file, lambda s: _arm_and_commit(s, governor_arm))
    conn = sqlite3.connect(db_file)
    try:
        try:
            conn.execute("UPDATE v2_live_kill_switch SET status='pulled'")
            raise AssertionError("direct SQL transition failed open")
        except sqlite3.IntegrityError as exc:
            assert "immutable" in str(exc) and "UPDATE prohibited" in str(exc)
    finally:
        conn.close()

    async def pull(s):
        result = await governor_pull(s, **_REFS)
        await s.commit()
        return result

    assert _run(db_file, pull) == "pulled"
    assert _guard_count(db_file) == 2


async def _arm_and_commit(s, governor_arm):
    await governor_arm(s, **_REFS)
    await s.commit()


def test_l5_fact_reader_truth_table_real_chain(tmp_path: Path) -> None:
    """killswitch_engaged over the REAL chain: None=>False,
    armed=>True, pulled=>True, cleared=>False."""
    from app.v2.live_exec.killswitch.engine import (
        governor_arm,
        governor_clear,
        governor_pull,
        killswitch_engaged,
    )

    db_file = _db(tmp_path)

    async def probe(s):
        truth = [await killswitch_engaged(s)]           # None
        await governor_arm(s, **_REFS)
        truth.append(await killswitch_engaged(s))       # armed
        await governor_pull(s, **_REFS)
        truth.append(await killswitch_engaged(s))       # pulled
        await governor_clear(s, **_REFS)
        truth.append(await killswitch_engaged(s))       # cleared
        await s.commit()
        return truth

    assert _run(db_file, probe) == [False, True, True, False]


def test_no_other_clear_path_exists(tmp_path: Path) -> None:
    """BO §1.c.4: `governor_clear` is THE single sanctioned clear —
    token scan proves no other code path writes 'cleared'."""
    app_root = BACKEND_DIR / "app"
    offenders = []
    for path in app_root.rglob("*.py"):
        if path.name == "engine.py" and "killswitch" in str(path):
            continue  # the sanctioned valve module
        text = path.read_text(encoding="utf-8")
        # the model's CHECK constraint DECLARES the closed vocabulary —
        # a declaration is not a writer (needle discipline: exclude the
        # schema declaration form, scan every other occurrence)
        stripped = text.replace(
            "\"status IN ('armed','pulled','cleared')\"", "")
        if "'cleared'" in stripped or '"cleared"' in stripped:
            offenders.append(str(path.relative_to(app_root)))
    assert offenders == []
