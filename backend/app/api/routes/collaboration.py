"""Human-AI collaboration API (Wave 5 + BO-B-06 ask path)."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import CurrentOperatorDep
from app.collaboration import (
    AssistantResearchResponseRepository,
    ChartResearchAnnotationDraft,
    ChartResearchAnnotationRepository,
    ManualJournalEntryRepository,
    RuleBasedGroundedAssistant,
    TradePlanNoteRepository,
)
from app.collaboration.contracts import AssistantRequest
from app.collaboration.grounding import assemble_grounding
from app.db.models.assistant_research_response import AssistantResearchResponse
from app.db.models.chart_research_annotation import ChartResearchAnnotation
from app.db.models.manual_trade_journal_entry import ManualTradeJournalEntryRecord
from app.db.models.trade_plan_note import TradePlanNoteRecord
from app.db.session import get_db_session
from app.models.assistant_ask import AssistantRespondRequest
from app.models.assistant_research_response import AssistantResearchResponseRead
from app.models.chart_research_annotation import (
    ChartResearchAnnotationCreate,
    ChartResearchAnnotationRead,
    ChartResearchAnnotationUpdate,
)
from app.models.manual_trade_journal_entry import (
    ManualTradeJournalEntryRead,
    ManualTradeJournalEntryWrite,
)
from app.models.trade_plan_note import TradePlanNoteRead, TradePlanNoteWrite

router = APIRouter(prefix="/collaboration", tags=["collaboration"])

SessionDep = Annotated[AsyncSession, Depends(get_db_session)]


def _assistant_response_repository(session: SessionDep) -> AssistantResearchResponseRepository:
    return AssistantResearchResponseRepository(session)


AssistantResponseRepositoryDep = Annotated[
    AssistantResearchResponseRepository, Depends(_assistant_response_repository)
]


def _chart_annotation_repository(session: SessionDep) -> ChartResearchAnnotationRepository:
    return ChartResearchAnnotationRepository(session)


ChartAnnotationRepositoryDep = Annotated[
    ChartResearchAnnotationRepository, Depends(_chart_annotation_repository)
]


def _trade_plan_repository(session: SessionDep) -> TradePlanNoteRepository:
    return TradePlanNoteRepository(session)


TradePlanRepositoryDep = Annotated[TradePlanNoteRepository, Depends(_trade_plan_repository)]


def _journal_repository(session: SessionDep) -> ManualJournalEntryRepository:
    return ManualJournalEntryRepository(session)


JournalRepositoryDep = Annotated[ManualJournalEntryRepository, Depends(_journal_repository)]


@router.get(
    "/assistant-responses",
    response_model=list[AssistantResearchResponseRead],
    summary="List read-only persisted assistant research responses",
)
async def list_assistant_responses(
    repository: AssistantResponseRepositoryDep,
    operator: CurrentOperatorDep,
    limit: int = Query(default=50, ge=1, le=200),
) -> list[AssistantResearchResponse]:
    _ = operator
    return list(await repository.list_responses(limit=limit))


@router.get(
    "/assistant-responses/{response_id}",
    response_model=AssistantResearchResponseRead,
    summary="Read one persisted assistant research response",
)
async def get_assistant_response(
    response_id: str,
    repository: AssistantResponseRepositoryDep,
    operator: CurrentOperatorDep,
) -> AssistantResearchResponse:
    _ = operator
    response = await repository.get_response(response_id)
    if response is None:
        raise HTTPException(status_code=404, detail="Assistant response not found")
    return response


@router.post(
    "/assistant-respond",
    response_model=AssistantResearchResponseRead,
    status_code=status.HTTP_201_CREATED,
    summary=(
        "BO-B-06: governed assistant ask path — deterministic, local, "
        "grounded; no external LLM, no actuation (operator-authenticated)"
    ),
)
async def assistant_respond(
    payload: AssistantRespondRequest,
    session: SessionDep,
    operator: CurrentOperatorDep,
) -> AssistantResearchResponse:
    """Resolve the operator-selected grounding ids to persisted summaries and
    delegate ENTIRELY to the existing rule-based responder. Empty grounding →
    the responder's own GROUNDING_REQUIRED refusal (no fabricated content).
    """
    grounding = await assemble_grounding(
        session, source_ids=payload.grounding_source_ids
    )
    assistant = RuleBasedGroundedAssistant(session)
    response = await assistant.respond(
        AssistantRequest(
            prompt=payload.prompt,
            operator_id=operator.username,
            grounding=grounding,
        )
    )
    record = await session.get(AssistantResearchResponse, response.response_id)
    if record is None:
        raise HTTPException(status_code=500, detail="Assistant response not persisted")
    await session.flush()
    return record


@router.get(
    "/chart-annotations",
    response_model=list[ChartResearchAnnotationRead],
    summary="List read-only chart research annotations",
)
async def list_chart_annotations(
    repository: ChartAnnotationRepositoryDep,
    operator: CurrentOperatorDep,
    symbol: str | None = Query(default=None, min_length=1, max_length=32),
    timeframe: str | None = Query(default=None, min_length=1, max_length=16),
    limit: int = Query(default=50, ge=1, le=200),
) -> list[ChartResearchAnnotation]:
    _ = operator
    return list(
        await repository.list_annotations(symbol=symbol, timeframe=timeframe, limit=limit)
    )


@router.get(
    "/chart-annotations/{annotation_id}",
    response_model=ChartResearchAnnotationRead,
    summary="Read one chart research annotation",
)
async def get_chart_annotation(
    annotation_id: str,
    repository: ChartAnnotationRepositoryDep,
    operator: CurrentOperatorDep,
) -> ChartResearchAnnotation:
    _ = operator
    annotation = await repository.get_annotation(annotation_id)
    if annotation is None:
        raise HTTPException(status_code=404, detail="Chart annotation not found")
    return annotation


@router.post(
    "/chart-annotations",
    response_model=ChartResearchAnnotationRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create an audited operator-authored chart research annotation",
)
async def create_chart_annotation(
    payload: ChartResearchAnnotationCreate,
    repository: ChartAnnotationRepositoryDep,
    operator: CurrentOperatorDep,
) -> ChartResearchAnnotation:
    draft = ChartResearchAnnotationDraft(
        artifact_type=payload.artifact_type,
        chart_context=payload.chart_context,
        content=payload.content,
        source_artifact_ids=tuple(payload.source_artifact_ids),
        provenance=payload.provenance,
        uncertainty=payload.uncertainty,
        research_status=payload.research_status,
    )
    try:
        return await repository.create_annotation(draft=draft, operator_id=operator.username)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.patch(
    "/chart-annotations/{annotation_id}",
    response_model=ChartResearchAnnotationRead,
    summary="Update an audited chart research annotation (CHART-P03 drawing reposition)",
)
async def update_chart_annotation(
    annotation_id: str,
    payload: ChartResearchAnnotationUpdate,
    repository: ChartAnnotationRepositoryDep,
    operator: CurrentOperatorDep,
) -> ChartResearchAnnotation:
    """S1: reposition a drawing by updating its geometry content. Same
    artifact, same inertness validation, same audit trail — the annotation
    contract's verb surface extended, not a parallel path."""
    updated = await repository.update_annotation_content(
        annotation_id=annotation_id,
        content=payload.content,
        operator_id=operator.username,
    )
    if updated is None:
        raise HTTPException(status_code=404, detail="Chart annotation not found")
    return updated


