"""BE-8 order lifecycle writers (design S2; BO T-5/T-7/T-8/T-9).

Zero-UPDATE regime: state lives ONLY in the append-only event ledger;
current state = to_state of max event_index (S2.3 derivation law).
The S2.6/C-1a derived rule `may_execute` is owned HERE, once, and
consumed by the run writer and by tests — no duplicated logic.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.v2_paper_trading import (
    V2PaperOrderEvent,
    V2PaperOrderIntent,
    V2PaperRiskDecision,
)
from app.v2.audit.contract import V2AuditEventCreate
from app.v2.audit.repository import V2AuditRepository
from app.v2.paper_trading.contracts import (
    LEGAL_TRANSITIONS,
    TERMINAL_STATES,
    PaperOutcome,
)

_DOMAIN = "v2.paper_trading"


async def audit(session: AsyncSession, action: str, *, details: dict,
                mode: str, operator_id: str, correlation_id: str | None,
                resource_type: str = "paper_order",
                resource_id: str | None = None) -> None:
    await V2AuditRepository(session).append(V2AuditEventCreate(
        domain=_DOMAIN, action=action, actor_id=operator_id,
        actor_type="operator", mode=mode, resource_type=resource_type,
        resource_id=resource_id, details=details, operator_id=operator_id,
        correlation_id=correlation_id))


async def current_state(session: AsyncSession, intent_row_id: str) -> str:
    """S2.3: the to_state of the max event_index — a query, not a column."""
    latest = (await session.execute(
        select(V2PaperOrderEvent)
        .where(V2PaperOrderEvent.intent_id == intent_row_id)
        .order_by(V2PaperOrderEvent.event_index.desc())
    )).scalars().first()
    return latest.to_state if latest is not None else "draft"


async def append_event(session: AsyncSession, *, intent_row_id: str,
                       from_state: str, to_state: str, event_class: str,
                       details: dict, actor_id: str, mode: str,
                       operator_id: str, correlation_id: str | None,
                       data_class: str) -> PaperOutcome:
    """The ONLY state-advancing writer. Refuses illegal transitions typed."""
    if (from_state, to_state) not in LEGAL_TRANSITIONS:
        await audit(session, "paper.order.transition_refused",
                    details={"from": from_state, "to": to_state,
                             "note": "absent from LEGAL_TRANSITIONS"},
                    mode=mode, operator_id=operator_id,
                    correlation_id=correlation_id,
                    resource_id=intent_row_id)
        await session.commit()  # C-1 durable-refusal law
        return PaperOutcome(outcome="refused", reasons=[
            {"failing": "transition", "from": from_state, "to": to_state}])
    observed = await current_state(session, intent_row_id)
    if observed != from_state:
        await audit(session, "paper.order.transition_refused",
                    details={"expected_from": from_state,
                             "observed": observed, "to": to_state},
                    mode=mode, operator_id=operator_id,
                    correlation_id=correlation_id,
                    resource_id=intent_row_id)
        await session.commit()
        return PaperOutcome(outcome="refused", reasons=[
            {"failing": "current_state", "observed": observed,
             "expected": from_state}])
    latest = (await session.execute(
        select(V2PaperOrderEvent)
        .where(V2PaperOrderEvent.intent_id == intent_row_id)
        .order_by(V2PaperOrderEvent.event_index.desc())
    )).scalars().first()
    next_index = 0 if latest is None else latest.event_index + 1
    row = V2PaperOrderEvent(
        intent_id=intent_row_id, event_index=next_index,
        from_state=from_state, to_state=to_state, event_class=event_class,
        details=details, actor_id=actor_id, data_class=data_class,
        mode=mode, operator_id=operator_id, correlation_id=correlation_id)
    session.add(row)
    await session.flush()
    return PaperOutcome(outcome="applied", reasons=[], record_id=row.id)


async def may_execute(session: AsyncSession, intent_row_id: str) -> tuple[bool, list]:
    """THE single derived executing-precondition rule (S2.6/C-1a), owned once.

    True iff: decision='pass', OR (decision='hold' AND a hold.confirmed
    event citing the decision's exact confirmation_ref exists AND no
    hold.cancelled event exists). All other cases: (False, reasons).
    """
    decision = (await session.execute(
        select(V2PaperRiskDecision)
        .where(V2PaperRiskDecision.intent_id == intent_row_id)
    )).scalar_one_or_none()
    if decision is None:
        return False, [{"failing": "risk_decision", "note": "absent"}]
    if decision.decision == "pass":
        return True, []
    if decision.decision == "block":
        return False, [{"failing": "risk_decision", "value": "block",
                        "note": "terminal; no confirmation path (C-1d)"}]
    # decision == 'hold'
    events = list((await session.execute(
        select(V2PaperOrderEvent)
        .where(V2PaperOrderEvent.intent_id == intent_row_id)
    )).scalars().all())
    cancelled = any(e.event_class == "hold.cancelled" for e in events)
    if cancelled:
        return False, [{"failing": "hold", "note": "cancelled"}]
    confirmed = any(
        e.event_class == "hold.confirmed"
        and e.details.get("confirmation_ref") == decision.confirmation_ref
        for e in events)
    if confirmed:
        return True, []
    return False, [{"failing": "hold", "note": "unresolved"}]


async def confirmation_status(session: AsyncSession,
                              intent_row_id: str) -> tuple[str, str | None]:
    """C-1b consumption derivation: ('none'|'open'|'confirmed'|'cancelled',
    the minted ref or None). Ledger-derived; no mutable marker exists."""
    decision = (await session.execute(
        select(V2PaperRiskDecision)
        .where(V2PaperRiskDecision.intent_id == intent_row_id)
    )).scalar_one_or_none()
    if decision is None or decision.decision != "hold":
        return "none", None
    events = list((await session.execute(
        select(V2PaperOrderEvent)
        .where(V2PaperOrderEvent.intent_id == intent_row_id)
    )).scalars().all())
    for e in events:
        if e.event_class == "hold.cancelled":
            return "cancelled", decision.confirmation_ref
    for e in events:
        if (e.event_class == "hold.confirmed"
                and e.details.get("confirmation_ref")
                == decision.confirmation_ref):
            return "confirmed", decision.confirmation_ref
    return "open", decision.confirmation_ref


async def confirm_hold(session: AsyncSession, *, intent_row_id: str,
                       supplied_ref: str, resolve_to: str, actor_id: str,
                       mode: str, operator_id: str,
                       correlation_id: str | None,
                       data_class: str) -> PaperOutcome:
    """The C-1b confirm/cancel writer with the four typed refusal classes.

    resolve_to: 'confirm' -> risk_hold -> risk_passed (hold.confirmed);
    'cancel' -> risk_hold -> cancelled (hold.cancelled).
    """
    async def _refuse(refusal_class: str, extra: dict) -> PaperOutcome:
        await audit(session, "paper.order.confirm_refused",
                    details={"refusal_class": refusal_class, **extra},
                    mode=mode, operator_id=operator_id,
                    correlation_id=correlation_id,
                    resource_id=intent_row_id)
        await session.commit()  # durable despite refusal
        return PaperOutcome(outcome="refused", reasons=[
            {"failing": refusal_class, **extra}])

    decision = (await session.execute(
        select(V2PaperRiskDecision)
        .where(V2PaperRiskDecision.intent_id == intent_row_id)
    )).scalar_one_or_none()
    if decision is None or decision.decision != "hold":
        return await _refuse("paper.confirmation.not_confirmable", {
            "decision": decision.decision if decision else None})
    status, minted_ref = await confirmation_status(session, intent_row_id)
    if status == "cancelled":
        return await _refuse("paper.confirmation.cancelled", {})
    if status == "confirmed":
        return await _refuse("paper.confirmation.already_consumed", {})
    if supplied_ref != minted_ref:
        return await _refuse("paper.confirmation.ref_mismatch", {})

    if resolve_to == "confirm":
        outcome = await append_event(
            session, intent_row_id=intent_row_id,
            from_state="risk_hold", to_state="risk_passed",
            event_class="hold.confirmed",
            details={"confirmation_ref": minted_ref,
                     "confirmed_by": actor_id},
            actor_id=actor_id, mode=mode, operator_id=operator_id,
            correlation_id=correlation_id, data_class=data_class)
        action = "paper.order.hold_confirmed"
    else:
        outcome = await append_event(
            session, intent_row_id=intent_row_id,
            from_state="risk_hold", to_state="cancelled",
            event_class="hold.cancelled",
            details={"confirmation_ref": minted_ref,
                     "cancelled_by": actor_id},
            actor_id=actor_id, mode=mode, operator_id=operator_id,
            correlation_id=correlation_id, data_class=data_class)
        action = "paper.order.hold_cancelled"
    if outcome.refused:
        return outcome
    await audit(session, action,
                details={"confirmation_ref": minted_ref},
                mode=mode, operator_id=operator_id,
                correlation_id=correlation_id, resource_id=intent_row_id)
    return outcome


async def cancel_order(session: AsyncSession, *, intent_row_id: str,
                       actor_id: str, mode: str, operator_id: str,
                       correlation_id: str | None,
                       data_class: str) -> PaperOutcome:
    """Pre-execution cancel only; terminal/executing = typed refusal."""
    state = await current_state(session, intent_row_id)
    if state in TERMINAL_STATES or state in ("executing", "filled",
                                             "partially_filled",
                                             "risk_passed"):
        await audit(session, "paper.order.cancel_refused",
                    details={"state": state}, mode=mode,
                    operator_id=operator_id, correlation_id=correlation_id,
                    resource_id=intent_row_id)
        await session.commit()
        return PaperOutcome(outcome="refused", reasons=[
            {"failing": "state", "value": state,
             "note": "cancel is pre-risk/pre-execution only"}])
    if state == "risk_hold":
        # hold-cancel goes through the C-1 mechanism, not this writer.
        await audit(session, "paper.order.cancel_refused",
                    details={"state": state,
                             "note": "resolve holds via the confirmation act"},
                    mode=mode, operator_id=operator_id,
                    correlation_id=correlation_id, resource_id=intent_row_id)
        await session.commit()
        return PaperOutcome(outcome="refused", reasons=[
            {"failing": "state", "value": state,
             "note": "hold resolution uses the confirmation mechanism"}])
    outcome = await append_event(
        session, intent_row_id=intent_row_id, from_state=state,
        to_state="cancelled", event_class="order.cancelled",
        details={"cancelled_by": actor_id}, actor_id=actor_id, mode=mode,
        operator_id=operator_id, correlation_id=correlation_id,
        data_class=data_class)
    if not outcome.refused:
        await audit(session, "paper.order.cancelled", details={},
                    mode=mode, operator_id=operator_id,
                    correlation_id=correlation_id, resource_id=intent_row_id)
    return outcome


async def get_intent(session: AsyncSession,
                     intent_row_id: str) -> V2PaperOrderIntent | None:
    return (await session.execute(
        select(V2PaperOrderIntent)
        .where(V2PaperOrderIntent.id == intent_row_id)
    )).scalar_one_or_none()
