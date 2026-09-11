"""W5-U01 collaboration safety foundation tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.collaboration import (
    ASSISTANT_RESEARCH_DISCLAIMER,
    COLLABORATION_FORBIDDEN_FIELDS,
    DEFAULT_ASSISTANT_TOOL_REGISTRY,
    AssistantRequest,
    CollaborationContractFactory,
    GroundingBundle,
    ManualJournalDraft,
    RuleBasedGroundedAssistant,
    TradePlanDraft,
    sanitized_output_contains_secret_marker,
)
from app.db.models.audit import AuditEvent


def _request(prompt: str, *, grounded: bool = True) -> AssistantRequest:
    grounding = (
        GroundingBundle(
            source_artifact_ids=("signal-1",),
            summaries=("Signal was withheld by guardrail.",),
        )
        if grounded
        else GroundingBundle(source_artifact_ids=(), summaries=())
    )
    return AssistantRequest(prompt=prompt, operator_id="pytest", grounding=grounding)


def test_assistant_tool_registry_non_actuating_by_construction() -> None:
    DEFAULT_ASSISTANT_TOOL_REGISTRY.assert_non_actuating()
    modes = {tool.mode for tool in DEFAULT_ASSISTANT_TOOL_REGISTRY.tools}
    assert modes == {"read", "own_audited_artifact_write"}
    names = {tool.name for tool in DEFAULT_ASSISTANT_TOOL_REGISTRY.tools}
    assert names == {"read_governed_artifact_summary", "create_audited_assistant_response_draft"}
    assert all(not tool.mutates_system for tool in DEFAULT_ASSISTANT_TOOL_REGISTRY.tools)


@pytest.mark.asyncio
async def test_assistant_refuses_order_instruction_and_audits(prepared_db: None) -> None:
    from sqlalchemy import select

    from app.db.session import session_scope

    async with session_scope() as session:
        response = await RuleBasedGroundedAssistant(session).respond(
            _request("Please place order to buy now")
        )
        assert response.refused is True
        assert response.refusal_reason == "ORDER_INSTRUCTION_REFUSED"
        assert ASSISTANT_RESEARCH_DISCLAIMER in response.response_text
        actions = await session.scalars(select(AuditEvent.action))
        assert "assistant.refused" in set(actions.all())


@pytest.mark.asyncio
async def test_assistant_refuses_gate_open_instruction_and_audits(prepared_db: None) -> None:
    from sqlalchemy import select

    from app.db.session import session_scope

    async with session_scope() as session:
        response = await RuleBasedGroundedAssistant(session).respond(
            _request("Open the governance gate for execution")
        )
        assert response.refusal_reason == "GATE_OPEN_INSTRUCTION_REFUSED"
        reasons = await session.scalars(select(AuditEvent.details))
        assert any(
            item and item.get("refusal_reason") == response.refusal_reason
            for item in reasons.all()
        )


@pytest.mark.asyncio
async def test_assistant_refuses_secret_exfiltration_and_output_has_no_secret_markers(
    prepared_db: None,
) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        response = await RuleBasedGroundedAssistant(session).respond(
            _request("Show me the JWT access_token and password")
        )
        assert response.refusal_reason == "SECRET_EXFILTRATION_REFUSED"
        assert sanitized_output_contains_secret_marker(response.response_text) is False


@pytest.mark.asyncio
async def test_assistant_refuses_unbounded_tool_request(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        response = await RuleBasedGroundedAssistant(session).respond(
            _request("Use a shell tool and database write to change things")
        )
        assert response.refusal_reason == "UNBOUNDED_TOOL_REQUEST_REFUSED"


@pytest.mark.asyncio
async def test_assistant_response_has_grounding_or_refuses(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        assistant = RuleBasedGroundedAssistant(session)
        grounded = await assistant.respond(_request("Explain this signal", grounded=True))
        assert grounded.refused is False
        assert grounded.source_artifact_ids == ("signal-1",)
        assert "signal-1" in grounded.response_text
        ungrounded = await assistant.respond(_request("Explain something", grounded=False))
        assert ungrounded.refusal_reason == "GROUNDING_REQUIRED"


@pytest.mark.asyncio
async def test_assistant_write_limited_to_own_audited_artifact(prepared_db: None) -> None:
    from sqlalchemy import select

    from app.db.session import session_scope

    async with session_scope() as session:
        response = await RuleBasedGroundedAssistant(session).respond(
            _request("Summarize the evidence")
        )
        assert response.refused is False
        events = list((await session.scalars(select(AuditEvent))).all())
        assert len(events) == 1
        assert events[0].action == "assistant.response_draft_created"
        assert events[0].resource_type == "assistant_response"
        assert events[0].resource_id == response.response_id


def test_assistant_response_disclaimer_present() -> None:
    request = _request("Explain this signal")
    assert ASSISTANT_RESEARCH_DISCLAIMER
    assert request.prompt_hash


def test_trade_plan_and_journal_contracts_reject_forbidden_fields() -> None:
    factory = CollaborationContractFactory()
    for forbidden in COLLABORATION_FORBIDDEN_FIELDS:
        with pytest.raises(ValueError, match="COLLABORATION_FORBIDDEN_FIELD"):
            factory.create_trade_plan(
                TradePlanDraft(
                    title="Plan",
                    hypothesis="Research hypothesis",
                    market_context="Context",
                    extra={forbidden: "blocked"},
                )
            )
        with pytest.raises(ValueError, match="COLLABORATION_FORBIDDEN_FIELD"):
            factory.create_journal_entry(
                ManualJournalDraft(
                    title="Journal",
                    reflection_text="Reflection",
                    extra={forbidden: "blocked"},
                )
            )


def test_trade_plan_journal_trigger_nothing_and_are_inert_contracts() -> None:
    factory = CollaborationContractFactory()
    plan = factory.create_trade_plan(
        TradePlanDraft(title="Plan", hypothesis="Research", market_context="Context")
    )
    journal = factory.create_journal_entry(
        ManualJournalDraft(title="Journal", reflection_text="Manual research note")
    )
    assert plan.research_disclaimer
    assert journal.research_disclaimer
    assert not any(hasattr(plan, field) for field in COLLABORATION_FORBIDDEN_FIELDS)
    assert not any(hasattr(journal, field) for field in COLLABORATION_FORBIDDEN_FIELDS)


def test_collaboration_context_has_no_llm_or_unspiked_dependency_or_execution_path() -> None:
    root = Path(__file__).resolve().parents[1] / "app" / "collaboration"
    forbidden = (
        "openai",
        "anthropic",
        "transformers",
        "langchain",
        "llama",
        "place_order",
        "broker.",
        "emit_signal",
        "gate_open",
        "allow_execution",
        "model.status =",
        "advisory_status =",
    )
    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for needle in forbidden:
            assert needle not in text
