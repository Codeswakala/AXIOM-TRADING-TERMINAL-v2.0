"""CHART-P02 fail-first tests: indicator breadth (16 new) + full-definition
required_bars + the scaling contracts.

Every test here MUST fail against the pre-CHART-P02 tree (the new functions,
registry entries and the engine field do not exist) and pass once the phase
ships. Every numeric fixture below is verifiable by inspection; conventions
are declared in the test docstrings exactly as the implementation states them.
"""

from __future__ import annotations

import math
from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient

from app.services.indicator_registry import INDICATOR_REGISTRY
from app.services.indicators import (
    adx_dmi,
    camarilla,
    cci,
    donchian,
    hma,
    ichimoku,
    keltner,
    linear_regression,
    percentile_rank,
    pivot_points,
    prev_day_levels,
    roc,
    session_levels,
    stochastic,
    supertrend,
    zscore,
)
from app.services.timeframes import TIMEFRAME_MINUTES

EPS = 1e-9


def _bars(closes: list[float], highs: list[float] | None = None, lows: list[float] | None = None, start: datetime | None = None) -> list[dict]:
    base = start or datetime(2026, 8, 17, 9, 0, tzinfo=timezone.utc)
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


def _line_values(out, name: str | None = None) -> list[float | None]:
    pts = out.points if name is None else (out.lines or {})[name]
    return [None if p.value is None else float(p.value) for p in pts]


# --- HMA -------------------------------------------------------------------

def test_chart_p02_hma_matches_hand_computed_values() -> None:
    # Convention declared: WMA weights 1..k; HMA = WMA(2*WMA(n/2) - WMA(n)) over
    # floor(sqrt(n)); for n=4: n/2=2, sqrt window 2.
    # closes 1..8 -> HMA(4) = [None,None,None,None, 5,6,7,8] (linear ramp:
    # WMA(2) lags 1/3, WMA(4) symmetric no lag -> raw = i+4/3 -> HMA = i+1).
    bars = _bars([float(i) for i in range(1, 9)])
    out = hma(bars, n=4)
    assert out.kind == "computed"
    values = _line_values(out)
    assert values == [None, None, None, None, 5.0, 6.0, 7.0, 8.0]


# --- Supertrend ------------------------------------------------------------

def test_chart_p02_supertrend_matches_hand_computed_values() -> None:
    # Convention declared: basic bands = (H+L)/2 +- mult*ATR(n) with ATR
    # Wilder-smoothed; band-locking rule (basic upper < prev final upper OR
    # prev close > prev final upper -> adopt basic, else hold). Output is the
    # two band lines ONLY — no trend verdict is emitted.
    n = 20
    mids: list[float] = []
    highs: list[float] = []
    lows: list[float] = []
    closes: list[float] = []
    for i in range(n):
        mids.append(100.0 + i)
        highs.append(100.0 + i + 2.0)  # H-L = 4, TR = 4 constant
        lows.append(100.0 + i - 2.0)
        closes.append(100.0 + i)
    # one extra bar continuing the pattern (flat TR series)
    mids.append(100.0 + n)
    highs.append(100.0 + n + 2.0)
    lows.append(100.0 + n - 2.0)
    closes.append(100.0 + n)
    bars = _bars(closes, highs=highs, lows=lows)
    out = supertrend(bars, n=10, multiplier=3.0)
    assert out.kind == "computed"
    upper = _line_values(out, "supertrend_upper")
    lower = _line_values(out, "supertrend_lower")
    # ATR(10) = 4 exactly; first band at bar 10 (mid 110) = 110 +- 12.
    # Band-locking: price rises steadily and never crosses the FINAL upper
    # band, so the upper band stays LOCKED at 122 (first computed value)
    # while the lower band follows the basic band up to 120-12 = 108.
    assert abs(upper[10] - 122.0) < EPS
    assert abs(upper[-1] - 122.0) < EPS  # locked — price never crossed it
    assert abs(lower[-1] - 108.0) < EPS  # follows the rising basic band
    assert upper[9] is None and lower[9] is None  # ATR needs 10 TRs
    assert set((out.lines or {}).keys()) == {"supertrend_upper", "supertrend_lower"}


