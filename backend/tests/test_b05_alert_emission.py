"""BO-B-05 — alert emission wiring tests (fail-first).

Pre-fix expectation (b05_probe_prefix.log): the POST /alerts/check and
/alerts/inference-health endpoints do not exist (405) — the four alert
creation methods have zero callers (the B-05 "written but unwired" gap).
Post-fix: real conditions emit inert, deduplicated, audited alerts.
"""

from __future__ import annotations

from datetime import timedelta
from decimal import Decimal

import pytest
from httpx import AsyncClient
from sqlalchemy import func, select

from app.core.time import utc_now
from app.db.models.advisory_signal import AdvisorySignal
from app.db.models.generalization import DriftMonitoringRecord
from app.db.models.model_artifact import ModelArtifact
from app.db.models.monitoring_alert import MonitoringAlert
from app.db.session import session_scope
from app.repositories.candle_repository import CandleRepository


async def _auth(client: AsyncClient) -> dict[str, str]:
    login = await client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert login.status_code == 200, login.text
    return {"Authorization": f"Bearer {login.json()['tokens']['access_token']}"}


async def _alert_count(session) -> int:  # noqa: ANN001
    return (
        await session.execute(select(func.count()).select_from(MonitoringAlert))
    ).scalar_one()


@pytest.mark.asyncio
async def test_b05_emission_endpoints_require_auth(async_client: AsyncClient) -> None:
    check = await async_client.post("/api/v1/alerts/check")
    assert check.status_code == 401
    health = await async_client.post(
        "/api/v1/alerts/inference-health",
        json={"component": "engine", "status": "degraded", "detail": "probe"},
    )
    assert health.status_code == 401


@pytest.mark.asyncio
async def test_b05_stale_feed_emits_deduped_alert(async_client: AsyncClient) -> None:
    async with session_scope() as session:
        await CandleRepository(session).upsert_ohlcv(
            market_class="forex",
            symbol="EURUSD",
            timeframe="M1",
            open_time=utc_now() - timedelta(hours=3),
            open=Decimal("1.1"),
            high=Decimal("1.11"),
            low=Decimal("1.09"),
            close=Decimal("1.10"),
            volume=Decimal("5"),
            source="live:simulated",
        )
    headers = await _auth(async_client)
    first = await async_client.post("/api/v1/alerts/check", headers=headers)
    assert first.status_code == 200, first.text
    body = first.json()
    assert body["stale_alerts_emitted"] == 1
    assert body["stale_symbols_checked"] >= 1
    assert len(body["emitted_alert_ids"]) == 1
    alert_id = body["emitted_alert_ids"][0]

    async with session_scope() as session:
        alert = await session.get(MonitoringAlert, alert_id)
        assert alert is not None
        assert alert.alert_type == "LIVE_DATA_STALE"
        assert alert.severity == "warning"
        assert alert.subject_type == "market_series"
        assert alert.symbol == "EURUSD"
        assert alert.evidence["staleness_seconds"] > 3600
        assert alert.evidence["threshold_seconds"] == 3600
        assert alert.lineage["source"] == "w1_live_market_observability"
        assert alert.acknowledged is False

    # Dedup: repeat check within cooldown → no new alert.
    second = await async_client.post("/api/v1/alerts/check", headers=headers)
    assert second.json()["stale_alerts_emitted"] == 0
    async with session_scope() as session:
        assert await _alert_count(session) == 1


@pytest.mark.asyncio
async def test_b05_fresh_feed_emits_no_alert(async_client: AsyncClient) -> None:
    async with session_scope() as session:
        await CandleRepository(session).upsert_ohlcv(
            market_class="forex",
            symbol="GBPUSD",
            timeframe="M1",
            open_time=utc_now() - timedelta(seconds=30),
            open=Decimal("1.27"),
            high=Decimal("1.28"),
            low=Decimal("1.26"),
            close=Decimal("1.27"),
            volume=Decimal("5"),
            source="live:simulated",
        )
    headers = await _auth(async_client)
    response = await async_client.post("/api/v1/alerts/check", headers=headers)
    assert response.status_code == 200
    assert response.json()["stale_alerts_emitted"] == 0


