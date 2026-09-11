"""W7-U04 API catalogue and research API hardening tests."""

from __future__ import annotations

import json
import re
from uuid import uuid4

import pytest
from httpx import AsyncClient

from app.auth.security import hash_password
from app.db.models.operator import Operator
from app.db.session import session_scope
from app.institutional_platform import CATALOGUE_VERSION, ResearchManagementRepository


async def _operator(*, role: str = "operator") -> tuple[str, str, str]:
    username = f"w7-u04-{role}-{uuid4().hex[:10]}"
    password = "operator-pass-123"
    async with session_scope() as session:
        operator = Operator(
            username=username,
            hashed_password=hash_password(password),
            role=role,
            is_active=True,
            display_name=f"W7-U04 {role} test operator",
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
    token = login.json()["tokens"]["access_token"]
    assert token
    return {"Authorization": f"Bearer {token}"}


async def _admin_headers(async_client: AsyncClient) -> dict[str, str]:
    return await _headers(async_client, "admin", "admin123")


def _probe_path(path: str) -> str:
    return re.sub(r"\{[^}]+\}", "missing", path)


async def _request(
    async_client: AsyncClient,
    *,
    method: str,
    path: str,
    headers: dict[str, str] | None = None,
):
    kwargs = {"headers": headers} if headers else {}
    if method in {"POST", "PUT", "PATCH"}:
        kwargs["json"] = {}
    return await async_client.request(method, path, **kwargs)


@pytest.mark.asyncio
async def test_api_catalogue_lists_versioned_research_routes(async_client: AsyncClient) -> None:
    headers = await _admin_headers(async_client)
    response = await async_client.get(
        "/api/v1/institutional-platform/api-catalogue", headers=headers
    )
    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["catalogue_version"] == CATALOGUE_VERSION
    assert payload["api_version"] == "v1"
    assert payload["actuation_surface_present"] is False
    assert payload["governance_gate_capability_present"] is False
    assert payload["persistence"]["catalogue_table_persisted"] is False
    assert payload["persistence"]["alembic_head_expected"] == "20260717_0037"
    assert payload["abuse_guard"]["status"] == "deferred"
    routes = payload["routes"]
    route_paths = {route["path"] for route in routes}
    assert "/api/v1/institutional-platform/api-catalogue" in route_paths
    assert "/api/v1/institutional-platform/research-collections" in route_paths
    assert "/api/v1/intelligence/scenario-reports" in route_paths
    assert "/api/v1/signals/history" in route_paths
    assert all(route["version"] == "v1" for route in routes)
    assert all(route["auth_required"] is True for route in routes)


@pytest.mark.asyncio
async def test_api_catalogue_and_research_api_have_no_execution_or_broker_or_gate_endpoint(
    async_client: AsyncClient,
) -> None:
    headers = await _admin_headers(async_client)
    response = await async_client.get(
        "/api/v1/institutional-platform/api-catalogue", headers=headers
    )
    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["actuation_surface_present"] is False
    assert payload["governance_gate_capability_present"] is False

    forbidden_probe_paths = (
        "/api/v1/execute",
        "/api/v1/order",
        "/api/v1/broker",
        "/api/v1/account",
        "/api/v1/open-gate",
        "/api/v1/go-live",
        "/api/v1/institutional-platform/execute",
        "/api/v1/institutional-platform/order",
        "/api/v1/institutional-platform/broker",
        "/api/v1/institutional-platform/account",
        "/api/v1/institutional-platform/open-gate",
        "/api/v1/institutional-platform/go-live",
    )
    for path in forbidden_probe_paths:
        result = await async_client.post(path, headers=headers, json={})
        assert result.status_code in {404, 405}, f"{path} -> {result.status_code}"


@pytest.mark.asyncio
async def test_all_catalogued_routes_require_auth(async_client: AsyncClient) -> None:
    headers = await _admin_headers(async_client)
    catalogue = await async_client.get(
        "/api/v1/institutional-platform/api-catalogue", headers=headers
    )
    assert catalogue.status_code == 200, catalogue.text
    for route in catalogue.json()["routes"]:
        path = _probe_path(route["path"])
        for method in route["methods"]:
            unauth = await _request(async_client, method=method, path=path)
            assert unauth.status_code == 401, f"UNAUTH {method} {path} -> {unauth.status_code}"
            auth = await _request(async_client, method=method, path=path, headers=headers)
            assert auth.status_code != 401, f"AUTH {method} {path} unexpectedly 401"


@pytest.mark.asyncio
async def test_api_catalogue_response_has_no_secret_or_pii_markers(
    async_client: AsyncClient,
) -> None:
    headers = await _admin_headers(async_client)
    response = await async_client.get(
        "/api/v1/institutional-platform/api-catalogue", headers=headers
    )
    assert response.status_code == 200, response.text
    text = json.dumps(response.json()).lower()
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


@pytest.mark.asyncio
async def test_api_surface_preserves_operator_scoping_two_operator(
    async_client: AsyncClient,
) -> None:
    operator_a_id, username_a, password_a = await _operator(role="operator")
    operator_b_id, username_b, password_b = await _operator(role="operator")
    async with session_scope() as session:
        collection_a = await ResearchManagementRepository(session).create_collection(
            operator_id=operator_a_id,
            payload={"name": f"A Catalogue Scope {uuid4().hex[:6]}"},
        )
        collection_b = await ResearchManagementRepository(session).create_collection(
            operator_id=operator_b_id,
            payload={"name": f"B Catalogue Scope {uuid4().hex[:6]}"},
        )
        collection_a_id = collection_a.collection_id
        collection_b_id = collection_b.collection_id

    headers_a = await _headers(async_client, username_a, password_a)
    headers_b = await _headers(async_client, username_b, password_b)
    own_a = await async_client.get(
        f"/api/v1/institutional-platform/research-collections/{collection_a_id}",
        headers=headers_a,
    )
    assert own_a.status_code == 200, own_a.text
    cross_read = await async_client.get(
        f"/api/v1/institutional-platform/research-collections/{collection_a_id}",
        headers=headers_b,
    )
    assert cross_read.status_code == 403
    list_b = await async_client.get(
        "/api/v1/institutional-platform/research-collections", headers=headers_b
    )
    assert list_b.status_code == 200, list_b.text
    assert not any(item["collection_id"] == collection_a_id for item in list_b.json())
    assert any(item["collection_id"] == collection_b_id for item in list_b.json())
    cross_mutate = await async_client.post(
        f"/api/v1/institutional-platform/research-collections/{collection_a_id}/members",
        headers=headers_b,
        json={},
    )
    assert cross_mutate.status_code == 403


def test_gate_remains_closed_for_wave7() -> None:
    from app.external_integration.broker import governance_gate

    assert governance_gate.broker_integration_authorized is False
    assert governance_gate.execution_authorized is False
