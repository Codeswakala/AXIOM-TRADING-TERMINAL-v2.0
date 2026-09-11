"""Seed W7-U08 closeout evidence rows for all Wave-7 tables."""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from uuid import uuid4

REPO_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = REPO_ROOT / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.auth.security import hash_password  # noqa: E402
from app.core.time import utc_now  # noqa: E402
from app.db.models.operator import Operator  # noqa: E402
from app.db.models.scenario_report import ScenarioReport  # noqa: E402
from app.db.session import close_db, init_db, session_scope  # noqa: E402
from app.institutional_platform import (  # noqa: E402
    ResearchManagementRepository,
    WorkspacePreferenceRepository,
)

OUTPUT = REPO_ROOT / "docs" / "evidence" / "W7-U08_CLOSEOUT_SEED.json"


async def scenario_report(session) -> ScenarioReport:  # noqa: ANN001
    now = utc_now()
    report = ScenarioReport(
        id=str(uuid4()),
        created_at=now,
        artifact_type="scenario_report",
        method_version="w7-u08.closeout.seed.v1",
        market_class="forex",
        symbol="EURUSD",
        timeframe="M1",
        as_of_start=now,
        as_of_end=now,
        sample_count=3,
        scenario_name=f"w7_u08_closeout_{uuid4().hex[:8]}",
        hypothetical_return=-0.01,
        scenario_result={"hypothetical_return": -0.01},
        assumptions={"scenario_name": "w7_u08_closeout"},
        inputs={"baseline_returns": [0.0, 0.01]},
        uncertainty={"method": "closeout_seed", "sample_count": 3},
        economic_usefulness={"verdict": "not_assessed"},
        config={"fixture": "w7-u08"},
        input_lineage={"policy": "closeout_seed"},
        source_artifact_ids=[],
        market_scope={"market_class": "forex"},
        results={"scenario_result": {"hypothetical_return": -0.01}},
        limitations=["research_only"],
        report_hash=f"w7u08-{uuid4().hex}",
        research_status="research_only",
        created_by="w7-u08-evidence",
        audit_correlation_id=str(uuid4()),
        notes="Wave-7 closeout evidence source artifact.",
    )
    session.add(report)
    await session.flush()
    return report


async def main() -> None:
    init_db()
    async with session_scope() as session:
        operator = Operator(
            username=f"w7-u08-closeout-{uuid4().hex[:8]}",
            hashed_password=hash_password("operator-pass-123"),
            role="operator",
            is_active=True,
        )
        session.add(operator)
        await session.flush()
        report = await scenario_report(session)
        preference = await WorkspacePreferenceRepository(session).create_preference(
            operator_id=operator.id,
            payload={
                "workspace_key": f"w7-u08-closeout-{uuid4().hex[:6]}",
                "layout_config": {"density": "comfortable"},
                "visible_modules": ["operations"],
                "theme_config": {"mode": "dark"},
                "metadata": {"note": "wave7 closeout evidence"},
            },
        )
        repo = ResearchManagementRepository(session)
        collection = await repo.create_collection(
            operator_id=operator.id,
            payload={"name": f"W7-U08 Closeout {uuid4().hex[:8]}"},
        )
        member = await repo.add_member(
            collection_id=collection.collection_id,
            operator_id=operator.id,
            payload={"artifact_type": "scenario_report", "artifact_id": report.id},
        )
        tag = await repo.create_tag(
            operator_id=operator.id,
            payload={
                "artifact_type": "scenario_report",
                "artifact_id": report.id,
                "tag": f"w7-u08-closeout-{uuid4().hex[:6]}",
            },
        )
        result = {
            "operator_id": operator.id,
            "scenario_report_id": report.id,
            "preference_id": preference.preference_id,
            "collection_id": collection.collection_id,
            "member_id": member.member_id,
            "tag_id": tag.tag_id,
        }
        OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
        print("W7_U08_CLOSEOUT_SEED_COMPLETE")
        for key, value in result.items():
            print(f"{key.upper()}={value}")
    await close_db()


if __name__ == "__main__":
    asyncio.run(main())
