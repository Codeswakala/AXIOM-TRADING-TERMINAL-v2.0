"""BE-5 U-5 diagnostics service — immutable ML diagnostic artifacts (P-2).

Builds one deterministic diagnostic report from decision outcomes; the
determinism anchor (model_artifact_id, inputs_hash, engine_versions_hash)
makes recomputation idempotent (existing report returned, not duplicated).
"""

from __future__ import annotations

import hashlib
import json

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.v2_research_governance import V2MlDiagnosticReport
from app.v2.audit.contract import V2AuditEventCreate
from app.v2.audit.repository import V2AuditRepository
from app.v2.lineage.contract import V2LineageRecordCreate
from app.v2.lineage.repository import V2LineageRepository
from app.v2.research_governance.contracts import DecisionOutcome

ENGINE_VERSIONS = {"ml_governance_engine": "mge-1.0.0"}


def _canonical(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)


def engine_versions_hash() -> str:
    return hashlib.sha256(_canonical(ENGINE_VERSIONS).encode()).hexdigest()


def inputs_hash(outcomes: list[DecisionOutcome]) -> str:
    payload = [o.as_decision_basis() for o in outcomes]
    return hashlib.sha256(_canonical(payload).encode()).hexdigest()


async def write_diagnostic_report(
    session: AsyncSession,
    *,
    model_artifact_id: str,
    governance_record_id: str | None,
    outcomes: list[DecisionOutcome],
    data_class: str,
    mode: str,
    operator_id: str,
    correlation_id: str | None,
) -> tuple[V2MlDiagnosticReport, bool]:
    """Returns (report, reused_existing)."""
    ih = inputs_hash(outcomes)
    evh = engine_versions_hash()

    existing = (await session.execute(
        select(V2MlDiagnosticReport).where(
            V2MlDiagnosticReport.model_artifact_id == model_artifact_id,
            V2MlDiagnosticReport.inputs_hash == ih,
            V2MlDiagnosticReport.engine_versions_hash == evh,
        )
    )).scalar_one_or_none()
    if existing is not None:
        return existing, True

    report = V2MlDiagnosticReport(
        model_artifact_id=model_artifact_id,
        governance_record_id=governance_record_id,
        diagnostics={
            "outcomes": [o.as_decision_basis() for o in outcomes],
            "summary": {o.contract: o.status for o in outcomes},
        },
        input_refs={"contracts": [o.contract for o in outcomes]},
        inputs_hash=ih,
        engine_versions=ENGINE_VERSIONS,
        engine_versions_hash=evh,
        data_class=data_class,
        mode=mode,
        operator_id=operator_id,
        correlation_id=correlation_id,
    )
    session.add(report)
    await session.flush()

    await V2AuditRepository(session).append(V2AuditEventCreate(
        domain="v2.research_governance",
        action="ml.diagnostics.computed",
        actor_id=operator_id, actor_type="operator", mode=mode,
        resource_type="ml_diagnostic_report", resource_id=report.id,
        details={"model_artifact_id": model_artifact_id,
                 "inputs_hash": ih, "summary": report.diagnostics["summary"]},
        operator_id=operator_id, correlation_id=correlation_id,
    ))
    await V2LineageRepository(session).append(V2LineageRecordCreate(
        artifact_type="ml_diagnostic_report",
        artifact_id=report.id,
        operator_id=operator_id,
        mode=mode,
        source_artifact_ids=[model_artifact_id]
        + ([governance_record_id] if governance_record_id else []),
        computation_version=evh,
        input_snapshot_id=ih,
    ))
    return report, False
