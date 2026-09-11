"""Live market inference adapter with as-of/no-look-ahead discipline (W3-U04)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.time import coerce_external_utc, require_utc, utc_now
from app.db.models.advisory_signal import AdvisorySignal
from app.db.models.candle import Candle
from app.db.models.model_artifact import ModelArtifact
from app.repositories.candle_repository import CandleRepository
from app.trading_intelligence.inference import InferenceInput, InferenceResult, LiveInferenceEngine
from app.trading_intelligence.live_market.errors import LiveMarketInferenceError
from app.trading_intelligence.signals import AdvisorySignalService, SignalGuardrailConfig

LIVE_INFERENCE_ALLOWED_SOURCES = ("live:simulated",)


@dataclass(frozen=True, slots=True)
class LiveMarketInferenceWindow:
    """Point-in-time live-market input assembled from persisted W1 live seam data."""

    requested_as_of_time: datetime
    effective_as_of_time: datetime
    market_class: str
    provider: str
    symbol: str
    timeframe: str
    regime: str
    feature_set_version: str
    inference_input: InferenceInput
    candle_open_times: tuple[datetime, ...]
    excluded_future_candle_count: int
    source: str


@dataclass(frozen=True, slots=True)
class LiveMarketSignalResult:
    """Governed live-path signal result plus its point-in-time window metadata."""

    window: LiveMarketInferenceWindow
    signal: AdvisorySignal


class LiveMarketInferenceAdapter:
    """Builds deterministic inference inputs from existing persisted live candles.

    The adapter intentionally uses the existing W1 live-market persistence/query
    seam. It opens no market-data connection and has no operator push surface.
    """

    def __init__(
        self,
        session: AsyncSession,
        guardrail_config: SignalGuardrailConfig | None = None,
    ) -> None:
        self._session = session
        self._candles = CandleRepository(session)
        self._guardrail_config = guardrail_config

    async def build_input(
        self,
        *,
        model: ModelArtifact,
        market_class: str,
        provider: str,
        symbol: str,
        timeframe: str,
        requested_as_of_time: datetime | None = None,
        window_size: int = 2,
        regime: str | None = None,
    ) -> LiveMarketInferenceWindow:
        """Assemble a causal inference input from candles at or before as-of time."""
        if not model.feature_set_version:
            raise LiveMarketInferenceError("MODEL_FEATURE_SET_VERSION_REQUIRED")
        requested_as_of = require_utc(
            requested_as_of_time or utc_now(), boundary="live_market_inference.requested_as_of_time"
        )
        assert requested_as_of is not None
        if requested_as_of > utc_now():
            raise LiveMarketInferenceError("FUTURE_AS_OF_REFUSED")
        if window_size < 1:
            raise LiveMarketInferenceError("WINDOW_SIZE_INVALID")

        candles = list(
            await self._candles.list_window_as_of(
                market_class=market_class,
                symbol=symbol,
                timeframe=timeframe,
                as_of_time=requested_as_of,
                limit=window_size,
                allowed_sources=LIVE_INFERENCE_ALLOWED_SOURCES,
            )
        )
        if not candles:
            any_source = list(
                await self._candles.list_window_as_of(
                    market_class=market_class,
                    symbol=symbol,
                    timeframe=timeframe,
                    as_of_time=requested_as_of,
                    limit=1,
                )
            )
            if any_source and any_source[-1].source == "seed:synthetic":
                raise LiveMarketInferenceError("SYNTHETIC_AUTHORITATIVE_INPUT_REFUSED")
            raise LiveMarketInferenceError("NO_LIVE_CANDLES_AS_OF")
        future_count = await self._candles.count_after(
            market_class=market_class,
            symbol=symbol,
            timeframe=timeframe,
            after_time=requested_as_of,
        )
        effective_as_of = coerce_external_utc(
            candles[-1].open_time, source="live_market_inference.effective_as_of"
        )
        assert effective_as_of is not None
        source = candles[-1].source or "unknown"
        if source not in LIVE_INFERENCE_ALLOWED_SOURCES:
            raise LiveMarketInferenceError("UNSUPPORTED_LIVE_SOURCE")
        resolved_regime = regime or self._default_regime(model)
        features = self._features(candles)
        inference_input = InferenceInput(
            as_of_time=effective_as_of,
            feature_set_version=model.feature_set_version,
            features=features,
            market_class=market_class,
            provider=provider,
            symbol=symbol,
            timeframe=timeframe,
            regime=resolved_regime,
            source=source,
        )
        return LiveMarketInferenceWindow(
            requested_as_of_time=requested_as_of,
            effective_as_of_time=effective_as_of,
            market_class=market_class,
            provider=provider,
            symbol=symbol,
            timeframe=timeframe,
            regime=resolved_regime,
            feature_set_version=model.feature_set_version,
            inference_input=inference_input,
            candle_open_times=tuple(
                coerce_external_utc(candle.open_time, source="live_market_inference.window")
                for candle in candles
            ),
            excluded_future_candle_count=future_count,
            source=source,
        )

    async def score_snapshot(
        self,
        *,
        model: ModelArtifact,
        window: LiveMarketInferenceWindow,
    ) -> InferenceResult:
        """Score a prebuilt live snapshot through the W3-U01 deterministic engine."""
        return await LiveInferenceEngine(self._session).score(
            model=model, inference_input=window.inference_input
        )

    async def produce_signal(
        self,
        *,
        model: ModelArtifact,
        market_class: str,
        provider: str,
        symbol: str,
        timeframe: str,
        rationale: str | None,
        requested_as_of_time: datetime | None = None,
        window_size: int = 2,
        regime: str | None = None,
        actor: str = "system",
        risk_notes: str | None = None,
        audit_correlation_id: str | None = None,
    ) -> LiveMarketSignalResult:
        """Build a live input and persist its governed W3-U02/U03 signal decision."""
        window = await self.build_input(
            model=model,
            market_class=market_class,
            provider=provider,
            symbol=symbol,
            timeframe=timeframe,
            requested_as_of_time=requested_as_of_time,
            window_size=window_size,
            regime=regime,
        )
        signal = await AdvisorySignalService(
            self._session, guardrail_config=self._guardrail_config
        ).produce(
            model=model,
            inference_input=window.inference_input,
            rationale=rationale,
            actor=actor,
            risk_notes=risk_notes,
            audit_correlation_id=audit_correlation_id,
        )
        return LiveMarketSignalResult(window=window, signal=signal)

    def _features(self, candles: Sequence[Candle]) -> dict[str, Decimal]:
        last = candles[-1]
        previous = candles[-2] if len(candles) >= 2 else last
        return {
            "return_1": self._ratio(last.close - previous.close, previous.close),
            "range_pct": self._ratio(last.high - last.low, last.close),
        }

    def _ratio(self, numerator: Decimal, denominator: Decimal) -> Decimal:
        if denominator == 0:
            return Decimal("0")
        return (numerator / denominator).quantize(Decimal("0.0000000001"))

    def _default_regime(self, model: ModelArtifact) -> str:
        domain = model.operating_domain or {}
        regimes = domain.get("regimes") or []
        if regimes:
            return str(regimes[0])
        return "unknown"
