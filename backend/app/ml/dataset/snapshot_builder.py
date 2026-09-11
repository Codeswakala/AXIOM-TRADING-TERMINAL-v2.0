"""Reproducible dataset snapshot builder (W2-U04)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.dataset import DatasetSnapshot
from app.db.models.dataset_split import DatasetSplitManifest
from app.db.models.feature import FeatureRecord
from app.ml.dataset.market_data_query import CanonicalOHLCVRecord, MarketSeriesKey
from app.ml.dataset.service import DatasetService, DatasetSnapshotInput
from app.ml.dataset.split_engine import TemporalSplitConfig, TemporalSplitEngine
from app.ml.features.store import FeatureStoreService


@dataclass(slots=True)
class SnapshotBuildResult:
    snapshot: DatasetSnapshot
    feature_records: list[FeatureRecord]
    feature_hash: str
    matrix_rows: list[dict]


class ReproducibleSnapshotBuilder:
    """Builds frozen, content-hashed dataset snapshots and feature matrices."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._datasets = DatasetService(session)
        self._features = FeatureStoreService(session)
        self._splitter = TemporalSplitEngine()

    async def build_from_records(
        self,
        *,
        snapshot_input: DatasetSnapshotInput,
        series_key: MarketSeriesKey,
        records: Sequence[CanonicalOHLCVRecord],
        as_of_time: datetime,
        ingestion_finished_at: datetime,
        feature_set_version: str = "feature_set.v1",
    ) -> SnapshotBuildResult:
        snapshot = await self._datasets.create_draft_snapshot(snapshot_input)
        frozen = await self._datasets.freeze_from_canonical_records(
            snapshot=snapshot,
            records=records,
            as_of_time=as_of_time,
            ingestion_finished_at=ingestion_finished_at,
        )
        if frozen.status != "frozen" or not frozen.content_hash:
            return SnapshotBuildResult(
                snapshot=frozen,
                feature_records=[],
                feature_hash="",
                matrix_rows=[],
            )
        feature_rows, report = await self._features.compute_and_store(
            series_key=series_key,
            records=records,
            feature_set_version=feature_set_version,
            source_dataset_hash=frozen.content_hash,
            as_of_time=as_of_time,
            ingestion_finished_at=ingestion_finished_at,
        )
        matrix_rows = [self._matrix_row(row) for row in feature_rows]
        return SnapshotBuildResult(
            snapshot=frozen,
            feature_records=feature_rows,
            feature_hash=report.content_hash,
            matrix_rows=matrix_rows,
        )

    async def create_split_manifest(
        self,
        *,
        snapshot: DatasetSnapshot,
        matrix_rows: Sequence[dict],
        config: TemporalSplitConfig,
    ) -> DatasetSplitManifest:
        split = self._splitter.split(rows=matrix_rows, config=config)
        manifest = DatasetSplitManifest(
            dataset_snapshot_id=snapshot.id,
            split_id=config.split_id,
            split_strategy=config.split_strategy,
            label_horizon_bars=config.label_horizon_bars,
            embargo_bars=config.embargo_bars,
            train_start=config.train_start,
            train_end=config.train_end,
            validation_start=config.validation_start,
            validation_end=config.validation_end,
            test_start=config.test_start,
            test_end=config.test_end,
            train_count=len(split.train),
            validation_count=len(split.validation),
            test_count=len(split.test),
            split_hash=split.split_hash,
            manifest=split.manifest,
            quality_summary="temporal split; identity fields excluded from matrix",
        )
        self._session.add(manifest)
        await self._session.flush()
        return manifest

    def _matrix_row(self, row: FeatureRecord) -> dict:
        return {
            "row_id": row.id,
            "as_of": row.as_of,
            "features": row.features,
            "source_dataset_hash": row.source_dataset_hash,
        }