# --- Ichimoku --------------------------------------------------------------

def test_chart_p02_ichimoku_matches_hand_computed_values() -> None:
    # Convention declared: (9,26,52); senkou A/B computed at bar i are plotted
    # at bar i+26; chikou (close i) plotted at bar i-26. NO point is plotted
    # beyond the last bar — the cloud ends at the last bar (the final 26
    # cloud values are the live projection, plotted at existing positions).
    # Full definition: 52 + 26 = 78 bars.
    closes = [float(i) for i in range(1, 79)]  # 1..78
    bars = _bars(closes)
    out = ichimoku(bars)
    assert out.kind == "computed"
    lines = out.lines
    assert set(lines.keys()) == {"tenkan", "kijun", "senkou_a", "senkou_b", "chikou"}

    tenkan = _line_values(out, "tenkan")
    kijun = _line_values(out, "kijun")
    senkou_a = _line_values(out, "senkou_a")
    senkou_b = _line_values(out, "senkou_b")
    chikou = _line_values(out, "chikou")

    # tenkan(8) = (9+1)/2 = 5 ; kijun(25) = (26+1)/2 = 13.5
    assert abs(tenkan[8] - 5.0) < EPS
    assert abs(kijun[25] - 13.5) < EPS
    # senkou_b(51) = (52+1)/2 = 26.5, plotted at bar 77
    assert abs(senkou_b[77] - 26.5) < EPS
    assert senkou_b[25] is None  # nothing before the first computed span
    # senkou_a(51) = (tenkan51 + kijun51)/2 = (48 + 39.5)/2 = 43.75 at bar 77
    assert abs(senkou_a[77] - 43.75) < EPS
    # chikou: last plotted point is at bar 51 with value close[77] = 78
    assert abs(chikou[51] - 78.0) < EPS
    assert chikou[52] is None
    # Multi-line indicators carry their points in `lines`; each line spans
    # the full bar window.
    assert len(tenkan) == 78 and len(senkou_a) == 78 and len(chikou) == 78


# --- Stochastic ------------------------------------------------------------

def test_chart_p02_stochastic_matches_hand_computed_values() -> None:
    # Convention declared: SLOW stochastic (14,3,3): raw %K = (C-LL14)/(HH14-LL14)*100,
    # %K = SMA3(raw), %D = SMA3(%K).
    closes = [float(i) for i in range(18)]
    highs = [float(i + 5) for i in range(18)]
    lows = [float(i - 5) for i in range(18)]
    bars = _bars(closes, highs=highs, lows=lows)
    out = stochastic(bars, k_period=14, smooth_k=3, smooth_d=3)
    assert out.kind == "computed"
    pct_k = _line_values(out, "percent_k")
    pct_d = _line_values(out, "percent_d")
    # Window HH=i+5, LL=i-18 -> raw %K = 18/23*100 = 78.260869... constant.
    expected = 18.0 / 23.0 * 100.0
    assert pct_k[15] is not None and abs(pct_k[15] - expected) < 1e-6
    assert pct_d[17] is not None and abs(pct_d[17] - expected) < 1e-6
    assert pct_d[16] is None  # %D not yet seeded
    assert pct_k[13] is None  # raw %K not yet defined


# --- CCI -------------------------------------------------------------------

def test_chart_p02_cci_matches_hand_computed_values() -> None:
    # Convention declared: CCI = (TP - SMA20(TP)) / (0.015 * mean absolute
    # deviation of TP) — MAD, not standard deviation.
    closes = [float(i) for i in range(1, 21)]  # TP = close (H=L=C)
    bars = _bars(closes, highs=list(closes), lows=list(closes))
    out = cci(bars, n=20)
    assert out.kind == "computed"
    values = _line_values(out)
    # mean 10.5, MAD = 5.0 -> CCI = 9.5 / 0.075 = 126.666...
    assert abs(values[-1] - 126.66666666666667) < 1e-6
    assert values[18] is None


# --- ROC -------------------------------------------------------------------

