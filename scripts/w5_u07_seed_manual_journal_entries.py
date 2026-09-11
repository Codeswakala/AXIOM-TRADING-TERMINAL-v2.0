"""Seed W5-U07 inert manual research journal evidence entries.

This creates operator-authored research reflections only. It does not import
broker records, reconcile fills, claim P&L, place orders, or open the Gate.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.collaboration import ManualJournalEntryRepository  # noqa: E402
from app.db.session import close_db, init_db, session_scope  # noqa: E402


async def main() -> None:
    init_db()
    async with session_scope() as session:
        repository = ManualJournalEntryRepository(session)
        entry = await repository.create_entry(
            operator_id="operator_evidence",
            payload={
                "title": "W5-U07 manual research reflection",
                "reflection_text": "Reviewed the research plan and noted process lessons only.",
                "linked_plan_id": "W5-U07-evidence-plan",
                "linked_signal_ids": ["W5-U07-evidence-signal"],
                "linked_report_ids": ["W5-U07-evidence-report"],
                "emotion_tags": ["calm", "patient"],
                "process_tags": ["followed-checklist", "reviewed-guardrails"],
                "lesson_notes": "Keep journal entries as reflections, not records of external activity.",
            },
        )
    await close_db()
    print("W5_U07_MANUAL_JOURNAL_ENTRY_SEED_COMPLETE")
    print(f"manual_trade_journal_entry\t{entry.journal_id}\t{entry.title}")


if __name__ == "__main__":
    asyncio.run(main())
