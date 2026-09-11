"""Seed W7-U07 multi-user readiness evidence resources."""

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
from app.db.models.operator import Operator  # noqa: E402
from app.db.session import close_db, init_db, session_scope  # noqa: E402
from app.institutional_platform import (  # noqa: E402
    ResearchManagementRepository,
    WorkspacePreferenceRepository,
)

PASSWORD = "operator-pass-123"
OUTPUT = REPO_ROOT / "docs" / "evidence" / "W7-U07_READINESS_SEED.json"


def workspace_payload(key: str) -> dict[str, object]:
    return {
        "workspace_key": key,
        "layout_config": {"density": "comfortable"},
        "visible_modules": ["operations"],
        "theme_config": {"mode": "dark"},
        "metadata": {"note": "w7-u07 readiness proof"},
    }


async def main() -> None:
    init_db()
    async with session_scope() as session:
        unprivileged = Operator(
            username=f"w7-u07-unprivileged-{uuid4().hex[:8]}",
            hashed_password=hash_password(PASSWORD),
            role="unprivileged",
            is_active=True,
        )
        session.add(unprivileged)
        await session.flush()
        a = Operator(
            username=f"w7-u07-a-{uuid4().hex[:8]}",
            hashed_password=hash_password(PASSWORD),
            role="operator",
            is_active=True,
        )
        b = Operator(
            username=f"w7-u07-b-{uuid4().hex[:8]}",
            hashed_password=hash_password(PASSWORD),
            role="operator",
            is_active=True,
        )
        session.add_all([a, b])
        await session.flush()
        prefs = WorkspacePreferenceRepository(session)
        research = ResearchManagementRepository(session)
        pref_a = await prefs.create_preference(
            operator_id=a.id,
            payload=workspace_payload("a-readiness-workspace"),
        )
        pref_b = await prefs.create_preference(
            operator_id=b.id,
            payload=workspace_payload("b-readiness-workspace"),
        )
        collection_a = await research.create_collection(
            operator_id=a.id,
            payload={"name": f"A readiness {uuid4().hex[:6]}"},
        )
        collection_b = await research.create_collection(
            operator_id=b.id,
            payload={"name": f"B readiness {uuid4().hex[:6]}"},
        )
        result = {
            "unprivileged_id": unprivileged.id,
            "unprivileged_username": unprivileged.username,
            "operator_a_id": a.id,
            "operator_a_username": a.username,
            "operator_b_id": b.id,
            "operator_b_username": b.username,
            "operator_password": PASSWORD,
            "preference_a_id": pref_a.preference_id,
            "preference_b_id": pref_b.preference_id,
            "collection_a_id": collection_a.collection_id,
            "collection_b_id": collection_b.collection_id,
        }
        OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
        print("W7_U07_READINESS_SEED_COMPLETE")
        for key, value in result.items():
            print(f"{key.upper()}={value}")
    await close_db()


if __name__ == "__main__":
    asyncio.run(main())
