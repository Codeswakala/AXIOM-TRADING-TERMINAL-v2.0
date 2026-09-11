"""FastAPI auth dependencies."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import safe_decode
from app.auth.service import AuthService
from app.core.config import Settings, get_settings
from app.db.models.operator import Operator
from app.db.session import get_db_session

bearer_scheme = HTTPBearer(auto_error=False)

SettingsDep = Annotated[Settings, Depends(get_settings)]
SessionDep = Annotated[AsyncSession, Depends(get_db_session)]


async def get_auth_service(session: SessionDep, settings: SettingsDep) -> AuthService:
    return AuthService(session, settings)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


async def get_current_operator(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    settings: SettingsDep,
    auth: AuthServiceDep,
) -> Operator:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = safe_decode(credentials.credentials, settings)
    if payload is None or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    operator_id = payload.get("sub")
    if not operator_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token subject",
        )
    operator = await auth.get_operator_by_id(str(operator_id))
    if operator is None or not operator.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Operator inactive")
    return operator


CurrentOperatorDep = Annotated[Operator, Depends(get_current_operator)]


def require_role(*roles: str):
    async def _checker(operator: CurrentOperatorDep) -> Operator:
        if operator.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires role in {roles}",
            )
        return operator

    return _checker
