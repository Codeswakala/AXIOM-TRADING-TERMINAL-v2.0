"""W0-U08.1 — mandatory regression: ws-ticket must return 200 and open WS (ITRGA F-1)."""

from __future__ import annotations

from fastapi.testclient import TestClient


def _login(client: TestClient) -> str:
    login = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert login.status_code == 200, login.text
    return login.json()["tokens"]["access_token"]


def test_ws_ticket_endpoint_returns_200_not_500(client: TestClient) -> None:
    """The exact failure mode from operator logs: POST /auth/ws-ticket → 500."""
    access = _login(client)
    resp = client.post(
        "/api/v1/auth/ws-ticket",
        headers={"Authorization": f"Bearer {access}"},
    )
    assert resp.status_code == 200, (
        f"ws-ticket must not 500 (ITRGA F-1); got {resp.status_code}: {resp.text}"
    )
    body = resp.json()
    assert body.get("ticket")
    usage = body.get("usage", "").lower()
    assert "token=" not in usage or "ticket" in usage


def test_ws_ticket_then_market_subscribe_no_jwt_in_url(client: TestClient) -> None:
    """Issue ticket → connect /ws/market?ticket=… without access JWT in URL."""
    access = _login(client)
    headers = {"Authorization": f"Bearer {access}"}

    ticket_resp = client.post("/api/v1/auth/ws-ticket", headers=headers)
    assert ticket_resp.status_code == 200, ticket_resp.text
    ticket = ticket_resp.json()["ticket"]

    # Ensure live service can start (regression of approved U05/U06 capability)
    start = client.post("/api/v1/market/live/start", headers=headers)
    assert start.status_code == 200, start.text

    url = f"/ws/market?ticket={ticket}"
    assert "token=" not in url  # access JWT must not appear in query string

    with client.websocket_connect(url) as ws:
        first = ws.receive_json()
        assert first["type"] == "subscribed"
        assert first["channel"] == "market"
        ws.send_text("ping")
        pong = ws.receive_json()
        assert pong["type"] in {"pong", "live_candle", "subscribed"}

    client.post("/api/v1/market/live/stop", headers=headers)


def test_audit_append_does_not_break_business_writes(client: TestClient) -> None:
    """Multiple audited endpoints in one session must remain 200."""
    access = _login(client)
    headers = {"Authorization": f"Bearer {access}"}

    # login already audited; ticket issues another audit write
    t1 = client.post("/api/v1/auth/ws-ticket", headers=headers)
    assert t1.status_code == 200
    t2 = client.post("/api/v1/auth/ws-ticket", headers=headers)
    assert t2.status_code == 200
    assert t1.json()["ticket"] != t2.json()["ticket"]


def test_refresh_rotation_old_rejected(client: TestClient) -> None:
    login = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    refresh = login.json()["tokens"]["refresh_token"]
    rotated = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh})
    assert rotated.status_code == 200
    old = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh})
    assert old.status_code == 401
