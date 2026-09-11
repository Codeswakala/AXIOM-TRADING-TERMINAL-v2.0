"""System identity service for operator-facing platform metadata."""

from __future__ import annotations

from datetime import datetime, timezone

from app.core.config import Settings
from app.models.system import SystemInfoResponse


class SystemService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def get_info(self) -> SystemInfoResponse:
        return SystemInfoResponse(
            name=self._settings.app_name,
            version=self._settings.version,
            environment=self._settings.environment,
            timestamp=datetime.now(timezone.utc),
        )
