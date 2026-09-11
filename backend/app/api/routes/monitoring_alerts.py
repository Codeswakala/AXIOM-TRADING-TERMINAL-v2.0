"""Authenticated monitoring alert history + governed emission API.

W3-U06 read/ack surface (unchanged contract) plus BO-B-05 emission wiring:
  - POST /alerts/check           — bounded governed check path (stale-feed,
                                   drift-record, withheld-signal emission)
  - POST /alerts/inference-health — explicit inference-health degradation input
Alerts remain INERT: acknowledgement mutates read-state only; no auto-action.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import CurrentOperatorDep
from app.core.config import get_settings
from app.db.models.monitoring_alert import MonitoringAlert
from app.db.session import get_db_session
from app.models.monitoring_alert import (
    AlertCheckResponse,
    InferenceHealthCheckRequest,
    MonitoringAlertRead,
)
from app.trading_intelligence.monitoring import MonitoringAlertFilter, MonitoringAlertService
from app.trading_intelligence.monitoring import emission as alert_emission

router = APIRouter(prefix="/alerts", tags=["monitoring-alerts"])

SessionDep = Annotated[AsyncSession, Depends(get_db_session)]


def _service(session: SessionDep) -> MonitoringAlertService:
    return MonitoringAlertService(session)


MonitoringAlertServiceDep = Annotated[MonitoringAlertService, Depends(_service)]


@router.get(
    "",
    response_model=list[MonitoringAlertRead],
    summary="List inert monitoring alerts (operator-authenticated)",
)
async def list_alerts(
    service: MonitoringAlertServiceDep,
    operator: CurrentOperatorDep,
    alert_type: str | None = None,
    severity: str | None = None,
    subject_type: str | None = None,
    subject_id: str | None = None,
    acknowledged: bool | None = None,
    limit: int = Query(default=50, ge=1, le=200),
) -> list[MonitoringAlert]:
    _ = operator
    return await service.list_alerts(
        MonitoringAlertFilter(
            alert_type=alert_type,
            severity=severity,
            subject_type=subject_type,
            subject_id=subject_id,
            acknowledged=acknowledged,
            limit=limit,
        )
    )


@router.get(
    "/{alert_id}",
    response_model=MonitoringAlertRead,
    summary="Get one inert monitoring alert by id (operator-authenticated)",
)
async def get_alert(
    alert_id: str,
    service: MonitoringAlertServiceDep,
    operator: CurrentOperatorDep,
) -> MonitoringAlert:
    _ = operator
    alert = await service.get_alert(alert_id)
    if alert is None:
        raise HTTPException(status_code=404, detail="Monitoring alert not found")
    return alert


@router.post(
    "/{alert_id}/ack",
    response_model=MonitoringAlertRead,
    summary="Acknowledge an alert read-state only (operator-authenticated)",
)
async def acknowledge_alert(
    alert_id: str,
    service: MonitoringAlertServiceDep,
    operator: CurrentOperatorDep,
) -> MonitoringAlert:
    alert = await service.acknowledge_alert(alert_id, actor=operator.username)
    if alert is None:
        raise HTTPException(status_code=404, detail="Monitoring alert not found")
    return alert


@router.post(
    "/check",
    response_model=AlertCheckResponse,
    summary=(
        "BO-B-05: governed bounded check path — emits stale-data, drift, and "
        "withheld-signal alerts from real conditions (operator-authenticated)"
    ),
)
async def run_alert_check(
    session: SessionDep,
    operator: CurrentOperatorDep,
) -> AlertCheckResponse:
    """On-request, bounded, deduplicated emission check.

    No background actor; no actuation. Reads feed staleness (freshest
    live:simulated candle per configured symbol), existing drift records, and
    persisted withheld signals — emitting inert alerts for genuine conditions.
    """
    settings = get_settings()
    symbols = alert_emission.staleness_symbols(settings.live_market_symbols)
    stale = await alert_emission.run_staleness_emission(
        session,
        symbols=symbols,
        threshold_seconds=settings.monitoring_alert_staleness_threshold_seconds,
        cooldown_seconds=settings.monitoring_alert_dedup_cooldown_seconds,
        actor=operator.username,
    )
    drift = await alert_emission.run_drift_emission(
        session,
        cooldown_seconds=settings.monitoring_alert_dedup_cooldown_seconds,
        actor=operator.username,
    )
    withheld = await alert_emission.run_withheld_signal_emission(
        session,
        cooldown_seconds=settings.monitoring_alert_dedup_cooldown_seconds,
        actor=operator.username,
    )
    await session.flush()
    return AlertCheckResponse(
        stale_alerts_emitted=len(stale),
        drift_alerts_emitted=len(drift),
        withheld_alerts_emitted=len(withheld),
        stale_symbols_checked=len(symbols),
        threshold_seconds=settings.monitoring_alert_staleness_threshold_seconds,
        cooldown_seconds=settings.monitoring_alert_dedup_cooldown_seconds,
        emitted_alert_ids=[alert.alert_id for alert in [*stale, *drift, *withheld]],
    )


@router.post(
    "/inference-health",
    response_model=MonitoringAlertRead,
    summary=(
        "BO-B-05.2: explicit inference-health degradation input — emits one "
        "inert INFERENCE_HEALTH_DEGRADED alert (deduplicated per component)"
    ),
)
async def report_inference_health(
    payload: InferenceHealthCheckRequest,
    session: SessionDep,
    operator: CurrentOperatorDep,
) -> MonitoringAlert:
    settings = get_settings()
    alert, deduped = await alert_emission.emit_inference_health(
        session,
        component=payload.component,
        status=payload.status,
        detail=payload.detail,
        cooldown_seconds=settings.monitoring_alert_dedup_cooldown_seconds,
        actor=operator.username,
    )
    if deduped:
        raise HTTPException(
            status_code=409,
            detail=(
                "Inference-health alert suppressed by cooldown: "
                f"component={payload.component}"
            ),
        )
    assert alert is not None
    await session.flush()
    return alert
