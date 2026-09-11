"""W6-U03 simulated paper research ledger tests."""

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
from app.db.models.simulated_paper_ledger import SimulatedPaperLedgerEntry
from app.db.session import session_scope
from app.execution_research import (
    RESEARCH_STATUS,
    SIMULATED_EXECUTION_RESEARCH_DISCLAIMER,
    SIMULATION_MODE,
    SimulatedExecutionRunSpec,
    SimulatedExecutionService,
    SimulatedPaperLedgerEntryDraft,
    SimulatedPaperLedgerService,
)
from app.repositories.candle_repository import CandleRepository


async def _operator(session: AsyncSession, username: str = "ledger-operator") -> Operator:
    operator = Operator(
        username=username,
        hashed_password="not-used-in-test",
        role="operator",
        is_active=True,
    )
    session.add(operator)
    await session.flush()
    return operator


async def _seed_candles(session: AsyncSession) -> tuple[object, object]:
    base = utc_now() - timedelta(minutes=12)
    closes = ["1.2000", "1.2010", "1.2020"]
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
            source="w6-u03:test",
        )
    return times[0], times[-1]


async def _create_run_and_fill(session: AsyncSession):  # noqa: ANN202
    operator = await _operator(session)
    start, end = await _seed_candles(session)
    result = await SimulatedExecutionService(session).create_run(
        operator_id=operator.id,
        spec=SimulatedExecutionRunSpec(
            market_class="forex",
            symbol="EURUSD",
            timeframe="M1",
            as_of_start=start,  # type: ignore[arg-type]
            as_of_end=end,  # type: ignore[arg-type]
            simulated_research_direction="long_bias",
            simulated_units=1.0,
            simulated_slippage_bps=0.5,
            max_fill_events=1,
            input_artifact_ids=("ledger-test-scope",),
        ),
    )
    return operator, result.run, result.fills[0]


async def _create_ledger_entry(session: AsyncSession) -> SimulatedPaperLedgerEntry:
    operator, run, fill = await _create_run_and_fill(session)
    return await SimulatedPaperLedgerService(session).create_entry(
        operator_id=operator.id,
        draft=SimulatedPaperLedgerEntryDraft(
            run_id=run.run_id,
            simulated_fill_id=fill.simulated_fill_id,
            simulated_exit_value=fill.simulated_fill_price * 1.01,
            uncertainty_width=0.001,
        ),
    )


async def _assert_ledger_audit_no_orphan(session: AsyncSession) -> None:
    stmt = (
        select(SimulatedPaperLedgerEntry.ledger_entry_id)
        .outerjoin(
            AuditEvent,
            and_(
                AuditEvent.resource_type == "simulated_paper_ledger_entry",
                AuditEvent.resource_id == SimulatedPaperLedgerEntry.ledger_entry_id,
                AuditEvent.correlation_id == SimulatedPaperLedgerEntry.audit_correlation_id,
                AuditEvent.action == "simulated_paper_ledger_entry.created",
            ),
        )
        .where(AuditEvent.id.is_(None))
    )
    assert list((await session.scalars(stmt)).all()) == []


async def _assert_lineage_no_orphan(session: AsyncSession) -> None:
    run_stmt = (
        select(SimulatedPaperLedgerEntry.ledger_entry_id)
        .outerjoin(
            SimulatedExecutionRun,
            SimulatedExecutionRun.run_id == SimulatedPaperLedgerEntry.run_id,
        )
        .where(SimulatedExecutionRun.run_id.is_(None))
    )
    fill_stmt = (
        select(SimulatedPaperLedgerEntry.ledger_entry_id)
        .outerjoin(
            SimulatedFillEvent,
            SimulatedFillEvent.simulated_fill_id == SimulatedPaperLedgerEntry.simulated_fill_id,
        )
        .where(SimulatedFillEvent.simulated_fill_id.is_(None))
    )
    operator_stmt = (
        select(SimulatedPaperLedgerEntry.ledger_entry_id)
        .outerjoin(Operator, Operator.id == SimulatedPaperLedgerEntry.operator_id)
        .where(Operator.id.is_(None))
    )
    assert list((await session.scalars(run_stmt)).all()) == []
    assert list((await session.scalars(fill_stmt)).all()) == []
    assert list((await session.scalars(operator_stmt)).all()) == []


