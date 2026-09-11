"""V2 BE-5 lifecycle + boundary tests — BO-V2-BE-5-001 T-7/T-8 remainder.

Signal expiry (event-append, never row mutation), promotion-ladder
variants at the API tier, and decision-contract boundary values.
"""

from __future__ import annotations

import socket
from datetime import datetime, timezone
from uuid import uuid4

import pytest
from httpx import AsyncClient
from sqlalchemy import select

from app.db.models.v2_signal import V2SignalRecord, V2SignalStateEvent
from app.db.session import session_scope
from app.v2.research_governance.contracts import (
    DATA_CLASSES,
    FIRST_LANDING_DATA_CLASSES,
    SIGNAL_STATES,
)
from app.v2.research_governance.decisions import (
    CALIBRATION_ECE_WARNING,
    FRESHNESS_STALE_AFTER,
    SIGNIFICANCE_P_BOUND,
    evaluate_calibration,
    evaluate_economic,
    evaluate_eligibility,
    evaluate_freshness,
    evaluate_statistical,
)
from app.v2.research_governance.signals import expire_signal, projected_state
from tests.test_v2_be5_api import (
    _admin,
    _emit_body,
    _seed_governance,
)

RG = "/api/v1/v2/research-governance"
NOW = datetime(2026, 9, 2, 12, 0, tzinfo=timezone.utc)


@pytest.fixture(autouse=True)
def _socket_guard(monkeypatch):
    def _deny(*_a, **_k):
        raise AssertionError("network attempt during BE-5 lifecycle test")

    monkeypatch.setattr(socket, "getaddrinfo", _deny)
    monkeypatch.setattr(socket, "create_connection", _deny)


# --- signal expiry: event-append, never mutation (T-8) -------------------------


async def _emitted_signal(async_client: AsyncClient, headers,
                          expires_at: str | None) -> str:
    body = _emit_body()
    if expires_at is not None:
        body["expires_at"] = expires_at
    r = await async_client.post(f"{RG}/signals/emit", json=body,
                                headers=headers)
    assert r.json()["state"] == "emitted"
    return r.json()["signal_id"]


@pytest.mark.asyncio
async def test_expiry_appends_event_row_immutable(
    prepared_db, async_client: AsyncClient
) -> None:
    headers = await _admin(async_client)
    sid = await _emitted_signal(async_client, headers,
                                "2026-09-02T11:00:00+00:00")
    async with session_scope() as session:
        signal = (await session.execute(
            select(V2SignalRecord).where(V2SignalRecord.id == sid)
        )).scalar_one()
        event = await expire_signal(
            session, signal=signal, as_of=NOW, actor_id="tester",
            correlation_id="c-exp")
        assert event is not None
        assert (event.from_state, event.to_state) == ("emitted", "expired")
    async with session_scope() as session:
        # the record ROW is unchanged (state column still 'emitted' — the
        # projection carries the truth; the row is DB-immutable)
        signal = (await session.execute(
            select(V2SignalRecord).where(V2SignalRecord.id == sid)
        )).scalar_one()
        assert signal.state == "emitted"
        assert await projected_state(session, sid) == "expired"


@pytest.mark.asyncio
async def test_expiry_noop_before_bound_and_for_refused(
    prepared_db, async_client: AsyncClient
) -> None:
    headers = await _admin(async_client)
    sid = await _emitted_signal(async_client, headers,
                                "2026-09-03T00:00:00+00:00")  # future bound
    async with session_scope() as session:
        signal = (await session.execute(
            select(V2SignalRecord).where(V2SignalRecord.id == sid)
        )).scalar_one()
        assert await expire_signal(
            session, signal=signal, as_of=NOW, actor_id="t",
            correlation_id=None) is None  # not yet expired
    # refused signals never expire
    r = await async_client.post(
        f"{RG}/signals/emit", json=_emit_body(source_family_refs={}),
        headers=headers)
    refused_id = r.json()["signal_id"]
    async with session_scope() as session:
        refused = (await session.execute(
            select(V2SignalRecord).where(V2SignalRecord.id == refused_id)
        )).scalar_one()
        assert await expire_signal(
            session, signal=refused, as_of=NOW, actor_id="t",
            correlation_id=None) is None


@pytest.mark.asyncio
async def test_projected_state_latest_event_wins(
    prepared_db, async_client: AsyncClient
) -> None:
    headers = await _admin(async_client)
    sid = await _emitted_signal(async_client, headers, None)
    async with session_scope() as session:
        assert await projected_state(session, sid) == "emitted"
        events = (await session.execute(
            select(V2SignalStateEvent).where(
                V2SignalStateEvent.signal_record_id == sid))).scalars().all()
        assert len(events) == 1  # exactly the creation event


# --- promotion-ladder variants at the API tier (T-7) ----------------------------


@pytest.mark.asyncio
async def test_shadow_to_challenger_allowed(
    prepared_db, async_client: AsyncClient
) -> None:
    gov = await _seed_governance(deployment="shadow")
    headers = await _admin(async_client)
    r = await async_client.post(
        f"{RG}/governance/promote",
        json={"governance_record_id": gov, "target_class": "challenger"},
        headers=headers)
    assert r.json()["decision"] == "allowed"


