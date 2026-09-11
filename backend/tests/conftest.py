"""Shared pytest fixtures with isolated async SQLite database (W0-U08 hardened env)."""

from __future__ import annotations

import os
from collections.abc import AsyncIterator, Iterator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

# Deterministic test environment BEFORE settings / app import.
os.environ["AXIOM_ENVIRONMENT"] = "testing"
os.environ["AXIOM_DEBUG"] = "false"
os.environ["AXIOM_LOG_LEVEL"] = "WARNING"
os.environ["AXIOM_LOG_JSON"] = "false"
os.environ["AXIOM_DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["AXIOM_DATABASE_AUTO_CREATE_SCHEMA"] = "true"
os.environ["AXIOM_DATABASE_ECHO"] = "false"
os.environ["AXIOM_LIVE_MARKET_AUTO_START"] = "false"
os.environ["AXIOM_LIVE_MARKET_INTERVAL_SECONDS"] = "0.1"
os.environ["AXIOM_LIVE_MARKET_SYMBOLS"] = "EURUSD,BTCUSD"
# Security allow for tests (explicit)
os.environ["AXIOM_ALLOW_INSECURE_DEV"] = "true"
os.environ["AXIOM_JWT_SECRET_KEY"] = "test-secret-key-at-least-32-chars-long!!"
os.environ["AXIOM_BOOTSTRAP_ADMIN_ENABLED"] = "true"
os.environ["AXIOM_BOOTSTRAP_ADMIN_USERNAME"] = "admin"
os.environ["AXIOM_BOOTSTRAP_ADMIN_PASSWORD"] = "admin123"
os.environ["AXIOM_WS_ALLOW_QUERY_JWT"] = "false"

from app.core.config import clear_settings_cache  # noqa: E402
from app.db.session import close_db, create_schema, init_db  # noqa: E402
from app.main import create_app  # noqa: E402
from app.market.live_service import reset_live_market_service  # noqa: E402


@pytest.fixture(autouse=True)
def _reset_settings() -> Iterator[None]:
    clear_settings_cache()
    reset_live_market_service()
    yield
    try:
        import asyncio

        from app.market.live_service import get_live_market_service

        svc = get_live_market_service()
        if svc.is_running:
            asyncio.get_event_loop().run_until_complete(svc.stop())
    except Exception:  # noqa: BLE001
        pass
    reset_live_market_service()
    clear_settings_cache()


@pytest_asyncio.fixture
async def prepared_db() -> AsyncIterator[None]:
    clear_settings_cache()
    await close_db()
    init_db()
    await create_schema()
    try:
        yield
    finally:
        await close_db()
        clear_settings_cache()


@pytest.fixture
def client() -> Iterator[TestClient]:
    clear_settings_cache()
    application = create_app()
    with TestClient(application) as test_client:
        yield test_client


@pytest.fixture
def auth_headers(client: TestClient) -> dict[str, str]:
    login = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert login.status_code == 200, login.text
    token = login.json()["tokens"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def async_client() -> AsyncIterator[AsyncClient]:
    clear_settings_cache()
    application = create_app()
    transport = ASGITransport(app=application)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        async with application.router.lifespan_context(application):
            yield ac
