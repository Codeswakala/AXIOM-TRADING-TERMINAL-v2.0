"""System info endpoint tests."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_system_info_requires_auth(client: TestClient) -> None:
    assert client.get("/system/info").status_code == 401


def test_system_info(client: TestClient, auth_headers: dict[str, str]) -> None:
    response = client.get("/system/info", headers=auth_headers)
    assert response.status_code == 200
    payload = response.json()
    assert payload["name"] == "AXIOM"
    assert payload["unit"] == "W7-U08"
    assert payload["architecture_version"] == "2.0.0"
    assert payload["wave"].startswith("7")
    assert payload["timestamp"].endswith("+00:00") or payload["timestamp"].endswith("Z")


def test_root(client: TestClient) -> None:
    # Prefer /api JSON root (SPA may own "/" when frontend/dist exists)
    response = client.get("/api")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "online"
    assert payload["health"] == "/health"
    assert "auth_login" in payload
