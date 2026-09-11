"""BE-12E reconciliation engine (BO-V2-BE12E-001 §1.c).

READ-ONLY BOUNDARY: imports BE-9 projections read-only; converts money
facts through THE locus only (§1.b.4); writes ONLY its own evidence
ledger.

SCOPE-OF-PARITY (closed, enumerated at design commit):
  (1) fill parity — every live_exec fill event's substantive money
      facts (price) canonical-compare against the projected BE-9 fill
      for the same correlation ref, where such a projection stands;
      live_exec fills lacking a projected counterpart are enumerated
      as drift facts (`fill_unprojected`);
  (2) position parity — projected position money facts (open_price)
      are canonicalizable and enumerated (count witnessed); position
      quantities (volume) ride the standing exact string-decimal
      discipline, NOT the money locus (non-money law, §1.b.3);
  (3) ledger consistency — every modify event names a standing
      submission; every fill event names a standing submission
      (`ledger_orphan` drift facts otherwise).
Nothing ad-hoc; nothing outside these three dimensions is compared.

C-2 CLEAN-RUNS-EVIDENCED LAW: EVERY run writes exactly ONE row — clean
runs included. Zero rows = defect; >1 = defect. NO VALVE — a report
never transitions; correction = a new run, never an edit.
"""

from __future__ import annotations

import hashlib
import json
from typing import Final
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.v2_broker_read import V2BrokerFill, V2BrokerPosition
from app.db.models.v2_live_exec_modify import V2LiveExecModifyEvent
from app.db.models.v2_live_exec_reconciliation import (
    V2LiveExecReconciliation,
)
from app.db.models.v2_live_exec_submission import (
    V2LiveExecFillEvent,
    V2LiveExecSubmission,
)
from app.v2.live_exec.reconcile.money import (
    MoneyNotCanonicalizable,
    to_canonical_money,
)

# Closed outcome vocabulary (§1.c.3; table CHECK mirrors it).
RECON_OUTCOMES: Final = ("clean", "parity_break")

# Closed drift-fact kinds (enumerated at design commit).
DRIFT_FACT_KINDS: Final = ("fill_price_mismatch", "fill_unprojected",
                           "position_money_uncanonical", "ledger_orphan")


def _canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      default=str)


def reconciliation_digest(row_facts: dict) -> str:
    """R-3.1 per-world register-facing digest (coupon recomputes)."""
    return hashlib.sha256(_canonical(row_facts).encode("utf-8")).hexdigest()


async def run_reconciliation(
    session: AsyncSession, *, actor_id: str, mode: str, operator_id: str,
    correlation_id: str | None = None,
) -> V2LiveExecReconciliation:
    """ONE operator-initiated run => exactly ONE evidence row."""
    drift_facts: list[dict] = []
    instruments: set[str] = set()

    # (1) fill parity vs projection (money via THE locus only)
    lx_fills = list((await session.execute(
        select(V2LiveExecFillEvent))).scalars().all())
    projected = {f.fill_ext_id: f for f in (await session.execute(
        select(V2BrokerFill))).scalars().all()}
    for fill in lx_fills:
        payload = fill.fill_payload or {}
        if payload.get("symbol"):
            instruments.add(str(payload["symbol"]))
        counterpart = projected.get(str(payload.get("deal_id")))
        if counterpart is None:
            drift_facts.append({
                "kind": "fill_unprojected",
                "fill_event_id": fill.id,
                "correlation_ref": fill.correlation_ref})
            continue
        # CR-1 (V2-BE12E-DEL-003, ridden by DA election): an ABSENT
        # price is a drift fact, never a silent zero — absence surfaces
        # through the existing fill_price_mismatch-with-note mechanism
        # (the late-binding path the uncanonicalizable arm uses);
        # the closed kinds stay 4.
        if "price" not in payload:
            drift_facts.append({
                "kind": "fill_price_mismatch",
                "fill_event_id": fill.id,
                "note": "price absent from fill payload -"
                        " absence is a drift fact, never a zero"})
            continue
        try:
            if not (to_canonical_money(payload["price"])
                    == to_canonical_money(counterpart.price)):
                drift_facts.append({
                    "kind": "fill_price_mismatch",
                    "fill_event_id": fill.id,
                    "live_exec": to_canonical_money(payload["price"]),
                    "projection": to_canonical_money(counterpart.price)})
        except MoneyNotCanonicalizable as refused:
            drift_facts.append({
                "kind": "fill_price_mismatch",
                "fill_event_id": fill.id,
                "note": f"uncanonicalizable: {refused.reason}"})

    # (2) position parity: money facts canonicalizable + enumerated
    positions = list((await session.execute(
        select(V2BrokerPosition))).scalars().all())
    for position in positions:
        if position.symbol_ext:
            instruments.add(str(position.symbol_ext))
        try:
            to_canonical_money(position.open_price)
        except MoneyNotCanonicalizable:
            drift_facts.append({
                "kind": "position_money_uncanonical",
                "position_id": position.id})

    # (3) ledger consistency (orphans)
    submission_ids = {s.id for s in (await session.execute(
        select(V2LiveExecSubmission))).scalars().all()}
    for fill in lx_fills:
        if fill.submission_id not in submission_ids:
            drift_facts.append({"kind": "ledger_orphan",
                                "table": "fill_event", "id": fill.id})
    for act in (await session.execute(
            select(V2LiveExecModifyEvent))).scalars().all():
        if act.submission_id not in submission_ids:
            drift_facts.append({"kind": "ledger_orphan",
                                "table": "modify_event", "id": act.id})

    outcome = "clean" if not drift_facts else "parity_break"
    scope = {"world": mode,
             "instrument_set": sorted(instruments),
             "window": {"basis": "full-ledger",
                        "fills": len(lx_fills),
                        "positions": len(positions)}}
    row_facts = {"scope": scope, "outcome": outcome,
                 "drift_facts": drift_facts if drift_facts else None,
                 "actor_id": actor_id, "mode": mode,
                 "operator_id": operator_id}
    row = V2LiveExecReconciliation(
        id=str(uuid4()), scope=scope, outcome=outcome,
        drift_facts=drift_facts if drift_facts else None,
        digest=reconciliation_digest(row_facts),
        actor_id=actor_id, data_class="evidence", mode=mode,
        operator_id=operator_id, correlation_id=correlation_id)
    session.add(row)
    await session.flush()
    return row
