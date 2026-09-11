"""V2 BE-6 API tests — BO-V2-BE-6-001 T-8 (states, writers, RBAC, labels).

Socket guard active on every test. Endpoint path:
``/api/v1/v2/portfolio-research/*``.
"""

from __future__ import annotations

import math
import socket
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from uuid import uuid4

import pytest
from httpx import AsyncClient
from sqlalchemy import select

from app.auth.security import hash_password
from app.db.models.candle import Candle
from app.db.models.operator import Operator
from app.db.models.v2_audit_event import V2AuditEvent
from app.db.models.v2_lineage_record import V2LineageRecord
from app.db.models.v2_marketdata import V2MdInstrument, V2MdSource
from app.db.models.v2_portfolio import (
    V2PortfolioDefinition,
    V2PortfolioRiskReport,
)
from app.db.session import session_scope
from app.v2.marketdata.seed import V2_MD_INSTRUMENT_SEED, V2_MD_SOURCE_SEED
from app.v2.temporal.validation import utc_now

PR = "/api/v1/v2/portfolio-research"
PASSWORD = "operator-pass-123"
UTC = timezone.utc


@pytest.fixture(autouse=True)
def _socket_guard(monkeypatch):
    def _deny(*_a, **_k):
        raise AssertionError("network attempt during BE-6 test")

    monkeypatch.setattr(socket, "getaddrinfo", _deny)
    monkeypatch.setattr(socket, "create_connection", _deny)


async def _login(client: AsyncClient, username: str,
                 password: str = PASSWORD) -> dict[str, str]:
    r = await client.post("/api/v1/auth/login",
                          json={"username": username, "password": password})
    assert r.status_code == 200, r.text
    return {"Authorization": f"Bearer {r.json()['tokens']['access_token']}"}


async def _admin(client: AsyncClient) -> dict[str, str]:
    return await _login(client, "admin", "admin123")


async def _make_operator() -> str:
    async with session_scope() as session:
        op = Operator(username=f"be6-op-{uuid4().hex[:10]}",
                      hashed_password=hash_password(PASSWORD),
                      role="operator", is_active=True)
        session.add(op)
        await session.flush()
        return op.username


async def _seed_reference() -> None:
    async with session_scope() as session:
        if (await session.execute(select(V2MdSource))).scalars().first():
            return
        for row in V2_MD_SOURCE_SEED:
            session.add(V2MdSource(id=str(uuid4()), created_at=utc_now(), **row))
        for row in V2_MD_INSTRUMENT_SEED:
            session.add(V2MdInstrument(id=str(uuid4()), created_at=utc_now(), **row))


async def _seed_bars(symbols=(("EURUSD", "forex"), ("BTCUSD", "crypto")),
                     n: int = 120) -> None:
    start = datetime(2026, 9, 1, tzinfo=UTC)
    async with session_scope() as session:
        for sym, mc in symbols:
            base = Decimal("1.10") if mc == "forex" else Decimal("50000")
            for i in range(n):
                px = base * (Decimal("1") + Decimal(str(round(0.004 * math.sin(i / 6), 8))))
                session.add(Candle(
                    id=str(uuid4()), market_class=mc, symbol=sym,
                    timeframe="M15",
                    open_time=start + timedelta(minutes=15 * i),
                    open=px, high=px * Decimal("1.001"),
                    low=px * Decimal("0.999"), close=px * Decimal("1.0004"),
                    volume=Decimal("100"), source="live:simulated"))


def _define_body(**over) -> dict:
    body = {
        "portfolio_id": "pf-w",
        "name": "Worked Sample W",
        "allocations": [
            {"instrument_id": "forex.eurusd", "weight": 0.6},
            {"instrument_id": "crypto.btcusd", "weight": 0.4},
        ],
        "data_class": "simulated",
        "assumptions": {"rebalancing": "none", "costs": "excluded"},
    }
    body.update(over)
    return body


async def _defined(client: AsyncClient, headers, **over) -> str:
    r = await client.post(f"{PR}/portfolios/define",
                          json=_define_body(**over), headers=headers)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["accepted"] is True, body["reasons"]
    return body["definition_id"]


