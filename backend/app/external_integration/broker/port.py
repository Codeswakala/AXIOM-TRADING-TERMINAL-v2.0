"""Broker adapter port contract (W1-U03)."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from app.external_integration.broker.models import (
    BrokerAccount,
    BrokerCapabilities,
    BrokerQuote,
    Instrument,
    OrderIntent,
)


@runtime_checkable
class BrokerPort(Protocol):
    """Pure broker-neutral port implemented by all future broker adapters."""

    @property
    def name(self) -> str:
        """Adapter name."""

    async def connect(self) -> None:
        """Connect lifecycle hook. Disabled adapters must refuse."""

    async def disconnect(self) -> None:
        """Disconnect lifecycle hook."""

    def is_connected(self) -> bool:
        """Return whether a real broker connection is active."""

    def describe_capabilities(self) -> BrokerCapabilities:
        """Describe neutral adapter capabilities."""

    async def get_instruments(self) -> list[Instrument]:
        """Return future instrument metadata."""

    async def get_account_info(self) -> BrokerAccount:
        """Return future account descriptor."""

    async def get_quote(self, symbol: str) -> BrokerQuote:
        """Return future quote/tick data."""

    async def place_order(self, intent: OrderIntent) -> str:
        """Future execution-shaped surface; must be gate-refused now."""

    async def cancel_order(self, order_id: str) -> None:
        """Future cancellation-shaped surface; must be gate-refused now."""
