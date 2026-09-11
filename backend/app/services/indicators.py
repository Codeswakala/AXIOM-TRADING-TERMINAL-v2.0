"""CHART-P01 server-side indicator computation (F-CHART-1 fix).

Pure, deterministic, OHLC-only computations over the candle window the series
endpoint already serves. Every function returns a typed result:

  IndicatorSeries(kind="computed", points=[...])
  IndicatorSeries(kind="insufficient", required=n, available=len(bars))

M4: an indicator needing n bars over a window with fewer than n MUST NOT emit
a value — no zeros, no nulls rendered as lines, no partial-window averages
presented as full-period ones.

Formulae (M2, each pinned by a hand-computed test):
  SMA(n)   — arithmetic mean of the last n closes.
  EMA(n)   — alpha = 2/(n+1); SEEDING RULE: the first emitted EMA is the SMA
             of the first n closes (the traditional charting convention;
             deterministic and self-consistent from bar n onward).
  RSI(n)   — Wilder's smoothing: first avgGain/avgLoss are plain means of the
             first n price changes; thereafter (prev*(n-1) + change)/n.
  MACD     — EMA12 - EMA26; signal = EMA9 of the MACD line (SMA-seeded over
             the first 9 MACD values); histogram = MACD - signal. Points
             before each seed carry None, never 0.
  Bollinger(n,k) — SMA +- k * POPULATION standard deviation (divide by n,
             not n-1).
  ATR(n)   — true range = max(H-L, |H-prevC|, |L-prevC|) with Wilder's
             smoothing; first ATR = mean of the first n true ranges (needs
             n+1 bars).

M7: inputs are sorted by open_time defensively (not order-preserving), so the
output is identical for any input ordering and for repeat calls.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from typing import Protocol


class _Bar(Protocol):
    open_time: datetime
    open: Decimal | float | str
    high: Decimal | float | str
    low: Decimal | float | str
    close: Decimal | float | str


@dataclass(frozen=True)
class LinePoint:
    time: datetime
    value: Decimal | None


@dataclass(frozen=True)
class BandPoint:
    time: datetime
    upper: Decimal | None
    middle: Decimal | None
    lower: Decimal | None


@dataclass(frozen=True)
class MacdPoint:
    time: datetime
    macd: Decimal | None
    signal: Decimal | None
    histogram: Decimal | None


@dataclass(frozen=True)
class IndicatorSeries:
    kind: str  # "computed" | "insufficient"
    points: list = field(default_factory=list)
    lines: dict[str, list] | None = None  # multi-line indicators (Ichimoku, ADX, levels…)
    required: int | None = None
    available: int | None = None


def _field(bar: _Bar | dict, name: str) -> object:
    """Attribute or mapping access — the service passes ORM/read models, the
    test fixtures pass plain dicts; both carry the same OHLCV fields."""
    if isinstance(bar, dict):
        return bar[name]
    return getattr(bar, name)


def _sorted_bars(bars: list[_Bar] | list[dict]) -> list:
    """Sort chronologically and materialize every bar into a plain float
    dict ONCE at function entry. Downstream per-point access then costs plain
    dict lookups instead of ORM attribute loads — this single conversion is
    what keeps 23 indicators × 2880 bars computable in milliseconds instead
    of seconds. Provenance-sensitive fields are not touched."""
    materialized: list[dict] = []
    for bar in bars:
        if isinstance(bar, dict):
            materialized.append(bar)
        else:
            materialized.append(
                {
                    "open_time": bar.open_time,
                    "open": float(bar.open),
                    "high": float(bar.high),
                    "low": float(bar.low),
                    "close": float(bar.close),
                }
            )
    return sorted(materialized, key=lambda b: _utc(b["open_time"]))


def _utc(dt: datetime) -> datetime:
    """Normalize to UTC. Naive values are assumed UTC (the storage invariant —
    every write path normalizes open_time before storage; the SQLite driver
    strips tzinfo on read), matching the DATA-P02 aggregation boundary."""
    if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _num(value: object) -> float:
    return float(value)


def _dec(value: float) -> Decimal:
    return Decimal(str(round(value, 10)))


def sma(bars: list[_Bar], n: int) -> IndicatorSeries:
    ordered = _sorted_bars(bars)
    if len(ordered) < n:
        return IndicatorSeries(kind="insufficient", required=n, available=len(ordered))
    points: list[LinePoint] = []
    window_sum = 0.0
    for i, bar in enumerate(ordered):
        close = _num(_field(bar, "close"))
        window_sum += close
        if i >= n:
            window_sum -= _num(_field(ordered[i - n], "close"))
        points.append(
            LinePoint(time=_utc(_field(bar, "open_time")), value=_dec(window_sum / n) if i >= n - 1 else None)
        )
    return IndicatorSeries(kind="computed", points=points, required=n, available=len(ordered))


def ema(bars: list[_Bar], n: int) -> IndicatorSeries:
    """EMA(n) with alpha = 2/(n+1), SMA-seeded at bar n."""
    ordered = _sorted_bars(bars)
    if len(ordered) < n:
        return IndicatorSeries(kind="insufficient", required=n, available=len(ordered))
    alpha = 2.0 / (n + 1.0)
    points: list[LinePoint] = []
    current: float | None = None
    for i, bar in enumerate(ordered):
        close = _num(_field(bar, "close"))
        if i < n - 1:
            points.append(LinePoint(time=_utc(_field(bar, "open_time")), value=None))
            continue
        if i == n - 1:
            # Seeding rule: SMA of the first n closes.
            current = sum(_num(_field(b, "close")) for b in ordered[:n]) / n
        else:
            current = current + alpha * (close - current)  # type: ignore[operator]
        points.append(LinePoint(time=_utc(_field(bar, "open_time")), value=_dec(current)))
    return IndicatorSeries(kind="computed", points=points, required=n, available=len(ordered))


def rsi(bars: list[_Bar], n: int) -> IndicatorSeries:
    """RSI(n) with Wilder's smoothing. First value needs n price changes
    (n+1 bars)."""
    ordered = _sorted_bars(bars)
    if len(ordered) < n + 1:
        return IndicatorSeries(kind="insufficient", required=n + 1, available=len(ordered))
    points: list[LinePoint] = []
    gains: list[float] = []
    losses: list[float] = []
    for i in range(1, len(ordered)):
        delta = _num(_field(ordered[i], "close")) - _num(_field(ordered[i - 1], "close"))
        gains.append(max(delta, 0.0))
        losses.append(max(-delta, 0.0))
    avg_gain: float | None = None
    avg_loss: float | None = None
    # Bar 0 has no change -> None. Bars 1..n-1: not enough changes.
    points.append(LinePoint(time=_utc(_field(ordered[0], "open_time")), value=None))
    for i in range(1, len(ordered)):
        change_index = i - 1
        if change_index < n - 1:
            points.append(LinePoint(time=_utc(_field(ordered[i], "open_time")), value=None))
            continue
        if change_index == n - 1:
            avg_gain = sum(gains[:n]) / n
            avg_loss = sum(losses[:n]) / n
        else:
            avg_gain = (avg_gain * (n - 1) + gains[change_index]) / n  # type: ignore[operator]
            avg_loss = (avg_loss * (n - 1) + losses[change_index]) / n  # type: ignore[operator]
        if avg_loss == 0:
            value = 100.0
        else:
            rs = avg_gain / avg_loss
            value = 100.0 - 100.0 / (1.0 + rs)
        points.append(LinePoint(time=_utc(_field(ordered[i], "open_time")), value=_dec(value)))
    return IndicatorSeries(kind="computed", points=points, required=n + 1, available=len(ordered))


def _ema_series(values: list[float | None], n: int) -> list[float | None]:
    """EMA over an arbitrary value list (used for the MACD signal line),
    SMA-seeded over the first n defined values."""
    alpha = 2.0 / (n + 1.0)
    out: list[float | None] = []
    seed_window: list[float] = []
    current: float | None = None
    seeded = False
    for value in values:
        if value is None:
            out.append(None)
            continue
        if not seeded:
            seed_window.append(value)
            if len(seed_window) == n:
                current = sum(seed_window) / n
                seeded = True
                out.append(current)
            else:
                out.append(None)
        else:
            current = current + alpha * (value - current)  # type: ignore[operator]
            out.append(current)
    return out


def macd(bars: list[_Bar]) -> IndicatorSeries:
    """MACD(12,26,9): line = EMA12 - EMA26; signal = EMA9 of the line;
    histogram = line - signal. Requires 26 bars for the line and 34 for a
    seeded signal."""
    ordered = _sorted_bars(bars)
    if len(ordered) < 26:
        return IndicatorSeries(kind="insufficient", required=26, available=len(ordered))
    ema12_full = ema(ordered, n=12).points
    ema26_full = ema(ordered, n=26).points
    macd_values: list[float | None] = []
    for i in range(len(ordered)):
        e12 = ema12_full[i].value
        e26 = ema26_full[i].value
        macd_values.append(float(e12) - float(e26) if e12 is not None and e26 is not None else None)
    signal_values = _ema_series(macd_values, n=9)
    points: list[MacdPoint] = []
    for i, bar in enumerate(ordered):
        m = macd_values[i]
        s = signal_values[i]
        points.append(
            MacdPoint(
                time=_utc(_field(bar, "open_time")),
                macd=_dec(m) if m is not None else None,
                signal=_dec(s) if s is not None else None,
                histogram=_dec(m - s) if m is not None and s is not None else None,
            )
        )
    return IndicatorSeries(kind="computed", points=points, required=26, available=len(ordered))


def bollinger(bars: list[_Bar], n: int, multiplier: float) -> IndicatorSeries:
    """SMA +- multiplier * POPULATION standard deviation (divide by n)."""
    ordered = _sorted_bars(bars)
    if len(ordered) < n:
        return IndicatorSeries(kind="insufficient", required=n, available=len(ordered))
    points: list[BandPoint] = []
    for i, bar in enumerate(ordered):
        if i < n - 1:
            points.append(BandPoint(time=_utc(_field(bar, "open_time")), upper=None, middle=None, lower=None))
            continue
        window = [_num(_field(b, "close")) for b in ordered[i - n + 1 : i + 1]]
        mean = sum(window) / n
        variance = sum((x - mean) ** 2 for x in window) / n  # population
        sigma = math.sqrt(variance)
        points.append(
            BandPoint(
                time=_utc(_field(bar, "open_time")),
                upper=_dec(mean + multiplier * sigma),
                middle=_dec(mean),
                lower=_dec(mean - multiplier * sigma),
            )
        )
    return IndicatorSeries(kind="computed", points=points, required=n, available=len(ordered))


def atr(bars: list[_Bar], n: int) -> IndicatorSeries:
    """ATR(n) — true range with Wilder's smoothing; first value at bar n
    (needs n+1 bars)."""
    ordered = _sorted_bars(bars)
    if len(ordered) < n + 1:
        return IndicatorSeries(kind="insufficient", required=n + 1, available=len(ordered))
    trs: list[float] = []
    for i in range(1, len(ordered)):
        high = _num(_field(ordered[i], "high"))
        low = _num(_field(ordered[i], "low"))
        prev_close = _num(_field(ordered[i - 1], "close"))
        tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
        trs.append(tr)
    points: list[LinePoint] = [LinePoint(time=_utc(_field(ordered[0], "open_time")), value=None)]
    current: float | None = None
    for i in range(1, len(ordered)):
        tr_index = i - 1
        if tr_index < n - 1:
            points.append(LinePoint(time=_utc(_field(ordered[i], "open_time")), value=None))
            continue
        if tr_index == n - 1:
            current = sum(trs[:n]) / n
        else:
            current = (current * (n - 1) + trs[tr_index]) / n  # type: ignore[operator]
        points.append(LinePoint(time=_utc(_field(ordered[i], "open_time")), value=_dec(current)))
    return IndicatorSeries(kind="computed", points=points, required=n + 1, available=len(ordered))


# =========================================================================
# CHART-P02 — indicator breadth (Trend / Momentum / Volatility / Levels /
# Statistics). Every function states its conventions; every convention is
# pinned by a hand-computable test in tests/test_chart_p02_indicators.py.
# =========================================================================


def _wma(values: list[float], n: int) -> list[float | None]:
    """Weighted moving average (weights 1..n)."""
    out: list[float | None] = []
    denom = n * (n + 1) / 2.0
    for i in range(len(values)):
        if i < n - 1:
            out.append(None)
            continue
        window = values[i - n + 1 : i + 1]
        out.append(sum((j + 1) * window[j] for j in range(n)) / denom)
    return out


def hma(bars: list[_Bar] | list[dict], n: int) -> IndicatorSeries:
    """HMA(n): WMA(2*WMA(n/2) - WMA(n)) over floor(sqrt(n)).
    Convention: n/2 uses integer floor, the final window is floor(sqrt(n))."""
    ordered = _sorted_bars(bars)
    if len(ordered) < n:
        return IndicatorSeries(kind="insufficient", required=n, available=len(ordered))
    half = n // 2
    root = math.floor(math.sqrt(n))
    full_definition = n + root - 1
    if len(ordered) < full_definition:
        return IndicatorSeries(
            kind="insufficient", required=full_definition, available=len(ordered)
        )
    closes = [_num(_field(b, "close")) for b in ordered]
    wma_half = _wma(closes, half)
    wma_full = _wma(closes, n)
    raw: list[float | None] = [
        None if a is None or b is None else 2.0 * a - b for a, b in zip(wma_half, wma_full)
    ]
    smoothed = _wma([v if v is not None else 0.0 for v in raw], root)
    points: list[LinePoint] = []
    for i, bar in enumerate(ordered):
        value = None
        # The first FULLY-seeded HMA needs raw values over the whole sqrt
        # window: index n-1 + (root-1).
        if raw[i] is not None and i >= n - 1 + (root - 1):
            value = smoothed[i]
        points.append(LinePoint(time=_utc(_field(bar, "open_time")), value=_dec(value) if value is not None else None))
    return IndicatorSeries(kind="computed", points=points, required=n, available=len(ordered))


def _wilders(values: list[float], n: int) -> list[float | None]:
    """Wilder's smoothing over a value list; first value = plain mean of the
    first n."""
    out: list[float | None] = []
    current: float | None = None
    for i, v in enumerate(values):
        if i < n - 1:
            out.append(None)
            continue
        if i == n - 1:
            current = sum(values[:n]) / n
        else:
            current = (current * (n - 1) + v) / n  # type: ignore[operator]
        out.append(current)
    return out


def supertrend(bars: list[_Bar] | list[dict], n: int, multiplier: float) -> IndicatorSeries:
    """Supertrend(n, multiplier): basic bands = (H+L)/2 +- multiplier*ATR(n)
    (Wilder); band-locking: adopt the basic band when it moves beyond the
    previous FINAL band or price closed beyond it, else hold the previous.
    Output is the two band lines ONLY — no trend verdict is emitted (M9)."""
    ordered = _sorted_bars(bars)
    if len(ordered) < n + 1:
        return IndicatorSeries(kind="insufficient", required=n + 1, available=len(ordered))
    atr_out = atr(ordered, n)
    atr_values = [None if p.value is None else float(p.value) for p in atr_out.points]
    upper: list[float | None] = [None] * len(ordered)
    lower: list[float | None] = [None] * len(ordered)
    final_upper: float | None = None
    final_lower: float | None = None
    prev_close: float | None = None
    for i, bar in enumerate(ordered):
        a = atr_values[i]
        if a is None:
            prev_close = _num(_field(bar, "close"))
            continue
        mid = (_num(_field(bar, "high")) + _num(_field(bar, "low"))) / 2.0
        basic_upper = mid + multiplier * a
        basic_lower = mid - multiplier * a
        if final_upper is None:
            final_upper, final_lower = basic_upper, basic_lower
        else:
            if basic_upper < final_upper or (prev_close is not None and prev_close > final_upper):
                final_upper = basic_upper
            if basic_lower > final_lower or (prev_close is not None and prev_close < final_lower):
                final_lower = basic_lower
        upper[i] = final_upper
        lower[i] = final_lower
        prev_close = _num(_field(bar, "close"))
    def pts(values: list[float | None]) -> list[LinePoint]:
        return [LinePoint(time=_utc(_field(b, "open_time")), value=_dec(v) if v is not None else None) for b, v in zip(ordered, values)]
    return IndicatorSeries(
        kind="computed",
        lines={"supertrend_upper": pts(upper), "supertrend_lower": pts(lower)},
        required=n + 1,
        available=len(ordered),
    )


def _highs_lows(ordered: list, n: int) -> tuple[list[float | None], list[float | None]]:
    highs: list[float | None] = []
    lows: list[float | None] = []
    for i in range(len(ordered)):
        if i < n - 1:
            highs.append(None)
            lows.append(None)
            continue
        window = ordered[i - n + 1 : i + 1]
        highs.append(max(_num(_field(b, "high")) for b in window))
        lows.append(min(_num(_field(b, "low")) for b in window))
    return highs, lows


def ichimoku(bars: list[_Bar] | list[dict]) -> IndicatorSeries:
    """Ichimoku (9, 26, 52). Convention: tenkan/kijun/senkou B are midpoints
    of the n-period high/low; senkou A = (tenkan+kijun)/2. DISPLACEMENT: the
    values computed at bar i are plotted at bar i+26 (senkou A/B) and bar
    i-26 (chikou close). NO point is plotted beyond the last bar — the cloud
    ends AT the last bar; its final 26 values are the live projection plotted
    at existing bar positions, so the price-pane time axis is never extended
    and nothing implies data beyond the last bar (M6).
    Full definition: 52 + 26 = 78 bars (M3)."""
    ordered = _sorted_bars(bars)
    required = 78
    if len(ordered) < required:
        return IndicatorSeries(kind="insufficient", required=required, available=len(ordered))
    n = len(ordered)
    closes = [_num(_field(b, "close")) for b in ordered]
    tenkan_h, tenkan_l = _highs_lows(ordered, 9)
    kijun_h, kijun_l = _highs_lows(ordered, 26)
    senkou_b_h, senkou_b_l = _highs_lows(ordered, 52)

    tenkan = [None if a is None else (a + b) / 2.0 for a, b in zip(tenkan_h, tenkan_l)]
    kijun = [None if a is None else (a + b) / 2.0 for a, b in zip(kijun_h, kijun_l)]
    senkou_b = [None if a is None else (a + b) / 2.0 for a, b in zip(senkou_b_h, senkou_b_l)]
    senkou_a = [
        None if a is None or b is None else (a + b) / 2.0 for a, b in zip(tenkan, kijun)
    ]

    def displaced(values: list[float | None], shift: int) -> list[LinePoint]:
        pts: list[LinePoint] = [LinePoint(time=_utc(_field(b, "open_time")), value=None) for b in ordered]
        for i, v in enumerate(values):
            j = i + shift
            if v is None or j < 0 or j >= n:
                continue
            pts[j] = LinePoint(time=_utc(_field(ordered[j], "open_time")), value=_dec(v))
        return pts

    chikou_raw = [None] * 26 + closes[26:]  # chikou(i) = close[i] plotted at i-26
    return IndicatorSeries(
        kind="computed",
        lines={
            "tenkan": [LinePoint(time=_utc(_field(b, "open_time")), value=_dec(v) if v is not None else None) for b, v in zip(ordered, tenkan)],
            "kijun": [LinePoint(time=_utc(_field(b, "open_time")), value=_dec(v) if v is not None else None) for b, v in zip(ordered, kijun)],
            "senkou_a": displaced(senkou_a, 26),
            "senkou_b": displaced(senkou_b, 26),
            "chikou": displaced(chikou_raw, -26),
        },
        required=required,
        available=len(ordered),
    )


def stochastic(
    bars: list[_Bar] | list[dict], k_period: int, smooth_k: int, smooth_d: int
) -> IndicatorSeries:
    """SLOW Stochastic (14,3,3): raw %K = (C-LL)/(HH-LL)*100 over k_period;
    %K = SMA(smooth_k) of raw; %D = SMA(smooth_d) of %K. Full definition:
    k_period + (smooth_k-1) + (smooth_d-1) bars."""
    ordered = _sorted_bars(bars)
    required = k_period + (smooth_k - 1) + (smooth_d - 1)
    if len(ordered) < required:
        return IndicatorSeries(kind="insufficient", required=required, available=len(ordered))
    highs, lows = _highs_lows(ordered, k_period)
    closes = [_num(_field(b, "close")) for b in ordered]
    raw_k: list[float | None] = []
    for i in range(len(ordered)):
        h, l = highs[i], lows[i]
        raw_k.append(None if h is None or l is None or h == l else (closes[i] - l) / (h - l) * 100.0)
    pct_k = _wma([0.0 if v is None else v for v in raw_k], 1)  # placeholder
    # SMA smoothing (simple means) over the raw stream
    def _sma_stream(values: list[float | None], window: int) -> list[float | None]:
        out: list[float | None] = []
        acc: list[float] = []
        for v in values:
            if v is None:
                out.append(None)
                continue
            acc.append(v)
            if len(acc) > window:
                acc.pop(0)
            out.append(sum(acc) / len(acc) if len(acc) == window else None)
        return out

    pct_k = _sma_stream(raw_k, smooth_k)
    pct_d = _sma_stream(pct_k, smooth_d)
    def pts(values: list[float | None]) -> list[LinePoint]:
        return [LinePoint(time=_utc(_field(b, "open_time")), value=_dec(v) if v is not None else None) for b, v in zip(ordered, values)]
    return IndicatorSeries(
        kind="computed",
        lines={"percent_k": pts(pct_k), "percent_d": pts(pct_d)},
        required=required,
        available=len(ordered),
    )


def cci(bars: list[_Bar] | list[dict], n: int) -> IndicatorSeries:
    """CCI(n): (TP - SMA(TP)) / (0.015 * mean absolute deviation of TP).
    Convention: MAD, NOT standard deviation; the 0.015 constant is Lambert's."""
    ordered = _sorted_bars(bars)
    if len(ordered) < n:
        return IndicatorSeries(kind="insufficient", required=n, available=len(ordered))
    tps = [
        (_num(_field(b, "high")) + _num(_field(b, "low")) + _num(_field(b, "close"))) / 3.0
        for b in ordered
    ]
    points: list[LinePoint] = []
    for i, bar in enumerate(ordered):
        if i < n - 1:
            points.append(LinePoint(time=_utc(_field(bar, "open_time")), value=None))
            continue
        window = tps[i - n + 1 : i + 1]
        mean = sum(window) / n
        mad = sum(abs(x - mean) for x in window) / n
        value = (tps[i] - mean) / (0.015 * mad) if mad > 0 else 0.0
        points.append(LinePoint(time=_utc(_field(bar, "open_time")), value=_dec(value)))
    return IndicatorSeries(kind="computed", points=points, required=n, available=len(ordered))


