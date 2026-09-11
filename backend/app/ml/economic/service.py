"""Economic validation framework (W2-U09)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.calibration_report import CalibrationReport
from app.db.models.economic_report import EconomicReport
from app.db.models.experiment import Experiment
from app.db.models.model_artifact import ModelArtifact
from app.db.models.validation_report import ValidationReport
from app.ml.economic.errors import (
    CostInputInvalidError,
    EconomicPinError,
    EconomicReportInvalidError,
)
from app.repositories.audit_repository import AuditRepository


class CostProvenance(StrEnum):
    MEASURED = "measured"
    PROVIDER_PUBLISHED = "provider_published"
    ASSUMED = "assumed"


@dataclass(frozen=True, slots=True)
class CostInput:
    name: str
    value_bps: float
    provenance: CostProvenance
    low_bps: float | None = None
    high_bps: float | None = None
    detail: str = ""

    def validate(self) -> None:
        if self.value_bps < 0:
            raise CostInputInvalidError(f"negative cost input: {self.name}")
        if self.provenance == CostProvenance.ASSUMED:
            if self.low_bps is None or self.high_bps is None:
                raise CostInputInvalidError(f"ASSUMED_COST_REQUIRES_SENSITIVITY: {self.name}")
            if not self.low_bps <= self.value_bps <= self.high_bps:
                raise CostInputInvalidError(f"ASSUMED_COST_RANGE_INVALID: {self.name}")


@dataclass(frozen=True, slots=True)
class CostScenario:
    name: str
    costs: list[CostInput]

    def validate(self) -> None:
        required = {"spread", "commission", "slippage", "latency", "liquidity", "transaction_costs"}
        present = {cost.name for cost in self.costs}
        missing = sorted(required - present)
        if missing:
            raise CostInputInvalidError(f"MISSING_COST_INPUTS: {missing}")
        for cost in self.costs:
            cost.validate()


@dataclass(frozen=True, slots=True)
class HypotheticalTrade:
    gross_return_bps: float
    market_class: str = "unknown"
    timeframe: str = "unknown"
    regime: str = "unknown"


class EconomicValidationService:
    """Creates research-only economic validation reports."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._audit = AuditRepository(session)

    async def validate(
        self,
        *,
        experiment_id: str,
        model_artifact_id: str,
        validation_report_id: str | None,
        calibration_report_id: str | None,
        trades: Sequence[HypotheticalTrade],
        statistical_conclusion: dict,
        scenarios: Sequence[CostScenario],
    ) -> EconomicReport:
        experiment, artifact, validation, calibration = await self._resolve_pins(
            experiment_id=experiment_id,
            model_artifact_id=model_artifact_id,
            validation_report_id=validation_report_id,
            calibration_report_id=calibration_report_id,
        )
        payload = self.build_payload(
            trades=trades,
            statistical_conclusion=statistical_conclusion,
            scenarios=scenarios,
        )
        payload.update(
            {
                "experiment_id": experiment.experiment_id,
                "model_artifact_id": artifact.id,
                "validation_report_id": validation.id if validation else None,
                "calibration_report_id": calibration.id if calibration else None,
                "research_status": "research_only",
            }
        )
        self.validate_report_contract(payload)
        report_hash = hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode("utf-8")
        ).hexdigest()
        report = EconomicReport(
            experiment_id=experiment.experiment_id,
            model_artifact_id=artifact.id,
            validation_report_id=validation.id if validation else None,
            calibration_report_id=calibration.id if calibration else None,
            cost_model=payload["cost_model"],
            scenario_results=payload["scenario_results"],
            statistical_conclusion=payload["statistical_conclusion"],
            economic_conclusion=payload["economic_conclusion"],
            sensitivity_summary=payload["sensitivity_summary"],
            per_slice=payload["per_slice"],
            report_hash=report_hash,
            research_status="research_only",
            notes="Research-only economic validation; hypothetical P&L only, no execution.",
        )
        self._session.add(report)
        await self._session.flush()
        await self._audit.append(
            category="ML",
            action="economic.report_created",
            actor="system",
            resource_type="economic_report",
            resource_id=report.id,
            message=f"Economic report created experiment={experiment.experiment_id}",
            details={"experiment_id": experiment.experiment_id, "report_hash": report_hash},
        )
        return report

    def build_payload(
        self,
        *,
        trades: Sequence[HypotheticalTrade],
        statistical_conclusion: dict,
        scenarios: Sequence[CostScenario],
    ) -> dict:
        if not trades:
            raise EconomicReportInvalidError("ECONOMIC_TRADES_REQUIRED")
        if "verdict" not in statistical_conclusion:
            raise EconomicReportInvalidError("STATISTICAL_CONCLUSION_REQUIRED")
        scenario_results = {
            scenario.name: self._scenario_result(trades, scenario) for scenario in scenarios
        }
        economic_verdict = "economically_usable"
        if (
            scenario_results.get("base", next(iter(scenario_results.values())))["net_return_bps"]
            <= 0
        ):
            economic_verdict = "economically_unusable"
        headline = None
        if (
            statistical_conclusion.get("verdict") == "statistically_positive"
            and economic_verdict == "economically_unusable"
        ):
            headline = "STATISTICALLY_POSITIVE_ECONOMICALLY_NEGATIVE"
        payload = {
            "cost_model": {
                scenario.name: [asdict(cost) for cost in scenario.costs] for scenario in scenarios
            },
            "scenario_results": scenario_results,
            "statistical_conclusion": statistical_conclusion,
            "economic_conclusion": {"verdict": economic_verdict, "headline": headline},
            "sensitivity_summary": self._sensitivity_summary(scenario_results),
            "per_slice": self._per_slice(trades=trades, scenario=next(iter(scenarios))),
        }
        return payload

    def validate_report_contract(self, payload: dict) -> None:
        required = [
            "statistical_conclusion",
            "economic_conclusion",
            "scenario_results",
            "cost_model",
        ]
        missing = [key for key in required if not payload.get(key)]
        if missing:
            raise EconomicReportInvalidError(f"ECONOMIC_REPORT_INCOMPLETE: {missing}")
        if payload["statistical_conclusion"] == payload["economic_conclusion"]:
            raise EconomicReportInvalidError("CONFLATED_STAT_ECON_CONCLUSION")
        if not isinstance(payload["statistical_conclusion"], dict) or not isinstance(
            payload["economic_conclusion"], dict
        ):
            raise EconomicReportInvalidError("CONFLATED_STAT_ECON_CONCLUSION")
        for scenario_name, costs in payload["cost_model"].items():
            if not costs:
                raise CostInputInvalidError(f"NO_COSTS_DECLARED: {scenario_name}")
            for cost in costs:
                if "provenance" not in cost:
                    raise CostInputInvalidError(f"UNDECLARED_COST_PROVENANCE: {scenario_name}")
                if cost["provenance"] == CostProvenance.ASSUMED.value and (
                    cost.get("low_bps") is None or cost.get("high_bps") is None
                ):
                    raise CostInputInvalidError(
                        f"ASSUMED_COST_REQUIRES_SENSITIVITY: {scenario_name}"
                    )

    async def _resolve_pins(
        self,
        *,
        experiment_id: str,
        model_artifact_id: str,
        validation_report_id: str | None,
        calibration_report_id: str | None,
    ) -> tuple[Experiment, ModelArtifact, ValidationReport | None, CalibrationReport | None]:
        from sqlalchemy import select

        result = await self._session.execute(
            select(Experiment)
            .where(Experiment.experiment_id == experiment_id)
            .order_by(Experiment.version.desc())
        )
        experiment = result.scalars().first()
        artifact = await self._session.get(ModelArtifact, model_artifact_id)
        validation = (
            await self._session.get(ValidationReport, validation_report_id)
            if validation_report_id
            else None
        )
        calibration = (
            await self._session.get(CalibrationReport, calibration_report_id)
            if calibration_report_id
            else None
        )
        if experiment is None or artifact is None:
            raise EconomicPinError("ECONOMIC_PIN_UNRESOLVED")
        if artifact.experiment_id != experiment.experiment_id:
            raise EconomicPinError("ECONOMIC_MODEL_EXPERIMENT_MISMATCH")
        if validation is not None and validation.experiment_id != experiment.experiment_id:
            raise EconomicPinError("ECONOMIC_VALIDATION_EXPERIMENT_MISMATCH")
        if calibration is not None and calibration.experiment_id != experiment.experiment_id:
            raise EconomicPinError("ECONOMIC_CALIBRATION_EXPERIMENT_MISMATCH")
        return experiment, artifact, validation, calibration

    def _scenario_result(self, trades: Sequence[HypotheticalTrade], scenario: CostScenario) -> dict:
        scenario.validate()
        total_cost = sum(cost.value_bps for cost in scenario.costs)
        gross = sum(trade.gross_return_bps for trade in trades)
        net = gross - total_cost * len(trades)
        return {
            "gross_return_bps": gross,
            "total_cost_bps_per_trade": total_cost,
            "net_return_bps": net,
            "trade_count": len(trades),
        }

    def _sensitivity_summary(self, scenario_results: dict[str, dict]) -> dict:
        values = [result["net_return_bps"] for result in scenario_results.values()]
        return {"min_net_return_bps": min(values), "max_net_return_bps": max(values)}

    def _per_slice(self, *, trades: Sequence[HypotheticalTrade], scenario: CostScenario) -> dict:
        result: dict[str, dict] = {}
        cost = sum(item.value_bps for item in scenario.costs)
        for field in ("market_class", "timeframe", "regime"):
            result[field] = {}
            for value in sorted({getattr(trade, field) for trade in trades}):
                subset = [trade for trade in trades if getattr(trade, field) == value]
                gross = sum(trade.gross_return_bps for trade in subset)
                result[field][value] = {
                    "trade_count": len(subset),
                    "gross_return_bps": gross,
                    "net_return_bps": gross - cost * len(subset),
                }
        return result
