"""BE-12A live-exec API (BO-V2-BE12A-001 §1.g authorized surface).

12A verbs: POST /live-exec/intents (register) · POST /evaluate ·
GET /intents. 12B verbs: POST /intents/{id}/submit · GET /submissions ·
GET /fills. The LIVE-lane door (`_actuation_door`) always refuses on
every world this band may lawfully field (activation instrument
nonexistent; funded posture absent) and its answer rides the register
envelope. The PRACTICE lane (12B) is the submit verb's door: it CAN
arm — PAPER mode + sealed practice vault under the R1 provisioning law
+ wired boundary + fresh basis — and refuses typed otherwise
(ITRGA-REV-V2-BE12B-001 finding V2-BE12B-DEL-001 closed by that law).
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.operator import Operator
from app.db.models.v2_live_exec import V2LiveExecIntent
from app.db.session import get_db_session
from app.v2.live_exec.eligibility import require_eligibility
from app.v2.live_exec.intents import (
    LiveExecRefused,
    register_intent,
    require_step_up,
)
from app.v2.live_exec.locks import (
    ActuationRefused,
    ActuationState,
    require_actuation,
)
from app.v2.live_exec.risk import evaluate_pre_trade_risk
from app.v2.rbac.dependencies import require_v2_permission

router = APIRouter(prefix="/live-exec", tags=["V2 Live Exec"])

RequireIntentWrite = Annotated[
    Operator, Depends(require_v2_permission("v2.live_exec.intent.write"))]
RequireEvaluateWrite = Annotated[
    Operator, Depends(require_v2_permission("v2.live_exec.evaluate.write"))]
RequireIntentsRead = Annotated[
    Operator, Depends(require_v2_permission("v2.live_exec.intents.read"))]
RequireSubmitWrite = Annotated[
    Operator, Depends(require_v2_permission("v2.live_exec.submit.write"))]
RequireSubmissionsRead = Annotated[
    Operator, Depends(require_v2_permission("v2.live_exec.submissions.read"))]
RequireFillsRead = Annotated[
    Operator, Depends(require_v2_permission("v2.live_exec.fills.read"))]
RequireModifyWrite = Annotated[
    Operator, Depends(require_v2_permission("v2.live_exec.modify.write"))]
RequireModifiesRead = Annotated[
    Operator, Depends(require_v2_permission("v2.live_exec.modifies.read"))]
RequireKillswitchArm = Annotated[
    Operator, Depends(require_v2_permission("v2.live_exec.killswitch.arm"))]
RequireKillswitchPull = Annotated[
    Operator, Depends(require_v2_permission("v2.live_exec.killswitch.pull"))]
RequireKillswitchClear = Annotated[
    Operator, Depends(require_v2_permission("v2.live_exec.killswitch.clear"))]
RequireKillswitchRead = Annotated[
    Operator, Depends(require_v2_permission("v2.live_exec.killswitch.read"))]
RequireActivationRead = Annotated[
    Operator, Depends(require_v2_permission("v2.live_exec.activation.read"))]
RequireActivationTemplateRead = Annotated[
    Operator, Depends(require_v2_permission(
        "v2.live_exec.activation.template.read"))]
RequireReconcileRun = Annotated[
    Operator, Depends(require_v2_permission("v2.live_exec.reconcile.run"))]
RequireReconcileRead = Annotated[
    Operator, Depends(require_v2_permission("v2.live_exec.reconcile.read"))]
RequireIncidentOpen = Annotated[
    Operator, Depends(require_v2_permission("v2.live_exec.incident.open"))]
RequireIncidentClose = Annotated[
    Operator, Depends(require_v2_permission("v2.live_exec.incident.close"))]
RequireIncidentRead = Annotated[
    Operator, Depends(require_v2_permission("v2.live_exec.incident.read"))]

# BE-12E §e.1 (BO-V2-BE12E-001; supersedes the 12D-era ordered line BY
# CITATION — the 12D exact-form pin moves to the 12E corpus): the
# HONESTY PAIR clause rides every envelope from this BO onward.
_REGISTER_LINE = ("BE-12E RECONCILIATION+INCIDENT |"
                  " LIVE=REGISTERED_LOCKED | funded account: NONE |"
                  " activation instrument: NOT IN FORCE |"
                  " LIVE real-network behavior: NOT PROVEN"
                  " (\u2260 FALSE)")


def _envelope(request: Request) -> dict:
    return {"mode": request.app.state.v2_mode,
            "register_line": _REGISTER_LINE,
            "correlation_id": getattr(request.state, "correlation_id", None),
            "timestamp": datetime.now(timezone.utc)}


def _refusal(request: Request, reason: str, notes: list[dict],
             status_code: int = 409):
    from fastapi.encoders import jsonable_encoder
    from fastapi.responses import JSONResponse
    return JSONResponse(status_code=status_code, content=jsonable_encoder({
        "refusal": {"reason": reason, "notes": notes},
        **_envelope(request)}))


class IntentRegisterRequest(BaseModel):
    idempotency_key: str = Field(min_length=1, max_length=128)
    requested_basis_id: str = Field(min_length=1, max_length=64)
    payload: dict
    step_up_ref: str | None = None


class IntentEvaluateRequest(BaseModel):
    account_present: bool
    account_posture_class: str | None = None
    instrument_mapped: bool
    session_open: bool
    basis_present: bool
    basis_age_hours: float | None = None
    max_age_hours: float
    quantity: str
    cited_price: str
    price_currency: str
    basis_currency: str
    margin_available: str


async def _actuation_door(request: Request,
                          session: AsyncSession) -> dict:
    """One reading of the lock inputs; the door's answer rides the
    envelope as a record of state (always a refusal before activation).

    12D (BO-V2-BE12D-001 SS1.b.4/SS1.c.3): L3 and L5 move from
    constructor constants to TABLE-BACKED FACT READERS over the real
    chain — the lock semantics and LOCK_ORDER are unchanged.
    """
    from app.v2.live_exec.activation.engine import (
        activation_instrument_rows,
    )
    from app.v2.live_exec.killswitch.engine import killswitch_engaged
    try:
        require_actuation(ActuationState(
            mode=request.app.state.v2_mode,
            credential_class=None,           # LIVE lane: no funded credential class exists
            activation_instrument_rows=(
                await activation_instrument_rows(session)),  # L3 fact
            funded_posture=False,            # R-6.3: no funded account
            killswitch_armed=await killswitch_engaged(session)))  # L5 fact
        return {"actuation": "unreachable_before_activation"}  # pragma: no cover
    except ActuationRefused as refused:
        return {"actuation_refusal": {
            "reason": refused.reason, "lock": refused.lock,
            "notes": refused.notes}}


@router.post("/intents")
async def api_register_intent(
    request: Request, body: IntentRegisterRequest,
    operator: RequireIntentWrite,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    """Register one immutable intent record (NO submission exists)."""
    try:
        # R1 (V2-BE12A-DEL-001): validate FIRST, then birth the row
        # complete — step_up_ref rides the constructor; no post-flush
        # mutation, no UPDATE, the zero-UPDATE guards never fire on the
        # lawful path.
        step_up = require_step_up(body.step_up_ref)
        row = await register_intent(
            session, idempotency_key=body.idempotency_key,
            requested_basis_id=body.requested_basis_id,
            posture="capability", payload=body.payload,
            actor_id=operator.username, mode=request.app.state.v2_mode,
            operator_id=operator.username,
            correlation_id=getattr(request.state, "correlation_id", None),
            step_up_ref=step_up)
        await session.commit()
    except LiveExecRefused as refused:
        await session.rollback()
        return _refusal(request, refused.reason, refused.notes)
    return {"intent": {"id": row.id, "digest": row.digest,
                       "record_state": row.record_state,
                       "posture": row.posture},
            **(await _actuation_door(request, session)),
            **_envelope(request)}


@router.post("/evaluate")
async def api_evaluate(
    request: Request, body: IntentEvaluateRequest,
    operator: RequireEvaluateWrite,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    """Eligibility + pre-trade risk as RECORDS OF STATE (no writes to
    any provider; no submission; the actuation door's typed refusal is
    carried in the envelope)."""
    try:
        eligibility = require_eligibility(
            account_present=body.account_present,
            account_posture_class=body.account_posture_class,
            instrument_mapped=body.instrument_mapped,
            session_open=body.session_open,
            basis_present=body.basis_present,
            basis_age_hours=body.basis_age_hours,
            max_age_hours=body.max_age_hours)
    except LiveExecRefused as refused:
        return _refusal(request, refused.reason, refused.notes)
    risk = evaluate_pre_trade_risk(
        quantity=body.quantity, cited_price=body.cited_price,
        price_currency=body.price_currency,
        basis_currency=body.basis_currency,
        margin_available=body.margin_available)
    return {"eligibility": eligibility, "risk": risk,
            **(await _actuation_door(request, session)),
            **_envelope(request)}


@router.get("/intents")
async def api_read_intents(
    request: Request, operator: RequireIntentsRead,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    limit: int = Query(default=100, ge=1, le=500),
):
    """Intent ledger reads (register-pinned envelope)."""
    rows = list((await session.execute(
        select(V2LiveExecIntent)
        .order_by(V2LiveExecIntent.created_at.desc())
        .limit(limit))).scalars().all())
    return {"intents": [
        {"id": r.id, "idempotency_key": r.idempotency_key,
         "requested_basis_id": r.requested_basis_id,
         "posture": r.posture, "digest": r.digest,
         "record_state": r.record_state} for r in rows],
        **_envelope(request)}


# --- BE-12B verbs (BO-V2-BE12B-001 SS1.c/SS1.d) -------------------------------------


class SubmitRequest(BaseModel):
    """Practice-lane submission ask. The lane is pinned server-side."""

    order_request: dict
    basis_age_hours: float | None = None


@router.post("/intents/{intent_id}/submit")
async def api_submit_intent(
    request: Request, intent_id: str, body: SubmitRequest,
    operator: RequireSubmitWrite,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    """The 12B submit writer: intent must exist, and the PRACTICE lane
    door must pass. The lane answer (pass or typed refusal) is the
    envelope's actuation record; on refusal NOTHING persists. On pass,
    the boundary speaks to the terminal via the sanctioned provider leg
    and the submission row is born complete with the terminal answer
    (no_answer => quarantined_unknown at persistence — a state).

    No credential material travels this API: the door reads only the
    vault RESOLUTION STATE (present/absent) from the sealed doorway.
    """
    from app.v2.live_exec.adapter_boundary import (
        BOUNDARY_STANCE,
        AdapterBoundaryRefused,
        practice_credential_state,
        submission_doorway,
    )
    from app.v2.live_exec.locks import (
        PracticeActuationRefused,
        PracticeActuationState,
    )
    from app.v2.live_exec.submissions import persist_submission, require_intent

    try:
        intent = await require_intent(session, intent_id)
    except LiveExecRefused as refused:
        return _refusal(request, refused.reason, refused.notes,
                        status_code=404)

    # ONE reading of the lane inputs (consistency ARM). The API never
    # holds a passphrase; the credential answer is a STATE STRING read
    # through the boundary (the one vault-naming doorway) — material
    # never reaches this module.
    lane_state = PracticeActuationState(
        lane="practice", mode=request.app.state.v2_mode,
        credential_state=practice_credential_state(),
        boundary_stance=BOUNDARY_STANCE,
        basis_age_hours=body.basis_age_hours)

    try:
        terminal_answer = submission_doorway(lane_state, body.order_request)
    except PracticeActuationRefused as refused:
        return _refusal(request, refused.reason, refused.notes,
                        status_code=409)
    except AdapterBoundaryRefused as refused:
        return _refusal(request, refused.reason, refused.notes,
                        status_code=503)

    try:
        row = await persist_submission(
            session, intent=intent, order_request=body.order_request,
            terminal_answer=terminal_answer,
            actor_id=operator.username, mode=request.app.state.v2_mode,
            operator_id=operator.username,
            correlation_id=getattr(request.state, "correlation_id", None))
        await session.commit()
    except LiveExecRefused as refused:
        await session.rollback()
        return _refusal(request, refused.reason, refused.notes)
    return {"submission": {"id": row.id, "intent_id": row.intent_id,
                           "terminal_state": row.terminal_state,
                           "server_ack_ref": row.server_ack_ref,
                           "digest": row.digest},
            **_envelope(request)}


@router.get("/submissions")
async def api_read_submissions(
    request: Request, operator: RequireSubmissionsRead,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    limit: int = Query(default=100, ge=1, le=500),
):
    """Submission ledger reads (register-pinned envelope)."""
    from app.db.models.v2_live_exec_submission import V2LiveExecSubmission
    rows = list((await session.execute(
        select(V2LiveExecSubmission)
        .order_by(V2LiveExecSubmission.created_at.desc())
        .limit(limit))).scalars().all())
    return {"submissions": [
        {"id": r.id, "intent_id": r.intent_id, "lane": r.lane,
         "terminal_state": r.terminal_state,
         "server_ack_ref": r.server_ack_ref,
         "digest": r.digest} for r in rows],
        **_envelope(request)}


@router.get("/fills")
async def api_read_fills(
    request: Request, operator: RequireFillsRead,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    limit: int = Query(default=100, ge=1, le=500),
):
    """Fill-event ledger reads (register-pinned envelope)."""
    from app.db.models.v2_live_exec_submission import V2LiveExecFillEvent
    rows = list((await session.execute(
        select(V2LiveExecFillEvent)
        .order_by(V2LiveExecFillEvent.created_at.desc())
        .limit(limit))).scalars().all())
    return {"fill_events": [
        {"id": r.id, "submission_id": r.submission_id,
         "fill_event_identity": r.fill_event_identity,
         "correlation_basis": r.correlation_basis,
         "correlation_ref": r.correlation_ref} for r in rows],
        **_envelope(request)}


# --- BE-12C verbs (BO-V2-BE12C-001 SS1.b/SS1.c) -------------------------------------


class ActRequest(BaseModel):
    """Cancel/modify act ask. `cancel_on_unknown=True` is the EXPLICIT
    operator election (§1.c law) — recorded on the row; without it an
    unknown-posture ask refuses (quarantine-hold default)."""

    request_payload: dict
    basis_age_hours: float | None = None
    cancel_on_unknown: bool = False


async def _act(request: Request, submission_id: str, verb: str,
               body: ActRequest, operator, session: AsyncSession):
    """Shared act path: door chain identical to the 12B submit."""
    from app.db.models.v2_live_exec_submission import V2LiveExecSubmission
    from app.v2.live_exec.adapter_boundary import (
        BOUNDARY_STANCE,
        AdapterBoundaryRefused,
        adapter_capability_map,
        cancel_doorway,
        modify_doorway,
        practice_credential_state,
    )
    from app.v2.live_exec.locks import (
        PracticeActuationRefused,
        PracticeActuationState,
    )
    from app.v2.live_exec.modify.engine import (
        persist_modify_event,
        require_actionable,
        require_verb_capability,
    )

    submission = (await session.execute(
        select(V2LiveExecSubmission)
        .where(V2LiveExecSubmission.id == submission_id))).scalars().first()
    if submission is None:
        return _refusal(request, "submission_not_found", [
            {"failing": "submission_id",
             "note": "no persisted submission carries this id"}],
            status_code=404)

    election = ("cancel_on_unknown" if body.cancel_on_unknown
                else "standard")
    try:
        # verb law: capability by CITED READ from the landed adapter
        spec = require_verb_capability(verb, adapter_capability_map())
        admitted = require_actionable(submission, verb, election)
        # CR-1 R1 (DEL-001 weld + DEL-002 allowlist): input-side arms
        # BEFORE the doorway — refusals are non-firing, no terminal
        # send, no row.
        from app.v2.live_exec.modify.engine import require_act_payload
        payload = require_act_payload(verb, spec, submission,
                                      body.request_payload, admitted)
    except LiveExecRefused as refused:
        return _refusal(request, refused.reason, refused.notes)

    lane_state = PracticeActuationState(
        lane="practice", mode=request.app.state.v2_mode,
        credential_state=practice_credential_state(),
        boundary_stance=BOUNDARY_STANCE,
        basis_age_hours=body.basis_age_hours)
    doorway = cancel_doorway if verb == "cancel" else modify_doorway
    try:
        act_answer = doorway(lane_state, payload)
    except PracticeActuationRefused as refused:
        return _refusal(request, refused.reason, refused.notes,
                        status_code=409)
    except AdapterBoundaryRefused as refused:
        return _refusal(request, refused.reason, refused.notes,
                        status_code=503)

    try:
        row = await persist_modify_event(
            session, submission=submission, verb=verb,
            request_payload=payload, act_answer=act_answer,
            operator_election=election, actor_id=operator.username,
            mode=request.app.state.v2_mode, operator_id=operator.username,
            correlation_id=getattr(request.state, "correlation_id", None))
        await session.commit()
    except LiveExecRefused as refused:
        await session.rollback()
        return _refusal(request, refused.reason, refused.notes)
    return {"modify_event": {
        "id": row.id, "submission_id": row.submission_id,
        "verb": row.verb, "outcome": row.outcome,
        "operator_election": row.operator_election,
        "act_identity": row.act_identity},
        **_envelope(request)}


@router.post("/submissions/{submission_id}/cancel")
async def api_cancel_submission(
    request: Request, submission_id: str, body: ActRequest,
    operator: RequireModifyWrite,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    """Cancel a pending (or elected-unknown) practice submission."""
    return await _act(request, submission_id, "cancel", body, operator,
                      session)


@router.post("/submissions/{submission_id}/modify")
async def api_modify_submission(
    request: Request, submission_id: str, body: ActRequest,
    operator: RequireModifyWrite,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    """Modify a pending practice submission (supported fields only)."""
    return await _act(request, submission_id, "modify", body, operator,
                      session)


@router.get("/modifies")
async def api_read_modifies(
    request: Request, operator: RequireModifiesRead,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    limit: int = Query(default=100, ge=1, le=500),
):
    """Modify-event ledger reads (register-pinned envelope)."""
    from app.db.models.v2_live_exec_modify import V2LiveExecModifyEvent
    rows = list((await session.execute(
        select(V2LiveExecModifyEvent)
        .order_by(V2LiveExecModifyEvent.created_at.desc())
        .limit(limit))).scalars().all())
    return {"modify_events": [
        {"id": r.id, "submission_id": r.submission_id, "verb": r.verb,
         "outcome": r.outcome, "operator_election": r.operator_election,
         "act_identity": r.act_identity} for r in rows],
        **_envelope(request)}


# --- BE-12D verbs (BO-V2-BE12D-001 SS1.b.3/SS1.c.4) ----------------------------------


class GovernorRequest(BaseModel):
    """Kill-switch governor ask. Confirm-rank: step-up mandatory."""

    step_up_ref: str | None = None


@router.get("/activation")
async def api_activation_state(
    request: Request, operator: RequireActivationRead,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    """The force-row state (zero-row => typed not-in-force shape on the
    envelope face, never an error). READ-ONLY; no writer route exists."""
    from app.v2.live_exec.activation.engine import activation_state_shape
    return {**(await activation_state_shape(session)),
            **_envelope(request)}


@router.get("/activation/template")
async def api_activation_template(
    request: Request, operator: RequireActivationTemplateRead,
):
    """The draft template body (version + hash echoed; hash recomputed
    from final bytes at every ask). READ-ONLY."""
    from app.v2.live_exec.activation.engine import (
        ACTIVATION_INSTRUMENT_TEMPLATE,
        TEMPLATE_VERSION,
        template_hash,
    )
    return {"template": ACTIVATION_INSTRUMENT_TEMPLATE,
            "template_version": TEMPLATE_VERSION,
            "template_hash": template_hash(),
            **_envelope(request)}


async def _governor(request: Request, verb: str, body: GovernorRequest,
                    operator, session: AsyncSession):
    from app.v2.live_exec.killswitch.engine import (
        governor_arm,
        governor_clear,
        governor_pull,
    )
    try:
        step_up = require_step_up(body.step_up_ref)
        actions = {"arm": governor_arm, "pull": governor_pull,
                   "clear": governor_clear}
        if verb == "arm":
            status = await actions[verb](
                session, actor_id=operator.username, step_up_ref=step_up,
                operator_id=operator.username,
                correlation_id=getattr(request.state, "correlation_id",
                                       None))
        else:
            status = await actions[verb](
                session, actor_id=operator.username, step_up_ref=step_up,
                operator_id=operator.username)
        await session.commit()
    except LiveExecRefused as refused:
        await session.rollback()
        return _refusal(request, refused.reason, refused.notes)
    return {"killswitch": {"status": status, "verb": verb},
            **_envelope(request)}


@router.post("/killswitch/arm")
async def api_killswitch_arm(
    request: Request, body: GovernorRequest,
    operator: RequireKillswitchArm,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    """Arm (operator-initiated; re-arm blocked until cleared)."""
    return await _governor(request, "arm", body, operator, session)


@router.post("/killswitch/pull")
async def api_killswitch_pull(
    request: Request, body: GovernorRequest,
    operator: RequireKillswitchPull,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    """Pull (armed only; anything else refuses typed)."""
    return await _governor(request, "pull", body, operator, session)


@router.post("/killswitch/clear")
async def api_killswitch_clear(
    request: Request, body: GovernorRequest,
    operator: RequireKillswitchClear,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    """THE single sanctioned clear path (no other clear exists)."""
    return await _governor(request, "clear", body, operator, session)


@router.get("/killswitch")
async def api_killswitch_state(
    request: Request, operator: RequireKillswitchRead,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    """Standing state (zero-row shape typed 'intact', never error)."""
    from app.v2.live_exec.killswitch.engine import (
        killswitch_engaged,
        killswitch_state,
    )
    status = await killswitch_state(session)
    return {"killswitch": {
        "status": status if status is not None else "intact",
        "engaged": await killswitch_engaged(session)},
        **_envelope(request)}


# --- BE-12E verbs (BO-V2-BE12E-001 SS1.c.6/SS1.d.3) ----------------------------------


class IncidentOpenRequest(BaseModel):
    """Confirm-rank open ask (SAL-4 + step-up on the sealed chain)."""

    severity: str
    instruments_pinned: list
    recovery_path: str = Field(min_length=1)
    step_up_ref: str | None = None


class IncidentCloseRequest(BaseModel):
    """Confirm-rank close ask (THE single sanctioned close path)."""

    step_up_ref: str | None = None


@router.post("/reconcile/run")
async def api_reconcile_run(
    request: Request, operator: RequireReconcileRun,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    """Operator-initiated reconciliation run (SAL-4; BO SS1.a.2 named
    exception: NO step-up — it writes only its own evidence ledger and
    actuates nothing; actor/operator carriage stands). Synchronous;
    returns the resulting row (C-2: exactly one row per run)."""
    from app.v2.live_exec.reconcile.engine import run_reconciliation
    row = await run_reconciliation(
        session, actor_id=operator.username,
        mode=request.app.state.v2_mode, operator_id=operator.username,
        correlation_id=getattr(request.state, "correlation_id", None))
    payload = {"reconciliation": {
        "id": row.id, "outcome": row.outcome, "scope": row.scope,
        "drift_facts": row.drift_facts, "digest": row.digest,
        "mode": row.mode}}
    await session.commit()
    return {**payload, **_envelope(request)}


@router.get("/reconcile/latest")
async def api_reconcile_latest(
    request: Request, operator: RequireReconcileRead,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    """Latest evidence row, or the typed zero-row shape (never error)."""
    from app.db.models.v2_live_exec_reconciliation import (
        V2LiveExecReconciliation,
    )
    row = (await session.execute(
        select(V2LiveExecReconciliation)
        .order_by(V2LiveExecReconciliation.created_at.desc())
        .limit(1))).scalars().first()
    if row is None:
        return {"reconciliation": "no_runs_recorded",
                **_envelope(request)}
    return {"reconciliation": {
        "id": row.id, "outcome": row.outcome, "scope": row.scope,
        "drift_facts": row.drift_facts, "digest": row.digest,
        "mode": row.mode}, **_envelope(request)}


@router.get("/reconcile/{reconciliation_id}")
async def api_reconcile_by_id(
    request: Request, reconciliation_id: str,
    operator: RequireReconcileRead,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    from app.db.models.v2_live_exec_reconciliation import (
        V2LiveExecReconciliation,
    )
    row = (await session.execute(
        select(V2LiveExecReconciliation)
        .where(V2LiveExecReconciliation.id == reconciliation_id)
    )).scalars().first()
    if row is None:
        return _refusal(request, "reconciliation_not_found", [
            {"failing": "reconciliation_id"}], status_code=404)
    return {"reconciliation": {
        "id": row.id, "outcome": row.outcome, "scope": row.scope,
        "drift_facts": row.drift_facts, "digest": row.digest,
        "mode": row.mode}, **_envelope(request)}


@router.post("/incident/open")
async def api_incident_open(
    request: Request, body: IncidentOpenRequest,
    operator: RequireIncidentOpen,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    """Confirm-rank OPEN (sealed step-up chain; severity typed at the
    edge before schema)."""
    from app.v2.live_exec.incident.engine import (
        INCIDENT_SEVERITIES,
        INCIDENT_SEVERITY_INVALID,
        open_incident,
    )
    try:
        step_up = require_step_up(body.step_up_ref)
        if body.severity not in INCIDENT_SEVERITIES:
            # CR-1 (DEL-001): the reason cites the ENGINE CONSTANT —
            # the wire and the closed vocabulary are one law.
            return _refusal(request, INCIDENT_SEVERITY_INVALID, [
                {"failing": "severity", "asked": body.severity,
                 "closed_set": list(INCIDENT_SEVERITIES)}],
                status_code=422)
        row = await open_incident(
            session, severity=body.severity,
            instruments_pinned=body.instruments_pinned,
            recovery_path=body.recovery_path, step_up_ref=step_up,
            opened_by=operator.username, actor_id=operator.username,
            mode=request.app.state.v2_mode, operator_id=operator.username,
            correlation_id=getattr(request.state, "correlation_id",
                                   None))
        payload = {"incident": {
            "id": row.id, "severity": row.severity,
            "instruments_pinned": row.instruments_pinned,
            "status": row.status, "digest": row.digest,
            "mode": row.mode}}
        await session.commit()
    except LiveExecRefused as refused:
        await session.rollback()
        return _refusal(request, refused.reason, refused.notes)
    return {**payload, **_envelope(request)}


@router.post("/incident/{incident_id}/close")
async def api_incident_close(
    request: Request, incident_id: str, body: IncidentCloseRequest,
    operator: RequireIncidentClose,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    """Confirm-rank CLOSE — THE single sanctioned close path."""
    from app.v2.live_exec.incident.engine import close_incident
    try:
        step_up = require_step_up(body.step_up_ref)
        answer = await close_incident(
            session, incident_id=incident_id,
            closed_by=operator.username, actor_id=operator.username,
            step_up_ref=step_up, operator_id=operator.username)
        await session.commit()
    except LiveExecRefused as refused:
        await session.rollback()
        return _refusal(request, refused.reason, refused.notes)
    return {"incident": answer, **_envelope(request)}


@router.get("/incidents")
async def api_incidents_list(
    request: Request, operator: RequireIncidentRead,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    limit: int = Query(default=100, ge=1, le=500),
):
    """List shape; zero-row shape typed, never error."""
    from app.db.models.v2_live_exec_incident import V2LiveExecIncident
    rows = list((await session.execute(
        select(V2LiveExecIncident)
        .order_by(V2LiveExecIncident.created_at.desc())
        .limit(limit))).scalars().all())
    return {"incidents": [
        {"id": r.id, "severity": r.severity, "status": r.status,
         "instruments_pinned": r.instruments_pinned,
         "digest": r.digest} for r in rows],
        **_envelope(request)}


@router.get("/incident/{incident_id}")
async def api_incident_by_id(
    request: Request, incident_id: str, operator: RequireIncidentRead,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    from app.db.models.v2_live_exec_incident import V2LiveExecIncident
    from app.v2.live_exec.incident.engine import INCIDENT_NOT_OPEN
    row = (await session.execute(
        select(V2LiveExecIncident)
        .where(V2LiveExecIncident.id == incident_id))).scalars().first()
    if row is None:
        # pinned-id lookup reuse (REV §5 DEL-002 acceptable-form) — the
        # reason cites the ENGINE CONSTANT, keeping the wire-literal
        # enrollment set closed at exactly the two lookup ids
        return _refusal(request, INCIDENT_NOT_OPEN, [
            {"failing": "incident_id"}], status_code=404)
    return {"incident": {
        "id": row.id, "opened_by": row.opened_by,
        "severity": row.severity,
        "instruments_pinned": row.instruments_pinned,
        "recovery_path": row.recovery_path, "status": row.status,
        "closed_at": row.closed_at, "closed_by": row.closed_by,
        "digest": row.digest, "mode": row.mode},
        **_envelope(request)}
