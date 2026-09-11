"""HTTP integration tests for authenticated persistence endpoints."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi.testclient import TestClient


def test_persistence_candle_lifecycle(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    payload = {
        "market_class": "forex",
        "symbol": "EURUSD",
        "timeframe": "H1",
        "open_time": datetime(2024, 6, 1, 10, 0, tzinfo=timezone.utc).isoformat(),
        "open": "1.0800",
        "high": "1.0850",
        "low": "1.0780",
        "close": "1.0825",
        "volume": "1500",
        "source": "test",
    }
    assert client.post("/api/v1/persistence/candles", json=payload).status_code == 401

    create = client.post("/api/v1/persistence/candles", json=payload, headers=auth_headers)
    assert create.status_code == 201, create.text
    body = create.json()
    assert body["symbol"] == "EURUSD"
    assert body["open_time"].endswith("+00:00") or body["open_time"].endswith("Z")
    candle_id = body["id"]

    listed = client.get(
        "/api/v1/persistence/candles",
        params={"symbol": "EURUSD"},
        headers=auth_headers,
    )
    assert listed.status_code == 200
    assert any(item["id"] == candle_id for item in listed.json())

    fetched = client.get(f"/api/v1/persistence/candles/{candle_id}", headers=auth_headers)
    assert fetched.status_code == 200
    fetched_body = fetched.json()
    assert fetched_body["close"] == "1.0825000000" or fetched_body["close"].startswith(
        "1.0825"
    )
    assert fetched_body["open_time"].endswith("+00:00") or fetched_body["open_time"].endswith("Z")

    audits = client.get("/api/v1/persistence/audit-events", headers=auth_headers)
    assert audits.status_code == 200
    assert any(a["action"] == "candle.create" for a in audits.json())

    stats = client.get("/api/v1/persistence/stats", headers=auth_headers)
    assert stats.status_code == 200
    stats_body = stats.json()
    assert stats_body["backend"] in {"sqlite", "postgresql"}
    assert stats_body["candle_count"] >= 1
    assert stats_body["audit_count"] >= 1


def test_ready_database_not_stub(client: TestClient) -> None:
    response = client.get("/ready")
    db = next(c for c in response.json()["checks"] if c["name"] == "database")
    assert db["status"] != "stub"
