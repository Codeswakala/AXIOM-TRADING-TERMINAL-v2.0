"""Portfolio research dashboard/report schemas (W7-U06)."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class PortfolioResearchMetricRead(BaseModel):
    key: str
    label: str
    value: int
    sample_count: int
    source_artifact_ids: list[str]
    uncertainty: dict[str, Any]
    limitations: list[str]
    economic_usefulness: dict[str, Any]


class PortfolioResearchDashboardRead(BaseModel):
    operator_id: str
    generated_at: str
    research_status: str
    disclaimer: str
    aggregate_cards: list[PortfolioResearchMetricRead]
    included_scope: dict[str, Any]
    limitations: list[str]
    economic_usefulness: dict[str, Any]
    source_artifact_ids: list[str]


class AdvancedResearchReportRead(BaseModel):
    report_id: str
    method_version: str
    operator_id: str
    research_status: str
    disclaimer: str
    included_scope: dict[str, Any]
    sections: list[dict[str, Any]]
    source_artifact_ids: list[str]
    limitations: list[str]
    economic_usefulness: dict[str, Any]
    report_hash: str
    export_preview_markdown: str
    persisted: bool
