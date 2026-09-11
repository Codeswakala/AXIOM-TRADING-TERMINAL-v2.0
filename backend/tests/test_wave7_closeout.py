"""W7-U08 Wave-7 closeout and whole-project completion tests."""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

import pytest
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import hash_password
from app.core.time import utc_now
from app.db.models.audit import AuditEvent
from app.db.models.operator import Operator
from app.db.models.operator_workspace_preference import OperatorWorkspacePreference
from app.db.models.research_management import (
    ResearchCollection,
    ResearchCollectionMember,
    ResearchTag,
)
from app.db.models.scenario_report import ScenarioReport
from app.db.session import session_scope
from app.institutional_platform import ResearchManagementRepository, WorkspacePreferenceRepository


def _app_root() -> Path:
    return Path(__file__).resolve().parents[1] / "app"


def test_wave7_bright_line_grep_no_execution_or_gate_path() -> None:
    root = _app_root()
    paths = [root / "institutional_platform", root / "api" / "routes" / "institutional_platform.py"]
    # Guardrail-validation modules intentionally contain forbidden marker constants.
    allowed_constant_files = {
        "institutional_platform/preferences.py",
        "institutional_platform/research_management.py",
        "institutional_platform/rbac.py",
    }
    forbidden = (
        "place_order",
        "broker.connect",
        "broker.execute",
        "go_live",
        "order_routing",
        "account_balance",
        "gate_open",
        "live_order",
        "real_money",
        "plugin_execution_audit_events",
    )
    offenders: list[str] = []
    for item in paths:
        files = item.rglob("*.py") if item.is_dir() else [item]
        for path in files:
            rel = path.relative_to(root).as_posix()
            if rel in allowed_constant_files:
                continue
            text = path.read_text(encoding="utf-8")
            for needle in forbidden:
                if needle in text:
                    offenders.append(f"{rel}:{needle}")
    assert offenders == []


def test_gate_remains_closed_across_all_waves() -> None:
    from app.external_integration.broker import governance_gate

    assert governance_gate.broker_integration_authorized is False
    assert governance_gate.execution_authorized is False
    assert governance_gate.broker_integration_authorized is governance_gate.execution_authorized


def test_broker_logic_contained_in_external_integration() -> None:
    root = _app_root()
    broker_specific = (
        "MetaTrader5",
        "MqlTrade",
        "TRADE_ACTION",
        "ORDER_TYPE",
        "BrokerClient",
        "broker_endpoint",
        "broker_credentials",
    )
    offenders: list[str] = []
    for path in root.rglob("*.py"):
        rel = path.relative_to(root).as_posix()
        if rel.startswith("external_integration/"):
            continue
        if rel.startswith("v2/broker_read/providers/"):
            # BO-V2-BE-9-001 D-1 sanctioned adapter location
            continue
        text = path.read_text(encoding="utf-8")
        for needle in broker_specific:
            if needle in text:
                offenders.append(f"{rel}:{needle}")
    assert offenders == []


async def _operator(session: AsyncSession) -> Operator:
    operator = Operator(
        username=f"wave7-closeout-{uuid4().hex[:10]}",
        hashed_password=hash_password("operator-pass-123"),
        role="operator",
        is_active=True,
    )
    session.add(operator)
    await session.flush()
    return operator


async def _scenario_report(session: AsyncSession) -> ScenarioReport:
    now = utc_now()
    report = ScenarioReport(
        id=str(uuid4()),
        created_at=now,
        artifact_type="scenario_report",
        method_version="w7-u08.closeout.scenario_reference.v1",
        market_class="forex",
        symbol="EURUSD",
        timeframe="M1",
        as_of_start=now,
        as_of_end=now,
        sample_count=3,
        scenario_name="w7_u08_closeout_reference",
        hypothetical_return=-0.01,
        scenario_result={"hypothetical_return": -0.01},
        assumptions={"scenario_name": "w7_u08_closeout_reference"},
        inputs={"baseline_returns": [0.0, 0.01]},
        uncertainty={"method": "closeout_fixture", "sample_count": 3},
        economic_usefulness={"verdict": "not_assessed"},
        config={"fixture": "w7-u08"},
        input_lineage={"policy": "closeout_fixture"},
        source_artifact_ids=[],
        market_scope={"market_class": "forex"},
        results={"scenario_result": {"hypothetical_return": -0.01}},
        limitations=["research_only"],
        report_hash=f"w7u08-{uuid4().hex}",
        research_status="research_only",
        created_by="pytest",
        audit_correlation_id=str(uuid4()),
        notes="Wave-7 closeout reference artifact.",
    )
    session.add(report)
    await session.flush()
    return report


