"""Authenticated WebSocket status integration tests."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


def _ws_ticket(client: TestClient, headers: dict[str, str]) -> str:
    response = client.post("/api/v1/auth/ws-ticket", headers=headers)
    assert response.status_code == 200, response.text
    return str(response.json()["ticket"])


def test_websocket_status_requires_auth(client: TestClient) -> None:
    with pytest.raises(Exception):
        with client.websocket_connect("/ws/status"):
            pass


def test_websocket_status_authenticated(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    ticket = _ws_ticket(client, auth_headers)
    with client.websocket_connect(f"/ws/status?ticket={ticket}") as websocket:
        data = websocket.receive_json()
        assert data["type"] == "status"
        assert data["live_streams"] is False
        websocket.send_text("ping")
        echo = websocket.receive_json()
        assert echo["type"] == "echo"
        assert echo["received"] == "ping"
