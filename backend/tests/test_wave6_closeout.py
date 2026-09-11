"""W6-U08 Wave-6 closeout and hardening tests."""

from __future__ import annotations

from datetime import timedelta
from decimal import Decimal
from pathlib import Path

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.time import utc_now
from app.db.models.audit import AuditEvent
from app.db.models.execution_experiment import ExecutionResearchExperiment
from app.db.models.execution_risk_report import ExecutionRiskResearchReport
from app.db.models.operator import Operator
from app.db.models.simulated_execution import SimulatedExecutionRun, SimulatedFillEvent
from app.db.models.simulated_execution_analytics_report import SimulatedExecutionAnalyticsReport
from app.db.models.simulated_paper_ledger import SimulatedPaperLedgerEntry
from app.db.session import session_scope
from app.execution_research import (
    RESEARCH_STATUS,
    SIMULATED_EXECUTION_RESEARCH_DISCLAIMER,
    SIMULATION_MODE,
    ExecutionResearchExperimentDraft,
    ExecutionResearchExperimentService,
    ExecutionRiskResearchReportDraft,
    ExecutionRiskResearchReportService,
    SimulatedExecutionAnalyticsReportDraft,
    SimulatedExecutionAnalyticsReportService,
    SimulatedExecutionRunSpec,
    SimulatedExecutionService,
    SimulatedPaperLedgerEntryDraft,
    SimulatedPaperLedgerService,
)
from app.repositories.candle_repository import CandleRepository


def test_wave6_bright_line_grep_no_live_execution_path() -> None:
    root = Path(__file__).resolve().parents[1] / "app"
    paths = [root / "execution_research", root / "api" / "routes" / "execution_research.py"]
    forbidden = (
        "place_order",
        "broker.connect",
        "broker.execute",
        "go_live",
        "live_order",
        "live_feed_url",
        "real_account",
        "account_balance",
        "margin",
        "capital",
        "broker_credentials",
        "broker_endpoint",
        "real_pnl",
        "gate_open",
        "allow_execution",
    )
    offenders: list[str] = []
    for item in paths:
        files = item.rglob("*.py") if item.is_dir() else [item]
        for path in files:
            text = path.read_text(encoding="utf-8")
            for needle in forbidden:
                if needle in text:
                    offenders.append(f"{path.relative_to(root).as_posix()}:{needle}")
    assert offenders == []


def test_governance_gate_remains_closed_for_wave6() -> None:
    from app.external_integration.broker import governance_gate

    assert governance_gate.broker_integration_authorized is False
    assert governance_gate.execution_authorized is False


def test_broker_logic_contained_in_external_integration() -> None:
    root = Path(__file__).resolve().parents[1] / "app"
    broker_specific = (
        "MetaTrader5",
        "MqlTrade",
        "TRADE_ACTION",
        "ORDER_TYPE",
        "BrokerClient",
        "broker_endpoint",
        "broker_credentials",
    )
    offenders: list[str] = []
    for path in root.rglob("*.py"):
        rel = path.relative_to(root).as_posix()
        if rel.startswith("external_integration/"):
            continue
        if rel.startswith("v2/broker_read/providers/"):
            # BO-V2-BE-9-001 D-1 sanctioned adapter location
            continue
        text = path.read_text(encoding="utf-8")
        for needle in broker_specific:
            if needle in text:
                offenders.append(f"{rel}:{needle}")
    assert offenders == []


