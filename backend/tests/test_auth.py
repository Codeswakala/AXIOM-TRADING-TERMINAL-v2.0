"""Auth tests including W0-U08 rotation + tickets."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.auth.security import create_token, hash_password, verify_password
from app.core.config import Settings


def test_password_hash_roundtrip() -> None:
    hashed = hash_password("secret123")
    assert hashed != "secret123"
    assert verify_password("secret123", hashed)
    assert not verify_password("wrong", hashed)


def test_jwt_access_token_roundtrip() -> None:
    settings = Settings(
        jwt_secret_key="unit-test-secret-key-for-jwt-32chars",
        allow_insecure_dev=True,
        environment="testing",
    )
    token = create_token(
        subject="op-1",
        token_type="access",
        settings=settings,
        extra_claims={"role": "admin"},
    )
    from app.auth.security import decode_token

    payload = decode_token(token, settings)
    assert payload["sub"] == "op-1"
    assert payload["type"] == "access"
    assert payload["role"] == "admin"


def test_login_bootstrap_and_me(client: TestClient) -> None:
    login = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert login.status_code == 200, login.text
    body = login.json()
    assert "access_token" in body["tokens"]
    assert "refresh_token" in body["tokens"]
    assert body["operator"]["username"] == "admin"
    access = body["tokens"]["access_token"]
    refresh = body["tokens"]["refresh_token"]

    me = client.get("/api/v1/operator/me", headers={"Authorization": f"Bearer {access}"})
    assert me.status_code == 200
    assert me.json()["username"] == "admin"

    unauth = client.get("/api/v1/ingestion/stats")
    assert unauth.status_code == 401

    auth_stats = client.get(
        "/api/v1/ingestion/stats",
        headers={"Authorization": f"Bearer {access}"},
    )
    assert auth_stats.status_code == 200

    refreshed = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh})
    assert refreshed.status_code == 200
    new_access = refreshed.json()["access_token"]
    new_refresh = refreshed.json()["refresh_token"]
    assert new_refresh != refresh

    # Old refresh must fail (rotation)
    reused = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh})
    assert reused.status_code == 401

    me2 = client.get("/api/v1/operator/me", headers={"Authorization": f"Bearer {new_access}"})
    assert me2.status_code == 200

    out = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {new_access}"},
        json={"refresh_token": new_refresh},
    )
    assert out.status_code == 200


def test_login_invalid_credentials(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "wrong-password"},
    )
    assert response.status_code == 401


def test_me_without_token(client: TestClient) -> None:
    assert client.get("/api/v1/operator/me").status_code == 401


def test_ready_includes_authentication(client: TestClient) -> None:
    response = client.get("/ready")
    assert response.status_code == 200
    names = {c["name"] for c in response.json()["checks"]}
    assert "authentication" in names


def test_ws_ticket_issued(client: TestClient) -> None:
    login = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    access = login.json()["tokens"]["access_token"]
    ticket = client.post(
        "/api/v1/auth/ws-ticket",
        headers={"Authorization": f"Bearer {access}"},
    )
    assert ticket.status_code == 200
    body = ticket.json()
    assert "ticket" in body
    assert body["expires_in"] >= 10
    assert "query string" in body["usage"].lower() or "ticket" in body["usage"].lower()
