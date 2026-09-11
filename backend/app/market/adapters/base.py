"""Pluggable market data adapter interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator, Awaitable, Callable
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from app.ingestion.types import NormalizedCandleRow

# Callback invoked for each normalized live candle
CandleHandler = Callable[[NormalizedCandleRow], Awaitable[None]]


@dataclass(slots=True)
class AdapterStatus:
    name: str
    connected: bool
    market_class: str
    symbol: str
    timeframe: str
    last_message_at: datetime | None = None
    messages_received: int = 0
    reconnect_count: int = 0
    last_error: str | None = None
    lag_ms: float | None = None
    details: dict[str, Any] = field(default_factory=dict)


class MarketDataAdapter(ABC):
    """Abstract live market data source.

    Implementations push normalized candles via the registered handler.
    Historical CSV paths remain separate (W0-U03) but share NormalizedCandleRow.
    """

    name: str

    @abstractmethod
    async def start(self, on_candle: CandleHandler) -> None:
        """Connect and begin emitting candles until stop()."""

    @abstractmethod
    async def stop(self) -> None:
        """Disconnect and release resources."""

    @abstractmethod
    def status(self) -> AdapterStatus:
        """Current connection / health snapshot."""

    async def stream(self) -> AsyncIterator[NormalizedCandleRow]:
        """Optional pull-style interface; default unused."""
        if False:  # pragma: no cover
            yield None  # type: ignore[misc]
