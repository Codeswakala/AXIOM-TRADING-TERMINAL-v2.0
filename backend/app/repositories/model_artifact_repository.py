"""Model artifact metadata repository."""

from __future__ import annotations

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.model_artifact import ModelArtifact
from app.repositories.base import BaseRepository


class ModelArtifactRepository(BaseRepository[ModelArtifact]):
    model = ModelArtifact

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get_by_name_version(self, name: str, version: str) -> ModelArtifact | None:
        stmt = select(ModelArtifact).where(
            ModelArtifact.name == name,
            ModelArtifact.version == version,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_status(self, status: str, *, limit: int = 50) -> Sequence[ModelArtifact]:
        stmt = (
            select(ModelArtifact)
            .where(ModelArtifact.status == status)
            .order_by(ModelArtifact.registered_at.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
