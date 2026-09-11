"""Pydantic schemas for the CHART-P01 indicator-series endpoint (M4/M6).

The per-indicator result is a discriminated union on `shape`:
  line         — single value per bar (SMA/EMA/RSI/ATR)
  band         — upper/middle/lower per bar (Bollinger)
  macd         — macd/signal/histogram per bar (signal/histogram null until
                 the signal line is seeded — absence, never 0)
  insufficient — typed: required vs available bars, no points, no padding

The envelope carries the DATA-P02 series kind the computation ran over —
an indicator computed over an aggregated series is disclosed as such, and
an unavailable series yields no indicator computation at all.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field, field_validator


class LinePointRead(BaseModel):
    time: datetime
    value: Decimal | None


class BandPointRead(BaseModel):
    time: datetime
    upper: Decimal | None
    middle: Decimal | None
    lower: Decimal | None


class MacdPointRead(BaseModel):
    time: datetime
    macd: Decimal | None
    signal: Decimal | None
    histogram: Decimal | None


class LineIndicatorRead(BaseModel):
    shape: Literal["line"] = "line"
    kind: Literal["computed"] = "computed"
    points: list[LinePointRead]


class MultiIndicatorRead(BaseModel):
    """CHART-P02: multi-line indicators (Ichimoku, ADX/DMI, Keltner, Donchian,
    stochastic, levels) — named line series, each with typed points."""

    shape: Literal["multi"] = "multi"
    kind: Literal["computed"] = "computed"
    lines: dict[str, list[LinePointRead]]


class BandIndicatorRead(BaseModel):
    shape: Literal["band"] = "band"
    kind: Literal["computed"] = "computed"
    points: list[BandPointRead]


class MacdIndicatorRead(BaseModel):
    shape: Literal["macd"] = "macd"
    kind: Literal["computed"] = "computed"
    points: list[MacdPointRead]


class InsufficientIndicatorRead(BaseModel):
    shape: Literal["insufficient"] = "insufficient"
    required: int
    available: int
    # Optional context (CHART-P02): e.g. session levels are not resolvable at
    # this timeframe. Never rendered as a value — text disclosure only.
    detail: str | None = None


IndicatorRead = Annotated[
    Union[
        LineIndicatorRead,
        MultiIndicatorRead,
        BandIndicatorRead,
        MacdIndicatorRead,
        InsufficientIndicatorRead,
    ],
    Field(discriminator="shape"),
]


class IndicatorSeriesEnvelope(BaseModel):
    """Top-level response: series provenance (M6) + per-indicator results.

    seriesKind="unavailable" means the underlying series could not be formed;
    `indicators` is then empty and `detail` states the reason — an indicator
    is NEVER computed over an unavailable series."""

    symbol: str
    timeframe: str
    seriesKind: Literal["native", "aggregated", "unavailable"]
    sourceTimeframe: str | None = None
    excludedPartialBuckets: int | None = None
    detail: str | None = None
    indicators: dict[str, IndicatorRead] = Field(default_factory=dict)

    @field_validator("detail")
    @classmethod
    def _no_whitespace_detail(cls, value: str | None) -> str | None:
        return value.strip() if value else None
