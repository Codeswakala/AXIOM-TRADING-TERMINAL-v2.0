"""Published extension contracts for W7-U05 plugin safety foundation."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

PluginCapability = Literal["report.export", "chart.type", "analytics.view"]
PluginContractKind = Literal["report_exporter", "chart_type", "analytics_view"]

PLUGIN_CONTRACT_VERSION = "w7-u05.plugin_contracts.v1"
PLUGIN_CAPABILITY_ALLOWLIST: tuple[PluginCapability, ...] = (
    "report.export",
    "chart.type",
    "analytics.view",
)
ALLOWED_IMPORT_PREFIXES: tuple[str, ...] = (
    "app.models.",
    "app.institutional_platform.plugins.",
)


@dataclass(frozen=True, slots=True)
class PublishedPluginContract:
    """Static descriptor for a built-in reference extension contract."""

    contract_id: str
    name: str
    kind: PluginContractKind
    capability: PluginCapability
    version: str
    description: str
    read_only: bool = True
    built_in: bool = True

    def to_public_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class PluginContractRequest:
    """Contract request metadata checked by the refusal seam."""

    requested_contract_id: str
    requested_capability: str
    requested_imports: tuple[str, ...] = ()
    requested_data_scope: str = "current_operator"
    writes_governed_artifact: bool = False
    reads_sensitive_material: bool = False
    network_access: bool = False


@dataclass(frozen=True, slots=True)
class PluginContractDecision:
    """Decision returned by the contract safety checker."""

    accepted: bool
    reason_code: str
    contract_id: str
    capability: str
    audit_correlation_id: str | None = None

    def to_public_dict(self) -> dict[str, object]:
        return asdict(self)