# --- define writer ---------------------------------------------------------------


@pytest.mark.asyncio
async def test_define_accepted_hypothetical_basis(
    prepared_db, async_client: AsyncClient
) -> None:
    await _seed_reference()
    headers = await _admin(async_client)
    r = await async_client.post(f"{PR}/portfolios/define",
                                json=_define_body(), headers=headers)
    body = r.json()
    assert body["accepted"] is True
    assert body["basis"] == "hypothetical"  # only possible value
    async with session_scope() as session:
        audits = [a for (a,) in (await session.execute(
            select(V2AuditEvent.action).where(
                V2AuditEvent.domain == "v2.portfolio_research"))).all()]
        assert "portfolio.defined" in audits


@pytest.mark.asyncio
async def test_define_refusals_typed(prepared_db, async_client: AsyncClient) -> None:
    await _seed_reference()
    headers = await _admin(async_client)
    # weight sum violation
    r = await async_client.post(
        f"{PR}/portfolios/define",
        json=_define_body(allocations=[
            {"instrument_id": "forex.eurusd", "weight": 0.7}]),
        headers=headers)
    body = r.json()
    assert body["accepted"] is False
    assert any(x.get("failing") == "weight_sum" for x in body["reasons"])
    # data honesty: historical_real refused
    r = await async_client.post(
        f"{PR}/portfolios/define",
        json=_define_body(data_class="historical_real"), headers=headers)
    assert r.json()["accepted"] is False
    # empty assumptions refused (visibility law)
    r = await async_client.post(
        f"{PR}/portfolios/define",
        json=_define_body(assumptions={}), headers=headers)
    assert r.json()["accepted"] is False
    # unknown instrument refused
    r = await async_client.post(
        f"{PR}/portfolios/define",
        json=_define_body(allocations=[
            {"instrument_id": "forex.nope", "weight": 1.0}]),
        headers=headers)
    assert r.json()["accepted"] is False


@pytest.mark.asyncio
async def test_define_versioning_supersede(
    prepared_db, async_client: AsyncClient
) -> None:
    await _seed_reference()
    headers = await _admin(async_client)
    first = await _defined(async_client, headers)
    # re-define without supersede → refused
    r = await async_client.post(f"{PR}/portfolios/define",
                                json=_define_body(), headers=headers)
    assert r.json()["accepted"] is False
    # supersede → seq 2, forward link to predecessor
    r = await async_client.post(
        f"{PR}/portfolios/define",
        json=_define_body(supersede=True,
                          assumptions={"rebalancing": "none",
                                       "costs": "excluded", "v": 2}),
        headers=headers)
    body = r.json()
    assert body["accepted"] is True and body["record_seq"] == 2
    async with session_scope() as session:
        rows = (await session.execute(
            select(V2PortfolioDefinition).order_by(
                V2PortfolioDefinition.record_seq))).scalars().all()
        assert len(rows) == 2
        assert rows[1].supersedes == first  # C-1 forward vocabulary
    # current_only projection returns only seq 2
    listing = (await async_client.get(
        f"{PR}/portfolios", headers=headers)).json()
    assert listing["total"] == 1
    assert listing["portfolios"][0]["record_seq"] == 2


# --- compute writer + states -------------------------------------------------------


@pytest.mark.asyncio
async def test_compute_available_with_full_contract(
    prepared_db, async_client: AsyncClient
) -> None:
    await _seed_reference()
    await _seed_bars()
    headers = await _admin(async_client)
    did = await _defined(async_client, headers)
    r = await async_client.post(
        f"{PR}/risk-reports/compute",
        json={"portfolio_definition_id": did,
              "scenarios": [{"name": "risk-off",
                             "shocks": {"crypto": -0.3}}]},
        headers=headers)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["status"] == "available"
    assert body["basis_label"] == "hypothetical-research"

    detail = (await async_client.get(
        f"{PR}/risk-reports/{body['report_id']}", headers=headers)).json()
    assert detail["basis_label"] == "hypothetical-research"
    metrics = {m["metric"]: m for m in detail["metrics"]}
    # both VaR methods present, separate
    assert "var_historical" in metrics and "var_parametric_normal" in metrics
    # full contract on every metric
    for m in detail["metrics"]:
        for k in ("metric", "method", "method_citation", "inputs", "value",
                  "uncertainty", "limitations", "time_basis", "insufficient"):
            assert k in m
    assert detail["scenarios"][0]["value"]["scenario"] == "risk-off"
    async with session_scope() as session:
        lineage = (await session.execute(
            select(V2LineageRecord).where(
                V2LineageRecord.artifact_type == "portfolio_risk_report"
            ))).scalars().all()
        assert lineage and lineage[0].input_snapshot_id == detail["inputs_hash"]


