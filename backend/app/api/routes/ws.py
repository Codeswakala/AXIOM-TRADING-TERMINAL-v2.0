"""WebSocket endpoints — ticket-based auth (W1-U01 hardened)."""

from __future__ import annotations

from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect

from app.auth.security import safe_decode
from app.auth.service import AuthService
from app.core.config import get_settings
from app.core.logging import get_logger
from app.db.session import get_session_factory
from app.market.hub import live_market_hub
from app.market.live_service import get_live_market_service
from app.services.observability_service import (
    new_correlation_id,
    reset_correlation_id,
    set_correlation_id,
)

router = APIRouter(tags=["websocket"])
logger = get_logger(__name__, category="API")


async def _authenticate_ws(
    websocket: WebSocket,
    *,
    ticket: str | None,
    token: str | None,
) -> bool:
    """Prefer one-time ticket; optionally legacy JWT if explicitly allowed."""
    settings = get_settings()
    factory = get_session_factory()

    if ticket:
        async with factory() as session:
            auth = AuthService(session, settings)
            operator = await auth.consume_ws_ticket(ticket)
            await session.commit()
            if operator is None or not operator.is_active:
                await websocket.close(code=4401)
                return False
        return True

    # Legacy path: access JWT in query — only if allowlisted for transition
    if token and settings.ws_allow_query_jwt:
        payload = safe_decode(token, settings)
        if payload is None or payload.get("type") != "access" or not payload.get("sub"):
            await websocket.close(code=4401)
            return False
        async with factory() as session:
            auth = AuthService(session, settings)
            operator = await auth.get_operator_by_id(str(payload["sub"]))
            if operator is None or not operator.is_active:
                await websocket.close(code=4401)
                return False
        return True

    # Authorization header Bearer (some non-browser clients can set it)
    auth_header = websocket.headers.get("authorization") or websocket.headers.get("Authorization")
    if auth_header and auth_header.lower().startswith("bearer "):
        raw = auth_header.split(" ", 1)[1].strip()
        payload = safe_decode(raw, settings)
        if payload and payload.get("type") == "access" and payload.get("sub"):
            async with factory() as session:
                auth = AuthService(session, settings)
                operator = await auth.get_operator_by_id(str(payload["sub"]))
                if operator is not None and operator.is_active:
                    return True

    await websocket.close(code=4401)
    return False


@router.websocket("/ws/status")
async def websocket_status(
    websocket: WebSocket,
    ticket: str | None = Query(default=None),
    token: str | None = Query(default=None),
) -> None:
    """Authenticated status channel with narrowly scoped, non-sensitive payload."""
    correlation_id = websocket.headers.get("x-correlation-id") or new_correlation_id()
    ctx_token = set_correlation_id(correlation_id)
    try:
        if not await _authenticate_ws(websocket, ticket=ticket, token=token):
            logger.info("WebSocket status channel rejected (auth)")
            return

        await websocket.accept()
        live = get_live_market_service().stats()
        logger.info("WebSocket status channel connected")
        await websocket.send_json(
            {
                "type": "status",
                "channel": "status",
                "message": "AXIOM WebSocket status channel",
                "live_streams": bool(live.get("running")),
                "live_symbol": live.get("symbol"),
            }
        )
        while True:
            message = await websocket.receive_text()
            await websocket.send_json(
                {
                    "type": "echo",
                    "received": message,
                    "note": "Use short-lived tickets for AXIOM WebSockets.",
                }
            )
    except WebSocketDisconnect:
        logger.info("WebSocket status channel disconnected")
    finally:
        reset_correlation_id(ctx_token)


@router.websocket("/ws/market")
async def websocket_market(
    websocket: WebSocket,
    ticket: str | None = Query(default=None),
    token: str | None = Query(default=None),
) -> None:
    """Authenticated live market channel (prefer ?ticket= short-lived)."""
    correlation_id = websocket.headers.get("x-correlation-id") or new_correlation_id()
    ctx_token = set_correlation_id(correlation_id)
    if not await _authenticate_ws(websocket, ticket=ticket, token=token):
        logger.info("Live market WS rejected (auth)")
        reset_correlation_id(ctx_token)
        return

    await live_market_hub.connect(websocket)
    stats = get_live_market_service().stats()
    try:
        await websocket.send_json(
            {
                "type": "subscribed",
                "channel": "market",
                "symbol": stats.get("symbol"),
                "timeframe": stats.get("timeframe"),
                "running": stats.get("running"),
                "message": "Subscribed to live market channel",
            }
        )
        while True:
            message = await websocket.receive_text()
            if message.strip().lower() in {"ping", "health"}:
                await websocket.send_json(
                    {
                        "type": "pong",
                        "stats": {
                            "running": get_live_market_service().is_running,
                            "subscribers": live_market_hub.subscriber_count,
                        },
                    }
                )
    except WebSocketDisconnect:
        pass
    finally:
        await live_market_hub.disconnect(websocket)
        reset_correlation_id(ctx_token)
