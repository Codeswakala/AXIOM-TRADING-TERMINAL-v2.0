"""W3-U06 monitoring, drift, and health alert tests."""

from __future__ import annotations

from datetime import timedelta
from pathlib import Path

import pytest
from httpx import AsyncClient

from app.core.time import utc_now
from app.db.models.audit import AuditEvent
from app.db.models.generalization import DriftMonitoringRecord
from app.db.models.model_artifact import ModelArtifact
from app.db.models.monitoring_alert import MonitoringAlert
from app.trading_intelligence.monitoring import MonitoringAlertService
from tests.test_live_inference_gate import _eligible_artifact


@pytest.mark.asyncio
async def test_market_health_and_drift_alerts_created_with_correct_types(
    prepared_db: None,
) -> None:
    from sqlalchemy import select

    from app.db.session import session_scope

    async with session_scope() as session:
        artifact = await _eligible_artifact(session)
        drift = DriftMonitoringRecord(
            model_artifact_id=artifact.id,
            drift_kind="feature_distribution",
            window_start=utc_now() - timedelta(hours=2),
            window_end=utc_now() - timedelta(hours=1),
            signals={"psi": 0.42},
            drift_detected=True,
            auto_retrain_requested=False,
            retrain_triggered=False,
            governance_required=True,
            evidence_summary="PSI exceeded research threshold; operator review required.",
            record_hash="w3-u06-drift-hash",
            research_status="research_only",
        )
        session.add(drift)
        await session.flush()
        service = MonitoringAlertService(session)
        market = await service.create_live_data_stale_alert(
            market_class="forex",
            symbol="EURUSD",
            timeframe="M1",
            freshest_as_of=utc_now() - timedelta(minutes=10),
            staleness_seconds=600,
            threshold_seconds=300,
            actor="pytest",
        )
        health = await service.create_inference_health_alert(
            component="live_inference_adapter",
            status="degraded",
            detail="input window is stale",
            actor="pytest",
        )
        drift_alert = await service.create_drift_alert(
            drift_record=drift, model=artifact, actor="pytest"
        )

        assert {market.alert_type, health.alert_type, drift_alert.alert_type} == {
            "LIVE_DATA_STALE",
            "INFERENCE_HEALTH_DEGRADED",
            "DRIFT_DETECTED",
        }
        assert all(alert.acknowledged is False for alert in [market, health, drift_alert])
        actions = await session.scalars(
            select(AuditEvent.action).where(AuditEvent.resource_type == "monitoring_alert")
        )
        assert list(actions.all()).count("monitoring_alert.created") == 3


@pytest.mark.asyncio
async def test_drift_alert_triggers_no_retrain_model_change_order_or_auto_action(
    prepared_db: None,
) -> None:
    from sqlalchemy import select

    from app.db.session import session_scope

    async with session_scope() as session:
        artifact = await _eligible_artifact(session)
        before = {
            "status": artifact.status,
            "research_status": artifact.research_status,
            "advisory_status": artifact.advisory_status,
            "approval_history": artifact.approval_history,
        }
        drift = DriftMonitoringRecord(
            model_artifact_id=artifact.id,
            drift_kind="prediction_distribution",
            window_start=utc_now() - timedelta(hours=2),
            window_end=utc_now() - timedelta(hours=1),
            signals={"ks_statistic": 0.31},
            drift_detected=True,
            auto_retrain_requested=False,
            retrain_triggered=False,
            governance_required=True,
            evidence_summary="Distribution shift observed; alert only.",
            record_hash="w3-u06-no-auto-action-hash",
            research_status="research_only",
        )
        session.add(drift)
        await session.flush()
        alert = await MonitoringAlertService(session).create_drift_alert(
            drift_record=drift,
            model=artifact,
            actor="pytest",
        )
        await session.flush()

        refreshed = await session.get(ModelArtifact, artifact.id)
        assert refreshed is not None
        assert refreshed.status == before["status"]
        assert refreshed.research_status == before["research_status"]
        assert refreshed.advisory_status == before["advisory_status"]
        assert refreshed.approval_history == before["approval_history"]
        assert drift.auto_retrain_requested is False
        assert drift.retrain_triggered is False
        assert alert.alert_type == "DRIFT_DETECTED"
        assert alert.evidence["drift_detected"] is True
        assert "remediation" not in alert.evidence
        model_audit = await session.scalars(
            select(AuditEvent.action).where(AuditEvent.resource_type == "model_artifact")
        )
        assert not set(model_audit.all())


