"""CHART-P01 fail-first tests: server-side indicator computation (F-CHART-1 fix).

Every test here MUST fail against the pre-CHART-P01 tree (no indicator
service, no registry, no indicator endpoint) and pass once the implementation
ships. M2 requires hand-computable fixtures — each expected value below can be
verified by inspection.

Formulae pinned by these tests:
  SMA(n)   — arithmetic mean of the last n closes.
  EMA(n)   — alpha = 2/(n+1), seeded with the SMA of the first n closes.
  RSI(n)   — Wilder's smoothing (first avgGain/avgLoss = plain mean of the
             first n changes; thereafter (prev*(n-1) + change)/n).
  MACD     — EMA12 - EMA26; signal = EMA9 of the MACD line (SMA-seeded);
             histogram = MACD - signal.
  Bollinger(20,2) — SMA +- 2 * POPULATION standard deviation.
  ATR(n)   — true range (max(H-L, |H-prevC|, |L-prevC|)) with Wilder's
             smoothing.
"""

from __future__ import annotations

import math
from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.db.models.candle import Candle
from app.db.session import session_scope
from app.services.indicator_registry import INDICATOR_REGISTRY
from app.services.indicators import (
    atr,
    bollinger,
    ema,
    macd,
    rsi,
    sma,
)

EPS = 1e-9


def _bars(closes: list[float], highs: list[float] | None = None, lows: list[float] | None = None) -> list[dict]:
    """Minimal bar records aligned to a UTC minute grid."""
    base = datetime(2026, 8, 17, 9, 0, tzinfo=timezone.utc)
    highs = highs if highs is not None else [c + 0.5 for c in closes]
    lows = lows if lows is not None else [c - 0.5 for c in closes]
    return [
        {
            "open_time": base + timedelta(minutes=i),
            "open": closes[i],
            "high": highs[i],
            "low": lows[i],
            "close": closes[i],
        }
        for i in range(len(closes))
    ]


# --- SMA -------------------------------------------------------------------

def test_chart_p01_sma_matches_hand_computed_values() -> None:
    bars = _bars([1.0, 2.0, 3.0, 4.0, 5.0])
    out = sma(bars, n=3)
    assert out.kind == "computed"
    values = [None if p.value is None else float(p.value) for p in out.points]
    assert values == [None, None, 2.0, 3.0, 4.0]
    assert len(out.points) == 5


# --- EMA -------------------------------------------------------------------

def test_chart_p01_ema_seeding_rule_and_alpha_correct() -> None:
    bars = _bars([1.0, 2.0, 3.0, 4.0, 5.0])
    out = ema(bars, n=3)
    assert out.kind == "computed"
    # alpha = 2/(3+1) = 0.5; SMA-seeded at index 2 with (1+2+3)/3 = 2.
    # EMA(4) = 2 + 0.5*(4-2) = 3 ; EMA(5) = 3 + 0.5*(5-3) = 4.
    values = [None if p.value is None else float(p.value) for p in out.points]
    assert values == [None, None, 2.0, 3.0, 4.0]
    # Seeding rule is SMA-based: the first emitted value equals the SMA of the
    # first n closes — asserted here so a silent switch to first-value seeding
    # fails.
    assert abs(values[2] - 2.0) < EPS


# --- RSI (Wilder) ----------------------------------------------------------

def test_chart_p01_rsi_wilder_smoothing_matches_reference() -> None:
    # 14 consecutive +1 gains -> avgGain=1, avgLoss=0 -> RSI=100 at index 14.
    closes = [float(i) for i in range(15)]  # 0..14, every delta +1
    bars = _bars(closes)
    out = rsi(bars, n=14)
    assert out.kind == "computed"
    assert out.points[13].value is None  # index 13: not enough deltas yet
    assert float(out.points[14].value) == 100.0  # first RSI value

    # Bar 15 drops by 14: avgGain=(13*1+0)/14=13/14, avgLoss=(13*0+14)/14=1,
    # RS=13/14, RSI = 100 - 100/(1+13/14) = 100 - 1400/27 = 48.148...
    closes.append(0.0)
    bars = _bars(closes)
    out = rsi(bars, n=14)
    expected = 100.0 - 100.0 / (1.0 + 13.0 / 14.0)
    assert abs(float(out.points[15].value) - expected) < 1e-6
    assert abs(expected - 48.14814814814815) < 1e-9  # hand-computed reference


# --- MACD ------------------------------------------------------------------

