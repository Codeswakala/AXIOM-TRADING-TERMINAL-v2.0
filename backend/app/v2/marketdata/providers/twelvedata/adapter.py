"""Twelve Data P1 fixture adapter — architecture candidate only.

Reads workspace-reviewed static fixtures through FixtureTransport; performs
no network activity; holds no credential; reports itself truthfully.
"""

from __future__ import annotations

from pathlib import Path

from app.v2.marketdata.providers.contract import (
    FixtureCredentialResolver,
    FixtureTransport,
    ProviderAdapter,
)
from app.v2.marketdata.providers.twelvedata.normalize import (
    NormalizedBar,
    normalize_quote,
    normalize_time_series,
)
from app.v2.marketdata.providers.twelvedata.symbols import to_td

FIXTURES_ROOT = Path(__file__).parent / "fixtures"


class TwelveDataAdapter(ProviderAdapter):
    """P1 fixture-fed adapter. Live entries inherit the refusal stubs."""

    provider_id = "twelvedata"
    display_name = "Twelve Data (architecture candidate)"

    def __init__(
        self,
        transport: FixtureTransport | None = None,
        credentials: FixtureCredentialResolver | None = None,
    ) -> None:
        super().__init__(
            transport=transport or FixtureTransport(FIXTURES_ROOT),
            credentials=credentials,
        )

    def fetch_bars_fixture(
        self, instrument_id: str, timeframe: str, *, fixture_name: str
    ) -> list[NormalizedBar]:
        """Contract-test path: load + normalize a named static fixture."""
        payload = self._transport.load(fixture_name)
        return normalize_time_series(
            payload,
            requested_instrument_id=instrument_id,
            requested_timeframe=timeframe,
        )

    def fetch_quote_fixture(self, instrument_id: str, *, fixture_name: str) -> dict:
        payload = self._transport.load(fixture_name)
        return normalize_quote(payload, requested_instrument_id=instrument_id)

    def supported_symbol(self, instrument_id: str) -> bool:
        return to_td(instrument_id) is not None
