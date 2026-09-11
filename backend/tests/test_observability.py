"""W1-U02 observability service tests."""

from __future__ import annotations

import json
import logging

from fastapi.testclient import TestClient

from app.core.logging import JsonFormatter
from app.services.observability_service import (
    redact,
    reset_correlation_id,
    set_correlation_id,
)


def test_redaction_removes_tokens_passwords_and_db_credentials() -> None:
    raw_token = "abc.def.secret-token"
    raw_password = "super-secret-password"
    raw_db = "postgresql+asyncpg://axiom:axiom_dev_password@localhost:5432/axiom"
    message = (
        f"Authorization: Bearer {raw_token} password={raw_password} "
        f"database={raw_db} access_token={raw_token}"
    )
    redacted = redact(message)
    assert raw_token not in redacted
    assert raw_password not in redacted
    assert "axiom_dev_password" not in redacted
    assert "[REDACTED]" in redacted


def test_json_formatter_has_required_fields_and_correlation_id() -> None:
    ctx = set_correlation_id("corr-test-123")
    try:
        record = logging.LogRecord(
            name="axiom.test",
            level=logging.INFO,
            pathname=__file__,
            lineno=1,
            msg="Authorization: Bearer raw-secret-token",
            args=(),
            exc_info=None,
        )
        record.category = "API"
        payload = json.loads(JsonFormatter().format(record))
    finally:
        reset_correlation_id(ctx)

    assert payload["timestamp"].endswith("+00:00")
    assert payload["level"] == "INFO"
    assert payload["logger"] == "axiom.test"
    assert payload["component"] == "API"
    assert payload["correlation_id"] == "corr-test-123"
    assert "raw-secret-token" not in payload["message"]


def test_request_correlation_id_response_header(client: TestClient) -> None:
    response = client.get("/health", headers={"X-Correlation-ID": "operator-correlation-id"})
    assert response.status_code == 200
    assert response.headers["X-Correlation-ID"] == "operator-correlation-id"


def test_metrics_requires_auth_and_exposes_shape(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    assert client.get("/api/v1/metrics").status_code == 401
    response = client.get("/api/v1/metrics", headers=auth_headers)
    assert response.status_code == 200
    body = response.json()
    assert "observability" in body
    assert "database" in body
    assert "live_market" in body
    assert "requests_total" in body["observability"]["http"]
    assert "latency_avg_ms" in body["observability"]["http"]
    assert "latency_ms" in body["database"]
    raw = json.dumps(body)
    assert "axiom_dev_password" not in raw
    assert "authorization" not in raw.lower()


def test_health_ready_include_latency_and_no_secrets(client: TestClient) -> None:
    health = client.get("/health")
    assert health.status_code == 200
    assert "latency_ms" in health.json()

    ready = client.get("/ready")
    assert ready.status_code == 200
    checks = ready.json()["checks"]
    assert checks
    assert all("latency_ms" in check for check in checks)
    assert "axiom_dev_password" not in ready.text
