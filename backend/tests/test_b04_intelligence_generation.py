"""BO-B-04 — intelligence generation endpoint tests (fail-first).

Pre-fix expectation (b04_probe_prefix.log): the five POST endpoints do not
exist — the router is read-only (the FIND-2 gap). Post-fix: authenticated
generation, structured insufficient-data failures, no actuation, and the
persisted data-class label.
"""

from __future__ import annotations

from datetime import timedelta
from decimal import Decimal  # noqa: E402

import pytest
from httpx import AsyncClient
from sqlalchemy import func, select

from app.core.time import utc_now
from app.db.models.advisory_signal import AdvisorySignal
from app.db.models.audit import AuditEvent
from app.db.models.model_artifact import ModelArtifact
from app.db.session import session_scope
from app.repositories.candle_repository import CandleRepository


async def _seed_candles(  # noqa: ANN001
    session,
    *,
    symbol: str,
    values: list[float],
    timeframe: str = "H1",
    source: str = "historical:real",
    base=None,
) -> tuple:
    if base is None:
        base = utc_now().replace(second=0, microsecond=0) - timedelta(hours=len(values) + 2)
    times = []
    for index, value in enumerate(values):
        open_time = base + timedelta(hours=index)
        times.append(open_time)
        await CandleRepository(session).upsert_ohlcv(
            market_class="crypto",
            symbol=symbol,
            timeframe=timeframe,
            open_time=open_time,
            open=Decimal(str(value)),
            high=Decimal(str(value + 0.5)),
            low=Decimal(str(value - 0.5)),
            close=Decimal(str(value)),
            volume=Decimal("10"),
            source=source,
        )
    return times[0], times[-1]


async def _auth(client: AsyncClient) -> dict[str, str]:
    login = await client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert login.status_code == 200, login.text
    return {"Authorization": f"Bearer {login.json()['tokens']['access_token']}"}


@pytest.mark.asyncio
async def test_b04_generation_requires_auth(async_client: AsyncClient) -> None:
    series = {"market_class": "crypto", "symbol": "BTCUSDT", "timeframe": "H1"}
    bodies = [
        (
            "/api/v1/intelligence/correlation-reports",
            {
                "left": series,
                "right": {"market_class": "crypto", "symbol": "ETHUSDT", "timeframe": "H1"},
                "as_of_start": "2025-01-01T00:00:00Z",
                "as_of_end": "2025-01-02T00:00:00Z",
            },
        ),
        (
            "/api/v1/intelligence/regime-reports",
            {
                "series": series,
                "as_of_start": "2025-01-01T00:00:00Z",
                "as_of_end": "2025-01-02T00:00:00Z",
            },
        ),
        (
            "/api/v1/intelligence/scenario-reports",
            {
                "series": series,
                "assumptions": {
                    "scenario_name": "x",
                    "shock_return": 0.01,
                    "horizon_bars": 4,
                },
                "as_of_start": "2025-01-01T00:00:00Z",
                "as_of_end": "2025-01-02T00:00:00Z",
            },
        ),
        (
            "/api/v1/intelligence/portfolio-risk-reports",
            {
                "series": series,
                "assumptions": {"report_name": "x"},
                "as_of_start": "2025-01-01T00:00:00Z",
                "as_of_end": "2025-01-02T00:00:00Z",
            },
        ),
        (
            "/api/v1/intelligence/signal-validation-reports",
            {
                "scope_start": "2025-01-01T00:00:00Z",
                "scope_end": "2025-01-02T00:00:00Z",
            },
        ),
    ]
    for path, body in bodies:
        response = await async_client.post(path, json=body)
        assert response.status_code == 401, (
            f"{path} must require auth, got {response.status_code}"
        )


@pytest.mark.asyncio
async def test_b04_correlation_generation_happy_path(async_client: AsyncClient) -> None:
    base = utc_now().replace(second=0, microsecond=0) - timedelta(hours=7)
    async with session_scope() as session:
        start, end = await _seed_candles(
            session, symbol="BTCUSDT", values=[100.0, 101.0, 102.0, 103.0, 104.0], base=base
        )
        await _seed_candles(
            session, symbol="ETHUSDT", values=[50.0, 50.5, 51.0, 51.5, 52.0], base=base
        )
    headers = await _auth(async_client)
    response = await async_client.post(
        "/api/v1/intelligence/correlation-reports",
        json={
            "left": {"market_class": "crypto", "symbol": "BTCUSDT", "timeframe": "H1"},
            "right": {"market_class": "crypto", "symbol": "ETHUSDT", "timeframe": "H1"},
            "as_of_start": start.isoformat(),
            "as_of_end": end.isoformat(),
        },
        headers=headers,
    )
    assert response.status_code == 201, response.text
    report = response.json()
    assert report["sample_count"] == 5
    assert report["uncertainty"]["sample_count"] == 5
    assert report["created_by"] == "admin"
    assert "data-class: historical:real" in (report["notes"] or "")
    assert report["economic_usefulness"]["verdict"] == "not_assessed"

    # The report is readable through the unchanged read surface.
    listed = await async_client.get(
        "/api/v1/intelligence/correlation-reports", headers=headers
    )
    assert any(row["id"] == report["id"] for row in listed.json())

    # Audit lineage written by the service (resource_type=correlation_report).
    async with session_scope() as session:
        events = (
            await session.execute(
                select(AuditEvent).where(AuditEvent.resource_type == "correlation_report")
            )
        ).scalars().all()
        assert any(event.resource_id == report["id"] for event in events)