def test_chart_p02_roc_matches_hand_computed_values() -> None:
    # Convention declared: ROC(n) = (close - close[n bars ago]) / close[n bars
    # ago] * 100.
    closes = [float(i) for i in range(1, 14)]  # 1..13
    bars = _bars(closes)
    out = roc(bars, n=12)
    values = _line_values(out)
    assert abs(values[12] - 1200.0) < 1e-6  # (13-1)/1*100
    assert values[11] is None


# --- ADX/DMI ---------------------------------------------------------------

def test_chart_p02_adx_dmi_matches_hand_computed_values() -> None:
    # Convention declared: Wilder smoothing for +DM/-DM/TR; DX = 100*|+DI - -DI|/(+DI + -DI);
    # ADX = Wilder average of DX. Full definition 2n bars: the first ADX needs
    # n DX values and DX starts at bar n+1 -> ADX first defined at bar 2n.
    # Every bar shifts up by 1 (close = 100+i, H = C+2, L = C-2):
    # +DM = 1, -DM = 0 (down move is negative -> zeroed), TR = 4 constant.
    # -> +DI = 100*1/4 = 25, -DI = 0, DX = 100, ADX = 100.
    n = 28
    closes = [float(100 + i) for i in range(n)]
    highs = [float(102 + i) for i in range(n)]
    lows = [float(98 + i) for i in range(n)]
    bars = _bars(closes, highs=highs, lows=lows)
    out = adx_dmi(bars, n=14)
    assert out.kind == "computed"
    plus_di = _line_values(out, "plus_di")
    minus_di = _line_values(out, "minus_di")
    adx_line = _line_values(out, "adx")
    assert abs(plus_di[27] - 25.0) < EPS
    assert abs(minus_di[27] - 0.0) < EPS
    assert abs(adx_line[27] - 100.0) < EPS
    assert adx_line[26] is None  # full definition: ADX seeded only at 2n
    assert abs(plus_di[14] - 25.0) < EPS  # DI defined earlier (bar n+1)


# --- Keltner ---------------------------------------------------------------

def test_chart_p02_keltner_matches_hand_computed_values() -> None:
    # Convention declared: EMA centre (SMA-seeded), channel = centre +- 2*ATR(10).
    closes = [float(i) for i in range(1, 21)]
    highs = [float(i + 1) for i in range(1, 21)]
    lows = [float(i - 1) for i in range(1, 21)]
    bars = _bars(closes, highs=highs, lows=lows)
    out = keltner(bars, ema_period=20, atr_period=10, multiplier=2.0)
    assert out.kind == "computed"
    upper = _line_values(out, "upper")
    middle = _line_values(out, "middle")
    lower = _line_values(out, "lower")
    # TR constant = 2 -> ATR10 = 2; EMA20 seed at bar 19 = SMA = 10.5.
    assert abs(middle[19] - 10.5) < EPS
    assert abs(upper[19] - 14.5) < EPS
    assert abs(lower[19] - 6.5) < EPS
    assert middle[18] is None


# --- Donchian --------------------------------------------------------------

def test_chart_p02_donchian_matches_hand_computed_values() -> None:
    closes = [float(i) for i in range(1, 21)]
    highs = [float(i + 5) for i in range(1, 21)]
    lows = [float(i - 5) for i in range(1, 21)]
    bars = _bars(closes, highs=highs, lows=lows)
    out = donchian(bars, n=20)
    upper = _line_values(out, "upper")
    middle = _line_values(out, "middle")
    lower = _line_values(out, "lower")
    assert abs(upper[19] - 25.0) < EPS
    assert abs(lower[19] - -4.0) < EPS
    assert abs(middle[19] - 10.5) < EPS
    assert upper[18] is None


# --- Pivots / Camarilla / Previous H/L -------------------------------------

def _two_day_bars() -> tuple[list[dict], datetime]:
    """Day A (UTC) with H=110, L=90, C=105; day B with three bars."""
    day_a = datetime(2026, 8, 17, 10, 0, tzinfo=timezone.utc)
    bars = [
        {"open_time": day_a + timedelta(minutes=m), "open": 100.0, "high": 110.0, "low": 90.0, "close": 105.0}
        for m in range(3)
    ]
    day_b = day_a + timedelta(days=1)
    for m, close in enumerate([101.0, 102.0, 103.0]):
        bars.append({"open_time": day_b + timedelta(minutes=m), "open": close, "high": close + 1, "low": close - 1, "close": close})
    return bars, day_b


