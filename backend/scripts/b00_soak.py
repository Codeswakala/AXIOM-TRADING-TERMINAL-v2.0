"""B-00.1 Level-I soak evidence — run with the backend venv python.

Two soaks:
  1. catch-up soak: feed started 120 minutes in the past catches up
     accelerated and then holds at the wall-clock minute;
  2. wall-minute soak: production default (interval 1.0s), feed started at
     the current minute — bar 2 must wait for the real next minute.

Output is raw console evidence for the B-00 delivery report.
"""

from __future__ import annotations

import asyncio
import sys
import time
from datetime import datetime, timedelta, timezone

sys.path.insert(0, ".")

from app.market.adapters.simulated import SimulatedCandleAdapter  # noqa: E402

MINUTE = timedelta(minutes=1)


def report(tag: str, candles: list, start: datetime, elapsed_wall: float) -> None:
    now = datetime.now(timezone.utc)
    times = [c.open_time for c in candles]
    print(f"[{tag}] wall_start={start.isoformat()}")
    print(f"[{tag}] bars_emitted={len(candles)} elapsed_wall={elapsed_wall:.2f}s")
    print(f"[{tag}] first={times[0].isoformat() if times else '—'}")
    print(f"[{tag}] last={times[-1].isoformat() if times else '—'}")
    print(f"[{tag}] utc_now={now.isoformat()}")
    future = [t for t in times if t > now]
    print(f"[{tag}] FUTURE_DATED_COUNT={len(future)}")
    for t in future:
        print(f"[{tag}] FUTURE {t.isoformat()}")
    strictly_stepped = times == sorted(set(times))
    print(f"[{tag}] strictly_stepped_no_duplicates={strictly_stepped}")
    bound = start + timedelta(seconds=elapsed_wall + 5)
    ahead_of_elapsed = [t for t in times if t > bound]
    print(
        f"[{tag}] ahead_of_elapsed_wall_bound_count={len(ahead_of_elapsed)} "
        f"(bound {bound.isoformat()})"
    )


async def catchup_soak() -> None:
    start = datetime.now(timezone.utc).replace(second=0, microsecond=0) - 120 * MINUTE
    candles: list = []

    async def handler(row: object) -> None:
        candles.append(row)

    adapter = SimulatedCandleAdapter(
        market_class="forex",
        symbol="EURUSD",
        timeframe="M1",
        interval_seconds=0.02,
        start_time=start,
    )
    t0 = time.monotonic()
    await adapter.start(handler)
    try:
        await asyncio.sleep(4.0)
        count_at_4s = len(candles)
        await asyncio.sleep(2.0)
        held = len(candles) == count_at_4s
        print(f"[catchup] bars_at_4s={count_at_4s} bars_at_6s={len(candles)} HOLD_CONFIRMED={held}")
    finally:
        await adapter.stop()
    report("catchup", candles, start, time.monotonic() - t0)


async def wall_minute_soak() -> None:
    start = datetime.now(timezone.utc).replace(second=0, microsecond=0)
    candles: list = []

    async def handler(row: object) -> None:
        candles.append(row)
        print(
            f"[wallminute] emitted {row.open_time.isoformat()} at "
            f"{datetime.now(timezone.utc).isoformat()}"
        )

    adapter = SimulatedCandleAdapter(
        market_class="forex",
        symbol="EURUSD",
        timeframe="M1",
        interval_seconds=1.0,  # production default cadence
        start_time=start,
    )
    t0 = time.monotonic()
    await adapter.start(handler)
    try:
        await asyncio.sleep(75.0)
    finally:
        await adapter.stop()
    report("wallminute", candles, start, time.monotonic() - t0)


async def main() -> None:
    await catchup_soak()
    await wall_minute_soak()


if __name__ == "__main__":
    asyncio.run(main())
