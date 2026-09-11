"""W6-U05 execution research experiment and replay tests."""

from __future__ import annotations

from datetime import timedelta
from decimal import Decimal
from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.time import utc_now
from app.db.models.audit import AuditEvent
from app.db.models.candle import Candle
from app.db.models.execution_experiment import ExecutionResearchExperiment
from app.db.models.operator import Operator
from app.db.session import session_scope
from app.execution_research import (
    RESEARCH_STATUS,
    SIMULATED_EXECUTION_RESEARCH_DISCLAIMER,
    SIMULATION_MODE,
    ExecutionResearchExperimentDraft,
    ExecutionResearchExperimentService,
)
from app.repositories.candle_repository import CandleRepository
from tests.test_simulated_paper_ledger import _create_ledger_entry


async def _seed_experiment_fixture(session: AsyncSession):  # noqa: ANN202
    ledger = await _create_ledger_entry(session)
    base = utc_now() - timedelta(minutes=30)
    repo = CandleRepository(session)
    included_times = [base + timedelta(minutes=i) for i in range(3)]
    for index, open_time in enumerate(included_times):
        close = Decimal("1.4000") + Decimal(index) / Decimal("1000")
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
            source="w6-u05:test",
        )
    future_time = included_times[-1] + timedelta(minutes=1)
    future, _ = await repo.upsert_ohlcv(
        market_class="forex",
        symbol="EURUSD",
        timeframe="M1",
        open_time=future_time,
        open=Decimal("9.9900"),
        high=Decimal("9.9900"),
        low=Decimal("9.9900"),
        close=Decimal("9.9900"),
        volume=Decimal("1"),
        source="w6-u05:test-future",
    )
    operator = await session.get(Operator, ledger.operator_id)
    assert operator is not None
    draft = ExecutionResearchExperimentDraft(
        experiment_title="Pre-registered replay test",
        hypothesis="Frozen as-of replay excludes future rows.",
        market_class="forex",
        symbol="EURUSD",
        timeframe="M1",
        as_of_start=included_times[0],
        as_of_time=included_times[-1],
        input_artifact_ids=(ledger.ledger_entry_id,),
        max_candles=10,
    )
    return operator, draft, future


async def _create_experiment(session: AsyncSession) -> tuple[ExecutionResearchExperiment, Candle]:
    operator, draft, future = await _seed_experiment_fixture(session)
    experiment = await ExecutionResearchExperimentService(session).register_and_replay(
        draft=draft, operator_id=operator.id
    )
    return experiment, future


async def _assert_experiment_audit_no_orphan(session: AsyncSession) -> None:
    stmt = (
        select(ExecutionResearchExperiment.experiment_id)
        .outerjoin(
            AuditEvent,
            and_(
                AuditEvent.resource_type == "execution_research_experiment",
                AuditEvent.resource_id == ExecutionResearchExperiment.experiment_id,
                AuditEvent.correlation_id == ExecutionResearchExperiment.audit_correlation_id,
                AuditEvent.action == "execution_research_experiment.created",
            ),
        )
        .where(AuditEvent.id.is_(None))
    )
    assert list((await session.scalars(stmt)).all()) == []


async def _assert_lineage_no_orphan(session: AsyncSession) -> None:
    from app.db.models.simulated_execution import SimulatedExecutionRun, SimulatedFillEvent
    from app.db.models.simulated_paper_ledger import SimulatedPaperLedgerEntry

    experiments = list((await session.scalars(select(ExecutionResearchExperiment))).all())
    for experiment in experiments:
        lineage = experiment.replay_input_lineage
        for run_id in lineage.get("simulated_run_ids", []):
            assert await session.get(SimulatedExecutionRun, run_id) is not None
        for fill_id in lineage.get("simulated_fill_ids", []):
            assert await session.get(SimulatedFillEvent, fill_id) is not None
        for ledger_id in lineage.get("simulated_ledger_entry_ids", []):
            assert await session.get(SimulatedPaperLedgerEntry, ledger_id) is not None
        for candle_id in lineage.get("included_candle_ids", []):
            assert await session.get(Candle, candle_id) is not None


