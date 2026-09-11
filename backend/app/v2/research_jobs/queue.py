"""BE-7 U-4 governed job queue (BO §1; REQ-1.7; conditions C1–C4).

Database-backed (ARCH row 89 decision); manual invocation only (C4).
The job row is the band's sole mutable state; every transition mints an
attempt-ledger row and an audit event (P-10). Submission-time fields are
write-once (C1); the mutable set is exactly C2's.
"""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.v2_research_jobs import (
    V2ResearchJob,
    V2ResearchJobAttempt,
    V2StrategyVersion,
)
from app.v2.audit.contract import V2AuditEventCreate
from app.v2.audit.repository import V2AuditRepository
from app.v2.research_jobs.contracts import (
    JOB_TERMINAL_STATES,
    RJ_FIRST_LANDING_DATA_CLASSES,
    SCHEDULE_KINDS_V1,
    TypedOutcome,
)

_DOMAIN = "v2.research_jobs"


@dataclass(frozen=True)
class JobSubmission:
    owner: str
    authorization_ref: str
    inputs: dict            # {"input_registry_id", "strategy_version_id",
    #                          "cost_model_id", "result_class", ...}
    schedule: dict
    data_class: str
    mode: str
    operator_id: str
    correlation_id: str | None


async def _audit(session: AsyncSession, action: str, *, details: dict,
                 mode: str, operator_id: str,
                 correlation_id: str | None,
                 resource_id: str | None = None) -> None:
    await V2AuditRepository(session).append(V2AuditEventCreate(
        domain=_DOMAIN, action=action, actor_id=operator_id,
        actor_type="operator", mode=mode,
        resource_type="research_job", resource_id=resource_id,
        details=details, operator_id=operator_id,
        correlation_id=correlation_id))


async def submit_job(session: AsyncSession, sub: JobSubmission) -> TypedOutcome:
    """Submission: typed refusals, durably audited (C-1 law); on pass the
    write-once row is INSERTed queued (C1)."""
    reasons: list = []
    if not sub.authorization_ref:
        reasons.append({"failing": "authorization_ref", "required": "set"})
    if sub.schedule.get("kind") not in SCHEDULE_KINDS_V1:
        reasons.append({"failing": "schedule.kind",
                        "value": sub.schedule.get("kind"),
                        "required": list(SCHEDULE_KINDS_V1),
                        "note": "C4 — v1 scope is manual invocation only"})
    if sub.data_class not in RJ_FIRST_LANDING_DATA_CLASSES:
        reasons.append({"failing": "data_class", "value": sub.data_class,
                        "required": list(RJ_FIRST_LANDING_DATA_CLASSES),
                        "note": "corpus-gated (V2-TD-18 continuity)"})
    if sub.mode != "RESEARCH":
        reasons.append({"failing": "mode", "value": sub.mode})

    # strategy must be a registered-current generation (REQ-1.6)
    sv_id = sub.inputs.get("strategy_version_id")
    if not sv_id:
        reasons.append({"failing": "inputs.strategy_version_id"})
    else:
        strategy = (await session.execute(
            select(V2StrategyVersion).where(V2StrategyVersion.id == sv_id)
        )).scalar_one_or_none()
        if strategy is None:
            reasons.append({"failing": "strategy_version", "value": "unresolvable"})
        else:
            newest = (await session.execute(
                select(V2StrategyVersion)
                .where(V2StrategyVersion.strategy_id == strategy.strategy_id)
                .order_by(V2StrategyVersion.record_seq.desc())
            )).scalars().first()
            if newest is None or newest.id != strategy.id:
                reasons.append({"failing": "strategy_version",
                                "value": "superseded generation — not current"})
            elif strategy.lifecycle_state != "registered":
                reasons.append({"failing": "strategy.lifecycle_state",
                                "value": strategy.lifecycle_state,
                                "required": "registered"})
    for key in ("input_registry_id", "cost_model_id", "result_class"):
        if not sub.inputs.get(key):
            reasons.append({"failing": f"inputs.{key}"})

    if reasons:
        await _audit(session, "job.submit.refused",
                     details={"reasons": reasons[:8]},
                     mode=sub.mode, operator_id=sub.operator_id,
                     correlation_id=sub.correlation_id)
        await session.commit()  # durable refusal audit (C-1 law)
        return TypedOutcome(outcome="refused", reasons=reasons)

    job = V2ResearchJob(
        owner=sub.owner,
        authorization_ref=sub.authorization_ref,
        inputs=sub.inputs,
        schedule=sub.schedule,
        job_state="queued",
        attempt_count=0,
        data_class=sub.data_class,
        mode=sub.mode,
        operator_id=sub.operator_id,
        correlation_id=sub.correlation_id,
    )
    session.add(job)
    await session.flush()
    await _audit(session, "job.submitted",
                 details={"owner": sub.owner,
                          "authorization_ref": sub.authorization_ref,
                          "inputs": sub.inputs},
                 mode=sub.mode, operator_id=sub.operator_id,
                 correlation_id=sub.correlation_id, resource_id=job.id)
    return TypedOutcome(outcome="registered", record_id=job.id)


async def cancel_job(session: AsyncSession, *, job_id: str, actor_id: str,
                     reason: str, mode: str,
                     correlation_id: str | None) -> TypedOutcome:
    """Typed cancel: terminal states refuse (REQ-1.7); every cancel mints
    a ledger row + audit event."""
    job = (await session.execute(
        select(V2ResearchJob).where(V2ResearchJob.id == job_id)
    )).scalar_one_or_none()
    if job is None:
        return TypedOutcome(outcome="refused",
                            reasons=[{"failing": "job_id", "value": "unresolvable"}])
    if job.job_state in JOB_TERMINAL_STATES:
        await _audit(session, "job.cancel.refused",
                     details={"job_state": job.job_state,
                              "note": "terminal state"},
                     mode=mode, operator_id=actor_id,
                     correlation_id=correlation_id, resource_id=job.id)
        await session.commit()
        return TypedOutcome(outcome="refused",
                            reasons=[{"failing": "job_state",
                                      "value": job.job_state,
                                      "note": "terminal — cancel refused"}])
    job.attempt_count += 1
    job.job_state = "cancelled"
    job.failure = {"cancelled_by": actor_id, "reason": reason}
    session.add(V2ResearchJobAttempt(
        job_id=job.id, attempt_index=job.attempt_count,
        outcome="cancelled", reason={"cancelled_by": actor_id,
                                     "reason": reason},
        actor_id=actor_id, mode=mode, operator_id=actor_id,
        correlation_id=correlation_id))
    await session.flush()
    await _audit(session, "job.cancelled",
                 details={"reason": reason, "attempt_index": job.attempt_count},
                 mode=mode, operator_id=actor_id,
                 correlation_id=correlation_id, resource_id=job.id)
    return TypedOutcome(outcome="registered", record_id=job.id)