@pytest.mark.asyncio
async def test_b05_inference_health_explicit_input_and_severity(
    async_client: AsyncClient,
) -> None:
    headers = await _auth(async_client)
    degraded = await async_client.post(
        "/api/v1/alerts/inference-health",
        json={"component": "inference-engine", "status": "degraded", "detail": "test degrade"},
        headers=headers,
    )
    assert degraded.status_code == 200, degraded.text
    assert degraded.json()["alert_type"] == "INFERENCE_HEALTH_DEGRADED"
    assert degraded.json()["severity"] == "warning"

    down = await async_client.post(
        "/api/v1/alerts/inference-health",
        json={"component": "inference-engine-2", "status": "down", "detail": "test down"},
        headers=headers,
    )
    assert down.status_code == 200
    assert down.json()["severity"] == "critical"

    # Invalid status rejected at the schema boundary.
    invalid = await async_client.post(
        "/api/v1/alerts/inference-health",
        json={"component": "x", "status": "ok", "detail": "not a degradation"},
        headers=headers,
    )
    assert invalid.status_code == 422

    # Dedup: same component within cooldown → 409.
    duplicate = await async_client.post(
        "/api/v1/alerts/inference-health",
        json={"component": "inference-engine", "status": "degraded", "detail": "again"},
        headers=headers,
    )
    assert duplicate.status_code == 409


@pytest.mark.asyncio
async def test_b05_drift_record_emits_alert_once(async_client: AsyncClient) -> None:
    async with session_scope() as session:
        artifact = ModelArtifact(
            name="b05-drift-model",
            version="1-42",
            status="research_only",
            framework="fixture",
            feature_set_version="feature_set.v1",
            research_status="research_only",
        )
        session.add(artifact)
        await session.flush()
        now = utc_now()
        session.add(
            DriftMonitoringRecord(
                model_artifact_id=artifact.id,
                drift_kind="input_distribution",
                window_start=now - timedelta(hours=2),
                window_end=now,
                signals={"ks_statistic": 0.2},
                drift_detected=True,
                auto_retrain_requested=False,
                retrain_triggered=False,
                governance_required=True,
                evidence_summary="B-05 drift emission test fixture.",
                record_hash="b05-drift-hash",
            )
        )
        await session.flush()
    headers = await _auth(async_client)
    first = await async_client.post("/api/v1/alerts/check", headers=headers)
    assert first.json()["drift_alerts_emitted"] == 1
    alert_id = first.json()["emitted_alert_ids"][0]
    async with session_scope() as session:
        alert = await session.get(MonitoringAlert, alert_id)
        assert alert is not None
        assert alert.alert_type == "DRIFT_DETECTED"
        assert alert.severity == "warning"
        assert alert.model_artifact_id == artifact.id
    second = await async_client.post("/api/v1/alerts/check", headers=headers)
    assert second.json()["drift_alerts_emitted"] == 0


@pytest.mark.asyncio
async def test_b05_withheld_signal_emits_alert_once(async_client: AsyncClient) -> None:
    async with session_scope() as session:
        artifact = ModelArtifact(
            name="b05-withheld-model",
            version="1-42",
            status="research_only",
            framework="fixture",
            feature_set_version="feature_set.v1",
            research_status="research_only",
        )
        session.add(artifact)
        await session.flush()
        session.add(
            AdvisorySignal(
                as_of_time=utc_now() - timedelta(minutes=5),
                market_class="forex",
                provider="internal",
                symbol="EURUSD",
                timeframe="M1",
                model_artifact_id=artifact.id,
                model_version=artifact.version,
                feature_set_version="feature_set.v1",
                experiment_id="exp-b05-withheld",
                inference_input_hash="b05-withheld-hash",
                audit_correlation_id="b05-withheld-correlation",
                raw_score=None,
                calibrated_confidence=None,
                signal_direction="withheld",
                signal_state="withheld",
                state_reason="STALE_INPUT",
                eligibility_reasons=["STALE_INPUT"],
                operating_domain_status="valid",
                calibration_status="not_evaluated",
                economic_verdict="not_evaluated",
                rationale="B-05 withheld-signal emission fixture (synthetic; disclosed).",
                explainability_summary={"freshness": {"freshness_status": "stale"}},
            )
        )
        await session.flush()
    headers = await _auth(async_client)
    first = await async_client.post("/api/v1/alerts/check", headers=headers)
    assert first.json()["withheld_alerts_emitted"] == 1
    alert_id = first.json()["emitted_alert_ids"][0]
    async with session_scope() as session:
        alert = await session.get(MonitoringAlert, alert_id)
        assert alert is not None
        assert alert.alert_type == "SIGNAL_WITHHELD"
        assert alert.signal_id is not None
    second = await async_client.post("/api/v1/alerts/check", headers=headers)
    assert second.json()["withheld_alerts_emitted"] == 0


