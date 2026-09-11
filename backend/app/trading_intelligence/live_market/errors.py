"""Live market inference adapter errors (W3-U04)."""

from __future__ import annotations


class LiveMarketInferenceError(ValueError):
    """Raised when live-market data cannot safely become inference input."""
