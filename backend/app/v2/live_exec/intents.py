"""BE-12A intent engine (BO-V2-BE12A-001 §1.b).

Intent chassis: uuid surrogate id; idempotency key (duplicate refusal
typed); requested basis id; posture field; operator-actor + step-up
reference SHAPE on confirm-class writes (V2-TD-29 adopted line: SECOND
FACTOR, not SECOND ACTOR). Digest per N-O13 per-world over
(requested_basis_id, payload, versions) — pxs-1.0.0 bound surface;
pins named by bytes. No submission verb exists in this module or this
sub-band (12B scope).
"""

from __future__ import annotations

import hashlib
import json
from typing import Final
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.v2_live_exec import V2LiveExecIntent

# Version surface (BO §1.b): pxs consumed AS-IS (compver-pinned, BE-8);
# lxe is the 12A engine name — its compver row arrives with a later
# sub-band's BO (12A carries NO compver row by order).
PXS_VERSION: Final = "pxs-1.0.0"
LXE_VERSION: Final = "lxe-1.0.0"
LXE_ENGINE_TUPLE: Final = (PXS_VERSION, LXE_VERSION)

# Closed intent record states (wording law: state nouns only).
INTENT_STATES: Final = ("registered",)

# Closed refusal vocabulary for this module.
INTENT_REFUSALS: Final = ("duplicate_intent", "step_up_reference_absent")


class LiveExecRefused(Exception):
    """Typed live_exec refusal; reason from a closed per-module set."""

    def __init__(self, reason: str, notes: list[dict] | None = None):
        self.reason = reason
        self.notes = notes or []
        super().__init__(reason)


def _canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      default=str)


def intent_digest(requested_basis_id: str, payload: dict) -> str:
    """N-O13 per-world digest; moves when basis or payload moves."""
    return hashlib.sha256(_canonical({
        "requested_basis_id": requested_basis_id,
        "payload": payload,
        "versions": {"pxs": PXS_VERSION, "lxe": LXE_VERSION},
    }).encode("utf-8")).hexdigest()


def require_step_up(step_up_ref: str | None) -> str:
    """Confirm-class writes carry the step-up reference or refuse.

    V2-TD-29 adopted line: the reference witnesses a SECOND FACTOR of
    the same operator; it does not (and in this deployment cannot)
    witness a second actor.
    """
    if not step_up_ref or not step_up_ref.strip():
        raise LiveExecRefused("step_up_reference_absent", [
            {"failing": "step_up_ref",
             "note": "confirm-class writes demand the second-factor"
                     " reference (R-3.4; V2-TD-29 adopted line)"}])
    return step_up_ref.strip()


async def register_intent(
    session: AsyncSession, *, idempotency_key: str,
    requested_basis_id: str, posture: str, payload: dict,
    actor_id: str, mode: str, operator_id: str,
    correlation_id: str | None = None,
    step_up_ref: str | None = None,
) -> V2LiveExecIntent:
    """Persist one immutable intent row; duplicates refuse typed.

    R1 (V2-BE12A-DEL-001, ITRGA-REV-V2-BE12A-001 §14): the validated
    step_up_ref enters HERE, in the constructor, BEFORE flush — the row
    is born complete and no UPDATE statement can ever exist against the
    zero-UPDATE regime. The api layer validates the shape first
    (require_step_up) and passes the result in.
    """
    existing = (await session.execute(
        select(V2LiveExecIntent)
        .where(V2LiveExecIntent.idempotency_key == idempotency_key)
    )).scalars().first()
    if existing is not None:
        raise LiveExecRefused("duplicate_intent", [
            {"failing": "idempotency_key",
             "standing_intent_id": existing.id,
             "note": "a live-exec intent never re-registers (R-3.3)"}])
    row = V2LiveExecIntent(
        id=str(uuid4()), idempotency_key=idempotency_key,
        requested_basis_id=requested_basis_id, posture=posture,
        payload=payload,
        digest=intent_digest(requested_basis_id, payload),
        record_state="registered", step_up_ref=step_up_ref,
        actor_id=actor_id,
        data_class="simulated", mode=mode, operator_id=operator_id,
        correlation_id=correlation_id)
    session.add(row)
    await session.flush()
    return row
