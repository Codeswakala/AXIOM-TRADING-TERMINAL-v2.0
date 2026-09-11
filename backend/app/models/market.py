"""Live market API schemas."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class LiveMarketControlResponse(BaseModel):
    status: str
    stats: dict[str, Any]


class LiveMarketStatsResponse(BaseModel):
    running: bool
    auto_start: bool
    adapter: str | None
    connected: bool
    market_class: str
    symbol: str
    symbols: list[str] = Field(default_factory=list)
    timeframe: str
    messages_received: int
    persist_count: int
    persist_errors: int
    lag_ms: float | None
    last_message_at: str | None
    last_persisted_at: str | None
    started_at: str | None
    subscribers: int
    last_candle: dict[str, Any] | None
    latest_by_symbol: dict[str, Any] = Field(default_factory=dict)
    last_error: str | None
    reconnect_count: int
    adapter_details: dict[str, Any] = Field(default_factory=dict)


class LiveSubscribeResponse(BaseModel):
    channel: str = "market"
    websocket_path: str = "/ws/market"
    auth: str = Field(
        default="Use POST /api/v1/auth/ws-ticket, then connect with ?ticket=<ticket>",
    )
    symbol: str
    symbols: list[str] = Field(default_factory=list)
    timeframe: str
