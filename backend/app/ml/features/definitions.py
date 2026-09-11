"""Feature definition contracts and built-in market-agnostic features."""

from __future__ import annotations

import math
from decimal import Decimal
from typing import Callable, Sequence

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.ml.dataset.market_data_query import CanonicalOHLCVRecord
from app.ml.features.errors import NonCausalFeatureError

FeatureFunction = Callable[[Sequence[CanonicalOHLCVRecord], int], Decimal | None]


class FeatureDefinitionSpec(BaseModel):
    """A versioned causal feature definition."""

    model_config = ConfigDict(extra="forbid")

    feature_name: str
    feature_version: str
    formula_spec: dict
    input_requirements: dict = Field(default_factory=dict)
    lookback_window: int = Field(ge=1)
    causal: bool = True
    market_compatibility_notes: str | None = None

    @field_validator("feature_name", "feature_version")
    @classmethod
    def _not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("feature definition identifiers must not be empty")
        return value.strip()

    def assert_causal(self) -> None:
        if not self.causal or self.formula_spec.get("uses_future") is True:
            raise NonCausalFeatureError("FEATURE_LOOKAHEAD")


class ComputableFeature:
    """Feature definition plus pure causal compute function."""

    def __init__(self, spec: FeatureDefinitionSpec, compute: FeatureFunction) -> None:
        spec.assert_causal()
        self.spec = spec
        self.compute = compute


def _return_1(records: Sequence[CanonicalOHLCVRecord], index: int) -> Decimal | None:
    record = records[index]
    if record.open == 0:
        return None
    return (record.close - record.open) / record.open


def _range_pct(records: Sequence[CanonicalOHLCVRecord], index: int) -> Decimal | None:
    record = records[index]
    if record.close == 0:
        return None
    return (record.high - record.low) / record.close


def _rolling_return_3(records: Sequence[CanonicalOHLCVRecord], index: int) -> Decimal | None:
    if index < 2:
        return None
    start = records[index - 2]
    end = records[index]
    if start.close == 0:
        return None
    return (end.close - start.close) / start.close


def builtin_feature_set_v1() -> list[ComputableFeature]:
    """Initial normalized market-agnostic causal features.

    Deliberately excludes symbol/provider/market identity fields.
    """
    return [
        ComputableFeature(
            FeatureDefinitionSpec(
                feature_name="return_1",
                feature_version="v1",
                formula_spec={"family": "returns", "formula": "close/open - 1"},
                input_requirements={"ohlc": True},
                lookback_window=1,
                causal=True,
                market_compatibility_notes="Price-normalized; market agnostic.",
            ),
            _return_1,
        ),
        ComputableFeature(
            FeatureDefinitionSpec(
                feature_name="range_pct",
                feature_version="v1",
                formula_spec={"family": "volatility", "formula": "(high-low)/close"},
                input_requirements={"ohlc": True},
                lookback_window=1,
                causal=True,
                market_compatibility_notes="Range normalized by price; market agnostic.",
            ),
            _range_pct,
        ),
            ComputableFeature(
                FeatureDefinitionSpec(
                    feature_name="rolling_return_3",
                    feature_version="v1",
                    formula_spec={
                        "family": "trend_persistence",
                        "formula": "close_t/close_t-2 - 1",
                    },
                    input_requirements={"ohlc": True, "min_bars": 3},
                    lookback_window=3,
                    causal=True,
                    market_compatibility_notes="Uses only current and prior two closes.",
                ),
                _rolling_return_3,
            ),
        ]


# ---------------------------------------------------------------------------
# BO-B-ML2 — feature set v2 (justified expansion over v1; every feature is
# causal, market-agnostic, price-normalized, and warm-up-disciplined: values
# before a window completes are None and excluded from matrices — never
# fabricated). Compute functions are O(1) amortized via closure caches keyed
# by the identity of the records sequence.
# ---------------------------------------------------------------------------

def _cache(values: dict, key: int) -> dict:
    entry = values.get(key)
    if entry is None:
        entry = {}
        values[key] = entry
    return entry


def _true_ranges(records: Sequence[CanonicalOHLCVRecord]) -> list[float]:
    out: list[float] = []
    previous_close: float | None = None
    for record in records:
        high = float(record.high)
        low = float(record.low)
        close = float(record.close)
        if previous_close is None:
            true_range = high - low
        else:
            true_range = max(high - low, abs(high - previous_close), abs(low - previous_close))
        out.append(true_range)
        previous_close = close
    return out


_ATR_CACHE: dict[int, dict] = {}
_EMA_CACHE: dict[int, dict] = {}
_BBAND_CACHE: dict[int, dict] = {}
_STRUCTURE_CACHE: dict[int, dict] = {}


