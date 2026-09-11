"""CHART-P03 Market Structure — geometric pattern detections over simulated
OHLC (M7/M8/M9).

CONSTITUTIONAL NAMING (M8, binding): these are GEOMETRIC PATTERN DETECTIONS
over simulated data. "Order Block" and every other conventional label here is
retained ONLY for recognisability; the surface must state plainly that the
patterns are geometries detected on a simulated feed — NOT evidence of
institutional activity, order placement, accumulation or distribution. There
are no institutions and no orders on a gauss() feed.

Every detection rule is declared here exactly as the hand-computed tests pin
it:

  SWINGS (k=5)  — bar i is a swing HIGH iff high[i] > high[j] for ALL j in
                  [i-5, i+5], j != i (strict); swing LOW symmetric. The last
                  k bars cannot be confirmed and emit nothing.
  STRUCT        — each confirmed swing is classified against the previous
                  swing of the SAME kind: higher high -> HH else LH; higher
                  low -> HL else LL. First of each kind unclassified.
  BOS           — BOS-up at bar i iff close[i] strictly exceeds the most
                  recent confirmed swing-high level (a swing bar cannot break
                  itself: close <= its own high); BOS-down symmetric.
  CHoCH         — the FIRST BOS whose direction differs from the previous BOS
                  is a change of character, emitted at that bar with the
                  broken level.
  FVG           — bullish gap at bar i (i>=2) iff low[i] > high[i-2]; zone
                  top = low[i], bottom = high[i-2] (bearish mirror). Zones
                  carry their levels while unfilled: bullish fills when a
                  close trades <= bottom; bearish fills when a close trades
                  >= top; max span 50 bars.
  OB PATTERN    — bullish pattern at bar i iff bar[i-1] is bearish
                  (close < open), close[i] > high[i-1] and range[i] >= 1.5 x
                  the MEDIAN range of the previous 20 bars; zone =
                  [low[i-1], high[i-1]]; unfilled until a close trades below
                  the zone bottom; max span 50 bars.

Full-definition required_bars (M3/M9, declared): SWINGS 2k+1 = 11 · STRUCT
5k+4 = 29 (four confirmed swings at worst-case spacing) · BOS 2k+2 = 12
(confirmed swing + one break bar) · CHoCH 4k+4 = 24 (two BOS breaks) · FVG 3
· OB 21 (20-bar window + 1).
"""

from __future__ import annotations

from app.services.indicators import (
    IndicatorSeries,
    LinePoint,
    _dec,
    _field,
    _sorted_bars,
    _utc,
)

STRUCTURE_DISCLOSURE = (
    "Geometric pattern detection over simulated OHLC — not evidence of "
    "institutional activity or order placement."
)

FVG_MAX_SPAN = 50
OB_MAX_SPAN = 50


def _line_pts(ordered: list, values: list[float | None]) -> list[LinePoint]:
    return [
        LinePoint(time=_utc(_field(b, "open_time")), value=_dec(v) if v is not None else None)
        for b, v in zip(ordered, values)
    ]


def swings(bars: list, k: int = 5) -> IndicatorSeries:
    ordered = _sorted_bars(bars)
    required = 2 * k + 1
    if len(ordered) < required:
        return IndicatorSeries(kind="insufficient", required=required, available=len(ordered))
    n = len(ordered)
    highs = [_field(b, "high") for b in ordered]
    lows = [_field(b, "low") for b in ordered]
    sh: list[float | None] = [None] * n
    sl: list[float | None] = [None] * n
    for i in range(k, n - k):
        h = highs[i]
        if all(h > highs[j] for j in range(i - k, i + k + 1) if j != i):
            sh[i] = float(h)
        l = lows[i]
        if all(l < lows[j] for j in range(i - k, i + k + 1) if j != i):
            sl[i] = float(l)
    return IndicatorSeries(
        kind="computed",
        lines={"swing_high": _line_pts(ordered, sh), "swing_low": _line_pts(ordered, sl)},
        required=required,
        available=n,
    )


def struct(bars: list, k: int = 5) -> IndicatorSeries:
    ordered = _sorted_bars(bars)
    required = 5 * k + 4
    if len(ordered) < required:
        return IndicatorSeries(kind="insufficient", required=required, available=len(ordered))
    base = swings(ordered, k=k)
    sh = [None if p.value is None else float(p.value) for p in base.lines["swing_high"]]
    sl = [None if p.value is None else float(p.value) for p in base.lines["swing_low"]]
    n = len(ordered)
    hh: list[float | None] = [None] * n
    lh: list[float | None] = [None] * n
    hl: list[float | None] = [None] * n
    ll: list[float | None] = [None] * n
    prev_high: float | None = None
    prev_low: float | None = None
    for i in range(n):
        if sh[i] is not None:
            if prev_high is not None:
                if sh[i] > prev_high:
                    hh[i] = sh[i]
                else:
                    lh[i] = sh[i]
            prev_high = sh[i]
        if sl[i] is not None:
            if prev_low is not None:
                if sl[i] > prev_low:
                    hl[i] = sl[i]
                else:
                    ll[i] = sl[i]
            prev_low = sl[i]
    return IndicatorSeries(
        kind="computed",
        lines={
            "hh": _line_pts(ordered, hh),
            "lh": _line_pts(ordered, lh),
            "hl": _line_pts(ordered, hl),
            "ll": _line_pts(ordered, ll),
        },
        required=required,
        available=n,
    )


