"""Multi-market generalization, registry maturation, and drift design (W2-U10)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.time import require_utc
from app.db.models.calibration_report import CalibrationReport
from app.db.models.economic_report import EconomicReport
from app.db.models.generalization import DriftMonitoringRecord, GeneralizationReport
from app.db.models.model_artifact import ModelArtifact
from app.db.models.validation_report import ValidationReport
from app.ml.generalization.errors import AutoRetrainProhibitedError, GeneralizationLeakageError
from app.repositories.audit_repository import AuditRepository


@dataclass(frozen=True, slots=True)
class Domain:
    markets: tuple[str, ...]
    timeframes: tuple[str, ...]
    regimes: tuple[str, ...]

    def to_dict(self) -> dict[str, list[str]]:
        return {
            "markets": sorted(set(self.markets)),
            "timeframes": sorted(set(self.timeframes)),
            "regimes": sorted(set(self.regimes)),
        }

    def contains(self, *, market: str, timeframe: str, regime: str) -> bool:
        return (
            market in set(self.markets)
            and timeframe in set(self.timeframes)
            and regime in set(self.regimes)
        )


@dataclass(frozen=True, slots=True)
class GeneralizationInput:
    market: str
    timeframe: str
    regime: str
    accuracy: float
    sample_count: int


class GeneralizationService:
    """Creates research-only generalization and drift design records."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._audit = AuditRepository(session)

    async def create_report(
        self,
        *,
        experiment_id: str,
        model_artifact_id: str,
        trained_on: Domain,
        evaluated_on: Sequence[GeneralizationInput],
        operating_domain: Domain,
    ) -> GeneralizationReport:
        artifact = await self._load_artifact(model_artifact_id=model_artifact_id)
        train_markets = set(trained_on.markets)
        eval_markets = {item.market for item in evaluated_on}
        overlap = train_markets.intersection(eval_markets)
        if overlap:
            raise GeneralizationLeakageError(f"MARKET_HOLDOUT_LEAKAGE: {sorted(overlap)}")
        holdout_results = {
            "trained_on": trained_on.to_dict(),
            "evaluated_on": [asdict(item) for item in evaluated_on],
            "aggregate_accuracy": (
                sum(item.accuracy for item in evaluated_on) / len(evaluated_on)
                if evaluated_on
                else None
            ),
        }
        warnings = [
            self.domain_warning(
                operating_domain, market=item.market, timeframe=item.timeframe, regime=item.regime
            )
            for item in evaluated_on
        ]
        warnings = [warning for warning in warnings if warning]
        payload = {
            "experiment_id": experiment_id,
            "model_artifact_id": artifact.id,
            "trained_on": trained_on.to_dict(),
            "evaluated_on": [asdict(item) for item in evaluated_on],
            "holdout_results": holdout_results,
            "operating_domain": operating_domain.to_dict(),
            "unsupported_domain_warnings": warnings,
            "research_status": "research_only",
        }
        report_hash = hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode("utf-8")
        ).hexdigest()
        report = GeneralizationReport(
            experiment_id=experiment_id,
            model_artifact_id=artifact.id,
            trained_on=payload["trained_on"],
            evaluated_on=payload["evaluated_on"],
            holdout_results=holdout_results,
            operating_domain=payload["operating_domain"],
            unsupported_domain_warnings=warnings,
            report_hash=report_hash,
            research_status="research_only",
            notes="Research-only generalization report; no live signal.",
        )
        self._session.add(report)
        artifact.operating_domain = payload["operating_domain"]
        artifact.unsupported_domains = {"warnings": warnings}
        await self._session.flush()
        await self._audit_event(
            "generalization.report_created", report.id, experiment_id, report_hash
        )
        return report

    async def mature_registry_entry(
        self,
        *,
        model_artifact_id: str,
        statistical_report_id: str,
        calibration_report_id: str,
        economic_report_id: str,
        operating_domain: Domain,
        approval_note: str,
    ) -> ModelArtifact:
        artifact = await self._load_artifact(model_artifact_id=model_artifact_id)
        if await self._session.get(ValidationReport, statistical_report_id) is None:
            raise GeneralizationLeakageError("MISSING_STATISTICAL_REPORT_LINK")
        if await self._session.get(CalibrationReport, calibration_report_id) is None:
            raise GeneralizationLeakageError("MISSING_CALIBRATION_REPORT_LINK")
        if await self._session.get(EconomicReport, economic_report_id) is None:
            raise GeneralizationLeakageError("MISSING_ECONOMIC_REPORT_LINK")
        artifact.statistical_report_id = statistical_report_id
        artifact.calibration_report_id = calibration_report_id
        artifact.economic_report_id = economic_report_id
        artifact.operating_domain = operating_domain.to_dict()
        artifact.approval_history = [
            {
                "status": "research_validated",
                "note": approval_note,
            }
        ]
        artifact.research_status = "research_only"
        await self._session.flush()
        return artifact

    async def record_drift_signal(
        self,
        *,
        model_artifact_id: str,
        drift_kind: str,
        window_start: datetime,
        window_end: datetime,
        signals: dict,
        auto_retrain_requested: bool = False,
    ) -> DriftMonitoringRecord:
        artifact = await self._load_artifact(model_artifact_id=model_artifact_id)
        start = require_utc(window_start, boundary="drift.window_start")
        end = require_utc(window_end, boundary="drift.window_end")
        assert start is not None and end is not None
        drift_detected = bool(signals.get("drift_detected", False))
        payload = {
            "model_artifact_id": artifact.id,
            "drift_kind": drift_kind,
            "window_start": start.isoformat(),
            "window_end": end.isoformat(),
            "signals": signals,
            "drift_detected": drift_detected,
            "auto_retrain_requested": auto_retrain_requested,
            "retrain_triggered": False,
            "governance_required": True,
        }
        record_hash = hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode("utf-8")
        ).hexdigest()
        record = DriftMonitoringRecord(
            model_artifact_id=artifact.id,
            drift_kind=drift_kind,
            window_start=start,
            window_end=end,
            signals=signals,
            drift_detected=drift_detected,
            auto_retrain_requested=auto_retrain_requested,
            retrain_triggered=False,
            governance_required=True,
            evidence_summary=(
                "Drift recorded for research review; automatic retraining is prohibited."
            ),
            record_hash=record_hash,
            research_status="research_only",
        )
        self._session.add(record)
        await self._session.flush()
        if auto_retrain_requested:
            await self._audit_event(
                "drift.auto_retrain_refused",
                record.id,
                artifact.experiment_id or "unknown",
                record_hash,
            )
        return record

    def domain_warning(
        self, domain: Domain, *, market: str, timeframe: str, regime: str
    ) -> dict | None:
        if domain.contains(market=market, timeframe=timeframe, regime=regime):
            return None
        return {
            "warning": "UNSUPPORTED_DOMAIN",
            "market": market,
            "timeframe": timeframe,
            "regime": regime,
        }

    def assert_no_auto_retrain(self, record: DriftMonitoringRecord) -> None:
        if record.retrain_triggered:
            raise AutoRetrainProhibitedError("AUTO_RETRAIN_PROHIBITED")

    async def _load_artifact(self, *, model_artifact_id: str) -> ModelArtifact:
        artifact = await self._session.get(ModelArtifact, model_artifact_id)
        if artifact is None:
            raise GeneralizationLeakageError("MODEL_ARTIFACT_NOT_FOUND")
        return artifact

    async def _audit_event(
        self, action: str, resource_id: str, experiment_id: str, report_hash: str
    ) -> None:
        await self._audit.append(
            category="ML",
            action=action,
            actor="system",
            resource_type="generalization",
            resource_id=resource_id,
            message=f"Generalization/drift action {action} experiment={experiment_id}",
            details={"experiment_id": experiment_id, "report_hash": report_hash},
        )
