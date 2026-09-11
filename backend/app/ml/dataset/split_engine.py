"""Temporal split engine with embargo and label-horizon guard (W2-U04)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from typing import Sequence

from app.core.time import require_utc
from app.ml.dataset.chronology_guard import ChronologyGuard, QuarantineReason


@dataclass(frozen=True, slots=True)
class TemporalSplitConfig:
    split_id: str
    train_start: datetime
    train_end: datetime
    validation_start: datetime
    validation_end: datetime
    test_start: datetime
    test_end: datetime
    label_horizon_bars: int
    embargo_bars: int
    split_strategy: str = "temporal"


@dataclass(frozen=True, slots=True)
class SplitRows:
    train: list[dict]
    validation: list[dict]
    test: list[dict]
    split_hash: str
    manifest: dict


class TemporalSplitEngine:
    """Deterministic temporal-only split engine."""

    def __init__(self, guard: ChronologyGuard | None = None) -> None:
        self._guard = guard or ChronologyGuard()

    def split(self, *, rows: Sequence[dict], config: TemporalSplitConfig) -> SplitRows:
        self._validate_config(config)
        # BO-B-ML reproducibility fix: cross-series rows sharing an as_of tie
        # must order deterministically. Row ids are uuids (unstable across
        # runs); an optional caller-supplied "sort_key" breaks ties stably.
        # The manifest still records the row_id (identity) — only the ORDER
        # is deterministic now.
        ordered = sorted(
            rows,
            key=lambda row: (
                row["as_of"].isoformat(),
                row.get("sort_key") or row.get("row_id", ""),
            ),
        )
        train = [row for row in ordered if config.train_start <= row["as_of"] <= config.train_end]
        validation = [
            row
            for row in ordered
            if config.validation_start <= row["as_of"] <= config.validation_end
        ]
        test = [row for row in ordered if config.test_start <= row["as_of"] <= config.test_end]
        manifest = {
            "split_id": config.split_id,
            "split_strategy": config.split_strategy,
            "label_horizon_bars": config.label_horizon_bars,
            "embargo_bars": config.embargo_bars,
            "boundaries": {
                "train_start": config.train_start.isoformat(),
                "train_end": config.train_end.isoformat(),
                "validation_start": config.validation_start.isoformat(),
                "validation_end": config.validation_end.isoformat(),
                "test_start": config.test_start.isoformat(),
                "test_end": config.test_end.isoformat(),
            },
            "counts": {
                "train": len(train),
                "validation": len(validation),
                "test": len(test),
            },
            "row_ids": {
                "train": [row.get("row_id") for row in train],
                "validation": [row.get("row_id") for row in validation],
                "test": [row.get("row_id") for row in test],
            },
        }
        split_hash = hashlib.sha256(
            json.dumps(manifest, sort_keys=True).encode("utf-8")
        ).hexdigest()
        return SplitRows(
            train=train,
            validation=validation,
            test=test,
            split_hash=split_hash,
            manifest=manifest,
        )

    def _validate_config(self, config: TemporalSplitConfig) -> None:
        self._guard.validate_temporal_split(split_strategy=config.split_strategy)
        for name in (
            "train_start",
            "train_end",
            "validation_start",
            "validation_end",
            "test_start",
            "test_end",
        ):
            value = getattr(config, name)
            require_utc(value, boundary=f"temporal_split.{name}")
        if not (
            config.train_start
            <= config.train_end
            < config.validation_start
            <= config.validation_end
        ):
            raise ValueError(QuarantineReason.SPLIT_LEAKAGE.value)
        if not config.validation_end < config.test_start <= config.test_end:
            raise ValueError(QuarantineReason.SPLIT_LEAKAGE.value)
        # W2-U04 unit-level bar-based approximation: the gap between training
        # boundary and validation boundary must be at least label horizon + embargo bars.
        required_gap = config.label_horizon_bars + config.embargo_bars
        actual_gap = int((config.validation_start - config.train_end).total_seconds() // 60) - 1
        if actual_gap < required_gap:
            raise ValueError(QuarantineReason.LABEL_HORIZON_LEAKAGE.value)
