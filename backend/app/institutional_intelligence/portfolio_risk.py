"""Hypothetical portfolio/risk research reports (W4-U05)."""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.time import coerce_external_utc, require_utc, utc_now
from app.db.models.advisory_signal import AdvisorySignal
from app.db.models.candle import Candle
from app.db.models.model_artifact import ModelArtifact
from app.db.models.portfolio_risk_report import PortfolioRiskReport
from app.institutional_intelligence.contracts import (
    IntelligenceArtifactDraft,
    IntelligenceArtifactFactory,
)
from app.repositories.audit_repository import AuditRepository


@dataclass(frozen=True, slots=True)
class PortfolioRiskSeriesSpec:
    market_class: str
    symbol: str
    timeframe: str


@dataclass(frozen=True, slots=True)
class PortfolioRiskAssumptions:
    report_name: str
    stress_multiplier: float = 2.0
    tail_quantile: float = 0.05


@dataclass(frozen=True, slots=True)
class PortfolioRiskComputationResult:
    report: PortfolioRiskReport
    excluded_future_candle_count: int


class PortfolioRiskReportService:
    """Creates persisted, audited, hypothetical market-series risk reports."""

    method_version = "w4-u05.market_series_risk_pure_python.v1"

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._audit = AuditRepository(session)
        self._factory = IntelligenceArtifactFactory()

    async def create_report(
        self,
        *,
        series: PortfolioRiskSeriesSpec,
        assumptions: PortfolioRiskAssumptions,
        as_of_start: datetime,
        as_of_end: datetime,
        actor: str = "system",
    ) -> PortfolioRiskComputationResult:
        start = require_utc(as_of_start, boundary="portfolio_risk_report.as_of_start")
        end = require_utc(as_of_end, boundary="portfolio_risk_report.as_of_end")
        assert start is not None and end is not None
        if start > end:
            raise ValueError("PORTFOLIO_RISK_AS_OF_RANGE_INVALID")
        if end > utc_now():
            raise ValueError("PORTFOLIO_RISK_FUTURE_AS_OF_REFUSED")
        if assumptions.stress_multiplier <= 0:
            raise ValueError("PORTFOLIO_RISK_STRESS_MULTIPLIER_INVALID")
        if not 0 < assumptions.tail_quantile < 0.5:
            raise ValueError("PORTFOLIO_RISK_TAIL_QUANTILE_INVALID")
        rows = await self._series_rows(series, start, end)
        if len(rows) < 4:
            raise ValueError("PORTFOLIO_RISK_REQUIRES_FOUR_OR_MORE_POINTS")
        closes = [item[1] for item in rows]
        returns = self._returns(closes)
        realized_volatility = self._stddev(returns)
        max_drawdown = self._max_drawdown(closes)
        tail_loss = self._historical_tail_loss(returns, assumptions.tail_quantile)
        stress_loss = min(0.0, tail_loss * assumptions.stress_multiplier)
        future_count = await self._future_count(series, end)
        metric_uncertainty = self._metric_uncertainty(realized_volatility, len(rows))
        metrics = {
            "max_drawdown": {
                "value": max_drawdown,
                "sample_count": len(rows),
                "uncertainty": metric_uncertainty,
            },
            "realized_volatility": {
                "value": realized_volatility,
                "sample_count": len(rows),
                "uncertainty": metric_uncertainty,
            },
            "stress_loss": {
                "value": stress_loss,
                "sample_count": len(rows),
                "uncertainty": metric_uncertainty,
            },
        }
        economic_usefulness = {
            "verdict": "not_assessed",
            "reason": "Risk report is hypothetical research and not a real portfolio outcome.",
        }
        results = {
            "metrics": metrics,
            "economic_usefulness": economic_usefulness,
            "excluded_future_candle_count": future_count,
        }
        source_ids = [item[2] for item in rows]
        draft = IntelligenceArtifactDraft(
            artifact_type="portfolio_risk_report",
            method_version=self.method_version,
            config={
                "implementation": "pure_python_market_series_risk",
                "series": asdict(series),
                "assumptions": asdict(assumptions),
            },
            input_lineage={
                "series": asdict(series),
                "as_of_start": start.isoformat(),
                "as_of_end": end.isoformat(),
                "included_timestamps": [item[0].isoformat() for item in rows],
                "excluded_future_candle_count": future_count,
                "linkage_policy": "market_series_only_no_account_or_broker_linkage",
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
            uncertainty={
                "method": "volatility_scaled_interval",
                "lower": -abs(realized_volatility * assumptions.stress_multiplier),
                "upper": abs(realized_volatility * assumptions.stress_multiplier),
                "confidence_level": 0.95,
                "sample_count": len(rows),
            },
            results=results,
            limitations=[
                "hypothetical_market_series_research_only",
                "not_a_real_portfolio_or_account",
                "not_a_prediction",
                "not_a_guaranteed_return",
                "not_a_trade_instruction",
                "not_financial_advice",
                "economic_usefulness_not_assessed",
            ],
            created_by=actor,
        )
        artifact = self._factory.build(draft)
        report = PortfolioRiskReport(
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
            max_drawdown=max_drawdown,
            realized_volatility=realized_volatility,
            stress_loss=stress_loss,
            metrics=metrics,
            uncertainty=artifact.uncertainty,
            assumptions=asdict(assumptions),
            economic_usefulness=economic_usefulness,
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
            notes="Hypothetical market-series risk research; not a real portfolio or account.",
        )
        self._session.add(report)
        await self._session.flush()
        await self._audit.append(
            category="GOVERNANCE",
            action="portfolio_risk_report.created",
            actor=actor,
            resource_type="portfolio_risk_report",
            resource_id=report.id,
            message=(
                f"Portfolio risk report created {series.symbol} "
                f"sample_count={report.sample_count}"
            ),
            details=artifact.to_audit_details(),
            correlation_id=report.audit_correlation_id,
        )
        return PortfolioRiskComputationResult(
            report=report, excluded_future_candle_count=future_count
        )

    async def list_reports(self, *, limit: int = 50) -> list[PortfolioRiskReport]:
        result = await self._session.scalars(
            select(PortfolioRiskReport).order_by(PortfolioRiskReport.created_at.desc()).limit(limit)
        )
        return list(result.all())

    async def get_report(self, report_id: str) -> PortfolioRiskReport | None:
        return await self._session.get(PortfolioRiskReport, report_id)

    async def assert_no_side_effects(
        self, *, model_statuses: dict[str, str], signal_count: int
    ) -> None:
        signals = list((await self._session.scalars(select(AdvisorySignal))).all())
        if len(signals) != signal_count:
            raise AssertionError("PORTFOLIO_RISK_SIGNAL_SIDE_EFFECT")
        for model_id, status in model_statuses.items():
            model = await self._session.get(ModelArtifact, model_id)
            if model is not None and model.status != status:
                raise AssertionError("PORTFOLIO_RISK_MODEL_MUTATION")

    async def _series_rows(
        self,
        spec: PortfolioRiskSeriesSpec,
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
            open_time = coerce_external_utc(row.open_time, source="portfolio_risk_report.open_time")
            assert open_time is not None
            output.append((open_time, float(row.close), row.id))
        return output

    async def _future_count(self, spec: PortfolioRiskSeriesSpec, end: datetime) -> int:
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

    def _returns(self, values: Sequence[float]) -> list[float]:
        return [
            0.0
            if values[index - 1] == 0
            else (values[index] - values[index - 1]) / values[index - 1]
            for index in range(1, len(values))
        ]

    def _stddev(self, values: Sequence[float]) -> float:
        if not values:
            return 0.0
        average = sum(values) / len(values)
        variance = sum((value - average) ** 2 for value in values) / len(values)
        return math.sqrt(variance)

    def _max_drawdown(self, closes: Sequence[float]) -> float:
        peak = closes[0]
        drawdown = 0.0
        for value in closes:
            peak = max(peak, value)
            if peak != 0:
                drawdown = min(drawdown, (value - peak) / peak)
        return drawdown

    def _historical_tail_loss(self, returns: Sequence[float], quantile: float) -> float:
        ordered = sorted(returns)
        index = max(0, min(len(ordered) - 1, int(math.floor(quantile * len(ordered)))))
        return ordered[index]

    def _metric_uncertainty(
        self, realized_volatility: float, sample_count: int
    ) -> dict[str, float | int | str]:
        width = abs(realized_volatility)
        return {
            "method": "volatility_scaled_interval",
            "lower": -width,
            "upper": width,
            "confidence_level": 0.95,
            "sample_count": sample_count,
        }
