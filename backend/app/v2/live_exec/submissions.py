"""BE-12B submission chassis (BO-V2-BE12B-001 §1.c).

The submit writer is migrate-gated: the input intent must EXIST, be
eligible per the 12A engines (caller-supplied evaluation), AND pass the
PRACTICE lane door. Idempotency is 12A-inherited plus schema:
uq(intent_id) on the submission table — a submitted intent never
re-submits (typed `duplicate_submission`, standing row cited).
Submission events persist under the zero-UPDATE law: rows are born
complete with their terminal answer (the LAW-BORDER-01 lesson is
structural here from birth).
"""

from __future__ import annotations

import hashlib
import json
from typing import Final
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.v2_live_exec import V2LiveExecIntent
from app.db.models.v2_live_exec_submission import V2LiveExecSubmission
from app.v2.live_exec.intents import LXE_VERSION, PXS_VERSION, LiveExecRefused

# Closed refusal vocabulary for this module (practice-lane citizens).
SUBMISSION_REFUSALS: Final = ("intent_not_found", "duplicate_submission")

# Terminal states that transition to quarantine at persistence
# (BE-8 S2.4 preimage law: no_answer => quarantined_unknown, a STATE).
_QUARANTINE_ON: Final = ("no_answer",)


def _canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      default=str)


def submission_digest(intent_id: str, order_request: dict,
                      terminal_state: str) -> str:
    """N-O13 per-world digest over the submission facts."""
    return hashlib.sha256(_canonical({
        "intent_id": intent_id, "order_request": order_request,
        "terminal_state": terminal_state,
        "versions": {"pxs": PXS_VERSION, "lxe": LXE_VERSION},
    }).encode("utf-8")).hexdigest()


async def require_intent(session: AsyncSession,
                         intent_id: str) -> V2LiveExecIntent:
    """The submit writer's first gate: the intent row must exist."""
    intent = (await session.execute(
        select(V2LiveExecIntent).where(V2LiveExecIntent.id == intent_id)
    )).scalars().first()
    if intent is None:
        raise LiveExecRefused("intent_not_found", [
            {"failing": "intent_id",
             "note": "no registered intent carries this id"}])
    return intent


async def persist_submission(
    session: AsyncSession, *, intent: V2LiveExecIntent,
    order_request: dict, terminal_answer: dict,
    actor_id: str, mode: str, operator_id: str,
    correlation_id: str | None = None,
) -> V2LiveExecSubmission:
    """Persist ONE immutable submission row, born complete.

    Duplicate (the intent already carries a submission) refuses typed
    with the standing row cited. `no_answer` terminal states persist as
    `quarantined_unknown` — quarantine is a STATE the record is born
    in, never an exception from the seam.
    """
    existing = (await session.execute(
        select(V2LiveExecSubmission)
        .where(V2LiveExecSubmission.intent_id == intent.id)
    )).scalars().first()
    if existing is not None:
        raise LiveExecRefused("duplicate_submission", [
            {"failing": "intent_id",
             "standing_submission_id": existing.id,
             "standing_terminal_state": existing.terminal_state,
             "note": "a submitted intent never re-submits (R-3.3;"
                     " BO-V2-BE12B-001 SS1.c)"}])
    terminal_state = terminal_answer["terminal_state"]
    if terminal_state in _QUARANTINE_ON:
        terminal_state = "quarantined_unknown"
    row = V2LiveExecSubmission(
        id=str(uuid4()), intent_id=intent.id, lane="practice",
        terminal_state=terminal_state,
        server_ack_ref=terminal_answer.get("server_ack_ref"),
        raw_note=terminal_answer.get("raw_note"),
        order_request=order_request,
        digest=submission_digest(intent.id, order_request, terminal_state),
        actor_id=actor_id, data_class="simulated", mode=mode,
        operator_id=operator_id, correlation_id=correlation_id)
    session.add(row)
    await session.flush()
    return row
