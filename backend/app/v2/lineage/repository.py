"""V2 Lineage Repository — append-only lineage record persistence.

Append-only: no update() or delete() methods exist.
DB triggers enforce immutability at the database level.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.v2_lineage_record import V2LineageRecord
from app.v2.identifiers import new_id
from app.v2.lineage.contract import V2LineageRecordCreate
from app.v2.temporal.validation import utc_now


class V2LineageRepository:
    """Append-only V2 lineage record repository."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def append(self, record: V2LineageRecordCreate) -> V2LineageRecord:
        """Append a new lineage record."""
        db_record = V2LineageRecord(
            id=new_id(),
            artifact_type=record.artifact_type,
            artifact_id=record.artifact_id,
            source_artifact_ids=record.source_artifact_ids,
            computation_version=record.computation_version,
            input_snapshot_id=record.input_snapshot_id,
            operator_id=record.operator_id,
            mode=record.mode,
            created_at=utc_now(),
        )
        self._session.add(db_record)
        await self._session.flush()
        return db_record

    async def read_by_operator(
        self,
        operator_id: str,
        *,
        artifact_type: str | None = None,
        limit: int = 50,
    ) -> list[V2LineageRecord]:
        """Read lineage records for a specific operator (operator-scoped)."""
        stmt = (
            select(V2LineageRecord)
            .where(V2LineageRecord.operator_id == operator_id)
            .order_by(V2LineageRecord.created_at.desc())
            .limit(limit)
        )
        if artifact_type:
            stmt = stmt.where(V2LineageRecord.artifact_type == artifact_type)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def read_all(
        self,
        *,
        artifact_type: str | None = None,
        limit: int = 50,
    ) -> list[V2LineageRecord]:
        """Read all lineage records (admin-only, SAL-4)."""
        stmt = (
            select(V2LineageRecord)
            .order_by(V2LineageRecord.created_at.desc())
            .limit(limit)
        )
        if artifact_type:
            stmt = stmt.where(V2LineageRecord.artifact_type == artifact_type)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def read_by_artifact(
        self,
        artifact_type: str,
        artifact_id: str,
        *,
        operator_id: str | None = None,
    ) -> list[V2LineageRecord]:
        """Read lineage records for a specific artifact.

        If operator_id is provided, filters by operator (operator-scoped).
        If operator_id is None, returns all (admin-only use).
        """
        stmt = (
            select(V2LineageRecord)
            .where(
                V2LineageRecord.artifact_type == artifact_type,
                V2LineageRecord.artifact_id == artifact_id,
            )
            .order_by(V2LineageRecord.created_at.desc())
        )
        if operator_id is not None:
            stmt = stmt.where(V2LineageRecord.operator_id == operator_id)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
