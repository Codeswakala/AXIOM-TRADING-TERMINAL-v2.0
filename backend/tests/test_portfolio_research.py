"""W7-U06 portfolio research dashboard and reporting tests."""

from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

import pytest
from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import hash_password
from app.core.time import utc_now
from app.db.models.operator import Operator
from app.db.models.simulated_execution import SimulatedExecutionRun
from app.db.session import session_scope
from app.institutional_platform import PortfolioResearchService


async def _operator(session: AsyncSession, *, role: str = "operator") -> Operator:
    operator = Operator(
        username=f"portfolio-research-{role}-{uuid4().hex[:10]}",
        hashed_password=hash_password("operator-pass-123"),
        role=role,
        is_active=True,
    )
    session.add(operator)
    await session.flush()
    return operator


async def _simulated_run(session: AsyncSession, *, operator_id: str) -> SimulatedExecutionRun:
    run = SimulatedExecutionRun(
        run_id=str(uuid4()),
        created_at=utc_now(),
        operator_id=operator_id,
        simulation_mode="SIMULATED",
        simulation_policy_version="w7-u06.test.policy.v1",
        input_artifact_ids=[str(uuid4())],
        replay_scope={"scope": "test_fixture"},
        fill_model_name="none",
        fill_model_version="none",
        assumptions={"fixture": True},
        limitations=["simulated_research_only"],
        research_status="research_only",
        simulation_disclaimer="SIMULATED research artifact only.",
        audit_correlation_id=str(uuid4()),
    )
    session.add(run)
    await session.flush()
    return run