@pytest.mark.asyncio
async def test_b04_regime_scenario_portfolio_generation(async_client: AsyncClient) -> None:
    async with session_scope() as session:
        start, end = await _seed_candles(
            session, symbol="SOLUSDT", values=[20.0, 21.0, 19.5, 22.0, 21.5, 23.0]
        )
    headers = await _auth(async_client)
    series = {"market_class": "crypto", "symbol": "SOLUSDT", "timeframe": "H1"}

    regime = await async_client.post(
        "/api/v1/intelligence/regime-reports",
        json={"series": series, "as_of_start": start.isoformat(), "as_of_end": end.isoformat()},
        headers=headers,
    )
    assert regime.status_code == 201, regime.text
    assert regime.json()["sample_count"] == 6
    assert "regime_label" in regime.json()
    assert "data-class: historical:real" in (regime.json()["notes"] or "")

    scenario = await async_client.post(
        "/api/v1/intelligence/scenario-reports",
        json={
            "series": series,
            "assumptions": {"scenario_name": "dovish", "shock_return": 0.02, "horizon_bars": 4},
            "as_of_start": start.isoformat(),
            "as_of_end": end.isoformat(),
        },
        headers=headers,
    )
    assert scenario.status_code == 201, scenario.text
    assert "uncertainty" in scenario.json()

    risk = await async_client.post(
        "/api/v1/intelligence/portfolio-risk-reports",
        json={
            "series": series,
            "assumptions": {
                "report_name": "hypothetical",
                "stress_multiplier": 2.0,
                "tail_quantile": 0.05,
            },
            "as_of_start": start.isoformat(),
            "as_of_end": end.isoformat(),
        },
        headers=headers,
    )
    assert risk.status_code == 201, risk.text
    assert "uncertainty" in risk.json()


@pytest.mark.asyncio
async def test_b04_signal_validation_generation(async_client: AsyncClient) -> None:
    async with session_scope() as session:
        artifact = ModelArtifact(
            name="b04-fixture-model",
            version="1-42",
            status="research_only",
            framework="fixture",
            feature_set_version="feature_set.v1",
            research_status="research_only",
        )
        session.add(artifact)
        await session.flush()
        now = utc_now()
        session.add(
            AdvisorySignal(
                as_of_time=now - timedelta(minutes=5),
                market_class="forex",
                provider="internal",
                symbol="EURUSD",
                timeframe="M1",
                model_artifact_id=artifact.id,
                model_version=artifact.version,
                feature_set_version="feature_set.v1",
                experiment_id="exp-b04-fixture",
                inference_input_hash="b04-hash",
                audit_correlation_id="b04-fixture-correlation",
                raw_score=0.6,
                calibrated_confidence=0.6,
                signal_direction="positive_bias",
                signal_state="emitted",
                state_reason="ELIGIBLE",
                eligibility_reasons=[],
                operating_domain_status="valid",
                calibration_status="calibrated",
                economic_verdict="economically_usable",
                rationale="B-04 signal-validation evidence fixture (synthetic; disclosed).",
                explainability_summary={"confidence": {"calibrated_confidence": 0.6}},
            )
        )
        await session.flush()
        start = now - timedelta(hours=1)
        end = now
    headers = await _auth(async_client)
    response = await async_client.post(
        "/api/v1/intelligence/signal-validation-reports",
        json={"scope_start": start.isoformat(), "scope_end": end.isoformat()},
        headers=headers,
    )
    assert response.status_code == 201, response.text
    report = response.json()
    assert report["sample_count"] == 1
    assert "metrics" in report
    assert report["created_by"] == "admin"


