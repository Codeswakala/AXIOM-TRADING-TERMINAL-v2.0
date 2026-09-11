"""Simulated execution research API schemas (W6-U02)."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.time import coerce_external_utc


class SimulatedExecutionRunCreate(BaseModel):
    market_class: str = Field(min_length=1, max_length=64)
    symbol: str = Field(min_length=1, max_length=128)
    timeframe: str = Field(min_length=1, max_length=32)
    as_of_start: datetime
    as_of_end: datetime
    simulated_research_direction: Literal[
        "long_bias", "short_bias", "neutral_research"
    ] = "long_bias"
    simulated_units: float = Field(default=1.0, gt=0)
    simulated_slippage_bps: float = 0.0
    max_fill_events: int = Field(default=5, ge=1, le=200)
    input_artifact_ids: list[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")

    @field_validator("as_of_start", "as_of_end")
    @classmethod
    def _datetimes_utc(cls, value: datetime) -> datetime:
        normalized = coerce_external_utc(value, source="simulated execution create")
        assert normalized is not None
        return normalized


class SimulatedFillEventRead(BaseModel):
    simulated_fill_id: str
    run_id: str
    created_at: datetime
    simulation_mode: str
    market_class: str
    symbol: str
    timeframe: str
    as_of_time: datetime
    simulated_research_direction: str
    simulated_units: float
    requested_reference_price: float
    simulated_fill_price: float
    simulated_slippage_bps: float
    source_candle_ids: list[Any]
    fill_model_name: str
    fill_model_version: str
    research_status: str
    simulation_disclaimer: str
    audit_correlation_id: str

    @field_validator("created_at", "as_of_time")
    @classmethod
    def _fill_datetimes_utc(cls, value: datetime) -> datetime:
        normalized = coerce_external_utc(value, source="simulated fill read")
        assert normalized is not None
        return normalized

    model_config = ConfigDict(from_attributes=True)


class SimulatedExecutionRunRead(BaseModel):
    run_id: str
    created_at: datetime
    operator_id: str
    simulation_mode: str
    simulation_policy_version: str
    input_artifact_ids: list[Any]
    replay_scope: dict[str, Any]
    fill_model_name: str
    fill_model_version: str
    assumptions: dict[str, Any]
    limitations: list[Any]
    research_status: str
    simulation_disclaimer: str
    audit_correlation_id: str

    @field_validator("created_at")
    @classmethod
    def _run_created_at_utc(cls, value: datetime) -> datetime:
        normalized = coerce_external_utc(value, source="simulated execution run read")
        assert normalized is not None
        return normalized

    model_config = ConfigDict(from_attributes=True)


class SimulatedExecutionRunWithFillsRead(BaseModel):
    run: SimulatedExecutionRunRead
    fills: list[SimulatedFillEventRead]
