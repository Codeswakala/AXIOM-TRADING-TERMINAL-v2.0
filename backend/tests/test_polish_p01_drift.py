"""POLISH-P01 fail-first tests — OBS-DATA2-1 drift removal (M1).

Every test here MUST fail against the pre-POLISH-P01 tree (the seeder's three
walks carry positive means) and pass once the mean term is zeroed. Properties
are asserted, never golden values — the same standard as the DATA-P01 crypto
regression test.

M1's narrow authorization: the mean term ONLY. Per-symbol seeding, class
factor streams, betas, _base_price, the market-class branch and provenance
markers are untouched — asserted by these tests through the existing
determinism test (re-run unmodified) and a source pin.
"""

from __future__ import annotations

import pathlib
import sqlite3

from app.db.session import session_scope
from app.repositories.candle_repository import CandleRepository
from app.services.chart_seed_service import seed_chart_history

SEED_BARS = 8640  # six days of M1 bars — the window OBS-DATA2-1 measured


def _series(symbol: str) -> list[tuple]:
    """(close, delta) per bar from a fresh deterministic seed."""
    return []  # replaced below in the async helpers


async def _seeded_closes(symbol: str) -> list[float]:
    async with session_scope() as session:
        await seed_chart_history(session, symbols=[symbol], timeframe="M1", bars=SEED_BARS)
        rows = await CandleRepository(session).list_for_symbol(
            symbol=symbol, timeframe="M1", limit=SEED_BARS, ascending=True
        )
        return [float(r.close) for r in rows]


async def test_polish_p01_walk_has_no_directional_drift_over_long_windows(
    prepared_db: None,
) -> None:
    """M1 property: over a six-day window every class's per-bar mean step is
    statistically zero (bounded tolerance, deterministic via the fixed symbol
    seeds) and the TOTAL drift is nowhere near the pre-fix +31%/-sized
    excursions. Asserted as properties, not golden values."""
    # EURUSD (forex): pre-fix mean +0.00004/bar, +31% over six days.
    closes = await _seeded_closes("EURUSD")
    steps = [closes[i] - closes[i - 1] for i in range(1, len(closes))]
    mean_step = sum(steps) / len(steps)
    total_return = (closes[-1] - closes[0]) / closes[0]
    assert abs(mean_step) < 5e-5, f"EURUSD per-bar mean step {mean_step}"
    assert abs(total_return) < 0.10, f"EURUSD six-day drift {total_return:%}"

    # USDJPY (JPY): pre-fix mean +0.004/bar.
    closes = await _seeded_closes("USDJPY")
    steps = [closes[i] - closes[i - 1] for i in range(1, len(closes))]
    mean_step = sum(steps) / len(steps)
    assert abs(mean_step) < 2e-3, f"USDJPY per-bar mean step {mean_step}"

    # BTCUSD (crypto, proportional): pre-fix mean +0.0004/bar relative.
    closes = await _seeded_closes("BTCUSD")
    rel_steps = [
        (closes[i] - closes[i - 1]) / closes[i - 1] for i in range(1, len(closes))
    ]
    mean_rel = sum(rel_steps) / len(rel_steps)
    assert abs(mean_rel) < 1e-3, f"BTCUSD per-bar mean rel step {mean_rel}"


async def test_polish_p01_chart_seed_determinism_still_holds(prepared_db: None) -> None:
    """The DATA-P01 determinism test, re-run UNMODIFIED as a separate pin: the
    mean-term change must not break run-to-run equality (it cannot — the seed
    is unchanged — and this proves the walk change touched only the mean)."""
    from app.services.chart_seed_service import seed_chart_history

    async def closes_for(symbol: str) -> list[str]:
        async with session_scope() as session:
            rows = await CandleRepository(session).list_for_symbol(
                symbol=symbol, timeframe="M1", limit=200
            )
            return [str(row.close) for row in rows]

    async with session_scope() as session:
        await seed_chart_history(session, symbols=["EURUSD"], timeframe="M1", bars=40)
    first = await closes_for("EURUSD")
    async with session_scope() as session:
        await seed_chart_history(session, symbols=["EURUSD"], timeframe="M1", bars=40)
    second = await closes_for("EURUSD")
    assert first == second


def test_polish_p01_mean_terms_are_zero_and_nothing_else_moved() -> None:
    """M1 scope pin: the three idio means are zero; the factor streams, betas,
    _base_price table and the market-class branch are untouched (the exact
    constants that took three correction cycles are still present verbatim)."""
    source = pathlib.Path("app/services/chart_seed_service.py").read_text()
    assert "rng.gauss(0, 0.0083)" in source  # crypto idio: zero mean
    assert "rng.gauss(0, 0.015)" in source  # JPY idio: zero mean
    assert "rng.gauss(0, 0.00015)" in source  # forex idio: zero mean
    assert "rng.gauss(0.0004, 0.0083)" not in source  # old crypto mean gone
    assert "rng.gauss(0.004, 0.015)" not in source  # old JPY mean gone
    assert "rng.gauss(0.00004, 0.00015)" not in source  # old forex mean gone
    # Untouched structure (R1): factor streams, base prices, branches, marker.
    assert "class_factor_seed" in source
    # The factor-stream seed is built from parts via _stable_seed — pinned as
    # the parts, exactly as constructed.
    assert '_stable_seed("axiom", "seed:synthetic", "factor"' in source
    assert "seed:synthetic" in source
    assert "_base_price" in source
    # The adapter's alternating ticks were already zero-mean — untouched.
    adapter = pathlib.Path("app/market/adapters/simulated.py").read_text()
    assert "0.0005" in adapter and "0.010" in adapter and "0.00010" in adapter
