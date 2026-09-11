"""V2 Audit Repository — append-only audit event persistence.

Append-only: no update() or delete() methods exist.
DB triggers enforce immutability at the database level.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.v2_audit_event import V2AuditEvent
from app.v2.audit.contract import STORABLE_CLASSIFICATIONS, V2AuditEventCreate
from app.v2.audit.redaction import has_sensitive_content, redact
from app.v2.errors.contract import AuditWriteRejectedError
from app.v2.identifiers import new_id
from app.v2.temporal.validation import utc_now


def _contains_unredactable_secret(value: object) -> bool:
    """True when the payload carries secret material redaction cannot remove.

    ``redact()`` rewrites string *values*, so pattern-detectable secrets in
    values are removable by construction. What it cannot rewrite are dict
    *keys*: secret-bearing key strings would persist verbatim in storage.
    Such payloads are refused per R-9.4 (reject rather than store).
    """
    if isinstance(value, dict):
        for key, nested in value.items():
            if isinstance(key, str) and has_sensitive_content(key):
                return True
            if _contains_unredactable_secret(nested):
                return True
        return False
    if isinstance(value, (list, tuple)):
        return any(_contains_unredactable_secret(v) for v in value)
    return False


class V2AuditRepository:
    """Append-only V2 audit event repository."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def append(self, event: V2AuditEventCreate) -> V2AuditEvent:
        """Append a new audit event.

        Write-time policy (ITRGA-ACC-V2-BE-1-INTAKE-001 §2 R-9.4):
        - classification must be public/internal/confidential; ``secret``
          (or unknown vocabulary) is refused with a safe generic error;
        - details are redacted before storage; if detectable secret
          material survives redaction the write is refused. The refusal
          never echoes the offending value.
        """
        if event.classification not in STORABLE_CLASSIFICATIONS:
            from app.core.logging import get_logger

            get_logger(__name__, category="SECURITY").warning(
                "V2 audit write rejected: unsupported classification=%s domain=%s action=%s",
                event.classification, event.domain, event.action,
            )
            raise AuditWriteRejectedError()

        # Redact sensitive fields
        redacted_details = redact(event.details) if event.details else None
        if redacted_details is not None and _contains_unredactable_secret(redacted_details):
            from app.core.logging import get_logger

            get_logger(__name__, category="SECURITY").warning(
                "V2 audit write rejected: unredactable secret material domain=%s action=%s",
                event.domain, event.action,
            )
            raise AuditWriteRejectedError()

        record = V2AuditEvent(
            id=new_id(),
            correlation_id=event.correlation_id or new_id(),
            causation_id=event.causation_id,
            actor_id=event.actor_id,
            actor_type=event.actor_type,
            domain=event.domain,
            action=event.action,
            resource_type=event.resource_type,
            resource_id=event.resource_id,
            mode=event.mode,
            details=redacted_details,
            classification=event.classification,
            operator_id=event.operator_id,
            created_at=utc_now(),
        )
        self._session.add(record)
        await self._session.flush()
        return record

    async def read_by_operator(
        self,
        operator_id: str,
        *,
        domain: str | None = None,
        limit: int = 50,
    ) -> list[V2AuditEvent]:
        """Read audit events for a specific operator (operator-scoped)."""
        stmt = (
            select(V2AuditEvent)
            .where(V2AuditEvent.operator_id == operator_id)
            .order_by(V2AuditEvent.created_at.desc())
            .limit(limit)
        )
        if domain:
            stmt = stmt.where(V2AuditEvent.domain == domain)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def read_all(
        self,
        *,
        domain: str | None = None,
        limit: int = 50,
    ) -> list[V2AuditEvent]:
        """Read all audit events (admin-only, SAL-4)."""
        stmt = (
            select(V2AuditEvent)
            .order_by(V2AuditEvent.created_at.desc())
            .limit(limit)
        )
        if domain:
            stmt = stmt.where(V2AuditEvent.domain == domain)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def read_by_correlation(
        self,
        correlation_id: str,
    ) -> list[V2AuditEvent]:
        """Read all audit events for a correlation ID."""
        stmt = (
            select(V2AuditEvent)
            .where(V2AuditEvent.correlation_id == correlation_id)
            .order_by(V2AuditEvent.created_at.asc())
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
