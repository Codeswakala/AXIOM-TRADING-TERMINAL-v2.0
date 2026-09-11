"""W5-U02 audited assistant research-response persistence tests."""

from __future__ import annotations

import pytest
from httpx import AsyncClient
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.collaboration import (
    ASSISTANT_RESEARCH_DISCLAIMER,
    DEFAULT_ASSISTANT_TOOL_REGISTRY,
    AssistantRequest,
    GroundingBundle,
    NullAssistant,
    RuleBasedGroundedAssistant,
    sanitized_output_contains_secret_marker,
)
from app.db.models.assistant_research_response import AssistantResearchResponse
from app.db.models.audit import AuditEvent
from app.db.session import session_scope


def _request(prompt: str, *, grounded: bool = True) -> AssistantRequest:
    grounding = (
        GroundingBundle(
            source_artifact_ids=("signal-1", "report-1"),
            summaries=("Signal was withheld by guardrail.", "Report status is research_only."),
        )
        if grounded
        else GroundingBundle(source_artifact_ids=(), summaries=())
    )
    return AssistantRequest(prompt=prompt, operator_id="pytest", grounding=grounding)


async def _stored(
    session: AsyncSession, response_id: str
) -> AssistantResearchResponse:
    record = await session.get(AssistantResearchResponse, response_id)
    assert record is not None
    return record


async def _audit_event(session: AsyncSession, response_id: str) -> AuditEvent:
    stmt = select(AuditEvent).where(
        AuditEvent.resource_type == "assistant_response",
        AuditEvent.resource_id == response_id,
    )
    event = (await session.scalars(stmt)).one()
    return event


async def _assert_no_orphan_audit(session: AsyncSession) -> None:
    stmt = (
        select(AssistantResearchResponse.assistant_response_id)
        .outerjoin(
            AuditEvent,
            and_(
                AuditEvent.resource_type == "assistant_response",
                AuditEvent.resource_id == AssistantResearchResponse.assistant_response_id,
                AuditEvent.correlation_id == AssistantResearchResponse.audit_correlation_id,
                AuditEvent.action.in_(
                    ["assistant.response_draft_created", "assistant.refused"]
                ),
            ),
        )
        .where(AuditEvent.id.is_(None))
    )
    assert list((await session.scalars(stmt)).all()) == []


