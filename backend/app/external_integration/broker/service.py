"""Broker integration service wiring (W1-U03)."""

from __future__ import annotations

from app.external_integration.broker.null_broker import NullBroker
from app.external_integration.broker.port import BrokerPort


class BrokerIntegrationService:
    """Application-facing broker integration seam.

    The current adapter is intentionally disabled. Future broker adapters must
    implement BrokerPort and remain behind the governance gate.
    """

    def __init__(self, broker: BrokerPort | None = None) -> None:
        self._broker = broker or NullBroker()

    @property
    def broker(self) -> BrokerPort:
        return self._broker

    def status(self) -> dict[str, object]:
        capabilities = self._broker.describe_capabilities()
        return {
            "adapter": self._broker.name,
            "connected": self._broker.is_connected(),
            "capabilities": capabilities.model_dump(mode="json"),
        }


def get_broker_integration_service() -> BrokerIntegrationService:
    return BrokerIntegrationService()
