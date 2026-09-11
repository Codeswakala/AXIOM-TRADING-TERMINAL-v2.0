"""BE-9 health surface (design S7; BO T-14).

Three independent facts — terminal / reachability / freshness — GREEN
requires ALL THREE. Classifier-visible facts only: no payload, no
credential material, no vault path. The surface cannot assert what it
has not measured.
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.v2_broker_read import (
    V2BrokerAccount,
    V2BrokerDiscrepancy,
    V2BrokerSyncRun,
)

FRESHNESS_STALE_AFTER_HOURS = 24  # BO-settable fact threshold


def classify(terminal_state: str, reachability: str,
             freshness_age_hours: float | None) -> str:
    """The three-facts law. Closed outcome vocabulary."""
    if terminal_state != "logged_in":
        return "terminal_down"
    if reachability != "reachable":
        return "terminal_up_unreachable"
    if freshness_age_hours is None:
        return "reachable_no_data"
    if freshness_age_hours > FRESHNESS_STALE_AFTER_HOURS:
        return "reachable_stale"
    return "green"


async def health_facts(session: AsyncSession) -> dict:
    """Assemble the fact surface from durable state (no live probe here —
    probes are sync-time facts; this read reports what was measured)."""
    last_run = (await session.execute(
        select(V2BrokerSyncRun)
        .order_by(V2BrokerSyncRun.created_at.desc()))).scalars().first()
    last_complete = (await session.execute(
        select(V2BrokerSyncRun)
        .where(V2BrokerSyncRun.outcome == "complete")
        .order_by(V2BrokerSyncRun.created_at.desc()))).scalars().first()
    newest_acct = (await session.execute(
        select(V2BrokerAccount)
        .order_by(V2BrokerAccount.record_seq.desc()))).scalars().first()
    unowned = 0
    seen: set[str] = set()
    for row in (await session.execute(
            select(V2BrokerDiscrepancy)
            .order_by(V2BrokerDiscrepancy.discrepancy_id,
                      V2BrokerDiscrepancy.record_seq.desc()))).scalars():
        if row.discrepancy_id in seen:
            continue
        seen.add(row.discrepancy_id)
        if row.state in ("detected", "triaged"):
            unowned += 1

    freshness_hours = None
    if last_complete is not None:
        created = last_complete.created_at
        if created.tzinfo is None:
            created = created.replace(tzinfo=timezone.utc)
        freshness_hours = (
            datetime.now(timezone.utc) - created).total_seconds() / 3600

    terminal_state = "unknown"
    reachability = "unknown"
    if last_run is not None:
        if last_run.outcome == "complete":
            terminal_state, reachability = "logged_in", "reachable"
        elif last_run.refusal and last_run.refusal.get("class") == \
                "broker.terminal.unavailable":
            terminal_state, reachability = "not_running", "unknown"
        elif last_run.refusal and last_run.refusal.get("class") == \
                "broker.unavailable":
            terminal_state, reachability = "logged_in", "unreachable"

    return {
        "provider_id": last_run.provider_id if last_run else None,
        "environment": "practice",
        "terminal": terminal_state,
        "reachability": reachability,
        "freshness_age_hours": freshness_hours,
        "status": classify(terminal_state, reachability, freshness_hours),
        "last_sync_run": ({"id": last_run.id, "outcome": last_run.outcome,
                           "basis": str(last_run.created_at)}
                          if last_run else None),
        "last_success_basis": (str(last_complete.created_at)
                               if last_complete else None),
        "last_refusal_class": (last_run.refusal.get("class")
                               if last_run and last_run.refusal else None),
        "read_only_login_asserted": (bool(newest_acct.read_only_login)
                                     if newest_acct else None),
        "vault_state": "locked",  # unlocked only inside the request scope
        "unowned_discrepancies": unowned,
    }
