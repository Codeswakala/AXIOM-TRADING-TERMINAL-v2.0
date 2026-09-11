"""UI-001-P04 shell preference persistence tests."""

from __future__ import annotations

from uuid import uuid4

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import hash_password
from app.db.models.operator import Operator
from app.db.session import session_scope
from app.institutional_platform import WorkspacePreferenceRepository

SHELL_WORKSPACE_KEY = "institutional-shell-v1"


def _shell_payload(workspace_key: str = SHELL_WORKSPACE_KEY) -> dict[str, object]:
    return {
        "workspace_key": workspace_key,
        "layout_config": {
            "active_workspace": "monitor.operations",
            "last_route": "/signals",
            "navigation": {"collapsed": False},
            "panel_layout": {
                "layoutId": "session.monitor.operations",
                "workspaceId": "monitor.operations",
                "placements": [],
            },
            "persistence_scope": "operator_shell_layout",
        },
        "visible_modules": ["operations", "research_journal", "institutional_intelligence"],
        "theme_config": {"mode": "dark", "density": "institutional"},
        "metadata": {"ui_workstream": "UI-001-P04", "version": "shell-persistence-v1"},
    }


async def _operator(session: AsyncSession, *, role: str = "operator") -> Operator:
    operator = Operator(
        username=f"ui-p04-{role}-{uuid4().hex[:10]}",
        hashed_password=hash_password("operator-pass-123"),
        role=role,
        is_active=True,
    )
    session.add(operator)
    await session.flush()
    return operator


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
async def test_shell_preferences_operator_scoped_B_cannot_read_A(
    async_client: AsyncClient,
) -> None:
    async with session_scope() as session:
        operator_a = await _operator(session)
        operator_b = await _operator(session)
        preference_a = await WorkspacePreferenceRepository(session).create_preference(
            operator_id=operator_a.id,
            payload=_shell_payload(),
        )
        preference_b = await WorkspacePreferenceRepository(session).create_preference(
            operator_id=operator_b.id,
            payload=_shell_payload("institutional-shell-v1-b"),
        )
        operator_a_id = operator_a.id
        operator_b_id = operator_b.id
        username_a = operator_a.username
        username_b = operator_b.username
        preference_a_id = preference_a.preference_id
        preference_b_id = preference_b.preference_id

    headers_a = await _headers(async_client, username_a)
    headers_b = await _headers(async_client, username_b)

    a_reads_own = await async_client.get(
        f"/api/v1/institutional-platform/workspace-preferences/{preference_a_id}",
        headers=headers_a,
    )
    assert a_reads_own.status_code == 200, a_reads_own.text
    assert a_reads_own.json()["operator_id"] == operator_a_id

    b_reads_a = await async_client.get(
        f"/api/v1/institutional-platform/workspace-preferences/{preference_a_id}",
        headers=headers_b,
    )
    assert b_reads_a.status_code == 403

    b_list = await async_client.get(
        "/api/v1/institutional-platform/workspace-preferences",
        headers=headers_b,
    )
    assert b_list.status_code == 200, b_list.text
    assert not any(item["operator_id"] == operator_a_id for item in b_list.json())
    assert any(item["preference_id"] == preference_b_id for item in b_list.json())
    assert all(item["operator_id"] == operator_b_id for item in b_list.json())

    b_writes_a = await async_client.put(
        f"/api/v1/institutional-platform/workspace-preferences/{preference_a_id}",
        headers=headers_b,
        json=_shell_payload(),
    )
    assert b_writes_a.status_code == 403