def roc(bars: list[_Bar] | list[dict], n: int) -> IndicatorSeries:
    """ROC(n) = (close - close[n ago]) / close[n ago] * 100. Needs n+1 bars."""
    ordered = _sorted_bars(bars)
    if len(ordered) < n + 1:
        return IndicatorSeries(kind="insufficient", required=n + 1, available=len(ordered))
    points: list[LinePoint] = []
    for i, bar in enumerate(ordered):
        if i < n:
            points.append(LinePoint(time=_utc(_field(bar, "open_time")), value=None))
            continue
        ref = _num(_field(ordered[i - n], "close"))
        value = (_num(_field(bar, "close")) - ref) / ref * 100.0 if ref != 0 else None
        points.append(LinePoint(time=_utc(_field(bar, "open_time")), value=_dec(value) if value is not None else None))
    return IndicatorSeries(kind="computed", points=points, required=n + 1, available=len(ordered))


def adx_dmi(bars: list[_Bar] | list[dict], n: int) -> IndicatorSeries:
    """ADX/DMI(n): +DM/-DM/TR with Wilder smoothing; +DI/-DI = 100*smoothed/ATR;
    DX = 100*|+DI - -DI|/(+DI + -DI); ADX = Wilder average of DX.
    Full definition: DX first defined at bar n+1 and the ADX average needs n
    DX values -> ADX first defined at bar 2n (declared required = 2n)."""
    ordered = _sorted_bars(bars)
    required = 2 * n
    if len(ordered) < required:
        return IndicatorSeries(kind="insufficient", required=required, available=len(ordered))
    trs: list[float] = []
    plus_dms: list[float] = []
    minus_dms: list[float] = []
    for i in range(1, len(ordered)):
        high = _num(_field(ordered[i], "high"))
        low = _num(_field(ordered[i], "low"))
        prev_close = _num(_field(ordered[i - 1], "close"))
        prev_high = _num(_field(ordered[i - 1], "high"))
        prev_low = _num(_field(ordered[i - 1], "low"))
        up = high - prev_high
        down = prev_low - low
        plus_dms.append(up if up > down and up > 0 else 0.0)
        minus_dms.append(down if down > up and down > 0 else 0.0)
        trs.append(max(high - low, abs(high - prev_close), abs(low - prev_close)))
    # Wilder smoothing over the PURE change series: tr_w[j] belongs to
    # absolute bar j+1 (the change is indexed by the bar it occurred at).
    tr_w = _wilders(trs, n)
    p_w = _wilders(plus_dms, n)
    m_w = _wilders(minus_dms, n)
    plus_di: list[float | None] = [None] * len(ordered)
    minus_di: list[float | None] = [None] * len(ordered)
    dx: list[float | None] = [None] * len(ordered)
    for j, t in enumerate(tr_w):
        if t is None or t == 0:
            continue
        pdi = 100.0 * p_w[j] / t  # type: ignore[operator]
        mdi = 100.0 * m_w[j] / t  # type: ignore[operator]
        plus_di[j + 1] = pdi
        minus_di[j + 1] = mdi
        dx[j + 1] = 100.0 * abs(pdi - mdi) / (pdi + mdi) if (pdi + mdi) != 0 else 0.0
    # ADX = Wilder average of the DX values once they exist; the first ADX
    # needs n DX values -> absolute index n + (n-1) = 2n - 1... the first DX
    # sits at absolute index n, so the first ADX is at index 2n.
    dx_pure = [v for v in dx if v is not None]
    adx_compact = _wilders(dx_pure, n)
    adx_line: list[float | None] = [None] * len(ordered)
    for j, v in enumerate(adx_compact):
        if v is not None:
            adx_line[n + j] = v
    def pts(values: list[float | None]) -> list[LinePoint]:
        return [LinePoint(time=_utc(_field(b, "open_time")), value=_dec(v) if v is not None else None) for b, v in zip(ordered, values)]
    return IndicatorSeries(
        kind="computed",
        lines={"adx": pts(adx_line), "plus_di": pts(plus_di), "minus_di": pts(minus_di)},
        required=required,
        available=len(ordered),
    )


