"""W7-U03 research management collections and tags tests."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from uuid import uuid4

import pytest
from httpx import AsyncClient
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import hash_password
from app.core.time import utc_now
from app.db.models.audit import AuditEvent
from app.db.models.operator import Operator
from app.db.models.research_management import (
    ResearchCollection,
    ResearchCollectionMember,
    ResearchTag,
)
from app.db.models.scenario_report import ScenarioReport
from app.db.session import session_scope
from app.institutional_platform import ResearchManagementFactory, ResearchManagementRepository


def _collection_payload(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "name": f"Scenario Research {uuid4().hex[:8]}",
        "description": "Reference-only collection for governed research artifacts.",
    }
    payload.update(overrides)
    return payload


def _member_payload(report: ScenarioReport) -> dict[str, object]:
    return {"artifact_type": "scenario_report", "artifact_id": report.id}


def _tag_payload(report: ScenarioReport, *, tag: str = "scenario-review") -> dict[str, object]:
    return {"artifact_type": "scenario_report", "artifact_id": report.id, "tag": tag}


async def _operator(session: AsyncSession, *, role: str = "operator") -> Operator:
    operator = Operator(
        username=f"research-mgmt-{role}-{uuid4().hex[:10]}",
        hashed_password=hash_password("operator-pass-123"),
        role=role,
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
        method_version="w7-u03.test.scenario_reference.v1",
        market_class="forex",
        symbol="EURUSD",
        timeframe="M1",
        as_of_start=now,
        as_of_end=now,
        sample_count=3,
        scenario_name="w7_u03_reference_scenario",
        hypothetical_return=-0.01,
        scenario_result={"hypothetical_return": -0.01},
        assumptions={"scenario_name": "w7_u03_reference_scenario"},
        inputs={"baseline_returns": [0.0, 0.01]},
        uncertainty={"method": "test_fixture", "sample_count": 3},
        economic_usefulness={"verdict": "not_assessed"},
        config={"fixture": "reference_only"},
        input_lineage={"policy": "test_fixture"},
        source_artifact_ids=[],
        market_scope={"market_class": "forex", "symbol_metadata_only": "EURUSD"},
        results={"scenario_result": {"hypothetical_return": -0.01}},
        limitations=["research_only", "not_a_trade_instruction"],
        report_hash=f"hash-{uuid4().hex}",
        research_status="research_only",
        created_by="pytest",
        audit_correlation_id=str(uuid4()),
        notes="Fixture scenario report used as a real governed source artifact.",
    )
    session.add(report)
    await session.flush()
    session.add(
        AuditEvent(
            category="GOVERNANCE",
            action="scenario_report.created",
            actor="pytest",
            resource_type="scenario_report",
            resource_id=report.id,
            message="Scenario report fixture created for W7-U03 source identity proof",
            details={"artifact_type": "scenario_report", "research_status": "research_only"},
            correlation_id=report.audit_correlation_id,
        )
    )
    await session.flush()
    return report


def _jsonable(value: object) -> object:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, dict):
        return {str(key): _jsonable(nested) for key, nested in value.items()}
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    return value


def _scenario_identity(report: ScenarioReport) -> str:
    identity = {
        column.name: _jsonable(getattr(report, column.name))
        for column in ScenarioReport.__table__.columns
    }
    return json.dumps(identity, sort_keys=True)


async def _assert_create_audit_no_orphan(
    session: AsyncSession, *, model: type, resource_type: str, id_attr: str
) -> None:
    stmt = (
        select(getattr(model, id_attr))
        .outerjoin(
            AuditEvent,
            and_(
                AuditEvent.resource_type == resource_type,
                AuditEvent.resource_id == getattr(model, id_attr),
                AuditEvent.correlation_id == model.audit_correlation_id,
                AuditEvent.action == f"{resource_type}.created",
            ),
        )
        .where(AuditEvent.id.is_(None))
    )
    assert list((await session.scalars(stmt)).all()) == []


async def _assert_operator_no_orphan(session: AsyncSession, *, model: type, id_attr: str) -> None:
    stmt = (
        select(getattr(model, id_attr))
        .outerjoin(Operator, Operator.id == model.operator_id)
        .where(Operator.id.is_(None))
    )
    assert list((await session.scalars(stmt)).all()) == []


@pytest.mark.asyncio
async def test_research_collection_persists_and_audit_no_orphan(prepared_db: None) -> None:
    async with session_scope() as session:
        operator = await _operator(session)
        collection = await ResearchManagementRepository(session).create_collection(
            operator_id=operator.id, payload=_collection_payload(name="Macro Scenarios")
        )
        assert collection.research_status == "research_only"
        assert collection.operator_id == operator.id
        await _assert_create_audit_no_orphan(
            session,
            model=ResearchCollection,
            resource_type="research_collection",
            id_attr="collection_id",
        )
        await _assert_operator_no_orphan(session, model=ResearchCollection, id_attr="collection_id")


@pytest.mark.asyncio
async def test_research_collection_member_persists_and_audit_no_orphan(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        operator = await _operator(session)
        report = await _scenario_report(session)
        repository = ResearchManagementRepository(session)
        collection = await repository.create_collection(
            operator_id=operator.id, payload=_collection_payload(name="Scenario Set")
        )
        member = await repository.add_member(
            collection_id=collection.collection_id,
            operator_id=operator.id,
            payload=_member_payload(report),
        )
        assert member.artifact_type == "scenario_report"
        assert member.artifact_id == report.id
        await _assert_create_audit_no_orphan(
            session,
            model=ResearchCollectionMember,
            resource_type="research_collection_member",
            id_attr="member_id",
        )
        await _assert_operator_no_orphan(
            session, model=ResearchCollectionMember, id_attr="member_id"
        )


@pytest.mark.asyncio
async def test_research_tag_persists_and_audit_no_orphan(prepared_db: None) -> None:
    async with session_scope() as session:
        operator = await _operator(session)
        report = await _scenario_report(session)
        tag = await ResearchManagementRepository(session).create_tag(
            operator_id=operator.id, payload=_tag_payload(report, tag="macro-shock")
        )
        assert tag.artifact_type == "scenario_report"
        assert tag.artifact_id == report.id
        await _assert_create_audit_no_orphan(
            session,
            model=ResearchTag,
            resource_type="research_tag",
            id_attr="tag_id",
        )
        await _assert_operator_no_orphan(session, model=ResearchTag, id_attr="tag_id")


@pytest.mark.asyncio
async def test_tagging_or_collecting_does_not_mutate_source_artifact_or_its_audit(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        operator = await _operator(session)
        report = await _scenario_report(session)
        report_id = report.id
        before_identity = _scenario_identity(report)
        before_audit_count = (
            await session.execute(
                select(func.count())
                .select_from(AuditEvent)
                .where(
                    AuditEvent.resource_type == "scenario_report",
                    AuditEvent.resource_id == report_id,
                )
            )
        ).scalar_one()
        repository = ResearchManagementRepository(session)
        collection = await repository.create_collection(
            operator_id=operator.id, payload=_collection_payload(name="Source Identity Proof")
        )
        await repository.add_member(
            collection_id=collection.collection_id,
            operator_id=operator.id,
            payload=_member_payload(report),
        )
        await repository.create_tag(
            operator_id=operator.id,
            payload=_tag_payload(report, tag="source-unchanged"),
        )
        after = await session.get(ScenarioReport, report_id)
        assert after is not None
        after_identity = _scenario_identity(after)
        after_audit_count = (
            await session.execute(
                select(func.count())
                .select_from(AuditEvent)
                .where(
                    AuditEvent.resource_type == "scenario_report",
                    AuditEvent.resource_id == report_id,
                )
            )
        ).scalar_one()
        assert after_identity == before_identity
        assert after_audit_count == before_audit_count


@pytest.mark.asyncio
async def test_research_management_is_operator_scoped_two_operator_isolation(
    async_client: AsyncClient,
) -> None:
    async with session_scope() as session:
        operator_a = await _operator(session)
        operator_b = await _operator(session)
        report_a = await _scenario_report(session)
        report_b = await _scenario_report(session)
        repository = ResearchManagementRepository(session)
        collection_a = await repository.create_collection(
            operator_id=operator_a.id, payload=_collection_payload(name="A Collection")
        )
        collection_b = await repository.create_collection(
            operator_id=operator_b.id, payload=_collection_payload(name="B Collection")
        )
        await repository.add_member(
            collection_id=collection_a.collection_id,
            operator_id=operator_a.id,
            payload=_member_payload(report_a),
        )
        await repository.add_member(
            collection_id=collection_b.collection_id,
            operator_id=operator_b.id,
            payload=_member_payload(report_b),
        )
        tag_a = await repository.create_tag(
            operator_id=operator_a.id, payload=_tag_payload(report_a, tag="a-only")
        )
        tag_b = await repository.create_tag(
            operator_id=operator_b.id, payload=_tag_payload(report_b, tag="b-only")
        )
        a_id = operator_a.id
        b_id = operator_b.id
        username_b = operator_b.username
        collection_a_id = collection_a.collection_id
        collection_b_id = collection_b.collection_id
        tag_a_id = tag_a.tag_id
        tag_b_id = tag_b.tag_id

    headers_b = await _headers(async_client, username_b)
    list_b = await async_client.get(
        "/api/v1/institutional-platform/research-collections", headers=headers_b
    )
    assert list_b.status_code == 200, list_b.text
    assert not any(item["collection_id"] == collection_a_id for item in list_b.json())
    assert any(item["collection_id"] == collection_b_id for item in list_b.json())
    assert not any(item["operator_id"] == a_id for item in list_b.json())
    assert all(item["operator_id"] == b_id for item in list_b.json())

    read_a_collection = await async_client.get(
        f"/api/v1/institutional-platform/research-collections/{collection_a_id}",
        headers=headers_b,
    )
    assert read_a_collection.status_code == 403

    mutate_a_collection = await async_client.post(
        f"/api/v1/institutional-platform/research-collections/{collection_a_id}/members",
        headers=headers_b,
        json={"artifact_type": "scenario_report", "artifact_id": str(uuid4())},
    )
    assert mutate_a_collection.status_code == 403

    tag_list_b = await async_client.get(
        "/api/v1/institutional-platform/research-tags", headers=headers_b
    )
    assert tag_list_b.status_code == 200, tag_list_b.text
    assert not any(item["tag_id"] == tag_a_id for item in tag_list_b.json())
    assert any(item["tag_id"] == tag_b_id for item in tag_list_b.json())

    read_a_tag = await async_client.get(
        f"/api/v1/institutional-platform/research-tags/{tag_a_id}", headers=headers_b
    )
    assert read_a_tag.status_code == 403
    delete_a_tag = await async_client.delete(
        f"/api/v1/institutional-platform/research-tags/{tag_a_id}", headers=headers_b
    )
    assert delete_a_tag.status_code == 403

    async with session_scope() as session:
        b_rows_for_a_collection = (
            await session.execute(
                select(func.count())
                .select_from(ResearchCollection)
                .where(
                    ResearchCollection.operator_id == b_id,
                    ResearchCollection.collection_id == collection_a_id,
                )
            )
        ).scalar_one()
        b_rows_for_a_tag = (
            await session.execute(
                select(func.count())
                .select_from(ResearchTag)
                .where(ResearchTag.operator_id == b_id, ResearchTag.tag_id == tag_a_id)
            )
        ).scalar_one()
    assert b_rows_for_a_collection == 0
    assert b_rows_for_a_tag == 0


@pytest.mark.asyncio
async def test_cross_operator_mutation_returns_403_before_body_validation(
    async_client: AsyncClient,
) -> None:
    async with session_scope() as session:
        operator_a = await _operator(session)
        operator_b = await _operator(session)
        repository = ResearchManagementRepository(session)
        collection_a = await repository.create_collection(
            operator_id=operator_a.id, payload=_collection_payload(name="Authorize First")
        )
        username_b = operator_b.username
        collection_a_id = collection_a.collection_id

    headers_b = await _headers(async_client, username_b)
    response = await async_client.post(
        f"/api/v1/institutional-platform/research-collections/{collection_a_id}/members",
        headers=headers_b,
        json={},
    )
    assert response.status_code == 403, response.text


@pytest.mark.asyncio
async def test_research_management_requires_auth(async_client: AsyncClient) -> None:
    unauth = await async_client.get("/api/v1/institutional-platform/research-collections")
    assert unauth.status_code == 401
    unauth_tags = await async_client.get("/api/v1/institutional-platform/research-tags")
    assert unauth_tags.status_code == 401

    async with session_scope() as session:
        operator = await _operator(session)
        report = await _scenario_report(session)
        username = operator.username
        report_id = report.id
    headers = await _headers(async_client, username)
    create = await async_client.post(
        "/api/v1/institutional-platform/research-collections",
        headers=headers,
        json={"name": "Auth Proof", "description": "created through API"},
    )
    assert create.status_code == 201, create.text
    collection_id = create.json()["collection_id"]
    member = await async_client.post(
        f"/api/v1/institutional-platform/research-collections/{collection_id}/members",
        headers=headers,
        json={"artifact_type": "scenario_report", "artifact_id": report_id},
    )
    assert member.status_code == 201, member.text
    tag = await async_client.post(
        "/api/v1/institutional-platform/research-tags",
        headers=headers,
        json={"artifact_type": "scenario_report", "artifact_id": report_id, "tag": "api-auth"},
    )
    assert tag.status_code == 201, tag.text


def test_research_management_tables_have_no_forbidden_or_source_content_columns() -> None:
    forbidden = {
        "order_payload",
        "order_intent",
        "broker_account_id",
        "account_id",
        "position_id",
        "live_position_id",
        "execution_status",
        "real_pnl",
        "pnl",
        "balance",
        "margin",
        "capital",
        "gate_state",
        "open_gate",
        "allow_execution",
        "source_artifact_content",
        "materialized_source_content",
    }
    for model in (ResearchCollection, ResearchCollectionMember, ResearchTag):
        assert set(model.__table__.columns.keys()).isdisjoint(forbidden)
    factory = ResearchManagementFactory()
    with pytest.raises(ValueError, match="RESEARCH_MANAGEMENT_FORBIDDEN_FIELD"):
        factory.collection_from_payload({"name": "bad", "source_artifact_content": "blocked"})
    with pytest.raises(ValueError, match="RESEARCH_MANAGEMENT_FORBIDDEN_FIELD"):
        factory.tag_from_payload(
            {"artifact_type": "scenario_report", "artifact_id": "id", "tag": "x", "pnl": 1}
        )


def test_research_management_has_no_secret_or_pii_markers() -> None:
    factory = ResearchManagementFactory()
    for marker in ("access_token", "refresh_token", "jwt", "password", "secret", "api_key"):
        with pytest.raises(ValueError, match="RESEARCH_MANAGEMENT_SECRET_OR_PII_MARKER"):
            factory.collection_from_payload({"name": f"contains {marker}"})
        with pytest.raises(ValueError, match="RESEARCH_MANAGEMENT_SECRET_OR_PII_MARKER"):
            factory.tag_from_payload(
                {
                    "artifact_type": "scenario_report",
                    "artifact_id": "scenario-1",
                    "tag": f"contains {marker}",
                }
            )


def test_gate_remains_closed_for_wave7() -> None:
    from app.external_integration.broker import governance_gate

    assert governance_gate.broker_integration_authorized is False
    assert governance_gate.execution_authorized is False


def test_research_management_page_has_no_forbidden_controls() -> None:
    root = Path(__file__).resolve().parents[2]
    # UI-CONV-P03 item 4: the UI-006 explorer relocated from
    # frontend/src/pages/ResearchManagementPage.tsx into the terminal research
    # stage view module. The guard pins the re-homed source, and the
    # non-vacuity assertion proves it is pinning the explorer itself (a guard
    # re-pointed to a file without the investigation UI would pass vacuously).
    page = (
        root
        / "frontend"
        / "src"
        / "components"
        / "terminal"
        / "research"
        / "ResearchHubView.tsx"
    )
    text = page.read_text(encoding="utf-8").lower()
    assert "unified research artifact explorer" in text
    forbidden = (
        "place_order",
        "submit order",
        "go live",
        "connect broker",
        "account_id",
        "order_ticket",
        "broker_account",
    )
    assert all(item not in text for item in forbidden)


async def _headers(async_client: AsyncClient, username: str) -> dict[str, str]:
    login = await async_client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": "operator-pass-123"},
    )
    assert login.status_code == 200, login.text
    return {"Authorization": f"Bearer {login.json()['tokens']['access_token']}"}
