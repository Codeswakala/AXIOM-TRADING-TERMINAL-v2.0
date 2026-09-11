"""Plugin contract safety checker and refusal audit seam (W7-U05)."""

from __future__ import annotations

from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.institutional_platform.plugins.contracts import (
    ALLOWED_IMPORT_PREFIXES,
    PLUGIN_CAPABILITY_ALLOWLIST,
    PLUGIN_CONTRACT_VERSION,
    PluginContractDecision,
    PluginContractRequest,
)
from app.institutional_platform.plugins.registry import get_contract, list_contracts
from app.repositories.audit_repository import AuditRepository


class PluginContractSafetyService:
    """Checks published contract requests without running plugin code."""

    method_version = PLUGIN_CONTRACT_VERSION

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._audit = AuditRepository(session)

    def published_contracts(self) -> list[dict[str, object]]:
        return [contract.to_public_dict() for contract in list_contracts()]

    def capability_allowlist(self) -> tuple[str, ...]:
        return tuple(PLUGIN_CAPABILITY_ALLOWLIST)

    async def assess_request(
        self, *, request: PluginContractRequest, operator_id: str
    ) -> PluginContractDecision:
        reason = self._refusal_reason(request)
        if reason is not None:
            return await self._refuse(request=request, operator_id=operator_id, reason_code=reason)
        return PluginContractDecision(
            accepted=True,
            reason_code="PLUGIN_CONTRACT_ACCEPTED",
            contract_id=request.requested_contract_id,
            capability=request.requested_capability,
        )

    def _refusal_reason(self, request: PluginContractRequest) -> str | None:
        contract = get_contract(request.requested_contract_id)
        if contract is None:
            return "PLUGIN_CONTRACT_UNKNOWN_REFUSED"
        if request.requested_capability not in PLUGIN_CAPABILITY_ALLOWLIST:
            return "PLUGIN_CONTRACT_CAPABILITY_REFUSED"
        if request.requested_capability != contract.capability:
            return "PLUGIN_CONTRACT_CAPABILITY_MISMATCH_REFUSED"
        if any(not self._import_allowed(item) for item in request.requested_imports):
            return "PLUGIN_CONTRACT_IMPORT_REFUSED"
        if request.requested_data_scope != "current_operator":
            return "PLUGIN_CONTRACT_SCOPE_REFUSED"
        if request.writes_governed_artifact:
            return "PLUGIN_CONTRACT_WRITE_REFUSED"
        if request.reads_sensitive_material:
            return "PLUGIN_CONTRACT_SENSITIVE_READ_REFUSED"
        if request.network_access:
            return "PLUGIN_CONTRACT_NETWORK_REFUSED"
        return None

    def _import_allowed(self, import_path: str) -> bool:
        return any(import_path.startswith(prefix) for prefix in ALLOWED_IMPORT_PREFIXES)

    async def _refuse(
        self, *, request: PluginContractRequest, operator_id: str, reason_code: str
    ) -> PluginContractDecision:
        correlation_id = str(uuid4())
        event = await self._audit.append(
            category="SECURITY",
            action="plugin_contract_request.refused",
            actor=operator_id,
            resource_type="plugin_contract_request",
            resource_id=request.requested_contract_id,
            message=f"Plugin contract request refused reason={reason_code}",
            details={
                "reason_code": reason_code,
                "requested_contract_id": request.requested_contract_id,
                "requested_capability": request.requested_capability,
                "requested_data_scope": request.requested_data_scope,
                "method_version": self.method_version,
                "accepted": False,
            },
            correlation_id=correlation_id,
        )
        if event is None:
            raise RuntimeError("PLUGIN_CONTRACT_REFUSAL_AUDIT_FAILED")
        return PluginContractDecision(
            accepted=False,
            reason_code=reason_code,
            contract_id=request.requested_contract_id,
            capability=request.requested_capability,
            audit_correlation_id=correlation_id,
        )
