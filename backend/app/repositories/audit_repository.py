"""Audit event repository — append-oriented; never crashes callers (W0-U08.1).

BO-B-AUDIT (2026-08-21) — eliminate silent audit loss under concurrency.

Root cause (evidenced in `tests/test_b_audit_concurrency.py` + the BO-B-AUDIT.1
repro): all SQLite configurations use StaticPool (ONE shared DBAPI connection),
and pysqlite's legacy transaction control silently suppresses a second
session's BEGIN — so concurrent sessions' transactions MERGE on the one
connection. The pre-fix append wrote inside `begin_nested()` on the business
session: a concurrent session's COMMIT/ROLLBACK landing between the audit
INSERT and the savepoint RELEASE orphaned the savepoint
(`no such savepoint: sa_savepoint_1`), the exception was swallowed, and the
row was lost silently — while the endpoint kept returning 200.

Fix mechanism (BO-B-AUDIT.3): the audit writer is DECOUPLED from the business
transaction (short-lived dedicated session per attempt), every write is
verified by a same-connection read-back after commit (detects the merged-
transaction loss mode too, where the commit "succeeds" as a no-op), one retry
is attempted, and a persistent failure is recorded as a durable
`AuditWriteFailureRecord` marker — queryable, never silent. The endpoint-safety
invariant is unchanged: append never raises into the business endpoint.

Consequence disclosed: audit rows now commit independently of the business
transaction. An audit row may persist for a business operation that later
rolls back — acceptable for an accountability trail (§5.7: record observed
activity), and it removes the pre-existing inverse loss (business rollback
silently discarding the audit row).
"""

from __future__ import annotations

from typing import Any, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.db.models.audit import AuditEvent, AuditWriteFailureRecord
from app.db.session import get_session_factory
from app.repositories.base import BaseRepository

logger = get_logger(__name__, category="AUDIT")

MAX_AUDIT_APPEND_ATTEMPTS = 2
MAX_MARKER_ATTEMPTS = 2


class AuditRepository(BaseRepository[AuditEvent]):
    model = AuditEvent

    def __init__(
        self,
        session: AsyncSession,
        session_factory: Any | None = None,
    ) -> None:
        """`session_factory` is the BO-B-AUDIT test seam: a zero-arg callable
        returning the sessionmaker used for the dedicated audit/marker
        sessions. Defaults to the application factory."""
        super().__init__(session)
        self._audit_session_factory = session_factory or get_session_factory

    async def append(
        self,
        *,
        category: str,
        action: str,
        message: str,
        actor: str = "system",
        resource_type: str | None = None,
        resource_id: str | None = None,
        details: dict[str, Any] | None = None,
        correlation_id: str | None = None,
    ) -> AuditEvent | None:
        """Append an audit event without endangering the business transaction.

        BO-B-AUDIT durability contract:
          1. the event is written through a short-lived dedicated session
             (decoupled from the business transaction),
          2. the write is verified by same-connection read-back after commit
             (catches the merged-transaction loss mode as well as savepoint
             orphaning),
          3. one retry is attempted on any failure or failed verification,
          4. a persistent failure is recorded as a durable
             `AuditWriteFailureRecord` marker (never silent),
          5. append NEVER raises into the business endpoint.
        """
        event = AuditEvent(
            category=category,
            action=action,
            message=message,
            actor=actor,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            correlation_id=correlation_id,
        )
        last_error: Exception | None = None
        for _ in range(MAX_AUDIT_APPEND_ATTEMPTS):
            try:
                landed = await self._write_and_verify(event)
            except Exception as exc:  # noqa: BLE001 — never propagate audit failure
                last_error = exc
                landed = False
            if landed:
                return event

        try:
            await self._record_failure_marker(event, last_error)
        except Exception as marker_exc:  # noqa: BLE001 — the marker path must
            # never endanger the endpoint either (defense-in-depth).
            logger.error("audit failure marker path raised err=%s", marker_exc)
        logger.exception(
            "audit append failed after %d attempts category=%s action=%s err=%s",
            MAX_AUDIT_APPEND_ATTEMPTS,
            category,
            action,
            last_error,
        )
        return None

    async def _write_and_verify(self, event: AuditEvent) -> bool:
        """Write + commit + same-connection read-back verification.

        NOTE: the writer intentionally does NOT take the W3-U08.1
        sqlite_staticpool_serialization lock — under `:memory:` StaticPool
        test harnesses the business session holds that (non-reentrant) lock
        for the whole endpoint; taking it here would deadlock. The read-back
        verification below is the durability guarantee instead.
        """
        factory = self._audit_session_factory()
        session = factory()
        try:
            session.add(event)
            await session.flush()
            await session.commit()
            # Post-commit verification on the SAME connection (a fresh
            # transaction): the row must be visible. Detects the merged-
            # transaction loss mode where a concurrent rollback removed
            # the row while the commit itself "succeeded".
            result = await session.execute(
                select(AuditEvent.id).where(AuditEvent.id == event.id)
            )
            return result.scalar_one_or_none() is not None
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def _record_failure_marker(
        self,
        event: AuditEvent,
        error: Exception | None,
    ) -> None:
        """Persist the durable failure marker (itself verified). If the marker
        cannot land either, the structured logger.exception in append() is the
        final surfacing — the loss is never silent."""
        marker = AuditWriteFailureRecord(
            category=event.category,
            action=event.action,
            message=event.message,
            actor=event.actor,
            resource_type=event.resource_type,
            resource_id=event.resource_id,
            correlation_id=event.correlation_id,
            details=event.details,
            failure_reason=f"{type(error).__name__}: {error}"[:2000],
            attempts=MAX_AUDIT_APPEND_ATTEMPTS,
        )
        for _ in range(MAX_MARKER_ATTEMPTS):
            try:
                landed = await self._write_and_verify_marker(marker)
            except Exception as exc:  # noqa: BLE001
                logger.error("audit failure marker write failed err=%s", exc)
                landed = False
            if landed:
                logger.error(
                    "audit append failed — durable failure marker persisted "
                    "marker_id=%s category=%s action=%s",
                    marker.id,
                    marker.category,
                    marker.action,
                )
                return
        logger.error(
            "audit append failed AND failure marker could not persist "
            "category=%s action=%s — structured log is the final record",
            marker.category,
            marker.action,
        )

    async def _write_and_verify_marker(self, marker: AuditWriteFailureRecord) -> bool:
        factory = self._audit_session_factory()
        session = factory()
        try:
            session.add(marker)
            await session.flush()
            await session.commit()
            result = await session.execute(
                select(AuditWriteFailureRecord.id).where(
                    AuditWriteFailureRecord.id == marker.id
                )
            )
            return result.scalar_one_or_none() is not None
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def list_recent(
        self,
        *,
        category: str | None = None,
        limit: int = 50,
    ) -> Sequence[AuditEvent]:
        stmt = select(AuditEvent)
        if category is not None:
            stmt = stmt.where(AuditEvent.category == category)
        stmt = stmt.order_by(AuditEvent.created_at.desc()).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()
