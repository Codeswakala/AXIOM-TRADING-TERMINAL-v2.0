"""DA capture tooling — DATA-P02 evidence fixture (untracked; NOT in any patch).

Seeds six days of M1 synthetic history (8640 bars/symbol × 11 symbols) into
the LOCAL dev database via the EXISTING chart_seed_service.seed_chart_history
seam — the same service the platform's authenticated seed-history endpoint
uses, invoked with a larger bars argument. No generator, walk, seeding,
correlation or provenance logic is modified (R1).

Why six days: D1 aggregation needs ≥ 1440 minutes of M1 coverage per complete
daily bucket; six days yields five complete UTC-day buckets plus partial edge
days (excluded and disclosed by the M6 rule). Disclosed in the delivery report
as a local evidence fixture (TD-UI-DATA-P02-* register row).
"""

from __future__ import annotations

import asyncio

from app.core.config import get_settings
from app.db.session import session_scope
from app.services.chart_seed_service import seed_chart_history


async def main() -> None:
    settings = get_settings()
    symbols = settings.live_market_symbols_list
    print(f"symbols: {symbols}")
    async with session_scope() as session:
        counts = await seed_chart_history(
            session,
            symbols=symbols,
            timeframe="M1",
            bars=8640,  # six days of minute bars per symbol
        )
        print("seeded:", counts)


if __name__ == "__main__":
    asyncio.run(main())
