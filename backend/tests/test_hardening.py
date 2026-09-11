"""W0-U08 security and data-integrity hardening tests."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings, clear_settings_cache


def test_jwt_secret_enforced_production() -> None:
    clear_settings_cache()
    s = Settings(
        environment="production",
        jwt_secret_key="short",
        database_auto_create_schema=False,
        allow_insecure_dev=False,
    )
    with pytest.raises(RuntimeError, match="JWT_SECRET"):
        s.validate_security_or_raise()


def test_jwt_secret_enforced_development_without_escape() -> None:
    clear_settings_cache()
    s = Settings(
        environment="development",
        jwt_secret_key="CHANGE-ME-DEV-ONLY",
        allow_insecure_dev=False,
        database_auto_create_schema=False,
    )
    with pytest.raises(RuntimeError, match="JWT_SECRET|weak"):
        s.validate_security_or_raise()


def test_production_forbids_auto_create_schema() -> None:
    clear_settings_cache()
    s = Settings(
        environment="production",
        jwt_secret_key="a" * 40,
        database_auto_create_schema=True,
        allow_insecure_dev=False,
    )
    with pytest.raises(RuntimeError, match="AUTO_CREATE_SCHEMA"):
        s.validate_security_or_raise()


def test_strong_secret_accepted() -> None:
    clear_settings_cache()
    s = Settings(
        environment="production",
        jwt_secret_key="a" * 40,
        database_auto_create_schema=False,
        allow_insecure_dev=False,
    )
    s.validate_security_or_raise()


def test_seed_source_marker(client: TestClient) -> None:
    login = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    headers = {"Authorization": f"Bearer {login.json()['tokens']['access_token']}"}
    seed = client.post("/api/v1/market/live/seed-history", headers=headers)
    assert seed.status_code == 200
    rows = client.get(
        "/api/v1/persistence/candles",
        params={"symbol": "EURUSD", "timeframe": "M1", "limit": 50, "order": "asc"},
        headers=headers,
    ).json()
    assert len(rows) >= 20
    sources = {r["source"] for r in rows}
    assert "seed:synthetic" in sources


def test_ws_ticket_connect(client: TestClient) -> None:
    login = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    access = login.json()["tokens"]["access_token"]
    ticket = client.post(
        "/api/v1/auth/ws-ticket",
        headers={"Authorization": f"Bearer {access}"},
    ).json()["ticket"]

    with client.websocket_connect(f"/ws/market?ticket={ticket}") as ws:
        first = ws.receive_json()
        assert first["type"] == "subscribed"

    # Ticket is one-time
    with pytest.raises(Exception):
        with client.websocket_connect(f"/ws/market?ticket={ticket}"):
            pass


def test_ws_query_jwt_rejected_by_default(client: TestClient) -> None:
    login = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    access = login.json()["tokens"]["access_token"]
    with pytest.raises(Exception):
        with client.websocket_connect(f"/ws/market?token={access}"):
            pass
