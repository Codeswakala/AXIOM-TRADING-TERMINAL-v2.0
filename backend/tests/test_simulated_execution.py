"""W6-U02 simulated execution runs and fill events tests."""

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
from app.db.models.operator import Operator
from app.db.models.simulated_execution import SimulatedExecutionRun, SimulatedFillEvent
from app.db.session import session_scope
from app.execution_research import (
    FILL_MODEL_VERSION,
    RESEARCH_STATUS,
    SIMULATED_EXECUTION_RESEARCH_DISCLAIMER,
    SIMULATION_MODE,
    DeterministicSimulatedFillModel,
    SimulatedExecutionRunSpec,
    SimulatedExecutionService,
)
from app.execution_research.contracts import EXECUTION_RESEARCH_POLICY_VERSION
from app.repositories.candle_repository import CandleRepository


async def _operator(session: AsyncSession) -> Operator:
    operator = Operator(
        username="sim-operator",
        hashed_password="not-used-in-test",
        role="operator",
        is_active=True,
    )
    session.add(operator)
    await session.flush()
    return operator


async def _seed_candles(session: AsyncSession) -> tuple[object, object]:
    base = utc_now() - timedelta(minutes=15)
    closes = ["1.1000", "1.1010", "1.1025", "1.1015"]
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
            source="w6-u02:test",
        )
    return times[0], times[-1]


def _spec(start: object, end: object) -> SimulatedExecutionRunSpec:
    return SimulatedExecutionRunSpec(
        market_class="forex",
        symbol="EURUSD",
        timeframe="M1",
        as_of_start=start,  # type: ignore[arg-type]
        as_of_end=end,  # type: ignore[arg-type]
        simulated_research_direction="long_bias",
        simulated_units=1.0,
        simulated_slippage_bps=0.5,
        max_fill_events=3,
        input_artifact_ids=("test-replay-scope",),
    )


async def _create_run(session: AsyncSession):  # noqa: ANN202
    operator = await _operator(session)
    start, end = await _seed_candles(session)
    return await SimulatedExecutionService(session).create_run(
        spec=_spec(start, end), operator_id=operator.id
    )


async def _assert_run_no_orphan(session: AsyncSession) -> None:
    stmt = (
        select(SimulatedExecutionRun.run_id)
        .outerjoin(
            AuditEvent,
            and_(
                AuditEvent.resource_type == "simulated_execution_run",
                AuditEvent.resource_id == SimulatedExecutionRun.run_id,
                AuditEvent.correlation_id == SimulatedExecutionRun.audit_correlation_id,
                AuditEvent.action == "simulated_execution_run.created",
            ),
        )
        .where(AuditEvent.id.is_(None))
    )
    assert list((await session.scalars(stmt)).all()) == []


async def _assert_fill_no_orphan(session: AsyncSession) -> None:
    stmt = (
        select(SimulatedFillEvent.simulated_fill_id)
        .outerjoin(
            AuditEvent,
            and_(
                AuditEvent.resource_type == "simulated_fill_event",
                AuditEvent.resource_id == SimulatedFillEvent.simulated_fill_id,
                AuditEvent.correlation_id == SimulatedFillEvent.audit_correlation_id,
                AuditEvent.action == "simulated_fill_event.created",
            ),
        )
        .where(AuditEvent.id.is_(None))
    )
    assert list((await session.scalars(stmt)).all()) == []


async def _assert_operator_no_orphan(session: AsyncSession) -> None:
    stmt = (
        select(SimulatedExecutionRun.run_id)
        .outerjoin(Operator, Operator.id == SimulatedExecutionRun.operator_id)
        .where(Operator.id.is_(None))
    )
    assert list((await session.scalars(stmt)).all()) == []


@pytest.mark.asyncio
async def test_simulated_execution_run_persists_and_audit_no_orphan(prepared_db: None) -> None:
    async with session_scope() as session:
        result = await _create_run(session)
        run = await session.get(SimulatedExecutionRun, result.run.run_id)
        assert run is not None
        assert run.simulation_mode == SIMULATION_MODE
        assert run.research_status == RESEARCH_STATUS
        assert run.simulation_policy_version == EXECUTION_RESEARCH_POLICY_VERSION
        assert run.fill_model_version == FILL_MODEL_VERSION
        assert run.simulation_disclaimer == SIMULATED_EXECUTION_RESEARCH_DISCLAIMER
        await _assert_run_no_orphan(session)
        await _assert_operator_no_orphan(session)


@pytest.mark.asyncio
async def test_simulated_fill_events_persist_and_audit_no_orphan(prepared_db: None) -> None:
    async with session_scope() as session:
        result = await _create_run(session)
        fills = list(
            (
                await session.scalars(
                    select(SimulatedFillEvent).where(SimulatedFillEvent.run_id == result.run.run_id)
                )
            ).all()
        )
        assert len(fills) == 3
        for fill in fills:
            assert fill.simulation_mode == SIMULATION_MODE
            assert fill.research_status == RESEARCH_STATUS
            assert fill.fill_model_version == FILL_MODEL_VERSION
            assert fill.simulated_units == pytest.approx(1.0)
            assert fill.source_candle_ids
            assert fill.simulation_disclaimer == SIMULATED_EXECUTION_RESEARCH_DISCLAIMER
        await _assert_fill_no_orphan(session)


