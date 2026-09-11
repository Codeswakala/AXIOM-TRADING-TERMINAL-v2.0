"""Monitoring, drift, and health alert service (W3-U06)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Literal
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.time import require_utc, utc_now
from app.db.models.advisory_signal import AdvisorySignal
from app.db.models.generalization import DriftMonitoringRecord
from app.db.models.model_artifact import ModelArtifact
from app.db.models.monitoring_alert import MonitoringAlert
from app.repositories.audit_repository import AuditRepository

AlertType = Literal[
    "MODEL_OUT_OF_DOMAIN",
    "MODEL_CALIBRATION_WARNING",
    "MODEL_ECONOMICALLY_UNUSABLE",
    "DRIFT_DETECTED",
    "LIVE_DATA_STALE",
    "INFERENCE_HEALTH_DEGRADED",
    "SIGNAL_WITHHELD",
]
Severity = Literal["info", "warning", "critical"]


@dataclass(frozen=True, slots=True)
class MonitoringAlertFilter:
    """Read-only alert query filters."""

    alert_type: str | None = None
    severity: str | None = None
    subject_type: str | None = None
    subject_id: str | None = None
    acknowledged: bool | None = None
    limit: int = 50


class MonitoringAlertService:
    """Creates inert persisted alerts and exposes read/ack operations."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._audit = AuditRepository(session)

    async def create_alert(
        self,
        *,
        alert_type: AlertType,
        severity: Severity,
        subject_type: str,
        subject_id: str,
        summary: str,
        evidence: dict[str, Any],
        lineage: dict[str, Any] | None = None,
        actor: str = "system",
        market_class: str | None = None,
        symbol: str | None = None,
        timeframe: str | None = None,
        model_artifact_id: str | None = None,
        signal_id: str | None = None,
        audit_correlation_id: str | None = None,
    ) -> MonitoringAlert:
        """Persist and audit one inert monitoring alert."""
        correlation_id = audit_correlation_id or str(uuid4())
        alert = MonitoringAlert(
            alert_type=alert_type,
            severity=severity,
            subject_type=subject_type,
            subject_id=subject_id,
            market_class=market_class,
            symbol=symbol,
            timeframe=timeframe,
            model_artifact_id=model_artifact_id,
            signal_id=signal_id,
            summary=summary,
            evidence=evidence,
            lineage=lineage or {},
            acknowledged=False,
            audit_correlation_id=correlation_id,
        )
        self._session.add(alert)
        await self._session.flush()
        await self._audit.append(
            category="GOVERNANCE",
            action="monitoring_alert.created",
            actor=actor,
            resource_type="monitoring_alert",
            resource_id=alert.alert_id,
            message=f"Monitoring alert created type={alert.alert_type} severity={alert.severity}",
            details={
                "alert_id": alert.alert_id,
                "alert_type": alert.alert_type,
                "severity": alert.severity,
                "subject_type": alert.subject_type,
                "subject_id": alert.subject_id,
            },
            correlation_id=correlation_id,
        )
        return alert

    async def create_live_data_stale_alert(
        self,
        *,
        market_class: str,
        symbol: str,
        timeframe: str,
        freshest_as_of: datetime,
        staleness_seconds: int,
        threshold_seconds: int,
        actor: str = "system",
    ) -> MonitoringAlert:
        normalized_as_of = require_utc(freshest_as_of, boundary="monitoring_alert.freshest_as_of")
        assert normalized_as_of is not None
        return await self.create_alert(
            alert_type="LIVE_DATA_STALE",
            severity="warning",
            subject_type="market_series",
            subject_id=f"{market_class}:{symbol}:{timeframe}",
            market_class=market_class,
            symbol=symbol,
            timeframe=timeframe,
            summary="Live market data is stale; operator attention required.",
            evidence={
                "freshest_as_of": normalized_as_of.isoformat(),
                "staleness_seconds": staleness_seconds,
                "threshold_seconds": threshold_seconds,
            },
            lineage={"source": "w1_live_market_observability"},
            actor=actor,
        )

    async def create_inference_health_alert(
        self,
        *,
        component: str,
        status: str,
        detail: str,
        actor: str = "system",
    ) -> MonitoringAlert:
        return await self.create_alert(
            alert_type="INFERENCE_HEALTH_DEGRADED",
            severity="warning" if status != "down" else "critical",
            subject_type="system_component",
            subject_id=component,
            summary=f"Inference health degraded for {component}.",
            evidence={"component": component, "status": status, "detail": detail},
            lineage={"source": "w1_observability"},
            actor=actor,
        )

    async def create_drift_alert(
        self,
        *,
        drift_record: DriftMonitoringRecord,
        model: ModelArtifact | None = None,
        actor: str = "system",
    ) -> MonitoringAlert:
        subject_id = model.id if model is not None else drift_record.model_artifact_id
        return await self.create_alert(
            alert_type="DRIFT_DETECTED",
            severity="warning" if drift_record.drift_detected else "info",
            subject_type="model_artifact",
            subject_id=subject_id,
            model_artifact_id=subject_id,
            summary="Drift monitoring evidence requires operator review.",
            evidence={
                "drift_record_id": drift_record.id,
                "drift_kind": drift_record.drift_kind,
                "drift_detected": drift_record.drift_detected,
                "signals": drift_record.signals,
                "evidence_summary": drift_record.evidence_summary,
            },
            lineage={
                "source": "w2_u10_drift_monitoring_record",
                "model_version": model.version if model is not None else None,
                "experiment_id": model.experiment_id if model is not None else None,
            },
            actor=actor,
        )

    async def create_signal_withheld_alert(
        self,
        *,
        signal: AdvisorySignal,
        actor: str = "system",
    ) -> MonitoringAlert:
        return await self.create_alert(
            alert_type="SIGNAL_WITHHELD",
            severity="warning",
            subject_type="advisory_signal",
            subject_id=signal.signal_id,
            market_class=signal.market_class,
            symbol=signal.symbol,
            timeframe=signal.timeframe,
            model_artifact_id=signal.model_artifact_id,
            signal_id=signal.signal_id,
            summary="Advisory signal was withheld by guardrails.",
            evidence={
                "signal_state": signal.signal_state,
                "state_reason": signal.state_reason,
                "freshness_status": signal.freshness_status,
            },
            lineage={
                "experiment_id": signal.experiment_id,
                "model_version": signal.model_version,
                "feature_set_version": signal.feature_set_version,
            },
            actor=actor,
        )

    async def list_alerts(self, filters: MonitoringAlertFilter) -> list[MonitoringAlert]:
        limit = min(max(filters.limit, 1), 200)
        stmt = select(MonitoringAlert)
        if filters.alert_type:
            stmt = stmt.where(MonitoringAlert.alert_type == filters.alert_type)
        if filters.severity:
            stmt = stmt.where(MonitoringAlert.severity == filters.severity)
        if filters.subject_type:
            stmt = stmt.where(MonitoringAlert.subject_type == filters.subject_type)
        if filters.subject_id:
            stmt = stmt.where(MonitoringAlert.subject_id == filters.subject_id)
        if filters.acknowledged is not None:
            stmt = stmt.where(MonitoringAlert.acknowledged == filters.acknowledged)
        stmt = stmt.order_by(MonitoringAlert.created_at.desc()).limit(limit)
        result = await self._session.scalars(stmt)
        return list(result.all())

    async def get_alert(self, alert_id: str) -> MonitoringAlert | None:
        return await self._session.get(MonitoringAlert, alert_id)

    async def acknowledge_alert(
        self,
        alert_id: str,
        *,
        actor: str,
    ) -> MonitoringAlert | None:
        alert = await self.get_alert(alert_id)
        if alert is None:
            return None
        alert.acknowledged = True
        alert.acknowledged_at = utc_now()
        alert.acknowledged_by = actor
        await self._session.flush()
        await self._audit.append(
            category="GOVERNANCE",
            action="monitoring_alert.acknowledged",
            actor=actor,
            resource_type="monitoring_alert",
            resource_id=alert.alert_id,
            message=f"Monitoring alert acknowledged alert_id={alert.alert_id}",
            details={"alert_id": alert.alert_id, "alert_type": alert.alert_type},
            correlation_id=alert.audit_correlation_id,
        )
        return alert
