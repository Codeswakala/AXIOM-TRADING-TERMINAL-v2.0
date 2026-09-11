"""W7-U05 plugin contract safety foundation tests."""

from __future__ import annotations

from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import select

from app.db.base import Base
from app.db.models.audit import AuditEvent
from app.db.session import session_scope
from app.institutional_platform import (
    PLUGIN_CAPABILITY_ALLOWLIST,
    PUBLISHED_PLUGIN_CONTRACTS,
    PluginContractRequest,
    PluginContractSafetyService,
)


def _plugin_root() -> Path:
    return Path(__file__).resolve().parents[1] / "app" / "institutional_platform" / "plugins"


def test_plugin_contract_layer_has_no_dynamic_or_thirdparty_code_execution() -> None:
    forbidden_patterns = (
        "eval",
        "exec(",
        "importlib",
        "__import__",
        "load_entry_point",
        "pkg_resources",
        "subprocess",
        "compile(",
    )
    offenders: list[str] = []
    for path in _plugin_root().rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for pattern in forbidden_patterns:
            if pattern in text:
                offenders.append(f"{path.relative_to(_plugin_root())}:{pattern}")
    assert offenders == []


def test_plugin_contract_disallows_broker_order_account_gate_imports() -> None:
    forbidden_patterns = (
        "place_order",
        "broker.connect",
        "broker.execute",
        "order_routing",
        "account_balance",
        "open_gate",
        "gate_open",
        "allow_execution",
        "socket",
        "requests.",
        "httpx.",
    )
    offenders: list[str] = []
    for path in _plugin_root().rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for pattern in forbidden_patterns:
            if pattern in text:
                offenders.append(f"{path.relative_to(_plugin_root())}:{pattern}")
    assert offenders == []


@pytest.mark.asyncio
async def test_hostile_plugin_request_refused_and_audited(prepared_db: None) -> None:
    async with session_scope() as session:
        service = PluginContractSafetyService(session)
        decision = await service.assess_request(
            operator_id="pytest-operator",
            request=PluginContractRequest(
                requested_contract_id="builtin.report_export.markdown.v1",
                requested_capability="report.export",
                requested_imports=("app.external_integration.broker",),
                requested_data_scope="all_operators",
                writes_governed_artifact=True,
                reads_sensitive_material=True,
                network_access=True,
            ),
        )
        assert decision.accepted is False
        assert decision.reason_code.endswith("REFUSED")
        audit = (
            await session.scalars(
                select(AuditEvent).where(
                    AuditEvent.resource_type == "plugin_contract_request",
                    AuditEvent.action == "plugin_contract_request.refused",
                    AuditEvent.correlation_id == decision.audit_correlation_id,
                )
            )
        ).one()
        assert audit.details is not None
        assert audit.details["reason_code"] == decision.reason_code
        assert audit.details["accepted"] is False


def test_plugin_capabilities_are_allowlisted_read_research_only() -> None:
    assert set(PLUGIN_CAPABILITY_ALLOWLIST) == {"report.export", "chart.type", "analytics.view"}
    forbidden_markers = (
        "execute",
        "order",
        "broker",
        "account",
        "gate",
        "position",
        "capital",
        "margin",
    )
    for capability in PLUGIN_CAPABILITY_ALLOWLIST:
        assert not any(marker in capability for marker in forbidden_markers)
    for contract in PUBLISHED_PLUGIN_CONTRACTS:
        assert contract.capability in PLUGIN_CAPABILITY_ALLOWLIST
        assert contract.read_only is True
        assert contract.built_in is True


def test_no_plugin_execution_audit_events_table() -> None:
    assert "plugin_execution_audit_events" not in Base.metadata.tables


@pytest.mark.asyncio
async def test_plugin_contract_surface_requires_auth(async_client: AsyncClient) -> None:
    unauth = await async_client.get("/api/v1/institutional-platform/plugin-contracts")
    assert unauth.status_code == 401
    login = await async_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert login.status_code == 200, login.text
    headers = {"Authorization": f"Bearer {login.json()['tokens']['access_token']}"}
    response = await async_client.get(
        "/api/v1/institutional-platform/plugin-contracts", headers=headers
    )
    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["contract_version"]
    assert payload["capability_allowlist"] == ["report.export", "chart.type", "analytics.view"]
    assert payload["dynamic_code_execution_enabled"] is False
    assert payload["third_party_plugin_execution_enabled"] is False
    assert payload["plugin_execution_audit_table_present"] is False
    assert payload["governance_gate_capability_present"] is False
    assert len(payload["contracts"]) >= 1


@pytest.mark.asyncio
async def test_plugin_contract_has_no_secret_or_pii_markers(async_client: AsyncClient) -> None:
    login = await async_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert login.status_code == 200, login.text
    headers = {"Authorization": f"Bearer {login.json()['tokens']['access_token']}"}
    response = await async_client.get(
        "/api/v1/institutional-platform/plugin-contracts", headers=headers
    )
    assert response.status_code == 200, response.text
    text = response.text.lower()
    forbidden = (
        "access_token",
        "refresh_token",
        "jwt",
        "password",
        "secret",
        "api_key",
        "private_key",
        "hashed_password",
    )
    assert not any(marker in text for marker in forbidden)


def test_gate_remains_closed_for_wave7() -> None:
    from app.external_integration.broker import governance_gate

    assert governance_gate.broker_integration_authorized is False
    assert governance_gate.execution_authorized is False
