"""Ingestion orchestration service — historical CSV foundation only."""

from __future__ import annotations

import time
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.db.models.ingestion_run import IngestionRun
from app.ingestion.csv_loader import CsvLoaderError, iter_csv_rows
from app.ingestion.normalize import normalize_row
from app.ingestion.types import IngestionResult
from app.ml.dataset.market_data_query import (
    MarketSeriesKey,
    MarketSeriesMetadataRead,
    authority_from_source,
)
from app.ml.dataset.metadata_service import MarketMetadataService
from app.repositories.audit_repository import AuditRepository
from app.repositories.candle_repository import CandleRepository
from app.repositories.ingestion_run_repository import IngestionRunRepository

logger = get_logger(__name__, category="MARKET")


class IngestionService:
    """Synchronous (request-scoped async) historical ingestion pipeline."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._candles = CandleRepository(session)
        self._runs = IngestionRunRepository(session)
        self._audit = AuditRepository(session)

    async def ingest_csv(
        self,
        *,
        path: str | Path,
        market_class: str,
        symbol: str,
        timeframe: str,
        source: str | None = None,
        max_error_samples: int = 25,
    ) -> IngestionResult:
        started = time.perf_counter()
        file_path = Path(path)
        source_label = source or f"csv:{file_path.name}"

        run = IngestionRun(
            source_type="csv",
            source_name=str(file_path),
            market_class=market_class,
            symbol=symbol,
            timeframe=timeframe,
            status="running",
        )
        await self._runs.add(run)

        result = IngestionResult(
            run_id=run.id,
            status="running",
            source_name=str(file_path),
            market_class=market_class,
            symbol=symbol,
            timeframe=timeframe,
        )

        try:
            for row_number, raw in iter_csv_rows(file_path):
                result.rows_read += 1
                normalized, error = normalize_row(
                    raw,
                    row_number=row_number,
                    market_class=market_class,
                    symbol=symbol,
                    timeframe=timeframe,
                    source=source_label,
                )
                if error is not None:
                    result.rows_invalid += 1
                    if len(result.errors) < max_error_samples:
                        result.errors.append(error)
                    continue

                assert normalized is not None
                result.rows_valid += 1
                _, action = await self._candles.upsert_ohlcv(
                    market_class=normalized.market_class,
                    symbol=normalized.symbol,
                    timeframe=normalized.timeframe,
                    open_time=normalized.open_time,
                    open=normalized.open,
                    high=normalized.high,
                    low=normalized.low,
                    close=normalized.close,
                    volume=normalized.volume,
                    source=normalized.source,
                )
                if action == "inserted":
                    result.rows_inserted += 1
                elif action == "updated":
                    result.rows_updated += 1
                else:
                    result.rows_unchanged += 1

            result.duration_ms = int((time.perf_counter() - started) * 1000)
            if result.rows_invalid and result.rows_valid:
                result.status = "completed_with_errors"
            elif result.rows_valid == 0 and result.rows_read > 0:
                result.status = "failed"
                result.error_summary = "No valid rows ingested"
            else:
                result.status = "completed"

            if result.errors:
                result.error_summary = (
                    f"{result.rows_invalid} invalid row(s); "
                    f"first: row {result.errors[0].row_number}: {result.errors[0].message}"
                )

            # BO-B-01.1: every ingested series carries a truthful metadata row
            # with its source authority (honest labeling end-to-end).
            if result.status != "failed" and result.rows_valid > 0:
                await self._upsert_series_metadata(
                    market_class=market_class,
                    symbol=symbol,
                    timeframe=timeframe,
                    source_label=source_label,
                )

            await self._finalize_run(run, result)
            await self._audit.append(
                category="MARKET",
                action="ingestion.csv.completed",
                message=(
                    f"Ingested {result.rows_inserted} new / {result.rows_updated} updated "
                    f"candles for {symbol} {timeframe}"
                ),
                resource_type="ingestion_run",
                resource_id=run.id,
                details={
                    "rows_read": result.rows_read,
                    "rows_valid": result.rows_valid,
                    "rows_invalid": result.rows_invalid,
                    "rows_inserted": result.rows_inserted,
                    "rows_updated": result.rows_updated,
                    "rows_unchanged": result.rows_unchanged,
                    "status": result.status,
                    "duration_ms": result.duration_ms,
                },
            )
            logger.info(
                "Ingestion finished run_id=%s status=%s read=%s inserted=%s "
                "updated=%s unchanged=%s invalid=%s ms=%s",
                run.id,
                result.status,
                result.rows_read,
                result.rows_inserted,
                result.rows_updated,
                result.rows_unchanged,
                result.rows_invalid,
                result.duration_ms,
            )
            return result

        except CsvLoaderError as exc:
            result.status = "failed"
            result.error_summary = str(exc)
            result.duration_ms = int((time.perf_counter() - started) * 1000)
            await self._finalize_run(run, result)
            logger.exception("CSV loader failure run_id=%s", run.id)
            return result
        except Exception as exc:  # noqa: BLE001
            result.status = "failed"
            result.error_summary = f"{exc.__class__.__name__}: {exc}"
            result.duration_ms = int((time.perf_counter() - started) * 1000)
            await self._finalize_run(run, result)
            logger.exception("Ingestion failure run_id=%s", run.id)
            return result

    async def _upsert_series_metadata(
        self,
        *,
        market_class: str,
        symbol: str,
        timeframe: str,
        source_label: str,
    ) -> None:
        """BO-B-01.1: persist a truthful per-series metadata row (source
        authority classified by the single shared mapping; provider aligned
        with the CandleMarketDataQueryAdapter default so metadata resolves
        under the same series key the dataset service queries)."""
        authority = authority_from_source(source_label)
        service = MarketMetadataService(self._session)
        await service.upsert_metadata(
            MarketSeriesMetadataRead(
                series_key=MarketSeriesKey(
                    market_class=market_class,
                    provider="internal",
                    symbol=symbol,
                    timeframe=timeframe,
                ),
                timezone_assumption="UTC",
                source_authority=authority,
                known_limitations=(
                    f"Labeled {source_label!r} → authority "
                    f"{authority.value!r} by the shared classification rule. "
                    "Verify the declared source before any research-tier use."
                ),
                metadata_role="csv_ingestion",
            )
        )

    async def _finalize_run(self, run: IngestionRun, result: IngestionResult) -> None:
        from app.db.base import utc_now

        run.status = result.status
        run.rows_read = result.rows_read
        run.rows_valid = result.rows_valid
        run.rows_invalid = result.rows_invalid
        run.rows_inserted = result.rows_inserted
        run.rows_updated = result.rows_updated
        run.rows_unchanged = result.rows_unchanged
        run.duration_ms = result.duration_ms
        run.error_summary = result.error_summary
        run.finished_at = utc_now()
        run.details = {
            "error_samples": [
                {"row": e.row_number, "message": e.message} for e in result.errors[:10]
            ]
        }
        await self._session.flush()

    async def list_runs(self, *, limit: int = 20) -> list[IngestionRun]:
        return list(await self._runs.list_recent(limit=limit))

    async def get_run(self, run_id: str) -> IngestionRun | None:
        return await self._runs.get_by_id(run_id)

    async def candle_counts(
        self,
        *,
        market_class: str | None = None,
        symbol: str | None = None,
        timeframe: str | None = None,
    ) -> int:
        return await self._candles.count_by_market(
            market_class=market_class,
            symbol=symbol,
            timeframe=timeframe,
        )
