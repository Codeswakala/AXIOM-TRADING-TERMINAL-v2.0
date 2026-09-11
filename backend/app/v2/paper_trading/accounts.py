"""BE-8 paper account writers (design S1/S7.2; BO T-5).

Versioned-immutable accounts (record_seq + supersedes; currency of the
greatest record_seq). Account lifecycle acts are confirmation-gated
(S7.2): the create/freeze/close primary act returns pending_confirmation
with a single-use ref; the confirm act executes the write. Consumption is
ledger-derived over the audit trail of this module's own pending registry
table-free design: the pending ref is held in the audit event and
re-derived — v1 keeps it simpler: the primary act stores NOTHING and
returns the ref; the confirm act carries the full payload + ref and the
writer verifies the ref was minted for exactly that payload (HMAC-free
deterministic digest — no secret, N1).
"""

from __future__ import annotations

import hashlib
import json

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.v2_paper_trading import V2PaperAccount
from app.v2.paper_trading.contracts import (
    ACCOUNT_STATES,
    BASE_CURRENCIES_V1,
    PaperOutcome,
)
from app.v2.paper_trading.orders import audit


def _canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


def mint_confirmation_ref(payload: dict) -> str:
    """Deterministic single-use ref bound to the exact payload (no secret)."""
    return "pconf-" + hashlib.sha256(
        _canonical(payload).encode()).hexdigest()[:32]


async def request_account_action(
    session: AsyncSession, *, action: str, payload: dict, mode: str,
    operator_id: str, correlation_id: str | None,
) -> PaperOutcome:
    """Primary act: validates and returns pending_confirmation + ref."""
    reasons: list = []
    if action == "create":
        if payload.get("base_currency") not in BASE_CURRENCIES_V1:
            reasons.append({"failing": "base_currency",
                            "allowed": list(BASE_CURRENCIES_V1)})
        try:
            if float(payload.get("initial_balance", "0")) <= 0:
                reasons.append({"failing": "initial_balance",
                                "note": "must be positive"})
        except (TypeError, ValueError):
            reasons.append({"failing": "initial_balance",
                            "note": "not a decimal"})
    if reasons:
        await audit(session, "paper.account.request_refused",
                    details={"action": action, "reasons": reasons},
                    mode=mode, operator_id=operator_id,
                    correlation_id=correlation_id,
                    resource_type="paper_account")
        await session.commit()
        return PaperOutcome(outcome="refused", reasons=reasons)
    ref = mint_confirmation_ref({"action": action, **payload})
    await audit(session, "paper.account.confirmation_requested",
                details={"action": action, "confirmation_ref": ref},
                mode=mode, operator_id=operator_id,
                correlation_id=correlation_id,
                resource_type="paper_account")
    return PaperOutcome(outcome="pending_confirmation", reasons=[],
                        confirmation_ref=ref)


async def confirm_account_action(
    session: AsyncSession, *, action: str, payload: dict,
    confirmation_ref: str, actor_id: str, mode: str, operator_id: str,
    correlation_id: str | None, data_class: str,
) -> PaperOutcome:
    """Confirm act: verifies the ref binds the exact payload, then writes."""
    expected = mint_confirmation_ref({"action": action, **payload})
    if confirmation_ref != expected:
        await audit(session, "paper.account.confirm_refused",
                    details={"refusal_class":
                             "paper.confirmation.ref_mismatch",
                             "action": action},
                    mode=mode, operator_id=operator_id,
                    correlation_id=correlation_id,
                    resource_type="paper_account")
        await session.commit()
        return PaperOutcome(outcome="refused", reasons=[
            {"failing": "paper.confirmation.ref_mismatch"}])

    account_id = payload["account_id"]
    newest = (await session.execute(
        select(V2PaperAccount)
        .where(V2PaperAccount.account_id == account_id)
        .order_by(V2PaperAccount.record_seq.desc())
    )).scalars().first()

    if action == "create":
        if newest is not None:
            await audit(session, "paper.account.confirm_refused",
                        details={"refusal_class":
                                 "paper.confirmation.already_consumed",
                                 "note": "account exists"},
                        mode=mode, operator_id=operator_id,
                        correlation_id=correlation_id,
                        resource_type="paper_account")
            await session.commit()
            return PaperOutcome(outcome="refused", reasons=[
                {"failing": "paper.confirmation.already_consumed",
                 "note": "account already exists (single-use ref consumed)"}])
        row = V2PaperAccount(
            account_id=account_id, record_seq=1, supersedes=None,
            name=payload["name"], base_currency=payload["base_currency"],
            initial_balance=str(payload["initial_balance"]),
            margin_params=payload.get("margin_params", {}),
            lifecycle_state="active", confirmation_ref=confirmation_ref,
            data_class=data_class, mode=mode, operator_id=operator_id,
            correlation_id=correlation_id)
        session.add(row)
        await session.flush()
        await audit(session, "paper.account.created",
                    details={"account_id": account_id,
                             "confirmation_ref": confirmation_ref},
                    mode=mode, operator_id=operator_id,
                    correlation_id=correlation_id,
                    resource_type="paper_account", resource_id=row.id)
        return PaperOutcome(outcome="applied", reasons=[], record_id=row.id)

    # freeze / close: supersede with the new lifecycle state.
    target_state = {"freeze": "frozen", "close": "closed"}.get(action)
    if target_state is None or target_state not in ACCOUNT_STATES:
        await session.commit()
        return PaperOutcome(outcome="refused", reasons=[
            {"failing": "action", "value": action}])
    if newest is None:
        await session.commit()
        return PaperOutcome(outcome="refused", reasons=[
            {"failing": "account_id", "note": "unknown account"}])
    row = V2PaperAccount(
        account_id=account_id, record_seq=newest.record_seq + 1,
        supersedes=newest.id, name=newest.name,
        base_currency=newest.base_currency,
        initial_balance=newest.initial_balance,
        margin_params=newest.margin_params,
        lifecycle_state=target_state, confirmation_ref=confirmation_ref,
        data_class=data_class, mode=mode, operator_id=operator_id,
        correlation_id=correlation_id)
    session.add(row)
    await session.flush()
    await audit(session, f"paper.account.{action}d",
                details={"account_id": account_id,
                         "confirmation_ref": confirmation_ref},
                mode=mode, operator_id=operator_id,
                correlation_id=correlation_id,
                resource_type="paper_account", resource_id=row.id)
    return PaperOutcome(outcome="applied", reasons=[], record_id=row.id)


async def current_account(session: AsyncSession,
                          account_id: str) -> V2PaperAccount | None:
    """Currency law: greatest record_seq is the current generation."""
    return (await session.execute(
        select(V2PaperAccount)
        .where(V2PaperAccount.account_id == account_id)
        .order_by(V2PaperAccount.record_seq.desc())
    )).scalars().first()
