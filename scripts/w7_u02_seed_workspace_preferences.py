"""Seed W7-U02 operator workspace preference evidence row.

Creates presentation-only preferences for the bootstrap/operator identity. No
execution, broker, account, Gate, or secret fields are written.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from sqlalchemy import select

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.auth.service import AuthService  # noqa: E402
from app.core.config import get_settings  # noqa: E402
from app.db.models.operator import Operator  # noqa: E402
from app.db.session import close_db, init_db, session_scope  # noqa: E402
from app.institutional_platform import WorkspacePreferenceRepository  # noqa: E402


async def main() -> None:
    init_db()
    async with session_scope() as session:
        await AuthService(session, get_settings()).ensure_bootstrap_admin()
        operator = (
            await session.scalars(select(Operator).order_by(Operator.created_at.asc()).limit(1))
        ).first()
        if operator is None:
            raise RuntimeError("W7_U02_OPERATOR_REQUIRED")
        repository = WorkspacePreferenceRepository(session)
        existing = await repository.get_by_workspace_key(
            operator_id=operator.id, workspace_key="default"
        )
        payload = {
            "workspace_key": "default",
            "layout_config": {"density": "comfortable", "columns": 12, "primary_view": "research"},
            "visible_modules": ["operations", "institutional_intelligence", "execution_research"],
            "theme_config": {"mode": "dark", "accent": "blue"},
            "metadata": {"note": "presentation preferences only"},
        }
        if existing is None:
            preference = await repository.create_preference(payload=payload, operator_id=operator.id)
            action = "created"
        else:
            preference = await repository.update_preference(
                preference_id=existing.preference_id,
                payload=payload,
                operator_id=operator.id,
            )
            action = "updated"
        assert preference is not None
    await close_db()
    print("W7_U02_WORKSPACE_PREFERENCE_SEED_COMPLETE")
    print(f"operator_workspace_preference\t{preference.preference_id}\t{action}")


if __name__ == "__main__":
    asyncio.run(main())