def keltner(
    bars: list[_Bar] | list[dict], ema_period: int, atr_period: int, multiplier: float
) -> IndicatorSeries:
    """Keltner channel: EMA centre (SMA-seeded), channel = centre +- mult*ATR
    (Wilder), ATR period distinct from the channel period."""
    ordered = _sorted_bars(bars)
    required = ema_period
    if len(ordered) < required:
        return IndicatorSeries(kind="insufficient", required=required, available=len(ordered))
    centre = ema(ordered, ema_period).points
    atr_out = atr(ordered, atr_period)
    atr_values = [None if p.value is None else float(p.value) for p in atr_out.points]
    upper: list[float | None] = []
    middle: list[float | None] = []
    lower: list[float | None] = []
    for i, bar in enumerate(ordered):
        c = centre[i].value
        a = atr_values[i]
        if c is None:
            upper.append(None)
            middle.append(None)
            lower.append(None)
            continue
        mid = float(c)
        band = multiplier * (a if a is not None else 0.0)
        upper.append(mid + band)
        middle.append(mid)
        lower.append(mid - band)
    def pts(values: list[float | None]) -> list[LinePoint]:
        return [LinePoint(time=_utc(_field(b, "open_time")), value=_dec(v) if v is not None else None) for b, v in zip(ordered, values)]
    return IndicatorSeries(
        kind="computed",
        lines={"upper": pts(upper), "middle": pts(middle), "lower": pts(lower)},
        required=required,
        available=len(ordered),
    )


