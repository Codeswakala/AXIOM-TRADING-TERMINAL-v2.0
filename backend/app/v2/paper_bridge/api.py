"""BE-11 endpoints (BO D-1; D-B11-MODE; marker convention D-1).

POST /paper-bridge/intents · POST /paper-bridge/evaluate ·
GET /paper-bridge/ledger · GET /paper-bridge/drift.
Writers demand mode == "PAPER" (4xx on LIVE or any other mode).
Idempotency: the standing BE-8 uq(account_id, idempotency_key) anchor —
a duplicate collision surfaces as the typed refusal `duplicate_intent`.
"""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.operator import Operator
from app.db.models.v2_paper_bridge import V2PaperBridgeDriftRun
from app.db.models.v2_paper_trading import V2PaperOrderIntent
from app.db.session import get_db_session
from app.v2.identifiers import new_id
from app.v2.paper_bridge.contract import BridgeRefused
from app.v2.paper_bridge.engine import (
    evaluate_intent,
    pin_basis,
    read_staleness_seed,
    read_tolerance_seeds,
    require_citation,
)
from app.v2.rbac.dependencies import require_v2_permission

router = APIRouter(prefix="/paper-bridge", tags=["V2 Paper Bridge"])

RequireIntentWrite = Annotated[
    Operator, Depends(require_v2_permission("v2.paper_bridge.intent.write"))]
RequireEvaluateWrite = Annotated[
    Operator, Depends(require_v2_permission("v2.paper_bridge.evaluate.write"))]
RequireLedgerRead = Annotated[
    Operator, Depends(require_v2_permission("v2.paper_bridge.ledger.read"))]
RequireDriftRead = Annotated[
    Operator, Depends(require_v2_permission("v2.paper_bridge.drift.read"))]

_DATA_CLASS = "simulated"


def _envelope(request: Request) -> dict:
    return {"mode": request.app.state.v2_mode,
            "correlation_id": getattr(request.state, "correlation_id", None),
            "timestamp": datetime.now(timezone.utc)}


def _require_paper(request: Request) -> str:
    """D-B11-MODE: the bridge knows no other writer mode."""
    mode = request.app.state.v2_mode
    if mode != "PAPER":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Paper-bridge writer not permitted in this mode")
    return mode


def _cid(request: Request) -> str:
    return getattr(request.state, "correlation_id", None) or new_id()


def _refusal(request: Request, exc: BridgeRefused) -> dict:
    return {"outcome": "refused", "reason": exc.reason,
            "details": exc.details, **_envelope(request)}


class IntentBody(BaseModel):
    account_id: str
    instrument_id: str
    side: str = Field(pattern="^(buy|sell)$")
    quantity: str
    idempotency_key: str = Field(min_length=1, max_length=64)
    reference_price: dict | None = None  # D-B11-CITE citation shape


class EvaluateBody(BaseModel):
    intent_row_id: str
    reference_price: dict | None = None


class DriftBody(BaseModel):
    paper_side: dict = Field(default_factory=dict)
    broker_side: dict = Field(default_factory=dict)


