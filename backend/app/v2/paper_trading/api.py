"""BE-8 endpoints (BO D-1/D-3; design S9; C3 law: POST-only writers).

Governed writers: accounts, accounts/confirm, orders, orders/confirm,
orders/cancel, orders/{id}/run. Reads: accounts, orders, orders/{id}/events,
fills, positions, balances, risk-decisions, reconciliations.
PAPER-mode writers (D-2 law; typed refusal otherwise). BE-1 envelope on
every response; unconditional paper-simulated disclaimer (N4).
"""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.operator import Operator
from app.db.models.v2_paper_trading import (
    V2PaperBalanceSnapshot,
    V2PaperFill,
    V2PaperOrderEvent,
    V2PaperOrderIntent,
    V2PaperPositionSnapshot,
    V2PaperReconciliation,
    V2PaperRiskDecision,
)
from app.db.session import get_db_session
from app.v2.identifiers import new_id
from app.v2.paper_trading.accounts import (
    confirm_account_action,
    current_account,
    request_account_action,
)
from app.v2.paper_trading.contracts import (
    INTENT_SIDES,
    INTENT_TYPES,
    PAPER_DISCLAIMER,
    PaperOrderIntent,
    PaperRefused,
)
from app.v2.paper_trading.ledger import derivation_hash, derive_balance
from app.v2.paper_trading.orders import (
    append_event,
    audit,
    cancel_order,
    confirm_hold,
    current_state,
    get_intent,
    may_execute,
)
from app.v2.paper_trading.reconciliation import (
    collect_account_fills,
    run_reconciliation,
)
from app.v2.paper_trading.risk import config_version, evaluate_intent
from app.v2.paper_trading.simulator import (
    ENGINE_VERSIONS,
    SIMULATOR_VERSION,
    engine_versions_hash,
    run_simulation,
    snapshot_content_hash,
)
from app.v2.rbac.dependencies import require_v2_permission

router = APIRouter(prefix="/paper", tags=["V2 Paper Trading"])

RequireAccountsRead = Annotated[
    Operator, Depends(require_v2_permission("v2.paper.accounts.read"))]
RequireAccountsManage = Annotated[
    Operator, Depends(require_v2_permission("v2.paper.accounts.manage"))]
RequireOrdersRead = Annotated[
    Operator, Depends(require_v2_permission("v2.paper.orders.read"))]
RequireOrdersPlace = Annotated[
    Operator, Depends(require_v2_permission("v2.paper.orders.place"))]
RequireOrdersCancel = Annotated[
    Operator, Depends(require_v2_permission("v2.paper.orders.cancel"))]
RequireOrdersConfirm = Annotated[
    Operator, Depends(require_v2_permission("v2.paper.orders.confirm"))]
RequireFillsRead = Annotated[
    Operator, Depends(require_v2_permission("v2.paper.fills.read"))]
RequireRiskRead = Annotated[
    Operator, Depends(require_v2_permission("v2.paper.risk.read"))]

_DATA_CLASS = "simulated"


def _envelope(request: Request) -> dict:
    return {"mode": request.app.state.v2_mode,
            "correlation_id": getattr(request.state, "correlation_id", None),
            "timestamp": datetime.now(timezone.utc),
            "disclaimer": PAPER_DISCLAIMER}


def _require_paper(request: Request) -> str:
    """D-2 law: paper writers demand mode == PAPER, typed refusal else."""
    mode = request.app.state.v2_mode
    if mode != "PAPER":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Paper writer not permitted in this mode")
    return mode


def _cid(request: Request) -> str:
    return getattr(request.state, "correlation_id", None) or new_id()


# --- request models -----------------------------------------------------------


class AccountRequest(BaseModel):
    action: str = Field(pattern="^(create|freeze|close)$")
    account_id: str = Field(min_length=1, max_length=64)
    name: str = ""
    base_currency: str = "USD"
    initial_balance: str = "0"
    margin_params: dict = Field(default_factory=dict)


