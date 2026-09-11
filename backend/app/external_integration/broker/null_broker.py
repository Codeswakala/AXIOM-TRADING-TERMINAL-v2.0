"""Disabled reference broker adapter (W1-U03).

`NullBroker` proves the broker seam is real and independently testable while
performing zero I/O, zero network calls, and zero execution.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.external_integration.broker.errors import BrokerDisabledError
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
from app.repositories.audit_repository import AuditRepository

GATE_CLOSED_CONNECT_REFUSED = "GATE_CLOSED_CONNECT_REFUSED"
GATE_CLOSED_EXECUTE_REFUSED = "GATE_CLOSED_EXECUTE_REFUSED"
BROKER_REFUSAL_RESOURCE_TYPE = "broker_integration"


class NullBroker:
    """Disabled adapter wired for current platform state."""

    name = "null-broker"

    def __init__(
        self,
        gate: ConstitutionalGovernanceGate | None = None,
        audit_session: AsyncSession | None = None,
    ) -> None:
        self._gate = gate or governance_gate
        self._audit_session = audit_session

    async def connect(self) -> None:
        await self._append_refusal_audit(
            action="broker.connect.refused",
            reason_code=GATE_CLOSED_CONNECT_REFUSED,
            resource_id=self.name,
            live_broker_connection_attempted=False,
            live_order_attempted=False,
        )
        self._gate.refuse_broker_connection(adapter_name=self.name)

    async def disconnect(self) -> None:
        return None

    def is_connected(self) -> bool:
        return False

    def describe_capabilities(self) -> BrokerCapabilities:
        return BrokerCapabilities(adapter_name=self.name)

    async def get_instruments(self) -> list[Instrument]:
        raise BrokerDisabledError("Broker instrument discovery disabled in W1-U03")

    async def get_account_info(self) -> BrokerAccount:
        raise BrokerDisabledError("Broker account info disabled in W1-U03")

    async def get_quote(self, symbol: str) -> BrokerQuote:
        _ = symbol
        raise BrokerDisabledError("Broker quotes disabled in W1-U03")

    async def place_order(self, intent: OrderIntent) -> str:
        await self._append_refusal_audit(
            action="broker.execute.refused",
            reason_code=GATE_CLOSED_EXECUTE_REFUSED,
            resource_id=intent.id,
            live_broker_connection_attempted=False,
            live_order_attempted=False,
        )
        self._gate.refuse_execution(action="broker.place_order", resource_id=intent.id)

    async def cancel_order(self, order_id: str) -> None:
        await self._append_refusal_audit(
            action="broker.execute.refused",
            reason_code=GATE_CLOSED_EXECUTE_REFUSED,
            resource_id=order_id,
            live_broker_connection_attempted=False,
            live_order_attempted=False,
        )
        self._gate.refuse_execution(action="broker.cancel_order", resource_id=order_id)

    async def _append_refusal_audit(
        self,
        *,
        action: str,
        reason_code: str,
        resource_id: str,
        live_broker_connection_attempted: bool,
        live_order_attempted: bool,
    ) -> None:
        if self._audit_session is None:
            return
        event = await AuditRepository(self._audit_session).append(
            category="GOVERNANCE",
            action=action,
            actor="system",
            resource_type=BROKER_REFUSAL_RESOURCE_TYPE,
            resource_id=resource_id,
            message=f"Governance Gate CLOSED broker refusal reason={reason_code}",
            details={
                "reason_code": reason_code,
                "gate_state": "CLOSED",
                "simulation_only": True,
                "adapter_name": self.name,
                "live_broker_connection_attempted": live_broker_connection_attempted,
                "live_order_attempted": live_order_attempted,
            },
        )
        if event is None:
            raise RuntimeError("BROKER_REFUSAL_AUDIT_FAILED")