@pytest.mark.asyncio
async def test_execution_research_experiment_persists_and_audit_no_orphan(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        experiment, _ = await _create_experiment(session)
        assert experiment.simulation_mode == SIMULATION_MODE
        assert experiment.research_status == RESEARCH_STATUS
        assert experiment.simulation_disclaimer == SIMULATED_EXECUTION_RESEARCH_DISCLAIMER
        assert len(experiment.plan_hash) == 64
        await _assert_experiment_audit_no_orphan(session)


@pytest.mark.asyncio
async def test_experiment_plan_hash_is_immutable_and_matches_preregistration(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        experiment, _ = await _create_experiment(session)
        service = ExecutionResearchExperimentService(session)
        assert service.compute_plan_hash(experiment.pre_registration_plan) == experiment.plan_hash
        assert not hasattr(ExecutionResearchExperimentService, "update_experiment")
        original_hash = experiment.plan_hash
        experiment.experiment_title = "Display title changed for local object only"
        assert service.compute_plan_hash(experiment.pre_registration_plan) == original_hash


@pytest.mark.asyncio
async def test_replay_excludes_future_rows_beyond_as_of(prepared_db: None) -> None:
    async with session_scope() as session:
        experiment, future = await _create_experiment(session)
        included = set(experiment.replay_input_lineage["included_candle_ids"])
        assert future.id not in included
        assert experiment.replay_input_lineage["excluded_future_candle_count"] >= 1
        future_rows = list(
            (
                await session.scalars(
                    select(Candle).where(
                        Candle.id.in_(included),
                        Candle.open_time > experiment.as_of_time,
                    )
                )
            ).all()
        )
        assert future_rows == []


@pytest.mark.asyncio
async def test_replay_included_scope_equals_preregistered_scope_no_cherry_picking(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        experiment, _ = await _create_experiment(session)
        declared = experiment.pre_registration_plan["replay_scope"]
        executed = experiment.included_scope_summary["executed_replay_scope"]
        assert executed == declared
        assert experiment.included_scope_summary["declared_replay_scope"] == declared
        assert experiment.included_scope_summary["included_candle_count"] == len(
            experiment.replay_input_lineage["included_candle_ids"]
        )


@pytest.mark.asyncio
async def test_registered_plan_mutation_is_refused(async_client: AsyncClient) -> None:
    async with session_scope() as session:
        experiment, _ = await _create_experiment(session)
        experiment_id = experiment.experiment_id
    login = await async_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert login.status_code == 200, login.text
    headers = {"Authorization": f"Bearer {login.json()['tokens']['access_token']}"}
    response = await async_client.put(
        f"/api/v1/execution-research/execution-experiments/{experiment_id}",
        headers=headers,
        json={"experiment_title": "blocked"},
    )
    assert response.status_code in {404, 405}


def test_execution_experiment_has_no_forbidden_account_pnl_or_sizing_columns() -> None:
    forbidden = {
        "account_balance",
        "real_account_balance",
        "margin",
        "capital",
        "real_capital",
        "broker_account_id",
        "account_id",
        "live_position_id",
        "position_id",
        "broker_endpoint",
        "broker_credentials",
        "order_payload",
        "order_intent",
        "real_pnl",
        "pnl",
        "realized_pnl",
        "position_size",
        "order_size",
        "live_feed_url",
        "execution_status_as_live",
    }
    assert set(ExecutionResearchExperiment.__table__.columns.keys()).isdisjoint(forbidden)


@pytest.mark.asyncio
async def test_execution_experiment_carries_uncertainty_and_limitations(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        experiment, _ = await _create_experiment(session)
        assert experiment.uncertainty["method"] == "replay_scope_count_limitation"
        assert experiment.uncertainty["sample_count"] >= 1
        assert "pre_registered_scope_not_cherry_picked" in experiment.limitations
        assert "as_of_bounded_no_future_rows" in experiment.limitations


def test_execution_research_experiment_create_path_has_no_live_feed_broker_or_gate_path() -> None:
    root = Path(__file__).resolve().parents[1] / "app"
    paths = [root / "execution_research", root / "api" / "routes" / "execution_research.py"]
    forbidden = (
        "place_order",
        "broker.connect",
        "broker.execute",
        "go_live",
        "live_order",
        "live_feed",
        "real_account",
        "account_balance",
        "margin",
        "position_size",
        "order_size",
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
                    offenders.append(f"{path.name}:{needle}")
    assert offenders == []


def test_governance_gate_remains_closed_for_wave6() -> None:
    from app.external_integration.broker import governance_gate

    assert governance_gate.broker_integration_authorized is False
    assert governance_gate.execution_authorized is False


async def _auth_headers(async_client: AsyncClient) -> dict[str, str]:
    login = await async_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert login.status_code == 200, login.text
    return {"Authorization": f"Bearer {login.json()['tokens']['access_token']}"}


@pytest.mark.asyncio
async def test_execution_experiment_api_auth_create_list_detail(async_client: AsyncClient) -> None:
    async with session_scope() as session:
        operator, draft, _ = await _seed_experiment_fixture(session)
        # The fixture creates linked simulated artifacts; preserve draft values for API.
        _ = operator
    headers = await _auth_headers(async_client)
    unauth = await async_client.get("/api/v1/execution-research/execution-experiments")
    assert unauth.status_code == 401
    create = await async_client.post(
        "/api/v1/execution-research/execution-experiments",
        headers=headers,
        json={
            "experiment_title": draft.experiment_title,
            "hypothesis": draft.hypothesis,
            "market_class": draft.market_class,
            "symbol": draft.symbol,
            "timeframe": draft.timeframe,
            "as_of_start": draft.as_of_start.isoformat(),
            "as_of_time": draft.as_of_time.isoformat(),
            "input_artifact_ids": list(draft.input_artifact_ids),
            "max_candles": draft.max_candles,
        },
    )
    assert create.status_code == 201, create.text
    payload = create.json()
    experiment_id = payload["experiment_id"]
    assert payload["simulation_mode"] == "SIMULATED"
    assert payload["plan_hash"]

    listing = await async_client.get(
        "/api/v1/execution-research/execution-experiments", headers=headers
    )
    assert listing.status_code == 200, listing.text
    assert any(item["experiment_id"] == experiment_id for item in listing.json())

    detail = await async_client.get(
        f"/api/v1/execution-research/execution-experiments/{experiment_id}",
        headers=headers,
    )
    assert detail.status_code == 200, detail.text
    blocked = await async_client.post(
        f"/api/v1/execution-research/execution-experiments/{experiment_id}/execute",
        headers=headers,
        json={},
    )
    assert blocked.status_code in {404, 405}
