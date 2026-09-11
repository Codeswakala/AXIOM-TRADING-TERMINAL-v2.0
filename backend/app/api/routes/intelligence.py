"""Read + generate (BO-B-04) Institutional Intelligence API (Wave 4)."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import CurrentOperatorDep
from app.db.models.candle import Candle
from app.db.models.correlation_report import CorrelationReport
from app.db.models.portfolio_risk_report import PortfolioRiskReport
from app.db.models.regime_report import RegimeReport
from app.db.models.scenario_report import ScenarioReport
from app.db.models.signal_validation_report import SignalValidationReport
from app.db.session import get_db_session
from app.institutional_intelligence import (
    CorrelationReportService,
    CorrelationSeriesSpec,
    PortfolioRiskAssumptions,
    PortfolioRiskReportService,
    PortfolioRiskSeriesSpec,
    RegimeReportService,
    RegimeSeriesSpec,
    ScenarioAssumptions,
    ScenarioReportService,
    ScenarioSeriesSpec,
    SignalValidationReportService,
    SignalValidationScope,
)
from app.models.correlation_report import CorrelationReportRead
from app.models.intelligence_generation import (
    CorrelationGenerationRequest,
    PortfolioRiskGenerationRequest,
    RegimeGenerationRequest,
    ScenarioGenerationRequest,
    SignalValidationGenerationRequest,
)
from app.models.portfolio_risk_report import PortfolioRiskReportRead
from app.models.regime_report import RegimeReportRead
from app.models.scenario_report import ScenarioReportRead
from app.models.signal_validation_report import SignalValidationReportRead

router = APIRouter(prefix="/intelligence", tags=["institutional-intelligence"])

SessionDep = Annotated[AsyncSession, Depends(get_db_session)]


def _correlation_service(session: SessionDep) -> CorrelationReportService:
    return CorrelationReportService(session)


CorrelationServiceDep = Annotated[CorrelationReportService, Depends(_correlation_service)]


def _regime_service(session: SessionDep) -> RegimeReportService:
    return RegimeReportService(session)


RegimeServiceDep = Annotated[RegimeReportService, Depends(_regime_service)]


def _scenario_service(session: SessionDep) -> ScenarioReportService:
    return ScenarioReportService(session)


ScenarioServiceDep = Annotated[ScenarioReportService, Depends(_scenario_service)]


def _portfolio_risk_service(session: SessionDep) -> PortfolioRiskReportService:
    return PortfolioRiskReportService(session)


PortfolioRiskServiceDep = Annotated[
    PortfolioRiskReportService, Depends(_portfolio_risk_service)
]


def _signal_validation_service(session: SessionDep) -> SignalValidationReportService:
    return SignalValidationReportService(session)


SignalValidationServiceDep = Annotated[
    SignalValidationReportService, Depends(_signal_validation_service)
]


@router.get(
    "/correlation-reports",
    response_model=list[CorrelationReportRead],
    summary="List read-only correlation intelligence reports",
)
async def list_correlation_reports(
    service: CorrelationServiceDep,
    operator: CurrentOperatorDep,
    limit: int = Query(default=50, ge=1, le=200),
) -> list[CorrelationReport]:
    _ = operator
    return await service.list_reports(limit=limit)


@router.get(
    "/correlation-reports/{report_id}",
    response_model=CorrelationReportRead,
    summary="Read one correlation intelligence report",
)
async def get_correlation_report(
    report_id: str,
    service: CorrelationServiceDep,
    operator: CurrentOperatorDep,
) -> CorrelationReport:
    _ = operator
    report = await service.get_report(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Correlation report not found")
    return report


@router.get(
    "/regime-reports",
    response_model=list[RegimeReportRead],
    summary="List read-only regime detection reports",
)
async def list_regime_reports(
    service: RegimeServiceDep,
    operator: CurrentOperatorDep,
    limit: int = Query(default=50, ge=1, le=200),
) -> list[RegimeReport]:
    _ = operator
    return await service.list_reports(limit=limit)


@router.get(
    "/regime-reports/{report_id}",
    response_model=RegimeReportRead,
    summary="Read one regime detection report",
)
async def get_regime_report(
    report_id: str,
    service: RegimeServiceDep,
    operator: CurrentOperatorDep,
) -> RegimeReport:
    _ = operator
    report = await service.get_report(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Regime report not found")
    return report

@router.get(
    "/scenario-reports",
    response_model=list[ScenarioReportRead],
    summary="List read-only scenario simulation research reports",
)
async def list_scenario_reports(
    service: ScenarioServiceDep,
    operator: CurrentOperatorDep,
    limit: int = Query(default=50, ge=1, le=200),
) -> list[ScenarioReport]:
    _ = operator
    return await service.list_reports(limit=limit)


@router.get(
    "/scenario-reports/{report_id}",
    response_model=ScenarioReportRead,
    summary="Read one scenario simulation research report",
)
async def get_scenario_report(
    report_id: str,
    service: ScenarioServiceDep,
    operator: CurrentOperatorDep,
) -> ScenarioReport:
    _ = operator
    report = await service.get_report(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Scenario report not found")
    return report

@router.get(
    "/portfolio-risk-reports",
    response_model=list[PortfolioRiskReportRead],
    summary="List read-only portfolio/risk research reports",
)
async def list_portfolio_risk_reports(
    service: PortfolioRiskServiceDep,
    operator: CurrentOperatorDep,
    limit: int = Query(default=50, ge=1, le=200),
) -> list[PortfolioRiskReport]:
    _ = operator
    return await service.list_reports(limit=limit)


@router.get(
    "/portfolio-risk-reports/{report_id}",
    response_model=PortfolioRiskReportRead,
    summary="Read one portfolio/risk research report",
)
async def get_portfolio_risk_report(
    report_id: str,
    service: PortfolioRiskServiceDep,
    operator: CurrentOperatorDep,
) -> PortfolioRiskReport:
    _ = operator
    report = await service.get_report(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Portfolio risk report not found")
    return report

@router.get(
    "/signal-validation-reports",
    response_model=list[SignalValidationReportRead],
    summary="List read-only professional signal validation reports",
)
async def list_signal_validation_reports(
    service: SignalValidationServiceDep,
    operator: CurrentOperatorDep,
    limit: int = Query(default=50, ge=1, le=200),
) -> list[SignalValidationReport]:
    _ = operator
    return await service.list_reports(limit=limit)


@router.get(
    "/signal-validation-reports/{report_id}",
    response_model=SignalValidationReportRead,
    summary="Read one professional signal validation report",
)
async def get_signal_validation_report(
    report_id: str,
    service: SignalValidationServiceDep,
    operator: CurrentOperatorDep,
) -> SignalValidationReport:
    _ = operator
    report = await service.get_report(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Signal validation report not found")
    return report


# ---------------------------------------------------------------------------
# BO-B-04 — governed generation endpoints.
#
# The five computation services existed since W4 but were never invoked (the
# FIND-2 gap). These POSTs wire generation: operator-authenticated,
# as-of-bounded, research-artifact-only. The services persist their own
# reports with uncertainty, sample counts, lineage, and audit rows; the
# endpoints add the honest data-class label (distinct candle source values
# in the requested window) to the persisted `notes` column.
# ---------------------------------------------------------------------------

INSUFFICIENT_DATA_CODES = {
    "CORRELATION_REQUIRES_THREE_ALIGNED_POINTS",
    "REGIME_REQUIRES_FOUR_OR_MORE_POINTS",
    "SCENARIO_REQUIRES_THREE_OR_MORE_POINTS",
    "PORTFOLIO_RISK_REQUIRES_FOUR_OR_MORE_POINTS",
    "SIGNAL_VALIDATION_EMPTY_SCOPE",
}


def _generation_failure(exc: ValueError) -> HTTPException:
    """Structured honest failure — no fabricated report, ever."""
    code = str(exc)
    return HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        detail={
            "error_code": code,
            "detail": code,
            "insufficient_data": code in INSUFFICIENT_DATA_CODES,
        },
    )


async def _data_class_label(
    session: AsyncSession,
    *,
    market_class: str,
    symbol: str,
    timeframe: str,
    as_of_start: datetime,
    as_of_end: datetime,
) -> str:
    """Distinct candle source labels present in the requested window — the
    honest data-class declaration persisted on every generated report."""
    result = await session.execute(
        select(Candle.source)
        .where(
            Candle.market_class == market_class,
            Candle.symbol == symbol,
            Candle.timeframe == timeframe,
            Candle.open_time >= as_of_start,
            Candle.open_time <= as_of_end,
        )
        .distinct()
    )
    sources = sorted({row[0] for row in result.all() if row[0]})
    return f"data-class: {', '.join(sources)}" if sources else "data-class: none"


@router.post(
    "/correlation-reports",
    response_model=CorrelationReportRead,
    status_code=status.HTTP_201_CREATED,
    summary="Generate a governed correlation intelligence report (research artifact)",
)
async def generate_correlation_report(
    payload: CorrelationGenerationRequest,
    service: CorrelationServiceDep,
    session: SessionDep,
    operator: CurrentOperatorDep,
) -> CorrelationReport:
    try:
        result = await service.create_report(
            left=CorrelationSeriesSpec(
                payload.left.market_class, payload.left.symbol, payload.left.timeframe
            ),
            right=CorrelationSeriesSpec(
                payload.right.market_class, payload.right.symbol, payload.right.timeframe
            ),
            as_of_start=payload.as_of_start,
            as_of_end=payload.as_of_end,
            actor=operator.username,
        )
    except ValueError as exc:
        raise _generation_failure(exc) from exc
    label = await _data_class_label(
        session,
        market_class=payload.left.market_class,
        symbol=payload.left.symbol,
        timeframe=payload.left.timeframe,
        as_of_start=payload.as_of_start,
        as_of_end=payload.as_of_end,
    )
    result.report.notes = f"{result.report.notes or 'BO-B-04 generation'}; {label}"
    await session.flush()
    return result.report


@router.post(
    "/regime-reports",
    response_model=RegimeReportRead,
    status_code=status.HTTP_201_CREATED,
    summary="Generate a governed regime detection report (research artifact)",
)
async def generate_regime_report(
    payload: RegimeGenerationRequest,
    service: RegimeServiceDep,
    session: SessionDep,
    operator: CurrentOperatorDep,
) -> RegimeReport:
    try:
        result = await service.create_report(
            series=RegimeSeriesSpec(
                payload.series.market_class, payload.series.symbol, payload.series.timeframe
            ),
            as_of_start=payload.as_of_start,
            as_of_end=payload.as_of_end,
            actor=operator.username,
        )
    except ValueError as exc:
        raise _generation_failure(exc) from exc
    label = await _data_class_label(
        session,
        market_class=payload.series.market_class,
        symbol=payload.series.symbol,
        timeframe=payload.series.timeframe,
        as_of_start=payload.as_of_start,
        as_of_end=payload.as_of_end,
    )
    result.report.notes = f"{result.report.notes or 'BO-B-04 generation'}; {label}"
    await session.flush()
    return result.report


@router.post(
    "/scenario-reports",
    response_model=ScenarioReportRead,
    status_code=status.HTTP_201_CREATED,
    summary="Generate a governed hypothetical scenario report (research artifact)",
)
async def generate_scenario_report(
    payload: ScenarioGenerationRequest,
    service: ScenarioServiceDep,
    session: SessionDep,
    operator: CurrentOperatorDep,
) -> ScenarioReport:
    try:
        result = await service.create_report(
            series=ScenarioSeriesSpec(
                payload.series.market_class, payload.series.symbol, payload.series.timeframe
            ),
            assumptions=ScenarioAssumptions(
                scenario_name=payload.assumptions.scenario_name,
                shock_return=payload.assumptions.shock_return,
                horizon_bars=payload.assumptions.horizon_bars,
                volatility_multiplier=payload.assumptions.volatility_multiplier,
            ),
            as_of_start=payload.as_of_start,
            as_of_end=payload.as_of_end,
            actor=operator.username,
        )
    except ValueError as exc:
        raise _generation_failure(exc) from exc
    label = await _data_class_label(
        session,
        market_class=payload.series.market_class,
        symbol=payload.series.symbol,
        timeframe=payload.series.timeframe,
        as_of_start=payload.as_of_start,
        as_of_end=payload.as_of_end,
    )
    result.report.notes = f"{result.report.notes or 'BO-B-04 generation'}; {label}"
    await session.flush()
    return result.report


@router.post(
    "/portfolio-risk-reports",
    response_model=PortfolioRiskReportRead,
    status_code=status.HTTP_201_CREATED,
    summary="Generate a governed hypothetical portfolio-risk report (research artifact)",
)
async def generate_portfolio_risk_report(
    payload: PortfolioRiskGenerationRequest,
    service: PortfolioRiskServiceDep,
    session: SessionDep,
    operator: CurrentOperatorDep,
) -> PortfolioRiskReport:
    try:
        result = await service.create_report(
            series=PortfolioRiskSeriesSpec(
                payload.series.market_class, payload.series.symbol, payload.series.timeframe
            ),
            assumptions=PortfolioRiskAssumptions(
                report_name=payload.assumptions.report_name,
                stress_multiplier=payload.assumptions.stress_multiplier,
                tail_quantile=payload.assumptions.tail_quantile,
            ),
            as_of_start=payload.as_of_start,
            as_of_end=payload.as_of_end,
            actor=operator.username,
        )
    except ValueError as exc:
        raise _generation_failure(exc) from exc
    label = await _data_class_label(
        session,
        market_class=payload.series.market_class,
        symbol=payload.series.symbol,
        timeframe=payload.series.timeframe,
        as_of_start=payload.as_of_start,
        as_of_end=payload.as_of_end,
    )
    result.report.notes = f"{result.report.notes or 'BO-B-04 generation'}; {label}"
    await session.flush()
    return result.report


@router.post(
    "/signal-validation-reports",
    response_model=SignalValidationReportRead,
    status_code=status.HTTP_201_CREATED,
    summary="Generate a governed professional signal validation report (research artifact)",
)
async def generate_signal_validation_report(
    payload: SignalValidationGenerationRequest,
    service: SignalValidationServiceDep,
    operator: CurrentOperatorDep,
) -> SignalValidationReport:
    try:
        result = await service.create_report(
            scope=SignalValidationScope(
                scope_start=payload.scope_start,
                scope_end=payload.scope_end,
                market_class=payload.market_class,
                symbol=payload.symbol,
                timeframe=payload.timeframe,
                include_states=tuple(payload.include_states),
            ),
            actor=operator.username,
        )
    except ValueError as exc:
        raise _generation_failure(exc) from exc
    result.report.notes = (
        f"{result.report.notes or 'BO-B-04 generation'}; "
        "data-class: declared advisory-signal scope (see validation_scope)"
    )
    return result.report
