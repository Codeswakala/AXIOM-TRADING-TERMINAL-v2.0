"""ORM models package — import side effects register metadata for Alembic."""

from app.db.models.advisory_signal import AdvisorySignal
from app.db.models.assistant_research_response import AssistantResearchResponse
from app.db.models.audit import AuditEvent, AuditWriteFailureRecord
from app.db.models.calibration_report import CalibrationReport
from app.db.models.candle import Candle
from app.db.models.chart_research_annotation import ChartResearchAnnotation
from app.db.models.correlation_report import CorrelationReport
from app.db.models.dataset import (
    DatasetLineageRecord,
    DatasetQuarantineRecord,
    DatasetSeriesMember,
    DatasetSnapshot,
)
from app.db.models.dataset_split import DatasetSplitManifest
from app.db.models.economic_report import EconomicReport
from app.db.models.execution_experiment import ExecutionResearchExperiment
from app.db.models.execution_risk_report import ExecutionRiskResearchReport
from app.db.models.experiment import Experiment
from app.db.models.feature import FeatureRecord
from app.db.models.feature_definition import FeatureDefinition, FeatureQualityReport
from app.db.models.generalization import DriftMonitoringRecord, GeneralizationReport
from app.db.models.ingestion_run import IngestionRun
from app.db.models.manual_trade_journal_entry import ManualTradeJournalEntryRecord
from app.db.models.market_metadata import MarketSeriesMetadata
from app.db.models.model_artifact import ModelArtifact
from app.db.models.monitoring_alert import MonitoringAlert
from app.db.models.operator import Operator
from app.db.models.operator_workspace_preference import OperatorWorkspacePreference
from app.db.models.portfolio_risk_report import PortfolioRiskReport
from app.db.models.refresh_token import RefreshTokenRecord
from app.db.models.regime_report import RegimeReport
from app.db.models.research_management import (
    ResearchCollection,
    ResearchCollectionMember,
    ResearchTag,
)
from app.db.models.scenario_report import ScenarioReport
from app.db.models.signal_validation_report import SignalValidationReport
from app.db.models.simulated_execution import SimulatedExecutionRun, SimulatedFillEvent
from app.db.models.simulated_execution_analytics_report import SimulatedExecutionAnalyticsReport
from app.db.models.simulated_paper_ledger import SimulatedPaperLedgerEntry
from app.db.models.trade_plan_note import TradePlanNoteRecord

# V2 models — must be imported so Alembic target_metadata includes them
from app.db.models.v2_audit_event import V2AuditEvent
from app.db.models.v2_broker_read import (
    V2BrokerAccount,
    V2BrokerBalance,
    V2BrokerDiscrepancy,
    V2BrokerFill,
    V2BrokerInstrumentPermission,
    V2BrokerOrder,
    V2BrokerPosition,
    V2BrokerReconcileRun,
    V2BrokerSyncRun,
)
from app.db.models.v2_capability_record import V2CapabilityRecord
from app.db.models.v2_lineage_record import V2LineageRecord
from app.db.models.v2_live_activation import (  # BE-12D (BO-V2-BE12D-001)
    V2LiveActivationInstrument,
)
from app.db.models.v2_live_exec import V2LiveExecIntent  # BE-12A (BO-V2-BE12A-001)
from app.db.models.v2_live_killswitch import (  # BE-12D (BO-V2-BE12D-001)
    V2LiveKillSwitch,
)
from app.db.models.v2_live_exec_incident import (  # BE-12E (BO-V2-BE12E-001)
    V2LiveExecIncident,
)
from app.db.models.v2_live_exec_modify import (  # BE-12C (BO-V2-BE12C-001)
    V2LiveExecModifyEvent,
)
from app.db.models.v2_live_exec_reconciliation import (  # BE-12E (BO-V2-BE12E-001)
    V2LiveExecReconciliation,
)
from app.db.models.v2_live_exec_submission import (  # BE-12B (BO-V2-BE12B-001)
    V2LiveExecFillEvent,
    V2LiveExecSubmission,
)
from app.db.models.v2_marketdata import (
    V2MdAsOfVerification,
    V2MdInstrument,
    V2MdIntegrityException,
    V2MdSeries,
    V2MdSource,
    V2MdSymbolMap,
)
from app.db.models.v2_paper_bridge import V2PaperBridgeDriftRun
from app.db.models.v2_paper_trading import (
    V2PaperAccount,
    V2PaperBalanceSnapshot,
    V2PaperFill,
    V2PaperOrderEvent,
    V2PaperOrderIntent,
    V2PaperPositionSnapshot,
    V2PaperReconciliation,
    V2PaperRiskDecision,
)
from app.db.models.v2_permission import V2Permission
from app.db.models.v2_portfolio import (
    V2PortfolioDefinition,
    V2PortfolioRiskReport,
)
from app.db.models.v2_provider import V2MdProvider, V2MdProviderStatusHistory
from app.db.models.v2_research import (
    V2ChartIntelligenceReport,
    V2ComputationVersion,
    V2MarketContextReport,
)
from app.db.models.v2_research_governance import (
    V2MlDiagnosticReport,
    V2MlGovernanceRecord,
    V2MlLifecycleEvent,
)
from app.db.models.v2_research_jobs import (
    V2BacktestInput,
    V2CostModel,
    V2ResearchJob,
    V2ResearchJobAttempt,
    V2ResearchResult,
    V2StrategyVersion,
)
from app.db.models.v2_signal import V2SignalRecord, V2SignalStateEvent
from app.db.models.validation_report import ValidationReport
from app.db.models.ws_ticket import WsTicket

