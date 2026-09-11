"""ML dataset architecture and market-agnostic access layer."""

from app.ml.dataset.chronology_guard import (
    ChronologyGuard,
    GuardRecord,
    GuardStage,
    QuarantineEvent,
    QuarantineReason,
    SourceAuthority,
)
from app.ml.dataset.market_data_query import (
    CANONICAL_MARKET_CLASSES,
    CandleMarketDataQueryAdapter,
    CanonicalMarketClass,
    CanonicalOHLCVRecord,
    MarketDataQueryPort,
    MarketSeriesKey,
    MarketSeriesMetadataRead,
    SourceMetadata,
)
from app.ml.dataset.metadata_service import MarketMetadataService
from app.ml.dataset.provider_adapters import (
    DerivSyntheticIndicesAdapter,
    InternalProviderAdapter,
    MarketDataProviderAdapter,
)
from app.ml.dataset.service import DatasetService, DatasetSnapshotInput
from app.ml.dataset.snapshot_builder import ReproducibleSnapshotBuilder, SnapshotBuildResult
from app.ml.dataset.split_engine import SplitRows, TemporalSplitConfig, TemporalSplitEngine

__all__ = [
    "CANONICAL_MARKET_CLASSES",
    "CandleMarketDataQueryAdapter",
    "CanonicalMarketClass",
    "CanonicalOHLCVRecord",
    "ChronologyGuard",
    "DatasetService",
    "DatasetSnapshotInput",
    "DerivSyntheticIndicesAdapter",
    "GuardRecord",
    "GuardStage",
    "InternalProviderAdapter",
    "MarketDataProviderAdapter",
    "MarketDataQueryPort",
    "MarketMetadataService",
    "MarketSeriesKey",
    "MarketSeriesMetadataRead",
    "QuarantineEvent",
    "QuarantineReason",
    "ReproducibleSnapshotBuilder",
    "SourceAuthority",
    "SourceMetadata",
    "SnapshotBuildResult",
    "SplitRows",
    "TemporalSplitConfig",
    "TemporalSplitEngine",
]