@router.post("/intents")
async def api_post_intent(
    body: IntentBody, request: Request, operator: RequireIntentWrite,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    mode = _require_paper(request)
    cid = _cid(request)
    try:
        basis = await pin_basis(session)          # consistency ARM: once
        citation = require_citation(body.reference_price)
        max_age = await read_staleness_seed(session)
        record = evaluate_intent(
            basis, {"account_id": body.account_id,
                    "instrument_id": body.instrument_id,
                    "side": body.side, "quantity": body.quantity,
                    "idempotency_key": body.idempotency_key},
            citation, max_age)
    except BridgeRefused as exc:
        return _refusal(request, exc)

    # idempotency (R-3.5): the standing BE-8 anchor law
    existing = (await session.execute(
        select(V2PaperOrderIntent).where(
            V2PaperOrderIntent.account_id == body.account_id,
            V2PaperOrderIntent.idempotency_key == body.idempotency_key)
    )).scalar_one_or_none()
    if existing is not None:
        return _refusal(request, BridgeRefused("duplicate_intent", [
            {"failing": "idempotency_key", "existing_id": existing.id}]))

    intent = V2PaperOrderIntent(
        intent_id=new_id(), account_id=body.account_id,
        instrument_id=body.instrument_id, side=body.side,
        order_type="market", quantity=body.quantity, limit_price=None,
        time_in_force="replay_window",
        idempotency_key=body.idempotency_key,
        snapshot_ref=f"bridge-basis:{basis.sync_run_id}",
        time_basis={"basis_sync_run_id": basis.sync_run_id,
                    "basis_age_hours": basis.basis_age_hours,
                    "citation": asdict(citation)},
        confirmation_ref=None, actor_id=operator.username,
        data_class=_DATA_CLASS, mode=mode, operator_id=operator.username,
        correlation_id=cid)
    session.add(intent)
    await session.flush()
    await session.commit()
    return {"outcome": "recorded", "intent_row_id": intent.id,
            "gateway": {"decision": record.decision,
                        "reasons": list(record.reasons),
                        "notes": list(record.notes)},
            "digest": record.digest,
            "basis_sync_run_id": record.basis_sync_run_id,
            "basis_staleness": basis.staleness,
            "engine_versions": record.engine_versions,
            **_envelope(request)}


@router.post("/evaluate")
async def api_post_evaluate(
    body: EvaluateBody, request: Request, operator: RequireEvaluateWrite,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    """Re-evaluation of an existing intent against the CURRENT basis —
    a fresh state record; the stored intent is untouched (BE-8 C1)."""
    _require_paper(request)
    intent = (await session.execute(
        select(V2PaperOrderIntent).where(
            V2PaperOrderIntent.id == body.intent_row_id)
    )).scalar_one_or_none()
    if intent is None:
        raise HTTPException(status_code=404, detail="Unknown intent")
    try:
        basis = await pin_basis(session)
        raw_citation = (body.reference_price
                        or intent.time_basis.get("citation"))
        citation = require_citation(raw_citation)
        max_age = await read_staleness_seed(session)
        record = evaluate_intent(
            basis, {"account_id": intent.account_id,
                    "instrument_id": intent.instrument_id,
                    "side": intent.side, "quantity": intent.quantity,
                    "idempotency_key": intent.idempotency_key},
            citation, max_age)
    except BridgeRefused as exc:
        return _refusal(request, exc)
    return {"outcome": "computed",
            "gateway": {"decision": record.decision,
                        "reasons": list(record.reasons),
                        "notes": list(record.notes)},
            "digest": record.digest,
            "basis_sync_run_id": record.basis_sync_run_id,
            "engine_versions": record.engine_versions,
            **_envelope(request)}


@router.get("/ledger")
async def api_get_ledger(
    request: Request, operator: RequireLedgerRead,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    limit: int = Query(default=100, ge=1, le=500),
):
    rows = list((await session.execute(
        select(V2PaperOrderIntent)
        .where(V2PaperOrderIntent.snapshot_ref.like("bridge-basis:%"))
        .order_by(V2PaperOrderIntent.created_at.desc())
        .limit(limit))).scalars().all())
    return {"ledger": [
        {"id": r.id, "account_id": r.account_id,
         "instrument_id": r.instrument_id, "side": r.side,
         "quantity": r.quantity, "snapshot_ref": r.snapshot_ref,
         "time_basis": r.time_basis} for r in rows],
        **_envelope(request)}


@router.get("/drift")
async def api_get_drift(
    request: Request, operator: RequireDriftRead,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    limit: int = Query(default=100, ge=1, le=500),
):
    """Drift lineage reads + the seeded-state census (never guesses)."""
    seeds = await read_tolerance_seeds(session)
    max_age = await read_staleness_seed(session)
    runs = list((await session.execute(
        select(V2PaperBridgeDriftRun)
        .where(V2PaperBridgeDriftRun.run_kind == "drift_run")
        .order_by(V2PaperBridgeDriftRun.created_at.desc())
        .limit(limit))).scalars().all())
    return {"drift_runs": [
        {"id": r.id, "basis_sync_run_id": r.basis_sync_run_id,
         "verdict": r.verdict, "digest": r.digest,
         "tolerances_in_force": r.tolerances_in_force} for r in runs],
        "tolerance_seeds_present": len(seeds),
        "staleness_seed_present": max_age is not None,
        "comparison_state": ("armed" if seeds and max_age is not None
                             else "refuse_to_compare_unseeded"),
        **_envelope(request)}