@router.delete(
    "/chart-annotations/{annotation_id}",
    response_model=ChartResearchAnnotationRead,
    summary="Delete an audited chart research annotation (CHART-P03 drawing removal)",
)
async def delete_chart_annotation(
    annotation_id: str,
    repository: ChartAnnotationRepositoryDep,
    operator: CurrentOperatorDep,
) -> ChartResearchAnnotation:
    deleted = await repository.delete_annotation(
        annotation_id=annotation_id,
        operator_id=operator.username,
    )
    if deleted is None:
        raise HTTPException(status_code=404, detail="Chart annotation not found")
    return deleted


@router.get(
    "/trade-plans",
    response_model=list[TradePlanNoteRead],
    summary="List inert trade plan research notes",
)
async def list_trade_plans(
    repository: TradePlanRepositoryDep,
    operator: CurrentOperatorDep,
    limit: int = Query(default=50, ge=1, le=200),
) -> list[TradePlanNoteRecord]:
    _ = operator
    return list(await repository.list_plans(limit=limit))


@router.get(
    "/trade-plans/{plan_id}",
    response_model=TradePlanNoteRead,
    summary="Read one inert trade plan research note",
)
async def get_trade_plan(
    plan_id: str,
    repository: TradePlanRepositoryDep,
    operator: CurrentOperatorDep,
) -> TradePlanNoteRecord:
    _ = operator
    plan = await repository.get_plan(plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="Trade plan note not found")
    return plan


