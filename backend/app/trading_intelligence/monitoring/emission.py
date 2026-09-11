"""BO-B-05 — alert emission wiring.

The MonitoringAlertService's `create_*` methods existed since W3-U06 but had
zero callers (the B-05 "written but unwired" gap). This module wires emission
to real, as-of-bounded trigger conditions:

  - LIVE_DATA_STALE:      freshest persisted `live:simulated` candle per
                          configured feed symbol older than the threshold.
  - INFERENCE_HEALTH_DEGRADED: explicit degraded/down component input.
  - DRIFT_DETECTED:       existing `DriftMonitoringRecord` rows with
                          `drift_detected=True` (no new drift algorithm).
  - SIGNAL_WITHHELD:      persisted advisory signals with
                          `signal_state == 'withheld'`.

Binding semantics (BO-B-05 §2/§7):
  - Deduplication: one alert per (alert_type, subject_id) within the cooldown
    window — bounded, no spam.
  - Inert: alerts are persisted and audited by the service; they NEVER mutate
    market, model, signal, order, account, or trading state. No auto-action.
"""

from __future__ import annotations

from datetime import timedelta
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.time import coerce_external_utc, utc_now
from app.db.models.advisory_signal import AdvisorySignal
from app.db.models.candle import Candle
from app.db.models.generalization import DriftMonitoringRecord
from app.db.models.model_artifact import ModelArtifact
from app.db.models.monitoring_alert import MonitoringAlert
from app.trading_intelligence.monitoring.service import MonitoringAlertService


async def _recent_alert_exists(
    session: AsyncSession,
    *,
    alert_type: str,
    subject_id: str,
    cooldown_seconds: int,
) -> bool:
    """Dedup check: the LATEST alert for (type, subject) is compared in
    Python — SQLite stores naive timestamps, so a SQL comparison against an
    aware cutoff is not portable."""
    result = await session.scalars(
        select(MonitoringAlert)
        .where(
            MonitoringAlert.alert_type == alert_type,
            MonitoringAlert.subject_id == subject_id,
        )
        .order_by(MonitoringAlert.created_at.desc())
        .limit(1)
    )
    latest = result.first()
    if latest is None:
        return False
    created = coerce_external_utc(
        latest.created_at, source="monitoring alert dedup window"
    )
    if created is None:
        return False
    cutoff = utc_now() - timedelta(seconds=cooldown_seconds)
    return created >= cutoff


async def run_staleness_emission(
    session: AsyncSession,
    *,
    symbols: Sequence[str],
    threshold_seconds: int,
    cooldown_seconds: int,
    actor: str = "system",
) -> list[MonitoringAlert]:
    """Emit LIVE_DATA_STALE for feed symbols whose freshest persisted
    live:simulated candle exceeds the staleness threshold.

    Honest semantics: a symbol with NO live:simulated candles is not "stale" —
    the feed was never started for it (observable via /market/live/status).
    """
    service = MonitoringAlertService(session)
    emitted: list[MonitoringAlert] = []
    now = utc_now()
    for symbol in symbols:
        result = await session.scalars(
            select(Candle)
            .where(Candle.symbol == symbol, Candle.source == "live:simulated")
            .order_by(Candle.open_time.desc())
            .limit(1)
        )
        freshest = result.first()
        if freshest is None:
            continue
        freshest_time = coerce_external_utc(
            freshest.open_time, source="monitoring staleness emission"
        )
        if freshest_time is None:
            continue
        staleness = (now - freshest_time).total_seconds()
        if staleness <= threshold_seconds:
            continue
        subject_id = f"{freshest.market_class}:{symbol}:{freshest.timeframe}"
        if await _recent_alert_exists(
            session,
            alert_type="LIVE_DATA_STALE",
            subject_id=subject_id,
            cooldown_seconds=cooldown_seconds,
        ):
            continue
        emitted.append(
            await service.create_live_data_stale_alert(
                market_class=freshest.market_class,
                symbol=symbol,
                timeframe=freshest.timeframe,
                freshest_as_of=freshest_time,
                staleness_seconds=int(staleness),
                threshold_seconds=threshold_seconds,
                actor=actor,
            )
        )
    return emitted


async def run_drift_emission(
    session: AsyncSession,
    *,
    cooldown_seconds: int,
    actor: str = "system",
) -> list[MonitoringAlert]:
    """Emit DRIFT_DETECTED for existing drift records flagged detected.

    No drift-detection algorithm is created (BO-B-05 §2): only persisted
    `DriftMonitoringRecord.drift_detected == True` rows become alerts.
    """
    service = MonitoringAlertService(session)
    result = await session.scalars(
        select(DriftMonitoringRecord).where(DriftMonitoringRecord.drift_detected.is_(True))
    )
    emitted: list[MonitoringAlert] = []
    for record in result.all():
        model = await session.get(ModelArtifact, record.model_artifact_id)
        # Condition key == the service's own subject_id (model id when the
        # artifact resolves, else the record's artifact reference).
        subject_id = model.id if model is not None else record.model_artifact_id
        if await _recent_alert_exists(
            session,
            alert_type="DRIFT_DETECTED",
            subject_id=subject_id,
            cooldown_seconds=cooldown_seconds,
        ):
            continue
        emitted.append(
            await service.create_drift_alert(
                drift_record=record,
                model=model,
                actor=actor,
            )
        )
    return emitted


async def run_withheld_signal_emission(
    session: AsyncSession,
    *,
    cooldown_seconds: int,
    actor: str = "system",
) -> list[MonitoringAlert]:
    """Emit SIGNAL_WITHHELD for persisted withheld advisory signals.

    With the predictive track deferred, no live inference withholds exist;
    this path fires from persisted withheld rows (test-proven) and remains
    ready for a future promoted model.
    """
    service = MonitoringAlertService(session)
    result = await session.scalars(
        select(AdvisorySignal).where(AdvisorySignal.signal_state == "withheld")
    )
    emitted: list[MonitoringAlert] = []
    for signal in result.all():
        # Condition key == the service's own subject_id (the bare signal id).
        subject_id = signal.signal_id
        if await _recent_alert_exists(
            session,
            alert_type="SIGNAL_WITHHELD",
            subject_id=subject_id,
            cooldown_seconds=cooldown_seconds,
        ):
            continue
        emitted.append(
            await service.create_signal_withheld_alert(signal=signal, actor=actor)
        )
    return emitted


async def emit_inference_health(
    session: AsyncSession,
    *,
    component: str,
    status: str,
    detail: str,
    cooldown_seconds: int,
    actor: str = "system",
) -> tuple[MonitoringAlert | None, bool]:
    """Wire INFERENCE_HEALTH_DEGRADED to an explicit health input.

    Returns (alert, deduped). `status` is validated by the request schema
    (degraded | down) at the endpoint boundary.
    """
    # Condition key == the service's own subject_id (the bare component).
    subject_id = component
    if await _recent_alert_exists(
        session,
        alert_type="INFERENCE_HEALTH_DEGRADED",
        subject_id=subject_id,
        cooldown_seconds=cooldown_seconds,
    ):
        return None, True
    service = MonitoringAlertService(session)
    alert = await service.create_inference_health_alert(
        component=component,
        status=status,
        detail=detail,
        actor=actor,
    )
    return alert, False


def staleness_symbols(symbols_field: str) -> list[str]:
    """Parse the configured live-market symbol list (comma-separated)."""
    return [item.strip() for item in symbols_field.split(",") if item.strip()]