def bos(bars: list, k: int = 5) -> IndicatorSeries:
    ordered = _sorted_bars(bars)
    required = 2 * k + 2
    if len(ordered) < required:
        return IndicatorSeries(kind="insufficient", required=required, available=len(ordered))
    base = swings(ordered, k=k)
    sh = [None if p.value is None else float(p.value) for p in base.lines["swing_high"]]
    sl = [None if p.value is None else float(p.value) for p in base.lines["swing_low"]]
    n = len(ordered)
    up: list[float | None] = [None] * n
    down: list[float | None] = [None] * n
    last_high: float | None = None
    last_low: float | None = None
    for i in range(n):
        if sh[i] is not None:
            last_high = sh[i]
        if sl[i] is not None:
            last_low = sl[i]
        close = float(_field(ordered[i], "close"))
        if last_high is not None and close > last_high:
            up[i] = last_high
        if last_low is not None and close < last_low:
            down[i] = last_low
    return IndicatorSeries(
        kind="computed",
        lines={"bos_up": _line_pts(ordered, up), "bos_down": _line_pts(ordered, down)},
        required=required,
        available=n,
    )


def choch(bars: list, k: int = 5) -> IndicatorSeries:
    ordered = _sorted_bars(bars)
    required = 4 * k + 4
    if len(ordered) < required:
        return IndicatorSeries(kind="insufficient", required=required, available=len(ordered))
    base = bos(ordered, k=k)
    up = [None if p.value is None else float(p.value) for p in base.lines["bos_up"]]
    down = [None if p.value is None else float(p.value) for p in base.lines["bos_down"]]
    n = len(ordered)
    cu: list[float | None] = [None] * n
    cd: list[float | None] = [None] * n
    last_dir: str | None = None
    for i in range(n):
        if up[i] is not None:
            if last_dir == "down":
                cu[i] = up[i]
            last_dir = "up"
        if down[i] is not None:
            if last_dir == "up":
                cd[i] = down[i]
            last_dir = "down"
    return IndicatorSeries(
        kind="computed",
        lines={"choch_up": _line_pts(ordered, cu), "choch_down": _line_pts(ordered, cd)},
        required=required,
        available=n,
    )


def fvg(bars: list) -> IndicatorSeries:
    ordered = _sorted_bars(bars)
    required = 3
    if len(ordered) < required:
        return IndicatorSeries(kind="insufficient", required=required, available=len(ordered))
    n = len(ordered)
    top: list[float | None] = [None] * n
    bottom: list[float | None] = [None] * n
    active: list[dict] = []  # {"top":, "bottom":, "bullish": bool, "since": i}
    for i in range(n):
        close = float(_field(ordered[i], "close"))
        # Fill FIRST: a bar that trades through the gap fills the zone — the
        # zone does not emit on its filling bar.
        active = [
            z
            for z in active
            if not ((z["bullish"] and close <= z["bottom"]) or (not z["bullish"] and close >= z["top"]))
        ]
        for zone in active:
            if i - zone["since"] > FVG_MAX_SPAN:
                continue
            top[i] = zone["top"]
            bottom[i] = zone["bottom"]
        if i >= 2:
            prev2_high = float(_field(ordered[i - 2], "high"))
            prev2_low = float(_field(ordered[i - 2], "low"))
            cur_low = float(_field(ordered[i], "low"))
            cur_high = float(_field(ordered[i], "high"))
            if cur_low > prev2_high:  # bullish gap
                active.append({"top": cur_low, "bottom": prev2_high, "bullish": True, "since": i})
                top[i] = cur_low
                bottom[i] = prev2_high
            elif cur_high < prev2_low:  # bearish gap
                active.append({"top": prev2_low, "bottom": cur_high, "bullish": False, "since": i})
                top[i] = prev2_low
                bottom[i] = cur_high
    return IndicatorSeries(
        kind="computed",
        lines={"fvg_top": _line_pts(ordered, top), "fvg_bottom": _line_pts(ordered, bottom)},
        required=required,
        available=n,
    )


def order_block_pattern(bars: list) -> IndicatorSeries:
    ordered = _sorted_bars(bars)
    required = 21
    if len(ordered) < required:
        return IndicatorSeries(kind="insufficient", required=required, available=len(ordered))
    n = len(ordered)
    top: list[float | None] = [None] * n
    bottom: list[float | None] = [None] * n
    active: list[dict] = []
    for i in range(n):
        close = float(_field(ordered[i], "close"))
        active = [z for z in active if not close < z["bottom"]]
        for zone in active:
            if i - zone["since"] > OB_MAX_SPAN:
                continue
            top[i] = zone["top"]
            bottom[i] = zone["bottom"]
        if i >= 20:
            window = [ordered[j] for j in range(i - 20, i)]
            ranges = sorted(float(_field(b, "high")) - float(_field(b, "low")) for b in window)
            median_range = ranges[10]
            prev = ordered[i - 1]
            prev_close = float(_field(prev, "close"))
            prev_open = float(_field(prev, "open"))
            prev_high = float(_field(prev, "high"))
            prev_low = float(_field(prev, "low"))
            cur_range = float(_field(ordered[i], "high")) - float(_field(ordered[i], "low"))
            if (
                median_range > 0
                and prev_close < prev_open
                and close > prev_high
                and cur_range >= 1.5 * median_range
            ):
                active.append({"top": prev_high, "bottom": prev_low, "since": i})
                top[i] = prev_high
                bottom[i] = prev_low
    return IndicatorSeries(
        kind="computed",
        lines={"ob_top": _line_pts(ordered, top), "ob_bottom": _line_pts(ordered, bottom)},
        required=required,
        available=n,
    )
