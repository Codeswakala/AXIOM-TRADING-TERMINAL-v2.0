"""BO-B-AUDIT — audit integrity under concurrency (2026-08-21).

Pins the B-AUDIT durability contract on the fixed `AuditRepository`:

  1. Deterministic reproduction of the production failure class (two
     sessions on the shared StaticPool connection; the concurrent session's
     rollback lands between the audit INSERT and the savepoint RELEASE) —
     post-fix, the audit row must land or a durable failure marker must
     exist, and append must never raise.
  2. The silent merged-transaction loss mode (concurrent rollback between
     flush and commit, commit "succeeds" as a no-op) is detected by the
     read-back verification → retry lands the row.
  3. A persistent failure produces a durable, queryable failure marker.
  4. The endpoint-safety invariant: audit failure never 500s the endpoint.

The pre-fix behaviour (evidenced in the prefix run + the BO-B-AUDIT.1 repro
log) was: `sqlite3.OperationalError: no such savepoint: sa_savepoint_1`
swallowed by append → `None` returned → audit row silently lost.
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.db import models  # noqa: F401
from app.db.base import Base
from app.db.models.ws_ticket import WsTicket
from app.repositories.audit_repository import AuditRepository

pytestmark = pytest.mark.asyncio


def make_file_engine(path: str):
    """The dev configuration: file SQLite + StaticPool (one shared connection),
    no serialization — the environment that produced the production error."""
    return create_async_engine(
        f"sqlite+aiosqlite:///{path}",
        echo=False,
        future=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )


class PausedFlush:
    """Wraps a session's flush so the interleaving window sits exactly where
    the production race lives: AFTER the audit INSERT has been executed and
    BEFORE the commit. The other session's rollback in that window orphans
    the savepoint (pre-fix) or silently undoes the merged-transaction INSERT
    (post-fix verification target)."""

    def __init__(self, real_flush, emitted: asyncio.Event, release: asyncio.Event):
        self._real = real_flush
        self._emitted = emitted
        self._release = release

    async def __call__(self, *args, **kwargs):
        result = await self._real(*args, **kwargs)
        self._emitted.set()
        await self._release.wait()
        return result


async def test_b_audit_concurrent_rollback_never_loses_row_or_is_silent(tmp_path):
    """The deterministic repro scenario (BO-B-AUDIT.1/.4).

    Two sessions share the StaticPool connection. Session B holds a real
    write transaction; the audit write (via the repository's dedicated
    writer session) is paused after its INSERT; B rolls the shared
    transaction back in that window; then the append completes.

    Contract: append returns the event (row landed, verified) OR the loss is
    recorded as a durable failure marker — never silent, never raised.
    """
    engine = make_file_engine(str(tmp_path / "b_audit_race.db"))
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
    )

    sb = factory()  # the concurrent request holding the shared transaction
    sb.add(
        WsTicket(
            ticket="concurrent-b",
            operator_id="op-b",
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=1),
        )
    )
    await sb.flush()  # REAL transaction on the shared connection (DML)

    emitted = asyncio.Event()
    release = asyncio.Event()
    first_attempt = {"done": False}

    def factory_wrapper():
        """Seam contract: return a callable that produces a writer session.
        The FIRST attempt's session gets the paused flush so the hostile
        rollback lands inside the vulnerable window."""
        if not first_attempt["done"]:
            first_attempt["done"] = True

            def paused_session_factory():
                session = factory()
                session.flush = PausedFlush(session.flush, emitted, release)  # type: ignore[method-assign]
                return session

            return paused_session_factory
        return factory

    business_session = factory()
    repo = AuditRepository(business_session, session_factory=factory_wrapper)

    async def do_append():
        return await repo.append(
            category="SECURITY",
            action="auth.ws_ticket_issued",
            message="B-AUDIT deterministic repro",
            actor="admin",
            correlation_id="b-audit-repro",
        )

    task = asyncio.create_task(do_append())
    await asyncio.wait_for(emitted.wait(), timeout=10)
    # The audit INSERT is on the shared connection; the concurrent request
    # rolls back NOW (production interleaving).
    await sb.rollback()
    release.set()
    result = await asyncio.wait_for(task, timeout=15)

    # Contract: append never raised; row landed OR durable marker exists.
    reader = factory()
    try:
        rows = (
            await reader.execute(
                text("SELECT COUNT(*) FROM audit_events WHERE action = 'auth.ws_ticket_issued'")
            )
        ).scalar_one()
        markers = (
            await reader.execute(
                text(
                    "SELECT COUNT(*) FROM audit_write_failure_records "
                    "WHERE action = 'auth.ws_ticket_issued'"
                )
            )
        ).scalar_one()
    finally:
        await reader.close()
    assert rows + markers >= 1, (
        f"audit loss must never be silent: rows={rows} markers={markers}"
    )
    if result is not None:
        assert rows >= 1
    else:
        assert markers >= 1

    await business_session.close()
    await sb.close()
    await engine.dispose()


async def test_b_audit_append_retries_then_lands(tmp_path):
    """BO-B-AUDIT.3 (a): first writer attempt fails with the orphaned-
    savepoint error; the retry lands the row."""
    engine = make_file_engine(str(tmp_path / "b_audit_retry.db"))
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
    )

    attempts = {"n": 0}

    def failing_once_factory():
        sm = async_sessionmaker(
            bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
        )

        class FailingSession(sm.class_):  # type: ignore[misc]
            async def flush(self, *args, **kwargs):
                attempts["n"] += 1
                if attempts["n"] == 1:
                    from sqlalchemy.exc import OperationalError

                    raise OperationalError(
                        "SELECT 1", {}, Exception("no such savepoint: sa_savepoint_1")
                    )
                return await super().flush(*args, **kwargs)

        failing = async_sessionmaker(
            bind=engine,
            class_=FailingSession,
            expire_on_commit=False,
            autoflush=False,
        )
        return failing

    session = factory()
    repo = AuditRepository(session, session_factory=failing_once_factory)
    result = await repo.append(
        category="SECURITY", action="retry.probe", message="retry test", actor="admin"
    )
    assert result is not None
    assert attempts["n"] == 2
    reader = factory()
    try:
        count = (
            await reader.execute(
                text("SELECT COUNT(*) FROM audit_events WHERE action = 'retry.probe'")
            )
        ).scalar_one()
    finally:
        await reader.close()
    assert count == 1
    await session.close()
    await engine.dispose()


async def test_b_audit_persistent_failure_writes_durable_marker(tmp_path):
    """BO-B-AUDIT.3 (c): both audit-event attempts fail → a durable, queryable
    failure marker row is persisted (the marker writer itself succeeds);
    append returns None; nothing raises."""
    engine = make_file_engine(str(tmp_path / "b_audit_marker.db"))
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
    )

    flushes = {"n": 0}

    class FailingFirstTwo(factory.class_):  # type: ignore[misc]
        async def flush(self, *args, **kwargs):
            flushes["n"] += 1
            if flushes["n"] <= 2:
                from sqlalchemy.exc import OperationalError

                raise OperationalError(
                    "SELECT 1", {}, Exception("no such savepoint: sa_savepoint_1")
                )
            return await super().flush(*args, **kwargs)

    def failing_factory():
        return async_sessionmaker(
            bind=engine,
            class_=FailingFirstTwo,
            expire_on_commit=False,
            autoflush=False,
        )

    session = factory()
    repo = AuditRepository(session, session_factory=failing_factory)
    result = await repo.append(
        category="SECURITY",
        action="marker.probe",
        message="persistent failure test",
        actor="admin",
        resource_type="operator",
        resource_id="op-1",
        correlation_id="marker-correlation",
    )
    assert result is None  # endpoint-safe: no raise, no event

    reader = factory()
    try:
        audit_rows = (
            await reader.execute(
                text("SELECT COUNT(*) FROM audit_events WHERE action = 'marker.probe'")
            )
        ).scalar_one()
        markers = (
            await reader.execute(text("SELECT * FROM audit_write_failure_records"))
        ).fetchall()
    finally:
        await reader.close()

    assert audit_rows == 0  # nothing fabricated
    assert len(markers) == 1
    marker = markers[0]._mapping
    assert marker["category"] == "SECURITY"
    assert marker["action"] == "marker.probe"
    assert marker["actor"] == "admin"
    assert marker["resource_type"] == "operator"
    assert marker["resource_id"] == "op-1"
    assert marker["correlation_id"] == "marker-correlation"
    assert "OperationalError" in marker["failure_reason"]
    assert marker["attempts"] == 2
    assert flushes["n"] >= 3  # 2 failed audit flushes + at least 1 marker flush
    await session.close()
    await engine.dispose()


def test_b_audit_append_failure_never_500s_endpoint(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """BO-B-AUDIT.4 regression: a HARD audit-storage failure (every writer
    attempt AND the marker writer failing) must never 500 the business
    endpoint — append's internal catch converts it to a logged loss."""

    async def write_fails(self, event):  # noqa: ANN001, ARG001
        raise RuntimeError("audit storage unavailable")

    async def marker_fails(self, event, error):  # noqa: ANN001, ARG001
        raise RuntimeError("audit marker storage unavailable")

    monkeypatch.setattr(AuditRepository, "_write_and_verify", write_fails)
    monkeypatch.setattr(AuditRepository, "_record_failure_marker", marker_fails)

    login = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert login.status_code == 200, login.text
    access = login.json()["tokens"]["access_token"]
    resp = client.post(
        "/api/v1/auth/ws-ticket",
        headers={"Authorization": f"Bearer {access}"},
    )
    assert resp.status_code == 200, (
        f"audit failure must never 500 the endpoint; got {resp.status_code}"
    )
    assert resp.json().get("ticket")


