"""Human-AI collaboration contracts (W5-U01)."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal, Mapping
from uuid import uuid4

from app.core.time import utc_now

ToolMode = Literal["read", "own_audited_artifact_write"]

COLLABORATION_FORBIDDEN_FIELDS = {
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

ASSISTANT_RESEARCH_DISCLAIMER = (
    "AI-generated research assistance only. Not financial advice, not an instruction, "
    "may be wrong. Operator judgment required. AXIOM does not act."
)

SECRET_MARKERS = ("access_token", "refresh_token", "password", "jwt", "axiom_dev_password")


@dataclass(frozen=True, slots=True)
class AssistantToolDefinition:
    """Static assistant tool registry entry."""

    name: str
    mode: ToolMode
    description: str
    mutates_system: bool = False


@dataclass(frozen=True, slots=True)
class AssistantToolRegistry:
    """Allowlist containing no actuating tools by construction."""

    tools: tuple[AssistantToolDefinition, ...]

    def assert_non_actuating(self) -> None:
        for tool in self.tools:
            if tool.mode not in {"read", "own_audited_artifact_write"}:
                raise ValueError(f"ASSISTANT_TOOL_MODE_FORBIDDEN:{tool.name}")
            if tool.mutates_system:
                raise ValueError(f"ASSISTANT_TOOL_MUTATION_FORBIDDEN:{tool.name}")
            self._assert_name_safe(tool.name)

    def _assert_name_safe(self, name: str) -> None:
        lower = name.lower()
        forbidden = ("broker", "order", "gate", "execute", "retrain", "position")
        if any(item in lower for item in forbidden):
            raise ValueError(f"ASSISTANT_TOOL_NAME_FORBIDDEN:{name}")


DEFAULT_ASSISTANT_TOOL_REGISTRY = AssistantToolRegistry(
    tools=(
        AssistantToolDefinition(
            name="read_governed_artifact_summary",
            mode="read",
            description=(
                "Read persisted governed AXIOM research summaries selected by the operator."
            ),
        ),
        AssistantToolDefinition(
            name="create_audited_assistant_response_draft",
            mode="own_audited_artifact_write",
            description="Create an audited assistant research-response draft event only.",
        ),
    )
)


@dataclass(frozen=True, slots=True)
class GroundingBundle:
    """Persisted AXIOM artifact summaries available to the assistant."""

    source_artifact_ids: tuple[str, ...]
    summaries: tuple[str, ...]

    @property
    def is_empty(self) -> bool:
        return not self.source_artifact_ids or not self.summaries


@dataclass(frozen=True, slots=True)
class AssistantRequest:
    """Operator request to the non-actuating assistant."""

    prompt: str
    operator_id: str
    grounding: GroundingBundle
    request_id: str = field(default_factory=lambda: str(uuid4()))
    requested_at: datetime = field(default_factory=utc_now)

    @property
    def prompt_hash(self) -> str:
        return hashlib.sha256(self.prompt.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class AssistantResponse:
    """Assistant research response or refusal."""

    response_id: str
    request_id: str
    created_at: datetime
    response_text: str
    refused: bool
    refusal_reason: str | None
    source_artifact_ids: tuple[str, ...]
    disclaimer: str
    audit_correlation_id: str


@dataclass(frozen=True, slots=True)
class TradePlanDraft:
    """Inert operator-authored trade-plan research note draft."""

    title: str
    hypothesis: str
    market_context: str
    linked_signal_ids: tuple[str, ...] = ()
    linked_report_ids: tuple[str, ...] = ()
    scenario_notes: str | None = None
    risk_notes: str | None = None
    invalidating_conditions_text: str | None = None
    decision_status: Literal["draft", "archived", "reviewed"] = "draft"
    extra: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class TradePlanNote:
    """Validated inert trade-plan research note."""

    plan_id: str
    created_at: datetime
    title: str
    hypothesis: str
    market_context: str
    linked_signal_ids: tuple[str, ...]
    linked_report_ids: tuple[str, ...]
    scenario_notes: str | None
    risk_notes: str | None
    invalidating_conditions_text: str | None
    decision_status: str
    research_disclaimer: str
    audit_correlation_id: str


@dataclass(frozen=True, slots=True)
class ManualJournalDraft:
    """Inert manual research-journal entry draft."""

    title: str
    reflection_text: str
    linked_plan_id: str | None = None
    linked_signal_ids: tuple[str, ...] = ()
    linked_report_ids: tuple[str, ...] = ()
    emotion_tags: tuple[str, ...] = ()
    process_tags: tuple[str, ...] = ()
    lesson_notes: str | None = None
    extra: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ManualJournalEntry:
    """Validated inert manual research-journal entry."""

    journal_id: str
    created_at: datetime
    title: str
    reflection_text: str
    linked_plan_id: str | None
    linked_signal_ids: tuple[str, ...]
    linked_report_ids: tuple[str, ...]
    emotion_tags: tuple[str, ...]
    process_tags: tuple[str, ...]
    lesson_notes: str | None
    research_disclaimer: str
    audit_correlation_id: str


class CollaborationContractFactory:
    """Builds inert collaboration contracts without persistence in W5-U01."""

    def create_trade_plan(self, draft: TradePlanDraft) -> TradePlanNote:
        self._assert_inert(draft.extra, path="trade_plan.extra")
        return TradePlanNote(
            plan_id=str(uuid4()),
            created_at=utc_now(),
            title=draft.title,
            hypothesis=draft.hypothesis,
            market_context=draft.market_context,
            linked_signal_ids=tuple(draft.linked_signal_ids),
            linked_report_ids=tuple(draft.linked_report_ids),
            scenario_notes=draft.scenario_notes,
            risk_notes=draft.risk_notes,
            invalidating_conditions_text=draft.invalidating_conditions_text,
            decision_status=draft.decision_status,
            research_disclaimer=self._research_disclaimer(),
            audit_correlation_id=str(uuid4()),
        )

    def create_journal_entry(self, draft: ManualJournalDraft) -> ManualJournalEntry:
        self._assert_inert(draft.extra, path="journal.extra")
        return ManualJournalEntry(
            journal_id=str(uuid4()),
            created_at=utc_now(),
            title=draft.title,
            reflection_text=draft.reflection_text,
            linked_plan_id=draft.linked_plan_id,
            linked_signal_ids=tuple(draft.linked_signal_ids),
            linked_report_ids=tuple(draft.linked_report_ids),
            emotion_tags=tuple(draft.emotion_tags),
            process_tags=tuple(draft.process_tags),
            lesson_notes=draft.lesson_notes,
            research_disclaimer=self._research_disclaimer(),
            audit_correlation_id=str(uuid4()),
        )

    def _research_disclaimer(self) -> str:
        return "Research note only; not an instruction, not an order, and AXIOM does not act."

    def _assert_inert(self, value: Any, *, path: str) -> None:
        if isinstance(value, Mapping):
            for key, nested in value.items():
                key_text = str(key)
                if key_text in COLLABORATION_FORBIDDEN_FIELDS:
                    raise ValueError(f"COLLABORATION_FORBIDDEN_FIELD:{path}.{key_text}")
                self._assert_inert(nested, path=f"{path}.{key_text}")
        elif isinstance(value, list | tuple):
            for index, nested in enumerate(value):
                self._assert_inert(nested, path=f"{path}[{index}]")


def sanitized_output_contains_secret_marker(text: str) -> bool:
    """Return true if sampled assistant output contains common secret markers."""
    lower = text.lower()
    return any(marker in lower for marker in SECRET_MARKERS)


def redact_secret_markers(text: str) -> str:
    """Redact common secret-marker tokens before assistant text is persisted."""
    redacted = text
    for marker in SECRET_MARKERS:
        redacted = re.sub(re.escape(marker), "[redacted-secret-marker]", redacted, flags=re.I)
    return redacted


def to_jsonable(value: Any) -> str:
    return json.dumps(value, sort_keys=True, default=str)