@pytest.mark.asyncio
async def test_simulated_paper_ledger_entry_persists_and_audit_no_orphan(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        entry = await _create_ledger_entry(session)
        stored = await session.get(SimulatedPaperLedgerEntry, entry.ledger_entry_id)
        assert stored is not None
        assert stored.simulation_mode == SIMULATION_MODE
        assert stored.research_status == RESEARCH_STATUS
        assert stored.simulation_disclaimer == SIMULATED_EXECUTION_RESEARCH_DISCLAIMER
        await _assert_ledger_audit_no_orphan(session)


@pytest.mark.asyncio
async def test_ledger_entry_references_existing_simulated_run_and_fill_only(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        operator, run, fill = await _create_run_and_fill(session)
        entry = await SimulatedPaperLedgerService(session).create_entry(
            operator_id=operator.id,
            draft=SimulatedPaperLedgerEntryDraft(
                run_id=run.run_id,
                simulated_fill_id=fill.simulated_fill_id,
                simulated_exit_value=fill.simulated_fill_price * 1.01,
            ),
        )
        assert entry.run_id == run.run_id
        assert entry.simulated_fill_id == fill.simulated_fill_id
        await _assert_lineage_no_orphan(session)
        with pytest.raises(ValueError, match="SIMULATED_LEDGER_FILL_REQUIRED"):
            await SimulatedPaperLedgerService(session).create_entry(
                operator_id=operator.id,
                draft=SimulatedPaperLedgerEntryDraft(
                    run_id=run.run_id,
                    simulated_fill_id="missing-fill",
                    simulated_exit_value=fill.simulated_fill_price,
                ),
            )


def test_simulated_paper_ledger_has_no_forbidden_account_or_pnl_columns() -> None:
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
        "execution_status_as_live",
    }
    columns = set(SimulatedPaperLedgerEntry.__table__.columns.keys())
    assert columns.isdisjoint(forbidden)


@pytest.mark.asyncio
async def test_simulated_return_estimate_carries_uncertainty_and_limitations(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        entry = await _create_ledger_entry(session)
        assert isinstance(entry.simulated_return_estimate, float)
        assert entry.uncertainty["method"] == "fixed_simulated_estimate_band"
        assert "lower" in entry.uncertainty
        assert "upper" in entry.uncertainty
        assert entry.limitations
        assert "single_fill_estimate_with_uncertainty" in entry.limitations


@pytest.mark.asyncio
async def test_simulated_ledger_records_have_no_real_pnl_or_realized_language(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        entry = await _create_ledger_entry(session)
        combined = " ".join(
            [
                str(entry.uncertainty),
                str(entry.limitations),
                entry.simulation_disclaimer,
                str(entry.simulated_return_estimate),
            ]
        ).lower()
        assert "guaranteed return" not in combined
        assert "live fill" not in combined
        assert "broker fill" not in combined
        assert "realized" not in combined
        assert "pnl" not in combined
        assert "not real p&l" in combined


@pytest.mark.asyncio
async def test_simulated_ledger_artifacts_labelled_simulated_and_disclaimer_present(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        entry = await _create_ledger_entry(session)
        assert entry.simulation_mode == "SIMULATED"
        assert entry.research_status == "research_only"
        assert "SIMULATED execution research only" in entry.simulation_disclaimer
        assert "Governance Gate CLOSED" in entry.simulation_disclaimer


def test_execution_research_ledger_create_path_has_no_live_broker_or_gate_path() -> None:
    root = Path(__file__).resolve().parents[1] / "app"
    paths = [root / "execution_research", root / "api" / "routes" / "execution_research.py"]
    forbidden = (
        "place_order",
        "broker.connect",
        "broker.execute",
        "go_live",
        "live_order",
        "real_account",
        "account_balance",
        "margin",
        "real_pnl",
        "realized",
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
async def test_simulated_ledger_api_auth_create_list_detail(async_client: AsyncClient) -> None:
    async with session_scope() as session:
        _, run, fill = await _create_run_and_fill(session)
        run_id = run.run_id
        fill_id = fill.simulated_fill_id
        exit_value = fill.simulated_fill_price * 1.01

    unauth = await async_client.get("/api/v1/execution-research/simulated-ledger-entries")
    assert unauth.status_code == 401
    headers = await _auth_headers(async_client)
    create = await async_client.post(
        "/api/v1/execution-research/simulated-ledger-entries",
        headers=headers,
        json={
            "run_id": run_id,
            "simulated_fill_id": fill_id,
            "simulated_exit_value": exit_value,
            "uncertainty_width": 0.001,
        },
    )
    assert create.status_code == 201, create.text
    payload = create.json()
    ledger_id = payload["ledger_entry_id"]
    assert payload["simulation_mode"] == "SIMULATED"
    assert payload["uncertainty"]

    listing = await async_client.get(
        "/api/v1/execution-research/simulated-ledger-entries", headers=headers
    )
    assert listing.status_code == 200, listing.text
    assert any(item["ledger_entry_id"] == ledger_id for item in listing.json())

    detail = await async_client.get(
        f"/api/v1/execution-research/simulated-ledger-entries/{ledger_id}",
        headers=headers,
    )
    assert detail.status_code == 200, detail.text
    blocked = await async_client.post(
        f"/api/v1/execution-research/simulated-ledger-entries/{ledger_id}/execute",
        headers=headers,
        json={},
    )
    assert blocked.status_code in {404, 405}
