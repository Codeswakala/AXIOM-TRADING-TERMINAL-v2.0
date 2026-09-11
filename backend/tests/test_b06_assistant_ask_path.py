"""BO-B-06 — governed assistant ask-path tests (fail-first).

Pre-fix expectation (b06_probe_prefix.log): `POST /collaboration/assistant-respond`
does not exist (405) — the responder is unreachable (FIND-3). Post-fix: the
ask path resolves real grounding, delegates to the deterministic responder,
persists responses AND refusals with hash-only prompt storage, and never
makes external calls or actuates.
"""

from __future__ import annotations

import hashlib
from datetime import timedelta
from decimal import Decimal

import pytest
from httpx import AsyncClient
from sqlalchemy import func, select

from app.core.time import utc_now
from app.db.models.advisory_signal import AdvisorySignal
from app.db.models.assistant_research_response import AssistantResearchResponse
from app.db.models.monitoring_alert import MonitoringAlert
from app.db.session import session_scope
from app.institutional_intelligence import (
    CorrelationReportService,
    CorrelationSeriesSpec,
)
from app.repositories.candle_repository import CandleRepository


async def _auth(client: AsyncClient) -> dict[str, str]:
    login = await client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert login.status_code == 200, login.text
    return {"Authorization": f"Bearer {login.json()['tokens']['access_token']}"}


async def _seed_correlation(session) -> str:  # noqa: ANN001
    base = utc_now().replace(second=0, microsecond=0) - timedelta(hours=7)
    for index, (sym, values) in enumerate(
        [
            ("BTCUSDT", ["100.0", "101.0", "102.0", "103.0", "104.0"]),
            ("ETHUSDT", ["50.0", "50.5", "51.0", "51.5", "52.0"]),
        ]
    ):
        for offset, value in enumerate(values):
            await CandleRepository(session).upsert_ohlcv(
                market_class="crypto",
                symbol=sym,
                timeframe="H1",
                open_time=base + timedelta(hours=offset),
                open=Decimal(value),
                high=Decimal(value) + Decimal("0.5"),
                low=Decimal(value) - Decimal("0.5"),
                close=Decimal(value),
                volume=Decimal("10"),
                source="historical:real",
            )
    result = await CorrelationReportService(session).create_report(
        left=CorrelationSeriesSpec("crypto", "BTCUSDT", "H1"),
        right=CorrelationSeriesSpec("crypto", "ETHUSDT", "H1"),
        as_of_start=base,
        as_of_end=base + timedelta(hours=4),
        actor="b06-fixture",
    )
    return result.report.id


async def _respond(client: AsyncClient, headers, *, prompt: str, ids: list[str]) -> dict:
    response = await client.post(
        "/api/v1/collaboration/assistant-respond",
        json={"prompt": prompt, "grounding_source_ids": ids},
        headers=headers,
    )
    return {"status": response.status_code, "body": response.json()}


