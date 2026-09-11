"""Integration tests for historical CSV ingestion service."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.db.session import session_scope
from app.ingestion.service import IngestionService
from app.repositories.candle_repository import CandleRepository

SAMPLES = Path(__file__).resolve().parents[1] / "sample_data"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


@pytest.mark.asyncio
async def test_ingest_csv_inserts_candles(prepared_db: None) -> None:
    async with session_scope() as session:
        service = IngestionService(session)
        result = await service.ingest_csv(
            path=SAMPLES / "eurusd_h1_sample.csv",
            market_class="forex",
            symbol="EURUSD",
            timeframe="H1",
        )
        assert result.status == "completed"
        assert result.rows_read == 5
        assert result.rows_valid == 5
        assert result.rows_inserted == 5
        assert result.rows_invalid == 0

    async with session_scope() as session:
        repo = CandleRepository(session)
        count = await repo.count_by_market(symbol="EURUSD", timeframe="H1")
        assert count == 5


@pytest.mark.asyncio
async def test_ingest_csv_deduplicates_on_reload(prepared_db: None) -> None:
    path = SAMPLES / "eurusd_h1_sample.csv"
    async with session_scope() as session:
        service = IngestionService(session)
        first = await service.ingest_csv(
            path=path, market_class="forex", symbol="EURUSD", timeframe="H1"
        )
        assert first.rows_inserted == 5

    async with session_scope() as session:
        service = IngestionService(session)
        second = await service.ingest_csv(
            path=path, market_class="forex", symbol="EURUSD", timeframe="H1"
        )
        assert second.rows_inserted == 0
        assert second.rows_unchanged == 5
        assert second.status == "completed"

    async with session_scope() as session:
        count = await CandleRepository(session).count_by_market(symbol="EURUSD")
        assert count == 5


@pytest.mark.asyncio
async def test_ingest_alternate_headers_crypto(prepared_db: None) -> None:
    async with session_scope() as session:
        service = IngestionService(session)
        result = await service.ingest_csv(
            path=SAMPLES / "btcusd_h1_sample.csv",
            market_class="crypto",
            symbol="BTCUSD",
            timeframe="H1",
        )
        assert result.status == "completed"
        assert result.rows_inserted == 4


@pytest.mark.asyncio
async def test_ingest_invalid_rows_partial(prepared_db: None) -> None:
    async with session_scope() as session:
        service = IngestionService(session)
        result = await service.ingest_csv(
            path=FIXTURES / "invalid_rows_sample.csv",
            market_class="forex",
            symbol="EURUSD",
            timeframe="H1",
        )
        assert result.rows_read == 4
        assert result.rows_valid == 1
        assert result.rows_invalid == 3
        assert result.status == "completed_with_errors"
        assert result.rows_inserted == 1


@pytest.mark.asyncio
async def test_list_runs_after_ingest(prepared_db: None) -> None:
    async with session_scope() as session:
        service = IngestionService(session)
        await service.ingest_csv(
            path=SAMPLES / "eurusd_h1_sample.csv",
            market_class="forex",
            symbol="EURUSD",
            timeframe="H1",
        )
        runs = await service.list_runs(limit=5)
        assert len(runs) >= 1
        assert runs[0].symbol == "EURUSD"
