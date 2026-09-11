"""V2 Lineage Contract — artifact metadata and source tracking.

Append-only: no update() or delete() methods exist.
DB triggers enforce immutability at the database level.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class V2LineageRecordCreate:
    """Contract for creating a V2 lineage record."""

    artifact_type: str
    artifact_id: str
    operator_id: str
    mode: str  # "RESEARCH" or "SIMULATION"
    source_artifact_ids: list[str] | None = None
    computation_version: str | None = None
    input_snapshot_id: str | None = None


@dataclass(frozen=True, slots=True)
class V2LineageRecordRead:
    """Contract for reading a V2 lineage record."""

    id: str
    artifact_type: str
    artifact_id: str
    operator_id: str
    mode: str
    source_artifact_ids: list[str] | None
    computation_version: str | None
    input_snapshot_id: str | None
    created_at: datetime
