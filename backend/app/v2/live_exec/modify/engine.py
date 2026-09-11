"""BE-12C cancel/modify engine (BO-V2-BE12C-001 §1.a–§1.c).

THE VERB LAW: the capability map arrives by CITED READ from the landed
adapter (through the boundary's `adapter_capability_map()`) — never
handwritten. A verb the adapter cannot evidence does not exist.
POSITION verbs are out of scope by charter: no position modify; a close
is a NEW opposite submission under 12B law.

UNKNOWN-STATE SEMANTICS (§1.c): governance default is FAIL-CLOSED
quarantine-hold — the machine never issues cancel/modify on its own
initiative (N4/N-O11 law). Cancel-on-unknown is an OPERATOR-INITIATED
recovery act: it executes ONLY under an explicit operator election
surfaced in the request and recorded on the row. An `unknown_outcome`
answer to that act escalates typed (`unknown_escalate` — the ARTIFACT;
the incident WORKFLOW is 12E's build, absent here by order).

APPEND-ONLY LAW: every act persists exactly one immutable row; parent
submission/fill rows are never mutated. Idempotency: same
(submission, verb, payload digest) => `duplicate_modify_event` with the
standing row cited; an act never re-fires.
"""

from __future__ import annotations

import hashlib
import json
from typing import Final
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.v2_live_exec_modify import V2LiveExecModifyEvent
from app.db.models.v2_live_exec_submission import V2LiveExecSubmission
from app.v2.live_exec.intents import LiveExecRefused

# Closed vocabularies (enumerated at design commit; coupon-pinned).
MODIFY_VERBS: Final = ("cancel", "modify")
ACT_OUTCOMES: Final = ("applied", "refused_terminal", "unknown_outcome",
                       "unknown_escalate")
OPERATOR_ELECTIONS: Final = ("standard", "cancel_on_unknown")
# CR-1 (ITRGA-REV-V2-BE12C-001): the tuple is the VOCABULARY UNION of
# act-refusal ids AND act-outcome nouns (LOW-1 re-homed by documentation:
# `cancel_refused_terminal`/`cancel_on_unknown_applied`/
# `cancel_unknown_outcome` are outcome-noun citizens seeded by the BO's
# own SS1.a mixed listing; they are never raised as refusals). The two
# NEW refusal ids close findings DEL-001 (weld) and DEL-002 (allowlist).
MODIFY_REFUSALS: Final = (
    "submission_not_found", "modify_not_supported_state",
    "duplicate_modify_event", "cancel_refused_terminal",
    "cancel_on_unknown_applied", "cancel_unknown_outcome",
    "unknown_escalate", "act_target_mismatch",
    "act_payload_field_not_supported")

# Submission postures where an act is meaningful: the terminal contract
# applies cancel/modify to PENDING orders; UNKNOWN postures admit ONLY
# the elected cancel-on-unknown recovery act.
_ACTIONABLE_STATES: Final = ("accepted", "requote")
_UNKNOWN_STATES: Final = ("no_answer", "quarantined_unknown")
_TERMINAL_STATES: Final = ("rejected",)


def _canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      default=str)


def act_identity(submission_id: str, verb: str, payload: dict) -> str:
    """Idempotency anchor: same (submission, verb, payload digest)
    computes the same identity; schema-fatal at the unique index."""
    return hashlib.sha256(_canonical({
        "submission_id": submission_id, "verb": verb, "payload": payload,
    }).encode("utf-8")).hexdigest()[:64]


def require_verb_capability(verb: str, capability_map: dict) -> dict:
    """The verb law gate: the ADAPTER-CITED map must evidence the verb.

    The map arrives from `adapter_capability_map()` (a cited read of the
    landed adapter object); a verb missing or unsupported there answers
    `modify_not_supported_state` — it does not exist in 12C.
    """
    spec = capability_map.get(verb)
    if not spec or not spec.get("supported"):
        raise LiveExecRefused("modify_not_supported_state", [
            {"failing": "verb", "asked": verb,
             "note": "the landed adapter capability map does not"
                     " evidence this verb (BO-V2-BE12C-001 SS1.a)"}])
    return spec


def require_actionable(submission: V2LiveExecSubmission, verb: str,
                       operator_election: str) -> str:
    """Posture gate + the §1.c election law. Returns the admitted
    posture class ('pending' | 'unknown_elected')."""
    state = submission.terminal_state
    if state in _ACTIONABLE_STATES:
        return "pending"
    if state in _UNKNOWN_STATES:
        if verb == "cancel" and operator_election == "cancel_on_unknown":
            return "unknown_elected"
        # QUARANTINE-HOLD default: no auto-acts; modify never applies to
        # an unknown posture; cancel without the election refuses.
        raise LiveExecRefused("modify_not_supported_state", [
            {"failing": "terminal_state", "observed": state,
             "note": "unknown posture holds in quarantine; cancel-on-"
                     "unknown requires the explicit operator election"
                     " (governance default FAIL-CLOSED, N4/N-O11 law)"}])
    # terminal states (rejected) and anything else: no act exists
    raise LiveExecRefused("modify_not_supported_state", [
        {"failing": "terminal_state", "observed": state,
         "note": "submission is in a terminal state; cancel/modify"
                 " applies to pending orders only (adapter contract)"}])


