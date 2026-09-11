"""BO-B-06.2 — real grounding-bundle resolution.

Resolves operator-selected artifact ids into a `GroundingBundle` built from
the artifacts' PERSISTED summaries/notes — never free-form generation, never
a fabricated summary. Families (deterministic resolution order):

  1. correlation reports      (B-04)  4. portfolio-risk reports (B-04)
  2. regime reports           (B-04)  5. signal-validation reports (B-04)
  3. scenario reports         (B-04)  6. dataset snapshots · 7. chart
  annotations · 8. journal entries · 9. trade-plan notes

Unknown ids are excluded; if nothing resolves, the bundle is EMPTY and the
responder's own `GROUNDING_REQUIRED` refusal fires — honest, never invented.
"""

from __future__ import annotations

from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.collaboration.contracts import GroundingBundle
from app.db.models.chart_research_annotation import ChartResearchAnnotation
from app.db.models.correlation_report import CorrelationReport
from app.db.models.dataset import DatasetSnapshot
from app.db.models.manual_trade_journal_entry import ManualTradeJournalEntryRecord
from app.db.models.portfolio_risk_report import PortfolioRiskReport
from app.db.models.regime_report import RegimeReport
from app.db.models.scenario_report import ScenarioReport
from app.db.models.signal_validation_report import SignalValidationReport
from app.db.models.trade_plan_note import TradePlanNoteRecord

_TRUNCATE = 500


def _clip(value: str | None) -> str:
    if not value:
        return ""
    return value[: _TRUNCATE]


async def _resolve_family(
    session: AsyncSession, *, model, ids: list[str], build_summary
) -> tuple[list[str], list[str]]:
    resolved_ids: list[str] = []
    summaries: list[str] = []
    for artifact_id in ids:
        row = await session.get(model, artifact_id)
        if row is None:
            continue
        summary = build_summary(row)
        if not summary:
            continue
        resolved_ids.append(artifact_id)
        summaries.append(summary)
    return resolved_ids, summaries


async def assemble_grounding(
    session: AsyncSession,
    *,
    source_ids: Sequence[str],
) -> GroundingBundle:
    """Resolve operator-selected ids to persisted summaries (order-preserving,
    deduplicated, capped at the request schema's bound)."""
    ordered: list[str] = []
    for item in source_ids:
        if item not in ordered:
            ordered.append(item)

    artifact_ids: list[str] = []
    summaries: list[str] = []

    def extend(ids: list[str], texts: list[str]) -> None:
        artifact_ids.extend(ids)
        summaries.extend(texts)

    remaining = list(ordered)
    families = [
        (
            CorrelationReport,
            lambda row: (
                f"Correlation {row.left_symbol}/{row.right_symbol} "
                f"r={float(row.correlation_value):.4f} n={row.sample_count}"
            ),
        ),
        (
            RegimeReport,
            lambda row: (
                f"Regime {row.regime_label} confidence={float(row.confidence):.3f} "
                f"on {row.symbol} {row.timeframe}"
            ),
        ),
        (
            ScenarioReport,
            lambda row: (
                f"Scenario '{row.scenario_name}': "
                f"{_clip(row.notes) or 'hypothetical research scenario'}"
            ),
        ),
        (
            PortfolioRiskReport,
            lambda row: (
                f"Portfolio-risk research '{_clip(getattr(row, 'report_name', ''))}': "
                f"hypothetical market-series risk, n={row.sample_count}"
            ),
        ),
        (
            SignalValidationReport,
            lambda row: (
                f"Signal validation: n={row.sample_count} signals, "
                f"outcomes={row.outcome_data_status.get('status')}"
            ),
        ),
        (
            DatasetSnapshot,
            lambda row: (
                f"Dataset {row.dataset_id} v{row.version} source={row.source} "
                f"content_hash={row.content_hash[:12] if row.content_hash else 'none'}"
            ),
        ),
        (
            ChartResearchAnnotation,
            lambda row: _clip(getattr(row, "content", None)),
        ),
        (
            ManualTradeJournalEntryRecord,
            lambda row: _clip(f"{row.title}: {getattr(row, 'lesson_notes', None) or ''}"),
        ),
        (
            TradePlanNoteRecord,
            lambda row: _clip(f"{row.title}: {getattr(row, 'scenario_notes', None) or ''}"),
        ),
    ]
    for model, build_summary in families:
        ids, texts = await _resolve_family(
            session, model=model, ids=remaining, build_summary=build_summary
        )
        extend(ids, texts)
        resolved_set = set(ids)
        remaining = [item for item in remaining if item not in resolved_set]

    return GroundingBundle(
        source_artifact_ids=tuple(artifact_ids),
        summaries=tuple(summaries),
    )
