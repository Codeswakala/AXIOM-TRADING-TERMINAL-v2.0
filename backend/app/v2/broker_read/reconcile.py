"""BE-9 read-side reconciliation (design S5/S5.1/S6; BO T-12/T-13).

Authority = the broker (V2-R-10). Writes ONLY discrepancy records and
the reconcile-run lineage row; projections are never touched. The clean
run is evidenced with both-side digests under the ONE S4.1 canon.
"""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.v2_broker_read import (
    V2BrokerBalance,
    V2BrokerDiscrepancy,
    V2BrokerFill,
    V2BrokerInstrumentPermission,
    V2BrokerOrder,
    V2BrokerPosition,
    V2BrokerReconcileRun,
)
from app.v2.broker_read.contract import (
    DISCREPANCY_TRANSITIONS,
)
from app.v2.broker_read.sync import _audit, canonical_digest

_DATA_CLASS = "simulated"


def _dec_eq(a, b) -> bool:
    try:
        return Decimal(str(a)) == Decimal(str(b))
    except (InvalidOperation, TypeError):
        return str(a) == str(b)


async def _projection_payload(session: AsyncSession,
                              sync_run_id: str) -> dict:
    """Rebuild the canonical payload set from the landed projections of
    the given sync run (one canon, two sides — S5.1)."""
    balances = list((await session.execute(
        select(V2BrokerBalance).where(
            V2BrokerBalance.sync_run_id == sync_run_id))).scalars().all())
    positions = list((await session.execute(
        select(V2BrokerPosition).where(
            V2BrokerPosition.sync_run_id == sync_run_id))).scalars().all())
    orders = list((await session.execute(
        select(V2BrokerOrder).where(
            V2BrokerOrder.sync_run_id == sync_run_id))).scalars().all())
    fills = list((await session.execute(select(V2BrokerFill))).scalars().all())
    instruments = list((await session.execute(
        select(V2BrokerInstrumentPermission).where(
            V2BrokerInstrumentPermission.sync_run_id
            == sync_run_id))).scalars().all())
    return {
        "balances": [{
            "broker_account_ext_id": b.broker_account_ext_id,
            "balance": b.balance, "margin_used": b.margin_used,
            "margin_available": b.margin_available,
            "unrealized_pl": b.unrealized_pl, "currency": b.currency,
        } for b in balances],
        "positions": [{
            "broker_account_ext_id": p.broker_account_ext_id,
            "instrument_ext_id": p.instrument_ext_id,
            "units_long": p.units_long, "units_short": p.units_short,
            "avg_price_long": p.avg_price_long,
            "avg_price_short": p.avg_price_short,
        } for p in positions],
        "orders": [{
            "order_ext_id": o.order_ext_id,
            "broker_account_ext_id": o.broker_account_ext_id,
            "order_state_ext": o.order_state_ext, "payload": o.payload,
        } for o in orders],
        "fills": [{
            "transaction_ext_id": f.transaction_ext_id,
            "broker_account_ext_id": f.broker_account_ext_id,
            "tx_type_ext": f.tx_type_ext,
            "instrument_ext_id": f.instrument_ext_id,
            "units": f.units, "price": f.price,
            "tx_time_ext": f.tx_time_ext,
        } for f in fills],
        "instrument_permissions": [{
            "broker_account_ext_id": i.broker_account_ext_id,
            "instrument_ext_id": i.instrument_ext_id,
            "visibility": i.visibility, "display_name": i.display_name,
        } for i in instruments],
    }


def _detect(broker: dict, projection: dict, provenance: dict) -> list[dict]:
    """The comparison law: exact compare (A-5), 7 closed classes."""
    found: list[dict] = []

    def _rec(cls, b_side, p_side):
        found.append({"class": cls, "broker_side": b_side,
                      "projection_side": p_side,
                      "provenance": provenance})

    # balances: per-account, per-field exact compare
    b_bal = {r["broker_account_ext_id"]: r
             for r in broker.get("balances", [])}
    p_bal = {r["broker_account_ext_id"]: r
             for r in projection.get("balances", [])}
    for acct in set(b_bal) | set(p_bal):
        if acct not in p_bal:
            _rec("missing_in_axiom", b_bal[acct], {})
            continue
        if acct not in b_bal:
            _rec("missing_on_broker", {}, p_bal[acct])
            continue
        b, p = b_bal[acct], p_bal[acct]
        if b.get("currency") != p.get("currency"):
            _rec("currency_mismatch", b, p)
        for f in ("balance", "margin_used", "margin_available",
                  "unrealized_pl"):
            if not _dec_eq(b.get(f), p.get(f)):
                _rec("amount_mismatch",
                     {"field": f, **b}, {"field": f, **p})

    # positions: units/prices per instrument
    def _pos_key(r):
        return (r["broker_account_ext_id"], r["instrument_ext_id"])
    b_pos = {_pos_key(r): r for r in broker.get("positions", [])}
    p_pos = {_pos_key(r): r for r in projection.get("positions", [])}
    for key in set(b_pos) | set(p_pos):
        if key not in p_pos:
            _rec("missing_in_axiom", b_pos[key], {})
        elif key not in b_pos:
            _rec("missing_on_broker", {}, p_pos[key])
        else:
            b, p = b_pos[key], p_pos[key]
            for f in ("units_long", "units_short", "avg_price_long",
                      "avg_price_short"):
                if not _dec_eq(b.get(f), p.get(f)):
                    _rec("amount_mismatch",
                         {"field": f, **b}, {"field": f, **p})

    # open-order set equality
    b_ord = {r["order_ext_id"] for r in broker.get("orders", [])}
    p_ord = {r["order_ext_id"] for r in projection.get("orders", [])}
    if b_ord != p_ord:
        _rec("set_mismatch", {"orders": sorted(b_ord)},
             {"orders": sorted(p_ord)})

    # fill-ledger completeness (broker ids vs anchors)
    b_tx = {r["transaction_ext_id"] for r in broker.get("fills", [])}
    p_tx = {r["transaction_ext_id"] for r in projection.get("fills", [])}
    for missing in b_tx - p_tx:
        _rec("missing_in_axiom", {"transaction_ext_id": missing}, {})

    # instrument-permission set equality
    b_ins = {r["instrument_ext_id"]
             for r in broker.get("instrument_permissions", [])}
    p_ins = {r["instrument_ext_id"]
             for r in projection.get("instrument_permissions", [])}
    if (b_ins or p_ins) and b_ins != p_ins:
        _rec("permission_visibility", {"instruments": sorted(b_ins)},
             {"instruments": sorted(p_ins)})
    return found