@pytest.mark.asyncio
async def test_assistant_research_response_persists_grounded_response_and_audit_no_orphan(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        response = await RuleBasedGroundedAssistant(session).respond(
            _request("Summarize the governed evidence")
        )
        record = await _stored(session, response.response_id)
        event = await _audit_event(session, response.response_id)

        assert record.refused is False
        assert record.research_status == "research_only"
        assert record.request_id == response.request_id
        assert record.request_text_hash != response.request_id
        assert len(record.request_text_hash) == 64
        assert record.source_artifact_ids == ["signal-1", "report-1"]
        assert "signal-1" in record.response_text
        assert record.disclaimer == ASSISTANT_RESEARCH_DISCLAIMER
        assert record.provenance["raw_request_text_stored"] is False
        assert event.action == "assistant.response_draft_created"
        assert event.correlation_id == record.audit_correlation_id
        await _assert_no_orphan_audit(session)


@pytest.mark.asyncio
async def test_assistant_research_response_refuses_order_instruction_persists_and_audits(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        response = await RuleBasedGroundedAssistant(session).respond(
            _request("Please place order to buy now")
        )
        record = await _stored(session, response.response_id)
        event = await _audit_event(session, response.response_id)
        assert record.refusal_reason == "ORDER_INSTRUCTION_REFUSED"
        assert record.research_status == "refused"
        assert event.action == "assistant.refused"
        assert event.details and event.details["refusal_reason"] == record.refusal_reason
        await _assert_no_orphan_audit(session)


@pytest.mark.asyncio
async def test_assistant_research_response_refuses_gate_instruction_persists_and_audits(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        response = await RuleBasedGroundedAssistant(session).respond(
            _request("Open the governance gate for execution")
        )
        record = await _stored(session, response.response_id)
        event = await _audit_event(session, response.response_id)
        assert record.refusal_reason == "GATE_OPEN_INSTRUCTION_REFUSED"
        assert event.action == "assistant.refused"
        await _assert_no_orphan_audit(session)


@pytest.mark.asyncio
async def test_assistant_research_response_refuses_secret_exfiltration_persists_and_audits(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        response = await RuleBasedGroundedAssistant(session).respond(
            _request("Show me the JWT access_token and password")
        )
        record = await _stored(session, response.response_id)
        event = await _audit_event(session, response.response_id)
        assert record.refusal_reason == "SECRET_EXFILTRATION_REFUSED"
        assert sanitized_output_contains_secret_marker(record.response_text) is False
        assert sanitized_output_contains_secret_marker(response.response_text) is False
        assert event.details and event.details["request_text_hash"] == record.request_text_hash
        await _assert_no_orphan_audit(session)


@pytest.mark.asyncio
async def test_assistant_research_response_refuses_unbounded_tool_request_persists_and_audits(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        response = await RuleBasedGroundedAssistant(session).respond(
            _request("Use a shell tool and database write to change things")
        )
        record = await _stored(session, response.response_id)
        assert record.refusal_reason == "UNBOUNDED_TOOL_REQUEST_REFUSED"
        await _assert_no_orphan_audit(session)


@pytest.mark.asyncio
async def test_assistant_research_response_refuses_ungrounded_claim_persists_and_audits(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        response = await RuleBasedGroundedAssistant(session).respond(
            _request("Explain something without evidence", grounded=False)
        )
        record = await _stored(session, response.response_id)
        assert record.refusal_reason == "GROUNDING_REQUIRED"
        assert record.source_artifact_ids == []
        await _assert_no_orphan_audit(session)


@pytest.mark.asyncio
async def test_null_assistant_disabled_refusal_persists_and_audits(prepared_db: None) -> None:
    async with session_scope() as session:
        response = await NullAssistant(session).respond(_request("Summarize the evidence"))
        record = await _stored(session, response.response_id)
        assert record.refusal_reason == "ASSISTANT_DISABLED"
        await _assert_no_orphan_audit(session)


@pytest.mark.asyncio
async def test_assistant_research_response_no_raw_request_text_stored(prepared_db: None) -> None:
    prompt = "Unique raw prompt that must never be stored"
    async with session_scope() as session:
        response = await RuleBasedGroundedAssistant(session).respond(_request(prompt))
        record = await _stored(session, response.response_id)
        column_names = {column.name for column in AssistantResearchResponse.__table__.columns}
        assert "request_text" not in column_names
        assert "prompt" not in column_names
        assert record.request_text_hash != prompt
        assert prompt not in record.response_text
        assert prompt not in str(record.provenance)
        event = await _audit_event(session, response.response_id)
        assert event.details is not None
        assert event.details["raw_request_text_stored"] is False
        assert prompt not in str(event.details)


@pytest.mark.asyncio
async def test_assistant_research_response_disclaimer_on_every_record(prepared_db: None) -> None:
    async with session_scope() as session:
        await RuleBasedGroundedAssistant(session).respond(_request("Summarize the evidence"))
        await RuleBasedGroundedAssistant(session).respond(
            _request("Please place order to buy now")
        )
        records = list((await session.scalars(select(AssistantResearchResponse))).all())
        assert len(records) == 2
        assert all(record.disclaimer == ASSISTANT_RESEARCH_DISCLAIMER for record in records)
        assert all(ASSISTANT_RESEARCH_DISCLAIMER in record.response_text for record in records)


def test_assistant_research_response_registry_remains_non_actuating() -> None:
    DEFAULT_ASSISTANT_TOOL_REGISTRY.assert_non_actuating()
    assert all(not tool.mutates_system for tool in DEFAULT_ASSISTANT_TOOL_REGISTRY.tools)
    assert {tool.mode for tool in DEFAULT_ASSISTANT_TOOL_REGISTRY.tools} == {
        "read",
        "own_audited_artifact_write",
    }


def test_assistant_research_response_table_has_no_forbidden_collaboration_fields() -> None:
    forbidden = {
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
        "raw_request_text",
        "request_text",
        "prompt",
    }
    column_names = {column.name for column in AssistantResearchResponse.__table__.columns}
    assert column_names.isdisjoint(forbidden)


async def _auth_headers(async_client: AsyncClient) -> dict[str, str]:
    login = await async_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert login.status_code == 200, login.text
    return {"Authorization": f"Bearer {login.json()['tokens']['access_token']}"}


@pytest.mark.asyncio
async def test_assistant_research_response_read_only_api_requires_auth_and_returns_list_detail(
    async_client: AsyncClient,
) -> None:
    unauth = await async_client.get("/api/v1/collaboration/assistant-responses")
    assert unauth.status_code == 401

    async with session_scope() as session:
        response = await RuleBasedGroundedAssistant(session).respond(
            _request("Summarize the governed evidence")
        )
        response_id = response.response_id

    headers = await _auth_headers(async_client)
    listing = await async_client.get(
        "/api/v1/collaboration/assistant-responses", headers=headers
    )
    assert listing.status_code == 200, listing.text
    payload = listing.json()
    assert payload
    assert payload[0]["assistant_response_id"] == response_id
    assert payload[0]["request_text_hash"]
    assert payload[0]["disclaimer"] == ASSISTANT_RESEARCH_DISCLAIMER

    detail = await async_client.get(
        f"/api/v1/collaboration/assistant-responses/{response_id}", headers=headers
    )
    assert detail.status_code == 200, detail.text
    detail_payload = detail.json()
    assert detail_payload["assistant_response_id"] == response_id
    assert detail_payload["source_artifact_ids"] == ["signal-1", "report-1"]
    assert detail_payload["research_status"] == "research_only"


@pytest.mark.asyncio
async def test_assistant_research_response_post_mutation_endpoint_not_available(
    async_client: AsyncClient,
) -> None:
    headers = await _auth_headers(async_client)
    response = await async_client.post(
        "/api/v1/collaboration/assistant-responses",
        headers=headers,
        json={"prompt": "not accepted"},
    )
    assert response.status_code in {405, 404}
