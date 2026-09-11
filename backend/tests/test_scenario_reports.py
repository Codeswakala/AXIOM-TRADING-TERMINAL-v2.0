"""W4-U04 Scenario Simulation report tests."""

from __future__ import annotations

from datetime import timedelta
from decimal import Decimal
from pathlib import Path

import pytest
from httpx import AsyncClient

from app.core.time import utc_now
from app.db.models.advisory_signal import AdvisorySignal
from app.db.models.audit import AuditEvent
from app.db.models.model_artifact import ModelArtifact
from app.db.models.scenario_report import ScenarioReport
from app.institutional_intelligence import (
    ScenarioAssumptions,
    ScenarioReportService,
    ScenarioSeriesSpec,
)
from app.repositories.candle_repository import CandleRepository
from tests.test_live_inference_gate import _eligible_artifact


async def _candle(session, *, symbol: str, open_time, close: str):
    return await CandleRepository(session).upsert_ohlcv(
        market_class="forex",
        symbol=symbol,
        timeframe="M1",
        open_time=open_time,
        open=Decimal(close),
        high=Decimal(close) + Decimal("0.0100"),
        low=Decimal(close) - Decimal("0.0100"),
        close=Decimal(close),
        volume=Decimal("1"),
        source="live:simulated",
    )


async def _seed_path(session, *, include_future: bool = False):
    base = utc_now() - timedelta(minutes=10)
    times = [base + timedelta(minutes=i) for i in range(4)]
    closes = ["1.00", "1.01", "1.02", "1.03"]
    for open_time, close in zip(times, closes, strict=True):
        await _candle(session, symbol="EURUSD", open_time=open_time, close=close)
    future_time = times[-1] + timedelta(minutes=1)
    if include_future:
        await _candle(session, symbol="EURUSD", open_time=future_time, close="9.99")
    return times[0], times[-1], future_time


def _assumptions() -> ScenarioAssumptions:
    return ScenarioAssumptions(
        scenario_name="hypothetical_minus_two_percent",
        shock_return=-0.02,
        horizon_bars=3,
        volatility_multiplier=1.0,
    )


@pytest.mark.asyncio
async def test_scenario_no_lookahead_future_candle_excluded_result_unchanged(
    prepared_db: None,
) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        start, end, future_time = await _seed_path(session, include_future=True)
        result = await ScenarioReportService(session).create_report(
            series=ScenarioSeriesSpec("forex", "EURUSD", "M1"),
            assumptions=_assumptions(),
            as_of_start=start,
            as_of_end=end,
            actor="pytest",
        )
        report = result.report
        assert result.excluded_future_candle_count == 1
        assert future_time.isoformat() not in report.input_lineage["included_timestamps"]
        assert report.sample_count == 4
        assert report.scenario_result["hypothetical_return"] == pytest.approx(-0.02)
        assert report.uncertainty["sample_count"] == 4


@pytest.mark.asyncio
async def test_scenario_report_hypothetical_uncertainty_assumptions_and_economics(
    prepared_db: None,
) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        start, end, _ = await _seed_path(session)
        report = (
            await ScenarioReportService(session).create_report(
                series=ScenarioSeriesSpec("forex", "EURUSD", "M1"),
                assumptions=_assumptions(),
                as_of_start=start,
                as_of_end=end,
                actor="pytest",
            )
        ).report
        assert report.artifact_type == "scenario_report"
        assert report.research_status == "research_only"
        assert report.uncertainty["method"] == "historical_volatility_band"
        assert report.assumptions["scenario_name"] == "hypothetical_minus_two_percent"
        assert "baseline_returns" in report.inputs
        assert report.economic_usefulness["verdict"] == "not_assessed"
        assert "hypothetical_counterfactual_research_only" in report.limitations
        assert "not_a_prediction" in report.limitations
        assert "not_a_trade_instruction" in report.limitations