@pytest.mark.asyncio
async def test_simulated_fill_model_is_deterministic(prepared_db: None) -> None:
    async with session_scope() as session:
        start, end = await _seed_candles(session)
        spec = _spec(start, end)
        service = SimulatedExecutionService(session)
        candles = await service._candles(spec, spec.as_of_start, spec.as_of_end)  # noqa: SLF001
        model = DeterministicSimulatedFillModel()
        first = model.preview(spec=spec, candles=candles)
        second = model.preview(spec=spec, candles=candles)
        assert first == second


def test_simulated_tables_have_no_forbidden_broker_or_account_columns() -> None:
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
        "execution_status_as_live",
        "real_pnl",
        "pnl",
        "position_id",
    }
    run_columns = set(SimulatedExecutionRun.__table__.columns.keys())
    fill_columns = set(SimulatedFillEvent.__table__.columns.keys())
    assert run_columns.isdisjoint(forbidden)
    assert fill_columns.isdisjoint(forbidden)


@pytest.mark.asyncio
async def test_simulated_artifacts_labelled_simulated_and_disclaimer_present(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        result = await _create_run(session)
        assert result.run.simulation_mode == "SIMULATED"
        assert result.run.research_status == "research_only"
        assert "SIMULATED execution research only" in result.run.simulation_disclaimer
        assert all(fill.simulation_mode == "SIMULATED" for fill in result.fills)
        assert all("Governance Gate CLOSED" in fill.simulation_disclaimer for fill in result.fills)


@pytest.mark.asyncio
async def test_simulated_records_have_no_real_pnl_or_live_fill_language(prepared_db: None) -> None:
    async with session_scope() as session:
        result = await _create_run(session)
        combined = " ".join(
            [
                str(result.run.assumptions),
                str(result.run.limitations),
                result.run.simulation_disclaimer,
                *[fill.simulation_disclaimer for fill in result.fills],
            ]
        ).lower()
        assert "guaranteed return" not in combined
        assert "live fill" not in combined
        assert "broker fill" not in combined
        assert "not real p&l" in combined
        assert "simulated_units_dimensionless" in str(result.run.assumptions)


@pytest.mark.asyncio
async def test_simulation_policy_and_fill_model_versions_are_immutable(prepared_db: None) -> None:
    async with session_scope() as session:
        result = await _create_run(session)
        actions = list(
            (
                await session.scalars(
                    select(AuditEvent.details).where(
                        AuditEvent.resource_type.in_(
                            ["simulated_execution_run", "simulated_fill_event"]
                        )
                    )
                )
            ).all()
        )
        assert not hasattr(SimulatedExecutionService, "update_run")
        assert result.run.simulation_policy_version == EXECUTION_RESEARCH_POLICY_VERSION
        assert result.run.fill_model_version == FILL_MODEL_VERSION
        assert all(
            item and item.get("fill_model_version") == FILL_MODEL_VERSION
            for item in actions
        )


def test_execution_research_create_path_has_no_live_broker_or_gate_path() -> None:
    root = Path(__file__).resolve().parents[1] / "app"
    paths = [root / "execution_research", root / "api" / "routes" / "execution_research.py"]
    forbidden = (
        "place_order",
        "cancel_order",
        "go_live",
        "live_order",
        "real_account",
        "account_balance",
        "margin",
        "broker.connect",
        "broker.execute",
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
async def test_simulated_execution_api_auth_create_list_detail_and_fills(
    async_client: AsyncClient,
) -> None:
    async with session_scope() as session:
        start, end = await _seed_candles(session)

    unauth = await async_client.get("/api/v1/execution-research/simulated-runs")
    assert unauth.status_code == 401
    headers = await _auth_headers(async_client)
    create = await async_client.post(
        "/api/v1/execution-research/simulated-runs",
        headers=headers,
        json={
            "market_class": "forex",
            "symbol": "EURUSD",
            "timeframe": "M1",
            "as_of_start": start.isoformat(),
            "as_of_end": end.isoformat(),
            "simulated_research_direction": "long_bias",
            "simulated_units": 1.0,
            "simulated_slippage_bps": 0.5,
            "max_fill_events": 2,
            "input_artifact_ids": ["api-test-scope"],
        },
    )
    assert create.status_code == 201, create.text
    payload = create.json()
    run_id = payload["run"]["run_id"]
    assert payload["run"]["simulation_mode"] == "SIMULATED"
    assert len(payload["fills"]) == 2

    listing = await async_client.get("/api/v1/execution-research/simulated-runs", headers=headers)
    assert listing.status_code == 200, listing.text
    assert any(row["run_id"] == run_id for row in listing.json())

    detail = await async_client.get(
        f"/api/v1/execution-research/simulated-runs/{run_id}", headers=headers
    )
    assert detail.status_code == 200, detail.text
    fills = await async_client.get(
        f"/api/v1/execution-research/simulated-runs/{run_id}/fills", headers=headers
    )
    assert fills.status_code == 200, fills.text
    assert len(fills.json()) == 2

    blocked = await async_client.post(
        f"/api/v1/execution-research/simulated-runs/{run_id}/execute",
        headers=headers,
        json={},
    )
    assert blocked.status_code in {404, 405}
