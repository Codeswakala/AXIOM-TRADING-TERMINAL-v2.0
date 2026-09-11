"""Seed script for SURF-P03 Level-I served evidence data (M3 access-denial).

Creates one active operator with role "unprivileged" — a role absent from
INSTITUTIONAL_ROLE_PERMISSIONS, so the real backend default-deny policy
returns 403 for the institutional platform endpoints. This powers the honest
Level-I capture of the scope-records access-denied notice (M3) and of the
per-source denial rows, produced by the REAL backend, not by interception.

This is an EVIDENCE FIXTURE (deviation register row
TD-UI-SURF-P03-UNPRIVILEGED-EVIDENCE-FIXTURE): it writes one local-dev
operator row only. No schema, endpoint or model change.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from sqlalchemy import select

from app.auth.security import hash_password
from app.db.models.operator import Operator
from app.db.session import init_db, session_scope

PASSWORD = "operator-pass-123"


async def seed_data() -> None:
    init_db()
    async with session_scope() as session:
        username = f"surf-p03-unprivileged-{uuid4().hex[:8]}"
        existing = (
            await session.scalars(select(Operator).where(Operator.username == username))
        ).one_or_none()
        if existing is not None:
            print("already exists:", username)
            return
        operator = Operator(
            username=username,
            hashed_password=hash_password(PASSWORD),
            role="unprivileged",
            is_active=True,
        )
        session.add(operator)
        await session.flush()
        print("created:", username, "role=unprivileged password=" + PASSWORD)


if __name__ == "__main__":
    asyncio.run(seed_data())
