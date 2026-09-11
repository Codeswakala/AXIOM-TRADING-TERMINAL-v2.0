"""Seed W5-U06 inert trade plan note evidence records.

This creates operator-authored research notes only. It does not place orders,
size positions, contact a broker, emit signals, or open the Governance Gate.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.collaboration import TradePlanNoteRepository  # noqa: E402
from app.db.session import close_db, init_db, session_scope  # noqa: E402


async def main() -> None:
    init_db()
    async with session_scope() as session:
        repository = TradePlanNoteRepository(session)
        plan = await repository.create_plan(
            operator_id="operator_evidence",
            payload={
                "title": "W5-U06 inert research plan note",
                "market_context": "EURUSD M1 research context linked to governed artifacts.",
                "hypothesis": "If guardrail context remains consistent, operator may continue research review.",
                "linked_signal_ids": ["W5-U06-evidence-signal"],
                "linked_report_ids": ["W5-U06-evidence-scenario", "W5-U06-evidence-risk"],
                "scenario_notes": "Hypothetical scenario context only; not a prediction.",
                "risk_notes": "Research risk notes only; no sizing or execution instruction.",
                "invalidating_conditions_text": "Archive if source evidence becomes stale or contradicted.",
                "decision_status": "draft",
            },
        )
    await close_db()
    print("W5_U06_TRADE_PLAN_NOTE_SEED_COMPLETE")
    print(f"trade_plan_note\t{plan.plan_id}\t{plan.title}")


if __name__ == "__main__":
    asyncio.run(main())
