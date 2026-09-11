"""Provider adapter contracts for market-agnostic ML data access (W2-U02)."""

from __future__ import annotations

from typing import Protocol, Sequence

from app.ml.dataset.chronology_guard import SourceAuthority
from app.ml.dataset.market_data_query import (
    CanonicalMarketClass,
    MarketSeriesKey,
    MarketSeriesMetadataRead,
)


class MarketDataProviderAdapter(Protocol):
    """Provider adapter contract.

    Provider-native vocabulary must be mapped to canonical DTOs inside the
    adapter before ML Research sees it.
    """

    provider_name: str
    market_class: CanonicalMarketClass

    def list_supported_series(self) -> Sequence[MarketSeriesMetadataRead]:
        """Return canonical series metadata without network I/O."""


class InternalProviderAdapter:
    """Adapter for existing internal/sample/simulated candle sources."""

    provider_name = "internal"
    market_class = CanonicalMarketClass.FOREX

    def list_supported_series(self) -> Sequence[MarketSeriesMetadataRead]:
        return []


class DerivSyntheticIndicesAdapter:
    """Design skeleton for Deriv Synthetic Indices as a Synthetic provider.

    This adapter performs no live connection, stores no credentials, and makes
    no network calls. Its sole purpose in W2-U02 is to prove provider placement
    under the canonical Synthetic market class.
    """

    provider_name = "deriv"
    market_class = CanonicalMarketClass.SYNTHETIC

    def list_supported_series(self) -> Sequence[MarketSeriesMetadataRead]:
        return [
            MarketSeriesMetadataRead(
                series_key=MarketSeriesKey(
                    market_class=self.market_class.value,
                    provider=self.provider_name,
                    symbol="DERIV_SYNTHETIC_INDEX_PLACEHOLDER",
                    timeframe="M1",
                ),
                session_calendar="provider-defined-continuous-synthetic",
                tick_size=None,
                price_precision=None,
                timezone_assumption="UTC",
                source_authority=SourceAuthority.SYNTHETIC,
                known_limitations=(
                    "Design skeleton only; no live Deriv connection or credentials in W2-U02"
                ),
            )
        ]
