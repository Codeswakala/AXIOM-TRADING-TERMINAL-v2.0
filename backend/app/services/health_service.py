"""Health and readiness domain service.

Business logic is isolated from API routers per SYSTEM_ARCHITECTURE.md.
"""

from __future__ import annotations

import time

from app.core.config import Settings
from app.core.logging import get_logger
from app.core.time import utc_now
from app.models.health import HealthResponse, ReadinessResponse, ServiceStatus
from app.services.database_health import check_database

logger = get_logger(__name__, category="SYSTEM")


class HealthService:
    """Evaluate process liveness and foundation readiness."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def liveness(self) -> HealthResponse:
        started = time.perf_counter()
        logger.debug("Liveness probe requested")
        latency_ms = (time.perf_counter() - started) * 1000.0
        return HealthResponse(
            status="ok",
            service=self._settings.app_name,
            version=self._settings.version,
            environment=self._settings.environment,
            timestamp=utc_now(),
            latency_ms=latency_ms,
        )

    async def readiness(self) -> ReadinessResponse:
        """Readiness includes real subsystem status and per-check latency."""
        db = await check_database(self._settings)

        checks = [
            ServiceStatus(
                name="configuration",
                status="up",
                detail=f"environment={self._settings.environment}",
                latency_ms=0.0,
            ),
            ServiceStatus(
                name="logging",
                status="up",
                detail="structured logging with correlation IDs configured",
                latency_ms=0.0,
            ),
            ServiceStatus(
                name="database",
                status=db.status,  # type: ignore[arg-type]
                detail=db.detail,
                latency_ms=db.latency_ms,
            ),
            ServiceStatus(
                name="ml_engine",
                status="stub",
                detail="ML platform deferred (Wave 2+); package stub present",
                latency_ms=0.0,
            ),
            ServiceStatus(
                name="broker",
                status="stub",
                detail=(
                    "Broker integration framework present; governance gate closed; "
                    "no connection/execution"
                ),
                latency_ms=0.0,
            ),
            ServiceStatus(
                name="market_ingestion",
                status="up",
                detail="Historical CSV ingestion available",
                latency_ms=0.0,
            ),
            ServiceStatus(
                name="authentication",
                status="up",
                detail=(
                    "JWT operator auth enabled"
                    + (
                        " (explicit local/test insecure-dev mode)"
                        if self._settings.jwt_secret_is_insecure
                        else ""
                    )
                ),
                latency_ms=0.0,
            ),
        ]

        # Live market feed (W0-U05) — imported lazily to avoid circular imports at module load.
        live_started = time.perf_counter()
        from app.market.live_service import get_live_market_service

        live_status, live_detail = get_live_market_service().readiness_detail()
        live_latency = (time.perf_counter() - live_started) * 1000.0
        checks.append(
            ServiceStatus(
                name="live_market",
                status=live_status,  # type: ignore[arg-type]
                detail=live_detail,
                latency_ms=live_latency,
            )
        )

        critical_names = {"configuration", "logging", "database"}
        critical_ok = all(
            check.status in {"up", "degraded"}
            for check in checks
            if check.name in critical_names
        )
        # Degraded DB still allows ready=true with visibility; down DB is not ready.
        db_down = db.status == "down"
        status = "not_ready" if db_down or not critical_ok else "ready"
        logger.info("Readiness probe status=%s database=%s", status, db.status)
        return ReadinessResponse(
            status=status,
            service=self._settings.app_name,
            version=self._settings.version,
            environment=self._settings.environment,
            timestamp=utc_now(),
            checks=checks,
        )
