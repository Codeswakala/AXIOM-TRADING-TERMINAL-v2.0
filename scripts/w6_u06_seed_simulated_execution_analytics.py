"""Seed W6-U06 simulated execution analytics report evidence records.

This creates a SIMULATED analytics research report only. It does not use a live
broker, real account, real P&L, or the Governance Gate.
"""

from __future__ import annotations

import asyncio
import sys
from datetime import timedelta
from decimal import Decimal
from pathlib import Path

from sqlalchemy import select

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.auth.service import AuthService  # noqa: E402
from app.core.config import get_settings  # noqa: E402
from app.core.time import utc_now  # noqa: E402
from app.db.models.operator import Operator  # noqa: E402
from app.db.session import close_db, init_db, session_scope  # noqa: E402
from app.execution_research import (  # noqa: E402
    ExecutionResearchExperimentDraft,
    ExecutionResearchExperimentService,
    SimulatedExecutionAnalyticsReportDraft,
    SimulatedExecutionAnalyticsReportService,
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
        raise RuntimeError("W6_U06_OPERATOR_REQUIRED")
    return operator.id


async def _seed_candles(session) -> tuple[object, object]:  # noqa: ANN001
    base = utc_now() - timedelta(minutes=50)
    closes = ["1.6000", "1.6010", "1.6020", "1.6030"]
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
            source="w6-u06:analytics-seed",
        )
    return times[0], times[-1]


async def main() -> None:
    init_db()
    async with session_scope() as session:
        operator_id = await _operator_id(session)
        start, as_of = await _seed_candles(session)
        run_result = await SimulatedExecutionService(session).create_run(
            operator_id=operator_id,
            spec=SimulatedExecutionRunSpec(
                market_class="forex",
                symbol="EURUSD",
                timeframe="M1",
                as_of_start=start,
                as_of_end=as_of,
                simulated_research_direction="long_bias",
                simulated_units=1.0,
                simulated_slippage_bps=0.5,
                max_fill_events=2,
                input_artifact_ids=("W6-U06-evidence-analytics-scope",),
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
        experiment = await ExecutionResearchExperimentService(session).register_and_replay(
            operator_id=operator_id,
            draft=ExecutionResearchExperimentDraft(
                experiment_title="W6-U06 analytics evidence replay",
                hypothesis="Full-scope analytics includes all declared artifacts.",
                market_class="forex",
                symbol="EURUSD",
                timeframe="M1",
                as_of_start=start,
                as_of_time=as_of,
                input_artifact_ids=(ledger.ledger_entry_id,),
                max_candles=10,
            ),
        )
        report = await SimulatedExecutionAnalyticsReportService(session).create_report(
            actor="operator_evidence",
            draft=SimulatedExecutionAnalyticsReportDraft(
                source_artifact_ids=(
                    fill.simulated_fill_id,
                    ledger.ledger_entry_id,
                    experiment.experiment_id,
                ),
                analytics_type="return_estimate",
            ),
        )
    await close_db()
    print("W6_U06_SIMULATED_ANALYTICS_REPORT_SEED_COMPLETE")
    print(f"simulated_fill_event\t{fill.simulated_fill_id}")
    print(f"simulated_paper_ledger_entry\t{ledger.ledger_entry_id}")
    print(f"execution_research_experiment\t{experiment.experiment_id}")
    print(f"simulated_execution_analytics_report\t{report.report_id}")
    print(f"report_hash\t{report.report_hash}")


if __name__ == "__main__":
    asyncio.run(main())