def donchian(bars: list[_Bar] | list[dict], n: int) -> IndicatorSeries:
    """Donchian(n): upper = n-period high, lower = n-period low,
    middle = (upper+lower)/2."""
    ordered = _sorted_bars(bars)
    if len(ordered) < n:
        return IndicatorSeries(kind="insufficient", required=n, available=len(ordered))
    highs, lows = _highs_lows(ordered, n)
    upper: list[float | None] = []
    middle: list[float | None] = []
    lower: list[float | None] = []
    for i in range(len(ordered)):
        h, l = highs[i], lows[i]
        if h is None or l is None:
            upper.append(None)
            middle.append(None)
            lower.append(None)
            continue
        upper.append(h)
        lower.append(l)
        middle.append((h + l) / 2.0)
    def pts(values: list[float | None]) -> list[LinePoint]:
        return [LinePoint(time=_utc(_field(b, "open_time")), value=_dec(v) if v is not None else None) for b, v in zip(ordered, values)]
    return IndicatorSeries(
        kind="computed",
        lines={"upper": pts(upper), "middle": pts(middle), "lower": pts(lower)},
        required=n,
        available=len(ordered),
    )


def _day_buckets(ordered: list) -> dict[tuple[int, int, int], list]:
    from collections import defaultdict

    buckets: dict[tuple[int, int, int], list] = defaultdict(list)
    for bar in ordered:
        t = _utc(_field(bar, "open_time"))
        buckets[(t.year, t.month, t.day)].append(bar)
    return buckets


