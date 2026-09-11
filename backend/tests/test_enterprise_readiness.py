"""W7-U07 enterprise scalability and multi-user readiness hardening tests."""

from __future__ import annotations

import json
import logging
from uuid import uuid4

import pytest
from httpx import AsyncClient
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import hash_password
from app.auth.service import AuthService
from app.core.config import Settings
from app.core.logging import JsonFormatter
from app.db.models.audit import AuditEvent
from app.db.models.operator import Operator
from app.db.models.research_management import ResearchCollection
from app.db.session import session_scope
from app.institutional_platform import (
    INSTITUTIONAL_ROLE_PERMISSIONS,
    RATE_GUARD_DISPOSITION,
    ResearchManagementRepository,
    WorkspacePreferenceRepository,
    assert_permission_vocabulary_safe,
)
from app.services.observability_service import redact


async def _operator(session: AsyncSession, *, role: str = "operator") -> Operator:
    operator = Operator(
        username=f"readiness-{role}-{uuid4().hex[:10]}",
        hashed_password=hash_password("operator-pass-123"),
        role=role,
        is_active=True,
    )
    session.add(operator)
    await session.flush()
    return operator


def _workspace_payload(name: str) -> dict[str, object]:
    return {
        "workspace_key": name,
        "layout_config": {"density": "comfortable"},
        "visible_modules": ["operations"],
        "theme_config": {"mode": "dark"},
        "metadata": {"note": "readiness proof"},
    }


async def _headers(async_client: AsyncClient, username: str) -> dict[str, str]:
    login = await async_client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": "operator-pass-123"},
    )
    assert login.status_code == 200, login.text
    token = login.json()["tokens"]["access_token"]
    assert token
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_rbac_default_denies_unprivileged_operator_at_scale(
    async_client: AsyncClient,
) -> None:
    async with session_scope() as session:
        unprivileged = await _operator(session, role="unprivileged")
        username = unprivileged.username
    headers = await _headers(async_client, username)
    protected_routes = (
        "/api/v1/institutional-platform/route-inventory",
        "/api/v1/institutional-platform/api-catalogue",
        "/api/v1/institutional-platform/plugin-contracts",
        "/api/v1/institutional-platform/rbac/permissions",
    )
    for route in protected_routes:
        response = await async_client.get(route, headers=headers)
        assert response.status_code == 403, f"{route} -> {response.status_code}"


