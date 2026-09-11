"""DATA-P02 server-side OHLC aggregation — M1 → M5/M15/H1/H4/D1 (F-DATA2-1 fix).

Semantics per bucket (M1):
  open   = first constituent's open   (by open_time)
  high   = max(high)
  low    = min(low)
  close  = LAST constituent's close   (by open_time)
  volume = sum(volume)

Buckets are wall-clock aligned (M1): an H1 bucket starts on the UTC hour, a
D1 bucket at UTC midnight — never "every Nth row in the result set".

Partial-bucket rule (M6, stated for the record): a bucket with fewer than the
full complement of constituent minutes is INCOMPLETE and is never rendered.
Complete buckets form the series; the count of excluded partial buckets is
returned alongside and disclosed by the caller. No padding of any kind —
a partial bucket presented as a complete bar is a wrong price at bar
granularity.

Provenance (R4): aggregated bars carry only the existing provenance values;
a bucket mixing sources joins them ("seed:synthetic+live:simulated"), never
a new or weaker marker.

Determinism (S1): constituents are sorted by open_time inside each bucket and
bar ids are derived from (symbol, target timeframe, bucket start), so the
output is identical regardless of input row ordering or repeat calls.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Iterable, Protocol

from app.core.logging import get_logger
from app.core.time import require_utc

logger = get_logger(__name__, category="MARKET")


class _M1Bar(Protocol):
    market_class: str
    symbol: str
    open_time: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal | None
    source: str | None


@dataclass(frozen=True)
class AggregatedBar:
    id: str
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
    complete: bool
    constituents: int


@dataclass(frozen=True)
class BucketSummary:
    """Per-bucket accounting — includes incomplete buckets so callers can
    disclose them, never silently."""

    open_time: datetime
    constituents: int
    complete: bool


@dataclass(frozen=True)
class AggregationOutcome:
    bars: tuple[AggregatedBar, ...]
    buckets: tuple[BucketSummary, ...]
    excluded_partial: int
    unaggregated_total: int


def bucket_start_for(open_time: datetime, minutes: int) -> datetime:
    """Floor a UTC datetime to the wall-clock bucket boundary.

    Intraday buckets align to UTC midnight (hour/minute multiples); the daily
    bucket aligns to the UTC day.
    """
    normalized = require_utc(open_time, boundary="ohlcv_aggregation.bucket_start_for")
    assert normalized is not None
    if minutes >= 1440:
        return normalized.replace(hour=0, minute=0, second=0, microsecond=0)
    total = normalized.hour * 60 + normalized.minute
    floored = (total // minutes) * minutes
    return normalized.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(
        minutes=floored
    )


def joined_provenance(sources: Iterable[str | None]) -> str:
    """R4: join distinct constituent sources deterministically — never invent.

    Canonical order mirrors the UI's provenance vocabulary (seed first, then
    live); any other markers follow alphabetically."""
    distinct = {s for s in sources if s}
    canonical = [s for s in ("seed:synthetic", "live:simulated") if s in distinct]
    remainder = sorted(distinct - set(canonical))
    return "+".join(canonical + remainder)


def aggregate_m1_to_target(
    candles: Iterable[_M1Bar],
    *,
    target_minutes: int,
    target_timeframe: str,
) -> AggregationOutcome:
    """Aggregate M1 bars into wall-clock-aligned buckets of `target_minutes`."""
    grouped: dict[datetime, list[_M1Bar]] = defaultdict(list)
    unaggregated_total = 0
    naive_assumed = 0
    for candle in candles:
        raw = candle.open_time
        if raw.tzinfo is None or raw.tzinfo.utcoffset(raw) is None:
            # SQLite driver serialization strips tzinfo; every write path
            # normalises open_time to UTC before storage, so assuming UTC on
            # read preserves the invariant. Assumption counted and logged
            # once per aggregation call, never silently per row.
            normalized = raw.replace(tzinfo=timezone.utc)
            naive_assumed += 1
        else:
            normalized = raw.astimezone(timezone.utc)
        key = bucket_start_for(normalized, target_minutes)
        grouped[key].append(candle)
        unaggregated_total += 1
    if naive_assumed:
        logger.warning(
            "Naive datetimes assumed UTC at aggregation boundary (SQLite driver serialization): %s rows",
            naive_assumed,
        )

    bucket_keys = sorted(grouped)
    summaries: list[BucketSummary] = []
    bars: list[AggregatedBar] = []
    excluded_partial = 0

    for key in bucket_keys:
        constituents = sorted(grouped[key], key=lambda c: c.open_time)
        complete = len(constituents) == target_minutes
        summaries.append(
            BucketSummary(open_time=key, constituents=len(constituents), complete=complete)
        )
        if not complete:
            excluded_partial += 1
            continue

        first = constituents[0]
        last = constituents[-1]
        symbol = first.symbol
        volume = sum((c.volume for c in constituents if c.volume is not None), Decimal("0"))
        bar = AggregatedBar(
            id=f"agg:{symbol}:{target_timeframe}:{key:%Y%m%d%H%M}",
            market_class=first.market_class,
            symbol=symbol,
            timeframe=target_timeframe,
            open_time=key,
            open=first.open,
            high=max((c.high for c in constituents), default=first.high),
            low=min((c.low for c in constituents), default=first.low),
            close=last.close,
            volume=volume,
            source=joined_provenance(c.source for c in constituents),
            complete=True,
            constituents=len(constituents),
        )
        bars.append(bar)

    return AggregationOutcome(
        bars=tuple(bars),
        buckets=tuple(summaries),
        excluded_partial=excluded_partial,
        unaggregated_total=unaggregated_total,
    )