def test_chart_p02_pivot_points_matches_hand_computed_values() -> None:
    # Convention declared: classic pivots from the PRIOR UTC day's H/L/C;
    # P=(H+L+C)/3; R1=2P-L; S1=2P-H; R2=P+(H-L); S2=P-(H-L); R3=H+2(P-L); S3=L-2(H-P).
    bars, _ = _two_day_bars()
    out = pivot_points(bars, tf_minutes=1440)
    lines = out.lines
    p = 305.0 / 3.0
    assert abs(_line_values(out, "P")[-1] - p) < 1e-6
    assert abs(_line_values(out, "R1")[-1] - (2 * p - 90.0)) < 1e-6
    assert abs(_line_values(out, "S1")[-1] - (2 * p - 110.0)) < 1e-6
    assert abs(_line_values(out, "R2")[-1] - (p + 20.0)) < 1e-6
    assert abs(_line_values(out, "S2")[-1] - (p - 20.0)) < 1e-6
    assert abs(_line_values(out, "R3")[-1] - (110.0 + 2 * (p - 90.0))) < 1e-6
    assert abs(_line_values(out, "S3")[-1] - (90.0 - 2 * (110.0 - p))) < 1e-6
    assert set(lines.keys()) == {"P", "R1", "S1", "R2", "S2", "R3", "S3"}


def test_chart_p02_camarilla_matches_hand_computed_values() -> None:
    # Convention declared: classic Camarilla from the prior UTC day's H/L/C:
    # R1=C+(H-L)*1.1/12; R2=C+(H-L)*1.1/6; R3=C+(H-L)*1.1/4; R4=C+(H-L)*1.1/2;
    # S1=C-(H-L)*1.1/12; S2=C-(H-L)*1.1/6; S3=C-(H-L)*1.1/4; S4=C-(H-L)*1.1/2.
    bars, _ = _two_day_bars()
    out = camarilla(bars, tf_minutes=1440)
    rng = 20.0 * 1.1
    assert abs(_line_values(out, "R1")[-1] - (105.0 + rng / 12)) < 1e-6
    assert abs(_line_values(out, "R2")[-1] - (105.0 + rng / 6)) < 1e-6
    assert abs(_line_values(out, "R3")[-1] - (105.0 + rng / 4)) < 1e-6
    assert abs(_line_values(out, "R4")[-1] - (105.0 + rng / 2)) < 1e-6
    assert abs(_line_values(out, "S1")[-1] - (105.0 - rng / 12)) < 1e-6
    assert abs(_line_values(out, "S2")[-1] - (105.0 - rng / 6)) < 1e-6
    assert abs(_line_values(out, "S3")[-1] - (105.0 - rng / 4)) < 1e-6
    assert abs(_line_values(out, "S4")[-1] - (105.0 - rng / 2)) < 1e-6


def test_chart_p02_prev_day_levels_matches_hand_computed_values() -> None:
    bars, _ = _two_day_bars()
    out = prev_day_levels(bars, tf_minutes=1440)
    assert abs(_line_values(out, "prev_high")[-1] - 110.0) < EPS
    assert abs(_line_values(out, "prev_low")[-1] - 90.0) < EPS


# --- Session levels --------------------------------------------------------

