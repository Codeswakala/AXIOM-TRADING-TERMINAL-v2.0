"""W2-U05 experiment registry and pre-registration tests."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path

import pytest

from app.db.models.audit import AuditEvent
from app.db.models.dataset import DatasetSnapshot
from app.db.models.dataset_split import DatasetSplitManifest
from app.ml.experiments import (
    ExperimentApprovalRequiredError,
    ExperimentPlanInput,
    ExperimentRegistryService,
    ImmutableExperimentError,
    IncompleteExperimentError,
    InvalidEvaluationPlanError,
    UnreproducibleExperimentPinError,
)


def _utc(minute: int = 0) -> datetime:
    return datetime(2026, 7, 13, 19, minute, tzinfo=timezone.utc)


def _plan(
    *,
    snapshot: DatasetSnapshot,
    split: DatasetSplitManifest,
    experiment_id: str = "exp-w2-u05-unit",
    version: int = 1,
) -> ExperimentPlanInput:
    return ExperimentPlanInput(
        experiment_id=experiment_id,
        version=version,
        purpose="Validate future baseline model harness wiring without running a model",
        hypothesis="A pre-registered pinned experiment can be approved before model work",
        dataset_snapshot_id=snapshot.id,
        dataset_content_hash=snapshot.content_hash or "",
        split_manifest_id=split.id,
        split_manifest_hash=split.split_hash,
        feature_set_version="feature_set.v1",
        model_family="baseline_future_inert",
        model_spec={"family": "baseline_future_inert", "training_enabled": False},
        evaluation_plan={"split_strategy": "temporal", "metrics": ["placeholder_accuracy"]},
        notes="No model/training/inference in W2-U05",
    )


async def _frozen_snapshot_and_split(session) -> tuple[DatasetSnapshot, DatasetSplitManifest]:  # noqa: ANN001
    snapshot = DatasetSnapshot(
        dataset_id="ds-exp-unit",
        name="Experiment registry unit dataset",
        version=1,
        market="forex",
        timeframe="M1",
        start_time=_utc(0),
        end_time=_utc(9),
        source="sample:experiment.csv",
        feature_version="feature_set.v1",
        quality_score="pass",
        status="frozen",
        content_hash="snapshot-hash-abc123",
        frozen_at=_utc(9),
        created_by="pytest",
    )
    session.add(snapshot)
    await session.flush()
    split = DatasetSplitManifest(
        dataset_snapshot_id=snapshot.id,
        split_id="split-temporal-v1",
        split_strategy="temporal",
        label_horizon_bars=1,
        embargo_bars=1,
        train_start=_utc(0),
        train_end=_utc(2),
        validation_start=_utc(5),
        validation_end=_utc(6),
        test_start=_utc(8),
        test_end=_utc(9),
        train_count=3,
        validation_count=2,
        test_count=2,
        split_hash="split-hash-def456",
        manifest={"feature_set_version": "feature_set.v1", "split_strategy": "temporal"},
        quality_summary="unit test split manifest",
    )
    session.add(split)
    await session.flush()
    return snapshot, split


@pytest.mark.asyncio
async def test_undocumented_experiment_rejected(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        snapshot, split = await _frozen_snapshot_and_split(session)
        service = ExperimentRegistryService(session)
        bad = _plan(snapshot=snapshot, split=split)
        bad = replace(bad, purpose="")
        with pytest.raises(IncompleteExperimentError, match="UNDOCUMENTED_EXPERIMENT"):
            await service.create_draft(bad)


@pytest.mark.asyncio
async def test_unpinned_unfrozen_or_unhashed_experiment_rejected(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        snapshot, split = await _frozen_snapshot_and_split(session)
        service = ExperimentRegistryService(session)

        draft_snapshot = DatasetSnapshot(
            dataset_id="ds-exp-draft",
            name="Draft snapshot",
            version=1,
            market="forex",
            timeframe="M1",
            start_time=_utc(0),
            end_time=_utc(9),
            source="sample:experiment.csv",
            feature_version="feature_set.v1",
            quality_score="draft",
            status="draft",
            content_hash="draft-hash",
        )
        session.add(draft_snapshot)
        await session.flush()
        bad_snapshot_plan = _plan(
            snapshot=draft_snapshot, split=split, experiment_id="exp-bad-draft"
        )
        with pytest.raises(UnreproducibleExperimentPinError, match="snapshot"):
            await service.create_draft(bad_snapshot_plan)

        split.split_hash = ""
        bad_split_plan = replace(
            _plan(snapshot=snapshot, split=split, experiment_id="exp-bad-split"),
            split_manifest_hash="claimed-split-hash",
        )
        with pytest.raises(UnreproducibleExperimentPinError, match="split"):
            await service.create_draft(bad_split_plan)


@pytest.mark.asyncio
async def test_pre_registered_and_approved_experiment_accepted(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        snapshot, split = await _frozen_snapshot_and_split(session)
        service = ExperimentRegistryService(session)
        experiment = await service.create_draft(_plan(snapshot=snapshot, split=split))
        assert experiment.status == "draft"
        await service.pre_register(experiment)
        assert experiment.status == "pre_registered"
        await service.approve(experiment, approver="ITRGA-test")
        assert experiment.status == "approved"
        assert experiment.approval_timestamp is not None
        assert experiment.approver == "ITRGA-test"
        assert experiment.dataset_content_hash == snapshot.content_hash
        assert experiment.split_manifest_hash == split.split_hash
        service.assert_runnable(experiment)


@pytest.mark.asyncio
async def test_approval_required_before_runnable(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        snapshot, split = await _frozen_snapshot_and_split(session)
        service = ExperimentRegistryService(session)
        experiment = await service.create_draft(_plan(snapshot=snapshot, split=split))
        with pytest.raises(ExperimentApprovalRequiredError):
            service.assert_runnable(experiment)
        await service.pre_register(experiment)
        with pytest.raises(ExperimentApprovalRequiredError):
            service.assert_runnable(experiment)


@pytest.mark.asyncio
async def test_approved_plan_immutable_new_version_created(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        snapshot, split = await _frozen_snapshot_and_split(session)
        service = ExperimentRegistryService(session)
        experiment = await service.create_draft(_plan(snapshot=snapshot, split=split))
        await service.pre_register(experiment)
        await service.approve(experiment, approver="ITRGA-test")
        with pytest.raises(ImmutableExperimentError):
            await service.update_approved_plan(experiment, {"hypothesis": "post hoc rewrite"})
        new_payload = _plan(snapshot=snapshot, split=split, version=2)
        new_version = await service.create_new_version(experiment, new_payload)
        assert experiment.status == "superseded"
        assert new_version.version == 2
        assert new_version.previous_experiment_id == experiment.id


@pytest.mark.asyncio
async def test_random_split_evaluation_plan_rejected(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        snapshot, split = await _frozen_snapshot_and_split(session)
        service = ExperimentRegistryService(session)
        bad = _plan(snapshot=snapshot, split=split)
        bad = replace(bad, evaluation_plan={"split_strategy": "random"})
        with pytest.raises(InvalidEvaluationPlanError, match="SPLIT_LEAKAGE"):
            await service.create_draft(bad)


@pytest.mark.asyncio
async def test_audit_events_written_for_workflow(prepared_db: None) -> None:
    from sqlalchemy import select

    from app.db.session import session_scope

    async with session_scope() as session:
        snapshot, split = await _frozen_snapshot_and_split(session)
        service = ExperimentRegistryService(session)
        experiment = await service.create_draft(_plan(snapshot=snapshot, split=split))
        await service.pre_register(experiment)
        await service.approve(experiment, approver="ITRGA-test")
        result = await session.execute(
            select(AuditEvent.action).where(AuditEvent.resource_type == "experiment")
        )
        actions = {row[0] for row in result.all()}
        assert {
            "experiment.create",
            "experiment.pre_register",
            "experiment.approve",
        }.issubset(actions)


def test_no_model_training_code_introduced_in_experiment_registry() -> None:
    root = Path(__file__).resolve().parents[1] / "app" / "ml" / "experiments"
    forbidden = ("fit(", "predict(", "train_test_split", "RandomForest", "XGBoost", "LightGBM")
    offenders: list[str] = []
    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for needle in forbidden:
            if needle in text:
                offenders.append(f"{path.relative_to(root)}:{needle}")
    assert offenders == []