@pytest.mark.asyncio
async def test_portfolio_dashboard_aggregates_existing_artifacts_read_only(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        operator = await _operator(session)
        run = await _simulated_run(session, operator_id=operator.id)
        before_count = (
            await session.execute(select(func.count()).select_from(SimulatedExecutionRun))
        ).scalar_one()
        dashboard = await PortfolioResearchService(session).dashboard(operator_id=operator.id)
        after_count = (
            await session.execute(select(func.count()).select_from(SimulatedExecutionRun))
        ).scalar_one()
        assert before_count == after_count
        assert dashboard["operator_id"] == operator.id
        assert run.run_id in dashboard["source_artifact_ids"]
        run_card = next(
            card
            for card in dashboard["aggregate_cards"]
            if card["key"] == "simulated_research_runs"
        )
        assert run_card["value"] == 1
        assert run_card["sample_count"] == 1
        assert run.run_id in run_card["source_artifact_ids"]


def test_portfolio_and_reports_have_no_real_account_or_pnl_field_or_label() -> None:
    forbidden = (
        "real_account_balance",
        "account_balance",
        "broker_account_id",
        "account_id",
        "position_id",
        "live_position_id",
        "real_pnl",
        "realized_pnl",
        "unrealized_pnl",
        "margin",
        "capital",
        "real_capital",
        "order_payload",
        "execution_status",
        "gate_state",
        "open_gate",
        "allow_execution",
    )
    root = Path(__file__).resolve().parents[2]
    page_text = (root / "frontend" / "src" / "components" / "terminal" / "docks" / "PortfolioResearchPanel.tsx").read_text(
        encoding="utf-8"
    )
    api_path = root / "backend" / "app" / "institutional_platform" / "portfolio_research.py"
    api_text = api_path.read_text(encoding="utf-8")
    combined = f"{page_text}\n{api_text}".lower()
    assert not any(item in combined for item in forbidden)
    assert "p&l" not in combined
    assert " balance" not in combined
    assert " account" not in combined


@pytest.mark.asyncio
async def test_reports_carry_uncertainty_limitations_and_separate_economic_usefulness(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        operator = await _operator(session)
        await _simulated_run(session, operator_id=operator.id)
        report = await PortfolioResearchService(session).advanced_report(operator_id=operator.id)
        assert report["economic_usefulness"]["verdict"] == "not_assessed"
        assert report["limitations"]
        assert report["sections"]
        for section in report["sections"]:
            figure = section["figure"]
            assert "uncertainty" in figure
            assert "sample_count" in figure
            assert section["economic_usefulness"]["verdict"] == "not_assessed"


@pytest.mark.asyncio
async def test_reports_have_no_real_pnl_or_guaranteed_return_language(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        operator = await _operator(session)
        await _simulated_run(session, operator_id=operator.id)
        report = await PortfolioResearchService(session).advanced_report(operator_id=operator.id)
        text = json.dumps(report).lower()
        forbidden_phrases = (
            "real_pnl",
            "p&l",
            "guaranteed return",
            "guaranteed outcome",
            "profit guaranteed",
        )
        assert not any(phrase in text for phrase in forbidden_phrases)


@pytest.mark.asyncio
async def test_report_full_scope_included_no_cherry_picking(prepared_db: None) -> None:
    async with session_scope() as session:
        operator = await _operator(session)
        run_a = await _simulated_run(session, operator_id=operator.id)
        run_b = await _simulated_run(session, operator_id=operator.id)
        report = await PortfolioResearchService(session).advanced_report(operator_id=operator.id)
        source_ids = set(report["source_artifact_ids"])
        assert {run_a.run_id, run_b.run_id}.issubset(source_ids)
        scope_ids = set(report["included_scope"]["artifact_source_ids"])
        assert source_ids == scope_ids
        first_hash = report["report_hash"]
        second = await PortfolioResearchService(session).advanced_report(operator_id=operator.id)
        assert second["report_hash"] == first_hash


@pytest.mark.asyncio
async def test_portfolio_and_reports_are_operator_scoped_two_operator(
    async_client: AsyncClient,
) -> None:
    async with session_scope() as session:
        operator_a = await _operator(session)
        operator_b = await _operator(session)
        run_a = await _simulated_run(session, operator_id=operator_a.id)
        run_b = await _simulated_run(session, operator_id=operator_b.id)
        username_a = operator_a.username
        username_b = operator_b.username
        operator_a_id = operator_a.id
        operator_b_id = operator_b.id

    headers_a = await _headers(async_client, username_a)
    headers_b = await _headers(async_client, username_b)
    dashboard_a = await async_client.get(
        "/api/v1/institutional-platform/portfolio-research/dashboard", headers=headers_a
    )
    assert dashboard_a.status_code == 200, dashboard_a.text
    assert dashboard_a.json()["operator_id"] == operator_a_id
    assert run_a.run_id in dashboard_a.json()["source_artifact_ids"]

    dashboard_b = await async_client.get(
        "/api/v1/institutional-platform/portfolio-research/dashboard", headers=headers_b
    )
    assert dashboard_b.status_code == 200, dashboard_b.text
    payload_b = dashboard_b.json()
    assert payload_b["operator_id"] == operator_b_id
    assert run_b.run_id in payload_b["source_artifact_ids"]
    assert run_a.run_id not in payload_b["source_artifact_ids"]

    report_b = await async_client.get(
        "/api/v1/institutional-platform/portfolio-research/report", headers=headers_b
    )
    assert report_b.status_code == 200, report_b.text
    assert run_a.run_id not in report_b.json()["source_artifact_ids"]
    assert run_b.run_id in report_b.json()["source_artifact_ids"]


@pytest.mark.asyncio
async def test_portfolio_and_reports_have_no_secret_or_pii_markers(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        operator = await _operator(session)
        await _simulated_run(session, operator_id=operator.id)
        dashboard = await PortfolioResearchService(session).dashboard(operator_id=operator.id)
        report = await PortfolioResearchService(session).advanced_report(operator_id=operator.id)
        text = json.dumps({"dashboard": dashboard, "report": report}).lower()
        forbidden = (
            "access_token",
            "refresh_token",
            "jwt",
            "password",
            "secret",
            "api_key",
            "private_key",
            "hashed_password",
        )
        assert not any(marker in text for marker in forbidden)


def test_gate_remains_closed_for_wave7() -> None:
    from app.external_integration.broker import governance_gate

    assert governance_gate.broker_integration_authorized is False
    assert governance_gate.execution_authorized is False


async def _headers(async_client: AsyncClient, username: str) -> dict[str, str]:
    login = await async_client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": "operator-pass-123"},
    )
    assert login.status_code == 200, login.text
    return {"Authorization": f"Bearer {login.json()['tokens']['access_token']}"}
