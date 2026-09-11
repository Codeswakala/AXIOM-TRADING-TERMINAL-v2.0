"""Unit / API tests for health and readiness endpoints."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_health_ok(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["service"] == "AXIOM"
    assert "version" in payload
    assert "timestamp" in payload


def test_health_under_api_prefix(client: TestClient) -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ready_includes_live_database(client: TestClient) -> None:
    response = client.get("/ready")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ready"
    by_name = {check["name"]: check for check in payload["checks"]}
    assert by_name["configuration"]["status"] == "up"
    assert by_name["logging"]["status"] == "up"
    assert by_name["database"]["status"] in {"up", "degraded"}
    assert "backend=" in (by_name["database"]["detail"] or "")
    assert by_name["ml_engine"]["status"] == "stub"
    assert by_name["broker"]["status"] == "stub"


def test_ready_under_api_prefix(client: TestClient) -> None:
    response = client.get("/api/v1/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"
