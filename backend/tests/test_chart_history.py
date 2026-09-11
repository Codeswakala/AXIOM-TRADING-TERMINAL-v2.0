"""Chart history API ordering + seed history (W0-U07/W1-U01 auth breadth)."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_seed_history_and_order_asc(client: TestClient, auth_headers: dict[str, str]) -> None:
    seed = client.post("/api/v1/market/live/seed-history", headers=auth_headers)
    assert seed.status_code == 200, seed.text
    body = seed.json()
    assert body["status"] == "ok"
    assert body["seeded"]["EURUSD"] >= 20 or body["seeded"]["EURUSD"] == 0

    assert (
        client.get(
            "/api/v1/persistence/candles",
            params={"symbol": "EURUSD", "timeframe": "M1", "limit": 100, "order": "asc"},
        ).status_code
        == 401
    )

    for sym in ("EURUSD", "BTCUSD"):
        asc = client.get(
            "/api/v1/persistence/candles",
            params={"symbol": sym, "timeframe": "M1", "limit": 100, "order": "asc"},
            headers=auth_headers,
        )
        assert asc.status_code == 200
        rows = asc.json()
        assert len(rows) >= 20
        times = [r["open_time"] for r in rows]
        assert times == sorted(times)
        assert all(t.endswith("+00:00") or t.endswith("Z") for t in times)


def test_seed_history_requires_auth(client: TestClient) -> None:
    assert client.post("/api/v1/market/live/seed-history").status_code == 401


def test_seed_chart_history_non_degenerate_walk(client: TestClient, auth_headers: dict[str, str]) -> None:
    """Verify seeded synthetic chart history exercises real OHLC geometry (CA-P03-3)."""
    seed = client.post("/api/v1/market/live/seed-history", headers=auth_headers)
    assert seed.status_code == 200, seed.text

    for sym in ("EURUSD", "BTCUSD"):
        resp = client.get(
            "/api/v1/persistence/candles",
            params={"symbol": sym, "timeframe": "M1", "limit": 80, "order": "asc"},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        rows = resp.json()
        assert len(rows) >= 20

        # Verify varying body heights across the series
        body_sizes = [abs(float(r["close"]) - float(r["open"])) for r in rows]
        unique_body_sizes = set(round(b, 6) for b in body_sizes)
        assert len(unique_body_sizes) >= 5, f"Expected varied body sizes for {sym}, got {unique_body_sizes}"

        # Verify highs and lows are not at constant fixed offsets (dynamic wicks)
        upper_wicks = [float(r["high"]) - max(float(r["open"]), float(r["close"])) for r in rows]
        lower_wicks = [min(float(r["open"]), float(r["close"])) - float(r["low"]) for r in rows]
        unique_upper_wicks = set(round(w, 6) for w in upper_wicks)
        unique_lower_wicks = set(round(w, 6) for w in lower_wicks)
        assert len(unique_upper_wicks) >= 5, f"Expected dynamic upper wicks for {sym}"
        assert len(unique_lower_wicks) >= 5, f"Expected dynamic lower wicks for {sym}"

        # Verify volume variation
        volumes = [float(r["volume"]) for r in rows if r.get("volume") is not None]
        assert len(set(volumes)) >= 5, f"Expected dynamic volumes for {sym}"

        # Verify non-authoritative source tagging (T-6)
        assert all(r["source"] == "seed:synthetic" for r in rows)

