"""Institutional Intelligence artifact contracts (W4-U01)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Mapping, Sequence
from uuid import uuid4

from app.core.time import require_utc, utc_now

FORBIDDEN_ACTION_KEYS = {
    "order_payload",
    "order_intent",
    "execution_payload",
    "remediation_payload",
    "signal_payload",
    "broker_account_id",
    "quantity",
    "target_price",
    "position_payload",
    "position_size",
    "order_size",
    "stop_loss",
    "take_profit",
    "auto_retrain",
    "retrain_triggered",
}


@dataclass(frozen=True, slots=True)
class IntelligenceArtifactContract:
    """Common inert report/artifact contract for future Wave-4 intelligence reports."""

    artifact_id: str
    created_at: datetime
    artifact_type: str
    method_version: str
    config: Mapping[str, Any]
    input_lineage: Mapping[str, Any]
    source_artifact_ids: Sequence[str]
    market_scope: Mapping[str, Any]
    as_of_start: datetime
    as_of_end: datetime
    sample_count: int
    uncertainty: Mapping[str, Any]
    results: Mapping[str, Any]
    limitations: Sequence[str]
    report_hash: str
    research_status: str
    created_by: str
    audit_correlation_id: str

    def to_audit_details(self) -> dict[str, Any]:
        """Return the future audit-event details payload for this artifact."""
        return {
            "artifact_id": self.artifact_id,
            "artifact_type": self.artifact_type,
            "method_version": self.method_version,
            "report_hash": self.report_hash,
            "research_status": self.research_status,
            "source_artifact_ids": list(self.source_artifact_ids),
            "audit_correlation_id": self.audit_correlation_id,
        }


@dataclass(frozen=True, slots=True)
class IntelligenceArtifactDraft:
    """Draft payload used to create an immutable intelligence artifact contract."""

    artifact_type: str
    method_version: str
    config: Mapping[str, Any]
    input_lineage: Mapping[str, Any]
    source_artifact_ids: Sequence[str]
    market_scope: Mapping[str, Any]
    as_of_start: datetime
    as_of_end: datetime
    sample_count: int
    uncertainty: Mapping[str, Any]
    results: Mapping[str, Any]
    limitations: Sequence[str]
    created_by: str
    research_status: str = "research_only"
    audit_correlation_id: str = field(default_factory=lambda: str(uuid4()))


class IntelligenceArtifactFactory:
    """Builds validated inert artifact contracts.

    The factory does not persist anything in W4-U01. Future units may combine this
    contract with their own Alembic-backed tables and AuditRepository writes.
    """

    def build(self, draft: IntelligenceArtifactDraft) -> IntelligenceArtifactContract:
        as_of_start = require_utc(draft.as_of_start, boundary="intelligence_artifact.as_of_start")
        as_of_end = require_utc(draft.as_of_end, boundary="intelligence_artifact.as_of_end")
        assert as_of_start is not None and as_of_end is not None
        created_at = utc_now()
        if as_of_start > as_of_end:
            raise ValueError("ARTIFACT_AS_OF_RANGE_INVALID")
        if draft.sample_count < 0:
            raise ValueError("ARTIFACT_SAMPLE_COUNT_INVALID")
        if draft.research_status != "research_only":
            raise ValueError("ARTIFACT_RESEARCH_ONLY_REQUIRED")
        self._assert_inert(draft.config, path="config")
        self._assert_inert(draft.results, path="results")
        self._assert_uncertainty(draft.uncertainty)
        artifact_id = str(uuid4())
        report_hash = self._report_hash(
            artifact_id=artifact_id,
            draft=draft,
            as_of_start=as_of_start,
            as_of_end=as_of_end,
        )
        return IntelligenceArtifactContract(
            artifact_id=artifact_id,
            created_at=created_at,
            artifact_type=draft.artifact_type,
            method_version=draft.method_version,
            config=dict(draft.config),
            input_lineage=dict(draft.input_lineage),
            source_artifact_ids=tuple(draft.source_artifact_ids),
            market_scope=dict(draft.market_scope),
            as_of_start=as_of_start,
            as_of_end=as_of_end,
            sample_count=draft.sample_count,
            uncertainty=dict(draft.uncertainty),
            results=dict(draft.results),
            limitations=tuple(draft.limitations),
            report_hash=report_hash,
            research_status=draft.research_status,
            created_by=draft.created_by,
            audit_correlation_id=draft.audit_correlation_id,
        )

    def _assert_uncertainty(self, uncertainty: Mapping[str, Any]) -> None:
        required = {"method", "confidence_level", "sample_count"}
        missing = required.difference(uncertainty)
        if missing:
            raise ValueError("ARTIFACT_UNCERTAINTY_REQUIRED:" + ",".join(sorted(missing)))

    def _assert_inert(self, value: Any, *, path: str) -> None:
        if isinstance(value, Mapping):
            for key, nested in value.items():
                key_text = str(key)
                if key_text in FORBIDDEN_ACTION_KEYS:
                    raise ValueError(f"ARTIFACT_ACTION_PAYLOAD_FORBIDDEN:{path}.{key_text}")
                self._assert_inert(nested, path=f"{path}.{key_text}")
        elif isinstance(value, list | tuple):
            for index, nested in enumerate(value):
                self._assert_inert(nested, path=f"{path}[{index}]")

    def _report_hash(
        self,
        *,
        artifact_id: str,
        draft: IntelligenceArtifactDraft,
        as_of_start: datetime,
        as_of_end: datetime,
    ) -> str:
        payload = {
            "artifact_id": artifact_id,
            "artifact_type": draft.artifact_type,
            "method_version": draft.method_version,
            "config": draft.config,
            "input_lineage": draft.input_lineage,
            "source_artifact_ids": list(draft.source_artifact_ids),
            "market_scope": draft.market_scope,
            "as_of_start": as_of_start.isoformat(),
            "as_of_end": as_of_end.isoformat(),
            "sample_count": draft.sample_count,
            "uncertainty": draft.uncertainty,
            "results": draft.results,
            "limitations": list(draft.limitations),
            "research_status": draft.research_status,
            "created_by": draft.created_by,
            "audit_correlation_id": draft.audit_correlation_id,
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
