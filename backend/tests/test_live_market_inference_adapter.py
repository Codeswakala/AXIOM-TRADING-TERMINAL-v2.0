"""W3-U04 live market inference adapter tests."""

from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path

import pytest

from app.core.time import utc_now
from app.db.models.economic_report import EconomicReport
from app.db.models.model_artifact import ModelArtifact
from app.repositories.candle_repository import CandleRepository
from app.trading_intelligence.inference import GovernedModelEligibilityGate
from app.trading_intelligence.live_market import (
    LiveMarketInferenceAdapter,
    LiveMarketInferenceError,
)
from app.trading_intelligence.signals import SignalGuardrailConfig
from tests.test_live_inference_gate import _eligible_artifact


async def _live_candle(
    session,
    *,
    open_time: datetime,
    close: str,
    source: str = "live:simulated",
):
    return await CandleRepository(session).upsert_ohlcv(
        market_class="forex",
        symbol="EURUSD",
        timeframe="M1",
        open_time=open_time,
        open=Decimal(close),
        high=Decimal(close) + Decimal("0.0100"),
        low=Decimal(close) - Decimal("0.0100"),
        close=Decimal(close),
        volume=Decimal("1"),
        source=source,
    )


async def _approved_artifact(session) -> ModelArtifact:  # noqa: ANN001
    artifact = await _eligible_artifact(session)
    artifact.operating_domain = {
        "markets": ["forex"],
        "timeframes": ["M1"],
        "regimes": ["trend"],
        "providers": ["internal"],
        "symbols": ["EURUSD"],
        "sources": ["live:simulated"],
    }
    gate = GovernedModelEligibilityGate(session)
    await gate.promote_to_advisory_approved(
        artifact,
        approver="ITRGA-test",
        approval_reason="W3-U04 live inference eligibility",
    )
    economic = await session.get(EconomicReport, artifact.economic_report_id)
    assert economic is not None
    economic.economic_conclusion = {"verdict": "economically_usable"}
    await session.flush()
    return artifact


@pytest.mark.asyncio
async def test_future_candle_cannot_enter_live_inference_input_no_lookahead(
    prepared_db: None,
) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        artifact = await _approved_artifact(session)
        base = utc_now() - timedelta(minutes=4)
        as_of = base + timedelta(minutes=1)
        future = as_of + timedelta(minutes=1)
        await _live_candle(session, open_time=base, close="1.1000")
        await _live_candle(session, open_time=as_of, close="1.2000")
        await _live_candle(session, open_time=future, close="9.9000")

        window = await LiveMarketInferenceAdapter(session).build_input(
            model=artifact,
            market_class="forex",
            provider="internal",
            symbol="EURUSD",
            timeframe="M1",
            requested_as_of_time=as_of,
            window_size=3,
        )

        assert window.excluded_future_candle_count == 1
        assert future not in window.candle_open_times
        assert all(open_time <= as_of for open_time in window.candle_open_times)
        assert window.effective_as_of_time == as_of
        assert window.inference_input.as_of_time == as_of
        assert set(window.inference_input.features) == {"return_1", "range_pct"}
        assert not {"symbol", "provider", "market_class"}.intersection(
            window.inference_input.features
        )
        assert window.inference_input.features["return_1"] == Decimal("0.0909090909")


@pytest.mark.asyncio
async def test_stale_live_data_withheld_stale_input(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        artifact = await _approved_artifact(session)
        await _live_candle(
            session,
            open_time=utc_now() - timedelta(minutes=10),
            close="1.1000",
        )
        adapter = LiveMarketInferenceAdapter(
            session,
            guardrail_config=SignalGuardrailConfig(max_input_staleness_seconds=30),
        )
        result = await adapter.produce_signal(
            model=artifact,
            market_class="forex",
            provider="internal",
            symbol="EURUSD",
            timeframe="M1",
            rationale="Stale live data must be withheld.",
            actor="pytest",
        )
        assert result.signal.signal_state == "withheld"
        assert result.signal.state_reason == "STALE_INPUT"
        assert result.signal.freshness_status == "stale"
        assert result.signal.raw_score is None


@pytest.mark.asyncio
async def test_deterministic_live_scoring_same_snapshot_same_score_and_hash(
    prepared_db: None,
) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        artifact = await _approved_artifact(session)
        base = utc_now() - timedelta(minutes=2)
        as_of = base + timedelta(minutes=1)
        await _live_candle(session, open_time=base, close="1.1000")
        await _live_candle(session, open_time=as_of, close="1.2000")
        adapter = LiveMarketInferenceAdapter(session)
        first_window = await adapter.build_input(
            model=artifact,
            market_class="forex",
            provider="internal",
            symbol="EURUSD",
            timeframe="M1",
            requested_as_of_time=as_of,
        )
        second_window = await adapter.build_input(
            model=artifact,
            market_class="forex",
            provider="internal",
            symbol="EURUSD",
            timeframe="M1",
            requested_as_of_time=as_of,
        )
        first = await adapter.score_snapshot(model=artifact, window=first_window)
        second = await adapter.score_snapshot(model=artifact, window=second_window)
        assert first.score == second.score
        assert first.inference_input_hash == second.inference_input_hash
        assert first.deterministic is True


@pytest.mark.asyncio
async def test_seed_synthetic_cannot_be_authoritative_live_inference_input(
    prepared_db: None,
) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        artifact = await _approved_artifact(session)
        as_of = utc_now() - timedelta(minutes=1)
        await _live_candle(
            session,
            open_time=as_of,
            close="1.1000",
            source="seed:synthetic",
        )
        with pytest.raises(LiveMarketInferenceError, match="SYNTHETIC_AUTHORITATIVE_INPUT_REFUSED"):
            await LiveMarketInferenceAdapter(session).build_input(
                model=artifact,
                market_class="forex",
                provider="internal",
                symbol="EURUSD",
                timeframe="M1",
                requested_as_of_time=as_of,
            )


@pytest.mark.asyncio
async def test_live_governed_path_refuses_non_advisory_model_by_name(
    prepared_db: None,
) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        artifact = await _eligible_artifact(session)
        artifact.operating_domain = {
            "markets": ["forex"],
            "timeframes": ["M1"],
            "regimes": ["trend"],
            "providers": ["internal"],
            "symbols": ["EURUSD"],
            "sources": ["live:simulated"],
        }
        as_of = utc_now() - timedelta(minutes=1)
        await _live_candle(session, open_time=as_of, close="1.1000")
        result = await LiveMarketInferenceAdapter(session).produce_signal(
            model=artifact,
            market_class="forex",
            provider="internal",
            symbol="EURUSD",
            timeframe="M1",
            rationale="Research-only live path must not emit.",
            requested_as_of_time=as_of,
            actor="pytest",
        )
        assert result.signal.signal_state == "withheld"
        assert "NOT_ADVISORY_APPROVED" in result.signal.state_reason
        assert "NOT_ADVISORY_APPROVED" in result.signal.eligibility_reasons


def test_live_market_inference_adapter_has_no_external_feed_or_execution_path() -> None:
    adapter_root = (
        Path(__file__).resolve().parents[1] / "app" / "trading_intelligence" / "live_market"
    )
    forbidden = (
        "place_order",
        "cancel_order",
        "broker.",
        "MetaTrader",
        "mt5",
        "requests.",
        "httpx.",
        "socket.",
        "websocket-client",
    )
    for path in adapter_root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for needle in forbidden:
            assert needle not in text
