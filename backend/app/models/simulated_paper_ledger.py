"""Simulated paper research ledger API schemas (W6-U03)."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.time import coerce_external_utc


class SimulatedPaperLedgerEntryCreate(BaseModel):
    run_id: str = Field(min_length=1)
    simulated_fill_id: str = Field(min_length=1)
    simulated_exit_value: float = Field(gt=0)
    ledger_event_type: Literal["simulated_close_estimate", "simulated_review_mark"] = (
        "simulated_close_estimate"
    )
    uncertainty_width: float = Field(default=0.0001, ge=0)

    model_config = ConfigDict(extra="forbid")


class SimulatedPaperLedgerEntryRead(BaseModel):
    ledger_entry_id: str
    created_at: datetime
    simulation_mode: str
    run_id: str
    simulated_fill_id: str
    operator_id: str
    ledger_event_type: str
    simulated_research_direction: str
    simulated_units: float
    simulated_entry_value: float
    simulated_exit_value: float
    simulated_return_estimate: float
    uncertainty: dict[str, Any]
    limitations: list[Any]
    research_status: str
    simulation_disclaimer: str
    audit_correlation_id: str

    @field_validator("created_at")
    @classmethod
    def _created_at_utc(cls, value: datetime) -> datetime:
        normalized = coerce_external_utc(value, source="simulated ledger read")
        assert normalized is not None
        return normalized

    model_config = ConfigDict(from_attributes=True)
