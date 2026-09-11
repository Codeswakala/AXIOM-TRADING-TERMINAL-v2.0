"""Synthetic history seed for chart foundation (W0-U07 / UI-NEW-P03 CA-P03-3).

Presentation enablement only — not a market data vendor.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from decimal import Decimal
import hashlib
import random

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.db.models.candle import Candle
from app.market.live_service import LiveMarketService
from app.repositories.candle_repository import CandleRepository

logger = get_logger(__name__, category="MARKET")


def _stable_seed(*parts: str) -> int:
    """Derive a deterministic 32-bit RNG seed from stable string parts."""
    digest = hashlib.sha256(":".join(parts).encode("utf-8")).hexdigest()
    return int(digest[:8], 16)


def symbol_seed(symbol: str, timeframe: str) -> int:
    """DATA-P01 S2: per-symbol seed derivation.

    sha256("axiom:seed:synthetic:{SYMBOL}:{timeframe}") first 8 hex digits.
    A symbol's series therefore depends only on (symbol, timeframe) — not on
    seeding order — and re-seeding reproduces it exactly (proven by the named
    test test_chart_seed_per_symbol_determinism_and_order_independence).
    """
    return _stable_seed("axiom", "seed:synthetic", symbol.upper(), timeframe)


def class_factor_seed(market_class: str, timeframe: str) -> int:
    """DATA-P01 S3: per-class correlation factor stream seed."""
    return _stable_seed("axiom", "seed:synthetic", "factor", market_class, timeframe)


async def seed_chart_history(
    session: AsyncSession,
    *,
    symbols: list[str],
    timeframe: str = "M1",
    bars: int = 80,
    force_refresh: bool = True,
) -> dict[str, int]:
    """Insert non-degenerate synthetic OHLC bars when history is sparse or refreshed (CA-P03-3).

    DATA-P01: each symbol's walk is generated from its own deterministic RNG
    (S2) blended with a shared per-class factor stream (S3 — forex USD factor,
    crypto risk factor; USD-base pairs take the inverse sign, the EUR/GBP
    cross takes none). Every bar carries source="seed:synthetic" (M1). The
    walk distributions are unchanged from the original single-RNG design.
    """
    repo = CandleRepository(session)
    counts: dict[str, int] = {}
    symbols = [s.upper() for s in symbols]
    class_for = {s: LiveMarketService._infer_class(s) for s in symbols}

    # Pre-generate per-class factor streams (order-independent; one stream per
    # class regardless of how many symbols share it). CA-DATA1-2: the crypto
    # factor stream is FRACTIONAL (0.2%/bar sigma) so it scales with each
    # symbol's own price — BTC, ETH and SOL share one relative volatility
    # profile instead of an absolute step calibrated for BTC.
    factor_streams: dict[str, list[Decimal]] = {}
    for market_class in set(class_for.values()):
        factor_rng = random.Random(class_factor_seed(market_class, timeframe))
        if market_class == "crypto":
            factor_streams[market_class] = [
                Decimal(str(round(factor_rng.gauss(0, 0.002), 5))) for _ in range(bars)
            ]
        else:
            factor_streams[market_class] = [
                Decimal(str(round(factor_rng.gauss(0, 0.00006), 5))) for _ in range(bars)
            ]

    for symbol in symbols:
        if not force_refresh:
            existing = await repo.count_by_market(symbol=symbol, timeframe=timeframe)
            if existing >= 20:
                counts[symbol] = 0
                continue
        else:
            # Clear previous synthetic bars for this symbol and timeframe to allow clean re-seed
            stmt = delete(Candle).where(
                Candle.symbol == symbol,
                Candle.timeframe == timeframe,
                Candle.source == "seed:synthetic",
            )
            await session.execute(stmt)

        market_class = class_for[symbol]
        base_price = LiveMarketService._base_price(symbol)
        price = base_price
        start = datetime.now(timezone.utc).replace(second=0, microsecond=0) - timedelta(
            minutes=bars
        )
        batch: list[Candle] = []
        rng = random.Random(symbol_seed(symbol, timeframe))
        factors = factor_streams[market_class]
        # S3 correlation betas (stated plainly in the delivery report):
        # USD-quoted majors follow the shared forex factor (+1); USD-base pairs
        # invert it (-1); the EUR/GBP cross and non-forex classes take none
        # unless noted. Crypto pairs share the crypto factor (+1).
        if market_class == "forex":
            if symbol in {"EURUSD", "GBPUSD", "AUDUSD", "NZDUSD"}:
                beta = Decimal("1.0")
            elif symbol in {"USDJPY", "USDCAD", "USDCHF"}:
                beta = Decimal("-1.0")
            else:
                beta = Decimal("0.0")
        elif market_class == "crypto":
            beta = Decimal("1.0")
        else:
            beta = Decimal("0.0")

        # CA-DATA1-1 (2026-08-17): the walk branches on MARKET CLASS, not on
        # price magnitude. The previous `price >= 100` proxy sent USD/JPY
        # (base 150.000) down the crypto walk — ±8 yen per bar. JPY-quote
        # pairs take the JPY tick convention: 3-decimal quantization and pip
        # steps ~100x a EUR/USD pip, so relative per-bar moves match the
        # majors. The forex factor stream stays in EUR/USD-pip units and is
        # scaled by the same factor, keeping the beta correlation at the same
        # relative weight (0.4 of one idiosyncratic sigma) for every forex
        # pair instead of being numerically inert for JPY.
        is_crypto = market_class == "crypto"
        is_jpy = market_class == "forex" and symbol.endswith("JPY")
        factor_scale = Decimal("100") if is_jpy else Decimal("1")

        for i in range(bars):
            open_time = start + timedelta(minutes=i)
            if is_crypto:
                # Crypto walk (CA-DATA1-2): PROPORTIONAL steps — idiosyncratic
                # sigma 0.83% and mean +0.04% of the CURRENT price, wick sigma
                # 0.2% of price. BTC/ETH/SOL therefore share one relative
                # volatility profile; the previous absolute step (±8/35) was
                # calibrated for BTC and tripled SOL within a session.
                idio_frac = Decimal(str(round(rng.gauss(0, 0.0083), 5)))
                step = price * idio_frac + price * beta * factors[i]
                open_ = price
                close = (open_ + step).quantize(Decimal("0.01"))
                high_wick = price * Decimal(str(round(abs(rng.gauss(0.0012, 0.002)), 5)))
                low_wick = price * Decimal(str(round(abs(rng.gauss(0.0012, 0.002)), 5)))
                high = (max(open_, close) + high_wick).quantize(Decimal("0.01"))
                low = (min(open_, close) - low_wick).quantize(Decimal("0.01"))
                volume = Decimal(str(int(1000 + abs(rng.gauss(500, 250)))))
            elif is_jpy:
                # JPY walk (CA-DATA1-1): 3-decimal ticks, pip step ~100x
                # EUR/USD. Step sigma 0.015 = 15 pips of 0.001; mean 0.004.
                idio_step = Decimal(str(round(rng.gauss(0, 0.015), 3)))
                step = idio_step + beta * factors[i] * factor_scale
                open_ = price
                close = (open_ + step).quantize(Decimal("0.001"))
                high_wick = Decimal(str(round(abs(rng.gauss(0.006, 0.005)), 3)))
                low_wick = Decimal(str(round(abs(rng.gauss(0.006, 0.005)), 3)))
                high = (max(open_, close) + high_wick).quantize(Decimal("0.001"))
                low = (min(open_, close) - low_wick).quantize(Decimal("0.001"))
                volume = Decimal(str(int(150000 + abs(rng.gauss(40000, 20000)))))
            else:
                # Forex walk: realistic multi-pip excursions, varying body sizes, wicks
                idio_step = Decimal(str(round(rng.gauss(0, 0.00015), 5)))
                step = idio_step + beta * factors[i]
                open_ = price
                close = (open_ + step).quantize(Decimal("0.00001"))
                high_wick = Decimal(str(round(abs(rng.gauss(0.00006, 0.00005)), 5)))
                low_wick = Decimal(str(round(abs(rng.gauss(0.00006, 0.00005)), 5)))
                high = (max(open_, close) + high_wick).quantize(Decimal("0.00001"))
                low = (min(open_, close) - low_wick).quantize(Decimal("0.00001"))
                volume = Decimal(str(int(150000 + abs(rng.gauss(40000, 20000)))))

            batch.append(
                Candle(
                    market_class=market_class,
                    symbol=symbol,
                    timeframe=timeframe,
                    open_time=open_time,
                    open=open_,
                    high=high,
                    low=low,
                    close=close,
                    volume=volume,
                    source="seed:synthetic",
                )
            )
            price = close

        session.add_all(batch)
        await session.flush()
        counts[symbol] = len(batch)
        logger.info("Chart seed symbol=%s bars=%s non-degenerate walk", symbol, len(batch))

    return counts
