"""Dependency injection providers for FastAPI routes and services."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from app.core.config import Settings, get_settings
from app.external_integration.broker.service import BrokerIntegrationService
from app.services.health_service import HealthService
from app.services.system_service import SystemService


def provide_settings() -> Settings:
    return get_settings()


def provide_health_service(
    settings: Annotated[Settings, Depends(provide_settings)],
) -> HealthService:
    return HealthService(settings=settings)


def provide_system_service(
    settings: Annotated[Settings, Depends(provide_settings)],
) -> SystemService:
    return SystemService(settings=settings)


def provide_broker_integration_service() -> BrokerIntegrationService:
    return BrokerIntegrationService()


SettingsDep = Annotated[Settings, Depends(provide_settings)]
HealthServiceDep = Annotated[HealthService, Depends(provide_health_service)]
SystemServiceDep = Annotated[SystemService, Depends(provide_system_service)]
BrokerIntegrationServiceDep = Annotated[
    BrokerIntegrationService,
    Depends(provide_broker_integration_service),
]
