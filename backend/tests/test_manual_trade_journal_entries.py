"""W5-U07 inert manual research journal tests."""

from __future__ import annotations

from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.collaboration import (
    JOURNAL_RESEARCH_DISCLAIMER,
    ManualJournalEntryFactory,
    ManualJournalEntryRepository,
)
from app.db.models.advisory_signal import AdvisorySignal
from app.db.models.assistant_research_response import AssistantResearchResponse
from app.db.models.audit import AuditEvent
from app.db.models.manual_trade_journal_entry import ManualTradeJournalEntryRecord
from app.db.session import session_scope


def _payload(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "title": "Manual research reflection",
        "reflection_text": "Reviewed reasoning and process lessons only.",
        "linked_plan_id": "plan-1",
        "linked_signal_ids": ["signal-1"],
        "linked_report_ids": ["report-1"],
        "emotion_tags": ["calm"],
        "process_tags": ["checklist"],
        "lesson_notes": "Keep reflections separate from external records.",
    }
    payload.update(overrides)
    return payload


async def _entry(session: AsyncSession, journal_id: str) -> ManualTradeJournalEntryRecord:
    entry = await session.get(ManualTradeJournalEntryRecord, journal_id)
    assert entry is not None
    return entry


async def _assert_no_orphan_created_audit(session: AsyncSession) -> None:
    stmt = (
        select(ManualTradeJournalEntryRecord.journal_id)
        .outerjoin(
            AuditEvent,
            and_(
                AuditEvent.resource_type == "manual_trade_journal_entry",
                AuditEvent.resource_id == ManualTradeJournalEntryRecord.journal_id,
                AuditEvent.correlation_id == ManualTradeJournalEntryRecord.audit_correlation_id,
                AuditEvent.action == "manual_trade_journal_entry.created",
            ),
        )
        .where(AuditEvent.id.is_(None))
    )
    assert list((await session.scalars(stmt)).all()) == []


async def _count(session: AsyncSession, model: type[object]) -> int:
    return int((await session.execute(select(func.count()).select_from(model))).scalar_one())


def test_manual_journal_contract_rejects_forbidden_fields_recursively() -> None:
    factory = ManualJournalEntryFactory()
    forbidden = [
        "order_payload",
        "order_intent",
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
        "fill_price",
        "pnl",
        "realized_return",
    ]
    for key in forbidden:
        with pytest.raises(ValueError, match="JOURNAL_FORBIDDEN_FIELD"):
            factory.validate_payload(_payload(process_tags=[{"nested": {key: "blocked"}}]))


def test_manual_journal_contract_rejects_pnl_and_broker_import_text() -> None:
    factory = ManualJournalEntryFactory()
    for text in ("broker import attempted", "fill price noted", "P&L claim", "realized return"):
        with pytest.raises(ValueError, match="JOURNAL_FORBIDDEN_TEXT"):
            factory.validate_payload(_payload(reflection_text=text))
    with pytest.raises(ValueError, match="JOURNAL_UNKNOWN_FIELD"):
        factory.validate_payload(_payload(external_record="not allowed"))


def test_manual_journal_schema_is_inert_no_broker_or_execution_columns() -> None:
    forbidden_columns = {
        "broker_account_id",
        "account_id",
        "execution_id",
        "execution_status",
        "fill_id",
        "fill_price",
        "fill_quantity",
        "order_payload",
        "order_intent",
        "quantity",
        "lot_size",
        "order_size",
        "position_size",
        "stop_loss",
        "take_profit",
        "pnl",
        "realized_return",
    }
    assert forbidden_columns.isdisjoint(set(ManualTradeJournalEntryRecord.__table__.columns.keys()))


@pytest.mark.asyncio
async def test_manual_journal_entry_persists_and_audits_no_orphan(prepared_db: None) -> None:
    async with session_scope() as session:
        entry = await ManualJournalEntryRepository(session).create_entry(
            payload=_payload(), operator_id="pytest"
        )
        stored = await _entry(session, entry.journal_id)
        assert stored.research_status == "research_only"
        assert stored.linked_plan_id == "plan-1"
        assert stored.linked_signal_ids == ["signal-1"]
        assert stored.linked_report_ids == ["report-1"]
        assert stored.emotion_tags == ["calm"]
        assert stored.process_tags == ["checklist"]
        assert stored.research_disclaimer == JOURNAL_RESEARCH_DISCLAIMER
        assert "AXIOM does not act" in stored.research_disclaimer
        event = (
            await session.scalars(
                select(AuditEvent).where(
                    AuditEvent.resource_type == "manual_trade_journal_entry",
                    AuditEvent.resource_id == stored.journal_id,
                    AuditEvent.action == "manual_trade_journal_entry.created",
                )
            )
        ).one()
        assert event.correlation_id == stored.audit_correlation_id
        await _assert_no_orphan_created_audit(session)