@pytest.mark.asyncio
async def test_compute_idempotent_anchor(
    prepared_db, async_client: AsyncClient
) -> None:
    await _seed_reference()
    await _seed_bars()
    headers = await _admin(async_client)
    did = await _defined(async_client, headers)
    payload = {"portfolio_definition_id": did,
               "as_of": "2026-09-03T00:00:00+00:00"}
    first = (await async_client.post(f"{PR}/risk-reports/compute",
                                     json=payload, headers=headers)).json()
    second = (await async_client.post(f"{PR}/risk-reports/compute",
                                      json=payload, headers=headers)).json()
    assert second["reused_existing"] is True
    assert second["report_id"] == first["report_id"]
    async with session_scope() as session:
        count = len((await session.execute(
            select(V2PortfolioRiskReport))).scalars().all())
        assert count == 1


@pytest.mark.asyncio
async def test_compute_unavailable_no_bars(
    prepared_db, async_client: AsyncClient
) -> None:
    await _seed_reference()  # no bars
    headers = await _admin(async_client)
    did = await _defined(async_client, headers)
    r = (await async_client.post(
        f"{PR}/risk-reports/compute",
        json={"portfolio_definition_id": did}, headers=headers)).json()
    assert r["status"] == "unavailable"
    assert set(r["insufficient_metrics"]) >= {"volatility", "drawdown"}


@pytest.mark.asyncio
async def test_compute_superseded_definition_refused(
    prepared_db, async_client: AsyncClient
) -> None:
    await _seed_reference()
    await _seed_bars()
    headers = await _admin(async_client)
    first = await _defined(async_client, headers)
    await _defined(async_client, headers, supersede=True,
                   assumptions={"v": 2})
    r = await async_client.post(
        f"{PR}/risk-reports/compute",
        json={"portfolio_definition_id": first}, headers=headers)
    assert r.status_code == 409
    assert "superseded" in r.json()["detail"].lower()


@pytest.mark.asyncio
async def test_future_as_of_rejected(prepared_db, async_client: AsyncClient) -> None:
    await _seed_reference()
    headers = await _admin(async_client)
    did = await _defined(async_client, headers)
    r = await async_client.post(
        f"{PR}/risk-reports/compute",
        json={"portfolio_definition_id": did,
              "as_of": "2099-01-01T00:00:00+00:00"},
        headers=headers)
    assert r.status_code == 400


# --- RBAC (denied) + hypothetical labels -----------------------------------------------


@pytest.mark.asyncio
async def test_rbac_and_labels(prepared_db, async_client: AsyncClient) -> None:
    await _seed_reference()
    admin = await _admin(async_client)
    operator = await _login(async_client, await _make_operator())
    await _defined(async_client, admin)

    for headers in (admin, operator):
        assert (await async_client.get(f"{PR}/portfolios",
                                       headers=headers)).status_code == 200
        assert (await async_client.get(f"{PR}/risk-reports",
                                       headers=headers)).status_code == 200
    for path, body in (
        (f"{PR}/portfolios/define", _define_body(portfolio_id="pf-x")),
        (f"{PR}/risk-reports/compute", {"portfolio_definition_id": "x"}),
    ):
        r = await async_client.post(path, json=body, headers=operator)
        assert r.status_code == 403
        assert r.json()["detail"] == "Permission denied"
    assert (await async_client.get(f"{PR}/portfolios")).status_code == 401

    # every portfolio response declares the hypothetical basis
    listing = (await async_client.get(f"{PR}/portfolios",
                                      headers=admin)).json()
    assert all(p["basis"] == "hypothetical" for p in listing["portfolios"])


