"""Inert chart research annotation contracts and persistence (W5-U03)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.collaboration.contracts import COLLABORATION_FORBIDDEN_FIELDS
from app.core.time import utc_now
from app.db.models.chart_research_annotation import ChartResearchAnnotation
from app.repositories.audit_repository import AuditRepository

CHART_RESEARCH_ANNOTATION_DISCLAIMER = (
    "Chart research annotation only. Not financial advice, not an instruction, "
    "not a signal, not an order. Operator judgment required. AXIOM does not act."
)

CHART_ANNOTATION_FORBIDDEN_FIELDS = COLLABORATION_FORBIDDEN_FIELDS | {
    "signal_payload",
    "signal_instruction",
    "signal_emit_payload",
    "emit_" + "signal",
    "raw_score",
    "raw_model_score",
    "predicted_outcome",
    "guaranteed_outcome",
    "guaranteed_profit",
    "price_target_for_execution",
}

_CHART_ANNOTATION_FORBIDDEN_TEXT = (
    "raw_score",
    "raw model score",
    "guaranteed profit",
    "guaranteed outcome",
    "will definitely",
)


@dataclass(frozen=True, slots=True)
class ChartResearchAnnotationDraft:
    """Operator-authored inert chart markup draft."""

    chart_context: Mapping[str, Any]
    content: Mapping[str, Any]
    source_artifact_ids: tuple[str, ...]
    artifact_type: str = "chart_research_annotation"
    provenance: Mapping[str, Any] = field(default_factory=dict)
    uncertainty: Mapping[str, Any] = field(default_factory=dict)
    research_status: str = "research_only"


class ChartResearchAnnotationFactory:
    """Validates inert chart annotation drafts before persistence."""

    def validate(self, draft: ChartResearchAnnotationDraft) -> None:
        if draft.artifact_type not in {"chart_research_annotation", "chart_research_drawing"}:
            raise ValueError("CHART_ANNOTATION_ARTIFACT_TYPE_INVALID")
        if draft.research_status != "research_only":
            raise ValueError("CHART_ANNOTATION_RESEARCH_STATUS_INVALID")
        if not draft.source_artifact_ids:
            raise ValueError("CHART_ANNOTATION_SOURCE_ARTIFACT_REQUIRED")
        for value, path in (
            (draft.chart_context, "chart_context"),
            (draft.content, "content"),
            (draft.provenance, "provenance"),
            (draft.uncertainty, "uncertainty"),
        ):
            self._assert_inert(value, path=path)
            self._assert_no_guarantee_text(value, path=path)

    def _assert_inert(self, value: Any, *, path: str) -> None:
        if isinstance(value, Mapping):
            for key, nested in value.items():
                key_text = str(key)
                if key_text in CHART_ANNOTATION_FORBIDDEN_FIELDS:
                    raise ValueError(f"CHART_ANNOTATION_FORBIDDEN_FIELD:{path}.{key_text}")
                self._assert_inert(nested, path=f"{path}.{key_text}")
        elif isinstance(value, list | tuple):
            for index, nested in enumerate(value):
                self._assert_inert(nested, path=f"{path}[{index}]")

    def _assert_no_guarantee_text(self, value: Any, *, path: str) -> None:
        if isinstance(value, str):
            lower = value.lower()
            for marker in _CHART_ANNOTATION_FORBIDDEN_TEXT:
                if marker in lower:
                    raise ValueError(f"CHART_ANNOTATION_FORBIDDEN_TEXT:{path}")
        elif isinstance(value, Mapping):
            for key, nested in value.items():
                self._assert_no_guarantee_text(nested, path=f"{path}.{key}")
        elif isinstance(value, list | tuple):
            for index, nested in enumerate(value):
                self._assert_no_guarantee_text(nested, path=f"{path}[{index}]")


class ChartResearchAnnotationRepository:
    """Repository for audited, inert chart annotation artifacts."""

    method_version = "w5-u03.chart_annotation.v1"

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._audit = AuditRepository(session)
        self._factory = ChartResearchAnnotationFactory()

    async def create_annotation(
        self,
        *,
        draft: ChartResearchAnnotationDraft,
        operator_id: str,
    ) -> ChartResearchAnnotation:
        self._factory.validate(draft)
        correlation_id = str(uuid4())
        annotation = ChartResearchAnnotation(
            id=str(uuid4()),
            created_at=utc_now(),
            operator_id=operator_id,
            artifact_type=draft.artifact_type,
            chart_context=dict(draft.chart_context),
            content=dict(draft.content),
            source_artifact_ids=list(draft.source_artifact_ids),
            provenance={
                "method_version": self.method_version,
                "operator_authored": True,
                "ai_assisted": False,
                "presentation_only": True,
                "source_artifact_ids": list(draft.source_artifact_ids),
                **dict(draft.provenance),
            },
            uncertainty=dict(draft.uncertainty),
            disclaimer=CHART_RESEARCH_ANNOTATION_DISCLAIMER,
            research_status=draft.research_status,
            audit_correlation_id=correlation_id,
        )
        self._session.add(annotation)
        await self._session.flush()
        event = await self._audit.append(
            category="GOVERNANCE",
            action="chart_research_annotation.created",
            actor=operator_id,
            resource_type="chart_research_annotation",
            resource_id=annotation.id,
            message="Chart research annotation created as inert presentation-only markup",
            details={
                "annotation_id": annotation.id,
                "artifact_type": annotation.artifact_type,
                "research_status": annotation.research_status,
                "source_artifact_ids": annotation.source_artifact_ids,
                "method_version": self.method_version,
                "operator_authored": True,
                "ai_assisted": False,
                "presentation_only": True,
                "disclaimer": annotation.disclaimer,
            },
            correlation_id=annotation.audit_correlation_id,
        )
        if event is None:
            raise RuntimeError("CHART_ANNOTATION_AUDIT_FAILED")
        return annotation

    async def update_annotation_content(
        self,
        *,
        annotation_id: str,
        content: dict,
        operator_id: str,
    ) -> ChartResearchAnnotation | None:
        """CHART-P03 (S1): reposition a drawing by updating its geometry
        content — same artifact, same inertness validation, same audit
        trail. Never a parallel persistence path."""
        annotation = await self._session.get(ChartResearchAnnotation, annotation_id)
        if annotation is None:
            return None
        draft = ChartResearchAnnotationDraft(
            artifact_type=annotation.artifact_type,
            chart_context=dict(annotation.chart_context),
            content=dict(content),
            source_artifact_ids=tuple(annotation.source_artifact_ids),
            provenance=dict(annotation.provenance),
            uncertainty=dict(annotation.uncertainty),
            research_status=annotation.research_status,
        )
        self._factory.validate(draft)
        annotation.content = dict(draft.content)
        await self._session.flush()
        event = await self._audit.append(
            category="GOVERNANCE",
            action="chart_research_annotation.updated",
            actor=operator_id,
            resource_type="chart_research_annotation",
            resource_id=annotation.id,
            message="Chart research annotation content updated (inert presentation-only markup)",
            details={"annotation_id": annotation.id, "artifact_type": annotation.artifact_type},
            correlation_id=annotation.audit_correlation_id,
        )
        if event is None:
            raise RuntimeError("CHART_ANNOTATION_AUDIT_FAILED")
        return annotation

    async def delete_annotation(
        self,
        *,
        annotation_id: str,
        operator_id: str,
    ) -> ChartResearchAnnotation | None:
        """CHART-P03 (S1): delete a drawing — audited removal of the same
        artifact."""
        annotation = await self._session.get(ChartResearchAnnotation, annotation_id)
        if annotation is None:
            return None
        await self._audit.append(
            category="GOVERNANCE",
            action="chart_research_annotation.deleted",
            actor=operator_id,
            resource_type="chart_research_annotation",
            resource_id=annotation.id,
            message="Chart research annotation deleted",
            details={"annotation_id": annotation.id, "artifact_type": annotation.artifact_type},
            correlation_id=annotation.audit_correlation_id,
        )
        await self._session.delete(annotation)
        await self._session.flush()
        return annotation

    async def list_annotations(
        self,
        *,
        symbol: str | None = None,
        timeframe: str | None = None,
        limit: int = 50,
    ) -> Sequence[ChartResearchAnnotation]:
        stmt = select(ChartResearchAnnotation)
        if symbol:
            stmt = stmt.where(ChartResearchAnnotation.chart_context["symbol"].as_string() == symbol)
        if timeframe:
            stmt = stmt.where(
                ChartResearchAnnotation.chart_context["timeframe"].as_string() == timeframe
            )
        stmt = stmt.order_by(ChartResearchAnnotation.created_at.desc()).limit(limit)
        return list((await self._session.scalars(stmt)).all())

    async def get_annotation(self, annotation_id: str) -> ChartResearchAnnotation | None:
        return await self._session.get(ChartResearchAnnotation, annotation_id)