async def run_reconciliation(session: AsyncSession, *, broker_payload: dict,
                             sync_run_id: str, provider_id: str,
                             actor_id: str, mode: str,
                             correlation_id: str | None) -> dict:
    projection_payload = await _projection_payload(session, sync_run_id)
    provenance = {"sync_run_id": sync_run_id, "provider_id": provider_id}
    discrepancies = _detect(broker_payload, projection_payload, provenance)

    run = V2BrokerReconcileRun(
        provider_id=provider_id, sync_run_id=sync_run_id,
        compare_scope={"models": ["balances", "positions", "orders",
                                  "fills", "instrument_permissions"]},
        broker_side_digest=canonical_digest(broker_payload),
        projection_side_digest=canonical_digest(projection_payload),
        compared_counts={k: len(v) for k, v in projection_payload.items()},
        discrepancy_count=len(discrepancies),
        outcome="clean" if not discrepancies else "discrepant",
        actor_id=actor_id, data_class=_DATA_CLASS, mode=mode,
        operator_id=actor_id, correlation_id=correlation_id)
    session.add(run)
    await session.flush()

    for d in discrepancies:
        session.add(V2BrokerDiscrepancy(
            discrepancy_id=f"disc-{uuid4().hex[:12]}", record_seq=1,
            supersedes=None, reconcile_run_id=run.id,
            discrepancy_class=d["class"], state="detected",
            broker_side=d["broker_side"],
            projection_side=d["projection_side"], owned_by=None,
            dismiss_reason=None, provider_id=provider_id,
            data_class=_DATA_CLASS, mode=mode, operator_id=actor_id,
            correlation_id=correlation_id))
    await session.flush()
    await _audit(session, "broker.reconcile.completed",
                 details={"outcome": run.outcome,
                          "discrepancy_count": len(discrepancies)},
                 mode=mode, operator_id=actor_id,
                 correlation_id=correlation_id, resource_id=run.id)
    return {"outcome": run.outcome, "reconcile_run_id": run.id,
            "discrepancy_count": len(discrepancies),
            "broker_side_digest": run.broker_side_digest,
            "projection_side_digest": run.projection_side_digest}


async def transition_discrepancy(session: AsyncSession, *,
                                 discrepancy_id: str, to_state: str,
                                 actor_id: str, reason: str | None,
                                 mode: str,
                                 correlation_id: str | None) -> dict:
    """S6 state machine: generations only, transitions typed + audited."""
    newest = (await session.execute(
        select(V2BrokerDiscrepancy)
        .where(V2BrokerDiscrepancy.discrepancy_id == discrepancy_id)
        .order_by(V2BrokerDiscrepancy.record_seq.desc()))).scalars().first()
    if newest is None:
        return {"outcome": "refused",
                "reasons": [{"failing": "discrepancy_id"}]}
    if (newest.state, to_state) not in DISCREPANCY_TRANSITIONS:
        await _audit(session, "broker.discrepancy.transition_refused",
                     details={"from": newest.state, "to": to_state},
                     mode=mode, operator_id=actor_id,
                     correlation_id=correlation_id, resource_id=newest.id)
        await session.commit()
        return {"outcome": "refused", "reasons": [
            {"failing": "transition", "from": newest.state,
             "to": to_state}]}
    if to_state == "dismissed_with_reason" and not reason:
        await _audit(session, "broker.discrepancy.transition_refused",
                     details={"to": to_state, "note": "reason mandatory"},
                     mode=mode, operator_id=actor_id,
                     correlation_id=correlation_id, resource_id=newest.id)
        await session.commit()
        return {"outcome": "refused", "reasons": [
            {"failing": "reason", "note": "dismissal requires a reason"}]}
    row = V2BrokerDiscrepancy(
        discrepancy_id=discrepancy_id, record_seq=newest.record_seq + 1,
        supersedes=newest.id, reconcile_run_id=newest.reconcile_run_id,
        discrepancy_class=newest.discrepancy_class, state=to_state,
        broker_side=newest.broker_side,
        projection_side=newest.projection_side,
        owned_by=actor_id if to_state == "owned" else newest.owned_by,
        dismiss_reason=reason if to_state == "dismissed_with_reason"
        else None,
        provider_id=newest.provider_id, data_class=_DATA_CLASS,
        mode=mode, operator_id=actor_id, correlation_id=correlation_id)
    session.add(row)
    await session.flush()
    await _audit(session, f"broker.discrepancy.{to_state}",
                 details={"discrepancy_id": discrepancy_id},
                 mode=mode, operator_id=actor_id,
                 correlation_id=correlation_id, resource_id=row.id)
    return {"outcome": "applied", "state": to_state, "record_id": row.id}
