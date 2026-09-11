"""BE-9 endpoints (design S9; BO T-4). 4 POST writers + 8 GET reads = 12.

Zero PUT/PATCH/DELETE (C3 law). BE-1 envelope everywhere; every read
carries provenance + staleness; degraded reads serve last-good with an
explicit staleness banner (Q7). No route reaches a mutation verb; no
route proxies to the provider from the frontend (N2).
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.operator import Operator
from app.db.models.v2_broker_read import (
    V2BrokerAccount,
    V2BrokerBalance,
    V2BrokerDiscrepancy,
    V2BrokerFill,
    V2BrokerInstrumentPermission,
    V2BrokerOrder,
    V2BrokerPosition,
    V2BrokerReconcileRun,
    V2BrokerSyncRun,
)
from app.db.session import get_db_session
from app.v2.broker_read.health import health_facts
from app.v2.broker_read.reconcile import (
    run_reconciliation,
    transition_discrepancy,
)
from app.v2.broker_read.sync import run_sync
from app.v2.identifiers import new_id
from app.v2.rbac.dependencies import require_v2_permission

router = APIRouter(prefix="/broker", tags=["V2 Broker Read"])

RequireAccountsRead = Annotated[
    Operator, Depends(require_v2_permission("v2.broker.accounts.read"))]
RequireBalancesRead = Annotated[
    Operator, Depends(require_v2_permission("v2.broker.balances.read"))]
RequirePositionsRead = Annotated[
    Operator, Depends(require_v2_permission("v2.broker.positions.read"))]
RequireOrdersFillsRead = Annotated[
    Operator, Depends(require_v2_permission("v2.broker.orders_fills.read"))]
RequireSyncRun = Annotated[
    Operator, Depends(require_v2_permission("v2.broker.sync.run"))]
RequireDiscrepancyManage = Annotated[
    Operator, Depends(require_v2_permission("v2.broker.discrepancy.manage"))]
RequireVaultManage = Annotated[
    Operator, Depends(require_v2_permission("v2.broker.vault.manage"))]

_TEST_PROVIDER = {"instance": None}  # suite injection point (fixture provider)


def _envelope(request: Request) -> dict:
    return {"mode": request.app.state.v2_mode,
            "correlation_id": getattr(request.state, "correlation_id", None),
            "timestamp": datetime.now(timezone.utc)}


def _cid(request: Request) -> str:
    return getattr(request.state, "correlation_id", None) or new_id()


async def _staleness(session: AsyncSession) -> dict:
    last_complete = (await session.execute(
        select(V2BrokerSyncRun)
        .where(V2BrokerSyncRun.outcome == "complete")
        .order_by(V2BrokerSyncRun.created_at.desc()))).scalars().first()
    if last_complete is None:
        return {"staleness": "no_data",
                "banner": "no complete sync has ever landed"}
    created = last_complete.created_at
    if created.tzinfo is None:
        created = created.replace(tzinfo=timezone.utc)
    hours = (datetime.now(timezone.utc) - created).total_seconds() / 3600
    return {"staleness": "stale" if hours > 24 else "fresh",
            "last_complete_sync": last_complete.id,
            "age_hours": round(hours, 3),
            "banner": ("last-good snapshot; provider not re-contacted"
                       " since the shown basis" if hours > 24 else None)}


# --- writers (POST only; T-4) ----------------------------------------------------


class SyncRequest(BaseModel):
    provider_id: str = "exness_mt5_demo"


class ReconcileRequest(BaseModel):
    sync_run_id: str


class DiscrepancyTransition(BaseModel):
    discrepancy_id: str
    to_state: str = Field(pattern="^(triaged|owned|resolved|"
                                  "dismissed_with_reason)$")
    reason: str | None = None


class VaultAct(BaseModel):
    action: str = Field(pattern="^(unlock|lock|rotate)$")


@router.post("/sync")
async def api_sync(
    body: SyncRequest, request: Request, operator: RequireSyncRun,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    provider = _TEST_PROVIDER["instance"]
    if provider is None:
        # The real leg (E1 act only; on the DA/test station this refuses
        # typed broker.terminal.unavailable via the deferred import).
        from app.v2.broker_read.providers.exness_mt5 import (
            ExnessMt5ReadProvider,
        )
        provider = ExnessMt5ReadProvider()
    result = await run_sync(
        session, provider=provider,
        provenance_expect={"provider_id": body.provider_id},
        actor_id=operator.username, mode=request.app.state.v2_mode,
        correlation_id=_cid(request))
    if result["outcome"] == "complete":
        await session.commit()
    result.pop("pages", None)  # never echo payloads on the wire
    return {**result, **_envelope(request)}


@router.post("/reconcile")
async def api_reconcile(
    body: ReconcileRequest, request: Request,
    operator: RequireSyncRun,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    provider = _TEST_PROVIDER["instance"]
    if provider is None:
        from app.v2.broker_read.providers.exness_mt5 import (
            ExnessMt5ReadProvider,
        )
        provider = ExnessMt5ReadProvider()
    # fresh broker fetch (authority side) via a pure-read sync-shaped pass
    from app.v2.broker_read.contract import ORIGIN_FLOOR_ISO, BrokerRefused
    try:
        accounts = await provider.read_accounts()
        summary = await provider.read_account_summary()
        positions = await provider.read_positions()
        orders = await provider.read_orders()
        instruments = await provider.read_instrument_permissions()
        from app.v2.broker_read.providers.exness_mt5 import history_windows
        fills: list = []
        now_iso = datetime.now(timezone.utc).isoformat()
        for i, (w_start, w_end) in enumerate(
                history_windows(ORIGIN_FLOOR_ISO, now_iso)):
            page = await provider.read_transactions(w_start, w_end, i)
            fills.extend(page.records)
        broker_payload = {
            "accounts": [dict(r) for r in accounts.records],
            "balances": [dict(r) for r in summary.records],
            "positions": [dict(r) for r in positions.records],
            "orders": [dict(r) for r in orders.records],
            "fills": [dict(r) for r in fills],
            "instrument_permissions": [dict(r) for r in
                                       instruments.records],
        }
    except BrokerRefused as exc:
        return {"outcome": "refused", "refusal_class": exc.refusal_class,
                "reasons": exc.reasons, **_envelope(request)}
    result = await run_reconciliation(
        session, broker_payload=broker_payload,
        sync_run_id=body.sync_run_id,
        provider_id="exness_mt5_demo", actor_id=operator.username,
        mode=request.app.state.v2_mode, correlation_id=_cid(request))
    await session.commit()
    return {**result, **_envelope(request)}


@router.post("/discrepancies/transition")
async def api_discrepancy_transition(
    body: DiscrepancyTransition, request: Request,
    operator: RequireDiscrepancyManage,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    result = await transition_discrepancy(
        session, discrepancy_id=body.discrepancy_id,
        to_state=body.to_state, actor_id=operator.username,
        reason=body.reason, mode=request.app.state.v2_mode,
        correlation_id=_cid(request))
    if result["outcome"] == "applied":
        await session.commit()
    return {**result, **_envelope(request)}


@router.post("/vault")
async def api_vault_act(
    body: VaultAct, request: Request, operator: RequireVaultManage,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    """Vault acts are console-interactive (no-echo passphrase prompts);
    over the API they are records-of-intent only: the act itself runs on
    the operator console. Every act audited; no material ever crosses."""
    from app.v2.broker_read.sync import _audit
    await _audit(session, f"broker.vault.{body.action}_requested",
                 details={"note": "console-interactive act; no material"
                          " crosses the API"},
                 mode=request.app.state.v2_mode,
                 operator_id=operator.username,
                 correlation_id=_cid(request))
    await session.commit()
    return {"outcome": "recorded", "action": body.action,
            **_envelope(request)}


# --- reads (GET; 8) ----------------------------------------------------------------


@router.get("/accounts")
async def api_accounts(
    request: Request, operator: RequireAccountsRead,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    limit: int = Query(default=100, ge=1, le=500),
):
    rows = list((await session.execute(
        select(V2BrokerAccount)
        .order_by(V2BrokerAccount.created_at.desc())
        .limit(limit))).scalars().all())
    return {"accounts": [
        {"id": r.id, "broker_account_ext_id": r.broker_account_ext_id,
         "record_seq": r.record_seq, "alias": r.alias,
         "currency": r.currency, "environment": r.environment,
         "read_only_login": r.read_only_login,
         "provider_id": r.provider_id} for r in rows],
        **await _staleness(session), **_envelope(request)}


@router.get("/balances")
async def api_balances(
    request: Request, operator: RequireBalancesRead,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    limit: int = Query(default=100, ge=1, le=500),
):
    rows = list((await session.execute(
        select(V2BrokerBalance)
        .order_by(V2BrokerBalance.created_at.desc())
        .limit(limit))).scalars().all())
    return {"balances": [
        {"id": r.id, "broker_account_ext_id": r.broker_account_ext_id,
         "balance": r.balance, "margin_used": r.margin_used,
         "margin_available": r.margin_available,
         "unrealized_pl": r.unrealized_pl, "currency": r.currency,
         "sync_run_id": r.sync_run_id} for r in rows],
        **await _staleness(session), **_envelope(request)}


@router.get("/positions")
async def api_positions(
    request: Request, operator: RequirePositionsRead,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    limit: int = Query(default=100, ge=1, le=500),
):
    rows = list((await session.execute(
        select(V2BrokerPosition)
        .order_by(V2BrokerPosition.created_at.desc())
        .limit(limit))).scalars().all())
    return {"positions": [
        {"id": r.id, "broker_account_ext_id": r.broker_account_ext_id,
         "instrument_ext_id": r.instrument_ext_id,
         "units_long": r.units_long, "units_short": r.units_short,
         "sync_run_id": r.sync_run_id} for r in rows],
        **await _staleness(session), **_envelope(request)}


@router.get("/orders")
async def api_orders(
    request: Request, operator: RequireOrdersFillsRead,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    limit: int = Query(default=100, ge=1, le=500),
):
    rows = list((await session.execute(
        select(V2BrokerOrder)
        .order_by(V2BrokerOrder.created_at.desc())
        .limit(limit))).scalars().all())
    return {"orders": [
        {"id": r.id, "order_ext_id": r.order_ext_id,
         "order_state_ext": r.order_state_ext, "payload": r.payload,
         "sync_run_id": r.sync_run_id} for r in rows],
        **await _staleness(session), **_envelope(request)}


@router.get("/fills")
async def api_fills(
    request: Request, operator: RequireOrdersFillsRead,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    limit: int = Query(default=100, ge=1, le=500),
):
    rows = list((await session.execute(
        select(V2BrokerFill)
        .order_by(V2BrokerFill.created_at.desc())
        .limit(limit))).scalars().all())
    return {"fills": [
        {"id": r.id, "transaction_ext_id": r.transaction_ext_id,
         "tx_type_ext": r.tx_type_ext,
         "instrument_ext_id": r.instrument_ext_id, "units": r.units,
         "price": r.price, "tx_time_ext": r.tx_time_ext} for r in rows],
        **await _staleness(session), **_envelope(request)}


@router.get("/instrument-permissions")
async def api_instrument_permissions(
    request: Request, operator: RequireAccountsRead,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    limit: int = Query(default=100, ge=1, le=500),
):
    rows = list((await session.execute(
        select(V2BrokerInstrumentPermission)
        .order_by(V2BrokerInstrumentPermission.created_at.desc())
        .limit(limit))).scalars().all())
    return {"instrument_permissions": [
        {"id": r.id, "instrument_ext_id": r.instrument_ext_id,
         "visibility": r.visibility, "display_name": r.display_name,
         "execution_capability": "none - read-model only (BE-9)"}
        for r in rows],
        **await _staleness(session), **_envelope(request)}


@router.get("/discrepancies")
async def api_discrepancies(
    request: Request, operator: RequireAccountsRead,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    limit: int = Query(default=100, ge=1, le=500),
):
    rows = list((await session.execute(
        select(V2BrokerDiscrepancy)
        .order_by(V2BrokerDiscrepancy.created_at.desc())
        .limit(limit))).scalars().all())
    recon = list((await session.execute(
        select(V2BrokerReconcileRun)
        .order_by(V2BrokerReconcileRun.created_at.desc())
        .limit(10))).scalars().all())
    return {"discrepancies": [
        {"id": r.id, "discrepancy_id": r.discrepancy_id,
         "record_seq": r.record_seq, "class": r.discrepancy_class,
         "state": r.state, "owned_by": r.owned_by,
         "dismiss_reason": r.dismiss_reason} for r in rows],
        "reconcile_runs": [
        {"id": r.id, "outcome": r.outcome,
         "discrepancy_count": r.discrepancy_count,
         "broker_side_digest": r.broker_side_digest,
         "projection_side_digest": r.projection_side_digest}
        for r in recon],
        **_envelope(request)}


@router.get("/health")
async def api_health(
    request: Request, operator: RequireAccountsRead,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    return {**await health_facts(session), **_envelope(request)}
