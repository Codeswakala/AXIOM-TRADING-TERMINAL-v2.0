"""Authentication endpoints (W0-U08: rotation + WS tickets)."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.auth.dependencies import AuthServiceDep, CurrentOperatorDep
from app.auth.service import AuthError
from app.models.auth import (
    LoginRequest,
    LoginResponse,
    OperatorRead,
    RefreshRequest,
    TokenResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])


class LogoutRequest(BaseModel):
    refresh_token: str | None = None


class WsTicketResponse(BaseModel):
    ticket: str
    expires_in: int
    websocket_path: str = "/ws/market"
    usage: str = Field(
        default="Connect to /ws/market?ticket=<ticket> (short-lived, one-time). "
        "Do not put access JWT in the query string.",
    )


@router.post("/login", response_model=LoginResponse, summary="Operator login")
async def login(payload: LoginRequest, auth: AuthServiceDep) -> LoginResponse:
    try:
        operator, tokens = await auth.authenticate(payload.username, payload.password)
    except AuthError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=exc.message) from exc
    return LoginResponse(
        tokens=TokenResponse(
            access_token=tokens.access_token,
            refresh_token=tokens.refresh_token,
            token_type=tokens.token_type,
            expires_in=tokens.expires_in,
        ),
        operator=OperatorRead.model_validate(operator),
    )


@router.post("/refresh", response_model=TokenResponse, summary="Rotate refresh + access tokens")
async def refresh(payload: RefreshRequest, auth: AuthServiceDep) -> TokenResponse:
    try:
        tokens = await auth.refresh(payload.refresh_token)
    except AuthError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=exc.message) from exc
    return TokenResponse(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
        token_type=tokens.token_type,
        expires_in=tokens.expires_in,
    )


@router.post("/logout", summary="Logout and revoke refresh tokens")
async def logout(
    operator: CurrentOperatorDep,
    auth: AuthServiceDep,
    payload: LogoutRequest | None = None,
) -> dict[str, str]:
    refresh = payload.refresh_token if payload else None
    await auth.logout(operator, refresh_token=refresh)
    return {"status": "logged_out", "username": operator.username}


@router.post(
    "/ws-ticket",
    response_model=WsTicketResponse,
    summary="Issue short-lived one-time WebSocket ticket",
)
async def ws_ticket(operator: CurrentOperatorDep, auth: AuthServiceDep) -> WsTicketResponse:
    ticket, ttl = await auth.issue_ws_ticket(operator)
    return WsTicketResponse(ticket=ticket, expires_in=ttl)
