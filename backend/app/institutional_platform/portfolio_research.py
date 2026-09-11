"""Portfolio research dashboard and advanced reporting (W7-U06)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.time import utc_now
from app.db.models.execution_experiment import ExecutionResearchExperiment
from app.db.models.research_management import ResearchCollection, ResearchTag
from app.db.models.simulated_execution import SimulatedExecutionRun

PORTFOLIO_RESEARCH_VERSION = "w7-u06.portfolio_research.v1"
PORTFOLIO_RESEARCH_STATUS = "research_only"
PORTFOLIO_RESEARCH_DISCLAIMER = (
    "Portfolio research view over governed advisory and simulated artifacts only. "
    "Figures are hypothetical research descriptors, not live venue records."
)


@dataclass(frozen=True, slots=True)
class PortfolioResearchMetric:
    key: str
    label: str
    value: int
    sample_count: int
    source_artifact_ids: tuple[str, ...]
    uncertainty: dict[str, Any]
    limitations: tuple[str, ...]
    economic_usefulness: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["source_artifact_ids"] = list(self.source_artifact_ids)
        data["limitations"] = list(self.limitations)
        return data


@dataclass(frozen=True, slots=True)
class PortfolioResearchSnapshot:
    operator_id: str
    generated_at: str
    research_status: str
    disclaimer: str
    aggregate_cards: tuple[PortfolioResearchMetric, ...]
    included_scope: dict[str, Any]
    limitations: tuple[str, ...]
    economic_usefulness: dict[str, Any]
    source_artifact_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "operator_id": self.operator_id,
            "generated_at": self.generated_at,
            "research_status": self.research_status,
            "disclaimer": self.disclaimer,
            "aggregate_cards": [card.to_dict() for card in self.aggregate_cards],
            "included_scope": self.included_scope,
            "limitations": list(self.limitations),
            "economic_usefulness": self.economic_usefulness,
            "source_artifact_ids": list(self.source_artifact_ids),
        }


class PortfolioResearchService:
    """Builds read-only portfolio research snapshots from existing artifacts."""

    method_version = PORTFOLIO_RESEARCH_VERSION

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def dashboard(self, *, operator_id: str) -> dict[str, Any]:
        snapshot = await self._snapshot(operator_id=operator_id)
        return snapshot.to_dict()

    async def advanced_report(self, *, operator_id: str) -> dict[str, Any]:
        snapshot = await self._snapshot(operator_id=operator_id)
        snapshot_dict = snapshot.to_dict()
        report_hash = self._hash_report(snapshot_dict)
        sections = [
            {
                "section_id": card.key,
                "title": card.label,
                "figure": {
                    "value": card.value,
                    "sample_count": card.sample_count,
                    "uncertainty": card.uncertainty,
                    "limitations": list(card.limitations),
                    "source_artifact_ids": list(card.source_artifact_ids),
                },
                "economic_usefulness": card.economic_usefulness,
            }
            for card in snapshot.aggregate_cards
        ]
        return {
            "report_id": report_hash,
            "method_version": self.method_version,
            "operator_id": operator_id,
            "research_status": PORTFOLIO_RESEARCH_STATUS,
            "disclaimer": PORTFOLIO_RESEARCH_DISCLAIMER,
            "included_scope": snapshot.included_scope,
            "sections": sections,
            "source_artifact_ids": list(snapshot.source_artifact_ids),
            "limitations": list(snapshot.limitations),
            "economic_usefulness": snapshot.economic_usefulness,
            "report_hash": report_hash,
            "export_preview_markdown": self._markdown_export(
                snapshot=snapshot,
                report_hash=report_hash,
            ),
            "persisted": False,
        }

    async def _snapshot(self, *, operator_id: str) -> PortfolioResearchSnapshot:
        runs = list(
            (
                await self._session.scalars(
                    select(SimulatedExecutionRun)
                    .where(SimulatedExecutionRun.operator_id == operator_id)
                    .order_by(SimulatedExecutionRun.created_at.desc())
                    .limit(200)
                )
            ).all()
        )
        experiments = list(
            (
                await self._session.scalars(
                    select(ExecutionResearchExperiment)
                    .where(ExecutionResearchExperiment.operator_id == operator_id)
                    .order_by(ExecutionResearchExperiment.created_at.desc())
                    .limit(200)
                )
            ).all()
        )
        collections = list(
            (
                await self._session.scalars(
                    select(ResearchCollection)
                    .where(ResearchCollection.operator_id == operator_id)
                    .order_by(ResearchCollection.updated_at.desc())
                    .limit(200)
                )
            ).all()
        )
        tags = list(
            (
                await self._session.scalars(
                    select(ResearchTag)
                    .where(ResearchTag.operator_id == operator_id)
                    .order_by(ResearchTag.created_at.desc())
                    .limit(200)
                )
            ).all()
        )
        run_ids = tuple(run.run_id for run in runs)
        experiment_ids = tuple(item.experiment_id for item in experiments)
        collection_ids = tuple(item.collection_id for item in collections)
        tag_ids = tuple(item.tag_id for item in tags)
        cards = (
            self._metric(
                key="simulated_research_runs",
                label="Simulated research runs",
                ids=run_ids,
            ),
            self._metric(
                key="simulated_research_experiments",
                label="Simulated research experiments",
                ids=experiment_ids,
            ),
            self._metric(
                key="research_collections",
                label="Research collections",
                ids=collection_ids,
            ),
            self._metric(
                key="research_tags",
                label="Research tags",
                ids=tag_ids,
            ),
        )
        source_ids = tuple(
            item
            for group in (run_ids, experiment_ids, collection_ids, tag_ids)
            for item in group
        )
        included_scope = {
            "policy": "full_current_operator_scope_no_cherry_picking",
            "operator_id": operator_id,
            "artifact_counts": {card.key: card.value for card in cards},
            "artifact_source_ids": list(source_ids),
        }
        return PortfolioResearchSnapshot(
            operator_id=operator_id,
            generated_at=utc_now().isoformat(),
            research_status=PORTFOLIO_RESEARCH_STATUS,
            disclaimer=PORTFOLIO_RESEARCH_DISCLAIMER,
            aggregate_cards=cards,
            included_scope=included_scope,
            limitations=(
                "descriptive_research_aggregation_only",
                "not_a_live_venue_record",
                "not_a_trade_instruction",
                "economic_usefulness_not_assessed",
            ),
            economic_usefulness={
                "verdict": "not_assessed",
                "reason": (
                    "Dashboard aggregates governed research artifacts without "
                    "economic conclusion."
                ),
            },
            source_artifact_ids=source_ids,
        )

    def _metric(self, *, key: str, label: str, ids: tuple[str, ...]) -> PortfolioResearchMetric:
        sample_count = len(ids)
        return PortfolioResearchMetric(
            key=key,
            label=label,
            value=sample_count,
            sample_count=sample_count,
            source_artifact_ids=ids,
            uncertainty={
                "method": "descriptive_count_only",
                "sample_count": sample_count,
                "interval": "not_applicable_for_count_descriptor",
            },
            limitations=(
                "count_descriptor_only",
                "insufficient_for_economic_conclusion",
            ),
            economic_usefulness={
                "verdict": "not_assessed",
                "reason": "Count descriptor is not an economic outcome.",
            },
        )

    def _hash_report(self, payload: dict[str, Any]) -> str:
        stable_payload = {
            "operator_id": payload["operator_id"],
            "included_scope": payload["included_scope"],
            "aggregate_cards": [
                {
                    "key": card["key"],
                    "value": card["value"],
                    "source_artifact_ids": card["source_artifact_ids"],
                    "sample_count": card["sample_count"],
                }
                for card in payload["aggregate_cards"]
            ],
            "method_version": self.method_version,
        }
        encoded = json.dumps(stable_payload, sort_keys=True).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def _markdown_export(
        self, *, snapshot: PortfolioResearchSnapshot, report_hash: str
    ) -> str:
        lines = [
            "# Portfolio Research Report",
            "",
            PORTFOLIO_RESEARCH_DISCLAIMER,
            "",
            f"Research status: {snapshot.research_status}",
            f"Report hash: {report_hash}",
            "",
            "## Figures",
        ]
        for card in snapshot.aggregate_cards:
            lines.append(
                f"- {card.label}: {card.value} "
                f"(sample_count={card.sample_count}, uncertainty={card.uncertainty['method']})"
            )
        lines.extend(
            [
                "",
                "## Economic usefulness",
                snapshot.economic_usefulness["verdict"],
                "",
                "## Limitations",
                *[f"- {item}" for item in snapshot.limitations],
            ]
        )
        return "\n".join(lines)