def test_chart_p01_macd_line_signal_histogram_correct() -> None:
    # 26 closes at 1000 (indices 0..25): EMA12 and EMA26 both seed at 1000.
    # Bar 26 closes at 1351 (delta = 351 = 27*13):
    #   EMA12 = 1000 + (2/13)*351 = 1054 ; EMA26 = 1000 + (2/27)*351 = 1026
    #   MACD(26) = 28 exactly.
    closes = [1000.0] * 26 + [1351.0]
    bars = _bars(closes)
    out = macd(bars)
    assert out.kind == "computed"
    p26 = out.points[26]
    assert p26.macd is not None
    assert abs(float(p26.macd) - 28.0) < EPS
    # Signal (EMA9 of MACD) needs 9 MACD values — null until then; the
    # histogram inherits the signal's absence, never 0 presented as real.
    assert p26.signal is None
    assert p26.histogram is None
    # Structural invariants on every defined point:
    for p in out.points:
        if p.signal is not None:
            assert p.histogram is not None
            assert abs(float(p.histogram) - (float(p.macd) - float(p.signal))) < 1e-6
    # MACD is undefined before EMA26 seeds (25 bars needed for the first
    # value at index 25).
    assert all(p.macd is None for p in out.points[:25])
    assert out.points[25].macd is not None


# --- Bollinger -------------------------------------------------------------

def test_chart_p01_bollinger_bands_two_sigma_correct() -> None:
    # Closes 1..20: mean = 10.5; population variance = sum((i-10.5)^2)/20
    # = 2*(0.5^2+1.5^2+...+9.5^2)/20 = 2*332.5/20 = 33.25; sigma = sqrt(33.25).
    closes = [float(i) for i in range(1, 21)]
    bars = _bars(closes)
    out = bollinger(bars, n=20, multiplier=2.0)
    assert out.kind == "computed"
    last = out.points[19]
    assert last.middle is not None and last.upper is not None and last.lower is not None
    assert abs(float(last.middle) - 10.5) < EPS
    sigma = math.sqrt(33.25)
    assert abs(float(last.upper) - (10.5 + 2 * sigma)) < 1e-9
    assert abs(float(last.lower) - (10.5 - 2 * sigma)) < 1e-9
    # All earlier points undefined (window not yet full).
    assert all(p.middle is None for p in out.points[:19])


# --- ATR -------------------------------------------------------------------

def test_chart_p01_atr_true_range_wilder_correct() -> None:
    # Bars 0..14: H-L=1, close at the high, previous close 1 below the next
    # high -> TR = 1 for the first 14 true ranges. Bar 15: H-L=15 -> TR=15.
    highs: list[float] = []
    lows: list[float] = []
    closes: list[float] = []
    for i in range(15):
        highs.append(100.0 + i)
        lows.append(99.0 + i)
        closes.append(100.0 + i)
    highs.append(115.0)
    lows.append(100.0)
    closes.append(100.0)
    bars = _bars(closes, highs=highs, lows=lows)
    out = atr(bars, n=14)
    assert out.kind == "computed"
    # First ATR at index 14 = mean of the first 14 TRs = 1.0.
    assert float(out.points[14].value) == 1.0
    # Wilder recursion at index 15: (13*1 + 15)/14 = 2.0 exactly.
    assert float(out.points[15].value) == 2.0
    assert out.points[13].value is None


# --- M4 insufficient -------------------------------------------------------

def test_chart_p01_insufficient_history_returns_typed_kind_not_padded_value() -> None:
    bars = _bars([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])  # 6 bars
    out = sma(bars, n=50)
    assert out.kind == "insufficient"
    assert out.required == 50
    assert out.available == 6
    assert out.points == []
    # Same discipline for every indicator type.
    assert atr(bars, n=14).kind == "insufficient"
    assert bollinger(bars, n=20, multiplier=2.0).kind == "insufficient"
    assert rsi(bars, n=14).kind == "insufficient"
    assert ema(bars, n=20).kind == "insufficient"
    assert macd(bars).kind == "insufficient"


# --- M7 determinism --------------------------------------------------------

def test_chart_p01_indicator_deterministic_and_order_independent() -> None:
    bars = _bars([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])
    shuffled = list(reversed(bars))

    def fingerprint(out) -> list:
        return [
            (p.time.isoformat(), None if p.value is None else str(p.value))
            for p in out.points
        ]

    f1 = fingerprint(sma(bars, n=3))
    f2 = fingerprint(sma(shuffled, n=3))
    f3 = fingerprint(sma(bars, n=3))
    assert f1 == f2 == f3
    assert len([v for _, v in f1 if v is not None]) == 8


# --- Registry (S1) ---------------------------------------------------------

