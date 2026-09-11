"""W6-U06 simulated execution analytics report tests."""

from __future__ import annotations

from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.audit import AuditEvent
from app.db.models.execution_experiment import ExecutionResearchExperiment
from app.db.models.simulated_execution import SimulatedFillEvent
from app.db.models.simulated_execution_analytics_report import SimulatedExecutionAnalyticsReport
from app.db.models.simulated_paper_ledger import SimulatedPaperLedgerEntry
from app.db.session import session_scope
from app.execution_research import (
    RESEARCH_STATUS,
    SIMULATED_EXECUTION_RESEARCH_DISCLAIMER,
    SIMULATION_MODE,
    SimulatedExecutionAnalyticsReportDraft,
    SimulatedExecutionAnalyticsReportService,
)
from tests.test_execution_experiments import _create_experiment


async def _source_ids(session: AsyncSession) -> tuple[str, ...]:
    experiment, _ = await _create_experiment(session)
    fill_id = experiment.replay_input_lineage["simulated_fill_ids"][0]
    ledger_id = experiment.replay_input_lineage["simulated_ledger_entry_ids"][0]
    return (fill_id, ledger_id, experiment.experiment_id)


async def _report(session: AsyncSession) -> SimulatedExecutionAnalyticsReport:
    source_ids = await _source_ids(session)
    return await SimulatedExecutionAnalyticsReportService(session).create_report(
        draft=SimulatedExecutionAnalyticsReportDraft(source_artifact_ids=source_ids),
        actor="pytest",
    )


async def _assert_report_audit_no_orphan(session: AsyncSession) -> None:
    stmt = (
        select(SimulatedExecutionAnalyticsReport.report_id)
        .outerjoin(
            AuditEvent,
            and_(
                AuditEvent.resource_type == "simulated_execution_analytics_report",
                AuditEvent.resource_id == SimulatedExecutionAnalyticsReport.report_id,
                AuditEvent.correlation_id == SimulatedExecutionAnalyticsReport.audit_correlation_id,
                AuditEvent.action == "simulated_execution_analytics_report.created",
            ),
        )
        .where(AuditEvent.id.is_(None))
    )
    assert list((await session.scalars(stmt)).all()) == []


async def _assert_lineage_no_orphan(
    session: AsyncSession, report: SimulatedExecutionAnalyticsReport
) -> None:
    for source_id in report.source_artifact_ids:
        fill = await session.get(SimulatedFillEvent, source_id)
        ledger = await session.get(SimulatedPaperLedgerEntry, source_id)
        experiment = await session.get(ExecutionResearchExperiment, source_id)
        assert fill is not None or ledger is not None or experiment is not None


@pytest.mark.asyncio
async def test_simulated_execution_analytics_report_persists_and_audit_no_orphan(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        report = await _report(session)
        stored = await session.get(SimulatedExecutionAnalyticsReport, report.report_id)
        assert stored is not None
        assert stored.simulation_mode == SIMULATION_MODE
        assert stored.research_status == RESEARCH_STATUS
        assert stored.simulation_disclaimer == SIMULATED_EXECUTION_RESEARCH_DISCLAIMER
        assert stored.report_hash
        await _assert_report_audit_no_orphan(session)


@pytest.mark.asyncio
async def test_analytics_report_includes_full_declared_scope_no_cherry_picking(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        report = await _report(session)
        declared = sorted(report.included_scope["declared_source_artifact_ids"])
        analyzed = sorted(report.included_scope["analyzed_source_artifact_ids"])
        assert analyzed == declared
        assert sorted(report.source_artifact_ids) == declared
        assert report.sample_count == len(declared)
        assert report.included_scope["full_scope_included"] is True
        await _assert_lineage_no_orphan(session, report)


@pytest.mark.asyncio
async def test_analytics_metrics_carry_uncertainty_or_insufficient_sample_limitation(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        report = await _report(session)
        metric_uncertainty = report.uncertainty["metrics"]
        assert set(metric_uncertainty) == set(report.metrics)
        for key, uncertainty in metric_uncertainty.items():
            assert "method" in uncertainty, key
            assert "sample_count" in uncertainty, key
            if uncertainty["sample_count"] <= 1:
                assert "limitation" in uncertainty, key
            else:
                assert "lower" in uncertainty and "upper" in uncertainty, key


@pytest.mark.asyncio
async def test_analytics_report_separates_statistical_from_economic_usefulness(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        report = await _report(session)
        assert "simulated_average_return_estimate" in report.metrics
        assert report.economic_usefulness["verdict"] == "not_assessed"
        assert "economic_usefulness" not in report.metrics
        assert "metrics" not in report.economic_usefulness


@pytest.mark.asyncio
async def test_analytics_report_hash_is_deterministic_and_recomputable(prepared_db: None) -> None:
    async with session_scope() as session:
        report = await _report(session)
        service = SimulatedExecutionAnalyticsReportService(session)
        recomputed = service.compute_report_hash(
            analytics_type=report.analytics_type,
            included_scope=report.included_scope,
            source_artifact_ids=tuple(report.source_artifact_ids),
        )
        assert recomputed == report.report_hash
        assert len(report.report_hash) == 64


@pytest.mark.asyncio
async def test_analytics_report_has_no_real_pnl_or_guaranteed_return_language(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        report = await _report(session)
        combined = " ".join(
            [
                str(report.metrics),
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


def test_analytics_report_has_no_forbidden_account_pnl_or_sizing_columns() -> None:
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
        "guaranteed_return",
        "position_size",
        "order_size",
        "execution_status_as_live",
    }
    assert set(SimulatedExecutionAnalyticsReport.__table__.columns.keys()).isdisjoint(forbidden)


def test_execution_research_analytics_create_path_has_no_live_broker_or_gate_path() -> None:
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
async def test_simulated_analytics_report_api_auth_create_list_detail(
    async_client: AsyncClient,
) -> None:
    async with session_scope() as session:
        source_ids = await _source_ids(session)

    unauth = await async_client.get("/api/v1/execution-research/simulated-analytics-reports")
    assert unauth.status_code == 401
    headers = await _auth_headers(async_client)
    create = await async_client.post(
        "/api/v1/execution-research/simulated-analytics-reports",
        headers=headers,
        json={"source_artifact_ids": list(source_ids), "analytics_type": "return_estimate"},
    )
    assert create.status_code == 201, create.text
    payload = create.json()
    report_id = payload["report_id"]
    assert payload["simulation_mode"] == "SIMULATED"
    assert payload["report_hash"]
    assert payload["economic_usefulness"]["verdict"] == "not_assessed"

    listing = await async_client.get(
        "/api/v1/execution-research/simulated-analytics-reports", headers=headers
    )
    assert listing.status_code == 200, listing.text
    assert any(item["report_id"] == report_id for item in listing.json())

    detail = await async_client.get(
        f"/api/v1/execution-research/simulated-analytics-reports/{report_id}",
        headers=headers,
    )
    assert detail.status_code == 200, detail.text
    blocked = await async_client.post(
        f"/api/v1/execution-research/simulated-analytics-reports/{report_id}/execute",
        headers=headers,
        json={},
    )
    assert blocked.status_code in {404, 405}
