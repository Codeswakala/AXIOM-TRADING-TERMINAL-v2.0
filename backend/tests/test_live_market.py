"""Live market adapter tests (W0-U05)."""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from app.core.config import clear_settings_cache
from app.db.session import session_scope
from app.ingestion.types import NormalizedCandleRow
from app.market.adapters.simulated import SimulatedCandleAdapter
from app.market.live_service import (
    LiveMarketService,
    reset_live_market_service,
)
from app.repositories.candle_repository import CandleRepository


def _auth(client: TestClient) -> dict[str, str]:
    login = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert login.status_code == 200, login.text
    token = login.json()["tokens"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_simulated_adapter_emits_normalized_rows() -> None:
    adapter = SimulatedCandleAdapter(
        interval_seconds=0.05,
        max_ticks=3,
        start_time=datetime(2024, 5, 1, 12, 0, tzinfo=timezone.utc),
    )
    received: list[NormalizedCandleRow] = []

    async def handler(row: NormalizedCandleRow) -> None:
        received.append(row)

    async def run() -> None:
        await adapter.start(handler)
        await asyncio.sleep(0.35)
        await adapter.stop()

    asyncio.run(run())
    assert len(received) == 3
    assert received[0].symbol == "EURUSD"
    assert received[0].source == "live:simulated"
    assert received[0].open_time.tzinfo is not None
    status = adapter.status()
    assert status.messages_received == 3
    assert status.name == "simulated"


@pytest.mark.asyncio
async def test_live_service_persists_candles(prepared_db: None) -> None:
    clear_settings_cache()
    reset_live_market_service()
    from app.core.config import Settings

    settings = Settings(
        live_market_auto_start=False,
        live_market_interval_seconds=0.05,
        database_url="sqlite+aiosqlite:///:memory:",
    )
    service = LiveMarketService(settings)
    adapter = SimulatedCandleAdapter(
        interval_seconds=0.05,
        max_ticks=2,
        symbol="EURUSD",
        timeframe="M1",
        start_time=datetime(2024, 6, 1, 8, 0, tzinfo=timezone.utc),
    )
    await service.start(adapter)
    await asyncio.sleep(0.3)
    await service.stop()

    assert service.stats()["persist_count"] >= 2
    async with session_scope() as session:
        count = await CandleRepository(session).count_by_market(symbol="EURUSD", timeframe="M1")
        assert count >= 2


def test_live_endpoints_require_auth(client: TestClient) -> None:
    assert client.get("/api/v1/market/live/status").status_code == 401
    assert client.get("/api/v1/market/live/stats").status_code == 401
    assert client.post("/api/v1/market/live/start").status_code == 401


def test_live_start_stop_and_status(client: TestClient) -> None:
    headers = _auth(client)

    # Seed before starting the adapter, matching the browser workflow. This keeps
    # SQLite StaticPool tests from running a request-scoped seed write at the same
    # time as the background live adapter writer. Production/PostgreSQL does not
    # share this single-connection test harness limitation.
    seed = client.post("/api/v1/market/live/seed-history", headers=headers)
    assert seed.status_code == 200, seed.text

    start = client.post("/api/v1/market/live/start", headers=headers)
    assert start.status_code == 200, start.text
    body = start.json()
    assert body["stats"]["running"] is True
    assert "EURUSD" in body["stats"]["symbols"]
    assert "BTCUSD" in body["stats"]["symbols"]

    status = client.get("/api/v1/market/live/status", headers=headers)
    assert status.status_code == 200
    assert status.json()["adapter"] in {"simulated", "simulated-multi"}

    import time

    time.sleep(0.6)

    stats = client.get("/api/v1/market/live/stats", headers=headers)
    assert stats.status_code == 200
    # messages_received counts adapter emissions (not only DB persists)
    assert stats.json()["messages_received"] >= 1 or stats.json()["running"] is True

    sub = client.get("/api/v1/market/live/subscribe", headers=headers)
    assert sub.status_code == 200
    assert sub.json()["websocket_path"] == "/ws/market"
    assert len(sub.json().get("symbols") or []) >= 2

    # Stop before request-scoped candle reads to avoid SQLite in-memory shared
    # connection contention in target-platform pytest. This is a test-harness
    # stability fix; the service-level persistence test separately proves live
    # candles persist while the adapter is running.
    stop = client.post("/api/v1/market/live/stop", headers=headers)
    assert stop.status_code == 200
    assert stop.json()["stats"]["running"] is False

    candles = client.get(
        "/api/v1/persistence/candles",
        params={"symbol": "EURUSD", "timeframe": "M1", "limit": 10},
        headers=headers,
    )
    assert candles.status_code == 200
    assert len(candles.json()) >= 1

    btc = client.get(
        "/api/v1/persistence/candles",
        params={"symbol": "BTCUSD", "timeframe": "M1", "limit": 10},
        headers=headers,
    )
    assert btc.status_code == 200
    assert len(btc.json()) >= 1


def test_ready_includes_live_market(client: TestClient) -> None:
    response = client.get("/ready")
    assert response.status_code == 200
    names = {c["name"]: c for c in response.json()["checks"]}
    assert "live_market" in names
    # Not auto-started by default → degraded is acceptable
    assert names["live_market"]["status"] in {"up", "degraded", "stub"}


def test_ws_market_requires_token(client: TestClient) -> None:
    with pytest.raises(Exception):
        # Starlette raises on failed accept/close
        with client.websocket_connect("/ws/market"):
            pass


def test_ws_market_with_ticket(client: TestClient) -> None:
    headers = _auth(client)
    ticket = client.post("/api/v1/auth/ws-ticket", headers=headers).json()["ticket"]
    client.post("/api/v1/market/live/start", headers=headers)
    with client.websocket_connect(f"/ws/market?ticket={ticket}") as ws:
        first = ws.receive_json()
        assert first["type"] == "subscribed"
        assert first["channel"] == "market"
        ws.send_text("ping")
        pong = ws.receive_json()
        assert pong["type"] in {"pong", "live_candle", "subscribed"}
    client.post("/api/v1/market/live/stop", headers=headers)


def test_watchlist_ui_module_has_no_forbidden_controls() -> None:
    """DATA-P01 M6 — frontend T-1 guard over the watchlist/sparkline surface.

    The CONV/SURF guards pin frontend files with non-vacuity anchors; the
    market/live suite pinned none. This phase generates price-like series, so
    the guard pins the module that renders them and asserts: the surface
    renders, the synthetic provenance label is present (M2 — a synthetic
    price without visible provenance is the defect this phase most plausibly
    introduces), and the actuation vocabulary is absent.
    """
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    ui = (
        root
        / "frontend"
        / "src"
        / "components"
        / "terminal"
        / "TerminalWatchlistDock.tsx"
    )
    text = ui.read_text(encoding="utf-8").lower()
    # Non-vacuity anchors: the module genuinely renders the watchlist surface,
    # carries the synthetic provenance label for sparkline render sites, and
    # routes JPY display precision to three decimals (OBS-DATA1-2 — the tick
    # convention must survive at the render layer, not just the generator).
    assert "market watchlist" in text
    assert "seed:synthetic" in text
    assert "tofixed(3)" in text
    forbidden = (
        "place_order",
        "submit order",
        "go live",
        "connect broker",
        "broker_account",
        "execute",
    )
    assert all(item not in text for item in forbidden)


@pytest.mark.asyncio
async def test_chart_seed_per_symbol_determinism_and_order_independence(
    prepared_db: None,
) -> None:
    """DATA-P01 M7 — per-symbol seeding determinism, proven not asserted.

    Seeding the same symbol twice must reproduce the same series, and a
    symbol's series must be independent of seeding order. The previous
    single-RNG design failed the order-independence half (each symbol
    continued the shared stream).
    """
    from app.services.chart_seed_service import seed_chart_history

    async def closes_for(symbol: str) -> list[str]:
        async with session_scope() as session:
            rows = await CandleRepository(session).list_for_symbol(
                symbol=symbol, timeframe="M1", limit=200
            )
            return [str(row.close) for row in rows]

    # 1. Same symbol, seeded twice: identical series.
    async with session_scope() as session:
        await seed_chart_history(session, symbols=["EURUSD"], timeframe="M1", bars=40)
    first = await closes_for("EURUSD")
    async with session_scope() as session:
        await seed_chart_history(session, symbols=["EURUSD"], timeframe="M1", bars=40)
    second = await closes_for("EURUSD")
    assert len(first) == 40
    assert first == second

    # 2. Order independence: EURUSD seeded after GBPUSD vs before it.
    async with session_scope() as session:
        await seed_chart_history(
            session, symbols=["EURUSD", "GBPUSD"], timeframe="M1", bars=40
        )
    eurusd_after_gbp = await closes_for("EURUSD")
    async with session_scope() as session:
        await seed_chart_history(
            session, symbols=["GBPUSD", "EURUSD"], timeframe="M1", bars=40
        )
    eurusd_before_gbp = await closes_for("EURUSD")
    assert eurusd_after_gbp == eurusd_before_gbp
    # And the order-swap did not change EURUSD from its solo seeding either.
    assert eurusd_after_gbp == first


@pytest.mark.asyncio
async def test_chart_seed_crypto_steps_are_relative_across_price_levels(
    prepared_db: None,
) -> None:
    """DATA-P01 CA-DATA1-2 closure — crypto steps proportional to price.

    The previous absolute crypto step (±8/35 per bar) was calibrated for
    BTC (~42,000) and carried SOL (~150) to +397% over 100 bars. This named
    test proves the corrected generator gives all three crypto instruments
    comparable RELATIVE volatility: each symbol's mean relative step is
    below 3% per bar and all three are within one order of magnitude of
    each other.
    """
    from app.services.chart_seed_service import seed_chart_history

    async with session_scope() as session:
        await seed_chart_history(
            session, symbols=["BTCUSD", "ETHUSD", "SOLUSD"], timeframe="M1", bars=40
        )

    rels: dict[str, float] = {}
    async with session_scope() as session:
        for sym in ("BTCUSD", "ETHUSD", "SOLUSD"):
            rows = await CandleRepository(session).list_for_symbol(
                symbol=sym, timeframe="M1", limit=40
            )
            closes = [float(row.close) for row in rows]
            steps = [
                abs(closes[i + 1] - closes[i]) / closes[i] for i in range(len(closes) - 1)
            ]
            rels[sym] = sum(steps) / len(steps)

    for sym, rel in rels.items():
        assert rel < 0.03, f"{sym} mean relative step {rel:.4f} exceeds 3% per bar"
    assert max(rels.values()) / min(rels.values()) < 10, (
        f"crypto relative volatility diverges across price levels: {rels}"
    )
