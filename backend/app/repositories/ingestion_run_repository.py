"""Repository for ingestion run metadata."""

from __future__ import annotations

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.ingestion_run import IngestionRun
from app.repositories.base import BaseRepository


class IngestionRunRepository(BaseRepository[IngestionRun]):
    model = IngestionRun

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def list_recent(self, *, limit: int = 20) -> Sequence[IngestionRun]:
        stmt = select(IngestionRun).order_by(IngestionRun.started_at.desc()).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()