__all__ = [
    "AdvisorySignal",
    "AssistantResearchResponse",
    "AuditEvent",
    "AuditWriteFailureRecord",
    "CalibrationReport",
    "Candle",
    "ChartResearchAnnotation",
    "CorrelationReport",
    "DatasetLineageRecord",
    "DatasetQuarantineRecord",
    "DatasetSeriesMember",
    "DatasetSnapshot",
    "DatasetSplitManifest",
    "EconomicReport",
    "ExecutionResearchExperiment",
    "ExecutionRiskResearchReport",
    "Experiment",
    "FeatureDefinition",
    "FeatureQualityReport",
    "FeatureRecord",
    "GeneralizationReport",
    "DriftMonitoringRecord",
    "IngestionRun",
    "ManualTradeJournalEntryRecord",
    "MarketSeriesMetadata",
    "ModelArtifact",
    "MonitoringAlert",
    "Operator",
    "OperatorWorkspacePreference",
    "PortfolioRiskReport",
    "RefreshTokenRecord",
    "RegimeReport",
    "ResearchCollection",
    "ResearchCollectionMember",
    "ResearchTag",
    "ScenarioReport",
    "SignalValidationReport",
    "SimulatedExecutionRun",
    "SimulatedFillEvent",
    "SimulatedExecutionAnalyticsReport",
    "SimulatedPaperLedgerEntry",
    "TradePlanNoteRecord",
    "ValidationReport",
    "WsTicket",
    # V2
    "V2AuditEvent",
    "V2LineageRecord",
    "V2CapabilityRecord",
    "V2Permission",
    "V2MdAsOfVerification",
    "V2MdInstrument",
    "V2MdIntegrityException",
    "V2MdSeries",
    "V2MdSource",
    "V2MdSymbolMap",
    "V2MdProvider",
    "V2MdProviderStatusHistory",
    "V2ComputationVersion",
    "V2MarketContextReport",
    "V2ChartIntelligenceReport",
    "V2MlGovernanceRecord",
    "V2MlLifecycleEvent",
    "V2MlDiagnosticReport",
    "V2SignalRecord",
    "V2SignalStateEvent",
    "V2PortfolioDefinition",
    "V2PortfolioRiskReport",
    "V2BacktestInput",
    "V2CostModel",
    "V2StrategyVersion",
    "V2ResearchJob",
    "V2ResearchJobAttempt",
    "V2ResearchResult",
    "V2PaperAccount",
    "V2PaperOrderIntent",
    "V2PaperRiskDecision",
    "V2PaperOrderEvent",
    "V2PaperFill",
    "V2PaperPositionSnapshot",
    "V2PaperBalanceSnapshot",
    "V2PaperReconciliation",
    "V2BrokerAccount",
    "V2BrokerBalance",
    "V2BrokerPosition",
    "V2BrokerOrder",
    "V2BrokerFill",
    "V2BrokerInstrumentPermission",
    "V2BrokerSyncRun",
    "V2BrokerReconcileRun",
    "V2BrokerDiscrepancy",
    "V2LiveExecFillEvent",
    "V2LiveActivationInstrument",
    "V2LiveExecIntent",
    "V2LiveKillSwitch",
    "V2LiveExecIncident",
    "V2LiveExecModifyEvent",
    "V2LiveExecReconciliation",
    "V2LiveExecSubmission",
    "V2PaperBridgeDriftRun",
]
