"""Code-defined built-in plugin contract registry (W7-U05)."""

from __future__ import annotations

from app.institutional_platform.plugins.contracts import (
    PLUGIN_CONTRACT_VERSION,
    PublishedPluginContract,
)

PUBLISHED_PLUGIN_CONTRACTS: tuple[PublishedPluginContract, ...] = (
    PublishedPluginContract(
        contract_id="builtin.report_export.markdown.v1",
        name="Markdown report export descriptor",
        kind="report_exporter",
        capability="report.export",
        version=PLUGIN_CONTRACT_VERSION,
        description="Read-only descriptor for formatting governed research reports as markdown.",
    ),
    PublishedPluginContract(
        contract_id="builtin.chart_type.research_overlay.v1",
        name="Research overlay chart descriptor",
        kind="chart_type",
        capability="chart.type",
        version=PLUGIN_CONTRACT_VERSION,
        description="Read-only descriptor for chart presentation overlays over governed artifacts.",
    ),
    PublishedPluginContract(
        contract_id="builtin.analytics_view.summary_cards.v1",
        name="Analytics summary cards descriptor",
        kind="analytics_view",
        capability="analytics.view",
        version=PLUGIN_CONTRACT_VERSION,
        description="Read-only descriptor for institutional analytics summary views.",
    ),
)


def list_contracts() -> tuple[PublishedPluginContract, ...]:
    return PUBLISHED_PLUGIN_CONTRACTS


def get_contract(contract_id: str) -> PublishedPluginContract | None:
    return next(
        (
            contract
            for contract in PUBLISHED_PLUGIN_CONTRACTS
            if contract.contract_id == contract_id
        ),
        None,
    )
