"""V2 BE-2 market-data router aggregate — mounted into the V2 API router."""

from __future__ import annotations

from fastapi import APIRouter

from app.v2.marketdata.api.contract_test import router as contract_test_router
from app.v2.marketdata.api.providers import router as providers_router
from app.v2.marketdata.api.reads import router as reads_router
from app.v2.marketdata.api.writers import router as writers_router

router = APIRouter()
router.include_router(reads_router)
router.include_router(writers_router)
router.include_router(providers_router)
router.include_router(contract_test_router)
