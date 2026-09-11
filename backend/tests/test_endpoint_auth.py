"""W1-U01 endpoint authorization breadth tests."""

from __future__ import annotations

from fastapi.testclient import TestClient

OPERATIONAL_GETS = [
    ("/system/info", {}),
    ("/api/v1/persistence/stats", {}),
    ("/api/v1/persistence/candles", {"symbol": "EURUSD"}),
    ("/api/v1/persistence/candle-series", {"symbol": "EURUSD", "timeframe": "M1"}),
    ("/api/v1/persistence/indicator-series", {"symbol": "EURUSD", "timeframe": "M1", "indicators": "SMA20"}),
    ("/api/v1/persistence/audit-events", {}),
    ("/api/v1/metrics", {}),
    ("/api/v1/ingestion/runs", {}),
    ("/api/v1/ingestion/candle-counts", {"symbol": "EURUSD"}),
    ("/api/v1/market/live/status", {}),
    ("/api/v1/signals/history", {}),
    ("/api/v1/alerts", {}),
    ("/api/v1/analytics/advisory-performance", {}),
    ("/api/v1/intelligence/correlation-reports", {}),
    ("/api/v1/intelligence/regime-reports", {}),
    ("/api/v1/intelligence/scenario-reports", {}),
    ("/api/v1/intelligence/portfolio-risk-reports", {}),
    ("/api/v1/intelligence/signal-validation-reports", {}),
]


def test_public_probe_endpoints_remain_public(client: TestClient) -> None:
    assert client.get("/health").status_code == 200
    assert client.get("/ready").status_code == 200


def test_operational_get_endpoints_require_bearer(client: TestClient) -> None:
    for path, params in OPERATIONAL_GETS:
        response = client.get(path, params=params)
        assert response.status_code == 401, path


def test_operational_get_endpoints_accept_bearer(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    for path, params in OPERATIONAL_GETS:
        response = client.get(path, params=params, headers=auth_headers)
        assert response.status_code in {200, 404}, path


def test_ingestion_write_requires_bearer(client: TestClient) -> None:
    payload = {
        "sample_name": "eurusd_h1_sample.csv",
        "market_class": "forex",
        "symbol": "EURUSD",
        "timeframe": "H1",
    }
    assert client.post("/api/v1/ingestion/sample", json=payload).status_code == 401
