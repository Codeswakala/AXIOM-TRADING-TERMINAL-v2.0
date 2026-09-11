"""Seed W6-U02 simulated execution run and fill event evidence records.

This creates SIMULATED research artifacts only. It does not connect to any
broker, place orders, use real accounts, or open the Governance Gate.
"""

from __future__ import annotations

import asyncio
import sys
from datetime import timedelta
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from sqlalchemy import select  # noqa: E402

from app.auth.service import AuthService  # noqa: E402
from app.core.config import get_settings  # noqa: E402
from app.core.time import utc_now  # noqa: E402
from app.db.models.operator import Operator  # noqa: E402
from app.db.session import close_db, init_db, session_scope  # noqa: E402
from app.execution_research import SimulatedExecutionRunSpec, SimulatedExecutionService  # noqa: E402
from app.repositories.candle_repository import CandleRepository  # noqa: E402


async def _operator_id(session) -> str:  # noqa: ANN001
    settings = get_settings()
    await AuthService(session, settings).ensure_bootstrap_admin()
    result = await session.scalars(select(Operator).order_by(Operator.created_at.asc()).limit(1))
    operator = result.first()
    if operator is None:
        raise RuntimeError("W6_U02_OPERATOR_REQUIRED")
    return operator.id


async def _seed_candles(session) -> tuple[object, object]:  # noqa: ANN001
    base = utc_now() - timedelta(minutes=20)
    closes = ["1.1000", "1.1010", "1.1025", "1.1015", "1.1030"]
    repo = CandleRepository(session)
    times = []
    for index, close in enumerate(closes):
        open_time = base + timedelta(minutes=index)
        times.append(open_time)
        await repo.upsert_ohlcv(
            market_class="forex",
            symbol="EURUSD",
            timeframe="M1",
            open_time=open_time,
            open=Decimal(close),
            high=Decimal(close) + Decimal("0.0020"),
            low=Decimal(close) - Decimal("0.0020"),
            close=Decimal(close),
            volume=Decimal("1"),
            source="w6-u02:simulated-execution-seed",
        )
    return times[0], times[-1]


async def main() -> None:
    init_db()
    async with session_scope() as session:
        operator_id = await _operator_id(session)
        start, end = await _seed_candles(session)
        result = await SimulatedExecutionService(session).create_run(
            operator_id=operator_id,
            spec=SimulatedExecutionRunSpec(
                market_class="forex",
                symbol="EURUSD",
                timeframe="M1",
                as_of_start=start,
                as_of_end=end,
                simulated_research_direction="long_bias",
                simulated_units=1.0,
                simulated_slippage_bps=0.5,
                max_fill_events=3,
                input_artifact_ids=("W6-U02-evidence-replay-scope",),
            ),
        )
    await close_db()
    print("W6_U02_SIMULATED_EXECUTION_SEED_COMPLETE")
    print(f"simulated_execution_run\t{result.run.run_id}")
    for fill in result.fills:
        print(f"simulated_fill_event\t{fill.simulated_fill_id}\t{fill.simulated_fill_price}")


if __name__ == "__main__":
    asyncio.run(main())