@router.post(
    "/trade-plans",
    response_model=TradePlanNoteRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create an audited inert trade plan research note",
)
async def create_trade_plan(
    payload: TradePlanNoteWrite,
    repository: TradePlanRepositoryDep,
    operator: CurrentOperatorDep,
) -> TradePlanNoteRecord:
    try:
        return await repository.create_plan(
            payload=payload.model_dump(), operator_id=operator.username
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.put(
    "/trade-plans/{plan_id}",
    response_model=TradePlanNoteRead,
    summary="Update an audited inert trade plan research note",
)
async def update_trade_plan(
    plan_id: str,
    payload: TradePlanNoteWrite,
    repository: TradePlanRepositoryDep,
    operator: CurrentOperatorDep,
) -> TradePlanNoteRecord:
    try:
        plan = await repository.update_plan(
            plan_id=plan_id,
            payload=payload.model_dump(),
            operator_id=operator.username,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    if plan is None:
        raise HTTPException(status_code=404, detail="Trade plan note not found")
    return plan


@router.get(
    "/journal-entries",
    response_model=list[ManualTradeJournalEntryRead],
    summary="List inert manual research journal entries",
)
async def list_journal_entries(
    repository: JournalRepositoryDep,
    operator: CurrentOperatorDep,
    limit: int = Query(default=50, ge=1, le=200),
) -> list[ManualTradeJournalEntryRecord]:
    _ = operator
    return list(await repository.list_entries(limit=limit))


@router.get(
    "/journal-entries/{journal_id}",
    response_model=ManualTradeJournalEntryRead,
    summary="Read one inert manual research journal entry",
)
async def get_journal_entry(
    journal_id: str,
    repository: JournalRepositoryDep,
    operator: CurrentOperatorDep,
) -> ManualTradeJournalEntryRecord:
    _ = operator
    entry = await repository.get_entry(journal_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Manual journal entry not found")
    return entry


@router.post(
    "/journal-entries",
    response_model=ManualTradeJournalEntryRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create an audited inert manual research journal entry",
)
async def create_journal_entry(
    payload: ManualTradeJournalEntryWrite,
    repository: JournalRepositoryDep,
    operator: CurrentOperatorDep,
) -> ManualTradeJournalEntryRecord:
    try:
        return await repository.create_entry(
            payload=payload.model_dump(), operator_id=operator.username
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.put(
    "/journal-entries/{journal_id}",
    response_model=ManualTradeJournalEntryRead,
    summary="Update an audited inert manual research journal entry",
)
async def update_journal_entry(
    journal_id: str,
    payload: ManualTradeJournalEntryWrite,
    repository: JournalRepositoryDep,
    operator: CurrentOperatorDep,
) -> ManualTradeJournalEntryRecord:
    try:
        entry = await repository.update_entry(
            journal_id=journal_id,
            payload=payload.model_dump(),
            operator_id=operator.username,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    if entry is None:
        raise HTTPException(status_code=404, detail="Manual journal entry not found")
    return entry
