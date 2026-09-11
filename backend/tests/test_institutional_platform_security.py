"""W7-U01 institutional platform security/API foundation tests."""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

import pytest
from httpx import AsyncClient

from app.auth.security import hash_password
from app.db.models.operator import Operator
from app.db.session import session_scope
from app.institutional_platform import (
    INSTITUTIONAL_ROLE_PERMISSIONS,
    assert_permission_vocabulary_safe,
)


async def _create_operator(*, role: str = "operator") -> tuple[str, str, str]:
    username = f"w7-{role}-{uuid4().hex[:10]}"
    password = "operator-pass-123"
    async with session_scope() as session:
        operator = Operator(
            username=username,
            hashed_password=hash_password(password),
            role=role,
            is_active=True,
            display_name=f"W7 {role} test operator",
        )
        session.add(operator)
        await session.flush()
        return operator.id, username, password


async def _headers(async_client: AsyncClient, username: str, password: str) -> dict[str, str]:
    login = await async_client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": password},
    )
    assert login.status_code == 200, login.text
    return {"Authorization": f"Bearer {login.json()['tokens']['access_token']}"}


def test_gate_remains_closed_for_wave7() -> None:
    from app.external_integration.broker import governance_gate

    assert governance_gate.broker_integration_authorized is False
    assert governance_gate.execution_authorized is False


@pytest.mark.asyncio
async def test_no_execution_or_broker_endpoint_in_wave7_api(async_client: AsyncClient) -> None:
    _, username, password = await _create_operator(role="admin")
    headers = await _headers(async_client, username, password)
    inventory = await async_client.get(
        "/api/v1/institutional-platform/route-inventory", headers=headers
    )
    assert inventory.status_code == 200, inventory.text
    routes = inventory.json()["routes"]
    route_text = " ".join(route["path"] for route in routes).lower()
    for forbidden in ("execute", "order", "broker", "account", "gate-open"):
        assert forbidden not in route_text

    for path in (
        "/api/v1/institutional-platform/execute",
        "/api/v1/institutional-platform/order",
        "/api/v1/institutional-platform/broker",
        "/api/v1/institutional-platform/account",
        "/api/v1/institutional-platform/open-gate",
    ):
        response = await async_client.post(path, headers=headers, json={})
        assert response.status_code in {404, 405}


@pytest.mark.asyncio
async def test_api_requires_auth_for_all_institutional_routes(async_client: AsyncClient) -> None:
    admin_id, username, password = await _create_operator(role="admin")
    admin_headers = await _headers(async_client, username, password)
    operator_id, op_username, op_password = await _create_operator(role="operator")
    operator_headers = await _headers(async_client, op_username, op_password)

    routes = (
        "/api/v1/institutional-platform/route-inventory",
        "/api/v1/institutional-platform/rbac/permissions",
        "/api/v1/institutional-platform/operator-scope-records",
        f"/api/v1/institutional-platform/operator-scope-records/{operator_id}",
    )
    for route in routes:
        unauth = await async_client.get(route)
        assert unauth.status_code == 401

    assert (
        await async_client.get(
            "/api/v1/institutional-platform/route-inventory", headers=admin_headers
        )
    ).status_code == 200
    assert (
        await async_client.get(
            "/api/v1/institutional-platform/rbac/permissions", headers=admin_headers
        )
    ).status_code == 200
    own = await async_client.get(
        f"/api/v1/institutional-platform/operator-scope-records/{operator_id}",
        headers=operator_headers,
    )
    assert own.status_code == 200, own.text
    assert own.json()["operator_id"] == operator_id
    cross = await async_client.get(
        f"/api/v1/institutional-platform/operator-scope-records/{admin_id}",
        headers=operator_headers,
    )
    assert cross.status_code == 403


