"""BE-9 sync engine (design S4; BO T-10/T-11/T-15).

All-or-nothing single-transaction landing: every page of every scope is
fetched and validated BEFORE any row lands; a failed page => the write
transaction never opens => `partial_refused` lineage row + typed refusal.
The S4.1 digest canon is implemented here verbatim (allow-list inclusion,
natural-key ordering, fixed model order, JSON canonical encoding).
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.v2_broker_read import (
    V2BrokerAccount,
    V2BrokerBalance,
    V2BrokerFill,
    V2BrokerInstrumentPermission,
    V2BrokerOrder,
    V2BrokerPosition,
    V2BrokerSyncRun,
)
from app.v2.audit.contract import V2AuditEventCreate
from app.v2.audit.repository import V2AuditRepository
from app.v2.broker_read.contract import (
    ORIGIN_FLOOR_ISO,
    BrokerRefused,
)

_DOMAIN = "v2.broker_read"
_DATA_CLASS = "simulated"

# --- S4.1 digest canon (C-1): allow-list inclusion, fixed order -----------------

CANON_FIELDS = {
    "accounts": ("broker_account_ext_id", "alias", "currency",
                 "environment"),
    "balances": ("broker_account_ext_id", "balance", "margin_used",
                 "margin_available", "unrealized_pl", "currency"),
    "positions": ("broker_account_ext_id", "instrument_ext_id",
                  "units_long", "units_short", "avg_price_long",
                  "avg_price_short"),
    # N-O1 refinement (ITRGA-REV-V2-BE-9-INT-001 §3): the orders canon
    # hashes the SUBSTANTIVE payload projection only (the design's
    # provider-named fields), never the verbatim payload — a provider
    # cannot flip run digests by smuggling a retrieval-volatile field
    # into the payload blob. The verbatim payload still lands in the
    # projection row (the lawful storage site); only the CANON excludes it.
    "orders": ("order_ext_id", "broker_account_ext_id", "order_state_ext",
               "payload_substantive"),
    "fills": ("transaction_ext_id", "broker_account_ext_id", "tx_type_ext",
              "instrument_ext_id", "units", "price", "tx_time_ext"),
    "instrument_permissions": ("broker_account_ext_id",
                               "instrument_ext_id", "visibility",
                               "display_name"),
}
CANON_MODEL_ORDER = ("accounts", "balances", "positions", "orders",
                     "fills", "instrument_permissions")
CANON_SORT_KEYS = {
    "accounts": ("broker_account_ext_id",),
    "balances": ("broker_account_ext_id",),
    "positions": ("broker_account_ext_id", "instrument_ext_id"),
    "orders": ("broker_account_ext_id", "order_ext_id"),
    "fills": ("broker_account_ext_id", "transaction_ext_id"),
    "instrument_permissions": ("broker_account_ext_id",
                               "instrument_ext_id"),
}


# The substantive order-payload projection (N-O1): provider-named fields
# from the design S1.2 list — type / units(volume) / price / time-in-force.
ORDER_PAYLOAD_SUBSTANTIVE = ("type", "volume", "units", "price",
                             "time_in_force", "symbol")


def _order_payload_substantive(payload: dict) -> dict:
    return {k: payload[k] for k in ORDER_PAYLOAD_SUBSTANTIVE
            if k in payload}


def canonical_digest(payload_set: dict) -> str:
    """S4.1 verbatim: allow-list projection, natural-key sort, fixed model
    order, JSON canonical encoding. Unknown/volatile fields excluded by
    construction (the allow-list IS the law). Orders: the substantive
    payload projection only (N-O1 refinement)."""
    canon: list = []
    for model in CANON_MODEL_ORDER:
        fields = CANON_FIELDS[model]
        records = payload_set.get(model, [])
        if model == "orders":
            records = [
                {**{k: r[k] for k in ("order_ext_id",
                                      "broker_account_ext_id",
                                      "order_state_ext") if k in r},
                 "payload_substantive":
                     _order_payload_substantive(r.get("payload", {}))}
                for r in records
            ]
        projected = [
            {k: r[k] for k in fields if k in r}
            for r in records
        ]
        projected.sort(key=lambda r: tuple(
            str(r.get(k, "")) for k in CANON_SORT_KEYS[model]))
        canon.append({"model": model, "records": projected})
    encoded = json.dumps(canon, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=False, default=str)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


async def _audit(session: AsyncSession, action: str, *, details: dict,
                 mode: str, operator_id: str, correlation_id: str | None,
                 resource_id: str | None = None) -> None:
    await V2AuditRepository(session).append(V2AuditEventCreate(
        domain=_DOMAIN, action=action, actor_id=operator_id,
        actor_type="operator", mode=mode, resource_type="broker_sync",
        resource_id=resource_id, details=details, operator_id=operator_id,
        correlation_id=correlation_id))


async def run_sync(session: AsyncSession, *, provider, provenance_expect: dict,
                   actor_id: str, mode: str,
                   correlation_id: str | None) -> dict:
    """Execute one operator-initiated sync (T-15).

    Fetch phase (pure-read, in memory) -> validate -> single-transaction
    landing. Any refusal in fetch => a lineage row with the typed outcome
    and ZERO projection rows.
    """
    now_iso = datetime.now(timezone.utc).isoformat()
    origin = ORIGIN_FLOOR_ISO  # T-20 N-4: origin fact recorded on the row
    pages: dict = {}
    page_counts: dict = {}

    async def _refused(exc: BrokerRefused) -> dict:
        run = V2BrokerSyncRun(
            provider_id=provenance_expect["provider_id"],
            scope={"models": list(CANON_MODEL_ORDER)},
            outcome=("partial_refused"
                     if exc.refusal_class == "broker.payload.invalid"
                     or pages else "failed"),
            page_counts=page_counts, origin_basis=origin,
            inputs_hash=hashlib.sha256(
                json.dumps(provenance_expect, sort_keys=True)
                .encode()).hexdigest(),
            result_digest="", refusal={"class": exc.refusal_class,
                                       "reasons": exc.reasons},
            actor_id=actor_id, data_class=_DATA_CLASS, mode=mode,
            operator_id=actor_id, correlation_id=correlation_id)
        session.add(run)
        await session.flush()
        await _audit(session, "broker.sync.refused",
                     details={"class": exc.refusal_class,
                              "reasons": exc.reasons[:4]},
                     mode=mode, operator_id=actor_id,
                     correlation_id=correlation_id, resource_id=run.id)
        await session.commit()  # durable refusal (C-1 law)
        return {"outcome": run.outcome, "sync_run_id": run.id,
                "refusal_class": exc.refusal_class,
                "reasons": exc.reasons}

    # --- fetch phase: everything in memory, nothing lands ---------------------
    try:
        accounts = await provider.read_accounts()
        summary = await provider.read_account_summary()
        positions = await provider.read_positions()
        orders = await provider.read_orders()
        instruments = await provider.read_instrument_permissions()
        from app.v2.broker_read.providers.exness_mt5 import history_windows
        fills: list = []
        windows = history_windows(origin, now_iso)
        for i, (w_start, w_end) in enumerate(windows):
            page = await provider.read_transactions(w_start, w_end, i)
            fills.extend(page.records)
        pages = {
            "accounts": [dict(r) for r in accounts.records],
            "balances": [dict(r) for r in summary.records],
            "positions": [dict(r) for r in positions.records],
            "orders": [dict(r) for r in orders.records],
            "fills": [dict(r) for r in fills],
            "instrument_permissions": [dict(r) for r in
                                       instruments.records],
        }
        page_counts = {k: len(v) for k, v in pages.items()}
        prov = accounts.provenance
    except BrokerRefused as exc:
        return await _refused(exc)

    digest = canonical_digest(pages)

    # --- landing phase: single transaction --------------------------------------
    run = V2BrokerSyncRun(
        provider_id=prov.provider_id,
        scope={"models": list(CANON_MODEL_ORDER)}, outcome="complete",
        page_counts=page_counts, origin_basis=origin,
        inputs_hash=hashlib.sha256(json.dumps(
            provenance_expect, sort_keys=True).encode()).hexdigest(),
        result_digest=digest, refusal=None, actor_id=actor_id,
        data_class=_DATA_CLASS, mode=mode, operator_id=actor_id,
        correlation_id=correlation_id)
    session.add(run)
    await session.flush()

    common = {"provider_id": prov.provider_id, "sync_run_id": run.id,
              "server_hostname": prov.server_hostname,
              "fetched_at_basis": prov.fetched_at,
              "data_class": _DATA_CLASS, "mode": mode,
              "operator_id": actor_id, "correlation_id": correlation_id}

    for r in pages["accounts"]:
        newest = (await session.execute(
            select(V2BrokerAccount)
            .where(V2BrokerAccount.broker_account_ext_id
                   == r["broker_account_ext_id"])
            .order_by(V2BrokerAccount.record_seq.desc()))).scalars().first()
        session.add(V2BrokerAccount(
            broker_account_ext_id=r["broker_account_ext_id"],
            record_seq=1 if newest is None else newest.record_seq + 1,
            supersedes=newest.id if newest is not None else None,
            alias=r["alias"], currency=r["currency"],
            environment=r["environment"],
            read_only_login=bool(r.get("read_only_login", False)),
            **common))
    for r in pages["balances"]:
        session.add(V2BrokerBalance(
            broker_account_ext_id=r["broker_account_ext_id"],
            balance=r["balance"], margin_used=r["margin_used"],
            margin_available=r["margin_available"],
            unrealized_pl=r["unrealized_pl"], currency=r["currency"],
            **common))
    for r in pages["positions"]:
        session.add(V2BrokerPosition(
            broker_account_ext_id=r["broker_account_ext_id"],
            instrument_ext_id=r["instrument_ext_id"],
            units_long=r["units_long"], units_short=r["units_short"],
            avg_price_long=r["avg_price_long"],
            avg_price_short=r["avg_price_short"], **common))
    for r in pages["orders"]:
        session.add(V2BrokerOrder(
            order_ext_id=r["order_ext_id"],
            broker_account_ext_id=r["broker_account_ext_id"],
            order_state_ext=r["order_state_ext"], payload=r["payload"],
            **common))
    reused = 0
    for r in pages["fills"]:
        existing = (await session.execute(
            select(V2BrokerFill).where(
                V2BrokerFill.provider_id == prov.provider_id,
                V2BrokerFill.broker_account_ext_id
                == r["broker_account_ext_id"],
                V2BrokerFill.transaction_ext_id
                == r["transaction_ext_id"]))).scalar_one_or_none()
        if existing is not None:
            reused += 1
            continue
        session.add(V2BrokerFill(
            broker_account_ext_id=r["broker_account_ext_id"],
            transaction_ext_id=r["transaction_ext_id"],
            tx_type_ext=r["tx_type_ext"],
            instrument_ext_id=r["instrument_ext_id"], units=r["units"],
            price=r["price"], tx_time_ext=r["tx_time_ext"], **common))
    for r in pages["instrument_permissions"]:
        session.add(V2BrokerInstrumentPermission(
            broker_account_ext_id=r["broker_account_ext_id"],
            instrument_ext_id=r["instrument_ext_id"],
            visibility=r["visibility"], display_name=r["display_name"],
            **common))
    await session.flush()
    if reused:
        await _audit(session, "broker.fill.reused",
                     details={"skipped": reused}, mode=mode,
                     operator_id=actor_id, correlation_id=correlation_id,
                     resource_id=run.id)
    await _audit(session, "broker.sync.completed",
                 details={"page_counts": page_counts,
                          "result_digest": digest},
                 mode=mode, operator_id=actor_id,
                 correlation_id=correlation_id, resource_id=run.id)
    return {"outcome": "complete", "sync_run_id": run.id,
            "result_digest": digest, "page_counts": page_counts,
            "fills_reused": reused, "pages": pages}
