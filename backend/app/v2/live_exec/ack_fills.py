"""BE-12B ack + fill processing (BO-V2-BE12B-001 §1.d).

Terminal-returned acks are captured on the submission record at birth
({server_ack_ref, terminal_state} — submissions.py persists them).
This module carries the FILL side: events correlated to submissions by
(server_ack_ref | terminal_order_id), DE-DUPE anchored on fill-event
identity (BE-9 election-derived law — fills are never double-
attributed; the second sighting of the same fill event refuses typed
`duplicate_fill_event` with the standing id, and dies at schema on the
unique identity index even if the engine is bypassed).
"""

from __future__ import annotations

import hashlib
import json
from typing import Final
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.v2_live_exec_submission import (
    V2LiveExecFillEvent,
    V2LiveExecSubmission,
)
from app.v2.live_exec.intents import LiveExecRefused

# Closed correlation-basis vocabulary (schema CHECK mirrors it).
CORRELATION_BASES: Final = ("server_ack_ref", "terminal_order_id")

FILL_REFUSALS: Final = ("duplicate_fill_event",)


def _canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      default=str)


def fill_event_identity(correlation_basis: str, correlation_ref: str,
                        fill_payload: dict) -> str:
    """The dedupe anchor (BE-9 election-derived law): identity is the
    hash of the correlation ref + the substantive fill facts — a second
    sighting of the same fill computes the same identity and dies at
    the schema unique index."""
    substantive = {k: fill_payload.get(k) for k in (
        "deal_id", "order_id", "volume", "price", "time")}
    return hashlib.sha256(_canonical({
        "basis": correlation_basis, "ref": correlation_ref,
        "facts": substantive,
    }).encode("utf-8")).hexdigest()[:64]


async def persist_fill_event(
    session: AsyncSession, *, submission: V2LiveExecSubmission,
    correlation_basis: str, correlation_ref: str, fill_payload: dict,
    actor_id: str, mode: str, operator_id: str,
    correlation_id: str | None = None,
) -> V2LiveExecFillEvent:
    """Persist ONE fill event; the second sighting refuses typed with
    the standing id (fills are never double-attributed)."""
    identity = fill_event_identity(correlation_basis, correlation_ref,
                                   fill_payload)
    existing = (await session.execute(
        select(V2LiveExecFillEvent)
        .where(V2LiveExecFillEvent.fill_event_identity == identity)
    )).scalars().first()
    if existing is not None:
        raise LiveExecRefused("duplicate_fill_event", [
            {"failing": "fill_event_identity",
             "standing_fill_event_id": existing.id,
             "note": "second sighting of the same fill event"
                     " (dedupe anchor law, BE-9 election-derived)"}])
    row = V2LiveExecFillEvent(
        id=str(uuid4()), submission_id=submission.id,
        fill_event_identity=identity,
        correlation_basis=correlation_basis,
        correlation_ref=correlation_ref, fill_payload=fill_payload,
        actor_id=actor_id, data_class="simulated", mode=mode,
        operator_id=operator_id, correlation_id=correlation_id)
    session.add(row)
    await session.flush()
    return row
