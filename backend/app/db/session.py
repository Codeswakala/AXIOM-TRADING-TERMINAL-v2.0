"""Async engine, session factory, and lifecycle helpers."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import Settings, get_settings
from app.core.logging import get_logger
from app.db.base import Base

logger = get_logger(__name__, category="DATABASE")

_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None
_sqlite_staticpool_locks: dict[int, asyncio.Lock] = {}


def _uses_sqlite_staticpool(settings: Settings) -> bool:
    """Return true for SQLite configurations that share one async connection.

    W3-U08.1: the in-memory SQLite test harness uses StaticPool so background
    live-market writes and request-scoped writes can otherwise race on the same
    aiosqlite connection. PostgreSQL and other DBs are unaffected.
    """
    return settings.is_sqlite and ":memory:" in settings.database_url


def _sqlite_staticpool_lock() -> asyncio.Lock:
    loop_id = id(asyncio.get_running_loop())
    lock = _sqlite_staticpool_locks.get(loop_id)
    if lock is None:
        lock = asyncio.Lock()
        _sqlite_staticpool_locks[loop_id] = lock
    return lock


@asynccontextmanager
async def sqlite_staticpool_serialization(settings: Settings) -> AsyncIterator[None]:
    """Serialize DB work only for SQLite StaticPool test harnesses."""
    if not _uses_sqlite_staticpool(settings):
        yield
        return
    async with _sqlite_staticpool_lock():
        yield


def _engine_kwargs(settings: Settings) -> dict[str, Any]:
    from sqlalchemy.pool import StaticPool

    kwargs: dict[str, Any] = {
        "echo": settings.database_echo,
        "future": True,
    }
    if settings.is_sqlite:
        # StaticPool keeps a single connection so :memory: databases are shared
        # across sessions (critical for tests and seed-on-start).
        kwargs["connect_args"] = {"check_same_thread": False}
        kwargs["poolclass"] = StaticPool
    else:
        kwargs["pool_size"] = settings.database_pool_size
        kwargs["max_overflow"] = settings.database_max_overflow
        kwargs["pool_timeout"] = settings.database_pool_timeout
        kwargs["pool_pre_ping"] = True
    return kwargs


def create_engine(settings: Settings | None = None) -> AsyncEngine:
    settings = settings or get_settings()
    logger.info(
        "Creating async engine backend=%s echo=%s",
        settings.database_backend_name,
        settings.database_echo,
    )
    return create_async_engine(settings.database_url, **_engine_kwargs(settings))


def init_db(settings: Settings | None = None) -> async_sessionmaker[AsyncSession]:
    """Initialize global engine and session factory (idempotent)."""
    global _engine, _session_factory
    if _session_factory is not None and _engine is not None:
        return _session_factory

    settings = settings or get_settings()
    _engine = create_engine(settings)
    _session_factory = async_sessionmaker(
        bind=_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )
    logger.info("Database session factory initialized")
    return _session_factory


def get_engine() -> AsyncEngine:
    if _engine is None:
        init_db()
    assert _engine is not None
    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    if _session_factory is None:
        return init_db()
    return _session_factory


async def create_schema() -> None:
    """Create tables from metadata (dev convenience; Alembic owns evolution)."""
    # Import models so metadata is populated.
    from app.db import models  # noqa: F401

    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Schema ensure complete (metadata.create_all)")


async def drop_schema() -> None:
    """Drop all tables (tests only)."""
    from app.db import models  # noqa: F401

    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    logger.info("Schema drop complete")


async def close_db() -> None:
    """Dispose engine and clear globals."""
    global _engine, _session_factory
    if _engine is not None:
        await _engine.dispose()
        logger.info("Database engine disposed")
    _engine = None
    _session_factory = None


@asynccontextmanager
async def session_scope() -> AsyncIterator[AsyncSession]:
    """Provide a transactional scope around a series of operations."""
    settings = get_settings()
    factory = get_session_factory()
    session = factory()
    async with sqlite_staticpool_serialization(settings):
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            logger.exception("Database transaction rolled back")
            raise
        finally:
            await session.close()


async def get_db_session() -> AsyncIterator[AsyncSession]:
    """FastAPI dependency: yield a request-scoped session with commit/rollback."""
    settings = get_settings()
    factory = get_session_factory()
    session = factory()
    async with sqlite_staticpool_serialization(settings):
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
