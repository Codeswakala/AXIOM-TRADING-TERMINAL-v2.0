"""W7-U02 operator workspace preference tests."""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

import pytest
from httpx import AsyncClient
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import hash_password
from app.db.models.audit import AuditEvent
from app.db.models.operator import Operator
from app.db.models.operator_workspace_preference import OperatorWorkspacePreference
from app.db.session import session_scope
from app.institutional_platform import WorkspacePreferenceFactory, WorkspacePreferenceRepository


def _payload(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "workspace_key": "default",
        "layout_config": {"density": "comfortable", "columns": 12},
        "visible_modules": ["operations", "execution_research"],
        "theme_config": {"mode": "dark", "accent": "blue"},
        "metadata": {"note": "presentation preferences only"},
    }
    payload.update(overrides)
    return payload


async def _operator(session: AsyncSession, *, role: str = "operator") -> Operator:
    operator = Operator(
        username=f"prefs-{role}-{uuid4().hex[:10]}",
        hashed_password=hash_password("operator-pass-123"),
        role=role,
        is_active=True,
    )
    session.add(operator)
    await session.flush()
    return operator


async def _assert_preference_no_orphan(session: AsyncSession) -> None:
    stmt = (
        select(OperatorWorkspacePreference.preference_id)
        .outerjoin(
            AuditEvent,
            and_(
                AuditEvent.resource_type == "operator_workspace_preference",
                AuditEvent.resource_id == OperatorWorkspacePreference.preference_id,
                AuditEvent.correlation_id == OperatorWorkspacePreference.audit_correlation_id,
                AuditEvent.action == "operator_workspace_preference.created",
            ),
        )
        .where(AuditEvent.id.is_(None))
    )
    assert list((await session.scalars(stmt)).all()) == []


async def _assert_operator_no_orphan(session: AsyncSession) -> None:
    stmt = (
        select(OperatorWorkspacePreference.preference_id)
        .outerjoin(Operator, Operator.id == OperatorWorkspacePreference.operator_id)
        .where(Operator.id.is_(None))
    )
    assert list((await session.scalars(stmt)).all()) == []


@pytest.mark.asyncio
async def test_operator_workspace_preferences_persist_and_audit_no_orphan(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        operator = await _operator(session)
        preference = await WorkspacePreferenceRepository(session).create_preference(
            payload=_payload(), operator_id=operator.id
        )
        assert preference.research_status == "research_only"
        assert preference.operator_id == operator.id
        assert preference.visible_modules == ["operations", "execution_research"]
        event = (
            await session.scalars(
                select(AuditEvent).where(
                    AuditEvent.resource_type == "operator_workspace_preference",
                    AuditEvent.resource_id == preference.preference_id,
                    AuditEvent.action == "operator_workspace_preference.created",
                )
            )
        ).one()
        assert event.correlation_id == preference.audit_correlation_id
        await _assert_preference_no_orphan(session)
        await _assert_operator_no_orphan(session)


@pytest.mark.asyncio
async def test_workspace_preferences_are_operator_scoped_two_operator_isolation(
    async_client: AsyncClient,
) -> None:
    async with session_scope() as session:
        operator_a = await _operator(session)
        operator_b = await _operator(session)
        preference = await WorkspacePreferenceRepository(session).create_preference(
            payload=_payload(workspace_key="operator-a"), operator_id=operator_a.id
        )
        a_id = operator_a.id
        b_id = operator_b.id
        a_username = operator_a.username
        b_username = operator_b.username

    headers_b = await _headers(async_client, b_username)
    list_b = await async_client.get(
        "/api/v1/institutional-platform/workspace-preferences", headers=headers_b
    )
    assert list_b.status_code == 200, list_b.text
    assert not any(item["operator_id"] == a_id for item in list_b.json())
    assert all(item["operator_id"] == b_id for item in list_b.json())

    read_a = await async_client.get(
        f"/api/v1/institutional-platform/workspace-preferences/{preference.preference_id}",
        headers=headers_b,
    )
    assert read_a.status_code == 403

    missing = await async_client.get(
        f"/api/v1/institutional-platform/workspace-preferences/{uuid4()}",
        headers=headers_b,
    )
    assert missing.status_code == 404

    write_a = await async_client.put(
        f"/api/v1/institutional-platform/workspace-preferences/{preference.preference_id}",
        headers=headers_b,
        json=_payload(workspace_key="operator-a"),
    )
    assert write_a.status_code == 403
    _ = a_username


def test_workspace_customization_has_no_action_or_account_or_execution_fields() -> None:
    forbidden = {
        "order_payload",
        "order_intent",
        "broker_account_id",
        "account_id",
        "position_id",
        "live_position_id",
        "execution_status",
        "real_pnl",
        "pnl",
        "balance",
        "margin",
        "capital",
        "gate_state",
        "open_gate",
        "allow_execution",
    }
    assert set(OperatorWorkspacePreference.__table__.columns.keys()).isdisjoint(forbidden)
    factory = WorkspacePreferenceFactory()
    for key in forbidden:
        with pytest.raises(ValueError):
            factory.validate_payload(_payload(metadata={key: "blocked"}))


def test_workspace_preferences_config_has_no_secret_or_pii_markers() -> None:
    factory = WorkspacePreferenceFactory()
    for marker in ("access_token", "refresh_token", "jwt", "password", "secret", "api_key"):
        with pytest.raises(ValueError, match="WORKSPACE_PREFERENCE_SECRET_MARKER"):
            factory.validate_payload(_payload(metadata={"note": f"contains {marker}"}))


@pytest.mark.asyncio
async def test_workspace_preferences_require_auth(async_client: AsyncClient) -> None:
    unauth = await async_client.get("/api/v1/institutional-platform/workspace-preferences")
    assert unauth.status_code == 401
    async with session_scope() as session:
        operator = await _operator(session)
        username = operator.username
    headers = await _headers(async_client, username)
    create = await async_client.post(
        "/api/v1/institutional-platform/workspace-preferences",
        headers=headers,
        json=_payload(),
    )
    assert create.status_code == 201, create.text
    preference_id = create.json()["preference_id"]
    listing = await async_client.get(
        "/api/v1/institutional-platform/workspace-preferences", headers=headers
    )
    assert listing.status_code == 200, listing.text
    assert any(item["preference_id"] == preference_id for item in listing.json())
    update = await async_client.put(
        f"/api/v1/institutional-platform/workspace-preferences/{preference_id}",
        headers=headers,
        json=_payload(layout_config={"density": "compact", "columns": 8}),
    )
    assert update.status_code == 200, update.text
    assert update.json()["layout_config"]["density"] == "compact"


def test_gate_remains_closed_for_wave7() -> None:
    from app.external_integration.broker import governance_gate

    assert governance_gate.broker_integration_authorized is False
    assert governance_gate.execution_authorized is False


async def _headers(async_client: AsyncClient, username: str) -> dict[str, str]:
    login = await async_client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": "operator-pass-123"},
    )
    assert login.status_code == 200, login.text
    return {"Authorization": f"Bearer {login.json()['tokens']['access_token']}"}


def test_workspace_preference_page_has_no_forbidden_controls() -> None:
    root = Path(__file__).resolve().parents[2]
    page = root / "frontend" / "src" / "components" / "terminal" / "settings" / "WorkspaceSettingsOverlay.tsx"
    text = page.read_text(encoding="utf-8").lower()
    forbidden = (
        "place_order",
        "submit order",
        "go live",
        "connect broker",
        "account_id",
        "order_ticket",
        "broker_account",
    )
    assert all(item not in text for item in forbidden)
