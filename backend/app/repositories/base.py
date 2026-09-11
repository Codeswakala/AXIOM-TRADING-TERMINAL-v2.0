"""Generic asynchronous repository foundation (W0-U08.1 audit-safe)."""

from __future__ import annotations

from typing import Any, Generic, Sequence, TypeVar

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.db.base import Base

ModelT = TypeVar("ModelT", bound=Base)
logger = get_logger(__name__, category="DATABASE")


class BaseRepository(Generic[ModelT]):
    """Reusable CRUD helpers for SQLAlchemy models.

    Concrete repositories specialize query methods; this base keeps the
    data-access layer replaceable and free of HTTP concerns.
    """

    model: type[ModelT]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, entity_id: Any) -> ModelT | None:
        logger.debug("get_by_id model=%s id=%s", self.model.__name__, entity_id)
        return await self.session.get(self.model, entity_id)

    async def list(
        self,
        *,
        limit: int = 100,
        offset: int = 0,
        statement: Select[Any] | None = None,
    ) -> Sequence[ModelT]:
        stmt = statement if statement is not None else select(self.model)
        stmt = stmt.limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        rows = result.scalars().all()
        logger.debug("list model=%s count=%s", self.model.__name__, len(rows))
        return rows

    async def count(self, statement: Select[Any] | None = None) -> int:
        if statement is None:
            stmt = select(func.count()).select_from(self.model)
        else:
            stmt = select(func.count()).select_from(statement.subquery())
        result = await self.session.execute(stmt)
        return int(result.scalar_one())

    async def add(self, entity: ModelT, *, refresh: bool = True) -> ModelT:
        """Insert entity.

        ``refresh`` is best-effort: some drivers/models can fail refresh after
        insert; business endpoints must not 500 solely because refresh fails.
        """
        self.session.add(entity)
        await self.session.flush()
        if refresh:
            try:
                await self.session.refresh(entity)
            except Exception as exc:  # noqa: BLE001 — never fail the write for refresh
                logger.warning(
                    "refresh skipped model=%s id=%s err=%s",
                    self.model.__name__,
                    getattr(entity, "id", None),
                    exc,
                )
        logger.info("add model=%s id=%s", self.model.__name__, getattr(entity, "id", None))
        return entity

    async def add_many(
        self,
        entities: Sequence[ModelT],
        *,
        refresh: bool = True,
    ) -> Sequence[ModelT]:
        self.session.add_all(list(entities))
        await self.session.flush()
        if refresh:
            for entity in entities:
                try:
                    await self.session.refresh(entity)
                except Exception as exc:  # noqa: BLE001
                    logger.warning(
                        "refresh skipped model=%s id=%s err=%s",
                        self.model.__name__,
                        getattr(entity, "id", None),
                        exc,
                    )
        logger.info("add_many model=%s count=%s", self.model.__name__, len(entities))
        return entities

    async def delete(self, entity: ModelT) -> None:
        await self.session.delete(entity)
        await self.session.flush()
        logger.info("delete model=%s id=%s", self.model.__name__, getattr(entity, "id", None))