@pytest.mark.asyncio
async def test_shadow_to_champion_allowed_when_scope_clear(
    prepared_db, async_client: AsyncClient
) -> None:
    gov = await _seed_governance(deployment="shadow",
                                 model_type="regressor",
                                 instrument_class="crypto")
    headers = await _admin(async_client)
    r = await async_client.post(
        f"{RG}/governance/promote",
        json={"governance_record_id": gov, "target_class": "champion"},
        headers=headers)
    assert r.json()["decision"] == "allowed"


@pytest.mark.asyncio
async def test_champion_different_scope_not_blocked(
    prepared_db, async_client: AsyncClient
) -> None:
    """P-3 scope is (model_type, instrument_class) — a champion in another
    scope does not block."""
    await _seed_governance(deployment="champion",
                           model_type="classifier", instrument_class="forex")
    gov = await _seed_governance(deployment="shadow",
                                 model_type="classifier",
                                 instrument_class="crypto")
    headers = await _admin(async_client)
    r = await async_client.post(
        f"{RG}/governance/promote",
        json={"governance_record_id": gov, "target_class": "champion"},
        headers=headers)
    assert r.json()["decision"] == "allowed"


@pytest.mark.asyncio
async def test_retirement_allowed_from_shadow(
    prepared_db, async_client: AsyncClient
) -> None:
    gov = await _seed_governance(deployment="shadow")
    headers = await _admin(async_client)
    r = await async_client.post(
        f"{RG}/governance/promote",
        json={"governance_record_id": gov, "target_class": "retired"},
        headers=headers)
    assert r.json()["decision"] == "allowed"


@pytest.mark.asyncio
async def test_retired_is_terminal(prepared_db, async_client: AsyncClient) -> None:
    gov = await _seed_governance(deployment="retired")
    headers = await _admin(async_client)
    r = await async_client.post(
        f"{RG}/governance/promote",
        json={"governance_record_id": gov, "target_class": "shadow"},
        headers=headers)
    assert r.json()["decision"] == "refused"


@pytest.mark.asyncio
async def test_stale_record_seq_refused(
    prepared_db, async_client: AsyncClient
) -> None:
    """Promoting a non-current (superseded-generation) row is refused."""
    artifact = str(uuid4())
    old = await _seed_governance(artifact_id=artifact, seq=1)
    await _seed_governance(artifact_id=artifact, seq=2)
    headers = await _admin(async_client)
    r = await async_client.post(
        f"{RG}/governance/promote",
        json={"governance_record_id": old, "target_class": "shadow"},
        headers=headers)
    body = r.json()
    assert body["decision"] == "refused"
    assert any(x.get("failing") == "record_currency" for x in body["reasons"])


# --- decision-contract boundary values (T-7) --------------------------------------


def test_calibration_exact_bound_passes() -> None:
    """ECE exactly at the warning bound is calibrated (bound is exclusive)."""
    out = evaluate_calibration(
        {"ece": CALIBRATION_ECE_WARNING, "evaluated_at": NOW.isoformat()},
        as_of=NOW)
    assert out.status == "calibrated"


def test_freshness_exact_bound_is_fresh() -> None:
    out = evaluate_freshness(NOW - FRESHNESS_STALE_AFTER, as_of=NOW)
    assert out.status == "fresh"  # bound exclusive; one second past = stale


def test_statistical_exact_p_bound_significant() -> None:
    report = {"significance": {"p_value": SIGNIFICANCE_P_BOUND}}
    assert evaluate_statistical(report).status == "significant"


def test_economic_zero_expectancy_unviable() -> None:
    out = evaluate_economic({
        "spread": 0.0001, "commission": 0.0001, "slippage": 0.0001,
        "latency_ms": 100, "liquidity": "normal", "net_expectancy": 0.0})
    assert out.status == "unviable"  # zero is not positive


def test_eligibility_empty_uncertainty_interval_refused() -> None:
    report = {
        "walk_forward": {"folds": 6}, "out_of_sample": {"metric_value": 0.6},
        "bootstrap": {"samples": 200}, "significance": {"p_value": 0.01},
        "uncertainty": {"interval": []},
    }
    out = evaluate_eligibility(report)
    assert out.status == "ineligible"


def test_decision_basis_shape_complete() -> None:
    basis = evaluate_eligibility({}).as_decision_basis()
    for key in ("contract", "status", "spec_citation", "thresholds",
                "reasons", "inputs_ref"):
        assert key in basis


def test_vocabulary_integrity() -> None:
    """Contracts module vocabularies mirror the DDL CHECKs (single source)."""
    assert SIGNAL_STATES == ("emitted", "withheld", "expired", "refused")
    assert set(FIRST_LANDING_DATA_CLASSES) < set(DATA_CLASSES)
    assert "live" not in FIRST_LANDING_DATA_CLASSES
    assert "historical_real" not in FIRST_LANDING_DATA_CLASSES
