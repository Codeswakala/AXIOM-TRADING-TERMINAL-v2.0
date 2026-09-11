"""BO-B-AUDIT.1 empirical repro investigation (DA tooling, untracked).

Recreates the dev configuration exactly — file-based SQLite + StaticPool
(one shared connection, no serialization) — and drives two concurrent
AsyncSessions through the exact interleavings that can orphan a savepoint,
using the REAL AuditRepository.append path.
"""

import asyncio
import logging
import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(BACKEND))

logging.getLogger("app").setLevel(logging.ERROR)  # capture the append failure lines

from sqlalchemy import text  # noqa: E402
from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import StaticPool  # noqa: E402

from datetime import datetime, timedelta, timezone  # noqa: E402

from app.db.base import Base  # noqa: E402
from app.db import models  # noqa: E402,F401
from app.db.models.ws_ticket import WsTicket  # noqa: E402
from app.repositories.audit_repository import AuditRepository  # noqa: E402


def make_engine(path: str):
    return create_async_engine(
        f"sqlite+aiosqlite:///{path}",
        echo=False,
        future=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )


class PausedFlush:
    """Wraps the session flush so the interleaving window sits exactly where
    the production race lives: AFTER the audit INSERT has emitted the
    SAVEPOINT + row (the point of no silent release) and BEFORE the nested
    commit emits RELEASE SAVEPOINT. The other session's commit/rollback in
    that window orphans the savepoint."""

    def __init__(self, real_flush, emitted: asyncio.Event, release: asyncio.Event):
        self._real = real_flush
        self._emitted = emitted
        self._release = release

    async def __call__(self, *args, **kwargs):
        result = await self._real(*args, **kwargs)
        self._emitted.set()
        await self._release.wait()
        return result


async def scenario(name: str, *, b_action: str, b_timing: str) -> None:
    engine = make_engine(f"/tmp/b_audit_{name}.db")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(bind=engine, class_=AsyncSession,
                                 expire_on_commit=False, autoflush=False)

    sb = factory()  # session B: the "other request" owning the shared connection
    sa = factory()  # session A: the audited request
    # DML, not SELECT: sqlite3 only starts a transaction on the first write.
    sb.add(WsTicket(ticket=f"b-{name}", operator_id="op-b",
                    expires_at=datetime.now(timezone.utc) + timedelta(minutes=1)))
    await sb.flush()  # B's root transaction is now REAL on the connection
    sa.add(WsTicket(ticket=f"a-{name}", operator_id="op-a",
                    expires_at=datetime.now(timezone.utc) + timedelta(minutes=1)))
    await sa.flush()  # A rides a dialect savepoint on B's transaction

    repo = AuditRepository(sa)
    result = None

    if b_timing == "before_append":
        if b_action == "commit":
            await sb.commit()
        else:
            await sb.rollback()
        result = await repo.append(
            category="SECURITY", action="auth.ws_ticket_issued",
            message="repro before-append", actor="admin",
        )
    else:
        real_flush = sa.flush
        emitted = asyncio.Event()
        release = asyncio.Event()
        sa.flush = PausedFlush(real_flush, emitted, release)  # type: ignore[method-assign]

        async def do_append():
            nonlocal result
            result = await repo.append(
                category="SECURITY", action="auth.ws_ticket_issued",
                message="repro mid-append", actor="admin",
            )

        task = asyncio.create_task(do_append())
        await asyncio.wait_for(emitted.wait(), timeout=5)
        if b_action == "commit":
            await sb.commit()
        else:
            await sb.rollback()
        release.set()
        await asyncio.wait_for(task, timeout=10)

    try:
        await asyncio.wait_for(sa.commit(), timeout=5)
    except Exception as exc:  # noqa: BLE001
        print(f"[{name}] sa.commit after append -> {type(exc).__name__}: {exc}")
        await sa.rollback()

    sc = factory()
    try:
        rows = (await sc.execute(
            text("SELECT COUNT(*) FROM audit_events"))).scalar_one()
    finally:
        await sc.close()
    print(f"[{name}] b={b_action}/{b_timing} -> append={result} audit_rows={rows}")

    await sa.close()
    await sb.close()
    await engine.dispose()


async def main() -> None:
    await scenario("c_before", b_action="commit", b_timing="before_append")
    await scenario("r_before", b_action="rollback", b_timing="before_append")
    await scenario("c_mid", b_action="commit", b_timing="mid_append")
    await scenario("r_mid", b_action="rollback", b_timing="mid_append")


if __name__ == "__main__":
    asyncio.run(main())
