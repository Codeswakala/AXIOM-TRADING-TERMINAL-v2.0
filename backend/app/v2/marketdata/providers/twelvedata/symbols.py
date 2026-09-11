"""Twelve Data symbology ↔ canonical instrument mapping (P1, static).

STATIC CANDIDATE DOCUMENTATION MAPPING — derived from unverified provider
candidate documentation; exact-match only; never auto-extended. The
authoritative runtime mapping lives in the seeded `v2_md_symbol_map` rows
(source_id 'twelvedata', inactive reserved source); this module provides the
pure-function view used by the fixture normalizer.
"""

from __future__ import annotations

from typing import Final

#: TD symbol form → canonical instrument_id. Exactly the 12-instrument universe.
TD_TO_CANONICAL: Final[dict[str, str]] = {
    "EUR/USD": "forex.eurusd",
    "GBP/USD": "forex.gbpusd",
    "USD/JPY": "forex.usdjpy",
    "AUD/USD": "forex.audusd",
    "USD/CAD": "forex.usdcad",
    "USD/CHF": "forex.usdchf",
    "NZD/USD": "forex.nzdusd",
    "EUR/GBP": "forex.eurgbp",
    "BTC/USD": "crypto.btcusd",
    "ETH/USD": "crypto.ethusd",
    "SOL/USD": "crypto.solusd",
    "XAU/USD": "metal.xauusd",
}

CANONICAL_TO_TD: Final[dict[str, str]] = {v: k for k, v in TD_TO_CANONICAL.items()}


def to_canonical(td_symbol: str) -> str | None:
    """Exact-match resolution; unmapped → None (caller surfaces unmapped state)."""
    return TD_TO_CANONICAL.get(td_symbol)


def to_td(instrument_id: str) -> str | None:
    return CANONICAL_TO_TD.get(instrument_id)