@pytest.mark.asyncio
async def test_rbac_default_denies_unprivileged_operator(async_client: AsyncClient) -> None:
    _, username, password = await _create_operator(role="unprivileged")
    headers = await _headers(async_client, username, password)
    response = await async_client.get(
        "/api/v1/institutional-platform/route-inventory", headers=headers
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_rbac_permission_vocabulary_excludes_gate_execution_account_capability(
    async_client: AsyncClient,
) -> None:
    assert_permission_vocabulary_safe()
    all_permissions = {
        permission
        for permission_set in INSTITUTIONAL_ROLE_PERMISSIONS.values()
        for permission in permission_set
    }
    forbidden_markers = (
        "gate",
        "execution",
        "execute",
        "order",
        "broker",
        "account",
        "position",
        "live",
        "capital",
        "margin",
    )
    for permission in all_permissions:
        assert not any(marker in permission for marker in forbidden_markers)

    _, username, password = await _create_operator(role="admin")
    headers = await _headers(async_client, username, password)
    response = await async_client.get(
        "/api/v1/institutional-platform/rbac/permissions", headers=headers
    )
    assert response.status_code == 200, response.text
    assert response.json()["forbidden_capabilities_present"] is False


@pytest.mark.asyncio
async def test_two_operator_isolation_no_cross_operator_leakage(async_client: AsyncClient) -> None:
    operator_a_id, username_a, password_a = await _create_operator(role="operator")
    operator_b_id, username_b, password_b = await _create_operator(role="operator")
    headers_a = await _headers(async_client, username_a, password_a)
    headers_b = await _headers(async_client, username_b, password_b)

    own_a = await async_client.get(
        f"/api/v1/institutional-platform/operator-scope-records/{operator_a_id}",
        headers=headers_a,
    )
    assert own_a.status_code == 200, own_a.text
    assert own_a.json()["operator_id"] == operator_a_id

    cross = await async_client.get(
        f"/api/v1/institutional-platform/operator-scope-records/{operator_a_id}",
        headers=headers_b,
    )
    assert cross.status_code == 403

    list_b = await async_client.get(
        "/api/v1/institutional-platform/operator-scope-records", headers=headers_b
    )
    assert list_b.status_code == 200, list_b.text
    ids_visible_to_b = {item["operator_id"] for item in list_b.json()}
    assert operator_b_id in ids_visible_to_b
    assert operator_a_id not in ids_visible_to_b

    mutate_attempt = await async_client.post(
        f"/api/v1/institutional-platform/operator-scope-records/{operator_a_id}",
        headers=headers_b,
        json={"blocked": True},
    )
    assert mutate_attempt.status_code in {404, 405}


def test_institutional_platform_has_no_secret_or_pii_markers() -> None:
    root = Path(__file__).resolve().parents[1] / "app" / "institutional_platform"
    route = (
        Path(__file__).resolve().parents[1]
        / "app"
        / "api"
        / "routes"
        / "institutional_platform.py"
    )
    forbidden_values = (
        "access_token",
        "refresh_token",
        "jwt_secret",
        "password=",
        "secret=",
        "api_key",
        "private_key",
    )
    text = "\n".join(
        [
            path.read_text(encoding="utf-8")
            for path in root.rglob("*.py")
            if path.name not in {"preferences.py", "research_management.py"}
        ]
        + [route.read_text(encoding="utf-8")]
    ).lower()
    for marker in forbidden_values:
        assert marker not in text


def test_wave7_bright_line_grep_no_execution_path() -> None:
    root = Path(__file__).resolve().parents[1] / "app" / "institutional_platform"
    route = (
        Path(__file__).resolve().parents[1]
        / "app"
        / "api"
        / "routes"
        / "institutional_platform.py"
    )
    forbidden = (
        "place_order",
        "broker.connect",
        "broker.execute",
        "go_live",
        "order_routing",
        "account_balance",
        "open_gate",
        "gate_open",
        "allow_execution",
    )
    offenders: list[str] = []
    for path in [
        *(
            path
            for path in root.rglob("*.py")
            if path.name not in {"preferences.py", "research_management.py"}
        ),
        route,
    ]:
        text = path.read_text(encoding="utf-8")
        for needle in forbidden:
            if needle in text:
                offenders.append(f"{path.name}:{needle}")
    assert offenders == []


def test_w7_u01_has_no_migration_or_plugin_execution_table() -> None:
    root = Path(__file__).resolve().parents[2]
    versions = root / "backend" / "alembic" / "versions"
    migration_names = {path.name for path in versions.glob("*.py")}
    assert not any("w7_u01" in name for name in migration_names)
    assert not any("plugin_execution" in name for name in migration_names)


def test_platform_records_ui_module_has_no_governance_mutation_controls() -> None:
    """SURF-P03 M1 — frontend T-1 guard over the platform records surface.

    The CONV/SURF guards pin frontend files with non-vacuity anchors; no
    institutional-platform security test pinned a frontend path before. The
    domain-specific risk of this surface is a governance-INSPECTION view
    appearing to confer governance-mutation capability: rendering an RBAC
    role list must never look like editing one, and a plugin contract list
    must never look like enabling a plugin. The guard pins the module that
    renders the records and asserts the mutation vocabulary absent.
    """
    root = Path(__file__).resolve().parents[2]
    ui = (
        root
        / "frontend"
        / "src"
        / "components"
        / "terminal"
        / "governance"
        / "PlatformRecordsSection.tsx"
    )
    text = ui.read_text(encoding="utf-8").lower()
    # Non-vacuity anchors: the module genuinely renders the record surfaces,
    # the M2 inspection posture, and the M3 access-denial notice.
    assert "platform records" in text
    assert "route inventory" in text
    assert "inspection view" in text
    assert "access restriction, not an empty result" in text
    forbidden = (
        "place_order",
        "submit order",
        "go live",
        "connect broker",
        "broker_account",
        "execute",
        "enable_plugin",
        "grant_permission",
        "elevate_role",
    )
    assert all(item not in text for item in forbidden)
