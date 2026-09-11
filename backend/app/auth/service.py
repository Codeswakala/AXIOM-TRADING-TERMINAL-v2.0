"""Authentication application service — refresh rotation + WS tickets (W0-U08)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import (
    create_token,
    hash_password,
    hash_token,
    new_jti,
    new_ws_ticket_value,
    safe_decode,
    verify_password,
)
from app.core.config import DEFAULT_BOOTSTRAP_PASSWORD, Settings
from app.core.logging import get_logger
from app.db.models.operator import Operator
from app.db.models.refresh_token import RefreshTokenRecord
from app.db.models.ws_ticket import WsTicket
from app.repositories.audit_repository import AuditRepository
from app.repositories.operator_repository import OperatorRepository

logger = get_logger(__name__, category="SECURITY")


class AuthError(Exception):
    def __init__(self, message: str, *, code: str = "auth_error") -> None:
        super().__init__(message)
        self.message = message
        self.code = code


@dataclass(slots=True)
class TokenPair:
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 0


class AuthService:
    def __init__(self, session: AsyncSession, settings: Settings) -> None:
        self._session = session
        self._settings = settings
        self._operators = OperatorRepository(session)
        self._audit = AuditRepository(session)

    async def ensure_bootstrap_admin(self) -> Operator | None:
        """Create bootstrap admin only when explicitly enabled with non-default credentials."""
        if not self._settings.bootstrap_admin_enabled:
            return None
        username = (self._settings.bootstrap_admin_username or "").strip().lower()
        password = self._settings.bootstrap_admin_password or ""
        if not username or not password:
            logger.warning("Bootstrap admin enabled but username/password not set — skipping")
            return None
        if password == DEFAULT_BOOTSTRAP_PASSWORD and not self._settings.allow_insecure_dev:
            raise RuntimeError(
                "Bootstrap password must not be the historical default admin123. "
                "Set AXIOM_BOOTSTRAP_ADMIN_PASSWORD to a strong value, or "
                "AXIOM_ALLOW_INSECURE_DEV=true for local-only demos."
            )
        if len(password) < 8:
            raise RuntimeError("AXIOM_BOOTSTRAP_ADMIN_PASSWORD must be at least 8 characters.")

        count = await self._operators.count_operators()
        if count > 0:
            return None

        operator = Operator(
            username=username,
            hashed_password=hash_password(password),
            role="admin",
            display_name="Bootstrap Admin",
            is_active=True,
        )
        created = await self._operators.add(operator)
        await self._audit.append(
            category="SECURITY",
            action="auth.bootstrap_admin",
            message=f"Bootstrap admin created: {username}",
            actor="system",
            resource_type="operator",
            resource_id=created.id,
        )
        logger.info("Bootstrap admin created username=%s", username)
        return created

    async def authenticate(self, username: str, password: str) -> tuple[Operator, TokenPair]:
        operator = await self._operators.get_by_username(username.strip().lower())
        if operator is None or not operator.is_active:
            await self._audit.append(
                category="SECURITY",
                action="auth.login_failed",
                message=f"Login failed for username={username}",
                actor=username,
            )
            raise AuthError("Invalid username or password", code="invalid_credentials")
        if not verify_password(password, operator.hashed_password):
            await self._audit.append(
                category="SECURITY",
                action="auth.login_failed",
                message=f"Bad password for username={username}",
                actor=username,
                resource_type="operator",
                resource_id=operator.id,
            )
            raise AuthError("Invalid username or password", code="invalid_credentials")

        operator.last_login_at = datetime.now(timezone.utc)
        await self._session.flush()
        tokens = await self._issue_tokens(operator)
        await self._audit.append(
            category="SECURITY",
            action="auth.login_success",
            message=f"Operator logged in: {operator.username}",
            actor=operator.username,
            resource_type="operator",
            resource_id=operator.id,
        )
        logger.info("Login success username=%s", operator.username)
        return operator, tokens

    async def _issue_tokens(self, operator: Operator) -> TokenPair:
        claims = {"role": operator.role, "username": operator.username}
        access = create_token(
            subject=operator.id,
            token_type="access",
            settings=self._settings,
            extra_claims=claims,
        )
        jti = new_jti()
        refresh = create_token(
            subject=operator.id,
            token_type="refresh",
            settings=self._settings,
            extra_claims=claims,
            jti=jti,
        )
        expires = datetime.now(timezone.utc) + timedelta(
            days=self._settings.refresh_token_expire_days
        )
        record = RefreshTokenRecord(
            jti=jti,
            operator_id=operator.id,
            token_hash=hash_token(refresh),
            expires_at=expires,
            revoked=False,
        )
        self._session.add(record)
        await self._session.flush()
        return TokenPair(
            access_token=access,
            refresh_token=refresh,
            expires_in=self._settings.access_token_expire_minutes * 60,
        )

    async def refresh(self, refresh_token: str) -> TokenPair:
        payload = safe_decode(refresh_token, self._settings)
        if payload is None or payload.get("type") != "refresh":
            raise AuthError("Invalid refresh token", code="invalid_refresh")
        jti = payload.get("jti")
        operator_id = payload.get("sub")
        if not jti or not operator_id:
            raise AuthError("Invalid refresh token", code="invalid_refresh")

        result = await self._session.execute(
            select(RefreshTokenRecord).where(RefreshTokenRecord.jti == jti)
        )
        record = result.scalar_one_or_none()
        if record is None:
            raise AuthError("Refresh token not recognized", code="invalid_refresh")

        # Reuse detection: revoked token presented again
        if record.revoked:
            await self._revoke_all_for_operator(str(operator_id))
            await self._audit.append(
                category="SECURITY",
                action="auth.refresh_reuse_detected",
                message=f"Refresh reuse for operator={operator_id}; family revoked",
                actor=str(operator_id),
                resource_type="operator",
                resource_id=str(operator_id),
            )
            raise AuthError("Refresh token reuse detected", code="refresh_reuse")

        now = datetime.now(timezone.utc)
        exp = record.expires_at
        if exp.tzinfo is None:
            exp = exp.replace(tzinfo=timezone.utc)
        if exp < now:
            record.revoked = True
            record.revoked_at = now
            await self._session.flush()
            raise AuthError("Refresh token expired", code="refresh_expired")

        if record.token_hash != hash_token(refresh_token):
            raise AuthError("Invalid refresh token", code="invalid_refresh")

        operator = await self._operators.get_by_id(str(operator_id))
        if operator is None or not operator.is_active:
            raise AuthError("Operator not found or inactive", code="operator_inactive")

        # Rotate: revoke old, issue new
        new_tokens = await self._issue_tokens(operator)
        new_payload = safe_decode(new_tokens.refresh_token, self._settings) or {}
        new_jti_val = new_payload.get("jti")
        record.revoked = True
        record.revoked_at = datetime.now(timezone.utc)
        record.replaced_by_jti = new_jti_val
        await self._session.flush()

        await self._audit.append(
            category="SECURITY",
            action="auth.token_refresh",
            message=f"Token rotated for {operator.username}",
            actor=operator.username,
            resource_type="operator",
            resource_id=operator.id,
        )
        return new_tokens

    async def _revoke_all_for_operator(self, operator_id: str) -> None:
        result = await self._session.execute(
            select(RefreshTokenRecord).where(
                RefreshTokenRecord.operator_id == operator_id,
                RefreshTokenRecord.revoked.is_(False),
            )
        )
        now = datetime.now(timezone.utc)
        for rec in result.scalars().all():
            rec.revoked = True
            rec.revoked_at = now
        await self._session.flush()

    async def logout(self, operator: Operator, refresh_token: str | None = None) -> None:
        if refresh_token:
            payload = safe_decode(refresh_token, self._settings)
            jti = (payload or {}).get("jti")
            if jti:
                result = await self._session.execute(
                    select(RefreshTokenRecord).where(RefreshTokenRecord.jti == jti)
                )
                rec = result.scalar_one_or_none()
                if rec and not rec.revoked:
                    rec.revoked = True
                    rec.revoked_at = datetime.now(timezone.utc)
                    await self._session.flush()
        await self._revoke_all_for_operator(operator.id)
        await self._audit.append(
            category="SECURITY",
            action="auth.logout",
            message=f"Operator logged out: {operator.username}",
            actor=operator.username,
            resource_type="operator",
            resource_id=operator.id,
        )
        logger.info("Logout username=%s", operator.username)

    async def get_operator_by_id(self, operator_id: str) -> Operator | None:
        return await self._operators.get_by_id(operator_id)

    async def issue_ws_ticket(self, operator: Operator) -> tuple[str, int]:
        """Issue short-lived one-time WS ticket (not a long-lived JWT).

        Ticket insert is authoritative; audit is best-effort and must not 500.
        """
        ticket = new_ws_ticket_value()
        ttl = self._settings.ws_ticket_expire_seconds
        expires = datetime.now(timezone.utc) + timedelta(seconds=ttl)
        row = WsTicket(
            ticket=ticket,
            operator_id=operator.id,
            expires_at=expires,
            used=False,
        )
        self._session.add(row)
        await self._session.flush()
        # Best-effort audit (savepoint-isolated; never fails this method)
        await self._audit.append(
            category="SECURITY",
            action="auth.ws_ticket_issued",
            message=f"WS ticket issued for {operator.username}",
            actor=operator.username,
            resource_type="operator",
            resource_id=operator.id,
        )
        return ticket, ttl

    async def consume_ws_ticket(self, ticket: str) -> Operator | None:
        result = await self._session.execute(
            select(WsTicket).where(WsTicket.ticket == ticket)
        )
        row = result.scalar_one_or_none()
        if row is None or row.used:
            return None
        now = datetime.now(timezone.utc)
        exp = row.expires_at
        if exp.tzinfo is None:
            exp = exp.replace(tzinfo=timezone.utc)
        if exp < now:
            return None
        row.used = True
        await self._session.flush()
        return await self._operators.get_by_id(row.operator_id)
