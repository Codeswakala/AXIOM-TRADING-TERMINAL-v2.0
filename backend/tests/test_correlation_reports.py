"""W4-U02 Correlation Intelligence report tests."""

from __future__ import annotations

from datetime import timedelta
from decimal import Decimal
from pathlib import Path

import pytest
from httpx import AsyncClient

from app.core.time import utc_now
from app.db.models.advisory_signal import AdvisorySignal
from app.db.models.audit import AuditEvent
from app.db.models.correlation_report import CorrelationReport
from app.institutional_intelligence import CorrelationReportService, CorrelationSeriesSpec
from app.repositories.candle_repository import CandleRepository


async def _candle(
    session,
    *,
    symbol: str,
    open_time,
    close: str,
):
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


async def _seed_pair(session, *, include_future: bool = False):  # noqa: ANN001, ANN201
    base = utc_now() - timedelta(minutes=10)
    times = [base + timedelta(minutes=i) for i in range(4)]
    for index, open_time in enumerate(times, start=1):
        await _candle(session, symbol="EURUSD", open_time=open_time, close=str(index))
        await _candle(session, symbol="GBPUSD", open_time=open_time, close=str(index * 2))
    future_time = times[-1] + timedelta(minutes=1)
    if include_future:
        await _candle(session, symbol="EURUSD", open_time=future_time, close="1000")
        await _candle(session, symbol="GBPUSD", open_time=future_time, close="-1000")
    return times[0], times[-1], future_time


@pytest.mark.asyncio
async def test_correlation_no_lookahead_future_candle_excluded_result_unchanged(
    prepared_db: None,
) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        start, end, future_time = await _seed_pair(session, include_future=True)
        result = await CorrelationReportService(session).create_report(
            left=CorrelationSeriesSpec("forex", "EURUSD", "M1"),
            right=CorrelationSeriesSpec("forex", "GBPUSD", "M1"),
            as_of_start=start,
            as_of_end=end,
            actor="pytest",
        )
        report = result.report
        assert result.excluded_future_candle_count == 2
        assert future_time.isoformat() not in report.input_lineage["aligned_timestamps"]
        assert report.sample_count == 4
        assert report.correlation_value == pytest.approx(1.0)
        assert report.uncertainty["sample_count"] == 4


@pytest.mark.asyncio
async def test_correlation_report_has_uncertainty_and_separate_economic_context(
    prepared_db: None,
) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        start, end, _ = await _seed_pair(session)
        report = (
            await CorrelationReportService(session).create_report(
                left=CorrelationSeriesSpec("forex", "EURUSD", "M1"),
                right=CorrelationSeriesSpec("forex", "GBPUSD", "M1"),
                as_of_start=start,
                as_of_end=end,
                actor="pytest",
            )
        ).report
        assert report.artifact_type == "correlation_report"
        assert report.research_status == "research_only"
        assert report.uncertainty["method"] == "fisher_z_interval"
        assert -1.0 <= report.uncertainty["lower"] <= report.uncertainty["upper"] <= 1.0
        assert report.significance["method"] == "not_computed_pure_python_foundation"
        assert report.economic_usefulness["verdict"] == "not_assessed"
        assert "correlation_does_not_imply_causation" in report.limitations
        assert "research_only_not_a_signal" in report.limitations


@pytest.mark.asyncio
async def test_correlation_report_persisted_audited_and_no_signal_side_effect(
    prepared_db: None,
) -> None:
    from sqlalchemy import select

    from app.db.session import session_scope

    async with session_scope() as session:
        start, end, _ = await _seed_pair(session)
        before_signals = list((await session.scalars(select(AdvisorySignal))).all())
        result = await CorrelationReportService(session).create_report(
            left=CorrelationSeriesSpec("forex", "EURUSD", "M1"),
            right=CorrelationSeriesSpec("forex", "GBPUSD", "M1"),
            as_of_start=start,
            as_of_end=end,
            actor="pytest",
        )
        report = result.report
        assert await session.get(CorrelationReport, report.id) is not None
        actions = list(
            (
                await session.scalars(
                    select(AuditEvent.action).where(AuditEvent.resource_id == report.id)
                )
            ).all()
        )
        assert "correlation_report.created" in actions
        after_signals = list((await session.scalars(select(AdvisorySignal))).all())
        assert len(after_signals) == len(before_signals)
        await CorrelationReportService(session).assert_no_signal_side_effect(len(before_signals))


def test_correlation_report_schema_is_inert_no_order_or_signal_payload() -> None:
    forbidden_columns = {
        "order_payload",
        "order_intent",
        "signal_payload",
        "execution_payload",
        "remediation_payload",
        "broker_account_id",
        "quantity",
        "take_profit",
        "stop_loss",
    }
    assert forbidden_columns.isdisjoint(set(CorrelationReport.__table__.columns.keys()))


@pytest.mark.asyncio
async def test_correlation_reports_api_auth_read_only_and_returns_uncertainty(
    async_client: AsyncClient,
) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        start, end, _ = await _seed_pair(session)
        report = (
            await CorrelationReportService(session).create_report(
                left=CorrelationSeriesSpec("forex", "EURUSD", "M1"),
                right=CorrelationSeriesSpec("forex", "GBPUSD", "M1"),
                as_of_start=start,
                as_of_end=end,
                actor="pytest",
            )
        ).report
        report_id = report.id

    unauth = await async_client.get("/api/v1/intelligence/correlation-reports")
    assert unauth.status_code == 401
    login = await async_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert login.status_code == 200, login.text
    headers = {"Authorization": f"Bearer {login.json()['tokens']['access_token']}"}
    listed = await async_client.get("/api/v1/intelligence/correlation-reports", headers=headers)
    assert listed.status_code == 200, listed.text
    rows = listed.json()
    assert any(row["id"] == report_id for row in rows)
    row = next(row for row in rows if row["id"] == report_id)
    assert row["sample_count"] == 4
    assert row["uncertainty"]["sample_count"] == 4
    assert row["economic_usefulness"]["verdict"] == "not_assessed"
    detail = await async_client.get(
        f"/api/v1/intelligence/correlation-reports/{report_id}", headers=headers
    )
    assert detail.status_code == 200, detail.text
    # BO-B-04 supersession: the POST generation endpoint now EXISTS.
    # A body-less POST fails request validation (422), no longer 405.
    post = await async_client.post("/api/v1/intelligence/correlation-reports", headers=headers)
    assert post.status_code == 422


def test_correlation_modules_use_no_unspiked_dependencies_or_execution_path() -> None:
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
        "advisory_status =",
        "model.status =",
    )
    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for needle in forbidden:
            assert needle not in text
