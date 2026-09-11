"""Broker integration error hierarchy (W1-U03)."""

from __future__ import annotations


class BrokerIntegrationError(RuntimeError):
    """Base class for external broker integration errors."""


class BrokerDisabledError(BrokerIntegrationError):
    """Raised when broker framework is intentionally disabled in the current unit."""


class BrokerNotConnectedError(BrokerIntegrationError):
    """Raised when a read-shaped broker operation is requested while disconnected."""


class GovernanceGateClosedError(BrokerIntegrationError):
    """Raised when the Constitutional Governance Gate refuses broker traversal."""
