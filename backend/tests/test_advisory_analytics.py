"""W3-U07 advisory performance analytics tests."""

from __future__ import annotations

from datetime import timedelta

import pytest
from httpx import AsyncClient

from app.core.time import utc_now
from app.db.models.advisory_signal import AdvisorySignal
from app.db.models.economic_report import EconomicReport
from app.trading_intelligence.analytics import AdvisoryAnalyticsService
from tests.test_live_inference_gate import _eligible_artifact


async def _signal(session, artifact, *, state: str, calibration_status: str = "calibrated"):
    economic = await session.get(EconomicReport, artifact.economic_report_id)
    assert economic is not None
    return AdvisorySignal(
        created_at=utc_now(),
        as_of_time=utc_now() - timedelta(minutes=1),
        market_class="forex",
        provider="internal",
        symbol="EURUSD",
        timeframe="M1",
        model_artifact_id=artifact.id,
        model_version=artifact.version,
        feature_set_version=artifact.feature_set_version or "feature_set.v1",
        experiment_id=artifact.experiment_id or "exp",
        statistical_report_id=artifact.statistical_report_id,
        calibration_report_id=artifact.calibration_report_id,
        economic_report_id=artifact.economic_report_id,
        generalization_report_id=None,
        inference_input_hash=f"hash-{state}-{calibration_status}",
        raw_score=0.987654,
        calibrated_confidence=0.5,
        input_staleness_seconds=60,
        signal_validity_seconds=300,
        expires_at=utc_now() + timedelta(minutes=5),
        freshness_status="fresh" if state != "expired" else "expired",
        signal_direction="positive_bias" if state != "withheld" else "withheld",
        signal_state=state,
        state_reason="ELIGIBLE" if state == "emitted" else state.upper(),
        eligibility_reasons=[] if state == "emitted" else [state.upper()],
        operating_domain_status="valid",
        calibration_status=calibration_status,
        economic_verdict=economic.economic_conclusion.get("verdict", "unknown"),
        risk_notes=None,
        rationale="Analytics fixture signal.",
        explainability_summary={"confidence": {"calibrated_confidence": 0.5}},
        state_transition_history=["candidate", "eligible_checked", state],
        audit_correlation_id=f"corr-{state}-{calibration_status}",
    )


@pytest.mark.asyncio
async def test_advisory_analytics_metrics_include_uncertainty_and_sample_counts(
    prepared_db: None,
) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        artifact = await _eligible_artifact(session)
        economic = await session.get(EconomicReport, artifact.economic_report_id)
        assert economic is not None
        economic.economic_conclusion = {"verdict": "economically_usable"}
        for item in [
            await _signal(session, artifact, state="emitted"),
            await _signal(session, artifact, state="warning"),
            await _signal(session, artifact, state="withheld"),
            await _signal(session, artifact, state="expired"),
        ]:
            session.add(item)
        await session.flush()

        service = AdvisoryAnalyticsService(session)
        snapshot = await service.snapshot()
        assert snapshot.generated_from == "advisory_signals_read_only"
        assert "not guaranteed" in snapshot.disclaimer
        assert snapshot.metrics
        for metric in snapshot.metrics:
            assert metric.sample_count == 4
            assert metric.uncertainty.sample_count == 4
            assert metric.uncertainty.method == "wilson_score_interval"
            assert 0.0 <= metric.uncertainty.lower <= metric.uncertainty.upper <= 1.0


@pytest.mark.asyncio
async def test_confidence_visualization_flags_poor_calibration_and_excludes_raw_score(
    prepared_db: None,
) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        artifact = await _eligible_artifact(session)
        economic = await session.get(EconomicReport, artifact.economic_report_id)
        assert economic is not None
        economic.economic_conclusion = {"verdict": "economically_usable"}
        session.add(
            await _signal(
                session,
                artifact,
                state="warning",
                calibration_status="warning:POORLY_CALIBRATED",
            )
        )
        await session.flush()
        service = AdvisoryAnalyticsService(session)
        payload = service.to_dict(await service.snapshot())
        assert "raw_score" not in str(payload)
        assert any(band["unreliable"] for band in payload["confidence_bands"])
        warning_bands = [band for band in payload["confidence_bands"] if band["unreliable"]]
        assert warning_bands[0]["calibration_status"] == "warning"
        assert warning_bands[0]["uncertainty"]["sample_count"] >= 1


@pytest.mark.asyncio
async def test_analytics_api_auth_read_only_and_uncertainty(async_client: AsyncClient) -> None:
    unauth = await async_client.get("/api/v1/analytics/advisory-performance")
    assert unauth.status_code == 401

    login = await async_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert login.status_code == 200, login.text
    headers = {"Authorization": f"Bearer {login.json()['tokens']['access_token']}"}
    response = await async_client.get("/api/v1/analytics/advisory-performance", headers=headers)
    assert response.status_code == 200, response.text
    body = response.json()
    assert "not guaranteed" in body["disclaimer"]
    for metric in body["metrics"]:
        assert "uncertainty" in metric
        assert "sample_count" in metric
    post = await async_client.post("/api/v1/analytics/advisory-performance", headers=headers)
    assert post.status_code == 405


def test_no_execution_or_mutation_path_in_analytics_modules() -> None:
    from pathlib import Path

    root = Path(__file__).resolve().parents[1] / "app" / "trading_intelligence" / "analytics"
    forbidden = (
        "place_order",
        "cancel_order",
        "broker.",
        "execute",
        "fit(",
        "predict(",
        "model.status =",
        "advisory_status =",
    )
    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for needle in forbidden:
            assert needle not in text
