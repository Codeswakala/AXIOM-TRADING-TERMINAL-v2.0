"""Correlation Intelligence report service (W4-U02)."""

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
from app.db.models.correlation_report import CorrelationReport
from app.institutional_intelligence.contracts import (
    IntelligenceArtifactDraft,
    IntelligenceArtifactFactory,
)
from app.institutional_intelligence.scientific_fallbacks import pearson_correlation
from app.repositories.audit_repository import AuditRepository


@dataclass(frozen=True, slots=True)
class CorrelationSeriesSpec:
    market_class: str
    symbol: str
    timeframe: str


@dataclass(frozen=True, slots=True)
class CorrelationComputationResult:
    report: CorrelationReport
    excluded_future_candle_count: int


class CorrelationReportService:
    """Creates persisted, audited, research-only correlation reports."""

    method_version = "w4-u02.pearson_pure_python.v1"

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._audit = AuditRepository(session)
        self._factory = IntelligenceArtifactFactory()

    async def create_report(
        self,
        *,
        left: CorrelationSeriesSpec,
        right: CorrelationSeriesSpec,
        as_of_start: datetime,
        as_of_end: datetime,
        actor: str = "system",
    ) -> CorrelationComputationResult:
        start = require_utc(as_of_start, boundary="correlation_report.as_of_start")
        end = require_utc(as_of_end, boundary="correlation_report.as_of_end")
        assert start is not None and end is not None
        if start > end:
            raise ValueError("CORRELATION_AS_OF_RANGE_INVALID")
        if end > utc_now():
            raise ValueError("CORRELATION_FUTURE_AS_OF_REFUSED")
        left_rows = await self._series_rows(left, start, end)
        right_rows = await self._series_rows(right, start, end)
        aligned = self._align(left_rows, right_rows)
        if len(aligned) < 3:
            raise ValueError("CORRELATION_REQUIRES_THREE_ALIGNED_POINTS")
        left_values = [item[1] for item in aligned]
        right_values = [item[2] for item in aligned]
        coefficient = pearson_correlation(left_values, right_values)
        uncertainty = self._fisher_interval(coefficient=coefficient, sample_count=len(aligned))
        excluded_future_count = (
            await self._future_count(left, end) + await self._future_count(right, end)
        )
        source_ids = [item[3] for item in aligned] + [item[4] for item in aligned]
        results = {
            "correlation_coefficient": coefficient,
            "estimator": "pearson",
            "statistical_significance": {
                "method": "not_computed_pure_python_foundation",
                "p_value": None,
                "statistically_significant": None,
            },
            "economic_usefulness": {
                "verdict": "not_assessed",
                "reason": "Correlation is research context and is not an economic edge or signal.",
            },
            "excluded_future_candle_count": excluded_future_count,
        }
        draft = IntelligenceArtifactDraft(
            artifact_type="correlation_report",
            method_version=self.method_version,
            config={
                "estimator": "pearson",
                "implementation": "pure_python_fallback",
                "left": asdict(left),
                "right": asdict(right),
            },
            input_lineage={
                "left_series": asdict(left),
                "right_series": asdict(right),
                "as_of_start": start.isoformat(),
                "as_of_end": end.isoformat(),
                "aligned_timestamps": [item[0].isoformat() for item in aligned],
                "excluded_future_candle_count": excluded_future_count,
            },
            source_artifact_ids=source_ids,
            market_scope={
                "left_market_class": left.market_class,
                "right_market_class": right.market_class,
                "symbols": [left.symbol, right.symbol],
                "timeframe": left.timeframe,
            },
            as_of_start=start,
            as_of_end=end,
            sample_count=len(aligned),
            uncertainty=uncertainty,
            results=results,
            limitations=[
                "correlation_does_not_imply_causation",
                "research_only_not_a_signal",
                "not_a_trade_instruction",
                "economic_usefulness_not_assessed",
            ],
            created_by=actor,
        )
        artifact = self._factory.build(draft)
        report = CorrelationReport(
            id=artifact.artifact_id,
            created_at=artifact.created_at,
            artifact_type=artifact.artifact_type,
            method_version=artifact.method_version,
            left_market_class=left.market_class,
            left_symbol=left.symbol,
            right_market_class=right.market_class,
            right_symbol=right.symbol,
            timeframe=left.timeframe,
            as_of_start=start,
            as_of_end=end,
            sample_count=artifact.sample_count,
            correlation_value=coefficient,
            uncertainty=artifact.uncertainty,
            significance=results["statistical_significance"],
            economic_usefulness=results["economic_usefulness"],
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
            notes="Research-only correlation context; not a signal and not causation.",
        )
        self._session.add(report)
        await self._session.flush()
        await self._audit.append(
            category="GOVERNANCE",
            action="correlation_report.created",
            actor=actor,
            resource_type="correlation_report",
            resource_id=report.id,
            message=(
                f"Correlation report created {left.symbol}/{right.symbol} "
                f"sample_count={report.sample_count}"
            ),
            details=artifact.to_audit_details(),
            correlation_id=report.audit_correlation_id,
        )
        return CorrelationComputationResult(
            report=report,
            excluded_future_candle_count=excluded_future_count,
        )

    async def list_reports(self, *, limit: int = 50) -> list[CorrelationReport]:
        result = await self._session.scalars(
            select(CorrelationReport).order_by(CorrelationReport.created_at.desc()).limit(limit)
        )
        return list(result.all())

    async def get_report(self, report_id: str) -> CorrelationReport | None:
        return await self._session.get(CorrelationReport, report_id)

    async def _series_rows(
        self,
        spec: CorrelationSeriesSpec,
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
            open_time = coerce_external_utc(row.open_time, source="correlation_report.open_time")
            assert open_time is not None
            output.append((open_time, self._to_float(row.close), row.id))
        return output

    async def _future_count(self, spec: CorrelationSeriesSpec, end: datetime) -> int:
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

    def _align(
        self,
        left_rows: Sequence[tuple[datetime, float, str]],
        right_rows: Sequence[tuple[datetime, float, str]],
    ) -> list[tuple[datetime, float, float, str, str]]:
        right_by_time = {item[0]: (item[1], item[2]) for item in right_rows}
        aligned: list[tuple[datetime, float, float, str, str]] = []
        for timestamp, left_value, left_id in left_rows:
            right_item = right_by_time.get(timestamp)
            if right_item is not None:
                aligned.append((timestamp, left_value, right_item[0], left_id, right_item[1]))
        return aligned

    def _fisher_interval(self, *, coefficient: float, sample_count: int) -> dict[str, Any]:
        if sample_count <= 3:
            return {
                "method": "fisher_z_interval_insufficient_sample",
                "lower": -1.0,
                "upper": 1.0,
                "confidence_level": 0.95,
                "sample_count": sample_count,
            }
        clamped = min(0.999999, max(-0.999999, coefficient))
        z_value = math.atanh(clamped)
        se = 1.0 / math.sqrt(sample_count - 3)
        z_score = 1.96
        return {
            "method": "fisher_z_interval",
            "lower": math.tanh(z_value - z_score * se),
            "upper": math.tanh(z_value + z_score * se),
            "confidence_level": 0.95,
            "sample_count": sample_count,
        }

    def _to_float(self, value: Decimal | float | int) -> float:
        return float(value)

    async def assert_no_signal_side_effect(self, before_count: int) -> None:
        result = await self._session.execute(select(AdvisorySignal))
        after_count = len(result.scalars().all())
        if after_count != before_count:
            raise AssertionError("CORRELATION_REPORT_SIGNAL_SIDE_EFFECT")