async def test_b_audit_failure_marker_model_registered_in_metadata() -> None:
    """The marker table is part of the schema metadata (queryable store)."""
    assert "audit_write_failure_records" in Base.metadata.tables
    table = Base.metadata.tables["audit_write_failure_records"]
    expected_columns = {
        "id",
        "category",
        "action",
        "message",
        "actor",
        "resource_type",
        "resource_id",
        "correlation_id",
        "details",
        "failure_reason",
        "attempts",
        "created_at",
    }
    assert expected_columns <= set(table.columns.keys())
    assert set(table.primary_key.columns.keys()) == {"id"}


async def test_b_audit_decoupled_writer_survives_business_rollback(tmp_path):
    """BO-B-AUDIT semantic consequence (pinned as intended): the audit row is
    written through its own short-lived session, so a business-transaction
    rollback no longer discards it (the pre-fix design lost audit rows on
    business rollback too)."""
    engine = make_file_engine(str(tmp_path / "b_audit_decoupled.db"))
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
    )

    business = factory()
    business.add(
        WsTicket(
            ticket="rollback-b",
            operator_id="op-b",
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=1),
        )
    )
    await business.flush()
    repo = AuditRepository(business, session_factory=lambda: factory)
    result = await repo.append(
        category="SECURITY", action="decouple.probe", message="decoupled test",
        actor="admin",
    )
    assert result is not None
    await business.rollback()  # the business operation fails

    reader = factory()
    try:
        count = (
            await reader.execute(
                text("SELECT COUNT(*) FROM audit_events WHERE action = 'decouple.probe'")
            )
        ).scalar_one()
    finally:
        await reader.close()
    assert count == 1  # the observed activity remains traceable
    await business.close()
    await engine.dispose()
