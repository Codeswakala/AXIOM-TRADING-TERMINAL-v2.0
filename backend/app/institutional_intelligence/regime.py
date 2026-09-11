"""Explainable market-regime detection reports (W4-U03)."""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.time import coerce_external_utc, require_utc, utc_now
from app.db.models.advisory_signal import AdvisorySignal
from app.db.models.candle import Candle
from app.db.models.model_artifact import ModelArtifact
from app.db.models.regime_report import RegimeReport
from app.institutional_intelligence.contracts import (
    IntelligenceArtifactDraft,
    IntelligenceArtifactFactory,
)
from app.repositories.audit_repository import AuditRepository


@dataclass(frozen=True, slots=True)
class RegimeSeriesSpec:
    market_class: str
    symbol: str
    timeframe: str


@dataclass(frozen=True, slots=True)
class RegimeFeatureVector:
    normalized_total_return: float
    trend_efficiency: float
    normalized_volatility: float
    sample_count: int


@dataclass(frozen=True, slots=True)
class RegimeClassification:
    label: str
    confidence: float
    evidence: dict[str, Any]


@dataclass(frozen=True, slots=True)
class RegimeComputationResult:
    report: RegimeReport
    excluded_future_candle_count: int


class RegimeReportService:
    """Creates persisted, audited, explainable regime reports."""

    method_version = "w4-u03.rules_normalized_features.v1"
    thresholds = {
        "trend_efficiency": 0.72,
        "volatile_volatility": 0.035,
        "calm_volatility": 0.006,
        "minimum_confidence": 0.50,
        "maximum_confidence": 0.95,
    }

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._audit = AuditRepository(session)
        self._factory = IntelligenceArtifactFactory()

    async def create_report(
        self,
        *,
        series: RegimeSeriesSpec,
        as_of_start: datetime,
        as_of_end: datetime,
        actor: str = "system",
    ) -> RegimeComputationResult:
        start = require_utc(as_of_start, boundary="regime_report.as_of_start")
        end = require_utc(as_of_end, boundary="regime_report.as_of_end")
        assert start is not None and end is not None
        if start > end:
            raise ValueError("REGIME_AS_OF_RANGE_INVALID")
        if end > utc_now():
            raise ValueError("REGIME_FUTURE_AS_OF_REFUSED")
        rows = await self._series_rows(series, start, end)
        if len(rows) < 4:
            raise ValueError("REGIME_REQUIRES_FOUR_OR_MORE_POINTS")
        features = self.features_from_closes([item[1] for item in rows])
        classification = self.classify_features(features)
        future_count = await self._future_count(series, end)
        evidence = {
            **classification.evidence,
            "normalized_features": asdict(features),
            "thresholds": self.thresholds,
            "excluded_future_candle_count": future_count,
            "feature_policy": "normalized_features_no_symbol_identity",
        }
        results = {
            "regime_label": classification.label,
            "confidence": classification.confidence,
            "evidence": evidence,
            "economic_meaning": {
                "verdict": "not_assessed",
                "reason": "Regime is research context and is not an economic edge or signal.",
            },
        }
        uncertainty = {
            "method": "threshold_margin_confidence_band",
            "lower": max(0.0, classification.confidence - 0.10),
            "upper": min(1.0, classification.confidence + 0.10),
            "confidence_level": 0.95,
            "sample_count": len(rows),
        }
        source_ids = [item[2] for item in rows]
        draft = IntelligenceArtifactDraft(
            artifact_type="regime_report",
            method_version=self.method_version,
            config={
                "implementation": "pure_python_rules",
                "series": asdict(series),
                "thresholds": self.thresholds,
            },
            input_lineage={
                "series": asdict(series),
                "as_of_start": start.isoformat(),
                "as_of_end": end.isoformat(),
                "included_timestamps": [item[0].isoformat() for item in rows],
                "excluded_future_candle_count": future_count,
                "features_exclude": ["symbol", "provider", "market_class"],
            },
            source_artifact_ids=source_ids,
            market_scope={
                "market_class": series.market_class,
                "timeframe": series.timeframe,
                "symbol_metadata_only": series.symbol,
            },
            as_of_start=start,
            as_of_end=end,
            sample_count=len(rows),
            uncertainty=uncertainty,
            results=results,
            limitations=[
                "regime_is_research_context_not_signal",
                "not_a_trade_instruction",
                "economic_usefulness_not_assessed",
                "normalized_features_exclude_symbol_identity",
            ],
            created_by=actor,
        )
        artifact = self._factory.build(draft)
        report = RegimeReport(
            id=artifact.artifact_id,
            created_at=artifact.created_at,
            artifact_type=artifact.artifact_type,
            method_version=artifact.method_version,
            market_class=series.market_class,
            symbol=series.symbol,
            timeframe=series.timeframe,
            as_of_start=start,
            as_of_end=end,
            sample_count=artifact.sample_count,
            regime_label=classification.label,
            confidence=classification.confidence,
            uncertainty=artifact.uncertainty,
            evidence=evidence,
            economic_meaning=results["economic_meaning"],
            config=artifact.config,
            input_lineage=artifact.input_lineage,
            source_artifact_ids=list(artifact.source_artifact_ids),
            market_scope=artifact.market_scope,
            results=artifact.results,
            limitations=list(artifact.limitations),
            report_hash=artifact.report_hash,
            research_status=artifact.research_status,
            created_by=artifact.created_by,
            audit_correlation_id=artifact.audit_correlation_id,
            notes="Research-only regime context; not a signal or instruction.",
        )
        self._session.add(report)
        await self._session.flush()
        await self._audit.append(
            category="GOVERNANCE",
            action="regime_report.created",
            actor=actor,
            resource_type="regime_report",
            resource_id=report.id,
            message=(
                f"Regime report created {series.symbol} label={report.regime_label} "
                f"sample_count={report.sample_count}"
            ),
            details=artifact.to_audit_details(),
            correlation_id=report.audit_correlation_id,
        )
        return RegimeComputationResult(report=report, excluded_future_candle_count=future_count)

    def features_from_closes(self, closes: Sequence[Decimal | float | int]) -> RegimeFeatureVector:
        if len(closes) < 4:
            raise ValueError("REGIME_REQUIRES_FOUR_OR_MORE_POINTS")
        values = [float(value) for value in closes]
        returns = [
            0.0
            if values[index - 1] == 0
            else (values[index] - values[index - 1]) / values[index - 1]
            for index in range(1, len(values))
        ]
        total_return = 0.0 if values[0] == 0 else (values[-1] - values[0]) / values[0]
        path_length = sum(abs(item) for item in returns)
        trend_efficiency = 0.0 if path_length == 0 else min(1.0, abs(total_return) / path_length)
        volatility = self._stddev(returns)
        return RegimeFeatureVector(
            normalized_total_return=round(total_return, 12),
            trend_efficiency=round(trend_efficiency, 12),
            normalized_volatility=round(volatility, 12),
            sample_count=len(values),
        )

    def classify_features(self, features: RegimeFeatureVector) -> RegimeClassification:
        if features.sample_count < 4:
            raise ValueError("REGIME_CONFIDENCE_REQUIRED")
        if features.normalized_volatility >= self.thresholds["volatile_volatility"]:
            margin = features.normalized_volatility - self.thresholds["volatile_volatility"]
            confidence = self._confidence(0.65 + margin * 3.0)
            return RegimeClassification(
                label="volatile",
                confidence=confidence,
                evidence={"rule": "normalized_volatility >= volatile_volatility"},
            )
        if features.trend_efficiency >= self.thresholds["trend_efficiency"]:
            margin = features.trend_efficiency - self.thresholds["trend_efficiency"]
            confidence = self._confidence(0.65 + margin)
            return RegimeClassification(
                label="trend",
                confidence=confidence,
                evidence={"rule": "trend_efficiency >= trend_efficiency_threshold"},
            )
        if features.normalized_volatility <= self.thresholds["calm_volatility"]:
            margin = self.thresholds["calm_volatility"] - features.normalized_volatility
            confidence = self._confidence(0.60 + margin * 5.0)
            return RegimeClassification(
                label="calm",
                confidence=confidence,
                evidence={"rule": "normalized_volatility <= calm_volatility"},
            )
        confidence = self._confidence(0.58 + (1.0 - features.trend_efficiency) * 0.10)
        return RegimeClassification(
            label="range",
            confidence=confidence,
            evidence={"rule": "default_range_after_trend_volatility_checks"},
        )

    async def list_reports(self, *, limit: int = 50) -> list[RegimeReport]:
        result = await self._session.scalars(
            select(RegimeReport).order_by(RegimeReport.created_at.desc()).limit(limit)
        )
        return list(result.all())

    async def get_report(self, report_id: str) -> RegimeReport | None:
        return await self._session.get(RegimeReport, report_id)

    async def assert_no_side_effects(
        self, *, model_statuses: dict[str, str], signal_count: int
    ) -> None:
        signals = list((await self._session.scalars(select(AdvisorySignal))).all())
        if len(signals) != signal_count:
            raise AssertionError("REGIME_REPORT_SIGNAL_SIDE_EFFECT")
        for model_id, status in model_statuses.items():
            model = await self._session.get(ModelArtifact, model_id)
            if model is not None and model.status != status:
                raise AssertionError("REGIME_REPORT_MODEL_MUTATION")

    async def _series_rows(
        self,
        spec: RegimeSeriesSpec,
        start: datetime,
        end: datetime,
    ) -> list[tuple[datetime, float, str]]:
        stmt = (
            select(Candle)
            .where(
                Candle.market_class == spec.market_class,
                Candle.symbol == spec.symbol,
                Candle.timeframe == spec.timeframe,
                Candle.open_time >= start,
                Candle.open_time <= end,
            )
            .order_by(Candle.open_time.asc())
        )
        rows = list((await self._session.scalars(stmt)).all())
        output: list[tuple[datetime, float, str]] = []
        for row in rows:
            open_time = coerce_external_utc(row.open_time, source="regime_report.open_time")
            assert open_time is not None
            output.append((open_time, float(row.close), row.id))
        return output

    async def _future_count(self, spec: RegimeSeriesSpec, end: datetime) -> int:
        from sqlalchemy import func

        stmt = (
            select(func.count())
            .select_from(Candle)
            .where(
                Candle.market_class == spec.market_class,
                Candle.symbol == spec.symbol,
                Candle.timeframe == spec.timeframe,
                Candle.open_time > end,
            )
        )
        return int((await self._session.execute(stmt)).scalar_one())

    def _confidence(self, value: float) -> float:
        return min(
            self.thresholds["maximum_confidence"],
            max(self.thresholds["minimum_confidence"], value),
        )

    def _stddev(self, values: Sequence[float]) -> float:
        if not values:
            return 0.0
        average = sum(values) / len(values)
        variance = sum((value - average) ** 2 for value in values) / len(values)
        return math.sqrt(variance)