def test_alert_record_is_inert_and_alert_code_has_no_execution_path() -> None:
    forbidden_columns = {
        "order_id",
        "order_payload",
        "order_intent",
        "execution_payload",
        "remediation_payload",
        "quantity",
        "stop_loss",
        "take_profit",
        "broker_account_id",
    }
    assert forbidden_columns.isdisjoint(set(MonitoringAlert.__table__.columns.keys()))

    root = Path(__file__).resolve().parents[1] / "app" / "trading_intelligence" / "monitoring"
    forbidden = (
        "place_order",
        "cancel_order",
        "broker.",
        "execute",
        "auto_retrain",
        "model.status =",
        "advisory_status =",
    )
    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for needle in forbidden:
            assert needle not in text


@pytest.mark.asyncio
async def test_alerts_api_auth_list_get_ack_read_state_only(async_client: AsyncClient) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        alert = await MonitoringAlertService(session).create_inference_health_alert(
            component="signal_store",
            status="degraded",
            detail="latency over threshold",
            actor="pytest",
        )
        alert_id = alert.alert_id

    unauth = await async_client.get("/api/v1/alerts")
    assert unauth.status_code == 401

    login = await async_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert login.status_code == 200, login.text
    headers = {"Authorization": f"Bearer {login.json()['tokens']['access_token']}"}

    listed = await async_client.get("/api/v1/alerts", headers=headers)
    assert listed.status_code == 200, listed.text
    assert any(row["alert_id"] == alert_id for row in listed.json())

    fetched = await async_client.get(f"/api/v1/alerts/{alert_id}", headers=headers)
    assert fetched.status_code == 200, fetched.text
    assert fetched.json()["acknowledged"] is False

    ack = await async_client.post(f"/api/v1/alerts/{alert_id}/ack", headers=headers)
    assert ack.status_code == 200, ack.text
    body = ack.json()
    assert body["acknowledged"] is True
    assert body["acknowledged_by"] == "admin"
    assert body["alert_type"] == "INFERENCE_HEALTH_DEGRADED"

    post_collection = await async_client.post("/api/v1/alerts", headers=headers)
    assert post_collection.status_code == 405


@pytest.mark.asyncio
async def test_monitoring_alert_ack_does_not_mutate_subject_model(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        artifact = await _eligible_artifact(session)
        before_status = artifact.status
        service = MonitoringAlertService(session)
        alert = await service.create_alert(
            alert_type="MODEL_CALIBRATION_WARNING",
            severity="warning",
            subject_type="model_artifact",
            subject_id=artifact.id,
            model_artifact_id=artifact.id,
            summary="Calibration warning surfaced to operator.",
            evidence={"calibration_status": "warning:POORLY_CALIBRATED"},
            lineage={"experiment_id": artifact.experiment_id},
            actor="pytest",
        )
        acknowledged = await service.acknowledge_alert(alert.alert_id, actor="pytest")
        assert acknowledged is not None
        assert acknowledged.acknowledged is True
        refreshed = await session.get(ModelArtifact, artifact.id)
        assert refreshed is not None
        assert refreshed.status == before_status
        assert refreshed.advisory_status == artifact.advisory_status


def test_alerts_ui_module_has_no_forbidden_controls() -> None:
    """SURF-P02 M4 — frontend T-1 guard over the alerts surface.

    The CONV/SURF-P01 guards pin frontend files with non-vacuity anchors; this
    suite previously pinned none. The alerts domain's specific T-1 risk is an
    alert appearing to TRIGGER a corrective action, so the guard pins the
    module that renders the alerts UI and asserts the actuation vocabulary
    absent.

    R1 carve-out (disclosed): Build Order R1 requires the disclaimer sentence
    "Read-only alerts inform the operator; they do not retrain, remediate, or
    act." verbatim in the module — the sentence legitimately contains
    "retrain" and "remediate". The guard therefore removes exactly that
    sentence before asserting absence, and asserts the sentence itself as a
    non-vacuity anchor. Everything outside the disclaimer must be clean.
    """
    root = Path(__file__).resolve().parents[2]
    ui = (
        root
        / "frontend"
        / "src"
        / "components"
        / "alerts"
        / "MonitoringAlertsPanel.tsx"
    )
    text = ui.read_text(encoding="utf-8")
    # Non-vacuity anchors: the module genuinely renders the alerts surface,
    # the R1 disclaimer, and the M1 read-state-only acknowledge label.
    assert "Monitoring Alerts" in text
    assert "Read-only alerts inform the operator; they do not retrain, remediate, or act." in text
    assert "Acknowledge" in text
    disclaimer = "read-only alerts inform the operator; they do not retrain, remediate, or act."
    residue = text.lower().replace(disclaimer, "")
    forbidden = (
        "place_order",
        "submit order",
        "go live",
        "connect broker",
        "broker_account",
        "resolve_alert",
        "auto_action",
        "execute",
        "retrain",
        "remediate",
    )
    assert all(item not in residue for item in forbidden)