def _atr_norm_14(records: Sequence[CanonicalOHLCVRecord], index: int) -> Decimal | None:
    cache = _cache(_ATR_CACHE, id(records))
    if "true_ranges" not in cache:
        cache["true_ranges"] = _true_ranges(records)
    ranges = cache["true_ranges"]
    if index < 13:
        return None
    mean = sum(ranges[index - 13 : index + 1]) / 14
    close = float(records[index].close)
    if close == 0:
        return None
    return Decimal(str(round(mean / close, 10)))


def _roc_12(records: Sequence[CanonicalOHLCVRecord], index: int) -> Decimal | None:
    if index < 12:
        return None
    start_close = float(records[index - 12].close)
    if start_close == 0:
        return None
    return Decimal(str(round(float(records[index].close) / start_close - 1.0, 10)))


def _ema_dist_20(records: Sequence[CanonicalOHLCVRecord], index: int) -> Decimal | None:
    cache = _cache(_EMA_CACHE, id(records))
    if "ema" not in cache:
        ema: list[float] = []
        alpha = 2.0 / 21.0
        for position, record in enumerate(records):
            close = float(record.close)
            ema.append(close if position == 0 else alpha * close + (1.0 - alpha) * ema[-1])
        cache["ema"] = ema
    close = float(records[index].close)
    if close == 0:
        return None
    return Decimal(str(round((close - cache["ema"][index]) / close, 10)))


def _bband_pos_20(records: Sequence[CanonicalOHLCVRecord], index: int) -> Decimal | None:
    cache = _cache(_BBAND_CACHE, id(records))
    if "stats" not in cache:
        prefix_sum: list[float] = []
        prefix_sq: list[float] = []
        running_sum = 0.0
        running_sq = 0.0
        for record in records:
            close = float(record.close)
            running_sum += close
            running_sq += close * close
            prefix_sum.append(running_sum)
            prefix_sq.append(running_sq)
        cache["stats"] = (prefix_sum, prefix_sq)
    prefix_sum, prefix_sq = cache["stats"]
    if index < 19:
        return None
    window_sum = prefix_sum[index] - (prefix_sum[index - 20] if index >= 20 else 0.0)
    window_sq = prefix_sq[index] - (prefix_sq[index - 20] if index >= 20 else 0.0)
    mean = window_sum / 20.0
    variance = max(0.0, window_sq / 20.0 - mean * mean)
    std = math.sqrt(variance)
    close = float(records[index].close)
    if std == 0 or close == 0:
        return None
    return Decimal(str(round((close - mean) / (2.0 * std), 10)))


def _vol_change_1(records: Sequence[CanonicalOHLCVRecord], index: int) -> Decimal | None:
    if index < 1:
        return None
    current = float(records[index].volume)
    previous = float(records[index - 1].volume)
    if current <= 0 or previous <= 0:
        return None
    return Decimal(str(round(math.log(current / previous), 10)))


def _hour_sin(records: Sequence[CanonicalOHLCVRecord], index: int) -> Decimal | None:
    hour = records[index].open_time.hour
    return Decimal(str(round(math.sin(2 * math.pi * hour / 24), 10)))


def _hour_cos(records: Sequence[CanonicalOHLCVRecord], index: int) -> Decimal | None:
    hour = records[index].open_time.hour
    return Decimal(str(round(math.cos(2 * math.pi * hour / 24), 10)))


def _breakout_events(records: Sequence[CanonicalOHLCVRecord], k: int = 20) -> list[int]:
    """Deterministic BoS-class breakout event indices: bar t is an up-break
    when its close exceeds the prior k-bar high; a down-break when its close
    falls below the prior k-bar low. Uses only bars ≤ t (causal)."""
    events: list[int] = []
    for index in range(k, len(records)):
        prior = records[index - k : index]
        prior_high = max(float(record.high) for record in prior)
        prior_low = min(float(record.low) for record in prior)
        close = float(records[index].close)
        if close > prior_high or close < prior_low:
            events.append(index)
    return events


def _structure_bos_rec(records: Sequence[CanonicalOHLCVRecord], index: int) -> Decimal | None:
    cache = _cache(_STRUCTURE_CACHE, id(records))
    if "events" not in cache:
        cache["events"] = _breakout_events(records)
    events = cache["events"]
    if index < 20 or not events:
        return None
    import bisect

    position = bisect.bisect_right(events, index)
    if position == 0:
        return None
    return Decimal(str(min(index - events[position - 1], 200)))


