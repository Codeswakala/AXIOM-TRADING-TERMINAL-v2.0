"""W5-U06 inert trade plan note tests."""

from __future__ import annotations

from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.collaboration import (
    TRADE_PLAN_RESEARCH_DISCLAIMER,
    TradePlanNoteFactory,
    TradePlanNoteRepository,
)
from app.db.models.advisory_signal import AdvisorySignal
from app.db.models.assistant_research_response import AssistantResearchResponse
from app.db.models.audit import AuditEvent
from app.db.models.trade_plan_note import TradePlanNoteRecord
from app.db.session import session_scope


def _payload(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "title": "Inert research plan",
        "market_context": "EURUSD M1 governed research context.",
        "hypothesis": "Research hypothesis linked to governed evidence.",
        "linked_signal_ids": ["signal-1"],
        "linked_report_ids": ["report-1"],
        "scenario_notes": "Hypothetical research context only.",
        "risk_notes": "Research risk notes only.",
        "invalidating_conditions_text": "Archive if evidence changes.",
        "decision_status": "draft",
    }
    payload.update(overrides)
    return payload


async def _plan(session: AsyncSession, plan_id: str) -> TradePlanNoteRecord:
    plan = await session.get(TradePlanNoteRecord, plan_id)
    assert plan is not None
    return plan


async def _assert_no_orphan_created_audit(session: AsyncSession) -> None:
    stmt = (
        select(TradePlanNoteRecord.plan_id)
        .outerjoin(
            AuditEvent,
            and_(
                AuditEvent.resource_type == "trade_plan_note",
                AuditEvent.resource_id == TradePlanNoteRecord.plan_id,
                AuditEvent.correlation_id == TradePlanNoteRecord.audit_correlation_id,
                AuditEvent.action == "trade_plan_note.created",
            ),
        )
        .where(AuditEvent.id.is_(None))
    )
    assert list((await session.scalars(stmt)).all()) == []


async def _count(session: AsyncSession, model: type[object]) -> int:
    return int((await session.execute(select(func.count()).select_from(model))).scalar_one())


def test_trade_plan_note_contract_rejects_forbidden_fields_recursively() -> None:
    factory = TradePlanNoteFactory()
    forbidden = [
        "order_payload",
        "order_intent",
        "side",
        "quantity",
        "lot_size",
        "order_size",
        "position_size",
        "entry_price_order",
        "stop_loss",
        "take_profit",
        "broker_account_id",
        "account_id",
        "position_id",
        "execution_status",
    ]
    for key in forbidden:
        with pytest.raises(ValueError, match="TRADE_PLAN_FORBIDDEN_FIELD"):
            factory.validate_payload(_payload(linked_report_ids=[{"nested": {key: "blocked"}}]))


def test_trade_plan_note_contract_rejects_unknown_and_guarantee_fields() -> None:
    factory = TradePlanNoteFactory()
    with pytest.raises(ValueError, match="TRADE_PLAN_UNKNOWN_FIELD"):
        factory.validate_payload(_payload(extra_note="not allowed"))
    with pytest.raises(ValueError, match="TRADE_PLAN_FORBIDDEN_TEXT"):
        factory.validate_payload(_payload(hypothesis="guaranteed profit claim"))
    with pytest.raises(ValueError, match="TRADE_PLAN_DECISION_STATUS_INVALID"):
        factory.validate_payload(_payload(decision_status="ready"))


def test_trade_plan_note_schema_is_inert_no_order_ticket_columns() -> None:
    forbidden_columns = {
        "order_payload",
        "order_intent",
        "side",
        "quantity",
        "lot_size",
        "order_size",
        "position_size",
        "entry_price_order",
        "stop_loss",
        "take_profit",
        "broker_account_id",
        "account_id",
        "position_id",
        "execution_status",
        "live_position",
    }
    assert forbidden_columns.isdisjoint(set(TradePlanNoteRecord.__table__.columns.keys()))


@pytest.mark.asyncio
async def test_trade_plan_note_persists_and_audits_no_orphan(prepared_db: None) -> None:
    async with session_scope() as session:
        plan = await TradePlanNoteRepository(session).create_plan(
            payload=_payload(), operator_id="pytest"
        )
        stored = await _plan(session, plan.plan_id)
        assert stored.research_status == "research_only"
        assert stored.decision_status == "draft"
        assert stored.linked_signal_ids == ["signal-1"]
        assert stored.linked_report_ids == ["report-1"]
        assert stored.research_disclaimer == TRADE_PLAN_RESEARCH_DISCLAIMER
        assert "AXIOM does not act" in stored.research_disclaimer
        event = (
            await session.scalars(
                select(AuditEvent).where(
                    AuditEvent.resource_type == "trade_plan_note",
                    AuditEvent.resource_id == stored.plan_id,
                    AuditEvent.action == "trade_plan_note.created",
                )
            )
        ).one()
        assert event.correlation_id == stored.audit_correlation_id
        await _assert_no_orphan_created_audit(session)


