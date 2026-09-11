"""V2 API Router — aggregate router for all V2 endpoints."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Request

from app.v2.account_context.api import router as account_context_router
from app.v2.api.audit import router as audit_router
from app.v2.api.capability import router as capability_router
from app.v2.api.lineage import router as lineage_router
from app.v2.api.mode import router as mode_router
from app.v2.broker_read.api import router as broker_read_router
from app.v2.errors.contract import V2ErrorCode
from app.v2.marketdata.api.router import router as marketdata_router
from app.v2.models.errors import V2ErrorTaxonomyResponse
from app.v2.live_exec.api import router as live_exec_router
from app.v2.paper_bridge.api import router as paper_bridge_router
from app.v2.paper_trading.api import router as paper_trading_router
from app.v2.portfolio_research.api import router as portfolio_research_router
from app.v2.rbac.dependencies import RequireV2ErrorRead
from app.v2.research.api import router as research_router
from app.v2.research_governance.api import router as research_governance_router
from app.v2.research_jobs.api import router as research_jobs_router

router = APIRouter(prefix="/v2", tags=["V2"])

# Include sub-routers
router.include_router(mode_router)
router.include_router(capability_router)
router.include_router(audit_router)
router.include_router(lineage_router)
router.include_router(marketdata_router)
router.include_router(research_router)  # BE-4 (BO-V2-BE-4-001 D-4)
router.include_router(research_governance_router)  # BE-5 (BO-V2-BE-5-001)
router.include_router(portfolio_research_router)  # BE-6 (BO-V2-BE-6-001)
router.include_router(research_jobs_router)  # BE-7 (BO-V2-BE-7-001)
router.include_router(paper_trading_router)  # BE-8 (BO-V2-BE-8-001 D-3)
router.include_router(broker_read_router)  # BE-9 (BO-V2-BE-9-001 D-3)
router.include_router(account_context_router)  # BE-10 (BO-V2-BE-10-001)
router.include_router(paper_bridge_router)  # BE-11 (BO-V2-BE-11-001)
router.include_router(live_exec_router)  # BE-12A (BO-V2-BE12A-001)


@router.get("/errors", response_model=V2ErrorTaxonomyResponse)
async def get_error_taxonomy(
    request: Request,
    operator: RequireV2ErrorRead,
) -> V2ErrorTaxonomyResponse:
    """Get V2 error taxonomy reference. Read-only."""
    error_codes = [
        {"code": code.value, "category": code.name.split("_")[0].lower()}
        for code in V2ErrorCode
    ]
    domain_statuses = ["available", "unavailable", "stale", "degraded", "unknown", "denied"]

    return V2ErrorTaxonomyResponse(
        error_codes=error_codes,
        domain_statuses=domain_statuses,
        mode=request.app.state.v2_mode,
        correlation_id=getattr(request.state, "correlation_id", None),
        timestamp=datetime.now(timezone.utc),
    )