@pytest.mark.asyncio
async def test_scenario_rejects_bare_invalid_scenario_without_uncertainty_inputs(
    prepared_db: None,
) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        start, end, _ = await _seed_path(session)
        with pytest.raises(ValueError, match="SCENARIO_HORIZON_INVALID"):
            await ScenarioReportService(session).create_report(
                series=ScenarioSeriesSpec("forex", "EURUSD", "M1"),
                assumptions=ScenarioAssumptions("bad", -0.02, 0),
                as_of_start=start,
                as_of_end=end,
                actor="pytest",
            )


@pytest.mark.asyncio
async def test_scenario_report_persisted_audited_no_signal_or_model_mutation(
    prepared_db: None,
) -> None:
    from sqlalchemy import select

    from app.db.session import session_scope

    async with session_scope() as session:
        artifact = await _eligible_artifact(session)
        before_statuses = {artifact.id: artifact.status}
        before_signals = len(list((await session.scalars(select(AdvisorySignal))).all()))
        start, end, _ = await _seed_path(session)
        service = ScenarioReportService(session)
        result = await service.create_report(
            series=ScenarioSeriesSpec("forex", "EURUSD", "M1"),
            assumptions=_assumptions(),
            as_of_start=start,
            as_of_end=end,
            actor="pytest",
        )
        report = result.report
        assert await session.get(ScenarioReport, report.id) is not None
        actions = list(
            (
                await session.scalars(
                    select(AuditEvent.action).where(AuditEvent.resource_id == report.id)
                )
            ).all()
        )
        assert "scenario_report.created" in actions
        await service.assert_no_side_effects(
            model_statuses=before_statuses,
            signal_count=before_signals,
        )
        refreshed = await session.get(ModelArtifact, artifact.id)
        assert refreshed is not None
        assert refreshed.status == before_statuses[artifact.id]


def test_scenario_report_schema_is_inert_no_order_sizing_or_signal_payload() -> None:
    forbidden_columns = {
        "order_payload",
        "order_intent",
        "signal_payload",
        "execution_payload",
        "remediation_payload",
        "broker_account_id",
        "quantity",
        "position_size",
        "order_size",
        "take_profit",
        "stop_loss",
    }
    assert forbidden_columns.isdisjoint(set(ScenarioReport.__table__.columns.keys()))


@pytest.mark.asyncio
async def test_scenario_reports_api_auth_read_only_and_returns_assumptions(
    async_client: AsyncClient,
) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        start, end, _ = await _seed_path(session)
        report = (
            await ScenarioReportService(session).create_report(
                series=ScenarioSeriesSpec("forex", "EURUSD", "M1"),
                assumptions=_assumptions(),
                as_of_start=start,
                as_of_end=end,
                actor="pytest",
            )
        ).report
        report_id = report.id

    unauth = await async_client.get("/api/v1/intelligence/scenario-reports")
    assert unauth.status_code == 401
    login = await async_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert login.status_code == 200, login.text
    headers = {"Authorization": f"Bearer {login.json()['tokens']['access_token']}"}
    listed = await async_client.get("/api/v1/intelligence/scenario-reports", headers=headers)
    assert listed.status_code == 200, listed.text
    rows = listed.json()
    assert any(row["id"] == report_id for row in rows)
    row = next(row for row in rows if row["id"] == report_id)
    assert row["uncertainty"]["sample_count"] == row["sample_count"]
    assert row["economic_usefulness"]["verdict"] == "not_assessed"
    detail = await async_client.get(
        f"/api/v1/intelligence/scenario-reports/{report_id}", headers=headers
    )
    assert detail.status_code == 200, detail.text
    # BO-B-04 supersession: the POST generation endpoint now EXISTS.
    # A body-less POST fails request validation (422), no longer 405.
    post = await async_client.post("/api/v1/intelligence/scenario-reports", headers=headers)
    assert post.status_code == 422


def test_scenario_modules_use_no_unspiked_dependencies_or_execution_path() -> None:
    root = Path(__file__).resolve().parents[1] / "app" / "institutional_intelligence"
    forbidden = (
        "import sklearn",
        "import statsmodels",
        "place_order",
        "cancel_order",
        "broker.",
        "emit_signal",
        "live_signal",
        "order_payload =",
        "remediation_payload =",
        "signal_payload =",
        "advisory_status =",
        "model.status =",
    )
    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for needle in forbidden:
            assert needle not in text
