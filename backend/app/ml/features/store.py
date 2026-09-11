"""Feature store v1 service (W2-U03)."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from decimal import Decimal
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.feature import FeatureRecord
from app.db.models.feature_definition import FeatureDefinition, FeatureQualityReport
from app.ml.dataset.chronology_guard import (
    ChronologyGuard,
    GuardRecord,
    GuardStage,
)
from app.ml.dataset.market_data_query import CanonicalOHLCVRecord, MarketSeriesKey
from app.ml.dataset.metadata_service import MarketMetadataService
from app.ml.features.definitions import (
    ComputableFeature,
    FeatureDefinitionSpec,
    builtin_feature_set_v1,
)
from app.ml.features.errors import (
    DuplicateFeatureDefinitionError,
    FeatureInputRejectedError,
)

IDENTITY_KEYS = {"symbol", "provider", "market_class"}


class FeatureStoreService:
    """Registers feature definitions and computes/stores causal feature records."""

    def __init__(self, session: AsyncSession, guard: ChronologyGuard | None = None) -> None:
        self._session = session
        self._guard = guard or ChronologyGuard()

    async def register_definition(self, spec: FeatureDefinitionSpec) -> FeatureDefinition:
        spec.assert_causal()
        existing = await self._session.execute(
            select(FeatureDefinition).where(
                FeatureDefinition.feature_name == spec.feature_name,
                FeatureDefinition.feature_version == spec.feature_version,
            )
        )
        if existing.scalar_one_or_none() is not None:
            raise DuplicateFeatureDefinitionError(
                f"duplicate feature definition {spec.feature_name}:{spec.feature_version}"
            )
        row = FeatureDefinition(
            feature_name=spec.feature_name,
            feature_version=spec.feature_version,
            formula_spec=spec.formula_spec,
            input_requirements=spec.input_requirements,
            lookback_window=spec.lookback_window,
            causal=spec.causal,
            market_compatibility_notes=spec.market_compatibility_notes,
        )
        self._session.add(row)
        await self._session.flush()
        return row

    async def register_builtin_definitions(self) -> list[FeatureDefinition]:
        rows: list[FeatureDefinition] = []
        for feature in builtin_feature_set_v1():
            rows.append(await self.register_definition(feature.spec))
        return rows

    async def compute_and_store(
        self,
        *,
        series_key: MarketSeriesKey,
        records: Sequence[CanonicalOHLCVRecord],
        features: Sequence[ComputableFeature] | None = None,
        feature_set_version: str = "feature_set.v1",
        source_dataset_hash: str,
        quality_score: str = "pass",
        as_of_time: datetime | None = None,
        ingestion_finished_at: datetime | None = None,
        tier: str = "research_validation",
    ) -> tuple[list[FeatureRecord], FeatureQualityReport]:
        features = list(features or builtin_feature_set_v1())
        self._assert_no_identity_output([feature.spec.feature_name for feature in features])
        if records:
            default_anchor = max(record.open_time for record in records)
        else:
            default_anchor = None
        guard_records = [
            self._guard_record_from_canonical(
                record,
                as_of_time=as_of_time or default_anchor or record.open_time,
                ingestion_finished_at=ingestion_finished_at or default_anchor or record.open_time,
            )
            for record in records
        ]
        # BO-B-01.1a: feature computation inherits the dataset's validation
        # tier. pipeline_validation may consume labeled synthetic sources;
        # every higher tier is authoritative-only (strict default).
        accepted, quarantine = self._guard.validate_records(
            guard_records,
            stage=GuardStage.TRAINING_SET_GENERATION,
            authoritative_training=tier != "pipeline_validation",
        )
        if quarantine:
            reasons = sorted({event.reason.value for event in quarantine})
            raise FeatureInputRejectedError(
                f"feature input rejected by chronology guard: {reasons}"
            )
        accepted_ids = {record.source_record_id for record in accepted}
        ordered = [record for record in records if record.source_record_id in accepted_ids]
        ordered.sort(key=lambda item: (item.open_time, item.source_record_id or ""))

        output: list[FeatureRecord] = []
        for index, record in enumerate(ordered):
            values: dict[str, str | None] = {}
            for feature in features:
                value = feature.compute(ordered, index)
                values[feature.spec.feature_name] = self._serialize_decimal(value)
            self._assert_no_identity_output(values.keys())
            row = FeatureRecord(
                feature_set_version=feature_set_version,
                provider=series_key.provider,
                market_class=series_key.market_class,
                symbol=series_key.symbol,
                timeframe=series_key.timeframe,
                as_of=record.open_time,
                features=values,
                quality_score=quality_score,
                source=record.source,
                source_dataset_hash=source_dataset_hash,
            )
            self._session.add(row)
            output.append(row)
        await self._session.flush()

        report_hash = self.compute_feature_hash(output, feature_set_version=feature_set_version)
        report = FeatureQualityReport(
            feature_set_version=feature_set_version,
            source_dataset_hash=source_dataset_hash,
            missing_rate=self._missing_rate(output),
            drift_summary={"status": "not_evaluated_in_w2_u03"},
            leakage_checks={"causal": True, "identity_fields_excluded": True},
            stationarity_notes="Not evaluated in W2-U03; report shape only.",
            cross_market_compatibility="Initial normalized market-agnostic features only.",
            content_hash=report_hash,
        )
        self._session.add(report)
        await self._session.flush()
        return output, report

    def compute_feature_hash(
        self,
        records: Sequence[FeatureRecord],
        *,
        feature_set_version: str,
    ) -> str:
        payload = {
            "feature_set_version": feature_set_version,
            "records": [
                {
                    "provider": row.provider,
                    "market_class": row.market_class,
                    "symbol": row.symbol,
                    "timeframe": row.timeframe,
                    "as_of": row.as_of.isoformat(),
                    "features": row.features,
                    "source_dataset_hash": row.source_dataset_hash,
                }
                for row in sorted(
                    records,
                    key=lambda item: (
                        item.market_class,
                        item.provider,
                        item.symbol,
                        item.timeframe,
                        item.as_of.isoformat(),
                    ),
                )
            ],
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()

    async def get_evaluation_metadata(self, series_key: MarketSeriesKey):  # noqa: ANN201
        return await MarketMetadataService(self._session).get_metadata(series_key)

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

    def _assert_no_identity_output(self, keys) -> None:  # noqa: ANN001
        present = IDENTITY_KEYS.intersection(set(keys))
        if present:
            raise ValueError(f"symbol/provider identity fields are not feature outputs: {present}")

    def _serialize_decimal(self, value: Decimal | None) -> str | None:
        return None if value is None else str(value)

    def _missing_rate(self, records: Sequence[FeatureRecord]) -> float:
        total = 0
        missing = 0
        for row in records:
            for value in row.features.values():
                total += 1
                if value is None:
                    missing += 1
        return 0.0 if total == 0 else missing / total
