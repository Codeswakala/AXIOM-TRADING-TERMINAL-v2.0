"""BE-10 endpoints (BO B-1.4; laws L1/L8/L9). TWO GETs, zero writers.

Both routes gated on `v2.account_context.read` (L9). BE-1 envelope;
banner carried end-to-end (L8); refusals typed (L4).
"""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.operator import Operator
from app.db.session import get_db_session
from app.v2.account_context.contract import AccountContextRefused
from app.v2.account_context.engine import compute_alignment
from app.v2.rbac.dependencies import require_v2_permission

router = APIRouter(prefix="/account-context", tags=["V2 Account Context"])

RequireContextRead = Annotated[
    Operator, Depends(require_v2_permission("v2.account_context.read"))]


def _envelope(request: Request) -> dict:
    return {"mode": request.app.state.v2_mode,
            "correlation_id": getattr(request.state, "correlation_id", None),
            "timestamp": datetime.now(timezone.utc)}


@router.get("/alignment")
async def api_alignment(
    request: Request, operator: RequireContextRead,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    try:
        matrix = await compute_alignment(session)
    except AccountContextRefused as exc:
        return {"outcome": "refused", "refusal_class": exc.refusal_class,
                "reasons": exc.reasons, **_envelope(request)}
    return {"outcome": "computed",
            "rows": [asdict(r) for r in matrix.rows],
            "basis_sync_run_id": matrix.basis_sync_run_id,
            "basis_age_hours": matrix.basis_age_hours,
            "staleness": matrix.staleness, "banner": matrix.banner,
            "digest": matrix.digest,
            "engine_version": matrix.engine_version,
            "unmapped_count": matrix.unmapped_count,
            **_envelope(request)}


@router.get("/summary")
async def api_summary(
    request: Request, operator: RequireContextRead,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    try:
        matrix = await compute_alignment(session)
    except AccountContextRefused as exc:
        return {"outcome": "refused", "refusal_class": exc.refusal_class,
                "reasons": exc.reasons, **_envelope(request)}
    counts: dict[str, int] = {}
    for r in matrix.rows:
        counts[r.verdict] = counts.get(r.verdict, 0) + 1
    return {"outcome": "computed", "verdict_counts": counts,
            "total_rows": len(matrix.rows),
            "unmapped_count": matrix.unmapped_count,
            "basis_sync_run_id": matrix.basis_sync_run_id,
            "basis_age_hours": matrix.basis_age_hours,
            "staleness": matrix.staleness, "banner": matrix.banner,
            "digest": matrix.digest, **_envelope(request)}