@pytest.mark.asyncio
async def test_b04_insufficient_data_is_structured(async_client: AsyncClient) -> None:
    async with session_scope() as session:
        start, end = await _seed_candles(session, symbol="DOGEUSDT", values=[0.1])
    headers = await _auth(async_client)
    response = await async_client.post(
        "/api/v1/intelligence/correlation-reports",
        json={
            "left": {"market_class": "crypto", "symbol": "DOGEUSDT", "timeframe": "H1"},
            "right": {"market_class": "crypto", "symbol": "BTCUSDT", "timeframe": "H1"},
            "as_of_start": start.isoformat(),
            "as_of_end": end.isoformat(),
        },
        headers=headers,
    )
    assert response.status_code == 422
    body = response.json()
    assert body["detail"]["insufficient_data"] is True
    assert body["detail"]["error_code"] == "CORRELATION_REQUIRES_THREE_ALIGNED_POINTS"
    # No fabricated report persisted.
    async with session_scope() as session:
        from app.db.models.correlation_report import CorrelationReport

        count = (
            await session.execute(select(func.count()).select_from(CorrelationReport))
        ).scalar_one()
        assert count == 0


@pytest.mark.asyncio
async def test_b04_future_as_of_refused(async_client: AsyncClient) -> None:
    headers = await _auth(async_client)
    future = (utc_now() + timedelta(days=1)).isoformat()
    response = await async_client.post(
        "/api/v1/intelligence/regime-reports",
        json={
            "series": {"market_class": "crypto", "symbol": "BTCUSDT", "timeframe": "H1"},
            "as_of_start": "2025-01-01T00:00:00Z",
            "as_of_end": future,
        },
        headers=headers,
    )
    assert response.status_code == 422
    assert response.json()["detail"]["error_code"] == "REGIME_FUTURE_AS_OF_REFUSED"
    assert response.json()["detail"]["insufficient_data"] is False


@pytest.mark.asyncio
async def test_b04_generation_mutates_nothing_but_the_report(
    async_client: AsyncClient,
) -> None:
    """Non-actuation invariant: generating a correlation report changes the
    correlation table only — no advisory signals, no model artifacts, no
    broker/execution state."""
    base = utc_now().replace(second=0, microsecond=0) - timedelta(hours=6)
    async with session_scope() as session:
        start, end = await _seed_candles(
            session, symbol="BTCUSDT", values=[100.0, 101.0, 102.0, 103.0], base=base
        )
        await _seed_candles(
            session, symbol="ETHUSDT", values=[50.0, 50.5, 51.0, 51.5], base=base
        )
    headers = await _auth(async_client)
    async with session_scope() as session:
        from app.db.models.correlation_report import CorrelationReport

        before_reports = (
            await session.execute(select(func.count()).select_from(CorrelationReport))
        ).scalar_one()
        before_signals = (
            await session.execute(select(func.count()).select_from(AdvisorySignal))
        ).scalar_one()
        before_artifacts = (
            await session.execute(select(func.count()).select_from(ModelArtifact))
        ).scalar_one()
    response = await async_client.post(
        "/api/v1/intelligence/correlation-reports",
        json={
            "left": {"market_class": "crypto", "symbol": "BTCUSDT", "timeframe": "H1"},
            "right": {"market_class": "crypto", "symbol": "ETHUSDT", "timeframe": "H1"},
            "as_of_start": start.isoformat(),
            "as_of_end": end.isoformat(),
        },
        headers=headers,
    )
    assert response.status_code == 201
    async with session_scope() as session:
        from app.db.models.correlation_report import CorrelationReport

        after_reports = (
            await session.execute(select(func.count()).select_from(CorrelationReport))
        ).scalar_one()
        after_signals = (
            await session.execute(select(func.count()).select_from(AdvisorySignal))
        ).scalar_one()
        after_artifacts = (
            await session.execute(select(func.count()).select_from(ModelArtifact))
        ).scalar_one()
    assert after_reports == before_reports + 1
    assert after_signals == before_signals
    assert after_artifacts == before_artifacts


def test_b04_router_has_no_execution_or_broker_surface() -> None:
    from pathlib import Path

    router = (
        Path(__file__).resolve().parents[1]
        / "app"
        / "api"
        / "routes"
        / "intelligence.py"
    ).read_text(encoding="utf-8").lower()
    # Code-level actuation surface tokens (comments explaining the boundary
    # are not actuation code).
    forbidden = (
        "place_order",
        "cancel_order",
        "emit_signal",
        "brokerrepository",
        "orderintent",
        "executionservice",
        "accountrepository",
        "signal_repository",
    )
    assert all(term not in router for term in forbidden)
    assert "currentoperatordep" in router  # every generation endpoint is authenticated
