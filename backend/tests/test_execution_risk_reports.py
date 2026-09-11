"""W6-U04 execution risk research report tests."""

from __future__ import annotations

from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.audit import AuditEvent
from app.db.models.execution_risk_report import ExecutionRiskResearchReport
from app.db.models.simulated_execution import SimulatedExecutionRun, SimulatedFillEvent
from app.db.models.simulated_paper_ledger import SimulatedPaperLedgerEntry
from app.db.session import session_scope
from app.execution_research import (
    RESEARCH_STATUS,
    SIMULATED_EXECUTION_RESEARCH_DISCLAIMER,
    SIMULATION_MODE,
    ExecutionRiskResearchReportDraft,
    ExecutionRiskResearchReportService,
)
from tests.test_simulated_paper_ledger import _create_ledger_entry


async def _risk_report(session: AsyncSession) -> ExecutionRiskResearchReport:
    ledger = await _create_ledger_entry(session)
    return await ExecutionRiskResearchReportService(session).create_report(
        draft=ExecutionRiskResearchReportDraft(
            input_artifact_ids=(ledger.run_id, ledger.simulated_fill_id, ledger.ledger_entry_id)
        ),
        actor="pytest",
    )


async def _assert_report_audit_no_orphan(session: AsyncSession) -> None:
    stmt = (
        select(ExecutionRiskResearchReport.report_id)
        .outerjoin(
            AuditEvent,
            and_(
                AuditEvent.resource_type == "execution_risk_research_report",
                AuditEvent.resource_id == ExecutionRiskResearchReport.report_id,
                AuditEvent.correlation_id == ExecutionRiskResearchReport.audit_correlation_id,
                AuditEvent.action == "execution_risk_research_report.created",
            ),
        )
        .where(AuditEvent.id.is_(None))
    )
    assert list((await session.scalars(stmt)).all()) == []


async def _count(session: AsyncSession, model: type[object]) -> int:
    return int((await session.execute(select(func.count()).select_from(model))).scalar_one())


@pytest.mark.asyncio
async def test_execution_risk_research_report_persists_and_audit_no_orphan(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        report = await _risk_report(session)
        stored = await session.get(ExecutionRiskResearchReport, report.report_id)
        assert stored is not None
        assert stored.simulation_mode == SIMULATION_MODE
        assert stored.research_status == RESEARCH_STATUS
        assert stored.simulation_disclaimer == SIMULATED_EXECUTION_RESEARCH_DISCLAIMER
        assert stored.risk_metrics["simulated_fill_count"]["value"] >= 1
        await _assert_report_audit_no_orphan(session)


@pytest.mark.asyncio
async def test_execution_risk_report_triggers_nothing_and_writes_report_only(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        ledger = await _create_ledger_entry(session)
        before_runs = await _count(session, SimulatedExecutionRun)
        before_fills = await _count(session, SimulatedFillEvent)
        before_ledgers = await _count(session, SimulatedPaperLedgerEntry)
        before_reports = await _count(session, ExecutionRiskResearchReport)
        report = await ExecutionRiskResearchReportService(session).create_report(
            draft=ExecutionRiskResearchReportDraft(input_artifact_ids=(ledger.ledger_entry_id,)),
            actor="pytest",
        )
        assert report.report_id
        assert await _count(session, SimulatedExecutionRun) == before_runs
        assert await _count(session, SimulatedFillEvent) == before_fills
        assert await _count(session, SimulatedPaperLedgerEntry) == before_ledgers
        assert await _count(session, ExecutionRiskResearchReport) == before_reports + 1
        assert not any("size" in key for key in report.risk_metrics)


def test_execution_risk_report_has_no_account_capital_margin_or_sizing_columns() -> None:
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
        "recommended_size",
        "sizing_directive",
        "execution_status_as_live",
    }
    columns = set(ExecutionRiskResearchReport.__table__.columns.keys())
    assert columns.isdisjoint(forbidden)


@pytest.mark.asyncio
async def test_execution_risk_report_carries_uncertainty_and_limitations(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        report = await _risk_report(session)
        assert report.uncertainty["method"] == "sample_range_or_single_sample_limitation"
        assert report.uncertainty["sample_count"] >= 1
        assert report.uncertainty["metrics"]
        assert report.limitations
        assert "economic_usefulness_not_assessed" in report.limitations


@pytest.mark.asyncio
async def test_execution_risk_report_separates_statistical_from_economic_usefulness(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        report = await _risk_report(session)
        assert "simulated_average_slippage_bps" in report.risk_metrics
        assert report.economic_usefulness["verdict"] == "not_assessed"
        assert "economic_usefulness" not in report.risk_metrics
        assert "risk_metrics" not in report.economic_usefulness


@pytest.mark.asyncio
async def test_execution_risk_report_has_no_real_pnl_or_guaranteed_language(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        report = await _risk_report(session)
        combined = " ".join(
            [
                str(report.risk_metrics),
                str(report.uncertainty),
                str(report.limitations),
                str(report.economic_usefulness),
                report.simulation_disclaimer,
            ]
        ).lower()
        assert "guaranteed" not in combined
        assert "profit" not in combined
        assert "realized" not in combined
        assert "real_pnl" not in combined
        assert "pnl" not in combined
        assert "not real p&l" in combined


def test_execution_research_risk_create_path_has_no_live_broker_or_gate_path() -> None:
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
async def test_execution_risk_report_api_auth_create_list_detail(async_client: AsyncClient) -> None:
    async with session_scope() as session:
        ledger = await _create_ledger_entry(session)
        ledger_id = ledger.ledger_entry_id

    unauth = await async_client.get("/api/v1/execution-research/execution-risk-reports")
    assert unauth.status_code == 401
    headers = await _auth_headers(async_client)
    create = await async_client.post(
        "/api/v1/execution-research/execution-risk-reports",
        headers=headers,
        json={"input_artifact_ids": [ledger_id]},
    )
    assert create.status_code == 201, create.text
    payload = create.json()
    report_id = payload["report_id"]
    assert payload["simulation_mode"] == "SIMULATED"
    assert payload["uncertainty"]
    assert payload["economic_usefulness"]["verdict"] == "not_assessed"

    listing = await async_client.get(
        "/api/v1/execution-research/execution-risk-reports", headers=headers
    )
    assert listing.status_code == 200, listing.text
    assert any(item["report_id"] == report_id for item in listing.json())

    detail = await async_client.get(
        f"/api/v1/execution-research/execution-risk-reports/{report_id}",
        headers=headers,
    )
    assert detail.status_code == 200, detail.text
    blocked = await async_client.post(
        f"/api/v1/execution-research/execution-risk-reports/{report_id}/execute",
        headers=headers,
        json={},
    )
    assert blocked.status_code in {404, 405}
