"""Market data ingestion foundation (W0-U03).

Historical CSV loading only — no live feeds in this unit.
"""

from app.ingestion.service import IngestionService

__all__ = ["IngestionService"]