async def _seed_wave7_artifacts(session: AsyncSession) -> dict[str, object]:
    operator = await _operator(session)
    scenario = await _scenario_report(session)
    preference = await WorkspacePreferenceRepository(session).create_preference(
        operator_id=operator.id,
        payload={
            "workspace_key": f"closeout-{uuid4().hex[:8]}",
            "layout_config": {"density": "comfortable"},
            "visible_modules": ["operations"],
            "theme_config": {"mode": "dark"},
            "metadata": {"note": "wave7 closeout"},
        },
    )
    repo = ResearchManagementRepository(session)
    collection = await repo.create_collection(
        operator_id=operator.id,
        payload={"name": f"Wave7 Closeout {uuid4().hex[:8]}"},
    )
    member = await repo.add_member(
        collection_id=collection.collection_id,
        operator_id=operator.id,
        payload={"artifact_type": "scenario_report", "artifact_id": scenario.id},
    )
    tag = await repo.create_tag(
        operator_id=operator.id,
        payload={"artifact_type": "scenario_report", "artifact_id": scenario.id, "tag": "closeout"},
    )
    return {
        "preference": preference,
        "collection": collection,
        "member": member,
        "tag": tag,
    }


async def _assert_no_orphan(
    session: AsyncSession,
    *,
    model: type,
    id_attr: str,
    resource_type: str,
    action: str,
) -> None:
    stmt = (
        select(getattr(model, id_attr))
        .outerjoin(
            AuditEvent,
            and_(
                AuditEvent.resource_type == resource_type,
                AuditEvent.resource_id == getattr(model, id_attr),
                AuditEvent.correlation_id == model.audit_correlation_id,
                AuditEvent.action == action,
            ),
        )
        .where(AuditEvent.id.is_(None))
    )
    assert list((await session.scalars(stmt)).all()) == []


@pytest.mark.asyncio
async def test_all_wave7_tables_audited_no_orphan(prepared_db: None) -> None:
    async with session_scope() as session:
        await _seed_wave7_artifacts(session)
        checks = [
            (
                OperatorWorkspacePreference,
                "preference_id",
                "operator_workspace_preference",
                "operator_workspace_preference.created",
            ),
            (
                ResearchCollection,
                "collection_id",
                "research_collection",
                "research_collection.created",
            ),
            (
                ResearchCollectionMember,
                "member_id",
                "research_collection_member",
                "research_collection_member.created",
            ),
            (ResearchTag, "tag_id", "research_tag", "research_tag.created"),
        ]
        for model, id_attr, resource_type, action in checks:
            count = len(list((await session.scalars(select(getattr(model, id_attr)))).all()))
            assert count >= 1
            await _assert_no_orphan(
                session,
                model=model,
                id_attr=id_attr,
                resource_type=resource_type,
                action=action,
            )


def test_platform_completion_reconciles_all_milestones_gate_closed() -> None:
    root = Path(__file__).resolve().parents[2]
    milestone_files = {
        "Professional Advisor Platform Complete": root
        / "docs"
        / "build-orders"
        / "ITRGA_VERDICT_W3-U08_FINAL_AND_WAVE3_CLOSURE.md",
        "Institutional Intelligence Layer Complete": root
        / "docs"
        / "build-orders"
        / "ITRGA_VERDICT_W4-U08_FINAL_AND_WAVE4_CLOSURE.md",
        "Human-AI Collaborative Workspace Complete": root
        / "docs"
        / "build-orders"
        / "ITRGA_VERDICT_W5-U08_FINAL_AND_WAVE5_CLOSURE.md",
        "Execution Research Environment": root
        / "docs"
        / "build-orders"
        / "ITRGA_VERDICT_W6-U08_FINAL_AND_WAVE6_CLOSURE.md",
    }
    for milestone, path in milestone_files.items():
        assert path.is_file(), path
        text = path.read_text(encoding="utf-8")
        assert milestone.lower() in text.lower()
        assert "closed" in text.lower()

    from app import __version__
    from app.external_integration.broker import governance_gate

    assert __version__ == "0.62.0"
    assert governance_gate.broker_integration_authorized is False
    assert governance_gate.execution_authorized is False
