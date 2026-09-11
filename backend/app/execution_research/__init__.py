"""Execution Research bounded context (Wave 6 safety foundation).

Wave 6 is simulation/research only. This package intentionally contains no
broker client, no network egress, no secrets, and no live execution path.
"""

from app.execution_research.analytics import (
    SimulatedExecutionAnalyticsReportDraft,
    SimulatedExecutionAnalyticsReportService,
)
from app.execution_research.contracts import (
    EXECUTION_RESEARCH_POLICY_VERSION,
    RESEARCH_STATUS,
    SIMULATED_EXECUTION_RESEARCH_DISCLAIMER,
    SIMULATION_MODE,
    ExecutionResearchSafetyContract,
)
from app.execution_research.experiment import (
    ExecutionResearchExperimentDraft,
    ExecutionResearchExperimentService,
)
from app.execution_research.ledger import (
    SimulatedPaperLedgerEntryDraft,
    SimulatedPaperLedgerService,
)
from app.execution_research.risk import (
    ExecutionRiskResearchReportDraft,
    ExecutionRiskResearchReportService,
)
from app.execution_research.simulation import (
    FILL_MODEL_NAME,
    FILL_MODEL_VERSION,
    DeterministicSimulatedFillModel,
    SimulatedExecutionCreationResult,
    SimulatedExecutionRunSpec,
    SimulatedExecutionService,
    SimulatedFillPreview,
)

__all__ = [
    "EXECUTION_RESEARCH_POLICY_VERSION",
    "FILL_MODEL_NAME",
    "FILL_MODEL_VERSION",
    "RESEARCH_STATUS",
    "SIMULATED_EXECUTION_RESEARCH_DISCLAIMER",
    "SIMULATION_MODE",
    "DeterministicSimulatedFillModel",
    "ExecutionResearchExperimentDraft",
    "ExecutionResearchExperimentService",
    "ExecutionResearchSafetyContract",
    "ExecutionRiskResearchReportDraft",
    "ExecutionRiskResearchReportService",
    "SimulatedExecutionCreationResult",
    "SimulatedExecutionAnalyticsReportDraft",
    "SimulatedExecutionAnalyticsReportService",
    "SimulatedExecutionRunSpec",
    "SimulatedExecutionService",
    "SimulatedFillPreview",
    "SimulatedPaperLedgerEntryDraft",
    "SimulatedPaperLedgerService",
]