def test_rbac_permission_vocabulary_excludes_gate_execution_account_capability() -> None:
    assert_permission_vocabulary_safe()
    forbidden = (
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
    permissions = {
        permission
        for permission_set in INSTITUTIONAL_ROLE_PERMISSIONS.values()
        for permission in permission_set
    }
    assert permissions
    for permission in permissions:
        assert not any(marker in permission for marker in forbidden)


@pytest.mark.asyncio
async def test_multi_user_two_operator_isolation_across_institutional_resources(
    async_client: AsyncClient,
) -> None:
    async with session_scope() as session:
        operator_a = await _operator(session)
        operator_b = await _operator(session)
        preference_a = await WorkspacePreferenceRepository(session).create_preference(
            operator_id=operator_a.id,
            payload=_workspace_payload("a-readiness-workspace"),
        )
        preference_b = await WorkspacePreferenceRepository(session).create_preference(
            operator_id=operator_b.id,
            payload=_workspace_payload("b-readiness-workspace"),
        )
        collection_a = await ResearchManagementRepository(session).create_collection(
            operator_id=operator_a.id,
            payload={"name": f"A Readiness {uuid4().hex[:6]}"},
        )
        collection_b = await ResearchManagementRepository(session).create_collection(
            operator_id=operator_b.id,
            payload={"name": f"B Readiness {uuid4().hex[:6]}"},
        )
        a_id = operator_a.id
        b_id = operator_b.id
        username_b = operator_b.username
        pref_a_id = preference_a.preference_id
        pref_b_id = preference_b.preference_id
        collection_a_id = collection_a.collection_id
        collection_b_id = collection_b.collection_id

    headers_b = await _headers(async_client, username_b)
    read_pref_a = await async_client.get(
        f"/api/v1/institutional-platform/workspace-preferences/{pref_a_id}",
        headers=headers_b,
    )
    assert read_pref_a.status_code == 403
    list_prefs_b = await async_client.get(
        "/api/v1/institutional-platform/workspace-preferences", headers=headers_b
    )
    assert list_prefs_b.status_code == 200, list_prefs_b.text
    assert not any(item["operator_id"] == a_id for item in list_prefs_b.json())
    assert any(item["preference_id"] == pref_b_id for item in list_prefs_b.json())

    read_collection_a = await async_client.get(
        f"/api/v1/institutional-platform/research-collections/{collection_a_id}",
        headers=headers_b,
    )
    assert read_collection_a.status_code == 403
    list_collections_b = await async_client.get(
        "/api/v1/institutional-platform/research-collections", headers=headers_b
    )
    assert list_collections_b.status_code == 200, list_collections_b.text
    assert not any(item["operator_id"] == a_id for item in list_collections_b.json())
    assert any(item["collection_id"] == collection_b_id for item in list_collections_b.json())
    assert all(item["operator_id"] == b_id for item in list_collections_b.json())


@pytest.mark.asyncio
async def test_authorize_before_validate_cross_operator_mutation_403(
    async_client: AsyncClient,
) -> None:
    async with session_scope() as session:
        operator_a = await _operator(session)
        operator_b = await _operator(session)
        collection_a = await ResearchManagementRepository(session).create_collection(
            operator_id=operator_a.id,
            payload={"name": f"A Authz First {uuid4().hex[:6]}"},
        )
        username_b = operator_b.username
        collection_a_id = collection_a.collection_id
    headers_b = await _headers(async_client, username_b)
    response = await async_client.post(
        f"/api/v1/institutional-platform/research-collections/{collection_a_id}/members",
        headers=headers_b,
        json={},
    )
    assert response.status_code == 403, response.text


@pytest.mark.asyncio
async def test_admin_default_credential_rejected_when_insecure_dev_off(
    prepared_db: None,
) -> None:
    settings = Settings(
        environment="production",
        jwt_secret_key="prodkey-abcdefghijklmnopqrstuvwxyz-1234567890",
        database_auto_create_schema=False,
        allow_insecure_dev=False,
        bootstrap_admin_enabled=True,
        bootstrap_admin_username="admin",
        bootstrap_admin_password="admin123",
    )
    settings.validate_security_or_raise()
    async with session_scope() as session:
        service = AuthService(session, settings)
        with pytest.raises(RuntimeError, match="historical default admin123"):
            await service.ensure_bootstrap_admin()


def test_abuse_or_rate_guard_enforced_or_documented_deferred() -> None:
    # BO-B-07.1 supersession (disclosed churn): the W7-U07 disposition was
    # `formally_deferred`; the BO closes it with an implemented in-memory
    # sliding-window limiter. The test now pins the implemented state and the
    # closure rationale (no assertion weakened — the debt id is unchanged).
    assert RATE_GUARD_DISPOSITION.status == "implemented"
    assert RATE_GUARD_DISPOSITION.technical_debt_id == "TD-W7-U07-RATE-GUARD"
    assert "BO-B-07.1" in RATE_GUARD_DISPOSITION.rationale
    assert "fail-safe" in RATE_GUARD_DISPOSITION.rationale


@pytest.mark.asyncio
async def test_scalability_change_preserves_audit_redaction_and_gate_closed(
    prepared_db: None,
) -> None:
    from app.external_integration.broker import governance_gate

    async with session_scope() as session:
        operator = await _operator(session)
        collection = await ResearchManagementRepository(session).create_collection(
            operator_id=operator.id,
            payload={"name": f"Audit Readiness {uuid4().hex[:6]}"},
        )
        stmt = (
            select(ResearchCollection.collection_id)
            .outerjoin(
                AuditEvent,
                and_(
                    AuditEvent.resource_type == "research_collection",
                    AuditEvent.resource_id == ResearchCollection.collection_id,
                    AuditEvent.correlation_id == ResearchCollection.audit_correlation_id,
                    AuditEvent.action == "research_collection.created",
                ),
            )
            .where(ResearchCollection.collection_id == collection.collection_id)
            .where(AuditEvent.id.is_(None))
        )
        assert list((await session.scalars(stmt)).all()) == []
    redacted = redact(
        "Authorization: Bearer raw-token password=admin123 "
        "postgresql+asyncpg://axiom:axiom_dev_password@localhost/axiom"
    )
    assert "raw-token" not in redacted
    assert "admin123" not in redacted
    assert "axiom_dev_password" not in redacted
    assert governance_gate.broker_integration_authorized is False
    assert governance_gate.execution_authorized is False


def test_no_secret_or_pii_in_observability_or_logs() -> None:
    record = logging.LogRecord(
        name="axiom.readiness",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="Authorization: Bearer raw-token password=admin123 access_token=raw-token",
        args=(),
        exc_info=None,
    )
    record.category = "SECURITY"
    payload = json.loads(JsonFormatter().format(record))
    text = json.dumps(payload).lower()
    assert "raw-token" not in text
    assert "admin123" not in text
    assert "access_token=raw-token" not in text


def test_gate_remains_closed_for_wave7() -> None:
    from app.external_integration.broker import governance_gate

    assert governance_gate.broker_integration_authorized is False
    assert governance_gate.execution_authorized is False
