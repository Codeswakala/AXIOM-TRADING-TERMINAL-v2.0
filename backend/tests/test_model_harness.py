"""W2-U06 baseline model harness tests."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from app.db.models.dataset import DatasetSnapshot
from app.db.models.dataset_split import DatasetSplitManifest
from app.db.models.experiment import Experiment
from app.db.models.feature import FeatureRecord
from app.ml.experiments import ExperimentPlanInput, ExperimentRegistryService
from app.ml.models import (
    BaselineModelHarness,
    ExperimentNotApprovedError,
    IdentityInModelInputError,
    NonTemporalSplitError,
    UnresolvedExperimentPinError,
)


def _utc(minute: int) -> datetime:
    return datetime(2026, 7, 14, 10, minute, tzinfo=timezone.utc)


async def _approved_experiment_fixture(session, *, identity: bool = False):  # noqa: ANN001, ANN201
    snapshot = DatasetSnapshot(
        dataset_id="model-harness-dataset",
        name="Model harness dataset",
        version=1,
        market="forex",
        timeframe="M1",
        start_time=_utc(0),
        end_time=_utc(9),
        source="sample:model.csv",
        feature_version="feature_set.v1",
        quality_score="pass",
        status="frozen",
        content_hash="model-dataset-hash",
        frozen_at=_utc(9),
        market_scope={"markets": ["forex"]},
    )
    session.add(snapshot)
    await session.flush()

    rows: list[FeatureRecord] = []
    labels = [1, 1, 0, 1, 0, 0, 1]
    for idx, label in enumerate(labels):
        features = {
            "return_1": str(0.01 * (idx + 1)),
            "range_pct": str(0.02 * (idx + 1)),
            "label_direction": label,
        }
        if identity and idx == 0:
            features["symbol"] = "EURUSD"
        row = FeatureRecord(
            feature_set_version="feature_set.v1",
            provider="internal",
            market_class="forex",
            symbol="EURUSD",
            timeframe="M1",
            as_of=_utc(idx),
            features=features,
            quality_score="pass",
            source="sample:model.csv",
            source_dataset_hash=snapshot.content_hash,
        )
        session.add(row)
        rows.append(row)
    await session.flush()

    split = DatasetSplitManifest(
        dataset_snapshot_id=snapshot.id,
        split_id="model-split-v1",
        split_strategy="temporal",
        label_horizon_bars=1,
        embargo_bars=1,
        train_start=_utc(0),
        train_end=_utc(2),
        validation_start=_utc(4),
        validation_end=_utc(5),
        test_start=_utc(6),
        test_end=_utc(6),
        train_count=3,
        validation_count=2,
        test_count=1,
        split_hash="model-split-hash",
        manifest={
            "feature_set_version": "feature_set.v1",
            "split_strategy": "temporal",
            "row_ids": {
                "train": [row.id for row in rows[:3]],
                "validation": [row.id for row in rows[4:6]],
                "test": [rows[6].id],
            },
        },
        quality_summary="unit split",
    )
    session.add(split)
    await session.flush()

    service = ExperimentRegistryService(session)
    plan = ExperimentPlanInput(
        experiment_id="approved-model-harness-exp",
        version=1,
        purpose="Train pure-python baseline for harness proof",
        hypothesis="Harness only trains with approved pinned experiment",
        dataset_snapshot_id=snapshot.id,
        dataset_content_hash=snapshot.content_hash,
        split_manifest_id=split.id,
        split_manifest_hash=split.split_hash,
        feature_set_version="feature_set.v1",
        model_family="pure_python_majority_baseline",
        model_spec={"framework": "pure-python", "seed": 42},
        evaluation_plan={"split_strategy": "temporal", "metrics": ["accuracy"]},
    )
    experiment = await service.create_draft(plan)
    await service.pre_register(experiment)
    await service.approve(experiment, approver="pytest")
    return snapshot, split, experiment


@pytest.mark.asyncio
async def test_baseline_model_trains_approved_pinned_experiment(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        _, _, experiment = await _approved_experiment_fixture(session)
        result = await BaselineModelHarness(session).train(experiment_id=experiment.experiment_id)
        artifact = result.artifact
        assert artifact.status == "research_only"
        assert artifact.research_status == "research_only"
        assert artifact.experiment_id == experiment.experiment_id
        assert artifact.dataset_content_hash == experiment.dataset_content_hash
        assert artifact.split_manifest_hash == experiment.split_manifest_hash
        assert artifact.artifact_hash == result.artifact_hash
        assert artifact.metrics["baseline_note"].startswith("Majority-class baseline")
        assert artifact.metrics["validation_accuracy"] is not None


@pytest.mark.asyncio
async def test_train_without_approved_experiment_refused(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        snapshot, split, _ = await _approved_experiment_fixture(session)
        draft = Experiment(
            experiment_id="draft-experiment",
            version=1,
            status="draft",
            purpose="draft",
            hypothesis="draft",
            dataset_snapshot_id=snapshot.id,
            dataset_content_hash=snapshot.content_hash,
            split_manifest_id=split.id,
            split_manifest_hash=split.split_hash,
            feature_set_version="feature_set.v1",
            model_family="pure_python_majority_baseline",
            model_spec={},
            evaluation_plan={"split_strategy": "temporal"},
            plan_hash="draft-plan-hash",
        )
        session.add(draft)
        await session.flush()
        with pytest.raises(ExperimentNotApprovedError, match="EXPERIMENT_NOT_APPROVED"):
            await BaselineModelHarness(session).train(experiment_id=draft.experiment_id)


@pytest.mark.asyncio
async def test_unresolved_pin_refused(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        _, _, experiment = await _approved_experiment_fixture(session)
        experiment.dataset_content_hash = "wrong-hash"
        await session.flush()
        with pytest.raises(UnresolvedExperimentPinError, match="UNRESOLVED_PIN"):
            await BaselineModelHarness(session).train(experiment_id=experiment.experiment_id)


@pytest.mark.asyncio
async def test_identity_in_model_input_refused(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        _, _, experiment = await _approved_experiment_fixture(session, identity=True)
        with pytest.raises(IdentityInModelInputError, match="IDENTITY_IN_MODEL_INPUT"):
            await BaselineModelHarness(session).train(experiment_id=experiment.experiment_id)


@pytest.mark.asyncio
async def test_non_temporal_split_refused(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        _, split, experiment = await _approved_experiment_fixture(session)
        split.split_strategy = "random"
        split.manifest["split_strategy"] = "random"
        await session.flush()
        with pytest.raises(NonTemporalSplitError, match="NON_TEMPORAL_SPLIT"):
            await BaselineModelHarness(session).train(experiment_id=experiment.experiment_id)


@pytest.mark.asyncio
async def test_reproducible_retrain_same_artifact_hash_and_metrics(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        _, _, experiment = await _approved_experiment_fixture(session)
        harness = BaselineModelHarness(session)
        first = await harness.train(experiment_id=experiment.experiment_id, seed=42)
        second = await harness.train(experiment_id=experiment.experiment_id, seed=42)
        assert first.artifact_hash == second.artifact_hash
        assert first.metrics == second.metrics


def test_pure_python_baseline_has_no_external_ml_dependency() -> None:
    import app.ml.models.baseline as baseline

    source = Path(baseline.__file__).read_text(encoding="utf-8")
    assert "sklearn" not in source
    assert "numpy" not in source
    assert "pandas" not in source


def test_no_live_signal_or_model_api_endpoint_added() -> None:
    root = Path(__file__).resolve().parents[1] / "app" / "api" / "routes"
    # BO-B-05 supersession (disclosed churn): the monitoring router gained an
    # inference-HEALTH INPUT endpoint — it reports health degradation, it does
    # not perform inference. The guard's intent (no live model/signal
    # inference endpoint) still covers every other router.
    exempt = {"monitoring_alerts.py"}
    forbidden = ("model/signal", "predict", "inference", "live_signal")
    offenders: list[str] = []
    for path in root.rglob("*.py"):
        if path.name in exempt:
            continue
        text = path.read_text(encoding="utf-8")
        for needle in forbidden:
            if needle in text:
                offenders.append(f"{path.name}:{needle}")
    assert offenders == []
