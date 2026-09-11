"""V2 BE-5 U-5 diagnostics tests — BO-V2-BE-5-001 (P-2 artifact table)."""

from __future__ import annotations

import socket
from datetime import datetime, timezone
from uuid import uuid4

import pytest
from sqlalchemy import select

from app.db.models.v2_audit_event import V2AuditEvent
from app.db.models.v2_lineage_record import V2LineageRecord
from app.db.session import session_scope
from app.v2.research_governance.decisions import (
    evaluate_economic,
    evaluate_eligibility,
    evaluate_freshness,
)
from app.v2.research_governance.diagnostics import (
    engine_versions_hash,
    inputs_hash,
    write_diagnostic_report,
)

NOW = datetime(2026, 9, 2, 12, 0, tzinfo=timezone.utc)


@pytest.fixture(autouse=True)
def _socket_guard(monkeypatch):
    def _deny(*_a, **_k):
        raise AssertionError("network attempt during BE-5 diagnostics test")

    monkeypatch.setattr(socket, "getaddrinfo", _deny)
    monkeypatch.setattr(socket, "create_connection", _deny)


def _outcomes():
    return [
        evaluate_eligibility({}),                      # ineligible, typed
        evaluate_freshness(None, as_of=NOW),           # unknown, typed
        evaluate_economic({"net_expectancy": 0.01}),   # unevaluated, typed
    ]


@pytest.mark.asyncio
async def test_diagnostic_report_written_with_audit_and_lineage(prepared_db) -> None:
    artifact = str(uuid4())
    async with session_scope() as session:
        report, reused = await write_diagnostic_report(
            session, model_artifact_id=artifact, governance_record_id=None,
            outcomes=_outcomes(), data_class="synthetic", mode="RESEARCH",
            operator_id="tester", correlation_id="c-1")
        assert reused is False
        assert report.diagnostics["summary"]["eligibility"] == "ineligible"
        assert report.diagnostics["summary"]["freshness"] == "unknown"
        assert len(report.inputs_hash) == 64
        assert report.engine_versions_hash == engine_versions_hash()

    async with session_scope() as session:
        audits = [a for (a,) in (await session.execute(
            select(V2AuditEvent.action).where(
                V2AuditEvent.action == "ml.diagnostics.computed"))).all()]
        assert audits
        lineage = (await session.execute(
            select(V2LineageRecord).where(
                V2LineageRecord.artifact_type == "ml_diagnostic_report"
            ))).scalars().all()
        assert lineage and lineage[0].input_snapshot_id == report.inputs_hash


@pytest.mark.asyncio
async def test_diagnostic_determinism_anchor_idempotent(prepared_db) -> None:
    artifact = str(uuid4())
    async with session_scope() as session:
        first, reused1 = await write_diagnostic_report(
            session, model_artifact_id=artifact, governance_record_id=None,
            outcomes=_outcomes(), data_class="synthetic", mode="RESEARCH",
            operator_id="tester", correlation_id="c-2")
        second, reused2 = await write_diagnostic_report(
            session, model_artifact_id=artifact, governance_record_id=None,
            outcomes=_outcomes(), data_class="synthetic", mode="RESEARCH",
            operator_id="tester", correlation_id="c-3")
        assert reused1 is False and reused2 is True
        assert first.id == second.id  # existing returned, not duplicated


def test_inputs_hash_deterministic_and_input_sensitive() -> None:
    a, b = _outcomes(), _outcomes()
    assert inputs_hash(a) == inputs_hash(b)
    changed = _outcomes()[:2]
    assert inputs_hash(changed) != inputs_hash(a)