@pytest.mark.asyncio
async def test_b05_ack_read_state_only_no_actuation(async_client: AsyncClient) -> None:
    async with session_scope() as session:
        artifact = ModelArtifact(
            name="b05-ack-model",
            version="1-42",
            status="research_only",
            framework="fixture",
            feature_set_version="feature_set.v1",
            research_status="research_only",
        )
        session.add(artifact)
        await session.flush()
        session.add(
            AdvisorySignal(
                as_of_time=utc_now() - timedelta(minutes=5),
                market_class="forex",
                provider="internal",
                symbol="GBPUSD",
                timeframe="M1",
                model_artifact_id=artifact.id,
                model_version=artifact.version,
                feature_set_version="feature_set.v1",
                experiment_id="exp-b05-ack",
                inference_input_hash="b05-ack-hash",
                audit_correlation_id="b05-ack-correlation",
                raw_score=None,
                calibrated_confidence=None,
                signal_direction="withheld",
                signal_state="withheld",
                state_reason="RATIONALE_REQUIRED",
                eligibility_reasons=["RATIONALE_REQUIRED"],
                operating_domain_status="valid",
                calibration_status="not_evaluated",
                economic_verdict="not_evaluated",
                rationale="B-05 ack non-actuation fixture.",
                explainability_summary={},
            )
        )
        await session.flush()
        signal_id = (
            await session.execute(select(AdvisorySignal.signal_id).limit(1))
        ).scalar_one()
    headers = await _auth(async_client)
    check = await async_client.post("/api/v1/alerts/check", headers=headers)
    alert_id = check.json()["emitted_alert_ids"][0]

    # Pre-ack state capture.
    async with session_scope() as session:
        pre_signal_state = (await session.get(AdvisorySignal, signal_id)).signal_state
        pre_ack = (await session.get(MonitoringAlert, alert_id)).acknowledged

    ack = await async_client.post(f"/api/v1/alerts/{alert_id}/ack", headers=headers)
    assert ack.status_code == 200
    assert ack.json()["acknowledged"] is True
    assert ack.json()["acknowledged_by"] == "admin"

    # Post-ack: alert read-state changed; the subject signal is untouched.
    async with session_scope() as session:
        post_signal = await session.get(AdvisorySignal, signal_id)
        assert post_signal.signal_state == pre_signal_state == "withheld"
        assert post_signal.state_reason == "RATIONALE_REQUIRED"
        alert = await session.get(MonitoringAlert, alert_id)
        assert alert.acknowledged is True
        assert pre_ack is False


def test_b05_emission_module_has_no_actuation_surface() -> None:
    from pathlib import Path

    module = (
        Path(__file__).resolve().parents[1]
        / "app"
        / "trading_intelligence"
        / "monitoring"
        / "emission.py"
    ).read_text(encoding="utf-8")
    # Actuation identifiers (imports/calls), not prose: the docstring's
    # boundary sentences legitimately name what the module must NOT do.
    forbidden = (
        "place_order",
        "cancel_order",
        "OrderIntent",
        "BrokerRepository",
        "ExecutionService",
        "retrain_triggered = True",
        "auto_retrain_requested = True",
        "emit_signal",
    )
    assert all(term not in module for term in forbidden)
