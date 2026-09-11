"""W1-U01 timezone-aware UTC regression coverage."""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from app.ingestion.types import NormalizedCandleRow
from app.services.candle_service import CandleService


def _assert_utc(value: str) -> None:
    assert value.endswith("+00:00") or value.endswith("Z"), value


def test_api_timestamps_are_timezone_aware_utc(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    # Auth path
    me = client.get("/api/v1/operator/me", headers=auth_headers)
    assert me.status_code == 200
    _assert_utc(me.json()["created_at"])

    # External API input may be naive; the compatibility assumption is made only
    # at the request schema boundary and the persisted/API value is UTC-aware.
    payload = {
        "market_class": "forex",
        "symbol": "EURUSD",
        "timeframe": "H1",
        "open_time": datetime(2026, 7, 12, 10, 0).isoformat(),
        "open": "1.0800",
        "high": "1.0850",
        "low": "1.0780",
        "close": "1.0825",
        "volume": "1500",
        "source": "utc-test",
    }
    created = client.post("/api/v1/persistence/candles", json=payload, headers=auth_headers)
    assert created.status_code == 201, created.text
    created_body = created.json()
    _assert_utc(created_body["open_time"])
    _assert_utc(created_body["created_at"])

    # Audit path
    audits = client.get("/api/v1/persistence/audit-events", headers=auth_headers)
    assert audits.status_code == 200
    assert audits.json()
    _assert_utc(audits.json()[0]["created_at"])

    # Ingestion path
    ingest = client.post(
        "/api/v1/ingestion/sample",
        json={
            "sample_name": "eurusd_h1_sample.csv",
            "market_class": "forex",
            "symbol": "EURUSD",
            "timeframe": "H1",
        },
        headers=auth_headers,
    )
    assert ingest.status_code == 200, ingest.text
    runs = client.get("/api/v1/ingestion/runs", headers=auth_headers)
    assert runs.status_code == 200
    _assert_utc(runs.json()[0]["started_at"])
    _assert_utc(runs.json()[0]["finished_at"])


def test_normalized_candle_row_rejects_naive_internal_time() -> None:
    with pytest.raises(ValueError, match="Naive datetime rejected"):
        NormalizedCandleRow(
            market_class="forex",
            symbol="EURUSD",
            timeframe="M1",
            open_time=datetime(2026, 7, 12, 10, 0),
            open=Decimal("1.0"),
            high=Decimal("1.1"),
            low=Decimal("0.9"),
            close=Decimal("1.0"),
            volume=None,
            source="unit-test",
        )


@pytest.mark.asyncio
async def test_candle_service_rejects_naive_internal_time(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        service = CandleService(session)
        with pytest.raises(ValueError, match="Naive datetime rejected"):
            await service.create_candle(
                market_class="forex",
                symbol="EURUSD",
                timeframe="M1",
                open_time=datetime(2026, 7, 12, 10, 0),
                open=Decimal("1.0"),
                high=Decimal("1.1"),
                low=Decimal("0.9"),
                close=Decimal("1.0"),
                volume=None,
                source="unit-test",
            )

        created = await service.create_candle(
            market_class="forex",
            symbol="EURUSD",
            timeframe="M1",
            open_time=datetime(2026, 7, 12, 10, 0, tzinfo=timezone.utc),
            open=Decimal("1.0"),
            high=Decimal("1.1"),
            low=Decimal("0.9"),
            close=Decimal("1.0"),
            volume=None,
            source="unit-test",
        )
        assert created.open_time.tzinfo is not None
