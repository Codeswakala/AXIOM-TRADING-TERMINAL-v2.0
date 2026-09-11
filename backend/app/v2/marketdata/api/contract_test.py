"""V2 BE-3 P2 authenticated contract-test endpoint — BO-V2-BE-3-P2-001 §3.3.

The ONLY invocation surface for the contract-test runner. Admin-only
permission `v2.marketdata.provider.contract_test` (SAL-4), server-side JWT
auth, server-generated correlation ID. No CLI or alternate runner path
exists (import-boundary enforced by tests).

Durable audit sequence (§3.5): start → per-call durable call_started (no
durable start = no attempt) → call_completed → complete. Completion-audit
failure → hard stop + independent incident marker + indeterminate state.
"""

from __future__ import annotations

import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.operator import Operator
from app.db.session import get_db_session
from app.v2.identifiers import new_id
from app.v2.marketdata.providers.contract_test import (
    AUTHORITY_REF,
    CALL_STATE_COMPLETED,
    CALL_STATE_INDETERMINATE,
    CALL_STATE_REFUSED,
    MAX_ATTEMPTS,
    RETRY_ALLOCATION,
    AttemptBudget,
    CallRecord,
    _durable_audit,
    build_call_plan,
    check_preconditions,
    classify_transport_exception,
    validate_body,
)
from app.v2.marketdata.providers.credentials import resolve_contract_test_credential
from app.v2.rbac.dependencies import require_v2_permission

RequireV2ProviderContractTest = Annotated[
    Operator, Depends(require_v2_permission("v2.marketdata.provider.contract_test"))
]

router = APIRouter(prefix="/marketdata/providers/twelvedata", tags=["V2 Provider Contract Test"])


class V2ContractTestCallModel(BaseModel):
    request_class: str
    instrument_id: str | None
    redacted_request: str
    response_status: int | None
    body_sha256: str | None
    schema_verdict: str
    error_category: str
    attempt_number: int | None
    budget_remaining: int
    call_state: str
    latency_ms: float | None


class V2ContractTestRunResponse(BaseModel):
    run_state: str  # "refused" | "completed" | "aborted"
    refusal_reasons: list[str] = []
    calls: list[V2ContractTestCallModel] = []
    completed: int = 0
    refused_before_call: int = 0
    indeterminate_after_start: int = 0
    delta_findings: int = 0
    authority_ref: str = AUTHORITY_REF
    mode: str
    correlation_id: str | None = None
    timestamp: datetime


def _incident_marker(correlation_id: str, reason: str) -> None:
    """Independent fail-safe incident channel (§3.5.5): SECURITY log + marker
    file that does NOT depend on the (failed) database path."""
    from app.core.logging import get_logger

    get_logger(__name__, category="SECURITY").error(
        "P2 contract-test incident: correlation=%s reason=%s", correlation_id, reason
    )
    marker_dir = Path(os.environ.get("AXIOM_TD_INCIDENT_DIR", tempfile.gettempdir()))
    try:
        (marker_dir / f"axiom_p2_incident_{correlation_id}.marker").write_text(
            f"reason={reason}\nutc={datetime.now(timezone.utc).isoformat()}\n"
        )
    except OSError:  # marker best-effort; the SECURITY log already fired
        pass


