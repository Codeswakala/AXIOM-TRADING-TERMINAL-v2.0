"""DATA-P02 fail-first tests: server-side OHLC aggregation (M1 → M5/M15/H1/H4/D1).

Written against the BUILD_ORDER_DATA-P02 contract. Every test here MUST fail
against the pre-DATA-P02 tree (no aggregation service, no timeframe vocabulary,
no typed candle-series envelope) and pass once the aggregation service ships.

F-DATA2-1 is the defect: the UI labels M1 bars as higher timeframes. These
tests pin the fix at the semantics level — first-open / max-high / min-low /
last-close / summed-volume, wall-clock bucket alignment, order-independent
determinism, partial-bucket disclosure, and the native/aggregated/unavailable
discriminant.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from decimal import Decimal

from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.db.models.candle import Candle
from app.db.session import session_scope
from app.services.ohlcv_aggregation import (
    aggregate_m1_to_target,
    bucket_start_for,
)
from app.services.timeframes import (
    TIMEFRAME_LABELS,
    TIMEFRAME_MINUTES,
    VALID_TIMEFRAMES,
)


def _m1(
    symbol: str,
    dt: datetime,
    o: str,
    h: str,
    l: str,
    c: str,
    vol: str = "10",
    source: str = "seed:synthetic",
) -> Candle:
    return Candle(
        market_class="forex",
        symbol=symbol,
        timeframe="M1",
        open_time=dt,
        open=Decimal(o),
        high=Decimal(h),
        low=Decimal(l),
        close=Decimal(c),
        volume=Decimal(vol),
        source=source,
    )


# --- S2 golden vocabulary -------------------------------------------------

def test_data_p02_timeframe_vocabulary_golden_table() -> None:
    """Single source of truth: the backend vocabulary is exactly six codes."""
    assert VALID_TIMEFRAMES == ("M1", "M5", "M15", "H1", "H4", "D1")
    assert TIMEFRAME_MINUTES == {"M1": 1, "M5": 5, "M15": 15, "H1": 60, "H4": 240, "D1": 1440}
    assert TIMEFRAME_LABELS == {
        "M1": "1m",
        "M5": "5m",
        "M15": "15m",
        "H1": "1h",
        "H4": "4h",
        "D1": "1d",
    }


# --- M1 semantics ---------------------------------------------------------

def test_data_p02_aggregation_ohlc_semantics_correct() -> None:
    """M1: open=first constituent open, high=max high, low=min low,
    close=LAST constituent close, volume=sum — asserted exactly on known input."""
    base = datetime(2026, 8, 17, 10, 0, tzinfo=timezone.utc)
    bars = [
        _m1("EURUSD", base + timedelta(minutes=0), "1.10000", "1.10500", "1.09900", "1.10100", "100"),
        _m1("EURUSD", base + timedelta(minutes=1), "1.10100", "1.10300", "1.10050", "1.10200", "200"),
        _m1("EURUSD", base + timedelta(minutes=2), "1.10200", "1.10800", "1.10100", "1.10400", "300"),
        _m1("EURUSD", base + timedelta(minutes=3), "1.10400", "1.10600", "1.10300", "1.10350", "400"),
        _m1("EURUSD", base + timedelta(minutes=4), "1.10350", "1.10400", "1.10000", "1.10200", "500"),
        # second bucket: 1 of 5 minutes — must be excluded, never padded
        _m1("EURUSD", base + timedelta(minutes=5), "2.00000", "2.01000", "1.99000", "2.00500", "50"),
    ]
    out = aggregate_m1_to_target(bars, target_minutes=5, target_timeframe="M5")
    assert out.excluded_partial == 1
    assert len(out.bars) == 1
    bar = out.bars[0]
    assert bar.open_time == base  # wall-clock aligned bucket start
    assert bar.open == Decimal("1.10000")
    assert bar.high == Decimal("1.10800")
    assert bar.low == Decimal("1.09900")
    assert bar.close == Decimal("1.10200")
    assert bar.volume == Decimal("1500")
    assert bar.constituents == 5
    assert bar.complete is True
    assert bar.source == "seed:synthetic"
    assert bar.timeframe == "M5"
    assert bar.symbol == "EURUSD"


def test_data_p02_aggregation_provenance_never_weakened() -> None:
    """R4: aggregated bars carry only the existing provenance values — joined
    when a bucket mixes sources, never a new or weaker marker, never null."""
    base = datetime(2026, 8, 17, 10, 0, tzinfo=timezone.utc)
    bars = [
        _m1("EURUSD", base + timedelta(minutes=i), "1.10000", "1.10500", "1.09900", "1.10100",
            source="seed:synthetic")
        for i in range(4)
    ]
    bars.append(
        _m1("EURUSD", base + timedelta(minutes=4), "1.10100", "1.10600", "1.10000", "1.10200",
            source="live:simulated")
    )
    out = aggregate_m1_to_target(bars, target_minutes=5, target_timeframe="M5")
    assert len(out.bars) == 1
    assert out.bars[0].source == "seed:synthetic+live:simulated"
    assert out.bars[0].source != "resampled"
    assert out.bars[0].source is not None


# --- M1 bucket boundaries -------------------------------------------------

def test_data_p02_aggregation_bucket_boundaries_wall_clock_aligned() -> None:
    """M1: buckets align to wall-clock intervals — an H1 bucket starts on the
    hour, a D1 bucket at UTC midnight — never to "every Nth row"."""
    cases = [
        (5, datetime(2026, 8, 17, 10, 0, tzinfo=timezone.utc), datetime(2026, 8, 17, 10, 0, tzinfo=timezone.utc)),
        (5, datetime(2026, 8, 17, 10, 4, tzinfo=timezone.utc), datetime(2026, 8, 17, 10, 0, tzinfo=timezone.utc)),
        (5, datetime(2026, 8, 17, 10, 5, tzinfo=timezone.utc), datetime(2026, 8, 17, 10, 5, tzinfo=timezone.utc)),
        (15, datetime(2026, 8, 17, 10, 14, tzinfo=timezone.utc), datetime(2026, 8, 17, 10, 0, tzinfo=timezone.utc)),
        (60, datetime(2026, 8, 17, 10, 59, tzinfo=timezone.utc), datetime(2026, 8, 17, 10, 0, tzinfo=timezone.utc)),
        (60, datetime(2026, 8, 17, 11, 0, tzinfo=timezone.utc), datetime(2026, 8, 17, 11, 0, tzinfo=timezone.utc)),
        (240, datetime(2026, 8, 17, 13, 59, tzinfo=timezone.utc), datetime(2026, 8, 17, 12, 0, tzinfo=timezone.utc)),
        (1440, datetime(2026, 8, 17, 23, 59, tzinfo=timezone.utc), datetime(2026, 8, 17, 0, 0, tzinfo=timezone.utc)),
        (1440, datetime(2026, 8, 18, 0, 0, tzinfo=timezone.utc), datetime(2026, 8, 18, 0, 0, tzinfo=timezone.utc)),
    ]
    for minutes, inp, expected in cases:
        assert bucket_start_for(inp, minutes) == expected, (minutes, inp)

    # Aggregate-level: bars spanning 09:58–10:03 must land in buckets
    # [09:55] (2 constituents) and [10:00] (4 constituents) — floor-aligned.
    base = datetime(2026, 8, 17, 9, 58, tzinfo=timezone.utc)
    bars = [
        _m1("EURUSD", base + timedelta(minutes=i), "1.10000", "1.10500", "1.09900", "1.10100")
        for i in range(6)
    ]
    out = aggregate_m1_to_target(bars, target_minutes=5, target_timeframe="M5")
    bucket_times = {b.open_time for b in out.buckets}
    assert datetime(2026, 8, 17, 9, 55, tzinfo=timezone.utc) in bucket_times
    assert datetime(2026, 8, 17, 10, 0, tzinfo=timezone.utc) in bucket_times
    # Neither bucket is complete (2/5 and 4/5): both are disclosed as partial,
    # no bar is emitted — floor alignment is proven via the bucket accounting.
    assert out.excluded_partial == 2
    assert len(out.bars) == 0
    assert {b.constituents for b in out.buckets} == {2, 4}


# --- S1 determinism -------------------------------------------------------

def test_data_p02_aggregation_deterministic_and_order_independent() -> None:
    """S1: identical output regardless of input row ordering or repeat calls."""
    base = datetime(2026, 8, 17, 10, 0, tzinfo=timezone.utc)

    def build() -> list[Candle]:
        bars: list[Candle] = []
        for i in range(5):
            o = Decimal("1.10000") + Decimal(i) / Decimal("100000")
            bars.append(
                _m1(
                    "EURUSD",
                    base + timedelta(minutes=i),
                    str(o),
                    str(o + Decimal("0.00050")),
                    str(o - Decimal("0.00050")),
                    str(o + Decimal("0.00020")),
                    str(100 + i),
                )
            )
        return bars

    forward = build()
    reversed_rows = list(reversed(build()))
    out_f = aggregate_m1_to_target(forward, target_minutes=5, target_timeframe="M5")
    out_r = aggregate_m1_to_target(reversed_rows, target_minutes=5, target_timeframe="M5")
    out_f2 = aggregate_m1_to_target(build(), target_minutes=5, target_timeframe="M5")

    def fingerprint(bars: list) -> list[tuple]:
        return [
            (b.id, b.open_time, b.open, b.high, b.low, b.close, b.volume, b.source, b.constituents)
            for b in bars
        ]

    assert fingerprint(out_f.bars) == fingerprint(out_r.bars)
    assert fingerprint(out_f.bars) == fingerprint(out_f2.bars)
    assert len(out_f.bars) == 1
    assert out_f.bars[0].constituents == 5


# --- M6 partial buckets ---------------------------------------------------

def test_data_p02_partial_bucket_disclosed_not_padded() -> None:
    """M6: an H1 bucket with 40 of 60 minutes is excluded and disclosed —
    never silently padded into a complete-looking bar."""
    base = datetime(2026, 8, 17, 0, 0, tzinfo=timezone.utc)
    bars: list[Candle] = []
    for hour, count in ((0, 60), (1, 40), (2, 60)):
        for minute in range(count):
            bars.append(
                _m1(
                    "EURUSD",
                    base + timedelta(hours=hour, minutes=minute),
                    "1.10000",
                    "1.10500",
                    "1.09900",
                    "1.10100",
                )
            )
    out = aggregate_m1_to_target(bars, target_minutes=60, target_timeframe="H1")
    assert out.excluded_partial == 1
    assert len(out.bars) == 2
    assert [b.open_time for b in out.bars] == [base, base + timedelta(hours=2)]
    assert all(b.complete for b in out.bars)
    # The incomplete hour-1 bucket must not appear in any form.
    assert base + timedelta(hours=1) not in [b.open_time for b in out.bars]
    assert all(b.constituents == 60 for b in out.bars)


# --- M4 typed series kind -------------------------------------------------

async def test_data_p02_aggregated_kind_from_controlled_window(
    prepared_db: None, async_client: AsyncClient
) -> None:
    """M4 aggregated: a controlled 120-minute M1 window must aggregate into
    exactly two complete H1 buckets via the API — and D1 for the same window
    is unavailable (insufficient coverage), not improvised.

    Fixture order matters: prepared_db (re-initialises the engine + schema)
    must resolve BEFORE async_client (whose lifespan bootstraps the admin
    operator into the current database)."""
    base = datetime(2026, 1, 5, 0, 0, tzinfo=timezone.utc)
    rows: list[Candle] = []
    for minute in range(120):
        rows.append(
            _m1(
                "TESTAGG",
                base + timedelta(minutes=minute),
                "1.10000",
                "1.10500",
                "1.09900",
                "1.10100",
                "10",
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
    auth_headers = {"Authorization": f"Bearer {login.json()['tokens']['access_token']}"}

    agg = await async_client.get(
        "/api/v1/persistence/candle-series",
        params={"symbol": "TESTAGG", "timeframe": "H1", "limit": 100, "order": "asc"},
        headers=auth_headers,
    )
    assert agg.status_code == 200
    agg_body = agg.json()
    assert agg_body["kind"] == "aggregated"
    assert agg_body["sourceTimeframe"] == "M1"
    assert agg_body["excludedPartialBuckets"] == 0
    assert len(agg_body["bars"]) == 2
    assert [b["open_time"] for b in agg_body["bars"]] == [
        "2026-01-05T00:00:00Z",
        "2026-01-05T01:00:00Z",
    ]
    assert all(b["timeframe"] == "H1" for b in agg_body["bars"])
    assert all(b["constituents"] == 60 for b in agg_body["bars"])
    assert all(b["complete"] is True for b in agg_body["bars"])
    # Semantics of the first aggregated bucket (M1): open=first, close=last.
    first = agg_body["bars"][0]
    assert Decimal(first["open"]) == Decimal("1.10000")
    assert Decimal(first["close"]) == Decimal("1.10100")
    assert first["source"] == "seed:synthetic"

    d1 = await async_client.get(
        "/api/v1/persistence/candle-series",
        params={"symbol": "TESTAGG", "timeframe": "D1", "limit": 100, "order": "asc"},
        headers=auth_headers,
    )
    assert d1.status_code == 200
    d1_body = d1.json()
    assert d1_body["kind"] == "unavailable"
    assert "D1" in d1_body["detail"]


def test_data_p02_series_kind_discriminates_native_aggregated_unavailable(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    """M4: the response carries a typed discriminant — native, aggregated
    (sourceTimeframe M1), or unavailable — never inferred by the consumer."""
    # Native: seed-history stores M1 rows.
    seed = client.post("/api/v1/market/live/seed-history", headers=auth_headers)
    assert seed.status_code == 200
    native = client.get(
        "/api/v1/persistence/candle-series",
        params={"symbol": "EURUSD", "timeframe": "M1", "limit": 100, "order": "asc"},
        headers=auth_headers,
    )
    assert native.status_code == 200
    native_body = native.json()
    assert native_body["kind"] == "native"
    assert native_body["timeframe"] == "M1"
    assert len(native_body["bars"]) >= 20
    assert all(b["timeframe"] == "M1" for b in native_body["bars"])

    # Unavailable: a symbol with no stored M1 coverage at all.
    unavailable = client.get(
        "/api/v1/persistence/candle-series",
        params={"symbol": "ZZZNOPE", "timeframe": "H1", "limit": 100, "order": "asc"},
        headers=auth_headers,
    )
    assert unavailable.status_code == 200
    unavailable_body = unavailable.json()
    assert unavailable_body["kind"] == "unavailable"
    assert unavailable_body["detail"]
    assert unavailable_body["bars"] == []