@pytest.mark.asyncio
async def test_trade_plan_note_update_is_audited_and_remains_inert(prepared_db: None) -> None:
    async with session_scope() as session:
        repository = TradePlanNoteRepository(session)
        plan = await repository.create_plan(payload=_payload(), operator_id="pytest")
        updated = await repository.update_plan(
            plan_id=plan.plan_id,
            payload=_payload(title="Reviewed research plan", decision_status="reviewed"),
            operator_id="pytest",
        )
        assert updated is not None
        assert updated.title == "Reviewed research plan"
        assert updated.decision_status == "reviewed"
        actions = set(
            (
                await session.scalars(
                    select(AuditEvent.action).where(AuditEvent.resource_id == plan.plan_id)
                )
            ).all()
        )
        assert {"trade_plan_note.created", "trade_plan_note.updated"}.issubset(actions)


@pytest.mark.asyncio
async def test_trade_plan_note_triggers_nothing_beyond_plan_and_audit(prepared_db: None) -> None:
    async with session_scope() as session:
        before_signals = await _count(session, AdvisorySignal)
        before_assistant = await _count(session, AssistantResearchResponse)
        await TradePlanNoteRepository(session).create_plan(payload=_payload(), operator_id="pytest")
        assert await _count(session, AdvisorySignal) == before_signals
        assert await _count(session, AssistantResearchResponse) == before_assistant


def test_trade_plan_note_not_read_by_execution_or_signal_paths() -> None:
    root = Path(__file__).resolve().parents[1] / "app"
    forbidden_roots = [root / "external_integration", root / "trading_intelligence"]
    for folder in forbidden_roots:
        for path in folder.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            assert "trade_plan" not in text
            assert "trade-plans" not in text


async def _auth_headers(async_client: AsyncClient) -> dict[str, str]:
    login = await async_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert login.status_code == 200, login.text
    return {"Authorization": f"Bearer {login.json()['tokens']['access_token']}"}


@pytest.mark.asyncio
async def test_trade_plan_note_api_auth_create_list_detail_update(
    async_client: AsyncClient,
) -> None:
    unauth = await async_client.get("/api/v1/collaboration/trade-plans")
    assert unauth.status_code == 401

    headers = await _auth_headers(async_client)
    create = await async_client.post(
        "/api/v1/collaboration/trade-plans",
        headers=headers,
        json=_payload(),
    )
    assert create.status_code == 201, create.text
    payload = create.json()
    assert payload["research_status"] == "research_only"
    assert payload["research_disclaimer"] == TRADE_PLAN_RESEARCH_DISCLAIMER
    plan_id = payload["plan_id"]

    listing = await async_client.get("/api/v1/collaboration/trade-plans", headers=headers)
    assert listing.status_code == 200, listing.text
    assert any(item["plan_id"] == plan_id for item in listing.json())

    detail = await async_client.get(
        f"/api/v1/collaboration/trade-plans/{plan_id}", headers=headers
    )
    assert detail.status_code == 200, detail.text
    assert detail.json()["linked_signal_ids"] == ["signal-1"]

    update = await async_client.put(
        f"/api/v1/collaboration/trade-plans/{plan_id}",
        headers=headers,
        json=_payload(title="Archived research plan", decision_status="archived"),
    )
    assert update.status_code == 200, update.text
    assert update.json()["decision_status"] == "archived"


@pytest.mark.asyncio
async def test_trade_plan_note_api_rejects_forbidden_payload_and_has_no_exec_endpoint(
    async_client: AsyncClient,
) -> None:
    headers = await _auth_headers(async_client)
    forbidden_payload = _payload()
    forbidden_payload["order_payload"] = {"blocked": True}
    response = await async_client.post(
        "/api/v1/collaboration/trade-plans",
        headers=headers,
        json=forbidden_payload,
    )
    assert response.status_code == 422

    create = await async_client.post(
        "/api/v1/collaboration/trade-plans",
        headers=headers,
        json=_payload(),
    )
    assert create.status_code == 201, create.text
    plan_id = create.json()["plan_id"]
    for suffix in ("execute", "submit", "emit-signal"):
        blocked = await async_client.post(
            f"/api/v1/collaboration/trade-plans/{plan_id}/{suffix}",
            headers=headers,
            json={},
        )
        assert blocked.status_code in {404, 405}
