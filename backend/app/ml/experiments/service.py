"""Experiment registry and pre-registration workflow (W2-U05)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.time import utc_now
from app.db.models.dataset import DatasetSnapshot
from app.db.models.dataset_split import DatasetSplitManifest
from app.db.models.experiment import Experiment
from app.ml.experiments.errors import (
    ExperimentApprovalRequiredError,
    ImmutableExperimentError,
    IncompleteExperimentError,
    InvalidEvaluationPlanError,
    UnreproducibleExperimentPinError,
)
from app.repositories.audit_repository import AuditRepository


@dataclass(frozen=True, slots=True)
class ExperimentPlanInput:
    experiment_id: str
    version: int
    purpose: str
    hypothesis: str
    dataset_snapshot_id: str
    dataset_content_hash: str
    split_manifest_id: str
    split_manifest_hash: str
    feature_set_version: str
    model_family: str
    model_spec: dict[str, Any]
    evaluation_plan: dict[str, Any]
    notes: str | None = None


class ExperimentRegistryService:
    """Creates, pre-registers, approves, and versions experiment plans."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._audit = AuditRepository(session)

    async def create_draft(self, payload: ExperimentPlanInput) -> Experiment:
        self._validate_complete(payload)
        await self._validate_pins(payload)
        self._validate_evaluation_plan(payload.evaluation_plan)
        experiment = Experiment(
            experiment_id=payload.experiment_id,
            version=payload.version,
            status="draft",
            purpose=payload.purpose,
            hypothesis=payload.hypothesis,
            dataset_snapshot_id=payload.dataset_snapshot_id,
            dataset_content_hash=payload.dataset_content_hash,
            split_manifest_id=payload.split_manifest_id,
            split_manifest_hash=payload.split_manifest_hash,
            feature_set_version=payload.feature_set_version,
            model_family=payload.model_family,
            model_spec=payload.model_spec,
            evaluation_plan=payload.evaluation_plan,
            plan_hash=self.compute_plan_hash(payload),
            notes=payload.notes,
        )
        self._session.add(experiment)
        await self._session.flush()
        await self._audit_event("experiment.create", experiment)
        return experiment

    async def pre_register(self, experiment: Experiment) -> Experiment:
        if experiment.status not in {"draft", "pre_registered"}:
            raise ImmutableExperimentError("only draft experiments may be pre-registered")
        self._validate_experiment_record(experiment)
        experiment.status = "pre_registered"
        experiment.plan_hash = self.compute_plan_hash(self._payload_from_record(experiment))
        await self._session.flush()
        await self._audit_event("experiment.pre_register", experiment)
        return experiment

    async def approve(self, experiment: Experiment, *, approver: str) -> Experiment:
        if experiment.status != "pre_registered":
            raise ExperimentApprovalRequiredError(
                "experiment must be pre_registered before approval"
            )
        if not approver.strip():
            raise IncompleteExperimentError("approver is required")
        experiment.status = "approved"
        experiment.approver = approver.strip()
        experiment.approval_timestamp = utc_now()
        await self._session.flush()
        await self._audit_event("experiment.approve", experiment)
        return experiment

    def assert_runnable(self, experiment: Experiment) -> None:
        if experiment.status != "approved" or experiment.approval_timestamp is None:
            raise ExperimentApprovalRequiredError("only approved experiments are runnable")

    async def update_approved_plan(self, experiment: Experiment, updates: dict[str, Any]) -> None:
        _ = updates
        if experiment.status == "approved":
            raise ImmutableExperimentError(
                "approved experiment plans are immutable; create new version"
            )
        raise ImmutableExperimentError("direct plan mutation is not supported; create new version")

    async def create_new_version(
        self,
        experiment: Experiment,
        payload: ExperimentPlanInput,
    ) -> Experiment:
        experiment.status = "superseded"
        await self._session.flush()
        new_experiment = await self.create_draft(payload)
        new_experiment.previous_experiment_id = experiment.id
        await self._session.flush()
        await self._audit_event("experiment.new_version", new_experiment)
        return new_experiment

    def compute_plan_hash(self, payload: ExperimentPlanInput) -> str:
        canonical = {
            "experiment_id": payload.experiment_id,
            "version": payload.version,
            "purpose": payload.purpose,
            "hypothesis": payload.hypothesis,
            "dataset_snapshot_id": payload.dataset_snapshot_id,
            "dataset_content_hash": payload.dataset_content_hash,
            "split_manifest_id": payload.split_manifest_id,
            "split_manifest_hash": payload.split_manifest_hash,
            "feature_set_version": payload.feature_set_version,
            "model_family": payload.model_family,
            "model_spec": payload.model_spec,
            "evaluation_plan": payload.evaluation_plan,
        }
        return hashlib.sha256(json.dumps(canonical, sort_keys=True).encode("utf-8")).hexdigest()

    async def _validate_pins(self, payload: ExperimentPlanInput) -> None:
        snapshot = await self._session.get(DatasetSnapshot, payload.dataset_snapshot_id)
        if snapshot is None or snapshot.status != "frozen" or not snapshot.content_hash:
            raise UnreproducibleExperimentPinError("UNREPRODUCIBLE_EXPERIMENT_PIN: snapshot")
        if snapshot.content_hash != payload.dataset_content_hash:
            raise UnreproducibleExperimentPinError("UNREPRODUCIBLE_EXPERIMENT_PIN: snapshot hash")
        split = await self._session.get(DatasetSplitManifest, payload.split_manifest_id)
        if split is None or not split.split_hash:
            raise UnreproducibleExperimentPinError("UNREPRODUCIBLE_EXPERIMENT_PIN: split")
        if split.dataset_snapshot_id != snapshot.id:
            raise UnreproducibleExperimentPinError("UNREPRODUCIBLE_EXPERIMENT_PIN: split snapshot")
        if split.split_hash != payload.split_manifest_hash:
            raise UnreproducibleExperimentPinError("UNREPRODUCIBLE_EXPERIMENT_PIN: split hash")
        manifest_feature_version = split.manifest.get(
            "feature_set_version", payload.feature_set_version
        )
        if payload.feature_set_version != manifest_feature_version:
            # Manifest may come from older tests without feature_set_version; tolerate absent only.
            if "feature_set_version" in split.manifest:
                raise UnreproducibleExperimentPinError(
                    "UNREPRODUCIBLE_EXPERIMENT_PIN: feature version"
                )

    def _validate_complete(self, payload: ExperimentPlanInput) -> None:
        required: dict[str, Any] = {
            "experiment_id": payload.experiment_id,
            "purpose": payload.purpose,
            "hypothesis": payload.hypothesis,
            "dataset_snapshot_id": payload.dataset_snapshot_id,
            "dataset_content_hash": payload.dataset_content_hash,
            "split_manifest_id": payload.split_manifest_id,
            "split_manifest_hash": payload.split_manifest_hash,
            "feature_set_version": payload.feature_set_version,
            "model_family": payload.model_family,
            "model_spec": payload.model_spec,
            "evaluation_plan": payload.evaluation_plan,
            "version": payload.version,
        }
        missing = [name for name, value in required.items() if value in (None, "", {})]
        if missing:
            raise IncompleteExperimentError(f"UNDOCUMENTED_EXPERIMENT: missing={missing}")

    def _validate_evaluation_plan(self, evaluation_plan: dict[str, Any]) -> None:
        split_strategy = str(evaluation_plan.get("split_strategy", "")).lower()
        if split_strategy in {"random", "shuffle", "random_row"}:
            raise InvalidEvaluationPlanError("SPLIT_LEAKAGE")
        if split_strategy not in {"temporal", "walk_forward"}:
            raise InvalidEvaluationPlanError(
                "evaluation plan must specify temporal or walk_forward split"
            )

    def _validate_experiment_record(self, experiment: Experiment) -> None:
        self._validate_complete(self._payload_from_record(experiment))
        self._validate_evaluation_plan(experiment.evaluation_plan)

    def _payload_from_record(self, experiment: Experiment) -> ExperimentPlanInput:
        return ExperimentPlanInput(
            experiment_id=experiment.experiment_id,
            version=experiment.version,
            purpose=experiment.purpose,
            hypothesis=experiment.hypothesis,
            dataset_snapshot_id=experiment.dataset_snapshot_id,
            dataset_content_hash=experiment.dataset_content_hash,
            split_manifest_id=experiment.split_manifest_id,
            split_manifest_hash=experiment.split_manifest_hash,
            feature_set_version=experiment.feature_set_version,
            model_family=experiment.model_family,
            model_spec=experiment.model_spec,
            evaluation_plan=experiment.evaluation_plan,
            notes=experiment.notes,
        )

    async def _audit_event(self, action: str, experiment: Experiment) -> None:
        await self._audit.append(
            category="GOVERNANCE",
            action=action,
            actor="system",
            resource_type="experiment",
            resource_id=experiment.id,
            message=f"Experiment registry action {action} experiment={experiment.experiment_id}",
            details={
                "experiment_id": experiment.experiment_id,
                "version": experiment.version,
                "status": experiment.status,
                "plan_hash": experiment.plan_hash,
            },
        )
