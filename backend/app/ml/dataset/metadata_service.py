"""Market series metadata persistence service (W2-U02)."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.market_metadata import MarketSeriesMetadata
from app.ml.dataset.market_data_query import MarketSeriesKey, MarketSeriesMetadataRead


class MarketMetadataService:
    """Stores/query governance/evaluation metadata for market series."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def upsert_metadata(self, metadata: MarketSeriesMetadataRead) -> MarketSeriesMetadata:
        key = metadata.series_key
        result = await self._session.execute(
            select(MarketSeriesMetadata).where(
                MarketSeriesMetadata.market_class == key.market_class,
                MarketSeriesMetadata.provider == key.provider,
                MarketSeriesMetadata.symbol == key.symbol,
                MarketSeriesMetadata.timeframe == key.timeframe,
            )
        )
        row = result.scalar_one_or_none()
        if row is None:
            row = MarketSeriesMetadata(
                market_class=key.market_class,
                provider=key.provider,
                symbol=key.symbol,
                timeframe=key.timeframe,
                source_authority=metadata.source_authority.value,
            )
            self._session.add(row)
        row.session_calendar = metadata.session_calendar
        row.tick_size = metadata.tick_size
        row.price_precision = metadata.price_precision
        row.timezone_assumption = metadata.timezone_assumption
        row.source_authority = metadata.source_authority.value
        row.known_limitations = metadata.known_limitations
        row.metadata_role = metadata.metadata_role
        await self._session.flush()
        return row

    async def get_metadata(self, key: MarketSeriesKey) -> MarketSeriesMetadataRead | None:
        result = await self._session.execute(
            select(MarketSeriesMetadata).where(
                MarketSeriesMetadata.market_class == key.market_class,
                MarketSeriesMetadata.provider == key.provider,
                MarketSeriesMetadata.symbol == key.symbol,
                MarketSeriesMetadata.timeframe == key.timeframe,
            )
        )
        row = result.scalar_one_or_none()
        if row is None:
            return None
        from app.ml.dataset.chronology_guard import SourceAuthority

        return MarketSeriesMetadataRead(
            series_key=key,
            session_calendar=row.session_calendar,
            tick_size=row.tick_size,
            price_precision=row.price_precision,
            timezone_assumption=row.timezone_assumption,
            source_authority=SourceAuthority(row.source_authority),
            known_limitations=row.known_limitations,
            metadata_role=row.metadata_role,
        )

    async def list_market_classes(self) -> list[str]:
        result = await self._session.execute(
            select(MarketSeriesMetadata.market_class).distinct().order_by(
                MarketSeriesMetadata.market_class
            )
        )
        return [str(row[0]) for row in result.all()]