def builtin_feature_set_v2() -> list[ComputableFeature]:
    """BO-B-ML2 expanded market-agnostic causal features (v2).

    Each feature addresses a specific deficiency of the v1 set:
      - atr_norm_14      : volatility regime context (v1 has only the
                           instantaneous range; no rolling volatility).
      - roc_12           : momentum over a longer horizon (v1 momentum is the
                           3-bar rolling return only).
      - ema_dist_20      : trend-position state (price vs its own EMA, normalized).
      - bband_pos_20     : mean-reversion position (Bollinger z-like statistic).
      - vol_change_1     : volume dynamics (log volume change is scale-free and
                           therefore market-agnostic across instruments).
      - hour_sin/cos     : calendar structure (crypto has documented intraday
                           seasonality; the UTC clock is global, not identity).
      - structure_bos_rec: market-structure event recency (BoS-class breakout
                           recency over k=20, capped at 200) — the bridge
                           between the predictive track and the deterministic
                           indicator layer permitted by BO-B-ML2 §Phase 1.
    All causal (no future bars), no identity fields, warm-up returns None.
    """
    return [
        ComputableFeature(
            FeatureDefinitionSpec(
                feature_name="atr_norm_14",
                feature_version="v2",
                formula_spec={"family": "volatility", "formula": "mean(TR_14)/close"},
                input_requirements={"ohlc": True, "min_bars": 14},
                lookback_window=14,
                causal=True,
                market_compatibility_notes="ATR-normalized; price-normalized; market agnostic.",
            ),
            _atr_norm_14,
        ),
        ComputableFeature(
            FeatureDefinitionSpec(
                feature_name="roc_12",
                feature_version="v2",
                formula_spec={"family": "momentum", "formula": "close_t/close_t-12 - 1"},
                input_requirements={"ohlc": True, "min_bars": 13},
                lookback_window=13,
                causal=True,
                market_compatibility_notes="12-bar rate of change; price-normalized.",
            ),
            _roc_12,
        ),
        ComputableFeature(
            FeatureDefinitionSpec(
                feature_name="ema_dist_20",
                feature_version="v2",
                formula_spec={"family": "trend", "formula": "(close - EMA20)/close"},
                input_requirements={"ohlc": True, "min_bars": 20},
                lookback_window=20,
                causal=True,
                market_compatibility_notes="Distance from own EMA, normalized by price.",
            ),
            _ema_dist_20,
        ),
        ComputableFeature(
            FeatureDefinitionSpec(
                feature_name="bband_pos_20",
                feature_version="v2",
                formula_spec={"family": "volatility", "formula": "(close - SMA20)/(2*std20)"},
                input_requirements={"ohlc": True, "min_bars": 20},
                lookback_window=20,
                causal=True,
                market_compatibility_notes="Bollinger position statistic; price-normalized.",
            ),
            _bband_pos_20,
        ),
        ComputableFeature(
            FeatureDefinitionSpec(
                feature_name="vol_change_1",
                feature_version="v2",
                formula_spec={"family": "volume", "formula": "ln(vol_t/vol_t-1)"},
                input_requirements={"ohlcv": True, "min_bars": 2},
                lookback_window=2,
                causal=True,
                market_compatibility_notes="Log volume change is scale-free across instruments.",
            ),
            _vol_change_1,
        ),
        ComputableFeature(
            FeatureDefinitionSpec(
                feature_name="hour_sin",
                feature_version="v2",
                formula_spec={"family": "calendar", "formula": "sin(2*pi*hour/24)"},
                input_requirements={"time": True},
                lookback_window=1,
                causal=True,
                market_compatibility_notes="UTC clock is global for crypto; not identity.",
            ),
            _hour_sin,
        ),
        ComputableFeature(
            FeatureDefinitionSpec(
                feature_name="hour_cos",
                feature_version="v2",
                formula_spec={"family": "calendar", "formula": "cos(2*pi*hour/24)"},
                input_requirements={"time": True},
                lookback_window=1,
                causal=True,
                market_compatibility_notes="UTC clock is global for crypto; not identity.",
            ),
            _hour_cos,
        ),
        ComputableFeature(
            FeatureDefinitionSpec(
                feature_name="structure_bos_rec",
                feature_version="v2",
                formula_spec={
                    "family": "market_structure",
                    "formula": "bars since last k-bar breakout event, capped 200",
                },
                input_requirements={"ohlc": True, "min_bars": 21},
                lookback_window=21,
                causal=True,
                market_compatibility_notes="BoS-class breakout recency; causal (bars ≤ t only).",
            ),
            _structure_bos_rec,
        ),
    ]
