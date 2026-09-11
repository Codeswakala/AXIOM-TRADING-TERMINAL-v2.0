"""BE-7 U-4 attempt-idempotent runner (P-10; conditions C2/C3; Part 10.1).

The ONLY path that transitions a job through running → succeeded/failed
and the ONLY artifact writer. Idempotency: the result determinism anchor
returns the existing artifact on a retried identical attempt; the ledger's
UNIQUE(job_id, attempt_index) forbids double-writes per attempt.
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.v2_research_jobs import (
    V2BacktestInput,
    V2CostModel,
    V2ResearchJob,
    V2ResearchJobAttempt,
    V2ResearchResult,
    V2StrategyVersion,
)
from app.v2.audit.contract import V2AuditEventCreate
from app.v2.audit.repository import V2AuditRepository
from app.v2.lineage.contract import V2LineageRecordCreate
from app.v2.lineage.repository import V2LineageRepository
from app.v2.research_jobs.contracts import (
    JOB_MUTABLE_COLUMNS,
    RUNNER_INSERT_TABLES,
    RUNNER_UPDATE_TABLES,
    require_constructible_result_class,
)
from app.v2.research_jobs.leakage import LeakageRefused, ReplayWindow
from app.v2.research_jobs.replay import (
    ENGINE_VERSIONS,
    engine_versions_hash,
    run_replay,
)

_DOMAIN = "v2.research_jobs"


def _utc_from_store(value: datetime | None) -> datetime | None:
    """SQLite discards tz on DateTime(timezone=True) — BE-2 normalizer law."""
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value



# Part 10.1 allow-list — asserted by test; the module constant IS the law.
WRITABLE_TABLES = {"insert": RUNNER_INSERT_TABLES,
                   "update": RUNNER_UPDATE_TABLES}
JOB_UPDATE_COLUMNS = JOB_MUTABLE_COLUMNS  # C2


async def _audit(session: AsyncSession, action: str, *, details: dict,
                 mode: str, operator_id: str, correlation_id: str | None,
                 resource_id: str | None = None) -> None:
    await V2AuditRepository(session).append(V2AuditEventCreate(
        domain=_DOMAIN, action=action, actor_id=operator_id,
        actor_type="operator", mode=mode,
        resource_type="research_job", resource_id=resource_id,
        details=details, operator_id=operator_id,
        correlation_id=correlation_id))


async def run_job(session: AsyncSession, *, job_id: str, actor_id: str,
                  bars: list[dict], correlation_id: str | None) -> dict:
    """Execute one attempt. Returns {job_state, result_id, reused, reasons}."""
    job = (await session.execute(
        select(V2ResearchJob).where(V2ResearchJob.id == job_id)
    )).scalar_one_or_none()
    if job is None:
        return {"job_state": "unknown", "result_id": None, "reused": False,
                "reasons": [{"failing": "job_id"}]}
    if job.job_state not in ("queued", "failed"):
        return {"job_state": job.job_state, "result_id": job.output_ref,
                "reused": job.job_state == "succeeded",
                "reasons": [{"failing": "job_state", "value": job.job_state,
                             "note": "only queued/failed jobs run"}]}

    mode = job.mode
    attempt = job.attempt_count + 1
    job.attempt_count = attempt          # C2 mutable set only
    job.job_state = "running"
    await session.flush()
    await _audit(session, "job.started",
                 details={"attempt_index": attempt}, mode=mode,
                 operator_id=actor_id, correlation_id=correlation_id,
                 resource_id=job.id)

    # resolve the lineage triple
    registry = (await session.execute(
        select(V2BacktestInput).where(
            V2BacktestInput.id == job.inputs["input_registry_id"])
    )).scalar_one_or_none()
    strategy = (await session.execute(
        select(V2StrategyVersion).where(
            V2StrategyVersion.id == job.inputs["strategy_version_id"])
    )).scalar_one_or_none()
    cost = (await session.execute(
        select(V2CostModel).where(
            V2CostModel.id == job.inputs["cost_model_id"])
    )).scalar_one_or_none()

    def _fail(reasons: list) -> dict:
        job.job_state = "failed"
        job.failure = {"reasons": reasons, "attempt_index": attempt}
        session.add(V2ResearchJobAttempt(
            job_id=job.id, attempt_index=attempt, outcome="failed",
            reason={"reasons": reasons}, actor_id=actor_id, mode=mode,
            operator_id=actor_id, correlation_id=correlation_id))
        return {"job_state": "failed", "result_id": None, "reused": False,
                "reasons": reasons}

    if registry is None or strategy is None or cost is None:
        result = _fail([{"failing": "lineage_resolution"}])
        await _audit(session, "job.failed", details=job.failure, mode=mode,
                     operator_id=actor_id, correlation_id=correlation_id,
                     resource_id=job.id)
        return result

    try:
        result_class = require_constructible_result_class(
            job.inputs["result_class"])  # P-9 construction point
    except Exception as exc:
        result = _fail([{"failing": "result_class", "value": str(exc)}])
        await _audit(session, "job.failed", details=job.failure, mode=mode,
                     operator_id=actor_id, correlation_id=correlation_id,
                     resource_id=job.id)
        return result

    versions_hash = engine_versions_hash()
    # P-10 idempotency: anchor lookup BEFORE computing
    existing = (await session.execute(
        select(V2ResearchResult).where(
            V2ResearchResult.strategy_version_id == strategy.id,
            V2ResearchResult.inputs_hash == registry.content_hash,
            V2ResearchResult.engine_versions_hash == versions_hash)
    )).scalar_one_or_none()
    if existing is not None:
        job.job_state = "succeeded"
        job.output_ref = existing.id
        session.add(V2ResearchJobAttempt(
            job_id=job.id, attempt_index=attempt, outcome="succeeded",
            artifact_ref=existing.id,
            reason={"idempotent_reuse": True,
                    "anchor": "uq_v2_result_determinism_anchor"},
            actor_id=actor_id, mode=mode, operator_id=actor_id,
            correlation_id=correlation_id))
        await session.flush()
        await _audit(session, "result.reused",
                     details={"result_id": existing.id,
                              "attempt_index": attempt},
                     mode=mode, operator_id=actor_id,
                     correlation_id=correlation_id, resource_id=job.id)
        return {"job_state": "succeeded", "result_id": existing.id,
                "reused": True, "reasons": []}

    window = ReplayWindow(
        window_start=_utc_from_store(registry.window_start),
        window_end=_utc_from_store(registry.window_end),
        as_of=_utc_from_store(registry.window_end))
    cost_model = {"spread": cost.spread, "commission": cost.commission,
                  "slippage": cost.slippage}
    try:
        replay = run_replay(
            bars=bars, window=window,
            strategy_rule=strategy.parameters["rule"],
            parameters=strategy.parameters,
            cost_model=cost_model,
            stored_content_hash=registry.content_hash,
            series_refs=registry.series_refs)
    except LeakageRefused as exc:
        result = _fail([{"failing": exc.guard, "reasons": exc.reasons}])
        await _audit(session, "job.failed", details=job.failure, mode=mode,
                     operator_id=actor_id, correlation_id=correlation_id,
                     resource_id=job.id)
        return result
    except ValueError as exc:
        # F-1 defense-in-depth (CR-V2-BE-7-001): engine vocabulary errors
        # (e.g. unknown cost unit on pre-gate rows) fail TYPED, never 500.
        result = _fail([{"failing": "engine_vocabulary", "value": str(exc)}])
        await _audit(session, "job.failed", details=job.failure, mode=mode,
                     operator_id=actor_id, correlation_id=correlation_id,
                     resource_id=job.id)
        return result

    artifact = V2ResearchResult(
        result_class=result_class,
        job_id=job.id, attempt_index=attempt,
        strategy_version_id=strategy.id,
        input_registry_id=registry.id,
        cost_model_id=cost.id,
        inputs_hash=registry.content_hash,
        engine_versions=ENGINE_VERSIONS,
        engine_versions_hash=versions_hash,
        summary=replay.summary,
        time_basis={"window_start": _utc_from_store(
                        registry.window_start).isoformat(),
                    "window_end": _utc_from_store(
                        registry.window_end).isoformat(),
                    "bars": replay.summary["bars_replayed"]},
        data_class=job.data_class,
        mode=mode, operator_id=actor_id, correlation_id=correlation_id)
    session.add(artifact)
    await session.flush()

    job.job_state = "succeeded"
    job.output_ref = artifact.id
    session.add(V2ResearchJobAttempt(
        job_id=job.id, attempt_index=attempt, outcome="succeeded",
        artifact_ref=artifact.id, reason={"computed": True},
        actor_id=actor_id, mode=mode, operator_id=actor_id,
        correlation_id=correlation_id))
    await session.flush()

    await _audit(session, "result.created",
                 details={"result_id": artifact.id,
                          "result_class": result_class,
                          "attempt_index": attempt},
                 mode=mode, operator_id=actor_id,
                 correlation_id=correlation_id, resource_id=job.id)
    await V2LineageRepository(session).append(V2LineageRecordCreate(
        artifact_type="research_result",
        artifact_id=artifact.id,
        operator_id=actor_id, mode=mode,
        source_artifact_ids=[registry.id, strategy.id, cost.id, job.id],
        computation_version=versions_hash,
        input_snapshot_id=registry.content_hash))
    await _audit(session, "job.succeeded",
                 details={"result_id": artifact.id,
                          "attempt_index": attempt},
                 mode=mode, operator_id=actor_id,
                 correlation_id=correlation_id, resource_id=job.id)
    return {"job_state": "succeeded", "result_id": artifact.id,
            "reused": False, "reasons": []}