def _prior_day_levels(ordered: list, compute: object) -> list[dict[str, float]]:
    """For each bar, the levels derived from the most recent COMPLETED prior
    UTC day (a day is 'complete' once a later day's bar exists)."""
    days = sorted(_day_buckets(ordered).items())
    if len(days) < 2:
        return [{} for _ in ordered]
    levels_by_bar: list[dict[str, float]] = []
    current_day = None
    current_levels: dict[str, float] = {}
    day_index = 0
    for bar in ordered:
        t = _utc(_field(bar, "open_time"))
        day_key = (t.year, t.month, t.day)
        if day_key != current_day:
            current_day = day_key
            # levels come from the last day before the current one
            prior = None
            for idx in range(len(days) - 1, -1, -1):
                if days[idx][0] < day_key:
                    prior = days[idx][1]
                    break
            if prior is not None:
                highs = [_num(_field(b, "high")) for b in prior]
                lows = [_num(_field(b, "low")) for b in prior]
                closes = [_num(_field(b, "close")) for b in prior]
                h = max(highs)
                l = min(lows)
                c = closes[-1]
                current_levels = _compute_levels(h, l, c, compute)
        levels_by_bar.append(dict(current_levels))
    return levels_by_bar


def _compute_levels(h: float, l: float, c: float, compute: object) -> dict[str, float]:
    fn = compute
    assert callable(fn)
    return fn(h, l, c)


