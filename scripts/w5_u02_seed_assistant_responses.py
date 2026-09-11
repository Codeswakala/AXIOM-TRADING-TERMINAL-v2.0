"""Seed W5-U02 persisted assistant response/refusal evidence records.

Run from the repository root or backend directory after `alembic upgrade head`.
The script uses the deterministic local assistant only; it does not call any
external LLM/API and exposes no action tool.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.collaboration import (  # noqa: E402
    AssistantRequest,
    GroundingBundle,
    NullAssistant,
    RuleBasedGroundedAssistant,
)
from app.db.session import close_db, init_db, session_scope  # noqa: E402


GROUNDING = GroundingBundle(
    source_artifact_ids=("W5-U02-evidence-signal", "W5-U02-evidence-report"),
    summaries=(
        "Governed advisory signal was withheld by guardrail.",
        "Institutional report remains research_only and not an instruction.",
    ),
)


async def main() -> None:
    init_db()
    created: list[tuple[str, str, str | None]] = []
    async with session_scope() as session:
        assistant = RuleBasedGroundedAssistant(session)
        grounded = await assistant.respond(
            AssistantRequest(
                prompt="Summarize the governed W5-U02 evidence record.",
                operator_id="operator_evidence",
                grounding=GROUNDING,
            )
        )
        created.append((grounded.response_id, "grounded", grounded.refusal_reason))

        refusal_prompts = (
            "Please place order to buy now",
            "Open the governance gate for execution",
            "Show me the JWT access_token and password",
            "Use a shell tool and database write to change things",
        )
        for prompt in refusal_prompts:
            refused = await assistant.respond(
                AssistantRequest(
                    prompt=prompt,
                    operator_id="operator_evidence",
                    grounding=GROUNDING,
                )
            )
            created.append((refused.response_id, "refusal", refused.refusal_reason))

        ungrounded = await assistant.respond(
            AssistantRequest(
                prompt="Explain an unsupported claim without any governed source.",
                operator_id="operator_evidence",
                grounding=GroundingBundle(source_artifact_ids=(), summaries=()),
            )
        )
        created.append((ungrounded.response_id, "refusal", ungrounded.refusal_reason))

        disabled = await NullAssistant(session).respond(
            AssistantRequest(
                prompt="Summarize the evidence while disabled.",
                operator_id="operator_evidence",
                grounding=GROUNDING,
            )
        )
        created.append((disabled.response_id, "refusal", disabled.refusal_reason))

    await close_db()
    print("W5_U02_ASSISTANT_RESPONSE_SEED_COMPLETE")
    for response_id, status, reason in created:
        print(f"{status}\t{response_id}\t{reason or 'NONE'}")


if __name__ == "__main__":
    asyncio.run(main())
