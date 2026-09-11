"""Feature record repository (placeholder store)."""

from __future__ import annotations

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.feature import FeatureRecord
from app.repositories.base import BaseRepository


class FeatureRepository(BaseRepository[FeatureRecord]):
    model = FeatureRecord

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def list_for_symbol(
        self,
        *,
        symbol: str,
        feature_set_version: str | None = None,
        limit: int = 50,
    ) -> Sequence[FeatureRecord]:
        stmt = select(FeatureRecord).where(FeatureRecord.symbol == symbol)
        if feature_set_version is not None:
            stmt = stmt.where(FeatureRecord.feature_set_version == feature_set_version)
        stmt = stmt.order_by(FeatureRecord.as_of.desc()).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()