def _pivot_levels(h: float, l: float, c: float) -> dict[str, float]:
    p = (h + l + c) / 3.0
    return {
        "P": p,
        "R1": 2 * p - l,
        "S1": 2 * p - h,
        "R2": p + (h - l),
        "S2": p - (h - l),
        "R3": h + 2 * (p - l),
        "S3": l - 2 * (h - p),
    }


def _camarilla_levels(h: float, l: float, c: float) -> dict[str, float]:
    rng = (h - l) * 1.1
    return {
        "R1": c + rng / 12,
        "R2": c + rng / 6,
        "R3": c + rng / 4,
        "R4": c + rng / 2,
        "S1": c - rng / 12,
        "S2": c - rng / 6,
        "S3": c - rng / 4,
        "S4": c - rng / 2,
    }


def _prev_hl_levels(h: float, l: float, c: float) -> dict[str, float]:
    return {"prev_high": h, "prev_low": l}


def _levels_series(ordered: list, compute: object, tf_minutes: int) -> IndicatorSeries:
    from app.services.timeframes import TIMEFRAME_MINUTES

    bars_per_day = max(1, TIMEFRAME_MINUTES["D1"] // tf_minutes)
    required = bars_per_day + 1
    if len(ordered) < required:
        return IndicatorSeries(kind="insufficient", required=required, available=len(ordered))
    per_bar = _prior_day_levels(ordered, compute)
    names = list(_compute_levels(1.0, 2.0, 3.0, compute).keys())
    lines: dict[str, list[LinePoint]] = {}
    for name in names:
        pts: list[LinePoint] = []
        for bar, levels in zip(ordered, per_bar):
            value = levels.get(name)
            pts.append(LinePoint(time=_utc(_field(bar, "open_time")), value=_dec(value) if value is not None else None))
        lines[name] = pts
    return IndicatorSeries(kind="computed", lines=lines, required=required, available=len(ordered))


def pivot_points(bars: list[_Bar] | list[dict], tf_minutes: int) -> IndicatorSeries:
    """Classic pivots from the most recent COMPLETED prior UTC day's H/L/C.
    Timeframe-aware full definition: one prior day's bars + 1."""
    return _levels_series(_sorted_bars(bars), _pivot_levels, tf_minutes)


def camarilla(bars: list[_Bar] | list[dict], tf_minutes: int) -> IndicatorSeries:
    """Classic Camarilla levels (multipliers 1.1/12, /6, /4, /2) from the most
    recent COMPLETED prior UTC day's H/L/C."""
    return _levels_series(_sorted_bars(bars), _camarilla_levels, tf_minutes)


def prev_day_levels(bars: list[_Bar] | list[dict], tf_minutes: int) -> IndicatorSeries:
    """Prior UTC day's high/low as level lines."""
    return _levels_series(_sorted_bars(bars), _prev_hl_levels, tf_minutes)


SESSION_SPECS: tuple[tuple[str, int, int], ...] = (
    ("london", 7, 16),
    ("newyork", 12, 21),
)


def session_levels(bars: list[_Bar] | list[dict], tf_minutes: int) -> IndicatorSeries:
    """Session levels: LONDON 07:00-16:00 UTC and NEW YORK 12:00-21:00 UTC
    (fixed windows, weekend-closed — mirrors the frontend session context).
    The level shown for session S is the most recent COMPLETED occurrence's
    high/low. Resolvable only when tf_minutes <= 60 and divides the 540-minute
    session evenly — on coarser timeframes the window cannot be resolved and
    the endpoint reports the typed insufficient result (required=0, available=
    bar count, with a detail set at the endpoint layer)."""
    from collections import defaultdict

    session_len = 9 * 60  # 540 minutes
    resolvable = tf_minutes <= 60 and session_len % tf_minutes == 0
    ordered = _sorted_bars(bars)
    if not resolvable:
        return IndicatorSeries(kind="insufficient", required=0, available=len(ordered))
    bars_per_session = session_len // tf_minutes
    required = bars_per_session + 1
    if len(ordered) < required:
        return IndicatorSeries(kind="insufficient", required=required, available=len(ordered))

    def in_session(t: datetime, start: int, end: int) -> bool:
        if t.weekday() >= 5:  # Sat/Sun closed
            return False
        return start <= t.hour < end

    # Bucket bars by (day, session id).
    by_session: dict[tuple[int, int, int, str], list] = defaultdict(list)
    for bar in ordered:
        t = _utc(_field(bar, "open_time"))
        for sid, start, end in SESSION_SPECS:
            if in_session(t, start, end):
                by_session[(t.year, t.month, t.day, sid)].append(bar)

    # Precompute each session's high/low ONCE (per-session stats), then map
    # per bar — the previous per-bar max/min over the full session list was
    # quadratic and dominated the request cost.
    session_stats: dict[tuple, tuple[float, float]] = {}
    for key, session_bars in by_session.items():
        highs = [_num(_field(b, "high")) for b in session_bars]
        lows = [_num(_field(b, "low")) for b in session_bars]
        session_stats[key] = (max(highs), min(lows))

    # Latest COMPLETED session (end strictly before t) per session id.
    def completed_stats(t: datetime, sid: str) -> tuple[float, float] | None:
        end_hour = SESSION_SPECS[0][2] if sid == "london" else SESSION_SPECS[1][2]
        best_key = None
        best_end = None
        for key in session_stats:
            if key[3] != sid:
                continue
            session_day = datetime(key[0], key[1], key[2], tzinfo=timezone.utc)
            end_time = session_day.replace(hour=end_hour, minute=0)
            if end_time < t and (best_end is None or end_time > best_end):
                best_key = key
                best_end = end_time
        return session_stats[best_key] if best_key is not None else None

    lines: dict[str, list[LinePoint]] = {}
    for sid, _s, _e in SESSION_SPECS:
        pts_h: list[LinePoint] = []
        pts_l: list[LinePoint] = []
        for bar in ordered:
            t = _utc(_field(bar, "open_time"))
            stats = completed_stats(t, sid)
            hv: float | None = None
            lv: float | None = None
            if stats is not None:
                hv, lv = stats
            pts_h.append(LinePoint(time=t, value=_dec(hv) if hv is not None else None))
            pts_l.append(LinePoint(time=t, value=_dec(lv) if lv is not None else None))
        lines[f"{sid}_high"] = pts_h
        lines[f"{sid}_low"] = pts_l
    return IndicatorSeries(kind="computed", lines=lines, required=required, available=len(ordered))


def zscore(bars: list[_Bar] | list[dict], n: int) -> IndicatorSeries:
    """Z-Score(n) = (close - SMA)/sigma, POPULATION standard deviation
    (matching Bollinger)."""
    ordered = _sorted_bars(bars)
    if len(ordered) < n:
        return IndicatorSeries(kind="insufficient", required=n, available=len(ordered))
    points: list[LinePoint] = []
    for i, bar in enumerate(ordered):
        if i < n - 1:
            points.append(LinePoint(time=_utc(_field(bar, "open_time")), value=None))
            continue
        window = [_num(_field(b, "close")) for b in ordered[i - n + 1 : i + 1]]
        mean = sum(window) / n
        variance = sum((x - mean) ** 2 for x in window) / n
        sigma = math.sqrt(variance)
        value = (_num(_field(bar, "close")) - mean) / sigma if sigma > 0 else 0.0
        points.append(LinePoint(time=_utc(_field(bar, "open_time")), value=_dec(value)))
    return IndicatorSeries(kind="computed", points=points, required=n, available=len(ordered))


def percentile_rank(bars: list[_Bar] | list[dict], n: int) -> IndicatorSeries:
    """Percentile rank of the current close within the last n closes.
    Convention: MIDPOINT rank = (count_less + 0.5*count_equal)/n * 100."""
    ordered = _sorted_bars(bars)
    if len(ordered) < n:
        return IndicatorSeries(kind="insufficient", required=n, available=len(ordered))
    points: list[LinePoint] = []
    for i, bar in enumerate(ordered):
        if i < n - 1:
            points.append(LinePoint(time=_utc(_field(bar, "open_time")), value=None))
            continue
        window = [_num(_field(b, "close")) for b in ordered[i - n + 1 : i + 1]]
        current = window[-1]
        less = sum(1 for x in window if x < current)
        equal = sum(1 for x in window if x == current)
        value = (less + 0.5 * equal) / n * 100.0
        points.append(LinePoint(time=_utc(_field(bar, "open_time")), value=_dec(value)))
    return IndicatorSeries(kind="computed", points=points, required=n, available=len(ordered))


def linear_regression(bars: list[_Bar] | list[dict], n: int) -> IndicatorSeries:
    """Linear regression channel(n): least-squares fit over the last n closes;
    channel width = MAX absolute deviation from the fit over the window."""
    ordered = _sorted_bars(bars)
    if len(ordered) < n:
        return IndicatorSeries(kind="insufficient", required=n, available=len(ordered))
    upper: list[float | None] = []
    middle: list[float | None] = []
    lower: list[float | None] = []
    for i, bar in enumerate(ordered):
        if i < n - 1:
            upper.append(None)
            middle.append(None)
            lower.append(None)
            continue
        window = ordered[i - n + 1 : i + 1]
        ys = [_num(_field(b, "close")) for b in window]
        xs = [float(j) for j in range(n)]
        x_mean = sum(xs) / n
        y_mean = sum(ys) / n
        sxx = sum((x - x_mean) ** 2 for x in xs)
        sxy = sum((xs[j] - x_mean) * (ys[j] - y_mean) for j in range(n))
        slope = sxy / sxx if sxx > 0 else 0.0
        intercept = y_mean - slope * x_mean
        fit = [intercept + slope * x for x in xs]
        max_dev = max(abs(ys[j] - fit[j]) for j in range(n))
        centre = intercept + slope * (n - 1)
        middle.append(centre)
        upper.append(centre + max_dev)
        lower.append(centre - max_dev)
    def pts(values: list[float | None]) -> list[LinePoint]:
        return [LinePoint(time=_utc(_field(b, "open_time")), value=_dec(v) if v is not None else None) for b, v in zip(ordered, values)]
    return IndicatorSeries(
        kind="computed",
        lines={"upper": pts(upper), "middle": pts(middle), "lower": pts(lower)},
        required=n,
        available=len(ordered),
    )
