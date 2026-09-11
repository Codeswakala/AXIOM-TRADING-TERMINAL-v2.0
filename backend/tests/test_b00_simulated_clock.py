"""B-00.1 — simulated clock chronology invariants (BO-B-00, option (a)).

Pinned tests for the wall-clock-bind model:
- catch-up emission (accelerated while behind the wall clock) is never
  future-dated and is strictly one-minute-stepped;
- a feed whose clock is ahead of the wall clock HOLDS until the wall clock
  catches up, then resumes;
- everything the corrected feed emits passes the W2-U01 ChronologyGuard with
  no FUTURE_OPEN_TIME quarantine (guard invoked, never weakened — a negative
  control proves it still rejects genuinely future records);
- a real-clock catch-up smoke (tolerant of the sandbox wall clock's known
  jumps: the wall-clock comparison applies only when the wall clock did not
  move backwards during the test).
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone

from app.ingestion.types import NormalizedCandleRow
from app.market.adapters.simulated import SimulatedCandleAdapter
from app.ml.dataset.chronology_guard import (
    ChronologyGuard,
    GuardRecord,
    GuardStage,
    SourceAuthority,
)

MINUTE = timedelta(minutes=1)


class FakeClock:
    """Mutable wall-clock stand-in for deterministic chronology tests."""

    def __init__(self, now: datetime) -> None:
        self.now = now

    def __call__(self) -> datetime:
        return self.now

    def advance(self, delta: timedelta) -> None:
        self.now += delta


async def collect(
    adapter: SimulatedCandleAdapter, seconds: float
) -> list[NormalizedCandleRow]:
    out: list[NormalizedCandleRow] = []

    async def handler(row: NormalizedCandleRow) -> None:
        out.append(row)

    await adapter.start(handler)
    try:
        await asyncio.sleep(seconds)
    finally:
        await adapter.stop()
    return out


def make_adapter(
    *, clock: FakeClock, start: datetime, max_ticks: int | None
) -> SimulatedCandleAdapter:
    return SimulatedCandleAdapter(
        market_class="forex",
        symbol="EURUSD",
        timeframe="M1",
        interval_seconds=0.05,
        max_ticks=max_ticks,
        start_time=start,
        now_fn=clock,
    )


async def test_catchup_emission_is_accelerated_and_never_future_dated() -> None:
    now = datetime(2026, 8, 19, 12, 0, 0, tzinfo=timezone.utc)
    clock = FakeClock(now)
    start = now - 3 * MINUTE
    candles = await collect(make_adapter(clock=clock, start=start, max_ticks=4), 0.5)
    assert len(candles) == 4, f"expected 4 catch-up bars, got {len(candles)}"
    times = [c.open_time for c in candles]
    assert all(t <= clock.now for t in times), "catch-up emitted a future-dated bar"
    assert times == [start, start + MINUTE, start + 2 * MINUTE, now], (
        "catch-up bars must be strictly one-minute-stepped"
    )


async def test_feed_holds_at_wall_clock_and_resumes_when_clock_advances() -> None:
    now = datetime(2026, 8, 19, 12, 0, 0, tzinfo=timezone.utc)
    clock = FakeClock(now)
    adapter = make_adapter(clock=clock, start=now, max_ticks=None)
    out: list[NormalizedCandleRow] = []

    async def handler(row: NormalizedCandleRow) -> None:
        out.append(row)

    await adapter.start(handler)
    try:
        await asyncio.sleep(0.3)
        # Wall clock still at 12:00:00 — only the current minute may emit.
        assert len(out) == 1, f"feed emitted ahead of the wall clock: {len(out)} bars"
        clock.advance(2 * MINUTE)
        await asyncio.sleep(0.3)
        # 12:01 and 12:02 are now due; 12:03 remains held.
        assert len(out) == 3, f"feed did not resume after the wall clock advanced: {len(out)} bars"
        assert all(c.open_time <= clock.now for c in out)
    finally:
        await adapter.stop()
    times = [c.open_time for c in out]
    assert times == sorted(set(times)), "emission must be strictly increasing without duplicates"


async def test_corrected_feed_passes_the_chronology_guard() -> None:
    now = datetime(2026, 8, 19, 12, 0, 0, tzinfo=timezone.utc)
    clock = FakeClock(now)
    start = now - 2 * MINUTE
    candles = await collect(make_adapter(clock=clock, start=start, max_ticks=3), 0.4)
    assert len(candles) == 3
    guard = ChronologyGuard()

    def record(index: int, candle: NormalizedCandleRow) -> GuardRecord:
        open_time = candle.open_time
        return GuardRecord(
            source_record_id=f"b00-{index}",
            market_class="forex",
            provider="simulated",
            symbol="EURUSD",
            timeframe="M1",
            open_time=open_time,
            source="live:simulated",
            authority=SourceAuthority.SIMULATED,
            ingestion_finished_at=clock.now,
            as_of_time=clock.now,
        )

    accepted, quarantined = guard.validate_records(
        [record(i, c) for i, c in enumerate(candles)],
        stage=GuardStage.INGESTION,
        authoritative_training=False,
    )
    assert len(accepted) == 3
    assert not [e for e in quarantined if e.reason.value == "FUTURE_OPEN_TIME"], (
        f"corrected feed quarantined as future-dated: {[e.detail for e in quarantined]}"
    )

    # Negative control: the guard itself still rejects a genuinely future record.
    future = GuardRecord(
        source_record_id="b00-negative",
        market_class="forex",
        provider="simulated",
        symbol="EURUSD",
        timeframe="M1",
        open_time=clock.now + MINUTE,
        source="live:simulated",
        authority=SourceAuthority.SIMULATED,
        ingestion_finished_at=clock.now,
        as_of_time=clock.now,
    )
    _, neg_events = guard.validate_records(
        [future], stage=GuardStage.INGESTION, authoritative_training=False
    )
    assert [e for e in neg_events if e.reason.value == "FUTURE_OPEN_TIME"], (
        "chronology guard no longer rejects future-dated records"
    )


async def test_real_clock_catchup_emits_only_past_bars() -> None:
    """Real-clock smoke: a feed started 2 minutes in the past catches up
    accelerated and then stops at the wall-clock minute. Tolerant of the
    sandbox wall clock jumping backwards mid-test: in that case only the
    strict-stepping invariant is asserted (the deterministic fake-clock tests
    carry the future-dating invariant)."""
    start = datetime.now(timezone.utc).replace(second=0, microsecond=0) - 2 * MINUTE
    adapter = SimulatedCandleAdapter(
        market_class="forex",
        symbol="EURUSD",
        timeframe="M1",
        interval_seconds=0.05,
        max_ticks=3,
        start_time=start,
    )
    candles = await collect(adapter, 0.5)
    assert len(candles) == 3, f"expected 3 catch-up bars, got {len(candles)}"
    times = [c.open_time for c in candles]
    assert times == sorted(set(times)), "emission must be strictly increasing without duplicates"
    post_now = datetime.now(timezone.utc)
    if post_now >= start:
        assert all(t <= post_now for t in times), "real-clock catch-up emitted a future-dated bar"
