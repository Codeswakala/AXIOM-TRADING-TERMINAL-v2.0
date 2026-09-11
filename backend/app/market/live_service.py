"""Live market service — adapter lifecycle, persistence, fan-out."""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any

from app.core.config import Settings, get_settings
from app.core.logging import get_logger
from app.db.session import get_session_factory, sqlite_staticpool_serialization
from app.ingestion.types import NormalizedCandleRow
from app.market.adapters.base import AdapterStatus, MarketDataAdapter
from app.market.adapters.simulated import (
    MultiSymbolSimulatedAdapter,
    SimulatedCandleAdapter,
    SimulatedSymbolSpec,
)
from app.market.hub import live_market_hub
from app.repositories.candle_repository import CandleRepository

logger = get_logger(__name__, category="MARKET")

_service: LiveMarketService | None = None


class LiveMarketService:
    """Owns the active live adapter and routes candles into persistence + hub."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._adapter: MarketDataAdapter | None = None
        self._running = False
        self._started_at: datetime | None = None
        self._last_persisted_at: datetime | None = None
        self._persist_count = 0
        self._persist_errors = 0
        self._last_candle: dict[str, Any] | None = None
        self._latest_by_symbol: dict[str, dict[str, Any]] = {}
        self._lock = asyncio.Lock()
        # Serialize DB access — required for SQLite StaticPool / shared connection
        self._db_lock = asyncio.Lock()

    @property
    def is_running(self) -> bool:
        return self._running

    def get_adapter_status(self) -> AdapterStatus | None:
        if self._adapter is None:
            return None
        return self._adapter.status()

    def stats(self) -> dict[str, Any]:
        status = self.get_adapter_status()
        symbols_cfg = self._settings.live_market_symbols_list
        return {
            "running": self._running,
            "auto_start": self._settings.live_market_auto_start,
            "adapter": status.name if status else None,
            "connected": status.connected if status else False,
            "market_class": status.market_class if status else self._settings.live_market_class,
            "symbol": status.symbol if status else self._settings.live_market_symbol,
            "symbols": symbols_cfg,
            "timeframe": status.timeframe if status else self._settings.live_market_timeframe,
            "messages_received": status.messages_received if status else 0,
            "persist_count": self._persist_count,
            "persist_errors": self._persist_errors,
            "lag_ms": status.lag_ms if status else None,
            "last_message_at": (
                status.last_message_at.isoformat() if status and status.last_message_at else None
            ),
            "last_persisted_at": (
                self._last_persisted_at.isoformat() if self._last_persisted_at else None
            ),
            "started_at": self._started_at.isoformat() if self._started_at else None,
            "subscribers": live_market_hub.subscriber_count,
            "last_candle": self._last_candle,
            "latest_by_symbol": self._latest_by_symbol,
            "last_error": status.last_error if status else None,
            "reconnect_count": status.reconnect_count if status else 0,
            "adapter_details": status.details if status else {},
        }

    def readiness_detail(self) -> tuple[str, str]:
        if not self._settings.live_market_enabled:
            return "stub", "live market disabled by configuration"
        if not self._running:
            return "degraded", "live adapter not running (start via API or auto_start)"
        status = self.get_adapter_status()
        if status is None:
            return "degraded", "no adapter attached"
        if status.connected:
            lag = f"{status.lag_ms:.0f}ms" if status.lag_ms is not None else "n/a"
            return "up", f"adapter={status.name}; symbols={status.symbol}; lag={lag}"
        return "degraded", f"adapter disconnected: {status.last_error or 'unknown'}"

    async def start(self, adapter: MarketDataAdapter | None = None) -> dict[str, Any]:
        async with self._lock:
            if self._running:
                return self.stats()
            self._adapter = adapter or self._build_default_adapter()
            self._running = True
            self._started_at = datetime.now(timezone.utc)
            await self._adapter.start(self._on_candle)
            logger.info("Live market service started adapter=%s", self._adapter.name)
            return self.stats()

    async def stop(self) -> dict[str, Any]:
        async with self._lock:
            if self._adapter is not None:
                await self._adapter.stop()
            self._running = False
            logger.info("Live market service stopped")
            return self.stats()

    def _build_default_adapter(self) -> MarketDataAdapter:
        symbols = self._settings.live_market_symbols_list
        interval = self._settings.live_market_interval_seconds
        timeframe = self._settings.live_market_timeframe
        if len(symbols) == 1:
            sym = symbols[0]
            return SimulatedCandleAdapter(
                market_class=self._infer_class(sym),
                symbol=sym,
                timeframe=timeframe,
                interval_seconds=interval,
                base_price=self._base_price(sym),
            )
        specs = [
            SimulatedSymbolSpec(
                market_class=self._infer_class(sym),
                symbol=sym,
                timeframe=timeframe,
                base_price=self._base_price(sym),
                interval_seconds=interval,
            )
            for sym in symbols
        ]
        return MultiSymbolSimulatedAdapter(specs)

    @staticmethod
    def _infer_class(symbol: str) -> str:
        s = symbol.upper()
        if s in {"BTCUSD", "ETHUSD", "SOLUSD", "BTCUSDT", "ETHUSDT", "SOLUSDT"}:
            return "crypto"
        if s in {"XAUUSD", "XAGUSD"}:
            return "metal"
        return "forex"

    @staticmethod
    def _base_price(symbol: str) -> Decimal:
        s = symbol.upper()
        # DATA-P01 S1: reference base prices for the simulated feed. These are
        # simulator inputs — plausible round levels per class — NOT market
        # observations and never presented as such (M2/M3).
        defaults = {
            "EURUSD": Decimal("1.10000"),
            "GBPUSD": Decimal("1.27000"),
            "USDJPY": Decimal("150.000"),
            "AUDUSD": Decimal("0.66000"),
            "USDCAD": Decimal("1.36000"),
            "USDCHF": Decimal("0.88000"),
            "NZDUSD": Decimal("0.61000"),
            "EURGBP": Decimal("0.86000"),
            "BTCUSD": Decimal("42000.00"),
            "ETHUSD": Decimal("2500.00"),
            "SOLUSD": Decimal("150.00"),
            "XAUUSD": Decimal("2300.00"),
        }
        # DATA-P01 M4: an unknown symbol must NOT silently receive a
        # plausible-looking default. Fail loudly at adapter build/seeding —
        # a wrong price is worse than no price.
        if s not in defaults:
            raise KeyError(f"no simulated base price for symbol {s} (seed:synthetic reference data)")
        return defaults[s]

    async def _on_candle(self, candle: NormalizedCandleRow) -> None:
        payload = {
            "type": "live_candle",
            "channel": "market",
            "market_class": candle.market_class,
            "symbol": candle.symbol,
            "timeframe": candle.timeframe,
            "open_time": candle.open_time.isoformat(),
            "open": str(candle.open),
            "high": str(candle.high),
            "low": str(candle.low),
            "close": str(candle.close),
            "volume": str(candle.volume) if candle.volume is not None else None,
            "source": candle.source,
            "received_at": datetime.now(timezone.utc).isoformat(),
        }
        self._last_candle = payload
        self._latest_by_symbol[candle.symbol] = payload

        # Persist best-effort: live feed must not crash request sessions if DB is busy
        # (SQLite StaticPool under concurrent writers). Always broadcast to WS.
        try:
            async with self._db_lock:
                async with sqlite_staticpool_serialization(self._settings):
                    factory = get_session_factory()
                    async with factory() as session:
                        try:
                            repo = CandleRepository(session)
                            entity, action = await repo.upsert_ohlcv(
                                market_class=candle.market_class,
                                symbol=candle.symbol,
                                timeframe=candle.timeframe,
                                open_time=candle.open_time,
                                open=candle.open,
                                high=candle.high,
                                low=candle.low,
                                close=candle.close,
                                volume=candle.volume,
                                source=candle.source,
                            )
                            await session.commit()
                            self._persist_count += 1
                            self._last_persisted_at = datetime.now(timezone.utc)
                            payload["persist_action"] = action
                            payload["candle_id"] = getattr(entity, "id", None)
                        except Exception as exc:  # noqa: BLE001
                            try:
                                await session.rollback()
                            except Exception:  # noqa: BLE001
                                pass
                            self._persist_errors += 1
                            payload["persist_error"] = f"{exc.__class__.__name__}: {exc}"
                            logger.exception("Failed to persist live candle")
        except Exception as exc:  # noqa: BLE001
            self._persist_errors += 1
            payload["persist_error"] = f"{exc.__class__.__name__}: {exc}"
            logger.exception("Live candle DB lock/session failure")

        try:
            await live_market_hub.broadcast(payload)
        except Exception:  # noqa: BLE001
            logger.exception("Live candle broadcast failure")


def get_live_market_service() -> LiveMarketService:
    global _service
    if _service is None:
        _service = LiveMarketService(get_settings())
    return _service


def reset_live_market_service() -> None:
    global _service
    _service = None
