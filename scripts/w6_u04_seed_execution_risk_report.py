"""Seed W6-U04 execution risk research report evidence records.

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
from app.execution_research import (  # noqa: E402
    ExecutionRiskResearchReportDraft,
    ExecutionRiskResearchReportService,
    SimulatedExecutionRunSpec,
    SimulatedExecutionService,
    SimulatedPaperLedgerEntryDraft,
    SimulatedPaperLedgerService,
)
from app.repositories.candle_repository import CandleRepository  # noqa: E402


async def _operator_id(session) -> str:  # noqa: ANN001
    settings = get_settings()
    await AuthService(session, settings).ensure_bootstrap_admin()
    result = await session.scalars(select(Operator).order_by(Operator.created_at.asc()).limit(1))
    operator = result.first()
    if operator is None:
        raise RuntimeError("W6_U04_OPERATOR_REQUIRED")
    return operator.id


async def _seed_candles(session) -> tuple[object, object]:  # noqa: ANN001
    base = utc_now() - timedelta(minutes=25)
    closes = ["1.3000", "1.3010", "1.3020", "1.3030"]
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
            source="w6-u04:execution-risk-seed",
        )
    return times[0], times[-1]


async def main() -> None:
    init_db()
    async with session_scope() as session:
        operator_id = await _operator_id(session)
        start, end = await _seed_candles(session)
        run_result = await SimulatedExecutionService(session).create_run(
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
                max_fill_events=2,
                input_artifact_ids=("W6-U04-evidence-risk-scope",),
            ),
        )
        fill = run_result.fills[0]
        ledger = await SimulatedPaperLedgerService(session).create_entry(
            operator_id=operator_id,
            draft=SimulatedPaperLedgerEntryDraft(
                run_id=run_result.run.run_id,
                simulated_fill_id=fill.simulated_fill_id,
                simulated_exit_value=float(fill.simulated_fill_price) * 1.01,
                uncertainty_width=0.001,
            ),
        )
        report = await ExecutionRiskResearchReportService(session).create_report(
            actor="operator_evidence",
            draft=ExecutionRiskResearchReportDraft(
                input_artifact_ids=(
                    run_result.run.run_id,
                    fill.simulated_fill_id,
                    ledger.ledger_entry_id,
                )
            ),
        )
    await close_db()
    print("W6_U04_EXECUTION_RISK_REPORT_SEED_COMPLETE")
    print(f"simulated_execution_run\t{run_result.run.run_id}")
    print(f"simulated_fill_event\t{fill.simulated_fill_id}")
    print(f"simulated_paper_ledger_entry\t{ledger.ledger_entry_id}")
    print(f"execution_risk_research_report\t{report.report_id}")


if __name__ == "__main__":
    asyncio.run(main())
