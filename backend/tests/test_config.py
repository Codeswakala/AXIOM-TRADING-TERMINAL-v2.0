"""Configuration unit tests."""

from __future__ import annotations

import os

from app.core.config import Settings, clear_settings_cache, get_settings


def test_settings_defaults_when_env_cleared(monkeypatch: object) -> None:
    """Defaults apply only when AXIOM_* env vars are absent.

    ITRR-W0-U03-001: must not hard-assert sqlite when an override is present.
    """
    clear_settings_cache()
    for key in list(os.environ):
        if key.startswith("AXIOM_"):
            monkeypatch.delenv(key, raising=False)  # type: ignore[attr-defined]
    settings = Settings(_env_file=None)
    assert settings.app_name == "AXIOM"
    assert settings.api_prefix == "/api/v1"
    assert settings.database_url.startswith("sqlite")
    assert settings.is_sqlite is True


def test_settings_respects_database_url_override() -> None:
    """When DATABASE_URL override is supplied, backend detection follows it."""
    settings = Settings(
        database_url="postgresql+asyncpg://user:pass@localhost:5432/axiom",
    )
    assert settings.is_postgres is True
    assert settings.database_backend_name == "postgresql"
    assert not settings.database_url.startswith("sqlite")


def test_get_settings_cached() -> None:
    clear_settings_cache()
    a = get_settings()
    b = get_settings()
    assert a is b
    clear_settings_cache()


def test_cors_origin_list_parsing() -> None:
    settings = Settings(cors_origins="http://a.com, http://b.com")
    assert settings.cors_origin_list == ["http://a.com", "http://b.com"]


def test_postgres_backend_detection() -> None:
    settings = Settings(
        database_url="postgresql+asyncpg://user:pass@localhost:5432/axiom",
    )
    assert settings.is_postgres is True
    assert settings.database_backend_name == "postgresql"
