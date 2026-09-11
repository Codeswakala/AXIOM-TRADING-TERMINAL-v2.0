"""V2 BE-10 API tests — BO-V2-BE-10-001 L8/L9 (both GETs: envelope, RBAC
paths, banner carriage)."""

from __future__ import annotations

import socket
from datetime import timezone
from uuid import uuid4

import pytest

from app.auth.security import hash_password
from app.db.models.operator import Operator
from app.db.session import session_scope
from tests.test_v2_be10_engine import (
    _seed_mapping,
    _seed_signal,
    _seed_sync,
)

AC = "/api/v1/v2/account-context"
PASSWORD = "operator-pass-123"
UTC = timezone.utc


@pytest.fixture(autouse=True)
def _socket_guard(monkeypatch):
    def _deny(*_a, **_k):
        raise AssertionError("network attempt during BE-10 test")

    monkeypatch.setattr(socket, "getaddrinfo", _deny)
    monkeypatch.setattr(socket, "create_connection", _deny)


async def _login(client, username, password=PASSWORD):
    r = await client.post("/api/v1/auth/login",
                          json={"username": username, "password": password})
    assert r.status_code == 200, r.text
    return {"Authorization": f"Bearer {r.json()['tokens']['access_token']}"}


async def _admin(client):
    return await _login(client, "admin", "admin123")


@pytest.mark.asyncio
async def test_alignment_end_to_end_with_envelope(prepared_db, async_client):
    async with session_scope() as session:
        await _seed_mapping(session)
        await _seed_sync(session, positions=(("EURUSDm", "1", "0"),))
        await _seed_signal(session, "forex.eurusd", "up")
    headers = await _admin(async_client)
    r = (await async_client.get(f"{AC}/alignment", headers=headers)).json()
    assert r["outcome"] == "computed"
    for key in ("mode", "correlation_id", "timestamp"):
        assert key in r  # BE-1 envelope
    row = {x["instrument_ext_id"]: x for x in r["rows"]}["EURUSDm"]
    assert row["verdict"] == "aligned"
    assert row["basis_sync_run_id"] == r["basis_sync_run_id"]
    assert len(r["digest"]) == 64
    assert r["engine_version"] == "ace-1.0.0"


@pytest.mark.asyncio
async def test_summary_census(prepared_db, async_client):
    async with session_scope() as session:
        await _seed_mapping(session)
        await _seed_sync(session, positions=(
            ("EURUSDm", "1", "0"), ("XAUUSDm", "1", "0")))
        await _seed_signal(session, "forex.eurusd", "down")
    headers = await _admin(async_client)
    r = (await async_client.get(f"{AC}/summary", headers=headers)).json()
    assert r["outcome"] == "computed"
    assert r["verdict_counts"]["opposed"] == 1       # long vs down-signal
    assert r["verdict_counts"]["unmapped"] == 1      # XAUUSDm not seeded
    assert r["unmapped_count"] == 1
    assert r["total_rows"] == 2


@pytest.mark.asyncio
async def test_l4_no_basis_refusal_on_the_wire(prepared_db, async_client):
    async with session_scope() as session:
        await _seed_mapping(session)
    headers = await _admin(async_client)
    r = (await async_client.get(f"{AC}/alignment", headers=headers)).json()
    assert r["outcome"] == "refused"
    assert r["refusal_class"] == "account_context.no_basis"


@pytest.mark.asyncio
async def test_l8_banner_carried_end_to_end(prepared_db, async_client):
    async with session_scope() as session:
        await _seed_mapping(session)
        await _seed_sync(session, positions=(("EURUSDm", "1", "0"),),
                         age_hours=30.0)
    headers = await _admin(async_client)
    for path in ("alignment", "summary"):
        r = (await async_client.get(f"{AC}/{path}",
                                    headers=headers)).json()
        assert r["staleness"] == "stale"
        assert "last-good" in r["banner"]  # never silently fresh


@pytest.mark.asyncio
async def test_l9_rbac_gates_both_routes(prepared_db, async_client):
    async with session_scope() as session:
        op = Operator(username=f"be10-op-{uuid4().hex[:10]}",
                      hashed_password=hash_password(PASSWORD),
                      role="operator", is_active=True)
        session.add(op)
        await session.flush()
        username = op.username
    headers = await _login(async_client, username)
    for path in ("alignment", "summary"):
        r = await async_client.get(f"{AC}/{path}", headers=headers)
        assert r.status_code == 403  # operator lacks the new permission
        assert r.json()["detail"] == "Permission denied"  # generic (BE-1)
        r = await async_client.get(f"{AC}/{path}")
        assert r.status_code == 401
