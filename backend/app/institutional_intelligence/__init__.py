"""Institutional Intelligence bounded context (Wave 4)."""

from app.institutional_intelligence.contracts import (
    FORBIDDEN_ACTION_KEYS,
    IntelligenceArtifactContract,
    IntelligenceArtifactDraft,
    IntelligenceArtifactFactory,
)
from app.institutional_intelligence.correlation import (
    CorrelationComputationResult,
    CorrelationReportService,
    CorrelationSeriesSpec,
)
from app.institutional_intelligence.portfolio_risk import (
    PortfolioRiskAssumptions,
    PortfolioRiskComputationResult,
    PortfolioRiskReportService,
    PortfolioRiskSeriesSpec,
)
from app.institutional_intelligence.regime import (
    RegimeComputationResult,
    RegimeFeatureVector,
    RegimeReportService,
    RegimeSeriesSpec,
)
from app.institutional_intelligence.scenario import (
    ScenarioAssumptions,
    ScenarioComputationResult,
    ScenarioReportService,
    ScenarioSeriesSpec,
)
from app.institutional_intelligence.scientific_dependencies import (
    APPROVED_COMPILED_DEPENDENCIES,
    SCIENTIFIC_DEPENDENCY_POLICY,
    WAVE4_CANDIDATE_DEPENDENCIES,
    ScientificDependencyCandidate,
)
from app.institutional_intelligence.signal_validation import (
    SignalValidationComputationResult,
    SignalValidationReportService,
    SignalValidationScope,
)

__all__ = [
    "APPROVED_COMPILED_DEPENDENCIES",
    "CorrelationComputationResult",
    "CorrelationReportService",
    "CorrelationSeriesSpec",
    "FORBIDDEN_ACTION_KEYS",
    "IntelligenceArtifactContract",
    "IntelligenceArtifactDraft",
    "IntelligenceArtifactFactory",
    "PortfolioRiskAssumptions",
    "PortfolioRiskComputationResult",
    "PortfolioRiskReportService",
    "PortfolioRiskSeriesSpec",
    "RegimeComputationResult",
    "RegimeFeatureVector",
    "RegimeReportService",
    "RegimeSeriesSpec",
    "SignalValidationComputationResult",
    "SignalValidationReportService",
    "SignalValidationScope",
    "ScenarioAssumptions",
    "ScenarioComputationResult",
    "ScenarioReportService",
    "ScenarioSeriesSpec",
    "SCIENTIFIC_DEPENDENCY_POLICY",
    "ScientificDependencyCandidate",
    "WAVE4_CANDIDATE_DEPENDENCIES",
]