def require_act_payload(verb: str, spec: dict, submission,
                        request_payload: dict,
                        admitted_posture: str) -> dict:
    """CR-1 R1 laws (V2-BE12C-DEL-001 + DEL-002) — the corridor's
    input-side arms, BEFORE the doorway; refusals are NON-FIRING (the
    terminal is never reached, no row persists).

    THE WELD LAW (DEL-001): when the submission carries a
    `server_ack_ref`, the terminal-bound ticket (`order`) MUST equal it
    — the addressed submission and the acted-on terminal order are ONE
    object or the act refuses `act_target_mismatch`. When the ack is
    absent (unknown posture), a body-supplied ticket is lawful ONLY on
    the elected cancel-on-unknown path (`admitted_posture ==
    'unknown_elected'` — already posture-gated by require_actionable);
    on that path the operator's ticket is the recovery target by
    definition and rides recorded on the immutable row.

    THE ALLOWLIST LAW (DEL-002): the terminal-bound payload is PROJECTED
    onto the CITED capability spec — `cancel` admits exactly the ticket
    key; `modify` admits ticket + spec["fields"] (read from the cited
    map, never hand-carved). Any other key refuses
    `act_payload_field_not_supported`.
    """
    ticket = request_payload.get("order")
    ack = submission.server_ack_ref
    if ack is not None:
        if ticket is None or str(ticket) != str(ack):
            raise LiveExecRefused("act_target_mismatch", [
                {"failing": "order", "asked": ticket,
                 "welded_target": ack,
                 "note": "the addressed submission and the terminal"
                         " ticket must be ONE object (weld law,"
                         " V2-BE12C-DEL-001 R1)"}])
    elif admitted_posture != "unknown_elected":
        raise LiveExecRefused("act_target_mismatch", [
            {"failing": "order",
             "note": "no server ack stands and the posture is not the"
                     " elected recovery path - no lawful target exists"}])
    elif ticket is None:
        raise LiveExecRefused("act_target_mismatch", [
            {"failing": "order",
             "note": "elected recovery requires the operator-supplied"
                     " ticket"}])
    allowed = {"order"}
    if verb == "modify":
        allowed |= set(spec.get("fields", ()))
    foreign = sorted(set(request_payload) - allowed)
    if foreign:
        raise LiveExecRefused("act_payload_field_not_supported", [
            {"failing": "request_payload", "foreign_keys": foreign,
             "allowed": sorted(allowed),
             "note": "payload projected onto the cited capability"
                     " (allowlist law, V2-BE12C-DEL-002 R1); supported"
                     " fields come from the adapter map, never a"
                     " hand-carved list"}])
    return {key: request_payload[key] for key in request_payload}


async def persist_modify_event(
    session: AsyncSession, *, submission: V2LiveExecSubmission,
    verb: str, request_payload: dict, act_answer: dict,
    operator_election: str, actor_id: str, mode: str, operator_id: str,
    correlation_id: str | None = None,
) -> V2LiveExecModifyEvent:
    """Persist ONE immutable act row, born complete (LAW-BORDER-01
    lesson structural). Duplicate acts refuse typed with the standing
    row cited. An elected cancel answering `unknown_outcome` is
    persisted as `unknown_escalate` — the typed escalation ARTIFACT
    (the 12E workflow does not exist here by order)."""
    identity = act_identity(submission.id, verb, request_payload)
    existing = (await session.execute(
        select(V2LiveExecModifyEvent)
        .where(V2LiveExecModifyEvent.act_identity == identity)
    )).scalars().first()
    if existing is not None:
        raise LiveExecRefused("duplicate_modify_event", [
            {"failing": "act_identity",
             "standing_modify_event_id": existing.id,
             "standing_outcome": existing.outcome,
             "note": "an act never re-fires (R-3.3;"
                     " BO-V2-BE12C-001 SS1.b)"}])
    outcome = act_answer["outcome"]
    if (operator_election == "cancel_on_unknown"
            and outcome == "unknown_outcome"):
        outcome = "unknown_escalate"
    row = V2LiveExecModifyEvent(
        id=str(uuid4()), submission_id=submission.id,
        intent_id=submission.intent_id, verb=verb,
        act_identity=identity, request_payload=request_payload,
        outcome=outcome, raw_note=act_answer.get("raw_note"),
        correlation_ref=submission.server_ack_ref,
        operator_election=operator_election,
        actor_id=actor_id, data_class="simulated", mode=mode,
        operator_id=operator_id, correlation_id=correlation_id)
    session.add(row)
    await session.flush()
    return row