@pytest.mark.asyncio
async def test_manual_journal_entry_update_is_audited_and_remains_inert(prepared_db: None) -> None:
    async with session_scope() as session:
        repository = ManualJournalEntryRepository(session)
        entry = await repository.create_entry(payload=_payload(), operator_id="pytest")
        updated = await repository.update_entry(
            journal_id=entry.journal_id,
            payload=_payload(title="Updated research reflection", process_tags=["reviewed"]),
            operator_id="pytest",
        )
        assert updated is not None
        assert updated.title == "Updated research reflection"
        assert updated.process_tags == ["reviewed"]
        actions = set(
            (
                await session.scalars(
                    select(AuditEvent.action).where(AuditEvent.resource_id == entry.journal_id)
                )
            ).all()
        )
        expected = {"manual_trade_journal_entry.created", "manual_trade_journal_entry.updated"}
        assert expected.issubset(actions)


@pytest.mark.asyncio
async def test_manual_journal_entry_triggers_nothing_beyond_entry_and_audit(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        before_signals = await _count(session, AdvisorySignal)
        before_assistant = await _count(session, AssistantResearchResponse)
        await ManualJournalEntryRepository(session).create_entry(
            payload=_payload(), operator_id="pytest"
        )
        assert await _count(session, AdvisorySignal) == before_signals
        assert await _count(session, AssistantResearchResponse) == before_assistant


def test_manual_journal_entry_not_read_by_execution_or_signal_paths() -> None:
    root = Path(__file__).resolve().parents[1] / "app"
    forbidden_roots = [root / "external_integration", root / "trading_intelligence"]
    for folder in forbidden_roots:
        for path in folder.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            assert "manual_trade_journal" not in text
            assert "journal-entries" not in text


async def _auth_headers(async_client: AsyncClient) -> dict[str, str]:
    login = await async_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert login.status_code == 200, login.text
    return {"Authorization": f"Bearer {login.json()['tokens']['access_token']}"}


@pytest.mark.asyncio
async def test_manual_journal_api_auth_create_list_detail_update(async_client: AsyncClient) -> None:
    unauth = await async_client.get("/api/v1/collaboration/journal-entries")
    assert unauth.status_code == 401

    headers = await _auth_headers(async_client)
    create = await async_client.post(
        "/api/v1/collaboration/journal-entries",
        headers=headers,
        json=_payload(),
    )
    assert create.status_code == 201, create.text
    payload = create.json()
    assert payload["research_status"] == "research_only"
    assert payload["research_disclaimer"] == JOURNAL_RESEARCH_DISCLAIMER
    journal_id = payload["journal_id"]

    listing = await async_client.get("/api/v1/collaboration/journal-entries", headers=headers)
    assert listing.status_code == 200, listing.text
    assert any(item["journal_id"] == journal_id for item in listing.json())

    detail = await async_client.get(
        f"/api/v1/collaboration/journal-entries/{journal_id}", headers=headers
    )
    assert detail.status_code == 200, detail.text
    assert detail.json()["linked_plan_id"] == "plan-1"

    update = await async_client.put(
        f"/api/v1/collaboration/journal-entries/{journal_id}",
        headers=headers,
        json=_payload(title="Updated journal reflection", emotion_tags=["focused"]),
    )
    assert update.status_code == 200, update.text
    assert update.json()["emotion_tags"] == ["focused"]


@pytest.mark.asyncio
async def test_manual_journal_api_rejects_forbidden_payload_and_has_no_exec_endpoint(
    async_client: AsyncClient,
) -> None:
    headers = await _auth_headers(async_client)
    forbidden_payload = _payload()
    forbidden_payload["execution_id"] = "blocked"
    response = await async_client.post(
        "/api/v1/collaboration/journal-entries",
        headers=headers,
        json=forbidden_payload,
    )
    assert response.status_code == 422

    create = await async_client.post(
        "/api/v1/collaboration/journal-entries",
        headers=headers,
        json=_payload(),
    )
    assert create.status_code == 201, create.text
    journal_id = create.json()["journal_id"]
    for suffix in ("execute", "submit", "emit-signal"):
        blocked = await async_client.post(
            f"/api/v1/collaboration/journal-entries/{journal_id}/{suffix}",
            headers=headers,
            json={},
        )
        assert blocked.status_code in {404, 405}
