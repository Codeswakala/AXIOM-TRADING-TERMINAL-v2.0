"""Broker integration framework boundary (W1-U03)."""

from app.external_integration.broker.errors import (
    BrokerDisabledError,
    BrokerIntegrationError,
    BrokerNotConnectedError,
    GovernanceGateClosedError,
)
from app.external_integration.broker.governance_gate import (
    ConstitutionalGovernanceGate,
    governance_gate,
)
from app.external_integration.broker.models import (
    BrokerAccount,
    BrokerCapabilities,
    BrokerQuote,
    Instrument,
    OrderIntent,
)
from app.external_integration.broker.null_broker import NullBroker
from app.external_integration.broker.port import BrokerPort
from app.external_integration.broker.service import BrokerIntegrationService

__all__ = [
    "BrokerAccount",
    "BrokerCapabilities",
    "BrokerDisabledError",
    "BrokerIntegrationError",
    "BrokerIntegrationService",
    "BrokerNotConnectedError",
    "BrokerPort",
    "BrokerQuote",
    "ConstitutionalGovernanceGate",
    "GovernanceGateClosedError",
    "Instrument",
    "NullBroker",
    "OrderIntent",
    "governance_gate",
]
