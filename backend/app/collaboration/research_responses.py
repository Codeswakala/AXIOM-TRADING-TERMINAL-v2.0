"""Audited assistant research-response persistence (W5-U02)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.collaboration.contracts import (
    AssistantRequest,
    AssistantResponse,
    sanitized_output_contains_secret_marker,
)
from app.db.models.assistant_research_response import AssistantResearchResponse
from app.repositories.audit_repository import AuditRepository


@dataclass(frozen=True, slots=True)
class AssistantProviderIdentity:
    """Deterministic local provider metadata for stored response records."""

    provider_name: str = "local_rule_based"
    provider_version: str = "w5-u02.persisted_response.v1"
    model_or_engine_version: str = "rule_based_grounded_assistant.v1"


class AssistantResearchResponseRepository:
    """Repository that persists assistant records and their audit event together."""

    def __init__(
        self,
        session: AsyncSession,
        *,
        provider: AssistantProviderIdentity = AssistantProviderIdentity(),
    ) -> None:
        self._session = session
        self._audit = AuditRepository(session)
        self._provider = provider

    async def create_from_response(
        self,
        *,
        request: AssistantRequest,
        response: AssistantResponse,
        policy_version: str,
        grounding_summary: str,
    ) -> AssistantResearchResponse:
        """Persist one response/refusal and append its required audit event.

        The method stores only ``request.prompt_hash``. It never persists raw
        prompt text. If audit append fails, an exception is raised so the outer
        transaction rolls back the response row rather than leaving an orphan.
        """
        if sanitized_output_contains_secret_marker(response.response_text):
            raise ValueError("ASSISTANT_RESPONSE_SECRET_MARKER_REFUSED")
        if sanitized_output_contains_secret_marker(grounding_summary):
            raise ValueError("ASSISTANT_GROUNDING_SECRET_MARKER_REFUSED")
        if not response.refused and not response.source_artifact_ids:
            raise ValueError("ASSISTANT_RESPONSE_GROUNDING_REQUIRED")
        if response.refused and not response.refusal_reason:
            raise ValueError("ASSISTANT_REFUSAL_REASON_REQUIRED")

        record = AssistantResearchResponse(
            assistant_response_id=response.response_id,
            created_at=response.created_at,
            operator_id=request.operator_id,
            request_id=request.request_id,
            request_text_hash=request.prompt_hash,
            assistant_policy_version=policy_version,
            provider_name=self._provider.provider_name,
            provider_version=self._provider.provider_version,
            model_or_engine_version=self._provider.model_or_engine_version,
            source_artifact_ids=list(response.source_artifact_ids),
            grounding_summary=grounding_summary,
            response_text=response.response_text,
            refused=response.refused,
            refusal_reason=response.refusal_reason,
            limitations=self._limitations(response),
            disclaimer=response.disclaimer,
            research_status="refused" if response.refused else "research_only",
            audit_correlation_id=response.audit_correlation_id,
            provenance={
                "request_id": request.request_id,
                "request_text_hash": request.prompt_hash,
                "source_artifact_ids": list(response.source_artifact_ids),
                "grounding_required": True,
                "raw_request_text_stored": False,
                "external_llm_used": False,
            },
        )
        self._session.add(record)
        await self._session.flush()

        event = await self._audit.append(
            category="GOVERNANCE",
            action="assistant.refused" if response.refused else "assistant.response_draft_created",
            actor=request.operator_id,
            resource_type="assistant_response",
            resource_id=record.assistant_response_id,
            message=(
                f"Assistant refusal persisted reason={response.refusal_reason}"
                if response.refused
                else "Assistant grounded research response persisted"
            ),
            details={
                "request_id": request.request_id,
                "request_text_hash": request.prompt_hash,
                "assistant_response_id": record.assistant_response_id,
                "refused": response.refused,
                "refusal_reason": response.refusal_reason,
                "source_artifact_ids": list(response.source_artifact_ids),
                "policy_version": policy_version,
                "provider_name": self._provider.provider_name,
                "disclaimer": response.disclaimer,
                "raw_request_text_stored": False,
            },
            correlation_id=record.audit_correlation_id,
        )
        if event is None:
            raise RuntimeError("ASSISTANT_RESEARCH_RESPONSE_AUDIT_FAILED")
        return record

    async def list_responses(self, *, limit: int = 50) -> Sequence[AssistantResearchResponse]:
        stmt = (
            select(AssistantResearchResponse)
            .order_by(AssistantResearchResponse.created_at.desc())
            .limit(limit)
        )
        return list((await self._session.scalars(stmt)).all())

    async def get_response(self, response_id: str) -> AssistantResearchResponse | None:
        return await self._session.get(AssistantResearchResponse, response_id)

    def _limitations(self, response: AssistantResponse) -> list[str]:
        limitations = [
            "research_assistance_only",
            "not_financial_advice",
            "not_an_instruction",
            "operator_judgment_required",
            "external_llm_not_used",
            "assistant_has_no_action_tools",
        ]
        if response.refused:
            limitations.append("refusal_recorded")
        else:
            limitations.extend(
                [
                    "grounded_in_operator_selected_artifacts",
                    "not_a_guarantee",
                ]
            )
        return limitations
