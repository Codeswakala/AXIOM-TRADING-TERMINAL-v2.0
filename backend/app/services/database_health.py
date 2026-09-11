"""Database connectivity and pool observability helpers."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

from sqlalchemy import text

from app.core.config import Settings
from app.core.logging import get_logger
from app.db.session import get_engine

logger = get_logger(__name__, category="DATABASE")


@dataclass(slots=True)
class DatabaseHealthResult:
    status: str  # up | down | degraded
    detail: str
    latency_ms: float | None
    backend: str
    pool: dict[str, Any]


async def check_database(settings: Settings) -> DatabaseHealthResult:
    """Execute a trivial query and capture latency + pool stats."""
    backend = settings.database_backend_name
    pool_stats: dict[str, Any] = {}
    try:
        engine = get_engine()
        pool = engine.sync_engine.pool
        # QueuePool exposes these; NullPool/StaticPool may not.
        for attr in ("size", "checkedin", "checkedout", "overflow"):
            method = getattr(pool, attr, None)
            if callable(method):
                try:
                    pool_stats[attr] = method()
                except Exception:  # noqa: BLE001 — pool introspection is best-effort
                    pool_stats[attr] = None

        started = time.perf_counter()
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        latency_ms = (time.perf_counter() - started) * 1000.0
        detail = f"backend={backend}; latency_ms={latency_ms:.2f}"
        logger.debug("Database health check ok %s", detail)
        status = "up"
        if latency_ms > 500:
            status = "degraded"
            detail += "; elevated_latency"
        return DatabaseHealthResult(
            status=status,
            detail=detail,
            latency_ms=latency_ms,
            backend=backend,
            pool=pool_stats,
        )
    except Exception as exc:  # noqa: BLE001 — readiness must never raise
        logger.exception("Database health check failed")
        return DatabaseHealthResult(
            status="down",
            detail=f"backend={backend}; error={exc.__class__.__name__}: {exc}",
            latency_ms=None,
            backend=backend,
            pool=pool_stats,
        )