async def _seed_wave6_artifacts(session: AsyncSession) -> dict[str, object]:
    operator = Operator(
        username="wave6-closeout-operator",
        hashed_password="not-used-in-test",
        role="operator",
        is_active=True,
    )
    session.add(operator)
    await session.flush()

    base = utc_now() - timedelta(minutes=60)
    repo = CandleRepository(session)
    times = []
    for index, close_text in enumerate(["1.7000", "1.7010", "1.7020", "1.7030"]):
        open_time = base + timedelta(minutes=index)
        times.append(open_time)
        close = Decimal(close_text)
        await repo.upsert_ohlcv(
            market_class="forex",
            symbol="EURUSD",
            timeframe="M1",
            open_time=open_time,
            open=close,
            high=close + Decimal("0.0020"),
            low=close - Decimal("0.0020"),
            close=close,
            volume=Decimal("1"),
            source="w6-u08:closeout-test",
        )
    future, _ = await repo.upsert_ohlcv(
        market_class="forex",
        symbol="EURUSD",
        timeframe="M1",
        open_time=times[-1] + timedelta(minutes=1),
        open=Decimal("9.9900"),
        high=Decimal("9.9900"),
        low=Decimal("9.9900"),
        close=Decimal("9.9900"),
        volume=Decimal("1"),
        source="w6-u08:future-exclusion-test",
    )

    run_result = await SimulatedExecutionService(session).create_run(
        operator_id=operator.id,
        spec=SimulatedExecutionRunSpec(
            market_class="forex",
            symbol="EURUSD",
            timeframe="M1",
            as_of_start=times[0],
            as_of_end=times[-1],
            simulated_research_direction="long_bias",
            simulated_units=1.0,
            simulated_slippage_bps=0.5,
            max_fill_events=2,
            input_artifact_ids=("w6-u08-closeout-scope",),
        ),
    )
    fill = run_result.fills[0]
    ledger = await SimulatedPaperLedgerService(session).create_entry(
        operator_id=operator.id,
        draft=SimulatedPaperLedgerEntryDraft(
            run_id=run_result.run.run_id,
            simulated_fill_id=fill.simulated_fill_id,
            simulated_exit_value=float(fill.simulated_fill_price) * 1.01,
            uncertainty_width=0.001,
        ),
    )
    risk_report = await ExecutionRiskResearchReportService(session).create_report(
        actor="pytest",
        draft=ExecutionRiskResearchReportDraft(
            input_artifact_ids=(
                run_result.run.run_id,
                fill.simulated_fill_id,
                ledger.ledger_entry_id,
            )
        ),
    )
    experiment = await ExecutionResearchExperimentService(session).register_and_replay(
        operator_id=operator.id,
        draft=ExecutionResearchExperimentDraft(
            experiment_title="Wave-6 closeout replay",
            hypothesis="Closeout replay excludes future candles.",
            market_class="forex",
            symbol="EURUSD",
            timeframe="M1",
            as_of_start=times[0],
            as_of_time=times[-1],
            input_artifact_ids=(ledger.ledger_entry_id,),
            max_candles=10,
        ),
    )
    analytics = await SimulatedExecutionAnalyticsReportService(session).create_report(
        actor="pytest",
        draft=SimulatedExecutionAnalyticsReportDraft(
            source_artifact_ids=(
                fill.simulated_fill_id,
                ledger.ledger_entry_id,
                experiment.experiment_id,
            )
        ),
    )
    return {
        "run": run_result.run,
        "fill": fill,
        "ledger": ledger,
        "risk": risk_report,
        "experiment": experiment,
        "analytics": analytics,
        "future": future,
    }


@pytest.mark.asyncio
async def test_all_wave6_simulated_tables_labelled_and_inert(prepared_db: None) -> None:
    async with session_scope() as session:
        artifacts = await _seed_wave6_artifacts(session)
        rows = [
            artifacts["run"],
            artifacts["fill"],
            artifacts["ledger"],
            artifacts["risk"],
            artifacts["experiment"],
            artifacts["analytics"],
        ]
        for row in rows:
            assert getattr(row, "simulation_mode") == SIMULATION_MODE
            assert getattr(row, "research_status") == RESEARCH_STATUS
            assert getattr(row, "simulation_disclaimer") == SIMULATED_EXECUTION_RESEARCH_DISCLAIMER

        experiment = artifacts["experiment"]
        future = artifacts["future"]
        assert isinstance(experiment, ExecutionResearchExperiment)
        assert future.id not in experiment.replay_input_lineage["included_candle_ids"]

        forbidden = {
            "broker_account_id",
            "account_id",
            "real_account_balance",
            "margin",
            "capital",
            "live_position_id",
            "broker_endpoint",
            "broker_credentials",
            "order_payload",
            "order_intent",
            "real_pnl",
            "pnl",
            "realized_pnl",
            "position_size",
            "order_size",
        }
        models = [
            SimulatedExecutionRun,
            SimulatedFillEvent,
            SimulatedPaperLedgerEntry,
            ExecutionRiskResearchReport,
            ExecutionResearchExperiment,
            SimulatedExecutionAnalyticsReport,
        ]
        for model in models:
            assert set(model.__table__.columns.keys()).isdisjoint(forbidden)


@pytest.mark.asyncio
async def test_all_wave6_artifacts_have_created_audit_events(prepared_db: None) -> None:
    async with session_scope() as session:
        artifacts = await _seed_wave6_artifacts(session)
        checks = [
            (
                artifacts["run"],
                "run_id",
                "simulated_execution_run",
                "simulated_execution_run.created",
            ),
            (
                artifacts["fill"],
                "simulated_fill_id",
                "simulated_fill_event",
                "simulated_fill_event.created",
            ),
            (
                artifacts["ledger"],
                "ledger_entry_id",
                "simulated_paper_ledger_entry",
                "simulated_paper_ledger_entry.created",
            ),
            (
                artifacts["risk"],
                "report_id",
                "execution_risk_research_report",
                "execution_risk_research_report.created",
            ),
            (
                artifacts["experiment"],
                "experiment_id",
                "execution_research_experiment",
                "execution_research_experiment.created",
            ),
            (
                artifacts["analytics"],
                "report_id",
                "simulated_execution_analytics_report",
                "simulated_execution_analytics_report.created",
            ),
        ]
        for artifact, id_attr, resource_type, action in checks:
            resource_id = getattr(artifact, id_attr)
            result = await session.scalars(
                select(AuditEvent).where(
                    AuditEvent.resource_type == resource_type,
                    AuditEvent.resource_id == resource_id,
                    AuditEvent.correlation_id == artifact.audit_correlation_id,
                    AuditEvent.action == action,
                )
            )
            assert result.one_or_none() is not None
