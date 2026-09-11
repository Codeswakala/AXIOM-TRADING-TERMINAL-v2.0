"""In-process fan-out hub for live market WebSocket subscribers."""

from __future__ import annotations

import asyncio
from typing import Any

from fastapi import WebSocket

from app.core.logging import get_logger

logger = get_logger(__name__, category="MARKET")


class LiveMarketHub:
    """Tracks authenticated WebSocket clients and broadcasts JSON payloads."""

    def __init__(self) -> None:
        self._clients: set[WebSocket] = set()
        self._lock = asyncio.Lock()

    @property
    def subscriber_count(self) -> int:
        return len(self._clients)

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        async with self._lock:
            self._clients.add(websocket)
        logger.info("Live market WS subscriber added count=%s", len(self._clients))

    async def disconnect(self, websocket: WebSocket) -> None:
        async with self._lock:
            self._clients.discard(websocket)
        logger.info("Live market WS subscriber removed count=%s", len(self._clients))

    async def broadcast(self, payload: dict[str, Any]) -> None:
        async with self._lock:
            clients = list(self._clients)
        stale: list[WebSocket] = []
        for ws in clients:
            try:
                await ws.send_json(payload)
            except Exception:  # noqa: BLE001
                stale.append(ws)
        for ws in stale:
            await self.disconnect(ws)


# Process-wide hub (single uvicorn process model)
live_market_hub = LiveMarketHub()