@router.post("/contract-test", response_model=V2ContractTestRunResponse)
async def run_contract_test(
    request: Request,
    operator: RequireV2ProviderContractTest,
    session: AsyncSession = Depends(get_db_session),
) -> V2ContractTestRunResponse:
    """Bounded provider contract evaluation (single run; §§3.4–3.7)."""
    mode = request.app.state.v2_mode
    correlation_id = getattr(request.state, "correlation_id", None) or new_id()
    now = lambda: datetime.now(timezone.utc)  # noqa: E731

    # ---- §3.4 preconditions (default deny) --------------------------------
    credential = resolve_contract_test_credential()
    preconditions = await check_preconditions(
        session, credential_state=credential.state, mode=mode
    )
    failed = [p.name for p in preconditions if not p.satisfied]
    if failed:
        await _durable_audit(
            session,
            action="provider.contract_test.refused",
            actor_id=operator.id,
            mode=mode,
            correlation_id=correlation_id,
            details={"failed_preconditions": failed},
        )
        return V2ContractTestRunResponse(
            run_state="refused",
            refusal_reasons=failed,
            mode=mode,
            correlation_id=correlation_id,
            timestamp=now(),
        )

    # ---- run start (durable) ----------------------------------------------
    await _durable_audit(
        session,
        action="provider.contract_test.start",
        actor_id=operator.id,
        mode=mode,
        correlation_id=correlation_id,
        details={
            "authority_ref": AUTHORITY_REF,
            "preconditions": {p.name: p.satisfied for p in preconditions},
            "budget_max": MAX_ATTEMPTS,
        },
    )

    # Transport constructed ONLY here, inside the authenticated chain.
    from app.v2.marketdata.providers.transport import NetworkTransport, construction_token

    transport = NetworkTransport(construction_token())
    budget = AttemptBudget(MAX_ATTEMPTS)
    records: list[CallRecord] = []
    aborted = False

    for call in build_call_plan():
        max_retries = RETRY_ALLOCATION[call.request_class]
        outcome: CallRecord | None = None
        for retry_index in range(max_retries + 1):
            attempt_number = budget.debit()
            if attempt_number is None:
                records.append(
                    CallRecord(
                        request_class=call.request_class,
                        instrument_id=call.instrument_id,
                        redacted_request=call.planned.redacted(),
                        response_status=None,
                        body_sha256=None,
                        schema_verdict="budget_exhausted",
                        error_category="none",
                        attempt_number=None,
                        budget_remaining=0,
                        call_state=CALL_STATE_REFUSED,
                        latency_ms=None,
                    )
                )
                outcome = records[-1]
                break

            # §3.5.2 durable call_started BEFORE the attempt
            try:
                await _durable_audit(
                    session,
                    action="provider.contract_test.call_started",
                    actor_id=operator.id,
                    mode=mode,
                    correlation_id=correlation_id,
                    details={
                        "request_class": call.request_class,
                        "instrument_id": call.instrument_id,
                        "redacted_request": call.planned.redacted(),
                        "attempt_number": attempt_number,
                        "budget_remaining": budget.remaining,
                    },
                )
            except Exception:  # §3.5.3 no durable start → no attempt
                records.append(
                    CallRecord(
                        request_class=call.request_class,
                        instrument_id=call.instrument_id,
                        redacted_request=call.planned.redacted(),
                        response_status=None,
                        body_sha256=None,
                        schema_verdict="start_audit_failed",
                        error_category="none",
                        attempt_number=attempt_number,
                        budget_remaining=budget.remaining,
                        call_state=CALL_STATE_REFUSED,
                        latency_ms=None,
                    )
                )
                aborted = True
                _incident_marker(correlation_id, "start_audit_failed")
                break

            # ---- the network attempt --------------------------------------
            apikey = "" if (call.request_class == "AUTH" and call.expect_error) else (
                credential.value or ""
            )
            try:
                result = transport.execute(call.planned, apikey=apikey)
            except Exception as transport_exc:
                # DEL-002: EVERY started attempt gets a durable completion
                # event (non-payload) BEFORE any retry decision.
                error_category = classify_transport_exception(transport_exc)
                failure_record = CallRecord(
                    request_class=call.request_class,
                    instrument_id=call.instrument_id,
                    redacted_request=call.planned.redacted(),
                    response_status=None,
                    body_sha256=None,
                    schema_verdict="transport_failure",
                    error_category=error_category,
                    attempt_number=attempt_number,
                    budget_remaining=budget.remaining,
                    call_state=CALL_STATE_COMPLETED,
                    latency_ms=None,
                )
                try:
                    await _durable_audit(
                        session,
                        action="provider.contract_test.call_completed",
                        actor_id=operator.id,
                        mode=mode,
                        correlation_id=correlation_id,
                        details={
                            "request_class": call.request_class,
                            "response_status": None,
                            "body_sha256": None,
                            "schema_verdict": "transport_failure",
                            "error_category": error_category,
                            "attempt_number": attempt_number,
                            "budget_remaining": budget.remaining,
                            "latency_ms": None,
                        },
                    )
                except Exception:
                    # completion write failed → started attempt is
                    # indeterminate; hard stop + incident path (§3.5.5)
                    failure_record.call_state = CALL_STATE_INDETERMINATE
                    records.append(failure_record)
                    aborted = True
                    _incident_marker(correlation_id, "completion_audit_failed")
                    break
                records.append(failure_record)
                if retry_index < max_retries:
                    continue
                outcome = failure_record
                break

            # transient body: hash + validate, then drop the only reference
            body_sha256, schema_verdict, error_category = validate_body(
                result.body, call
            )
            status_code, latency_ms = result.status_code, result.latency_ms
            del result  # drop the sole reference holding the transient body
            record = CallRecord(
                request_class=call.request_class,
                instrument_id=call.instrument_id,
                redacted_request=call.planned.redacted(),
                response_status=status_code,
                body_sha256=body_sha256,
                schema_verdict=schema_verdict,
                error_category=error_category,
                attempt_number=attempt_number,
                budget_remaining=budget.remaining,
                call_state=CALL_STATE_COMPLETED,
                latency_ms=round(latency_ms, 2),
            )

            # §3.5.4/5 completion audit; failure → hard stop + incident
            try:
                await _durable_audit(
                    session,
                    action="provider.contract_test.call_completed",
                    actor_id=operator.id,
                    mode=mode,
                    correlation_id=correlation_id,
                    details={
                        "request_class": record.request_class,
                        "response_status": record.response_status,
                        "body_sha256": record.body_sha256,
                        "schema_verdict": record.schema_verdict,
                        "error_category": record.error_category,
                        "attempt_number": record.attempt_number,
                        "budget_remaining": record.budget_remaining,
                        "latency_ms": record.latency_ms,
                    },
                )
            except Exception:
                record.call_state = CALL_STATE_INDETERMINATE
                records.append(record)
                aborted = True
                _incident_marker(correlation_id, "completion_audit_failed")
                break

            records.append(record)
            outcome = record
            # retry only on retryable classes (transport/5xx/429)
            if record.response_status in (500, 502, 503, 504, 429) and retry_index < max_retries:
                continue
            break

        if aborted:
            break
        if (
            outcome is not None
            and outcome.call_state == CALL_STATE_REFUSED
            and outcome.schema_verdict == "budget_exhausted"
        ):
            break  # §3.6 post-exhaustion: no further calls of any kind

    completed = sum(1 for r in records if r.call_state == CALL_STATE_COMPLETED)
    refused = sum(1 for r in records if r.call_state == CALL_STATE_REFUSED)
    indeterminate = sum(1 for r in records if r.call_state == CALL_STATE_INDETERMINATE)
    deltas = sum(1 for r in records if r.schema_verdict.startswith("delta-finding"))

    try:
        await _durable_audit(
            session,
            action="provider.contract_test.complete",
            actor_id=operator.id,
            mode=mode,
            correlation_id=correlation_id,
            details={
                "completed": completed,
                "refused_before_call": refused,
                "indeterminate_after_start": indeterminate,
                "delta_findings": deltas,
                "aborted": aborted,
            },
        )
    except Exception:
        # DEL-005: a run whose final completion audit could not be durably
        # committed must NOT be represented as completed — fail closed.
        aborted = True
        final_audit_incomplete = True
        _incident_marker(correlation_id, "complete_audit_failed")
    else:
        final_audit_incomplete = False

    run_state = "aborted" if aborted else "completed"
    if final_audit_incomplete:
        run_state = "aborted:final-audit-incomplete"

    return V2ContractTestRunResponse(
        run_state=run_state,
        calls=[
            V2ContractTestCallModel(**{
                "request_class": r.request_class,
                "instrument_id": r.instrument_id,
                "redacted_request": r.redacted_request,
                "response_status": r.response_status,
                "body_sha256": r.body_sha256,
                "schema_verdict": r.schema_verdict,
                "error_category": r.error_category,
                "attempt_number": r.attempt_number,
                "budget_remaining": r.budget_remaining,
                "call_state": r.call_state,
                "latency_ms": r.latency_ms,
            })
            for r in records
        ],
        completed=completed,
        refused_before_call=refused,
        indeterminate_after_start=indeterminate,
        delta_findings=deltas,
        mode=mode,
        correlation_id=correlation_id,
        timestamp=datetime.now(timezone.utc),
    )
