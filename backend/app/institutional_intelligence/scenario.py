"""Hypothetical scenario simulation research reports (W4-U04)."""

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
from app.db.models.scenario_report import ScenarioReport
from app.institutional_intelligence.contracts import (
    IntelligenceArtifactDraft,
    IntelligenceArtifactFactory,
)
from app.repositories.audit_repository import AuditRepository


@dataclass(frozen=True, slots=True)
class ScenarioSeriesSpec:
    market_class: str
    symbol: str
    timeframe: str


@dataclass(frozen=True, slots=True)
class ScenarioAssumptions:
    scenario_name: str
    shock_return: float
    horizon_bars: int
    volatility_multiplier: float = 1.0


@dataclass(frozen=True, slots=True)
class ScenarioComputationResult:
    report: ScenarioReport
    excluded_future_candle_count: int


class ScenarioReportService:
    """Creates persisted, audited, hypothetical scenario reports."""

    method_version = "w4-u04.hypothetical_path.v1"

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._audit = AuditRepository(session)
        self._factory = IntelligenceArtifactFactory()

    async def create_report(
        self,
        *,
        series: ScenarioSeriesSpec,
        assumptions: ScenarioAssumptions,
        as_of_start: datetime,
        as_of_end: datetime,
        actor: str = "system",
    ) -> ScenarioComputationResult:
        start = require_utc(as_of_start, boundary="scenario_report.as_of_start")
        end = require_utc(as_of_end, boundary="scenario_report.as_of_end")
        assert start is not None and end is not None
        if start > end:
            raise ValueError("SCENARIO_AS_OF_RANGE_INVALID")
        if end > utc_now():
            raise ValueError("SCENARIO_FUTURE_AS_OF_REFUSED")
        if assumptions.horizon_bars < 1:
            raise ValueError("SCENARIO_HORIZON_INVALID")
        rows = await self._series_rows(series, start, end)
        if len(rows) < 3:
            raise ValueError("SCENARIO_REQUIRES_THREE_OR_MORE_POINTS")
        returns = self._returns([item[1] for item in rows])
        realized_volatility = self._stddev(returns)
        last_value = rows[-1][1]
        hypothetical_return = assumptions.shock_return
        counterfactual_index = last_value * (1.0 + hypothetical_return)
        uncertainty_width = abs(realized_volatility * assumptions.volatility_multiplier)
        uncertainty = {
            "method": "historical_volatility_band",
            "lower": hypothetical_return - uncertainty_width,
            "upper": hypothetical_return + uncertainty_width,
            "confidence_level": 0.95,
            "sample_count": len(rows),
        }
        future_count = await self._future_count(series, end)
        scenario_result = {
            "hypothetical_return": hypothetical_return,
            "counterfactual_index": counterfactual_index,
            "baseline_last_value": last_value,
            "horizon_bars": assumptions.horizon_bars,
        }
        inputs = {
            "baseline_returns": returns,
            "realized_volatility": realized_volatility,
            "last_value": last_value,
        }
        economic_usefulness = {
            "verdict": "not_assessed",
            "reason": (
                "Scenario is hypothetical research and is not a tradable "
                "or economic instruction."
            ),
        }
        results = {
            "scenario_result": scenario_result,
            "economic_usefulness": economic_usefulness,
            "excluded_future_candle_count": future_count,
        }
        source_ids = [item[2] for item in rows]
        draft = IntelligenceArtifactDraft(
            artifact_type="scenario_report",
            method_version=self.method_version,
            config={
                "implementation": "pure_python_hypothetical_path",
                "series": asdict(series),
                "assumptions": asdict(assumptions),
            },
            input_lineage={
                "series": asdict(series),
                "as_of_start": start.isoformat(),
                "as_of_end": end.isoformat(),
                "included_timestamps": [item[0].isoformat() for item in rows],
                "excluded_future_candle_count": future_count,
                "input_policy": "as_of_bounded_hypothetical_research",
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
                "hypothetical_counterfactual_research_only",
                "not_a_prediction",
                "not_a_trade_instruction",
                "not_financial_advice",
                "economic_usefulness_not_assessed",
            ],
            created_by=actor,
        )
        artifact = self._factory.build(draft)
        report = ScenarioReport(
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
            scenario_name=assumptions.scenario_name,
            hypothetical_return=hypothetical_return,
            scenario_result=scenario_result,
            assumptions=asdict(assumptions),
            inputs=inputs,
            uncertainty=artifact.uncertainty,
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
            notes="Hypothetical research scenario; not an instruction or prediction.",
        )
        self._session.add(report)
        await self._session.flush()
        await self._audit.append(
            category="GOVERNANCE",
            action="scenario_report.created",
            actor=actor,
            resource_type="scenario_report",
            resource_id=report.id,
            message=f"Scenario report created {series.symbol} scenario={report.scenario_name}",
            details=artifact.to_audit_details(),
            correlation_id=report.audit_correlation_id,
        )
        return ScenarioComputationResult(report=report, excluded_future_candle_count=future_count)

    async def list_reports(self, *, limit: int = 50) -> list[ScenarioReport]:
        result = await self._session.scalars(
            select(ScenarioReport).order_by(ScenarioReport.created_at.desc()).limit(limit)
        )
        return list(result.all())

    async def get_report(self, report_id: str) -> ScenarioReport | None:
        return await self._session.get(ScenarioReport, report_id)

    async def assert_no_side_effects(
        self, *, model_statuses: dict[str, str], signal_count: int
    ) -> None:
        signals = list((await self._session.scalars(select(AdvisorySignal))).all())
        if len(signals) != signal_count:
            raise AssertionError("SCENARIO_REPORT_SIGNAL_SIDE_EFFECT")
        for model_id, status in model_statuses.items():
            model = await self._session.get(ModelArtifact, model_id)
            if model is not None and model.status != status:
                raise AssertionError("SCENARIO_REPORT_MODEL_MUTATION")

    async def _series_rows(
        self,
        spec: ScenarioSeriesSpec,
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
            open_time = coerce_external_utc(row.open_time, source="scenario_report.open_time")
            assert open_time is not None
            output.append((open_time, float(row.close), row.id))
        return output

    async def _future_count(self, spec: ScenarioSeriesSpec, end: datetime) -> int:
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
