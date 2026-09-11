"""HTTP integration tests for authenticated ingestion endpoints."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_ingest_sample_and_stats(client: TestClient, auth_headers: dict[str, str]) -> None:
    payload = {
        "sample_name": "eurusd_h1_sample.csv",
        "market_class": "forex",
        "symbol": "EURUSD",
        "timeframe": "H1",
    }
    assert client.post("/api/v1/ingestion/sample", json=payload).status_code == 401

    response = client.post("/api/v1/ingestion/sample", json=payload, headers=auth_headers)
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["status"] == "completed"
    assert body["rows_inserted"] == 5
    run_id = body["run_id"]

    # Dedup
    again = client.post("/api/v1/ingestion/sample", json=payload, headers=auth_headers)
    assert again.status_code == 200
    assert again.json()["rows_unchanged"] == 5
    assert again.json()["rows_inserted"] == 0

    runs = client.get("/api/v1/ingestion/runs", headers=auth_headers)
    assert runs.status_code == 200
    assert any(r["id"] == run_id for r in runs.json())
    started_at = runs.json()[0]["started_at"]
    assert started_at.endswith("+00:00") or started_at.endswith("Z")

    one = client.get(f"/api/v1/ingestion/runs/{run_id}", headers=auth_headers)
    assert one.status_code == 200
    assert one.json()["rows_inserted"] == 5

    stats = client.get("/api/v1/ingestion/stats", headers=auth_headers)
    assert stats.status_code == 200
    assert stats.json()["candle_count_total"] >= 5
    assert stats.json()["total_runs"] >= 2

    counts = client.get(
        "/api/v1/ingestion/candle-counts",
        params={"symbol": "EURUSD", "market_class": "forex"},
        headers=auth_headers,
    )
    assert counts.status_code == 200
    assert counts.json()["count"] >= 5


def test_ingest_sample_missing(client: TestClient, auth_headers: dict[str, str]) -> None:
    response = client.post(
        "/api/v1/ingestion/sample",
        json={
            "sample_name": "nope.csv",
            "market_class": "forex",
            "symbol": "X",
            "timeframe": "H1",
        },
        headers=auth_headers,
    )
    assert response.status_code == 404


def test_ingest_path_traversal_rejected(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    response = client.post(
        "/api/v1/ingestion/csv",
        json={
            "path": "/etc/passwd",
            "market_class": "forex",
            "symbol": "EURUSD",
            "timeframe": "H1",
        },
        headers=auth_headers,
    )
    assert response.status_code == 400


def test_ready_includes_market_ingestion(client: TestClient) -> None:
    response = client.get("/ready")
    assert response.status_code == 200
    names = {c["name"] for c in response.json()["checks"]}
    assert "market_ingestion" in names
