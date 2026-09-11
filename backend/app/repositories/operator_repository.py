"""Operator repository."""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.operator import Operator
from app.repositories.base import BaseRepository


class OperatorRepository(BaseRepository[Operator]):
    model = Operator

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get_by_username(self, username: str) -> Operator | None:
        stmt = select(Operator).where(Operator.username == username.lower())
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def count_operators(self) -> int:
        result = await self.session.execute(select(func.count()).select_from(Operator))
        return int(result.scalar_one())
