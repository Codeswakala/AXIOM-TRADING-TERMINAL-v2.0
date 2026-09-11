"""Baseline market-agnostic model training harness (W2-U06)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.time import coerce_external_utc
from app.db.models.dataset import DatasetSnapshot
from app.db.models.dataset_split import DatasetSplitManifest
from app.db.models.experiment import Experiment
from app.db.models.feature import FeatureRecord
from app.db.models.model_artifact import ModelArtifact
from app.ml.dataset.market_data_query import (
    CandleMarketDataQueryAdapter,
    MarketSeriesKey,
)
from app.ml.models.baseline import MajorityClassBaseline
from app.ml.models.errors import (
    ExperimentNotApprovedError,
    IdentityInModelInputError,
    NonTemporalSplitError,
    UnresolvedExperimentPinError,
)
from app.repositories.audit_repository import AuditRepository

IDENTITY_KEYS = {
    "symbol",
    "provider",
    "market_class",
    "symbol" + "_id",
    "one_hot" + "_symbol",
    "symbol" + "_identity",
}
LABEL_KEY = "label_direction"


async def derive_candle_labels(
    session: AsyncSession,
    rows: Sequence[FeatureRecord],
) -> dict[str, int]:
    """BO-B-02: derive forward labels from candle closes, no look-ahead.

    Label at bar t = 1 if the NEXT bar's close is above bar t's close, else 0.
    The final bar of each series is never labeled (no future bar exists), so
    it is excluded from any training/validation matrix. Rows whose candle
    cannot be resolved are excluded (fail honest, never fabricate a label).
    """
    labels: dict[str, int] = {}
    series_cache: dict[tuple[str, str, str, str], list[tuple[object, float]]] = {}
    adapter = CandleMarketDataQueryAdapter(session, provider="internal")
    for row in rows:
        key = (row.market_class, row.symbol, row.timeframe, row.source or "")
        if key not in series_cache:
            records = await adapter.get_candles(
                series_key=MarketSeriesKey(
                    market_class=row.market_class,
                    provider="internal",
                    symbol=row.symbol,
                    timeframe=row.timeframe,
                ),
                source_filter=row.source,
            )
            series_cache[key] = [(r.open_time, float(r.close)) for r in records]
        series = series_cache[key]
        times = [t for t, _close in series]
        closes = {t: c for t, c in series}
        # SQLite stores naive timestamps; coerce to UTC before comparing
        # against the adapter's aware candle times.
        as_of = coerce_external_utc(row.as_of, source="harness label derivation")
        if as_of is None:
            continue  # unresolved timestamp — excluded, never fabricated
        # Binary search for the next strictly-greater open_time.
        import bisect

        position = bisect.bisect_right(times, as_of)
        if position >= len(times):
            continue  # final bar — unlabeled by design
        next_time = times[position]
        if as_of not in closes:
            continue  # unresolved candle — excluded, never fabricated
        labels[row.id] = 1 if closes[next_time] > closes[as_of] else 0
    return labels


@dataclass(frozen=True, slots=True)
class TrainingResult:
    artifact: ModelArtifact
    artifact_hash: str
    metrics: dict[str, Any]


class BaselineModelHarness:
    """Trains a deterministic research-only baseline via an approved experiment."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._audit = AuditRepository(session)

    async def train(
        self,
        *,
        experiment_id: str,
        seed: int = 42,
        labels_from_candles: bool = False,
    ) -> TrainingResult:
        experiment = await self._load_approved_experiment(experiment_id)
        snapshot = await self._resolve_snapshot(experiment)
        split = await self._resolve_split(experiment, snapshot)
        if split.split_strategy not in {"temporal", "walk_forward"}:
            raise NonTemporalSplitError("NON_TEMPORAL_SPLIT")

        rows = await self._load_feature_rows(experiment)
        by_id = {row.id: row for row in rows}
        row_ids = split.manifest.get("row_ids") or {}
        train_rows = self._rows_from_manifest(by_id, row_ids.get("train", []), split_name="train")
        validation_rows = self._rows_from_manifest(
            by_id, row_ids.get("validation", []), split_name="validation"
        )
        test_rows = self._rows_from_manifest(by_id, row_ids.get("test", []), split_name="test")

        # BO-B-02: when features carry no label column, derive forward labels
        # from candle closes (no look-ahead; final bars excluded).
        label_overrides: Mapping[str, int] | None = None
        if labels_from_candles:
            label_overrides = await derive_candle_labels(self._session, rows)

        train_x, train_y, feature_columns = self._matrix_and_labels(
            train_rows, label_overrides=label_overrides
        )
        val_x, val_y, _ = self._matrix_and_labels(
            validation_rows, expected_columns=feature_columns, label_overrides=label_overrides
        )
        test_x, test_y, _ = self._matrix_and_labels(
            test_rows, expected_columns=feature_columns, label_overrides=label_overrides
        )

        model = MajorityClassBaseline(seed=seed)
        model.fit(train_y)
        metrics = {
            "train_accuracy": model.evaluate(train_x, train_y).accuracy,
            "validation_accuracy": model.evaluate(val_x, val_y).accuracy,
            "test_accuracy": model.evaluate(test_x, test_y).accuracy,
            "baseline_note": (
                "Majority-class baseline; proves harness mechanics, "
                "not predictive skill."
            ),
        }
        payload = {
            "experiment_id": experiment.experiment_id,
            "experiment_version": experiment.version,
            "dataset_snapshot_id": snapshot.id,
            "dataset_content_hash": snapshot.content_hash,
            "split_manifest_hash": split.split_hash,
            "feature_set_version": experiment.feature_set_version,
            "model": model.artifact_payload(feature_columns=feature_columns),
            "metrics": metrics,
        }
        artifact_hash = hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode("utf-8")
        ).hexdigest()
        artifact = ModelArtifact(
            name=f"baseline-{experiment.experiment_id}",
            version=f"{experiment.version}-{seed}",
            status="research_only",
            framework=model.framework,
            feature_set_version=experiment.feature_set_version,
            supported_markets=snapshot.market_scope,
            metrics=metrics,
            artifact_uri=f"sha256:{artifact_hash}",
            notes="Research-only baseline artifact; no live signal or execution use.",
            experiment_id=experiment.experiment_id,
            dataset_snapshot_id=snapshot.id,
            dataset_content_hash=snapshot.content_hash,
            split_manifest_hash=split.split_hash,
            hyperparameters={"seed": seed, "model": model.framework},
            artifact_hash=artifact_hash,
            research_status="research_only",
        )
        self._session.add(artifact)
        await self._session.flush()
        await self._audit.append(
            category="ML",
            action="model.baseline_trained",
            actor="system",
            resource_type="model_artifact",
            resource_id=artifact.id,
            message=f"Baseline model trained for experiment={experiment.experiment_id}",
            details={"experiment_id": experiment.experiment_id, "artifact_hash": artifact_hash},
        )
        return TrainingResult(artifact=artifact, artifact_hash=artifact_hash, metrics=metrics)

    async def _load_approved_experiment(self, experiment_id: str) -> Experiment:
        result = await self._session.execute(
            select(Experiment)
            .where(Experiment.experiment_id == experiment_id)
            .order_by(Experiment.version.desc())
        )
        experiment = result.scalars().first()
        if (
            experiment is None
            or experiment.status != "approved"
            or experiment.approval_timestamp is None
        ):
            raise ExperimentNotApprovedError("EXPERIMENT_NOT_APPROVED")
        return experiment

    async def _resolve_snapshot(self, experiment: Experiment) -> DatasetSnapshot:
        snapshot = await self._session.get(DatasetSnapshot, experiment.dataset_snapshot_id)
        if snapshot is None or snapshot.status != "frozen" or not snapshot.content_hash:
            raise UnresolvedExperimentPinError("UNRESOLVED_PIN: snapshot")
        if snapshot.content_hash != experiment.dataset_content_hash:
            raise UnresolvedExperimentPinError("UNRESOLVED_PIN: snapshot hash")
        return snapshot

    async def _resolve_split(
        self, experiment: Experiment, snapshot: DatasetSnapshot
    ) -> DatasetSplitManifest:
        split = await self._session.get(DatasetSplitManifest, experiment.split_manifest_id)
        if split is None or not split.split_hash:
            raise UnresolvedExperimentPinError("UNRESOLVED_PIN: split")
        if split.dataset_snapshot_id != snapshot.id:
            raise UnresolvedExperimentPinError("UNRESOLVED_PIN: split snapshot")
        if split.split_hash != experiment.split_manifest_hash:
            raise UnresolvedExperimentPinError("UNRESOLVED_PIN: split hash")
        return split

    async def _load_feature_rows(self, experiment: Experiment) -> list[FeatureRecord]:
        result = await self._session.execute(
            select(FeatureRecord)
            .where(
                FeatureRecord.feature_set_version == experiment.feature_set_version,
                FeatureRecord.source_dataset_hash == experiment.dataset_content_hash,
            )
            .order_by(FeatureRecord.as_of.asc(), FeatureRecord.id.asc())
        )
        rows = list(result.scalars().all())
        if not rows:
            raise UnresolvedExperimentPinError("UNRESOLVED_PIN: feature records")
        return rows

    def _rows_from_manifest(
        self, by_id: dict[str, FeatureRecord], row_ids: Sequence[str], *, split_name: str
    ) -> list[FeatureRecord]:
        rows: list[FeatureRecord] = []
        for row_id in row_ids:
            row = by_id.get(row_id)
            if row is None:
                raise UnresolvedExperimentPinError(f"UNRESOLVED_PIN: {split_name} row {row_id}")
            rows.append(row)
        return rows

    def _matrix_and_labels(
        self,
        rows: Sequence[FeatureRecord],
        *,
        expected_columns: Sequence[str] | None = None,
        label_overrides: Mapping[str, int] | None = None,
        feature_filter: set[str] | None = None,
    ) -> tuple[list[dict[str, float]], list[int], list[str]]:
        matrix: list[dict[str, float]] = []
        labels: list[int] = []
        columns: list[str] | None = list(expected_columns) if expected_columns is not None else None
        for row in rows:
            keys = set(row.features)
            identity = IDENTITY_KEYS.intersection(keys)
            if identity:
                raise IdentityInModelInputError(f"IDENTITY_IN_MODEL_INPUT: {sorted(identity)}")
            if label_overrides is not None:
                if row.id not in label_overrides:
                    continue  # BO-B-02: unlabeled rows are excluded, never fabricated
                label = label_overrides[row.id]
            else:
                if LABEL_KEY not in row.features:
                    raise UnresolvedExperimentPinError("UNRESOLVED_PIN: label")
                label = int(row.features[LABEL_KEY])
            feature_values: dict[str, float] = {}
            incomplete = False
            for key, value in row.features.items():
                if key == LABEL_KEY:
                    continue
                if feature_filter is not None and key not in feature_filter:
                    continue
                if value is None:
                    # BO-B-02/BO-B-ML2: feature warm-up gaps (e.g. rolling
                    # lookback) are excluded from matrices, never fabricated.
                    incomplete = True
                    break
                feature_values[key] = float(value)
            if incomplete:
                continue
            labels.append(label)
            if columns is None:
                columns = sorted(feature_values)
            if set(feature_values) != set(columns):
                raise UnresolvedExperimentPinError("UNRESOLVED_PIN: inconsistent feature columns")
            matrix.append({key: feature_values[key] for key in columns})
        if not matrix:
            raise UnresolvedExperimentPinError("UNRESOLVED_PIN: no labeled rows in split")
        return matrix, labels, list(columns or [])