class AccountConfirm(AccountRequest):
    confirmation_ref: str


class OrderRequest(BaseModel):
    account_id: str
    instrument_id: str
    side: str
    order_type: str = "market"
    quantity: str
    limit_price: str | None = None
    idempotency_key: str = Field(min_length=1, max_length=64)
    snapshot_ref: str = Field(min_length=1, max_length=64)
    bars: list[dict] = Field(default_factory=list)
    window_start: str = ""
    window_end: str = ""


class OrderConfirm(BaseModel):
    order_id: str
    confirmation_ref: str
    resolve_to: str = Field(pattern="^(confirm|cancel)$")


class OrderCancel(BaseModel):
    order_id: str


class OrderRun(BaseModel):
    bars: list[dict] = Field(default_factory=list)
    cost_model: dict | None = None


# --- writers (POST only; C3) ----------------------------------------------------


@router.post("/accounts")
async def api_account_request(
    body: AccountRequest, request: Request, operator: RequireAccountsManage,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    mode = _require_paper(request)
    result = await request_account_action(
        session, action=body.action,
        payload=body.model_dump(exclude={"action"}),
        mode=mode, operator_id=operator.username,
        correlation_id=_cid(request))
    if not result.refused:
        await session.commit()
    return {"outcome": result.outcome, "reasons": result.reasons,
            "confirmation_ref": result.confirmation_ref,
            **_envelope(request)}


@router.post("/accounts/confirm")
async def api_account_confirm(
    body: AccountConfirm, request: Request, operator: RequireAccountsManage,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    mode = _require_paper(request)
    result = await confirm_account_action(
        session, action=body.action,
        payload=body.model_dump(exclude={"action", "confirmation_ref"}),
        confirmation_ref=body.confirmation_ref,
        actor_id=operator.username, mode=mode,
        operator_id=operator.username, correlation_id=_cid(request),
        data_class=_DATA_CLASS)
    if not result.refused:
        await session.commit()
    return {"outcome": result.outcome, "reasons": result.reasons,
            "record_id": result.record_id, **_envelope(request)}


@router.post("/orders")
async def api_place_order(
    body: OrderRequest, request: Request, operator: RequireOrdersPlace,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    """Intent + validation + risk decision in one governed act (S2 draft ->
    validated -> risk_*). N3: every field of the law on the row."""
    mode = _require_paper(request)
    cid = _cid(request)

    reasons: list = []
    account = await current_account(session, body.account_id)
    account_row_id = account.id if account is not None else None
    if account is None:
        reasons.append({"failing": "account_id", "note": "unknown account"})

    # Idempotency (S8): same (account, key) returns the existing intent.
    # Rows pin the account ROW id — dedupe on it, not the logical id.
    if account_row_id is not None:
        existing = (await session.execute(
            select(V2PaperOrderIntent).where(
                V2PaperOrderIntent.account_id == account_row_id,
                V2PaperOrderIntent.idempotency_key == body.idempotency_key)
        )).scalar_one_or_none()
        if existing is not None:
            await audit(session, "paper.order.reused",
                        details={"idempotency_key": body.idempotency_key},
                        mode=mode, operator_id=operator.username,
                        correlation_id=cid, resource_id=existing.id)
            await session.commit()
            state = await current_state(session, existing.id)
            return {"outcome": "reused", "order_id": existing.id,
                    "state": state, "reasons": [], **_envelope(request)}
    if body.side not in INTENT_SIDES:
        reasons.append({"failing": "side", "allowed": list(INTENT_SIDES)})
    if body.order_type not in INTENT_TYPES:
        reasons.append({"failing": "order_type",
                        "allowed": list(INTENT_TYPES)})
    if (body.order_type == "limit") != (body.limit_price is not None):
        reasons.append({"failing": "limit_price",
                        "note": "present iff order_type=limit"})
    try:
        quantity = Decimal(body.quantity)
        if quantity <= 0:
            reasons.append({"failing": "quantity", "note": "must be > 0"})
    except InvalidOperation:
        quantity = Decimal(0)
        reasons.append({"failing": "quantity", "note": "not a decimal"})
    if not body.bars:
        reasons.append({"failing": "bars",
                        "note": "governed snapshot bars required (Q4)"})

    if reasons:
        await audit(session, "paper.order.rejected",
                    details={"reasons": reasons[:8]}, mode=mode,
                    operator_id=operator.username, correlation_id=cid)
        await session.commit()
        return {"outcome": "rejected", "order_id": None,
                "reasons": reasons, **_envelope(request)}

    content = snapshot_content_hash(body.bars, body.snapshot_ref)
    intent = V2PaperOrderIntent(
        intent_id=new_id(), account_id=account_row_id,
        instrument_id=body.instrument_id, side=body.side,
        order_type=body.order_type, quantity=str(quantity),
        limit_price=body.limit_price, time_in_force="replay_window",
        idempotency_key=body.idempotency_key,
        snapshot_ref=body.snapshot_ref,
        time_basis={"window_start": body.window_start,
                    "window_end": body.window_end,
                    "snapshot_content_hash": content},
        confirmation_ref=None, actor_id=operator.username,
        data_class=_DATA_CLASS, mode=mode,
        operator_id=operator.username, correlation_id=cid)
    session.add(intent)
    await session.flush()

    ev = await append_event(
        session, intent_row_id=intent.id, from_state="draft",
        to_state="validated", event_class="order.validated",
        details={}, actor_id=operator.username, mode=mode,
        operator_id=operator.username, correlation_id=cid,
        data_class=_DATA_CLASS)
    assert not ev.refused

    # Risk gateway — exactly once (S3/S8).
    reference_price = Decimal(str(body.bars[0]["close"]))
    fills_so_far = await collect_account_fills(session, account_row_id)
    balance = derive_balance(
        initial_balance=Decimal(account.initial_balance),
        fills=fills_so_far,
        marks={body.instrument_id: reference_price},
        margin_params=account.margin_params)
    notional = quantity * reference_price
    equity = Decimal(balance["equity"])
    concentration = (notional / equity) if equity > 0 else Decimal(1)
    session_count = len((await session.execute(
        select(V2PaperOrderIntent.id).where(
            V2PaperOrderIntent.account_id == account_row_id)
    )).all())
    decision, limits, decision_reasons = evaluate_intent(
        quantity=quantity, reference_price=reference_price,
        account_state=account.lifecycle_state, instrument_known=True,
        margin_available=Decimal(balance["margin_available"]),
        margin_required=notional * Decimal(str(account.margin_params.get(
            "margin_rate", "0.5"))),
        concentration_fraction=concentration,
        session_intent_count=session_count - 1)

    confirmation_ref = new_id() if decision == "hold" else None
    session.add(V2PaperRiskDecision(
        intent_id=intent.id, decision=decision,
        evaluated_limits=limits, reasons={"items": decision_reasons},
        risk_config_version=config_version(),
        decided_at_basis={"reference_price": str(reference_price)},
        confirmation_ref=confirmation_ref, data_class=_DATA_CLASS,
        mode=mode, operator_id=operator.username, correlation_id=cid))
    await session.flush()

    if decision == "pass":
        ev = await append_event(
            session, intent_row_id=intent.id, from_state="validated",
            to_state="risk_passed", event_class="risk.passed",
            details={"limits": limits}, actor_id=operator.username,
            mode=mode, operator_id=operator.username, correlation_id=cid,
            data_class=_DATA_CLASS)
        await audit(session, "paper.risk.passed", details={},
                    mode=mode, operator_id=operator.username,
                    correlation_id=cid, resource_id=intent.id)
    elif decision == "block":
        ev = await append_event(
            session, intent_row_id=intent.id, from_state="validated",
            to_state="risk_blocked", event_class="risk.blocked",
            details={"reasons": decision_reasons},
            actor_id=operator.username, mode=mode,
            operator_id=operator.username, correlation_id=cid,
            data_class=_DATA_CLASS)
        await audit(session, "paper.risk.blocked",
                    details={"reasons": decision_reasons}, mode=mode,
                    operator_id=operator.username, correlation_id=cid,
                    resource_id=intent.id)
    else:
        ev = await append_event(
            session, intent_row_id=intent.id, from_state="validated",
            to_state="risk_hold", event_class="hold.issued",
            details={"confirmation_ref": confirmation_ref,
                     "reasons": decision_reasons},
            actor_id=operator.username, mode=mode,
            operator_id=operator.username, correlation_id=cid,
            data_class=_DATA_CLASS)
        await audit(session, "paper.risk.hold_issued",
                    details={"confirmation_ref": confirmation_ref},
                    mode=mode, operator_id=operator.username,
                    correlation_id=cid, resource_id=intent.id)
    assert not ev.refused
    await session.commit()
    state = await current_state(session, intent.id)
    return {"outcome": "registered", "order_id": intent.id,
            "state": state, "decision": decision,
            "confirmation_ref": confirmation_ref,
            "reasons": decision_reasons, **_envelope(request)}


@router.post("/orders/confirm")
async def api_confirm_order(
    body: OrderConfirm, request: Request, operator: RequireOrdersConfirm,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    mode = _require_paper(request)
    result = await confirm_hold(
        session, intent_row_id=body.order_id,
        supplied_ref=body.confirmation_ref, resolve_to=body.resolve_to,
        actor_id=operator.username, mode=mode,
        operator_id=operator.username, correlation_id=_cid(request),
        data_class=_DATA_CLASS)
    if not result.refused:
        await session.commit()
    state = await current_state(session, body.order_id)
    return {"outcome": result.outcome, "state": state,
            "reasons": result.reasons, **_envelope(request)}


@router.post("/orders/cancel")
async def api_cancel_order(
    body: OrderCancel, request: Request, operator: RequireOrdersCancel,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    mode = _require_paper(request)
    result = await cancel_order(
        session, intent_row_id=body.order_id, actor_id=operator.username,
        mode=mode, operator_id=operator.username,
        correlation_id=_cid(request), data_class=_DATA_CLASS)
    if not result.refused:
        await session.commit()
    state = await current_state(session, body.order_id)
    return {"outcome": result.outcome, "state": state,
            "reasons": result.reasons, **_envelope(request)}


@router.post("/orders/{order_id}/run")
async def api_run_order(
    order_id: str, body: OrderRun, request: Request,
    operator: RequireOrdersPlace,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    """Governed simulator invocation (manual, Q3). Enforces may_execute."""
    mode = _require_paper(request)
    cid = _cid(request)
    intent = await get_intent(session, order_id)
    if intent is None:
        raise HTTPException(status_code=404, detail="Unknown order")

    allowed, reasons = await may_execute(session, order_id)
    if not allowed:
        await audit(session, "paper.order.run_refused",
                    details={"reasons": reasons}, mode=mode,
                    operator_id=operator.username, correlation_id=cid,
                    resource_id=order_id)
        await session.commit()
        return {"outcome": "refused", "state": await current_state(
            session, order_id), "reasons": reasons, **_envelope(request)}

    state = await current_state(session, order_id)
    if state != "risk_passed":
        await audit(session, "paper.order.run_refused",
                    details={"state": state}, mode=mode,
                    operator_id=operator.username, correlation_id=cid,
                    resource_id=order_id)
        await session.commit()
        return {"outcome": "refused", "state": state,
                "reasons": [{"failing": "state", "value": state}],
                **_envelope(request)}

    # Idempotent re-run: existing fills => converge, no re-execution (S8).
    existing_fills = list((await session.execute(
        select(V2PaperFill).where(V2PaperFill.intent_id == order_id)
    )).scalars().all())
    if existing_fills:
        await audit(session, "paper.order.run_reused",
                    details={"fill_count": len(existing_fills)}, mode=mode,
                    operator_id=operator.username, correlation_id=cid,
                    resource_id=order_id)
        await session.commit()
        return {"outcome": "reused", "state": state,
                "fill_count": len(existing_fills), "reasons": [],
                **_envelope(request)}

    ev = await append_event(
        session, intent_row_id=order_id, from_state="risk_passed",
        to_state="executing", event_class="execution.started", details={},
        actor_id=operator.username, mode=mode,
        operator_id=operator.username, correlation_id=cid,
        data_class=_DATA_CLASS)
    assert not ev.refused

    typed = PaperOrderIntent(
        intent_id=intent.intent_id, account_id=intent.account_id,
        instrument_id=intent.instrument_id, side=intent.side,
        order_type=intent.order_type, quantity=Decimal(intent.quantity),
        limit_price=(Decimal(intent.limit_price)
                     if intent.limit_price is not None else None),
        snapshot_ref=intent.snapshot_ref,
        window_start=str(intent.time_basis.get("window_start")),
        window_end=str(intent.time_basis.get("window_end")),
        cost_model=body.cost_model or {
            "spread": {"value": "0", "unit": "price", "citation": "none"},
            "commission": {"value": "0", "unit": "price",
                           "citation": "none"},
            "slippage": {"value": "0", "unit": "price", "citation": "none"},
        })
    try:
        result = run_simulation(
            typed, body.bars,
            stored_content_hash=intent.time_basis["snapshot_content_hash"])
    except PaperRefused as exc:
        ev = await append_event(
            session, intent_row_id=order_id, from_state="executing",
            to_state="quarantined_unknown", event_class="order.quarantined",
            details={"refusal_class": exc.refusal_class,
                     "reasons": exc.reasons},
            actor_id=operator.username, mode=mode,
            operator_id=operator.username, correlation_id=cid,
            data_class=_DATA_CLASS)
        await audit(session, "paper.order.quarantined",
                    details={"refusal_class": exc.refusal_class},
                    mode=mode, operator_id=operator.username,
                    correlation_id=cid, resource_id=order_id)
        await session.commit()
        return {"outcome": "quarantined", "state": "quarantined_unknown",
                "reasons": exc.reasons, **_envelope(request)}

    for f in result["fills"]:
        session.add(V2PaperFill(
            fill_id=new_id(), intent_id=order_id,
            fill_index=f["fill_index"], quantity=f["quantity"],
            raw_price=f["raw_price"], effective_price=f["effective_price"],
            cost_model_ref=typed.cost_model, fill_class=f["fill_class"],
            simulator_version=SIMULATOR_VERSION,
            snapshot_ref=intent.snapshot_ref,
            time_basis=intent.time_basis, data_class=_DATA_CLASS,
            mode=mode, operator_id=operator.username, correlation_id=cid))
    await session.flush()

    outcome_state = {"filled": "filled",
                     "partially_filled": "partially_filled",
                     "expired": "expired"}[result["outcome"]]
    event_class = {"filled": "execution.filled",
                   "partially_filled": "execution.partially_filled",
                   "expired": "execution.expired"}[result["outcome"]]
    ev = await append_event(
        session, intent_row_id=order_id, from_state="executing",
        to_state=outcome_state, event_class=event_class,
        details={"fill_count": len(result["fills"]),
                 "unfilled_quantity": result["unfilled_quantity"]},
        actor_id=operator.username, mode=mode,
        operator_id=operator.username, correlation_id=cid,
        data_class=_DATA_CLASS)
    assert not ev.refused

    if outcome_state in ("filled", "partially_filled"):
        ev = await append_event(
            session, intent_row_id=order_id, from_state=outcome_state,
            to_state="settled", event_class="order.settled",
            details={"voided_remainder": result["unfilled_quantity"]},
            actor_id=operator.username, mode=mode,
            operator_id=operator.username, correlation_id=cid,
            data_class=_DATA_CLASS)
        assert not ev.refused

        # Derived artifacts (S5): positions + balances with anchors.
        from app.db.models.v2_paper_trading import V2PaperAccount
        acct = (await session.execute(
            select(V2PaperAccount)
            .where(V2PaperAccount.id == intent.account_id)
        )).scalar_one()
        fills_all = await collect_account_fills(session, acct.id)
        marks = {intent.instrument_id:
                 Decimal(str(body.bars[-1]["close"])) if body.bars
                 else Decimal(0)}
        balance = derive_balance(
            initial_balance=Decimal(acct.initial_balance),
            fills=fills_all, marks=marks,
            margin_params=acct.margin_params)
        d_hash = derivation_hash({"fills": fills_all, "marks": {
            k: str(v) for k, v in marks.items()}})
        ev_hash = engine_versions_hash()
        session.add(V2PaperPositionSnapshot(
            account_id=acct.id,
            as_of_basis={"window_end": str(
                intent.time_basis.get("window_end"))},
            positions=balance["positions"],
            derivation_inputs_hash=d_hash, engine_versions_hash=ev_hash,
            data_class=_DATA_CLASS, mode=mode,
            operator_id=operator.username, correlation_id=cid))
        session.add(V2PaperBalanceSnapshot(
            account_id=acct.id,
            as_of_basis={"window_end": str(
                intent.time_basis.get("window_end")),
                "positions": balance["positions"]},
            cash=balance["cash"], equity=balance["equity"],
            margin_used=balance["margin_used"],
            margin_available=balance["margin_available"],
            unrealized_pnl=balance["unrealized_pnl"],
            realized_pnl=balance["realized_pnl"],
            derivation_inputs_hash=d_hash, engine_versions_hash=ev_hash,
            data_class=_DATA_CLASS, mode=mode,
            operator_id=operator.username, correlation_id=cid))
        await session.flush()
        await run_reconciliation(
            session, account_row_id=acct.id,
            initial_balance=Decimal(acct.initial_balance),
            marks=marks, margin_params=acct.margin_params,
            mode=mode, operator_id=operator.username, correlation_id=cid,
            data_class=_DATA_CLASS)

    await audit(session, "paper.order.executed",
                details={"outcome": result["outcome"],
                         "fill_count": len(result["fills"])},
                mode=mode, operator_id=operator.username,
                correlation_id=cid, resource_id=order_id)
    await session.commit()
    return {"outcome": result["outcome"],
            "state": await current_state(session, order_id),
            "fills": result["fills"],
            "engine_versions": ENGINE_VERSIONS,
            "reasons": [], **_envelope(request)}


# --- reads ----------------------------------------------------------------------


@router.get("/accounts")
async def api_list_accounts(
    request: Request, operator: RequireAccountsRead,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    limit: int = Query(default=100, ge=1, le=500),
):
    from app.db.models.v2_paper_trading import V2PaperAccount
    rows = list((await session.execute(
        select(V2PaperAccount).order_by(V2PaperAccount.created_at.desc())
        .limit(limit))).scalars().all())
    return {"accounts": [
        {"id": r.id, "account_id": r.account_id, "record_seq": r.record_seq,
         "name": r.name, "lifecycle_state": r.lifecycle_state,
         "base_currency": r.base_currency,
         "initial_balance": r.initial_balance} for r in rows],
        **_envelope(request)}


@router.get("/orders")
async def api_list_orders(
    request: Request, operator: RequireOrdersRead,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    limit: int = Query(default=100, ge=1, le=500),
):
    rows = list((await session.execute(
        select(V2PaperOrderIntent)
        .order_by(V2PaperOrderIntent.created_at.desc())
        .limit(limit))).scalars().all())
    out = []
    for r in rows:
        out.append({"id": r.id, "intent_id": r.intent_id,
                    "account_id": r.account_id, "side": r.side,
                    "order_type": r.order_type, "quantity": r.quantity,
                    "state": await current_state(session, r.id)})
    return {"orders": out, **_envelope(request)}


@router.get("/orders/{order_id}/events")
async def api_order_events(
    order_id: str, request: Request, operator: RequireOrdersRead,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    rows = list((await session.execute(
        select(V2PaperOrderEvent)
        .where(V2PaperOrderEvent.intent_id == order_id)
        .order_by(V2PaperOrderEvent.event_index))).scalars().all())
    return {"events": [
        {"event_index": r.event_index, "from_state": r.from_state,
         "to_state": r.to_state, "event_class": r.event_class,
         "details": r.details} for r in rows], **_envelope(request)}


@router.get("/fills")
async def api_list_fills(
    request: Request, operator: RequireFillsRead,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    limit: int = Query(default=100, ge=1, le=500),
):
    rows = list((await session.execute(
        select(V2PaperFill).order_by(V2PaperFill.created_at.desc())
        .limit(limit))).scalars().all())
    return {"fills": [
        {"id": r.id, "intent_id": r.intent_id, "fill_index": r.fill_index,
         "quantity": r.quantity, "raw_price": r.raw_price,
         "effective_price": r.effective_price,
         "fill_class": r.fill_class,
         "simulator_version": r.simulator_version} for r in rows],
        **_envelope(request)}


@router.get("/positions")
async def api_list_positions(
    request: Request, operator: RequireAccountsRead,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    limit: int = Query(default=100, ge=1, le=500),
):
    rows = list((await session.execute(
        select(V2PaperPositionSnapshot)
        .order_by(V2PaperPositionSnapshot.created_at.desc())
        .limit(limit))).scalars().all())
    return {"positions": [
        {"id": r.id, "account_id": r.account_id,
         "positions": r.positions, "as_of_basis": r.as_of_basis}
        for r in rows], **_envelope(request)}


@router.get("/balances")
async def api_list_balances(
    request: Request, operator: RequireAccountsRead,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    limit: int = Query(default=100, ge=1, le=500),
):
    rows = list((await session.execute(
        select(V2PaperBalanceSnapshot)
        .order_by(V2PaperBalanceSnapshot.created_at.desc())
        .limit(limit))).scalars().all())
    return {"balances": [
        {"id": r.id, "account_id": r.account_id, "cash": r.cash,
         "equity": r.equity, "margin_used": r.margin_used,
         "margin_available": r.margin_available,
         "unrealized_pnl": r.unrealized_pnl,
         "realized_pnl": r.realized_pnl} for r in rows],
        **_envelope(request)}


@router.get("/risk-decisions")
async def api_list_risk_decisions(
    request: Request, operator: RequireRiskRead,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    limit: int = Query(default=100, ge=1, le=500),
):
    rows = list((await session.execute(
        select(V2PaperRiskDecision)
        .order_by(V2PaperRiskDecision.created_at.desc())
        .limit(limit))).scalars().all())
    return {"risk_decisions": [
        {"id": r.id, "intent_id": r.intent_id, "decision": r.decision,
         "evaluated_limits": r.evaluated_limits,
         "risk_config_version": r.risk_config_version} for r in rows],
        **_envelope(request)}


@router.get("/reconciliations")
async def api_list_reconciliations(
    request: Request, operator: RequireAccountsRead,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    limit: int = Query(default=100, ge=1, le=500),
):
    rows = list((await session.execute(
        select(V2PaperReconciliation)
        .order_by(V2PaperReconciliation.created_at.desc())
        .limit(limit))).scalars().all())
    return {"reconciliations": [
        {"id": r.id, "account_id": r.account_id, "outcome": r.outcome,
         "discrepancies": r.discrepancies} for r in rows],
        **_envelope(request)}