# --- C-1 closure: durable compute-refusal audits (per-event live probes) ---------


async def _refusal_audits() -> list[dict]:
    async with session_scope() as session:
        rows = (await session.execute(
            select(V2AuditEvent).where(
                V2AuditEvent.action == "portfolio_risk.compute.unknown")
        )).scalars().all()
        return [r.details for r in rows]


@pytest.mark.asyncio
async def test_c1_asof_future_refusal_audited(
    prepared_db, async_client: AsyncClient
) -> None:
    await _seed_reference()
    headers = await _admin(async_client)
    did = await _defined(async_client, headers)
    r = await async_client.post(
        f"{PR}/risk-reports/compute",
        json={"portfolio_definition_id": did,
              "as_of": "2099-01-01T00:00:00+00:00"}, headers=headers)
    assert r.status_code == 400
    audits = await _refusal_audits()
    assert any(a.get("refusal_class") == "as_of_in_future" for a in audits)


@pytest.mark.asyncio
async def test_c1_definition_not_found_refusal_audited(
    prepared_db, async_client: AsyncClient
) -> None:
    await _seed_reference()
    headers = await _admin(async_client)
    r = await async_client.post(
        f"{PR}/risk-reports/compute",
        json={"portfolio_definition_id": "ghost"}, headers=headers)
    assert r.status_code == 404
    audits = await _refusal_audits()
    assert any(a.get("refusal_class") == "definition_not_found"
               for a in audits)


@pytest.mark.asyncio
async def test_c1_superseded_refusal_audited(
    prepared_db, async_client: AsyncClient
) -> None:
    await _seed_reference()
    headers = await _admin(async_client)
    first = await _defined(async_client, headers)
    await _defined(async_client, headers, supersede=True,
                   assumptions={"v": 2})
    r = await async_client.post(
        f"{PR}/risk-reports/compute",
        json={"portfolio_definition_id": first}, headers=headers)
    assert r.status_code == 409
    audits = await _refusal_audits()
    assert any(a.get("refusal_class") == "definition_superseded"
               for a in audits)


@pytest.mark.asyncio
async def test_c1_unknown_source_refusal_audited(
    prepared_db, async_client: AsyncClient
) -> None:
    await _seed_reference()
    headers = await _admin(async_client)
    did = await _defined(async_client, headers)
    r = await async_client.post(
        f"{PR}/risk-reports/compute",
        json={"portfolio_definition_id": did, "source_id": "nope.local"},
        headers=headers)
    assert r.status_code == 404
    audits = await _refusal_audits()
    assert any(a.get("refusal_class") == "source_unknown_or_inactive"
               for a in audits)


@pytest.mark.asyncio
async def test_c1_dropped_weight_refused_never_silent(
    prepared_db, async_client: AsyncClient
) -> None:
    """C-1 cluster 2: an instrument resolvable at definition time but
    unresolvable at compute time refuses with `unknown_instrument` and a
    durable audit naming the credited weight — never a silent series drop."""
    await _seed_reference()
    await _seed_bars()
    headers = await _admin(async_client)
    did = await _defined(async_client, headers)
    # simulate registry drift: remove one instrument after definition
    async with session_scope() as session:
        row = (await session.execute(
            select(V2MdInstrument).where(
                V2MdInstrument.instrument_id == "crypto.btcusd")
        )).scalar_one()
        await session.delete(row)
    r = await async_client.post(
        f"{PR}/risk-reports/compute",
        json={"portfolio_definition_id": did}, headers=headers)
    assert r.status_code == 409
    assert "no longer resolvable" in r.json()["detail"]
    audits = await _refusal_audits()
    entry = next(a for a in audits
                 if a.get("refusal_class") == "unknown_instrument")
    assert entry["instrument_id"] == "crypto.btcusd"
    assert entry["credited_weight"] == 0.4  # the dropped weight is NAMED
    # zero side effects: no report row created
    async with session_scope() as session:
        count = len((await session.execute(
            select(V2PortfolioRiskReport))).scalars().all())
        assert count == 0