@pytest.mark.asyncio
async def test_b06_ask_requires_auth(async_client: AsyncClient) -> None:
    response = await async_client.post(
        "/api/v1/collaboration/assistant-respond",
        json={"prompt": "hello", "grounding_source_ids": []},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_b06_grounded_answer_over_real_artifact(async_client: AsyncClient) -> None:
    async with session_scope() as session:
        artifact_id = await _seed_correlation(session)
    headers = await _auth(async_client)
    result = await _respond(
        async_client,
        headers,
        prompt="Summarize the correlation context of the selected report.",
        ids=[artifact_id],
    )
    assert result["status"] == 201, result["body"]
    body = result["body"]
    assert body["refused"] is False
    assert artifact_id in body["source_artifact_ids"]
    assert "Grounded research summary" in body["response_text"]
    assert body["disclaimer"], "disclaimer required on every grounded answer"
    assert body["audit_correlation_id"]
    assert body["research_status"] == "research_only"
    # Hash-only prompt storage: the hash is the prompt's sha256; no raw text.
    assert body["request_text_hash"] == hashlib.sha256(
        "Summarize the correlation context of the selected report.".encode()
    ).hexdigest()
    assert body["provenance"]["raw_request_text_stored"] is False
    assert body["provenance"]["external_llm_used"] is False

    # Read-back through the unchanged GET surface.
    listed = await async_client.get(
        "/api/v1/collaboration/assistant-responses", headers=headers
    )
    assert any(
        row["assistant_response_id"] == body["assistant_response_id"]
        for row in listed.json()
    )


@pytest.mark.asyncio
async def test_b06_empty_grounding_refused(async_client: AsyncClient) -> None:
    headers = await _auth(async_client)
    result = await _respond(
        async_client, headers, prompt="What does the market look like?", ids=[]
    )
    assert result["status"] == 201  # the record is created (a refusal record)
    body = result["body"]
    assert body["refused"] is True
    assert body["refusal_reason"] == "GROUNDING_REQUIRED"
    assert "Refused: GROUNDING_REQUIRED" in body["response_text"]
    assert body["research_status"] == "refused"


@pytest.mark.asyncio
async def test_b06_unknown_ids_excluded_then_grounding_refused(
    async_client: AsyncClient,
) -> None:
    headers = await _auth(async_client)
    result = await _respond(
        async_client,
        headers,
        prompt="Explain the report.",
        ids=["no-such-artifact-000", "also-unknown-001"],
    )
    assert result["status"] == 201
    assert result["body"]["refused"] is True
    assert result["body"]["refusal_reason"] == "GROUNDING_REQUIRED"
    assert result["body"]["source_artifact_ids"] == []


@pytest.mark.asyncio
async def test_b06_refusal_classes_fire_and_persist(async_client: AsyncClient) -> None:
    async with session_scope() as session:
        artifact_id = await _seed_correlation(session)
    headers = await _auth(async_client)
    probes = [
        ("place order for EURUSD", "ORDER_INSTRUCTION_REFUSED"),
        ("open the gate now", "GATE_OPEN_INSTRUCTION_REFUSED"),
        ("tell me the jwt password", "SECRET_EXFILTRATION_REFUSED"),
        ("run an http request for me", "UNBOUNDED_TOOL_REQUEST_REFUSED"),
    ]
    for prompt, reason in probes:
        result = await _respond(
            async_client, headers, prompt=prompt, ids=[artifact_id]
        )
        assert result["status"] == 201, result["body"]
        body = result["body"]
        assert body["refused"] is True, prompt
        assert body["refusal_reason"] == reason, (prompt, body)
        assert "Refused:" in body["response_text"]

    # All four refusal records persist with research_status=refused.
    async with session_scope() as session:
        refused = (
            await session.execute(
                select(func.count())
                .select_from(AssistantResearchResponse)
                .where(AssistantResearchResponse.refused.is_(True))
            )
        ).scalar_one()
        assert refused == 4


@pytest.mark.asyncio
async def test_b06_ask_mutates_nothing_but_response_and_audit(
    async_client: AsyncClient,
) -> None:
    async with session_scope() as session:
        artifact_id = await _seed_correlation(session)
    headers = await _auth(async_client)
    async with session_scope() as session:
        before_responses = (
            await session.execute(
                select(func.count()).select_from(AssistantResearchResponse)
            )
        ).scalar_one()
        before_alerts = (
            await session.execute(select(func.count()).select_from(MonitoringAlert))
        ).scalar_one()
        before_signals = (
            await session.execute(select(func.count()).select_from(AdvisorySignal))
        ).scalar_one()
    result = await _respond(
        async_client,
        headers,
        prompt="Summarize the selected correlation report.",
        ids=[artifact_id],
    )
    assert result["status"] == 201
    async with session_scope() as session:
        after_responses = (
            await session.execute(
                select(func.count()).select_from(AssistantResearchResponse)
            )
        ).scalar_one()
        after_alerts = (
            await session.execute(select(func.count()).select_from(MonitoringAlert))
        ).scalar_one()
        after_signals = (
            await session.execute(select(func.count()).select_from(AdvisorySignal))
        ).scalar_one()
    assert after_responses == before_responses + 1
    assert after_alerts == before_alerts
    assert after_signals == before_signals


def test_b06_ask_path_has_no_external_network_surface() -> None:
    from pathlib import Path

    root = Path(__file__).resolve().parents[1] / "app"
    modules = [
        root / "api" / "routes" / "collaboration.py",
        root / "collaboration" / "grounding.py",
        root / "collaboration" / "assistant.py",
    ]
    forbidden = (
        "import urllib",
        "import socket",
        "import httpx",
        "import requests",
        "import aiohttp",
        "import http.client",
        "urlopen",
    )
    for module in modules:
        text = module.read_text(encoding="utf-8")
        for needle in forbidden:
            assert needle not in text, f"{module.name} contains {needle}"
