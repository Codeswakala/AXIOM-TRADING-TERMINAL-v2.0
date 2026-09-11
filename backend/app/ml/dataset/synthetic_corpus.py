"""Deterministic synthetic corpus generator (BO-B-01.1).

Produces the labeled synthetic corpus this unit ingests: zero-mean random
walks in the same discipline as the chart seeder (per-market-class step
sigma, no drift), explicitly labeled ``source = "synthetic"``. Deterministic
per (market_class, symbol, seed) so ITRGA can regenerate byte-identical CSVs.

Honesty rule (B-01.1a): these rows are SYNTHETIC — they may close
pipeline-validation work only, never a research conclusion.
"""

from __future__ import annotations

import csv
import random
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path
from typing import Sequence

from app.ml.dataset.market_data_query import MarketSeriesKey

CORPUS_BASE_TIME = datetime(2025, 6, 1, 0, 0, tzinfo=timezone.utc)
CORPUS_SOURCE = "synthetic"
CORPUS_PROVIDER = "internal"

# Per-market-class zero-mean step sigma (matches chart_seed_service discipline):
# crypto gauss(0, 0.0083) · JPY-quote gauss(0, 0.015) · other forex gauss(0, 0.00015)
_CORPUS_SPECS: tuple[tuple[str, str, str, str], ...] = (
    # (market_class, symbol, base_price, step_kind)
    ("forex", "EURUSD", "1.10000", "forex"),
    ("forex", "GBPUSD", "1.27000", "forex"),
    ("forex", "USDJPY", "150.000", "jpy"),
    ("crypto", "BTCUSD", "65000.00", "crypto"),
    ("crypto", "ETHUSD", "3200.00", "crypto"),
)

CORPUS_SERIES_KEYS: tuple[MarketSeriesKey, ...] = tuple(
    MarketSeriesKey(
        market_class=market_class,
        provider=CORPUS_PROVIDER,
        symbol=symbol,
        timeframe="H1",
    )
    for market_class, symbol, _base, _kind in _CORPUS_SPECS
)


@dataclass(frozen=True, slots=True)
class SyntheticBar:
    """One generated corpus bar — attribute-shaped so both
    DatasetService.freeze_from_candles and the CSV writer can consume it."""

    market_class: str
    symbol: str
    timeframe: str
    open_time: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    source: str
    record_id: str


def _step_sigma(market_class: str, symbol: str) -> Decimal:
    if market_class == "crypto":
        return Decimal("0.0083")
    if market_class == "forex" and symbol.endswith("JPY"):
        return Decimal("0.015")
    return Decimal("0.00015")


def generate_series(
    *,
    market_class: str,
    symbol: str,
    bars: int,
    timeframe: str = "H1",
    seed: int = 20260819,
    base_time: datetime = CORPUS_BASE_TIME,
) -> list[SyntheticBar]:
    """Deterministic zero-mean synthetic series with honest labels."""
    spec = next(
        (s for s in _CORPUS_SPECS if s[0] == market_class and s[1] == symbol),
        None,
    )
    base_price = Decimal(spec[2]) if spec else Decimal("1.00000")
    rng = random.Random(f"b01-corpus:{market_class}:{symbol}:{seed}")
    sigma = _step_sigma(market_class, symbol)
    price = base_price
    out: list[SyntheticBar] = []
    for index in range(bars):
        open_ = price
        step = Decimal(str(rng.gauss(0.0, float(sigma))))
        close = open_ + step
        if market_class == "crypto":
            close = close.quantize(Decimal("0.01"))
            wick = abs(step) / Decimal("2")
            high = max(open_, close) + wick
            low = min(open_, close) - wick
            volume = Decimal("100") + Decimal(index % 17)
        elif market_class == "forex" and symbol.endswith("JPY"):
            close = close.quantize(Decimal("0.001"))
            high = max(open_, close) + Decimal("0.005")
            low = min(open_, close) - Decimal("0.005")
            volume = Decimal("1000") + Decimal(index % 71)
        else:
            close = close.quantize(Decimal("0.00001"))
            high = max(open_, close) + Decimal("0.00005")
            low = min(open_, close) - Decimal("0.00005")
            volume = Decimal("1000") + Decimal(index % 53)
        out.append(
            SyntheticBar(
                market_class=market_class,
                symbol=symbol,
                timeframe=timeframe,
                open_time=base_time + timedelta(hours=index),
                open=open_,
                high=high,
                low=low,
                close=close,
                volume=volume,
                source=CORPUS_SOURCE,
                record_id=f"b01-synth-{market_class}-{symbol}-{index:05d}",
            )
        )
        price = close
    return out


def write_corpus_csv(path: str | Path, bars: Sequence[SyntheticBar]) -> None:
    """Write corpus bars as an ingestion-seam CSV (alias-compatible header)."""
    path = Path(path)
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["timestamp", "open", "high", "low", "close", "volume"])
        for bar in bars:
            writer.writerow(
                [
                    bar.open_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    format(bar.open, "f"),
                    format(bar.high, "f"),
                    format(bar.low, "f"),
                    format(bar.close, "f"),
                    format(bar.volume, "f"),
                ]
            )
