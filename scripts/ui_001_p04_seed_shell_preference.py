"""Seed UI-001-P04 shell preference evidence row via existing W7-U02 repository."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = REPO_ROOT / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.auth.security import hash_password  # noqa: E402
from app.db.models.operator import Operator  # noqa: E402
from app.db.session import close_db, init_db, session_scope  # noqa: E402
from app.institutional_platform import WorkspacePreferenceRepository  # noqa: E402

SHELL_WORKSPACE_KEY = "institutional-shell-v1"


def payload() -> dict[str, object]:
    return {
        "workspace_key": SHELL_WORKSPACE_KEY,
        "layout_config": {
            "active_workspace": "monitor.operations",
            "last_route": "/signals",
            "navigation": {"collapsed": False},
            "panel_layout": {
                "layoutId": "session.monitor.operations",
                "workspaceId": "monitor.operations",
                "placements": [
                    {
                        "panelId": "shell.context.workspace",
                        "dock": "right",
                        "order": 0,
                        "dimensions": {"width": 352, "height": 180},
                        "visible": True,
                    }
                ],
            },
            "persistence_scope": "operator_shell_layout",
        },
        "visible_modules": ["operations", "research_journal", "institutional_intelligence"],
        "theme_config": {"mode": "dark", "density": "institutional"},
        "metadata": {"ui_workstream": "UI-001-P04", "version": "shell-persistence-v1"},
    }


async def main() -> None:
    init_db()
    async with session_scope() as session:
        operator = Operator(
            username="ui-p04-shell-evidence-operator",
            hashed_password=hash_password("operator-pass-123"),
            role="operator",
            is_active=True,
        )
        session.add(operator)
        await session.flush()
        repository = WorkspacePreferenceRepository(session)
        existing = await repository.get_by_workspace_key(
            operator_id=operator.id,
            workspace_key=SHELL_WORKSPACE_KEY,
        )
        if existing is None:
            preference = await repository.create_preference(
                operator_id=operator.id,
                payload=payload(),
            )
            action = "created"
        else:
            preference = await repository.update_preference(
                operator_id=operator.id,
                preference_id=existing.preference_id,
                payload=payload(),
            )
            action = "updated"
        assert preference is not None
        print("UI_001_P04_SHELL_PREFERENCE_SEED_COMPLETE")
        print(f"SHELL_PREFERENCE_ACTION={action}")
        print(f"OPERATOR_ID={operator.id}")
        print(f"SHELL_WORKSPACE_KEY={SHELL_WORKSPACE_KEY}")
        print(f"SHELL_PREFERENCE_ID={preference.preference_id}")
        print(f"SHELL_AUDIT_CORRELATION_ID={preference.audit_correlation_id}")
    await close_db()


if __name__ == "__main__":
    asyncio.run(main())
