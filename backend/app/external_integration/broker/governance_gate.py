"""Constitutional Governance Gate for broker integration (W1-U03).

The gate is hard closed in this unit and cannot be opened by ordinary runtime
configuration. Future changes require roadmap/governance authorization.
"""

from __future__ import annotations

from app.core.logging import get_logger
from app.external_integration.broker.errors import GovernanceGateClosedError
from app.services.observability_service import get_observability_service

logger = get_logger(__name__, category="GOVERNANCE")


class ConstitutionalGovernanceGate:
    """Single chokepoint for broker connection/execution traversal."""

    _broker_integration_authorized: bool = False
    _execution_authorized: bool = False

    @property
    def broker_integration_authorized(self) -> bool:
        return self._broker_integration_authorized

    @property
    def execution_authorized(self) -> bool:
        return self._execution_authorized

    def refuse_broker_connection(self, *, adapter_name: str) -> None:
        self._refuse(
            action="broker.connect",
            message=(
                f"Constitutional Governance Gate CLOSED: broker connection refused "
                f"adapter={adapter_name}"
            ),
        )

    def refuse_execution(self, *, action: str, resource_id: str | None = None) -> None:
        detail = f" action={action}"
        if resource_id:
            detail += f" resource_id={resource_id}"
        self._refuse(
            action=action,
            message=(
                "Constitutional Governance Gate CLOSED: execution path refused" + detail
            ),
        )

    def _refuse(self, *, action: str, message: str) -> None:
        get_observability_service().record_governance_gate_refusal(action=action)
        logger.warning(message)
        raise GovernanceGateClosedError(message)


governance_gate = ConstitutionalGovernanceGate()
