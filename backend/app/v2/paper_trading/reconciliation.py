"""BE-8 reconciliation writer (design S5/S1.1 row 8; BO T-12).

Genesis recompute over the full fill ledger vs the latest stored balance
snapshot; content comparison (PGF-012); outcome row immutable; discrepant
is a typed alarm surface — NEVER auto-corrected.
"""

from __future__ import annotations

from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.v2_paper_trading import (
    V2PaperBalanceSnapshot,
    V2PaperFill,
    V2PaperOrderIntent,
    V2PaperReconciliation,
)
from app.v2.paper_trading.contracts import PaperOutcome
from app.v2.paper_trading.ledger import derivation_hash, derive_balance, reconcile
from app.v2.paper_trading.orders import audit


async def collect_account_fills(session: AsyncSession,
                                account_row_id: str) -> list[dict]:
    """All fills for the account, chronological, with side/instrument."""
    intents = {
        row.id: row
        for row in (await session.execute(
            select(V2PaperOrderIntent)
            .where(V2PaperOrderIntent.account_id == account_row_id)
        )).scalars().all()
    }
    if not intents:
        return []
    fills = list((await session.execute(
        select(V2PaperFill)
        .where(V2PaperFill.intent_id.in_(list(intents)))
        .order_by(V2PaperFill.created_at, V2PaperFill.fill_index)
    )).scalars().all())
    out = []
    for f in fills:
        intent = intents[f.intent_id]
        out.append({
            "instrument_id": intent.instrument_id, "side": intent.side,
            "quantity": f.quantity, "effective_price": f.effective_price})
    return out


async def run_reconciliation(
    session: AsyncSession, *, account_row_id: str,
    initial_balance: Decimal, marks: dict, margin_params: dict,
    mode: str, operator_id: str, correlation_id: str | None,
    data_class: str,
) -> PaperOutcome:
    fills = await collect_account_fills(session, account_row_id)
    recomputed = derive_balance(
        initial_balance=initial_balance, fills=fills,
        marks={k: Decimal(str(v)) for k, v in marks.items()},
        margin_params=margin_params)
    latest = (await session.execute(
        select(V2PaperBalanceSnapshot)
        .where(V2PaperBalanceSnapshot.account_id == account_row_id)
        .order_by(V2PaperBalanceSnapshot.created_at.desc())
    )).scalars().first()
    if latest is None:
        outcome, discrepancies = "consistent", []
    else:
        stored = {
            "positions": latest.as_of_basis.get("positions",
                                                recomputed["positions"]),
            "cash": latest.cash, "equity": latest.equity,
            "margin_used": latest.margin_used,
            "margin_available": latest.margin_available,
            "unrealized_pnl": latest.unrealized_pnl,
            "realized_pnl": latest.realized_pnl,
        }
        stored["positions"] = recomputed["positions"] if not isinstance(
            stored["positions"], dict) else stored["positions"]
        outcome, discrepancies = reconcile(snapshot=stored,
                                           recomputed=recomputed)
    row = V2PaperReconciliation(
        account_id=account_row_id,
        run_basis={"fills": len(fills), "marks": {
            k: str(v) for k, v in marks.items()}},
        outcome=outcome, discrepancies={"items": discrepancies},
        inputs_hash=derivation_hash({"fills": fills, "marks": {
            k: str(v) for k, v in marks.items()}}),
        data_class=data_class, mode=mode, operator_id=operator_id,
        correlation_id=correlation_id)
    session.add(row)
    await session.flush()
    await audit(session, "paper.reconciliation.completed",
                details={"outcome": outcome,
                         "discrepancy_count": len(discrepancies)},
                mode=mode, operator_id=operator_id,
                correlation_id=correlation_id,
                resource_type="paper_reconciliation", resource_id=row.id)
    return PaperOutcome(outcome=outcome, reasons=discrepancies,
                        record_id=row.id)