def test_chart_p02_session_levels_matches_hand_computed_values() -> None:
    # Convention declared: LONDON 07:00-16:00 UTC and NEW YORK 12:00-21:00 UTC
    # (fixed windows, weekend-closed — mirrors the frontend session context);
    # the level shown for session S is the MOST RECENT COMPLETED S's H/L.
    monday = datetime(2026, 8, 17, 7, 0, tzinfo=timezone.utc)  # Monday
    bars = []
    # Monday London session, 9 hourly bars (07:00-15:00 UTC), H=100, L=80 —
    # the session is COMPLETE once its window ends at 16:00.
    for m in range(9):
        t = monday + timedelta(minutes=m * 60)
        bars.append({"open_time": t, "open": 90.0, "high": 100.0, "low": 80.0, "close": 90.0})
    # Tuesday (same UTC time) bar: levels must show Monday's 100/80.
    tuesday = monday + timedelta(days=1)
    bars.append({"open_time": tuesday, "open": 95.0, "high": 96.0, "low": 94.0, "close": 95.0})
    out = session_levels(bars, tf_minutes=60)
    assert out.kind == "computed"
    assert abs(_line_values(out, "london_high")[-1] - 100.0) < EPS
    assert abs(_line_values(out, "london_low")[-1] - 80.0) < EPS
    assert set((out.lines or {}).keys()) == {"london_high", "london_low", "newyork_high", "newyork_low"}


# --- Statistics ------------------------------------------------------------

def test_chart_p02_zscore_matches_hand_computed_values() -> None:
    # Convention declared: population standard deviation (matching Bollinger).
    closes = [float(i) for i in range(1, 21)]
    bars = _bars(closes)
    out = zscore(bars, n=20)
    values = _line_values(out)
    sigma = math.sqrt(33.25)
    assert abs(values[19] - (9.5 / sigma)) < 1e-9
    assert values[18] is None


def test_chart_p02_percentile_rank_matches_hand_computed_values() -> None:
    # Convention declared: MIDPOINT percentile rank within the last n closes:
    # (count_less + 0.5*count_equal)/n * 100.
    closes = [float(i) for i in range(1, 21)]
    bars = _bars(closes)
    out = percentile_rank(bars, n=20)
    values = _line_values(out)
    assert abs(values[19] - 97.5) < 1e-9  # 19 below, 1 equal
    # tie case: current 10 within 1..19 + 10
    closes2 = [float(i) for i in range(1, 20)] + [10.0]
    out2 = percentile_rank(_bars(closes2), n=20)
    v2 = _line_values(out2)
    assert abs(v2[19] - 50.0) < 1e-9  # 9 below, 2 equal -> (9+1)/20*100
    assert v2[18] is None


def test_chart_p02_linear_regression_channel_matches_hand_computed_values() -> None:
    # Convention declared: least-squares fit; channel width = MAX absolute
    # deviation from the fit over the window.
    closes = [2.0, 4.0, 9.0]
    bars = _bars(closes)
    out = linear_regression(bars, n=3)
    upper = _line_values(out, "upper")
    middle = _line_values(out, "middle")
    lower = _line_values(out, "lower")
    # fit: slope 3.5, intercept 1.5 -> centre at x=2 is 8.5; maxDev = 1.0.
    assert abs(middle[2] - 8.5) < 1e-9
    assert abs(upper[2] - 9.5) < 1e-9
    assert abs(lower[2] - 7.5) < 1e-9
    assert middle[1] is None


# --- M3 full-definition required_bars --------------------------------------

