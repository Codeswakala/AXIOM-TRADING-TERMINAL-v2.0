"""W4-U05 Portfolio/Risk Research Analytics report tests."""

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
from app.db.models.portfolio_risk_report import PortfolioRiskReport
from app.institutional_intelligence import (
    PortfolioRiskAssumptions,
    PortfolioRiskReportService,
    PortfolioRiskSeriesSpec,
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
    times = [base + timedelta(minutes=i) for i in range(5)]
    closes = ["1.00", "1.02", "0.99", "1.03", "1.01"]
    for open_time, close in zip(times, closes, strict=True):
        await _candle(session, symbol="EURUSD", open_time=open_time, close=close)
    future_time = times[-1] + timedelta(minutes=1)
    if include_future:
        await _candle(session, symbol="EURUSD", open_time=future_time, close="9.99")
    return times[0], times[-1], future_time


def _assumptions() -> PortfolioRiskAssumptions:
    return PortfolioRiskAssumptions(report_name="hypothetical_market_series_risk")


@pytest.mark.asyncio
async def test_portfolio_risk_no_lookahead_future_candle_excluded_metrics_unchanged(
    prepared_db: None,
) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        start, end, future_time = await _seed_path(session, include_future=True)
        result = await PortfolioRiskReportService(session).create_report(
            series=PortfolioRiskSeriesSpec("forex", "EURUSD", "M1"),
            assumptions=_assumptions(),
            as_of_start=start,
            as_of_end=end,
            actor="pytest",
        )
        report = result.report
        assert result.excluded_future_candle_count == 1
        assert future_time.isoformat() not in report.input_lineage["included_timestamps"]
        assert report.sample_count == 5
        assert report.metrics["max_drawdown"]["sample_count"] == 5
        assert report.input_lineage["linkage_policy"] == (
            "market_series_only_no_account_or_broker_linkage"
        )


@pytest.mark.asyncio
async def test_portfolio_risk_metrics_have_uncertainty_and_economic_usefulness(
    prepared_db: None,
) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        start, end, _ = await _seed_path(session)
        report = (
            await PortfolioRiskReportService(session).create_report(
                series=PortfolioRiskSeriesSpec("forex", "EURUSD", "M1"),
                assumptions=_assumptions(),
                as_of_start=start,
                as_of_end=end,
                actor="pytest",
            )
        ).report
        assert report.artifact_type == "portfolio_risk_report"
        assert report.research_status == "research_only"
        for metric in ("max_drawdown", "realized_volatility", "stress_loss"):
            assert "value" in report.metrics[metric]
            assert report.metrics[metric]["sample_count"] == 5
            assert report.metrics[metric]["uncertainty"]["sample_count"] == 5
        assert report.uncertainty["method"] == "volatility_scaled_interval"
        assert report.economic_usefulness["verdict"] == "not_assessed"
        assert "hypothetical_market_series_research_only" in report.limitations
        assert "not_a_real_portfolio_or_account" in report.limitations
        assert "not_a_guaranteed_return" in report.limitations


@pytest.mark.asyncio
async def test_portfolio_risk_rejects_invalid_bare_metric_assumptions(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        start, end, _ = await _seed_path(session)
        with pytest.raises(ValueError, match="PORTFOLIO_RISK_STRESS_MULTIPLIER_INVALID"):
            await PortfolioRiskReportService(session).create_report(
                series=PortfolioRiskSeriesSpec("forex", "EURUSD", "M1"),
                assumptions=PortfolioRiskAssumptions("bad", stress_multiplier=0.0),
                as_of_start=start,
                as_of_end=end,
                actor="pytest",
            )


@pytest.mark.asyncio
async def test_portfolio_risk_persisted_audited_no_signal_or_model_mutation(
    prepared_db: None,
) -> None:
    from sqlalchemy import select

    from app.db.session import session_scope

    async with session_scope() as session:
        artifact = await _eligible_artifact(session)
        before_statuses = {artifact.id: artifact.status}
        before_signals = len(list((await session.scalars(select(AdvisorySignal))).all()))
        start, end, _ = await _seed_path(session)
        service = PortfolioRiskReportService(session)
        result = await service.create_report(
            series=PortfolioRiskSeriesSpec("forex", "EURUSD", "M1"),
            assumptions=_assumptions(),
            as_of_start=start,
            as_of_end=end,
            actor="pytest",
        )
        report = result.report
        assert await session.get(PortfolioRiskReport, report.id) is not None
        actions = list(
            (
                await session.scalars(
                    select(AuditEvent.action).where(AuditEvent.resource_id == report.id)
                )
            ).all()
        )
        assert "portfolio_risk_report.created" in actions
        await service.assert_no_side_effects(
            model_statuses=before_statuses,
            signal_count=before_signals,
        )
        refreshed = await session.get(ModelArtifact, artifact.id)
        assert refreshed is not None
        assert refreshed.status == before_statuses[artifact.id]


def test_portfolio_risk_schema_has_no_account_broker_position_or_order_linkage() -> None:
    forbidden_columns = {
        "account_id",
        "broker_account_id",
        "position_id",
        "live_position",
        "holding",
        "order_payload",
        "execution_payload",
        "quantity",
        "order_size",
        "position_size",
    }
    assert forbidden_columns.isdisjoint(set(PortfolioRiskReport.__table__.columns.keys()))


@pytest.mark.asyncio
async def test_portfolio_risk_api_auth_read_only_and_returns_metrics(
    async_client: AsyncClient,
) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        start, end, _ = await _seed_path(session)
        report = (
            await PortfolioRiskReportService(session).create_report(
                series=PortfolioRiskSeriesSpec("forex", "EURUSD", "M1"),
                assumptions=_assumptions(),
                as_of_start=start,
                as_of_end=end,
                actor="pytest",
            )
        ).report
        report_id = report.id

    unauth = await async_client.get("/api/v1/intelligence/portfolio-risk-reports")
    assert unauth.status_code == 401
    login = await async_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert login.status_code == 200, login.text
    headers = {"Authorization": f"Bearer {login.json()['tokens']['access_token']}"}
    listed = await async_client.get("/api/v1/intelligence/portfolio-risk-reports", headers=headers)
    assert listed.status_code == 200, listed.text
    rows = listed.json()
    assert any(row["id"] == report_id for row in rows)
    row = next(row for row in rows if row["id"] == report_id)
    assert row["metrics"]["max_drawdown"]["sample_count"] == row["sample_count"]
    assert row["economic_usefulness"]["verdict"] == "not_assessed"
    detail = await async_client.get(
        f"/api/v1/intelligence/portfolio-risk-reports/{report_id}", headers=headers
    )
    assert detail.status_code == 200, detail.text
    # BO-B-04 supersession: the POST generation endpoint now EXISTS.
    # A body-less POST fails request validation (422), no longer 405.
    post = await async_client.post("/api/v1/intelligence/portfolio-risk-reports", headers=headers)
    assert post.status_code == 422


def test_portfolio_risk_modules_use_no_unspiked_dependencies_or_execution_path() -> None:
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
        "execution_payload =",
        "broker_account_id =",
        "account_id =",
        "position_id =",
        "live_position =",
        "advisory_status =",
        "model.status =",
    )
    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for needle in forbidden:
            assert needle not in text
