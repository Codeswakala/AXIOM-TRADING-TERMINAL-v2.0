"""Execution Research API — simulated artifacts only (Wave 6)."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import CurrentOperatorDep
from app.db.models.execution_experiment import ExecutionResearchExperiment
from app.db.models.execution_risk_report import ExecutionRiskResearchReport
from app.db.models.simulated_execution import SimulatedExecutionRun, SimulatedFillEvent
from app.db.models.simulated_execution_analytics_report import SimulatedExecutionAnalyticsReport
from app.db.models.simulated_paper_ledger import SimulatedPaperLedgerEntry
from app.db.session import get_db_session
from app.execution_research import (
    ExecutionResearchExperimentDraft,
    ExecutionResearchExperimentService,
    ExecutionRiskResearchReportDraft,
    ExecutionRiskResearchReportService,
    SimulatedExecutionAnalyticsReportDraft,
    SimulatedExecutionAnalyticsReportService,
    SimulatedExecutionRunSpec,
    SimulatedExecutionService,
    SimulatedPaperLedgerEntryDraft,
    SimulatedPaperLedgerService,
)
from app.models.execution_experiment import (
    ExecutionResearchExperimentCreate,
    ExecutionResearchExperimentRead,
)
from app.models.execution_risk_report import (
    ExecutionRiskResearchReportCreate,
    ExecutionRiskResearchReportRead,
)
from app.models.simulated_execution import (
    SimulatedExecutionRunCreate,
    SimulatedExecutionRunRead,
    SimulatedExecutionRunWithFillsRead,
    SimulatedFillEventRead,
)
from app.models.simulated_execution_analytics import (
    SimulatedExecutionAnalyticsReportCreate,
    SimulatedExecutionAnalyticsReportRead,
)
from app.models.simulated_paper_ledger import (
    SimulatedPaperLedgerEntryCreate,
    SimulatedPaperLedgerEntryRead,
)

router = APIRouter(prefix="/execution-research", tags=["execution-research"])

SessionDep = Annotated[AsyncSession, Depends(get_db_session)]


def _simulation_service(session: SessionDep) -> SimulatedExecutionService:
    return SimulatedExecutionService(session)


SimulationServiceDep = Annotated[SimulatedExecutionService, Depends(_simulation_service)]


def _ledger_service(session: SessionDep) -> SimulatedPaperLedgerService:
    return SimulatedPaperLedgerService(session)


LedgerServiceDep = Annotated[SimulatedPaperLedgerService, Depends(_ledger_service)]


def _risk_report_service(session: SessionDep) -> ExecutionRiskResearchReportService:
    return ExecutionRiskResearchReportService(session)


RiskReportServiceDep = Annotated[
    ExecutionRiskResearchReportService, Depends(_risk_report_service)
]


def _experiment_service(session: SessionDep) -> ExecutionResearchExperimentService:
    return ExecutionResearchExperimentService(session)


ExperimentServiceDep = Annotated[ExecutionResearchExperimentService, Depends(_experiment_service)]


def _analytics_service(session: SessionDep) -> SimulatedExecutionAnalyticsReportService:
    return SimulatedExecutionAnalyticsReportService(session)


AnalyticsServiceDep = Annotated[
    SimulatedExecutionAnalyticsReportService, Depends(_analytics_service)
]


@router.post(
    "/simulated-runs",
    response_model=SimulatedExecutionRunWithFillsRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create simulated execution research run and deterministic fill events",
)
async def create_simulated_run(
    payload: SimulatedExecutionRunCreate,
    service: SimulationServiceDep,
    operator: CurrentOperatorDep,
) -> dict[str, object]:
    spec = SimulatedExecutionRunSpec(
        market_class=payload.market_class,
        symbol=payload.symbol,
        timeframe=payload.timeframe,
        as_of_start=payload.as_of_start,
        as_of_end=payload.as_of_end,
        simulated_research_direction=payload.simulated_research_direction,
        simulated_units=payload.simulated_units,
        simulated_slippage_bps=payload.simulated_slippage_bps,
        max_fill_events=payload.max_fill_events,
        input_artifact_ids=tuple(payload.input_artifact_ids),
    )
    try:
        result = await service.create_run(spec=spec, operator_id=operator.id)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {"run": result.run, "fills": list(result.fills)}


@router.get(
    "/simulated-runs",
    response_model=list[SimulatedExecutionRunRead],
    summary="List simulated execution research runs",
)
async def list_simulated_runs(
    service: SimulationServiceDep,
    operator: CurrentOperatorDep,
    limit: int = Query(default=50, ge=1, le=200),
) -> list[SimulatedExecutionRun]:
    _ = operator
    return await service.list_runs(limit=limit)


@router.get(
    "/simulated-runs/{run_id}",
    response_model=SimulatedExecutionRunWithFillsRead,
    summary="Read one simulated execution run with fill events",
)
async def get_simulated_run(
    run_id: str,
    service: SimulationServiceDep,
    operator: CurrentOperatorDep,
) -> dict[str, object]:
    _ = operator
    run = await service.get_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Simulated execution run not found")
    fills = await service.list_fills(run_id=run_id, limit=200)
    return {"run": run, "fills": fills}


@router.get(
    "/simulated-runs/{run_id}/fills",
    response_model=list[SimulatedFillEventRead],
    summary="List simulated fill events for one run",
)
async def list_simulated_fills_for_run(
    run_id: str,
    service: SimulationServiceDep,
    operator: CurrentOperatorDep,
    limit: int = Query(default=100, ge=1, le=500),
) -> list[SimulatedFillEvent]:
    _ = operator
    run = await service.get_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Simulated execution run not found")
    return await service.list_fills(run_id=run_id, limit=limit)


@router.get(
    "/simulated-fills/{fill_id}",
    response_model=SimulatedFillEventRead,
    summary="Read one simulated fill event",
)
async def get_simulated_fill(
    fill_id: str,
    service: SimulationServiceDep,
    operator: CurrentOperatorDep,
) -> SimulatedFillEvent:
    _ = operator
    fill = await service.get_fill(fill_id)
    if fill is None:
        raise HTTPException(status_code=404, detail="Simulated fill event not found")
    return fill


@router.post(
    "/simulated-ledger-entries",
    response_model=SimulatedPaperLedgerEntryRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create simulated paper research ledger entry",
)
async def create_simulated_ledger_entry(
    payload: SimulatedPaperLedgerEntryCreate,
    service: LedgerServiceDep,
    operator: CurrentOperatorDep,
) -> SimulatedPaperLedgerEntry:
    draft = SimulatedPaperLedgerEntryDraft(
        run_id=payload.run_id,
        simulated_fill_id=payload.simulated_fill_id,
        simulated_exit_value=payload.simulated_exit_value,
        ledger_event_type=payload.ledger_event_type,
        uncertainty_width=payload.uncertainty_width,
    )
    try:
        return await service.create_entry(draft=draft, operator_id=operator.id)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get(
    "/simulated-ledger-entries",
    response_model=list[SimulatedPaperLedgerEntryRead],
    summary="List simulated paper research ledger entries",
)
async def list_simulated_ledger_entries(
    service: LedgerServiceDep,
    operator: CurrentOperatorDep,
    limit: int = Query(default=50, ge=1, le=200),
) -> list[SimulatedPaperLedgerEntry]:
    _ = operator
    return list(await service.list_entries(limit=limit))


@router.get(
    "/simulated-ledger-entries/{ledger_entry_id}",
    response_model=SimulatedPaperLedgerEntryRead,
    summary="Read one simulated paper research ledger entry",
)
async def get_simulated_ledger_entry(
    ledger_entry_id: str,
    service: LedgerServiceDep,
    operator: CurrentOperatorDep,
) -> SimulatedPaperLedgerEntry:
    _ = operator
    entry = await service.get_entry(ledger_entry_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Simulated ledger entry not found")
    return entry


@router.post(
    "/execution-risk-reports",
    response_model=ExecutionRiskResearchReportRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create simulated execution-risk research report",
)
async def create_execution_risk_report(
    payload: ExecutionRiskResearchReportCreate,
    service: RiskReportServiceDep,
    operator: CurrentOperatorDep,
) -> ExecutionRiskResearchReport:
    _ = operator
    draft = ExecutionRiskResearchReportDraft(input_artifact_ids=tuple(payload.input_artifact_ids))
    try:
        return await service.create_report(draft=draft, actor="operator")
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get(
    "/execution-risk-reports",
    response_model=list[ExecutionRiskResearchReportRead],
    summary="List simulated execution-risk research reports",
)
async def list_execution_risk_reports(
    service: RiskReportServiceDep,
    operator: CurrentOperatorDep,
    limit: int = Query(default=50, ge=1, le=200),
) -> list[ExecutionRiskResearchReport]:
    _ = operator
    return list(await service.list_reports(limit=limit))


@router.get(
    "/execution-risk-reports/{report_id}",
    response_model=ExecutionRiskResearchReportRead,
    summary="Read one simulated execution-risk research report",
)
async def get_execution_risk_report(
    report_id: str,
    service: RiskReportServiceDep,
    operator: CurrentOperatorDep,
) -> ExecutionRiskResearchReport:
    _ = operator
    report = await service.get_report(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Execution risk report not found")
    return report


@router.post(
    "/execution-experiments",
    response_model=ExecutionResearchExperimentRead,
    status_code=status.HTTP_201_CREATED,
    summary="Register and replay simulated execution research experiment",
)
async def create_execution_experiment(
    payload: ExecutionResearchExperimentCreate,
    service: ExperimentServiceDep,
    operator: CurrentOperatorDep,
) -> ExecutionResearchExperiment:
    draft = ExecutionResearchExperimentDraft(
        experiment_title=payload.experiment_title,
        hypothesis=payload.hypothesis,
        market_class=payload.market_class,
        symbol=payload.symbol,
        timeframe=payload.timeframe,
        as_of_start=payload.as_of_start,
        as_of_time=payload.as_of_time,
        input_artifact_ids=tuple(payload.input_artifact_ids),
        max_candles=payload.max_candles,
    )
    try:
        return await service.register_and_replay(draft=draft, operator_id=operator.id)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get(
    "/execution-experiments",
    response_model=list[ExecutionResearchExperimentRead],
    summary="List simulated execution research experiments",
)
async def list_execution_experiments(
    service: ExperimentServiceDep,
    operator: CurrentOperatorDep,
    limit: int = Query(default=50, ge=1, le=200),
) -> list[ExecutionResearchExperiment]:
    _ = operator
    return list(await service.list_experiments(limit=limit))


@router.get(
    "/execution-experiments/{experiment_id}",
    response_model=ExecutionResearchExperimentRead,
    summary="Read one simulated execution research experiment",
)
async def get_execution_experiment(
    experiment_id: str,
    service: ExperimentServiceDep,
    operator: CurrentOperatorDep,
) -> ExecutionResearchExperiment:
    _ = operator
    experiment = await service.get_experiment(experiment_id)
    if experiment is None:
        raise HTTPException(status_code=404, detail="Execution experiment not found")
    return experiment


@router.post(
    "/simulated-analytics-reports",
    response_model=SimulatedExecutionAnalyticsReportRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create simulated execution analytics report",
)
async def create_simulated_analytics_report(
    payload: SimulatedExecutionAnalyticsReportCreate,
    service: AnalyticsServiceDep,
    operator: CurrentOperatorDep,
) -> SimulatedExecutionAnalyticsReport:
    _ = operator
    draft = SimulatedExecutionAnalyticsReportDraft(
        source_artifact_ids=tuple(payload.source_artifact_ids),
        analytics_type=payload.analytics_type,
    )
    try:
        return await service.create_report(draft=draft, actor="operator")
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get(
    "/simulated-analytics-reports",
    response_model=list[SimulatedExecutionAnalyticsReportRead],
    summary="List simulated execution analytics reports",
)
async def list_simulated_analytics_reports(
    service: AnalyticsServiceDep,
    operator: CurrentOperatorDep,
    limit: int = Query(default=50, ge=1, le=200),
) -> list[SimulatedExecutionAnalyticsReport]:
    _ = operator
    return list(await service.list_reports(limit=limit))


@router.get(
    "/simulated-analytics-reports/{report_id}",
    response_model=SimulatedExecutionAnalyticsReportRead,
    summary="Read one simulated execution analytics report",
)
async def get_simulated_analytics_report(
    report_id: str,
    service: AnalyticsServiceDep,
    operator: CurrentOperatorDep,
) -> SimulatedExecutionAnalyticsReport:
    _ = operator
    report = await service.get_report(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Simulated analytics report not found")
    return report
