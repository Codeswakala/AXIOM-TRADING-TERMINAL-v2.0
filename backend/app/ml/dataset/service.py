"""Canonical dataset service (W2-U01)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.time import require_utc, utc_now
from app.db.models.dataset import (
    DatasetLineageRecord,
    DatasetQuarantineRecord,
    DatasetSeriesMember,
    DatasetSnapshot,
)
from app.ml.dataset.chronology_guard import (
    ChronologyGuard,
    GuardRecord,
    GuardStage,
    QuarantineEvent,
)
from app.ml.dataset.market_data_query import (
    CanonicalOHLCVRecord,
    MarketDataQueryPort,
    MarketSeriesKey,
    authority_from_source,
)


@dataclass(frozen=True, slots=True)
class DatasetSnapshotInput:
    dataset_id: str
    name: str
    version: int
    market: str
    timeframe: str
    start_time: datetime
    end_time: datetime
    source: str
    feature_version: str
    quality_score: str
    created_by: str | None = None
    notes: str | None = None
    # BO-B-01.1a — validation-tier separation (binding programme rule).
    # pipeline_validation: synthetic permitted (this tier only).
    # research_validation / economic_validation / generalization_validation:
    # authoritative sources only. Default is the strict research tier so no
    # caller can silently obtain synthetic acceptance.
    tier: str = "research_validation"


VALIDATION_TIERS = (
    "pipeline_validation",
    "research_validation",
    "economic_validation",
    "generalization_validation",
)


class DatasetService:
    """Owns dataset snapshot governance and immutability."""

    def __init__(self, session: AsyncSession, guard: ChronologyGuard | None = None) -> None:
        self._session = session
        self._guard = guard or ChronologyGuard()

    async def create_draft_snapshot(self, payload: DatasetSnapshotInput) -> DatasetSnapshot:
        self._validate_mandatory(payload)
        if payload.tier not in VALIDATION_TIERS:
            raise ValueError(
                f"unknown validation tier {payload.tier!r}; "
                f"must be one of {VALIDATION_TIERS}"
            )
        start = require_utc(payload.start_time, boundary="dataset_snapshot.start_time")
        end = require_utc(payload.end_time, boundary="dataset_snapshot.end_time")
        assert start is not None and end is not None
        if end < start:
            raise ValueError("dataset end_time must be >= start_time")
        snapshot = DatasetSnapshot(
            dataset_id=payload.dataset_id,
            name=payload.name,
            version=payload.version,
            market=payload.market,
            timeframe=payload.timeframe,
            start_time=start,
            end_time=end,
            source=payload.source,
            feature_version=payload.feature_version,
            quality_score=payload.quality_score,
            status="draft",
            created_by=payload.created_by,
            notes=payload.notes,
            market_scope={"market": payload.market},
            source_policy={
                "source": payload.source,
                # BO-B-01.1a: only the pipeline-validation tier may accept
                # synthetic/simulated sources. Every higher tier is
                # authoritative-only, and the tier is persisted on the
                # snapshot so downstream consumers can verify it.
                "authoritative_only": payload.tier != "pipeline_validation",
                "tier": payload.tier,
            },
        )
        self._session.add(snapshot)
        await self._session.flush()
        return snapshot

    async def freeze_from_query(
        self,
        *,
        snapshot: DatasetSnapshot,
        query_port: MarketDataQueryPort,
        market_class: str,
        provider: str,
        symbol: str,
        timeframe: str,
        as_of_time: datetime,
        ingestion_finished_at: datetime,
    ) -> DatasetSnapshot:
        series_key = MarketSeriesKey(
            market_class=market_class,
            provider=provider,
            symbol=symbol,
            timeframe=timeframe,
        )
        records = await query_port.get_candles(
            series_key=series_key,
            start=snapshot.start_time,
            end=snapshot.end_time,
        )
        return await self.freeze_from_canonical_records(
            snapshot=snapshot,
            records=list(records),
            as_of_time=as_of_time,
            ingestion_finished_at=ingestion_finished_at,
        )

    async def freeze_from_candles(
        self,
        *,
        snapshot: DatasetSnapshot,
        candles: Sequence[object],
        provider: str,
        as_of_time: datetime,
        ingestion_finished_at: datetime,
    ) -> DatasetSnapshot:
        """Compatibility wrapper for existing candle-like objects.

        W2-U02 ML code should prefer ``freeze_from_canonical_records`` via
        MarketDataQueryPort; this wrapper remains for tests and service callers.
        """
        canonical = [
            self._canonical_from_candle_like(candle, provider=provider)
            for candle in candles
        ]
        return await self.freeze_from_canonical_records(
            snapshot=snapshot,
            records=canonical,
            as_of_time=as_of_time,
            ingestion_finished_at=ingestion_finished_at,
        )

    async def freeze_from_canonical_records(
        self,
        *,
        snapshot: DatasetSnapshot,
        records: Sequence[CanonicalOHLCVRecord],
        as_of_time: datetime,
        ingestion_finished_at: datetime,
    ) -> DatasetSnapshot:
        if snapshot.status == "frozen":
            raise ValueError("frozen dataset snapshot is immutable")
        guard_records = [
            self._guard_record_from_canonical(
                record,
                as_of_time=as_of_time,
                ingestion_finished_at=ingestion_finished_at,
            )
            for record in records
        ]
        # BO-B-01.1a: the snapshot's persisted tier governs what may enter it.
        # pipeline_validation accepts labeled synthetic/simulated sources
        # (still rejecting future-dated, out-of-order, duplicate, and naive
        # records); every other tier is authoritative-only.
        tier = (snapshot.source_policy or {}).get("tier", "research_validation")
        authoritative_training = tier != "pipeline_validation"
        accepted, quarantine = self._guard.validate_records(
            guard_records,
            stage=GuardStage.DATASET_CONSTRUCTION,
            authoritative_training=authoritative_training,
        )
        await self._write_quarantine(snapshot, quarantine)
        if not accepted:
            snapshot.status = "quarantined"
            await self._session.flush()
            return snapshot

        for record in accepted:
            self._session.add(
                DatasetLineageRecord(
                    dataset_snapshot_id=snapshot.id,
                    source_candle_id=record.source_record_id or "unknown",
                    normalized_record_hash=self._record_hash(record),
                    lineage_stage=GuardStage.DATASET_CONSTRUCTION.value,
                )
            )
        await self._write_series_members(snapshot, accepted)
        snapshot.content_hash = self.compute_content_hash(
            snapshot=snapshot,
            records=accepted,
        )
        snapshot.status = "frozen"
        snapshot.frozen_at = utc_now()
        await self._session.flush()
        return snapshot

    def compute_content_hash(
        self,
        *,
        snapshot: DatasetSnapshot,
        records: Sequence[GuardRecord],
    ) -> str:
        ordered = sorted(
            records,
            key=lambda r: (
                r.market_class,
                r.provider,
                r.symbol,
                r.timeframe,
                r.open_time.isoformat(),
                r.source,
                r.source_record_id or "",
            ),
        )
        payload = {
            "feature_version": snapshot.feature_version,
            "records": [
                {
                    "id": r.source_record_id,
                    "market_class": r.market_class,
                    "provider": r.provider,
                    "symbol": r.symbol,
                    "timeframe": r.timeframe,
                    "open_time": r.open_time.isoformat(),
                    "source": r.source,
                }
                for r in ordered
            ],
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()

    async def create_new_version_from_frozen(
        self,
        snapshot: DatasetSnapshot,
        *,
        version: int,
    ) -> DatasetSnapshot:
        if snapshot.status != "frozen":
            raise ValueError("only frozen snapshots require new version updates")
        new_snapshot = DatasetSnapshot(
            dataset_id=snapshot.dataset_id,
            name=snapshot.name,
            version=version,
            market=snapshot.market,
            timeframe=snapshot.timeframe,
            start_time=snapshot.start_time,
            end_time=snapshot.end_time,
            source=snapshot.source,
            feature_version=snapshot.feature_version,
            quality_score=snapshot.quality_score,
            status="draft",
            created_by=snapshot.created_by,
            notes="new version created from immutable frozen snapshot",
            market_scope=snapshot.market_scope,
            source_policy=snapshot.source_policy,
        )
        self._session.add(new_snapshot)
        await self._session.flush()
        return new_snapshot

    async def list_quarantine(
        self, snapshot_id: str | None = None
    ) -> list[DatasetQuarantineRecord]:
        stmt = select(DatasetQuarantineRecord)
        if snapshot_id is not None:
            stmt = stmt.where(DatasetQuarantineRecord.dataset_snapshot_id == snapshot_id)
        result = await self._session.execute(
            stmt.order_by(DatasetQuarantineRecord.detected_at.asc())
        )
        return list(result.scalars().all())

    def validate_temporal_split(self, split_strategy: str) -> None:
        self._guard.validate_temporal_split(split_strategy=split_strategy)

    def validate_label_horizon(self, **kwargs) -> None:  # type: ignore[no-untyped-def]
        self._guard.validate_label_horizon(**kwargs)

    def _validate_mandatory(self, payload: DatasetSnapshotInput) -> None:
        required = {
            "dataset_id": payload.dataset_id,
            "market": payload.market,
            "timeframe": payload.timeframe,
            "start_time": payload.start_time,
            "end_time": payload.end_time,
            "source": payload.source,
            "feature_version": payload.feature_version,
            "quality_score": payload.quality_score,
        }
        missing = [name for name, value in required.items() if value in (None, "")]
        if missing:
            raise ValueError(f"anonymous/incomplete dataset rejected; missing={missing}")

    def _canonical_from_candle_like(
        self,
        candle: object,
        *,
        provider: str,
    ) -> CanonicalOHLCVRecord:
        source = getattr(candle, "source", None) or "unknown"
        authority = authority_from_source(source)
        return CanonicalOHLCVRecord(
            series_key=MarketSeriesKey(
                market_class=getattr(candle, "market_class"),
                provider=provider,
                symbol=getattr(candle, "symbol"),
                timeframe=getattr(candle, "timeframe"),
            ),
            open_time=getattr(candle, "open_time"),
            open=getattr(candle, "open"),
            high=getattr(candle, "high"),
            low=getattr(candle, "low"),
            close=getattr(candle, "close"),
            volume=getattr(candle, "volume", None),
            source=source,
            ingestion_run_id=None,
            authority_classification=authority,
            source_record_id=getattr(candle, "id", None),
        )

    def _guard_record_from_canonical(
        self,
        record: CanonicalOHLCVRecord,
        *,
        as_of_time: datetime,
        ingestion_finished_at: datetime,
    ) -> GuardRecord:
        return GuardRecord(
            source_record_id=record.source_record_id,
            market_class=record.series_key.market_class,
            provider=record.series_key.provider,
            symbol=record.series_key.symbol,
            timeframe=record.series_key.timeframe,
            open_time=record.open_time,
            source=record.source,
            authority=record.authority_classification,
            ingestion_finished_at=ingestion_finished_at,
            as_of_time=as_of_time,
        )

    async def _write_quarantine(
        self,
        snapshot: DatasetSnapshot,
        events: Sequence[QuarantineEvent],
    ) -> None:
        for event in events:
            record = event.record
            self._session.add(
                DatasetQuarantineRecord(
                    dataset_snapshot_id=snapshot.id,
                    source_record_id=record.source_record_id if record else None,
                    market_class=record.market_class if record else "unknown",
                    provider=record.provider if record else "unknown",
                    symbol=record.symbol if record else "unknown",
                    timeframe=record.timeframe if record else "unknown",
                    open_time=event.open_time,
                    source=record.source if record else "unknown",
                    reason_code=event.reason.value,
                    detected_stage=event.stage.value,
                    detail=event.detail,
                )
            )
        await self._session.flush()

    async def _write_series_members(
        self,
        snapshot: DatasetSnapshot,
        records: Sequence[GuardRecord],
    ) -> None:
        by_series: dict[tuple[str, str, str, str, str], list[GuardRecord]] = {}
        for record in records:
            key = (*record.series_key, record.source)
            by_series.setdefault(key, []).append(record)
        for (
                market_class,
                provider,
                symbol,
                timeframe,
                source,
            ), series_records in by_series.items():
            ordered = sorted(series_records, key=lambda r: (r.open_time, r.source_record_id or ""))
            series_hash = hashlib.sha256(
                json.dumps(
                    [
                        {
                            "id": r.source_record_id,
                            "open_time": r.open_time.isoformat(),
                            "source": r.source,
                        }
                        for r in ordered
                    ],
                    sort_keys=True,
                ).encode("utf-8")
            ).hexdigest()
            self._session.add(
                DatasetSeriesMember(
                    dataset_snapshot_id=snapshot.id,
                    market_class=market_class,
                    provider=provider,
                    symbol=symbol,
                    timeframe=timeframe,
                    source=source,
                    authoritative=True,
                    record_count=len(ordered),
                    first_open_time=ordered[0].open_time,
                    last_open_time=ordered[-1].open_time,
                    series_hash=series_hash,
                )
            )
        await self._session.flush()

    def _record_hash(self, record: GuardRecord) -> str:
        return hashlib.sha256(
            json.dumps(
                {
                    "id": record.source_record_id,
                    "market_class": record.market_class,
                    "provider": record.provider,
                    "symbol": record.symbol,
                    "timeframe": record.timeframe,
                    "open_time": record.open_time.isoformat(),
                    "source": record.source,
                },
                sort_keys=True,
            ).encode("utf-8")
        ).hexdigest()