def test_chart_p02_required_bars_are_full_definition_not_earliest_drawable() -> None:
    reg = INDICATOR_REGISTRY
    # CHART-P01 precedent (MACD 34) extended to the new entries.
    assert reg["ICHIMOKU952652"].required_bars == 78  # 52 + 26 displacement
    assert reg["ADX14"].required_bars == 28  # DX seeded at n+1, ADX at 2n
    assert reg["STOCH1433"].required_bars == 18  # 14 + 2 + 2 smoothing
    assert reg["ROC12"].required_bars == 13
    assert reg["SUPERTREND103"].required_bars == 11  # ATR10 needs 11 bars
    assert reg["KELTNER20"].required_bars == 20
    assert reg["HMA20"].required_bars == 23  # n + floor(sqrt(n)) - 1: full sqrt window
    assert reg["DONCHIAN20"].required_bars == 20
    assert reg["CCI20"].required_bars == 20
    assert reg["ZSCORE20"].required_bars == 20
    assert reg["PCTRANK20"].required_bars == 20
    assert reg["REGCHAN20"].required_bars == 20
    # Timeframe-aware full definitions (day/session derived levels).
    assert reg["PIVOTCL"].required_bars_fn is not None
    assert reg["PIVOTCL"].required_bars_fn(TIMEFRAME_MINUTES["M1"]) == 1441
    assert reg["PIVOTCL"].required_bars_fn(TIMEFRAME_MINUTES["H1"]) == 25
    assert reg["PIVOTCL"].required_bars_fn(TIMEFRAME_MINUTES["D1"]) == 2
    assert reg["CAMARILLA"].required_bars_fn(TIMEFRAME_MINUTES["M1"]) == 1441
    assert reg["PREVHL"].required_bars_fn(TIMEFRAME_MINUTES["M1"]) == 1441
    # Session levels: resolvable only where the session length divides evenly
    # (540 min sessions; tf <= 60 and 540 % tf == 0).
    assert reg["SESSLVL"].required_bars_fn(TIMEFRAME_MINUTES["M1"]) == 541
    assert reg["SESSLVL"].required_bars_fn(TIMEFRAME_MINUTES["H1"]) == 10
    assert reg["SESSLVL"].required_bars_fn(TIMEFRAME_MINUTES["H4"]) is None  # unresolvable
    assert reg["SESSLVL"].required_bars_fn(TIMEFRAME_MINUTES["D1"]) is None


# --- Registry breadth + engine field (S1) ----------------------------------

def test_chart_p02_registry_carries_engine_and_all_new_entries() -> None:
    reg = INDICATOR_REGISTRY
    expected = [
        "SMA20", "SMA50", "EMA20", "RSI14", "MACD12269", "BBANDS201", "ATR14",
        "HMA20", "SUPERTREND103", "ICHIMOKU952652",
        "STOCH1433", "CCI20", "ROC12", "ADX14",
        "KELTNER20", "DONCHIAN20",
        "PIVOTCL", "CAMARILLA", "PREVHL", "SESSLVL",
        "ZSCORE20", "PCTRANK20", "REGCHAN20",
        # CHART-P03 widens the registry (MarketStructure engine) — the
        # CHART-P02 twenty-three keep their exact positions.
        "SWINGS55", "STRUCT55", "BOS55", "CHOCH55", "FVG3", "OBPATTERN",
    ]
    assert sorted(reg.keys()) == sorted(expected)
    assert len(reg) == 29
    engines = {d.engine for d in reg.values()}
    assert engines == {"Trend", "Momentum", "Volatility", "Levels", "Statistics", "MarketStructure"}
    assert reg["HMA20"].engine == "Trend"
    assert reg["STOCH1433"].engine == "Momentum"
    assert reg["KELTNER20"].engine == "Volatility"
    assert reg["PIVOTCL"].engine == "Levels"
    assert reg["ZSCORE20"].engine == "Statistics"
    for defn in reg.values():
        assert defn.pane in {"overlay", "pane"}


# --- Insufficiency for the long-period new indicators ----------------------

def test_chart_p02_long_period_indicators_return_typed_insufficient() -> None:
    bars = _bars([float(i) for i in range(1, 6)])  # 5 bars
    assert ichimoku(bars).kind == "insufficient"
    assert ichimoku(bars).required == 78
    assert ichimoku(bars).available == 5
    assert ichimoku(bars).points == []


# --- Endpoint: new indicators served + 422 unknown -------------------------

def test_chart_p02_endpoint_serves_new_indicators_over_seeded_series(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    seed = client.post("/api/v1/market/live/seed-history", headers=auth_headers)
    assert seed.status_code == 200
    resp = client.get(
        "/api/v1/persistence/indicator-series",
        params={"symbol": "EURUSD", "timeframe": "M1", "indicators": "HMA20,ADX14,ROC12"},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["indicators"]["HMA20"]["shape"] == "line"
    assert body["indicators"]["HMA20"]["kind"] == "computed"
    assert body["indicators"]["ADX14"]["shape"] == "multi"
    assert set(body["indicators"]["ADX14"]["lines"].keys()) == {"adx", "plus_di", "minus_di"}
    assert body["indicators"]["ROC12"]["shape"] == "line"
