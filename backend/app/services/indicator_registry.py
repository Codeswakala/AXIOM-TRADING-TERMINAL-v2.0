"""Indicator registry — the single source of truth (CHART-P01 S1, scaled in
CHART-P02).

CHART-P02 extensions, stated explicitly (M1):
1. `engine` field — data-driven grouping for the toolbar (S1).
2. `required_bars_fn` — an optional timeframe-aware full-definition hook for
   the four day/session-derived LEVEL indicators, whose bar requirements
   depend on the timeframe's bar width (a day of M1 bars is 1440 bars, a day
   of D1 bars is one bar). Indicators without the hook keep the static
   `required_bars`. This is the ONLY registry-contract change; the endpoint
   and the client architecture are otherwise untouched.
3. VWMA is NOT registered — see the delivery report (volume is gauss() noise
   uncorrelated to price; a volume-weighted indicator over noise volume is
   arithmetically correct and informationally empty).

Full-definition required_bars (M3) — the COMPLETE indicator, never the
earliest drawable point:
  HMA20 23 (n + floor(sqrt(n)) - 1) · SUPERTREND103 11 (ATR10 needs 11 bars)
  ICHIMOKU952652 78 (52 + 26 displacement)
  STOCH1433 18 · CCI20 20 · ROC12 13 · ADX14 28 (DX at n+1, ADX at 2n)
  KELTNER20 20 · DONCHIAN20 20
  PIVOTCL/CAMARILLA/PREVHL  floor(1440/tf)+1 (one prior UTC day + 1)
  SESSLVL 540/tf + 1 where resolvable (tf <= 60 and 540 % tf == 0); None
          (unresolvable) otherwise
  ZSCORE20/PCTRANK20/REGCHAN20 20
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable

from app.services import indicators as _ind
from app.services import market_structure as _ms

SESSION_MINUTES = 9 * 60
DAY_MINUTES = 24 * 60


def _bars_per_day(tf_minutes: int) -> int:
    return max(1, DAY_MINUTES // tf_minutes)


def _session_required(tf_minutes: int) -> int | None:
    if tf_minutes <= 60 and SESSION_MINUTES % tf_minutes == 0:
        return SESSION_MINUTES // tf_minutes + 1
    return None  # unresolvable at this timeframe


@dataclass(frozen=True)
class IndicatorDefinition:
    id: str
    label: str
    pane: str  # "overlay" (drawn on the price chart) | "pane" (separate chart)
    required_bars: int | None
    engine: str
    compute: Callable
    required_bars_fn: Callable[[int], int | None] | None = None
    # CHART-P03 M8: mandatory disclosure for indicators whose conventional
    # labels could imply institutional behaviour. Rendered in the product
    # whenever the indicator is active.
    disclosure: str | None = None


def _sma20(bars): return _ind.sma(bars, n=20)
def _sma50(bars): return _ind.sma(bars, n=50)
def _ema20(bars): return _ind.ema(bars, n=20)
def _rsi14(bars): return _ind.rsi(bars, n=14)
def _macd(bars): return _ind.macd(bars)
def _bbands(bars): return _ind.bollinger(bars, n=20, multiplier=2.0)
def _atr14(bars): return _ind.atr(bars, n=14)


INDICATOR_REGISTRY: dict[str, IndicatorDefinition] = {
    "SMA20": IndicatorDefinition("SMA20", "SMA 20", "overlay", 20, "Trend", _sma20),
    "SMA50": IndicatorDefinition("SMA50", "SMA 50", "overlay", 50, "Trend", _sma50),
    "EMA20": IndicatorDefinition("EMA20", "EMA 20", "overlay", 20, "Trend", _ema20),
    "RSI14": IndicatorDefinition("RSI14", "RSI 14", "pane", 15, "Momentum", _rsi14),
    "MACD12269": IndicatorDefinition("MACD12269", "MACD", "pane", 34, "Momentum", _macd),
    "BBANDS201": IndicatorDefinition("BBANDS201", "Bollinger", "overlay", 20, "Volatility", _bbands),
    "ATR14": IndicatorDefinition("ATR14", "ATR 14", "pane", 15, "Volatility", _atr14),
    # --- CHART-P02 breadth -------------------------------------------------
    "HMA20": IndicatorDefinition(
        "HMA20", "HMA 20", "overlay", 23, "Trend",
        lambda bars: _ind.hma(bars, n=20),
    ),
    "SUPERTREND103": IndicatorDefinition(
        "SUPERTREND103", "Supertrend", "overlay", 11, "Trend",
        lambda bars: _ind.supertrend(bars, n=10, multiplier=3.0),
    ),
    "ICHIMOKU952652": IndicatorDefinition(
        "ICHIMOKU952652", "Ichimoku", "overlay", 78, "Trend",
        lambda bars: _ind.ichimoku(bars),
    ),
    "STOCH1433": IndicatorDefinition(
        "STOCH1433", "Stochastic", "pane", 18, "Momentum",
        lambda bars: _ind.stochastic(bars, k_period=14, smooth_k=3, smooth_d=3),
    ),
    "CCI20": IndicatorDefinition(
        "CCI20", "CCI 20", "pane", 20, "Momentum",
        lambda bars: _ind.cci(bars, n=20),
    ),
    "ROC12": IndicatorDefinition(
        "ROC12", "ROC 12", "pane", 13, "Momentum",
        lambda bars: _ind.roc(bars, n=12),
    ),
    "ADX14": IndicatorDefinition(
        "ADX14", "ADX/DMI", "pane", 28, "Momentum",
        lambda bars: _ind.adx_dmi(bars, n=14),
    ),
    "KELTNER20": IndicatorDefinition(
        "KELTNER20", "Keltner", "overlay", 20, "Volatility",
        lambda bars: _ind.keltner(bars, ema_period=20, atr_period=10, multiplier=2.0),
    ),
    "DONCHIAN20": IndicatorDefinition(
        "DONCHIAN20", "Donchian", "overlay", 20, "Volatility",
        lambda bars: _ind.donchian(bars, n=20),
    ),
    "PIVOTCL": IndicatorDefinition(
        "PIVOTCL", "Pivots", "overlay", None, "Levels",
        lambda bars, tf_minutes: _ind.pivot_points(bars, tf_minutes),
        required_bars_fn=lambda tf: _bars_per_day(tf) + 1,
    ),
    "CAMARILLA": IndicatorDefinition(
        "CAMARILLA", "Camarilla", "overlay", None, "Levels",
        lambda bars, tf_minutes: _ind.camarilla(bars, tf_minutes),
        required_bars_fn=lambda tf: _bars_per_day(tf) + 1,
    ),
    "PREVHL": IndicatorDefinition(
        "PREVHL", "Prev H/L", "overlay", None, "Levels",
        lambda bars, tf_minutes: _ind.prev_day_levels(bars, tf_minutes),
        required_bars_fn=lambda tf: _bars_per_day(tf) + 1,
    ),
    "SESSLVL": IndicatorDefinition(
        "SESSLVL", "Session Lvls", "overlay", None, "Levels",
        lambda bars, tf_minutes: _ind.session_levels(bars, tf_minutes),
        required_bars_fn=_session_required,
    ),
    # --- CHART-P03 Market Structure (geometric pattern detections) ---------
    "SWINGS55": IndicatorDefinition(
        "SWINGS55", "Swings", "overlay", 11, "MarketStructure",
        lambda bars: _ms.swings(bars, k=5),
        disclosure=_ms.STRUCTURE_DISCLOSURE,
    ),
    "STRUCT55": IndicatorDefinition(
        "STRUCT55", "HH/HL/LH/LL", "overlay", 29, "MarketStructure",
        lambda bars: _ms.struct(bars, k=5),
        disclosure=_ms.STRUCTURE_DISCLOSURE,
    ),
    "BOS55": IndicatorDefinition(
        "BOS55", "BOS", "overlay", 12, "MarketStructure",
        lambda bars: _ms.bos(bars, k=5),
        disclosure=_ms.STRUCTURE_DISCLOSURE,
    ),
    "CHOCH55": IndicatorDefinition(
        "CHOCH55", "CHoCH", "overlay", 24, "MarketStructure",
        lambda bars: _ms.choch(bars, k=5),
        disclosure=_ms.STRUCTURE_DISCLOSURE,
    ),
    "FVG3": IndicatorDefinition(
        "FVG3", "FVG", "overlay", 3, "MarketStructure",
        lambda bars: _ms.fvg(bars),
        disclosure=_ms.STRUCTURE_DISCLOSURE,
    ),
    "OBPATTERN": IndicatorDefinition(
        "OBPATTERN", "Order Blocks (Pattern)", "overlay", 21, "MarketStructure",
        lambda bars: _ms.order_block_pattern(bars),
        disclosure=_ms.STRUCTURE_DISCLOSURE,
    ),
    "ZSCORE20": IndicatorDefinition(
        "ZSCORE20", "Z-Score", "overlay", 20, "Statistics",
        lambda bars: _ind.zscore(bars, n=20),
    ),
    "PCTRANK20": IndicatorDefinition(
        "PCTRANK20", "Percentile", "overlay", 20, "Statistics",
        lambda bars: _ind.percentile_rank(bars, n=20),
    ),
    "REGCHAN20": IndicatorDefinition(
        "REGCHAN20", "Reg Chan", "overlay", 20, "Statistics",
        lambda bars: _ind.linear_regression(bars, n=20),
    ),
}


def known_indicator_ids() -> tuple[str, ...]:
    return tuple(INDICATOR_REGISTRY)
