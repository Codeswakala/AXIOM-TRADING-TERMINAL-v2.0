"""Direct service-layer unit tests."""

from __future__ import annotations

import pytest

from app.core.config import Settings
from app.services.health_service import HealthService


@pytest.mark.asyncio
async def test_health_service_liveness() -> None:
    service = HealthService(Settings(environment="testing", version="0.2.0"))
    result = service.liveness()
    assert result.status == "ok"
    assert result.environment == "testing"


@pytest.mark.asyncio
async def test_health_service_readiness_with_db(prepared_db: None) -> None:
    settings = Settings(
        environment="testing",
        database_url="sqlite+aiosqlite:///:memory:",
        database_auto_create_schema=True,
    )
    # prepared_db already inited; re-bind is fine for service check using global engine
    service = HealthService(settings)
    result = await service.readiness()
    assert result.status == "ready"
    db_check = next(c for c in result.checks if c.name == "database")
    assert db_check.status in {"up", "degraded"}