def test_chart_p01_indicator_registry_golden_table() -> None:
    # CHART-P02/P03 extend the registry (29 entries); the CHART-P01 seven
    # keep their exact positions and properties — the phase-1 contract is
    # not weakened, only widened.
    assert list(INDICATOR_REGISTRY)[:7] == [
        "SMA20",
        "SMA50",
        "EMA20",
        "RSI14",
        "MACD12269",
        "BBANDS201",
        "ATR14",
    ]
    assert len(INDICATOR_REGISTRY) == 29
    assert INDICATOR_REGISTRY["SMA20"].label == "SMA 20"
    assert INDICATOR_REGISTRY["SMA20"].pane == "overlay"
    assert INDICATOR_REGISTRY["SMA20"].required_bars == 20
    assert INDICATOR_REGISTRY["SMA50"].required_bars == 50
    assert INDICATOR_REGISTRY["EMA20"].required_bars == 20
    assert INDICATOR_REGISTRY["RSI14"].pane == "pane"
    assert INDICATOR_REGISTRY["RSI14"].required_bars == 15
    assert INDICATOR_REGISTRY["MACD12269"].pane == "pane"
    assert INDICATOR_REGISTRY["MACD12269"].required_bars == 34
    assert INDICATOR_REGISTRY["BBANDS201"].pane == "overlay"
    assert INDICATOR_REGISTRY["BBANDS201"].required_bars == 20
    assert INDICATOR_REGISTRY["ATR14"].pane == "pane"
    assert INDICATOR_REGISTRY["ATR14"].required_bars == 15


# --- Endpoint --------------------------------------------------------------

def test_chart_p01_indicator_endpoint_requires_auth(client: TestClient) -> None:
    assert (
        client.get(
            "/api/v1/persistence/indicator-series",
            params={"symbol": "EURUSD", "timeframe": "M1", "indicators": "SMA20"},
        ).status_code
        == 401
    )


def test_chart_p01_indicator_endpoint_rejects_unknown_indicator(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    resp = client.get(
        "/api/v1/persistence/indicator-series",
        params={"symbol": "EURUSD", "timeframe": "M1", "indicators": "SMA20,VWAP"},
        headers=auth_headers,
    )
    assert resp.status_code == 422


def test_chart_p01_indicator_endpoint_computed_over_seeded_series(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    seed = client.post("/api/v1/market/live/seed-history", headers=auth_headers)
    assert seed.status_code == 200
    resp = client.get(
        "/api/v1/persistence/indicator-series",
        params={"symbol": "EURUSD", "timeframe": "M1", "indicators": "SMA20,SMA50"},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["seriesKind"] == "native"
    assert body["indicators"]["SMA20"]["shape"] == "line"
    assert body["indicators"]["SMA20"]["kind"] == "computed"
    assert len(body["indicators"]["SMA20"]["points"]) >= 80
    assert body["indicators"]["SMA50"]["shape"] == "line"
    assert body["indicators"]["SMA50"]["kind"] == "computed"
    # Determinism at the wire level: repeat call → identical points.
    again = client.get(
        "/api/v1/persistence/indicator-series",
        params={"symbol": "EURUSD", "timeframe": "M1", "indicators": "SMA20"},
        headers=auth_headers,
    ).json()
    assert again["indicators"]["SMA20"]["points"] == body["indicators"]["SMA20"]["points"]


async def test_chart_p01_indicator_endpoint_insufficient_and_unavailable(
    prepared_db: None, async_client: AsyncClient
) -> None:
    """Typed states over the wire: insufficient over a short controlled window,
    unavailable when the underlying series does not exist."""
    base = datetime(2026, 1, 5, 0, 0, tzinfo=timezone.utc)
    rows: list[Candle] = []
    for minute in range(6):
        rows.append(
            Candle(
                market_class="forex",
                symbol="SHORT1M",
                timeframe="M1",
                open_time=base + timedelta(minutes=minute),
                open=1.0,
                high=1.5,
                low=0.5,
                close=1.1,
                volume=None,
                source="seed:synthetic",
            )
        )
    async with session_scope() as session:
        session.add_all(rows)
        await session.commit()

    login = await async_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert login.status_code == 200, login.text
    headers = {"Authorization": f"Bearer {login.json()['tokens']['access_token']}"}

    insufficient = await async_client.get(
        "/api/v1/persistence/indicator-series",
        params={"symbol": "SHORT1M", "timeframe": "M1", "indicators": "SMA50"},
        headers=headers,
    )
    assert insufficient.status_code == 200
    ins_body = insufficient.json()
    assert ins_body["seriesKind"] == "native"
    assert ins_body["indicators"]["SMA50"]["shape"] == "insufficient"
    assert ins_body["indicators"]["SMA50"]["required"] == 50
    assert ins_body["indicators"]["SMA50"]["available"] == 6

    unavailable = await async_client.get(
        "/api/v1/persistence/indicator-series",
        params={"symbol": "NOPEZZZ", "timeframe": "H1", "indicators": "SMA20"},
        headers=headers,
    )
    assert unavailable.status_code == 200
    unav_body = unavailable.json()
    assert unav_body["seriesKind"] == "unavailable"
    assert unav_body["indicators"] == {}
    assert unav_body["detail"]
