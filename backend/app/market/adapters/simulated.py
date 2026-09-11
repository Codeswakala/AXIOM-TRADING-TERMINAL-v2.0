"""Simulated live candle adapter(s) — foundation feeds without external APIs.

B-00.1 (BO-B-00): wall-clock-bind chronology model (option (a)). The adapter
emits bar `N` only when the wall clock has reached `start_time + N minutes`;
while the simulated clock is behind the wall clock (fresh start, restart,
catch-up after a wall-clock jump) emission proceeds at the configured
accelerated tick cadence. The invariant: **no emitted bar is ever dated in the
future** — `open_time <= utc_now()` at the moment of emission.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Callable

from app.core.logging import get_logger
from app.ingestion.types import NormalizedCandleRow
from app.market.adapters.base import AdapterStatus, CandleHandler, MarketDataAdapter

logger = get_logger(__name__, category="MARKET")


@dataclass(slots=True)
class SimulatedSymbolSpec:
    market_class: str
    symbol: str
    timeframe: str = "M1"
    base_price: Decimal = Decimal("1.10000")
    interval_seconds: float = 1.0


class SimulatedCandleAdapter(MarketDataAdapter):
    """Emits synthetic OHLCV bars for one symbol."""

    name = "simulated"

    def __init__(
        self,
        *,
        market_class: str = "forex",
        symbol: str = "EURUSD",
        timeframe: str = "M1",
        interval_seconds: float = 1.0,
        base_price: Decimal = Decimal("1.10000"),
        max_ticks: int | None = None,
        start_time: datetime | None = None,
        now_fn: Callable[[], datetime] | None = None,
    ) -> None:
        self._market_class = market_class.lower()
        self._symbol = symbol.upper()
        self._timeframe = timeframe.upper()
        self._interval = max(0.05, float(interval_seconds))
        self._base = base_price
        self._max_ticks = max_ticks
        self._start_time = start_time or datetime.now(timezone.utc).replace(second=0, microsecond=0)
        # B-00.1: injectable wall clock (defaults to real UTC) so chronology
        # invariants are deterministically testable.
        self._now_fn = now_fn or (lambda: datetime.now(timezone.utc))

        self._task: asyncio.Task[None] | None = None
        self._stop = asyncio.Event()
        self._connected = False
        self._messages = 0
        self._reconnects = 0
        self._last_message_at: datetime | None = None
        self._last_error: str | None = None
        self._price = base_price
        self._seq = 0
        self._holding = False

    async def start(self, on_candle: CandleHandler) -> None:
        if self._task and not self._task.done():
            return
        self._stop.clear()
        self._connected = True
        self._last_error = None
        logger.info(
            "Simulated adapter starting %s %s %s interval=%ss",
            self._market_class,
            self._symbol,
            self._timeframe,
            self._interval,
        )
        self._task = asyncio.create_task(self._run(on_candle), name=f"sim-{self._symbol}")

    async def stop(self) -> None:
        self._stop.set()
        self._connected = False
        if self._task is not None:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None
        logger.info("Simulated adapter stopped symbol=%s messages=%s", self._symbol, self._messages)

    def status(self) -> AdapterStatus:
        lag: float | None = None
        if self._last_message_at is not None:
            lag = (datetime.now(timezone.utc) - self._last_message_at).total_seconds() * 1000.0
        return AdapterStatus(
            name=self.name,
            connected=self._connected and not self._stop.is_set(),
            market_class=self._market_class,
            symbol=self._symbol,
            timeframe=self._timeframe,
            last_message_at=self._last_message_at,
            messages_received=self._messages,
            reconnect_count=self._reconnects,
            last_error=self._last_error,
            lag_ms=lag,
            details={"interval_seconds": self._interval, "base_price": str(self._base)},
        )

    async def _run(self, on_candle: CandleHandler) -> None:
        try:
            while not self._stop.is_set():
                if self._max_ticks is not None and self._seq >= self._max_ticks:
                    break
                # B-00.1 (a): never emit a bar dated in the future. Hold until
                # the wall clock reaches the next bar's open minute.
                await self._hold_until_due()
                if self._stop.is_set():
                    break
                candle = self._next_candle()
                self._messages += 1
                self._last_message_at = datetime.now(timezone.utc)
                await on_candle(candle)
                try:
                    await asyncio.wait_for(self._stop.wait(), timeout=self._interval)
                except TimeoutError:
                    continue
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001
            self._last_error = f"{exc.__class__.__name__}: {exc}"
            self._connected = False
            logger.exception("Simulated adapter failed symbol=%s", self._symbol)
        finally:
            self._connected = False

    def _candidate_open_time(self) -> datetime:
        """The bar `self._seq` is dated at this wall-clock minute."""
        return self._start_time + timedelta(minutes=self._seq)

    async def _hold_until_due(self) -> None:
        """B-00.1 (a): block until the wall clock reaches the next bar's minute.

        While the simulated clock is behind the wall clock (fresh start,
        restart, catch-up), `remaining <= 0` and the loop returns immediately —
        emission proceeds at the configured accelerated tick cadence. Once the
        wall clock is the limiting side, one M1 bar is emitted per real minute.
        The wait is sliced to at most `interval` so `stop()` stays responsive.
        """
        while not self._stop.is_set():
            remaining = (self._candidate_open_time() - self._now_fn()).total_seconds()
            if remaining <= 0:
                if self._holding:
                    logger.debug(
                        "Simulated adapter resumed symbol=%s seq=%s",
                        self._symbol,
                        self._seq,
                    )
                    self._holding = False
                return
            if not self._holding:
                self._holding = True
                logger.debug(
                    "Simulated adapter holding symbol=%s seq=%s until=%s (%.1fs)",
                    self._symbol,
                    self._seq,
                    self._candidate_open_time().isoformat(),
                    remaining,
                )
            try:
                await asyncio.wait_for(
                    self._stop.wait(), timeout=min(remaining, self._interval)
                )
            except TimeoutError:
                continue

    def _next_candle(self) -> NormalizedCandleRow:
        delta = Decimal("0.00010") * (1 if self._seq % 2 == 0 else -1)
        # CA-DATA1-1 (2026-08-17): branch on MARKET CLASS, not on price
        # magnitude. The previous `price >= 100` proxy sent USD/JPY (base
        # 150.000) down the crypto-scale step (±5 per tick — the capture
        # carried it from 150 to 155 within the first minute). JPY-quote
        # pairs take the JPY tick convention: 3-decimal ticks with a pip
        # step ~100x the EUR/USD pip, matching the corrected chart seeder.
        if self._market_class == "crypto":
            # CA-DATA1-2 (2026-08-18): proportional crypto tick — ±0.05% of
            # the CURRENT price, wicks ±0.025% of price. The previous absolute
            # ±5.00 step was 0.012% of BTC but 3.33% of SOL; the proportional
            # step gives BTC, ETH and SOL one relative volatility profile.
            delta = (self._price * Decimal("0.0005")) * (1 if self._seq % 2 == 0 else -1)
            open_ = self._price
            close = (open_ + delta).quantize(Decimal("0.01"))
            wick = (self._price * Decimal("0.00025")).quantize(Decimal("0.01"))
            high = max(open_, close) + wick
            low = min(open_, close) - wick
        elif self._market_class == "forex" and self._symbol.endswith("JPY"):
            delta = Decimal("0.010") * (1 if self._seq % 2 == 0 else -1)
            open_ = self._price
            close = (open_ + delta).quantize(Decimal("0.001"))
            high = max(open_, close) + Decimal("0.005")
            low = min(open_, close) - Decimal("0.005")
        else:
            open_ = self._price
            close = (open_ + delta).quantize(Decimal("0.00001"))
            high = max(open_, close) + Decimal("0.00005")
            low = min(open_, close) - Decimal("0.00005")
        open_time = self._start_time + timedelta(minutes=self._seq)
        self._price = close
        self._seq += 1
        return NormalizedCandleRow(
            market_class=self._market_class,
            symbol=self._symbol,
            timeframe=self._timeframe,
            open_time=open_time if open_time.tzinfo else open_time.replace(tzinfo=timezone.utc),
            open=open_,
            high=high,
            low=low,
            close=close,
            volume=Decimal("100") + Decimal(self._seq),
            source="live:simulated",
            extra={"seq": self._seq, "adapter": self.name},
        )


class MultiSymbolSimulatedAdapter(MarketDataAdapter):
    """Composite adapter that runs multiple SimulatedCandleAdapter instances."""

    name = "simulated-multi"

    def __init__(self, specs: list[SimulatedSymbolSpec], *, max_ticks: int | None = None) -> None:
        if not specs:
            raise ValueError("at least one symbol spec required")
        self._children = [
            SimulatedCandleAdapter(
                market_class=s.market_class,
                symbol=s.symbol,
                timeframe=s.timeframe,
                interval_seconds=s.interval_seconds,
                base_price=s.base_price,
                max_ticks=max_ticks,
            )
            for s in specs
        ]
        self._connected = False
        self._started = False

    async def start(self, on_candle: CandleHandler) -> None:
        self._connected = True
        self._started = True
        for child in self._children:
            await child.start(on_candle)
        logger.info(
            "Multi-symbol simulated adapter started symbols=%s",
            [c.status().symbol for c in self._children],
        )

    async def stop(self) -> None:
        for child in self._children:
            await child.stop()
        self._connected = False
        logger.info("Multi-symbol simulated adapter stopped")

    def status(self) -> AdapterStatus:
        children = [c.status() for c in self._children]
        messages = sum(c.messages_received for c in children)
        last_times = [c.last_message_at for c in children if c.last_message_at is not None]
        last_msg = max(last_times) if last_times else None
        lag = None
        if last_msg is not None:
            lag = (datetime.now(timezone.utc) - last_msg).total_seconds() * 1000.0
        connected = self._started and all(c.connected for c in children)
        primary = children[0]
        return AdapterStatus(
            name=self.name,
            connected=connected,
            market_class="multi",
            symbol=",".join(c.symbol for c in children),
            timeframe=primary.timeframe,
            last_message_at=last_msg,
            messages_received=messages,
            reconnect_count=sum(c.reconnect_count for c in children),
            last_error=next((c.last_error for c in children if c.last_error), None),
            lag_ms=lag,
            details={
                "symbols": [
                    {
                        "symbol": c.symbol,
                        "market_class": c.market_class,
                        "messages": c.messages_received,
                        "connected": c.connected,
                    }
                    for c in children
                ]
            },
        )
