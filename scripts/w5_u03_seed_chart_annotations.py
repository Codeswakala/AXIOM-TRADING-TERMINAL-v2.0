"""Seed W5-U03 inert chart annotation evidence records.

Run after `alembic upgrade head`. The script creates operator-authored chart
research annotations only; it does not emit signals, place orders, call an LLM,
or open the Governance Gate.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.collaboration import (  # noqa: E402
    ChartResearchAnnotationDraft,
    ChartResearchAnnotationRepository,
)
from app.db.session import close_db, init_db, session_scope  # noqa: E402


async def main() -> None:
    init_db()
    created: list[str] = []
    async with session_scope() as session:
        repository = ChartResearchAnnotationRepository(session)
        drafts = (
            ChartResearchAnnotationDraft(
                artifact_type="chart_research_annotation",
                chart_context={
                    "market_class": "forex",
                    "symbol": "EURUSD",
                    "timeframe": "M1",
                    "anchor": {"mode": "visible_window", "label": "recent guardrail context"},
                },
                content={
                    "drawing_kind": "research_note",
                    "text": "Guardrail context note linked to governed advisory evidence.",
                    "visual": {"x_percent": 18, "y_percent": 28},
                },
                source_artifact_ids=("W5-U03-evidence-signal", "W5-U03-evidence-report"),
                provenance={"seed_script": "w5_u03_seed_chart_annotations.py"},
                uncertainty={"method": "not_applicable_operator_markup"},
            ),
            ChartResearchAnnotationDraft(
                artifact_type="chart_research_drawing",
                chart_context={
                    "market_class": "forex",
                    "symbol": "EURUSD",
                    "timeframe": "M1",
                    "anchor": {"mode": "operator_drawn_zone", "label": "research zone"},
                },
                content={
                    "drawing_kind": "research_zone",
                    "text": "Operator-marked research zone for later review only.",
                    "visual": {"x_percent": 54, "y_percent": 44},
                },
                source_artifact_ids=("W5-U03-evidence-chart-context",),
                provenance={"seed_script": "w5_u03_seed_chart_annotations.py"},
                uncertainty={"method": "not_applicable_operator_markup"},
            ),
        )
        for draft in drafts:
            annotation = await repository.create_annotation(
                draft=draft, operator_id="operator_evidence"
            )
            created.append(annotation.id)
    await close_db()
    print("W5_U03_CHART_ANNOTATION_SEED_COMPLETE")
    for annotation_id in created:
        print(f"chart_research_annotation\t{annotation_id}")


if __name__ == "__main__":
    asyncio.run(main())
