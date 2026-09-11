"""BE-4 repositories — append-only (defense-in-depth alongside the R-2
DB guards). No update() or delete() method exists on any class here."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.v2_research import (
    V2ChartIntelligenceReport,
    V2ComputationVersion,
    V2MarketContextReport,
)


class V2ComputationVersionRepository:
    """Read + append-only registry access."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[V2ComputationVersion]:
        result = await self._session.execute(
            select(V2ComputationVersion).order_by(
                V2ComputationVersion.component, V2ComputationVersion.version
            )
        )
        return list(result.scalars().all())

    async def get(self, component: str, version: str) -> V2ComputationVersion | None:
        result = await self._session.execute(
            select(V2ComputationVersion).where(
                V2ComputationVersion.component == component,
                V2ComputationVersion.version == version,
            )
        )
        return result.scalar_one_or_none()


class V2MarketContextReportRepository:
    """Append + read. Reports are immutable artifacts."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def append(self, report: V2MarketContextReport) -> V2MarketContextReport:
        self._session.add(report)
        await self._session.flush()
        return report

    async def get(self, report_id: str) -> V2MarketContextReport | None:
        result = await self._session.execute(
            select(V2MarketContextReport).where(V2MarketContextReport.id == report_id)
        )
        return result.scalar_one_or_none()

    async def find_by_anchor(
        self, instrument_id: str, input_content_hash: str, engine_versions_hash: str
    ) -> V2MarketContextReport | None:
        """Determinism-anchor lookup (R-1 idempotency: same input + versions
        ⇒ the existing report is returned, not duplicated)."""
        result = await self._session.execute(
            select(V2MarketContextReport).where(
                V2MarketContextReport.instrument_id == instrument_id,
                V2MarketContextReport.input_content_hash == input_content_hash,
                V2MarketContextReport.engine_versions_hash == engine_versions_hash,
            )
        )
        return result.scalar_one_or_none()

    async def list_reports(
        self,
        *,
        instrument_id: str | None = None,
        mode: str | None = None,
        status: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[V2MarketContextReport]:
        stmt = select(V2MarketContextReport).order_by(
            V2MarketContextReport.created_at.desc()
        )
        if instrument_id is not None:
            stmt = stmt.where(V2MarketContextReport.instrument_id == instrument_id)
        if mode is not None:
            stmt = stmt.where(V2MarketContextReport.mode == mode)
        if status is not None:
            stmt = stmt.where(V2MarketContextReport.status == status)
        stmt = stmt.limit(min(limit, 500)).offset(offset)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())


class V2ChartIntelligenceReportRepository:
    """Append + read. Artifacts are immutable."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def append(
        self, report: V2ChartIntelligenceReport
    ) -> V2ChartIntelligenceReport:
        self._session.add(report)
        await self._session.flush()
        return report

    async def get(self, report_id: str) -> V2ChartIntelligenceReport | None:
        result = await self._session.execute(
            select(V2ChartIntelligenceReport).where(
                V2ChartIntelligenceReport.id == report_id
            )
        )
        return result.scalar_one_or_none()

    async def get_by_market_context(
        self, market_context_report_id: str
    ) -> V2ChartIntelligenceReport | None:
        result = await self._session.execute(
            select(V2ChartIntelligenceReport).where(
                V2ChartIntelligenceReport.market_context_report_id
                == market_context_report_id
            )
        )
        return result.scalars().first()


def utc_normalized(value: datetime | None) -> datetime | None:
    """SQLite discards tz on DateTime(timezone=True) — BE-2 normalizer
    pattern reused."""
    from datetime import timezone

    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value
