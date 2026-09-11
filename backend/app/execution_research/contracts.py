"""Simulation-only execution research contracts (W6-U01)."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

SIMULATION_MODE = "SIMULATED"
RESEARCH_STATUS = "research_only"
EXECUTION_RESEARCH_POLICY_VERSION = "w6-u01.gate_closed_simulation_envelope.v1"

SIMULATED_EXECUTION_RESEARCH_DISCLAIMER = (
    "SIMULATED execution research only. Not a live order, not financial advice, "
    "not real P&L. AXIOM does not act. Governance Gate CLOSED."
)


class ExecutionResearchSafetyContract(BaseModel):
    """Minimal safety contract reserved for future simulated artifacts."""

    simulation_mode: str = Field(default=SIMULATION_MODE)
    research_status: str = Field(default=RESEARCH_STATUS)
    policy_version: str = Field(default=EXECUTION_RESEARCH_POLICY_VERSION)
    disclaimer: str = Field(default=SIMULATED_EXECUTION_RESEARCH_DISCLAIMER)

    model_config = ConfigDict(extra="forbid", frozen=True)

    def assert_simulation_only(self) -> None:
        if self.simulation_mode != SIMULATION_MODE:
            raise ValueError("EXECUTION_RESEARCH_SIMULATION_MODE_REQUIRED")
        if self.research_status != RESEARCH_STATUS:
            raise ValueError("EXECUTION_RESEARCH_RESEARCH_STATUS_REQUIRED")
        if "Governance Gate CLOSED" not in self.disclaimer:
            raise ValueError("EXECUTION_RESEARCH_GATE_CLOSED_DISCLAIMER_REQUIRED")
