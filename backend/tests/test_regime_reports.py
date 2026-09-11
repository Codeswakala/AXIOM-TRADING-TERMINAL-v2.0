"""W4-U03 Regime Detection report tests."""

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
from app.db.models.regime_report import RegimeReport
from app.institutional_intelligence import RegimeReportService, RegimeSeriesSpec
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


async def _seed_trend(session, *, symbol: str = "EURUSD", include_future: bool = False):
    base = utc_now() - timedelta(minutes=10)
    times = [base + timedelta(minutes=i) for i in range(5)]
    closes = ["1.00", "1.02", "1.04", "1.06", "1.08"]
    for open_time, close in zip(times, closes, strict=True):
        await _candle(session, symbol=symbol, open_time=open_time, close=close)
    future_time = times[-1] + timedelta(minutes=1)
    if include_future:
        await _candle(session, symbol=symbol, open_time=future_time, close="0.50")
    return times[0], times[-1], future_time


@pytest.mark.asyncio
async def test_regime_no_lookahead_future_candle_excluded_label_unchanged(
    prepared_db: None,
) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        start, end, future_time = await _seed_trend(session, include_future=True)
        result = await RegimeReportService(session).create_report(
            series=RegimeSeriesSpec("forex", "EURUSD", "M1"),
            as_of_start=start,
            as_of_end=end,
            actor="pytest",
        )
        report = result.report
        assert result.excluded_future_candle_count == 1
        assert future_time.isoformat() not in report.input_lineage["included_timestamps"]
        assert report.regime_label == "trend"
        assert report.evidence["excluded_future_candle_count"] == 1
        assert report.sample_count == 5


@pytest.mark.asyncio
async def test_regime_report_has_confidence_uncertainty_and_explainable_evidence(
    prepared_db: None,
) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        start, end, _ = await _seed_trend(session)
        report = (
            await RegimeReportService(session).create_report(
                series=RegimeSeriesSpec("forex", "EURUSD", "M1"),
                as_of_start=start,
                as_of_end=end,
                actor="pytest",
            )
        ).report
        assert report.artifact_type == "regime_report"
        assert report.research_status == "research_only"
        assert report.confidence >= 0.5
        assert report.uncertainty["method"] == "threshold_margin_confidence_band"
        assert report.uncertainty["sample_count"] == report.sample_count
        assert "normalized_features" in report.evidence
        assert "thresholds" in report.evidence
        assert report.economic_meaning["verdict"] == "not_assessed"
        assert "regime_is_research_context_not_signal" in report.limitations
        assert "normalized_features_exclude_symbol_identity" in report.limitations


def test_regime_market_agnostic_same_normalized_inputs_same_label_without_symbol_feature() -> None:
    service = RegimeReportService.__new__(RegimeReportService)
    features_a = service.features_from_closes([1.00, 1.02, 1.04, 1.06, 1.08])
    features_b = service.features_from_closes([100.0, 102.0, 104.0, 106.0, 108.0])
    assert features_a == features_b
    class_a = service.classify_features(features_a)
    class_b = service.classify_features(features_b)
    assert class_a.label == class_b.label == "trend"

    with pytest.raises(ValueError, match="REGIME_CONFIDENCE_REQUIRED"):
        service.classify_features(features_a.__class__(0.0, 0.0, 0.0, 3))


@pytest.mark.asyncio
async def test_regime_report_persisted_audited_no_signal_or_model_mutation(
    prepared_db: None,
) -> None:
    from sqlalchemy import select

    from app.db.session import session_scope

    async with session_scope() as session:
        artifact = await _eligible_artifact(session)
        before_statuses = {artifact.id: artifact.status}
        before_signals = len(list((await session.scalars(select(AdvisorySignal))).all()))
        start, end, _ = await _seed_trend(session)
        service = RegimeReportService(session)
        result = await service.create_report(
            series=RegimeSeriesSpec("forex", "EURUSD", "M1"),
            as_of_start=start,
            as_of_end=end,
            actor="pytest",
        )
        report = result.report
        assert await session.get(RegimeReport, report.id) is not None
        actions = list(
            (
                await session.scalars(
                    select(AuditEvent.action).where(AuditEvent.resource_id == report.id)
                )
            ).all()
        )
        assert "regime_report.created" in actions
        await service.assert_no_side_effects(
            model_statuses=before_statuses,
            signal_count=before_signals,
        )
        refreshed = await session.get(ModelArtifact, artifact.id)
        assert refreshed is not None
        assert refreshed.status == before_statuses[artifact.id]
        assert refreshed.advisory_status == artifact.advisory_status


def test_regime_report_schema_is_inert_no_order_remediation_or_signal_payload() -> None:
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
    assert forbidden_columns.isdisjoint(set(RegimeReport.__table__.columns.keys()))


@pytest.mark.asyncio
async def test_regime_reports_api_auth_read_only_and_returns_evidence(
    async_client: AsyncClient,
) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        start, end, _ = await _seed_trend(session)
        report = (
            await RegimeReportService(session).create_report(
                series=RegimeSeriesSpec("forex", "EURUSD", "M1"),
                as_of_start=start,
                as_of_end=end,
                actor="pytest",
            )
        ).report
        report_id = report.id

    unauth = await async_client.get("/api/v1/intelligence/regime-reports")
    assert unauth.status_code == 401
    login = await async_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert login.status_code == 200, login.text
    headers = {"Authorization": f"Bearer {login.json()['tokens']['access_token']}"}
    listed = await async_client.get("/api/v1/intelligence/regime-reports", headers=headers)
    assert listed.status_code == 200, listed.text
    rows = listed.json()
    assert any(row["id"] == report_id for row in rows)
    row = next(row for row in rows if row["id"] == report_id)
    assert row["regime_label"] == "trend"
    assert row["uncertainty"]["sample_count"] == row["sample_count"]
    assert row["evidence"]["feature_policy"] == "normalized_features_no_symbol_identity"
    detail = await async_client.get(
        f"/api/v1/intelligence/regime-reports/{report_id}", headers=headers
    )
    assert detail.status_code == 200, detail.text
    # BO-B-04 supersession: the POST generation endpoint now EXISTS.
    # A body-less POST fails request validation (422), no longer 405.
    post = await async_client.post("/api/v1/intelligence/regime-reports", headers=headers)
    assert post.status_code == 422


def test_regime_modules_use_no_unspiked_dependencies_or_execution_path() -> None:
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
