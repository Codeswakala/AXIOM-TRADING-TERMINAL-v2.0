"""Seed W7-U03 research collections/tags evidence rows."""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from uuid import uuid4

REPO_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = REPO_ROOT / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from sqlalchemy import func, select

from app.auth.security import hash_password
from app.core.time import utc_now
from app.db.models.audit import AuditEvent
from app.db.models.operator import Operator
from app.db.models.scenario_report import ScenarioReport
from app.db.session import close_db, init_db, session_scope
from app.institutional_platform import ResearchManagementRepository


def _jsonable(value: object) -> object:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, dict):
        return {str(key): _jsonable(nested) for key, nested in value.items()}
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    return value


def _source_hash(report: ScenarioReport) -> str:
    payload = {
        column.name: _jsonable(getattr(report, column.name))
        for column in ScenarioReport.__table__.columns
    }
    encoded = json.dumps(payload, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


async def _operator(session) -> Operator:  # noqa: ANN001
    username = os.environ.get("AXIOM_BOOTSTRAP_ADMIN_USERNAME", "admin")
    existing = (
        await session.scalars(select(Operator).where(Operator.username == username))
    ).one_or_none()
    if existing is not None:
        return existing
    password = os.environ.get("AXIOM_BOOTSTRAP_ADMIN_PASSWORD", "admin123")
    operator = Operator(
        username=username,
        hashed_password=hash_password(password),
        role="admin",
        is_active=True,
        display_name="W7-U03 evidence operator",
    )
    session.add(operator)
    await session.flush()
    return operator


async def _scenario_report(session) -> ScenarioReport:  # noqa: ANN001
    now = utc_now()
    report = ScenarioReport(
        id=str(uuid4()),
        created_at=now,
        artifact_type="scenario_report",
        method_version="w7-u03.evidence.scenario_reference.v1",
        market_class="forex",
        symbol="EURUSD",
        timeframe="M1",
        as_of_start=now,
        as_of_end=now,
        sample_count=3,
        scenario_name=f"w7_u03_reference_scenario_{uuid4().hex[:8]}",
        hypothetical_return=-0.01,
        scenario_result={"hypothetical_return": -0.01},
        assumptions={"scenario_name": "w7_u03_reference_scenario"},
        inputs={"baseline_returns": [0.0, 0.01]},
        uncertainty={"method": "evidence_fixture", "sample_count": 3},
        economic_usefulness={"verdict": "not_assessed"},
        config={"fixture": "reference_only"},
        input_lineage={"policy": "evidence_fixture"},
        source_artifact_ids=[],
        market_scope={"market_class": "forex", "symbol_metadata_only": "EURUSD"},
        results={"scenario_result": {"hypothetical_return": -0.01}},
        limitations=["research_only", "not_a_trade_instruction"],
        report_hash=f"w7u03-{uuid4().hex}",
        research_status="research_only",
        created_by="w7-u03-evidence",
        audit_correlation_id=str(uuid4()),
        notes="Evidence scenario report for W7-U03 no-mutation proof.",
    )
    session.add(report)
    await session.flush()
    session.add(
        AuditEvent(
            category="GOVERNANCE",
            action="scenario_report.created",
            actor="w7-u03-evidence",
            resource_type="scenario_report",
            resource_id=report.id,
            message="W7-U03 evidence source scenario report created",
            details={"artifact_type": "scenario_report", "research_status": "research_only"},
            correlation_id=report.audit_correlation_id,
        )
    )
    await session.flush()
    return report


async def _source_audit_count(session, report_id: str) -> int:  # noqa: ANN001
    return int(
        (
            await session.execute(
                select(func.count())
                .select_from(AuditEvent)
                .where(
                    AuditEvent.resource_type == "scenario_report",
                    AuditEvent.resource_id == report_id,
                )
            )
        ).scalar_one()
    )


async def main() -> None:
    init_db()
    async with session_scope() as session:
        operator = await _operator(session)
        report = await _scenario_report(session)
        before_hash = _source_hash(report)
        before_audit = await _source_audit_count(session, report.id)
        repository = ResearchManagementRepository(session)
        collection = await repository.create_collection(
            operator_id=operator.id,
            payload={
                "name": f"W7-U03 Evidence Collection {uuid4().hex[:8]}",
                "description": "Reference-only governed research collection.",
            },
        )
        member = await repository.add_member(
            collection_id=collection.collection_id,
            operator_id=operator.id,
            payload={"artifact_type": "scenario_report", "artifact_id": report.id},
        )
        tag = await repository.create_tag(
            operator_id=operator.id,
            payload={
                "artifact_type": "scenario_report",
                "artifact_id": report.id,
                "tag": f"w7-u03-evidence-{uuid4().hex[:6]}",
            },
        )
        after = await session.get(ScenarioReport, report.id)
        assert after is not None
        after_hash = _source_hash(after)
        after_audit = await _source_audit_count(session, report.id)
        print("W7_U03_RESEARCH_MANAGEMENT_SEED_COMPLETE")
        print(f"OPERATOR_ID={operator.id}")
        print(f"SCENARIO_REPORT_ID={report.id}")
        print(f"COLLECTION_ID={collection.collection_id}")
        print(f"MEMBER_ID={member.member_id}")
        print(f"TAG_ID={tag.tag_id}")
        print(f"SOURCE_BEFORE_HASH={before_hash}")
        print(f"SOURCE_AFTER_HASH={after_hash}")
        print(f"SOURCE_IDENTITY_UNCHANGED={before_hash == after_hash}")
        print(f"SOURCE_AUDIT_BEFORE={before_audit}")
        print(f"SOURCE_AUDIT_AFTER={after_audit}")
        print(f"SOURCE_AUDIT_UNCHANGED={before_audit == after_audit}")
    await close_db()


if __name__ == "__main__":
    asyncio.run(main())
