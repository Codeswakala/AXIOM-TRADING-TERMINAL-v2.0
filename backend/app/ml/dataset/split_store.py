"""Split-manifest persistence (BO-B-01.2).

The W2-U04 ``TemporalSplitEngine`` is pure/deterministic; until B-01 nothing
persisted its manifests. This module stores executed splits into the
``dataset_split_manifests`` table so B-02 experiments can reference them by
id + hash (the ``split_manifest_id`` / ``split_manifest_hash`` FK contract
already declared on the experiment and model-artifact models).
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.dataset import DatasetSnapshot
from app.db.models.dataset_split import DatasetSplitManifest
from app.ml.dataset.split_engine import SplitRows, TemporalSplitConfig


async def store_manifest(
    session: AsyncSession,
    *,
    snapshot: DatasetSnapshot,
    split: SplitRows,
    config: TemporalSplitConfig,
) -> DatasetSplitManifest:
    """Persist an executed temporal split for a frozen snapshot.

    The unique constraint (dataset_snapshot_id, split_id) makes double-storing
    the same split a hard error rather than a silent duplicate.
    """
    row = DatasetSplitManifest(
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
        quality_summary=(
            "temporal no-look-ahead split; "
            f"label_horizon_bars={config.label_horizon_bars} "
            f"embargo_bars={config.embargo_bars}"
        ),
    )
    session.add(row)
    await session.flush()
    return row
