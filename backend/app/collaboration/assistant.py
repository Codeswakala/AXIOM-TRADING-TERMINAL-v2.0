"""Non-actuating grounded assistant boundary (W5-U01)."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.collaboration.contracts import (
    ASSISTANT_RESEARCH_DISCLAIMER,
    DEFAULT_ASSISTANT_TOOL_REGISTRY,
    AssistantRequest,
    AssistantResponse,
    AssistantToolRegistry,
    redact_secret_markers,
)
from app.collaboration.research_responses import AssistantResearchResponseRepository
from app.core.time import utc_now


@dataclass(frozen=True, slots=True)
class AssistantSafetyPolicy:
    """Assistant safety policy that user text cannot override."""

    policy_version: str = "w5-u01.non_actuating.v1"

    def refusal_reason(self, prompt: str) -> str | None:
        lower = prompt.lower()
        if any(term in lower for term in ("place order", "submit order", "buy ", "sell ")):
            return "ORDER_INSTRUCTION_REFUSED"
        if "open the gate" in lower or "governance gate" in lower:
            return "GATE_OPEN_INSTRUCTION_REFUSED"
        if any(term in lower for term in ("secret", "token", "password", "jwt")):
            return "SECRET_EXFILTRATION_REFUSED"
        if any(term in lower for term in ("tool", "shell", "database write", "http request")):
            return "UNBOUNDED_TOOL_REQUEST_REFUSED"
        return None


class AssistantPort:
    """Provider-neutral assistant boundary."""

    async def respond(
        self, request: AssistantRequest
    ) -> AssistantResponse:  # pragma: no cover - port
        raise NotImplementedError


class RuleBasedGroundedAssistant(AssistantPort):
    """Deterministic local assistant with no external LLM and no action tools."""

    def __init__(
        self,
        session: AsyncSession,
        *,
        registry: AssistantToolRegistry = DEFAULT_ASSISTANT_TOOL_REGISTRY,
        policy: AssistantSafetyPolicy = AssistantSafetyPolicy(),
    ) -> None:
        self._responses = AssistantResearchResponseRepository(session)
        self.registry = registry
        self.policy = policy
        self.registry.assert_non_actuating()

    async def respond(self, request: AssistantRequest) -> AssistantResponse:
        refusal = self.policy.refusal_reason(request.prompt)
        if refusal is not None:
            return await self._refuse(request, refusal)
        if request.grounding.is_empty:
            return await self._refuse(request, "GROUNDING_REQUIRED")
        return await self._answer(request)

    async def _answer(self, request: AssistantRequest) -> AssistantResponse:
        correlation_id = str(uuid4())
        summary = redact_secret_markers(" ".join(request.grounding.summaries))
        response = AssistantResponse(
            response_id=str(uuid4()),
            request_id=request.request_id,
            created_at=utc_now(),
            response_text=(
                "Grounded research summary: "
                f"{summary} Sources: {', '.join(request.grounding.source_artifact_ids)}. "
                f"{ASSISTANT_RESEARCH_DISCLAIMER}"
            ),
            refused=False,
            refusal_reason=None,
            source_artifact_ids=tuple(request.grounding.source_artifact_ids),
            disclaimer=ASSISTANT_RESEARCH_DISCLAIMER,
            audit_correlation_id=correlation_id,
        )
        await self._responses.create_from_response(
            request=request,
            response=response,
            policy_version=self.policy.policy_version,
            grounding_summary=summary,
        )
        return response

    async def _refuse(self, request: AssistantRequest, reason: str) -> AssistantResponse:
        correlation_id = str(uuid4())
        summary = redact_secret_markers(" ".join(request.grounding.summaries))
        response = AssistantResponse(
            response_id=str(uuid4()),
            request_id=request.request_id,
            created_at=utc_now(),
            response_text=f"Refused: {reason}. {ASSISTANT_RESEARCH_DISCLAIMER}",
            refused=True,
            refusal_reason=reason,
            source_artifact_ids=tuple(request.grounding.source_artifact_ids),
            disclaimer=ASSISTANT_RESEARCH_DISCLAIMER,
            audit_correlation_id=correlation_id,
        )
        await self._responses.create_from_response(
            request=request,
            response=response,
            policy_version=self.policy.policy_version,
            grounding_summary=summary,
        )
        return response


class NullAssistant(AssistantPort):
    """Disabled assistant implementation that refuses safely."""

    def __init__(self, session: AsyncSession) -> None:
        self._assistant = RuleBasedGroundedAssistant(session)

    async def respond(self, request: AssistantRequest) -> AssistantResponse:
        return await self._assistant._refuse(request, "ASSISTANT_DISABLED")
