"""Seed W7-U06 portfolio research evidence artifacts."""

from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path
from uuid import uuid4

REPO_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = REPO_ROOT / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from sqlalchemy import select  # noqa: E402

from app.auth.security import hash_password  # noqa: E402
from app.core.time import utc_now  # noqa: E402
from app.db.models.operator import Operator  # noqa: E402
from app.db.models.simulated_execution import SimulatedExecutionRun  # noqa: E402
from app.db.session import close_db, init_db, session_scope  # noqa: E402
from app.institutional_platform import PortfolioResearchService  # noqa: E402

PASSWORD = "operator-pass-123"
OUTPUT = REPO_ROOT / "docs" / "evidence" / "W7-U06_PORTFOLIO_SEED.json"


async def _operator(session, *, username: str, role: str = "operator") -> Operator:  # noqa: ANN001
    existing = (
        await session.scalars(select(Operator).where(Operator.username == username))
    ).one_or_none()
    if existing is not None:
        return existing
    operator = Operator(
        username=username,
        hashed_password=hash_password(
            os.environ.get("AXIOM_BOOTSTRAP_ADMIN_PASSWORD", "admin123")
            if username == os.environ.get("AXIOM_BOOTSTRAP_ADMIN_USERNAME", "admin")
            else PASSWORD
        ),
        role=role,
        is_active=True,
        display_name=f"W7-U06 evidence {role}",
    )
    session.add(operator)
    await session.flush()
    return operator


async def _run(session, *, operator_id: str, label: str) -> SimulatedExecutionRun:  # noqa: ANN001
    run = SimulatedExecutionRun(
        run_id=str(uuid4()),
        created_at=utc_now(),
        operator_id=operator_id,
        simulation_mode="SIMULATED",
        simulation_policy_version="w7-u06.evidence.policy.v1",
        input_artifact_ids=[str(uuid4())],
        replay_scope={"label": label, "scope": "w7-u06-evidence"},
        fill_model_name="evidence_descriptor_only",
        fill_model_version="w7-u06.none",
        assumptions={"fixture": "portfolio_research"},
        limitations=["simulated_research_only"],
        research_status="research_only",
        simulation_disclaimer="SIMULATED research artifact only.",
        audit_correlation_id=str(uuid4()),
    )
    session.add(run)
    await session.flush()
    return run


async def main() -> None:
    init_db()
    async with session_scope() as session:
        admin_username = os.environ.get("AXIOM_BOOTSTRAP_ADMIN_USERNAME", "admin")
        admin = await _operator(session, username=admin_username, role="admin")
        operator_a = await _operator(session, username=f"w7-u06-a-{uuid4().hex[:8]}")
        operator_b = await _operator(session, username=f"w7-u06-b-{uuid4().hex[:8]}")
        admin_run = await _run(session, operator_id=admin.id, label="admin-dashboard")
        run_a = await _run(session, operator_id=operator_a.id, label="operator-a")
        run_b = await _run(session, operator_id=operator_b.id, label="operator-b")
        service = PortfolioResearchService(session)
        admin_dashboard = await service.dashboard(operator_id=admin.id)
        admin_report = await service.advanced_report(operator_id=admin.id)
        result = {
            "admin_operator_id": admin.id,
            "admin_username": admin.username,
            "admin_run_id": admin_run.run_id,
            "operator_a_id": operator_a.id,
            "operator_a_username": operator_a.username,
            "operator_b_id": operator_b.id,
            "operator_b_username": operator_b.username,
            "operator_password": PASSWORD,
            "run_a_id": run_a.run_id,
            "run_b_id": run_b.run_id,
            "admin_dashboard_source_count": len(admin_dashboard["source_artifact_ids"]),
            "admin_report_hash": admin_report["report_hash"],
        }
        OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
        print("W7_U06_PORTFOLIO_RESEARCH_SEED_COMPLETE")
        for key, value in result.items():
            print(f"{key.upper()}={value}")
    await close_db()


if __name__ == "__main__":
    asyncio.run(main())
