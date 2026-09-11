"""BO-B-04 — intelligence generation request schemas.

These request contracts feed the five existing deterministic computation
services (correlation / regime / scenario / portfolio-risk / signal
validation). Generation is research-artifact creation only: no actuation,
no broker/account/execution state, no signal emission.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from app.core.time import coerce_external_utc


class SeriesSpecIn(BaseModel):
    """One market series reference for generation."""

    market_class: str = Field(min_length=1, max_length=32)
    symbol: str = Field(min_length=1, max_length=64)
    timeframe: str = Field(min_length=1, max_length=16)


class _AsOfWindow(BaseModel):
    """as-of bounded window (both bounds required; no look-ahead enforced by
    the services)."""

    as_of_start: datetime
    as_of_end: datetime

    @field_validator("as_of_start", "as_of_end")
    @classmethod
    def _utc(cls, value: datetime) -> datetime:
        normalized = coerce_external_utc(value, source="intelligence generation request")
        assert normalized is not None
        return normalized


class CorrelationGenerationRequest(_AsOfWindow):
    left: SeriesSpecIn
    right: SeriesSpecIn


class RegimeGenerationRequest(_AsOfWindow):
    series: SeriesSpecIn


class ScenarioAssumptionsIn(BaseModel):
    scenario_name: str = Field(min_length=1, max_length=128)
    shock_return: float
    horizon_bars: int = Field(ge=1, le=100_000)
    volatility_multiplier: float = Field(default=1.0, gt=0)


class ScenarioGenerationRequest(_AsOfWindow):
    series: SeriesSpecIn
    assumptions: ScenarioAssumptionsIn


class PortfolioRiskAssumptionsIn(BaseModel):
    report_name: str = Field(min_length=1, max_length=128)
    stress_multiplier: float = Field(default=2.0, gt=0)
    tail_quantile: float = Field(default=0.05, gt=0, lt=0.5)


class PortfolioRiskGenerationRequest(_AsOfWindow):
    series: SeriesSpecIn
    assumptions: PortfolioRiskAssumptionsIn


class SignalValidationGenerationRequest(BaseModel):
    scope_start: datetime
    scope_end: datetime
    market_class: str | None = None
    symbol: str | None = None
    timeframe: str | None = None
    include_states: list[str] = Field(
        default_factory=lambda: ["emitted", "warning", "withheld", "expired"]
    )

    @field_validator("scope_start", "scope_end")
    @classmethod
    def _utc(cls, value: datetime) -> datetime:
        normalized = coerce_external_utc(value, source="signal validation generation request")
        assert normalized is not None
        return normalized
