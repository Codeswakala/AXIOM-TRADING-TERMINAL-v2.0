"""V2 BE-8 order lifecycle + API tests — BO-V2-BE-8-001 T-2/T-5/T-8/T-9/T-16.

E1 end-to-end lifecycle; the S2.6/C-1 hold seam (all four refusal classes
+ C-1d both arms); idempotency (E2); failure taxonomy (E3); RBAC + mode
gate. PAPER-mode app (D-2). Socket guard on every test.
"""

from __future__ import annotations

import socket
from decimal import Decimal
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select

from app.auth.security import hash_password
from app.db.models.operator import Operator
from app.db.models.v2_audit_event import V2AuditEvent
from app.db.models.v2_paper_trading import (
    V2PaperFill,
    V2PaperOrderEvent,
    V2PaperRiskDecision,
)
from app.db.session import session_scope

PT = "/api/v1/v2/paper"
PASSWORD = "operator-pass-123"
ANNEX_COSTS = {
    "spread": {"value": "0.10", "unit": "price", "citation": "band-declared"},
    "commission": {"value": "0.05", "unit": "price",
                   "citation": "band-declared"},
    "slippage": {"value": "0", "unit": "price", "citation": "band-declared"},
}


@pytest.fixture(autouse=True)
def _socket_guard(monkeypatch):
    def _deny(*_a, **_k):
        raise AssertionError("network attempt during BE-8 test")

    monkeypatch.setattr(socket, "getaddrinfo", _deny)
    monkeypatch.setattr(socket, "create_connection", _deny)


@pytest_asyncio.fixture
async def paper_client(prepared_db, monkeypatch):
    """App in PAPER mode (D-2 law) — the band's writer mode."""
    monkeypatch.setenv("AXIOM_V2_MODE", "PAPER")
    from app.core.config import clear_settings_cache
    from app.main import create_app

    clear_settings_cache()
    application = create_app()
    transport = ASGITransport(app=application)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        async with application.router.lifespan_context(application):
            yield ac


@pytest_asyncio.fixture
async def research_client(prepared_db, monkeypatch):
    """App in RESEARCH mode — negative-mode arm (T-2)."""
    monkeypatch.setenv("AXIOM_V2_MODE", "RESEARCH")
    from app.core.config import clear_settings_cache
    from app.main import create_app

    clear_settings_cache()
    application = create_app()
    transport = ASGITransport(app=application)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        async with application.router.lifespan_context(application):
            yield ac


async def _login(client, username, password=PASSWORD):
    r = await client.post("/api/v1/auth/login",
                          json={"username": username, "password": password})
    assert r.status_code == 200, r.text
    return {"Authorization": f"Bearer {r.json()['tokens']['access_token']}"}


async def _admin(client):
    return await _login(client, "admin", "admin123")


async def _operator_headers(client):
    async with session_scope() as session:
        op = Operator(username=f"be8-op-{uuid4().hex[:10]}",
                      hashed_password=hash_password(PASSWORD),
                      role="operator", is_active=True)
        session.add(op)
        await session.flush()
        username = op.username
    return await _login(client, username)


def _bars(closes=None, liquidity="2"):
    closes = closes or ["100", "99", "97", "96", "99", "102", "104", "103",
                        "101", "100"]
    out = []
    for i, close in enumerate(closes):
        c = Decimal(close)
        out.append({"open_time": f"2026-09-01T{i:02d}:00:00+00:00",
                    "open": str(c), "high": str(c + 1), "low": str(c - 1),
                    "close": str(c), "liquidity": liquidity})
    return out


async def _account(client, headers, account_id="acct-1",
                   initial_balance="1000000") -> str:
    """Two-act confirmation flow (S7.2). Returns account row id."""
    payload = {"action": "create", "account_id": account_id,
               "name": "Test", "base_currency": "USD",
               "initial_balance": initial_balance,
               "margin_params": {"margin_rate": "0.5"}}
    r1 = (await client.post(f"{PT}/accounts", headers=headers,
                            json=payload)).json()
    assert r1["outcome"] == "pending_confirmation", r1
    r2 = (await client.post(f"{PT}/accounts/confirm", headers=headers,
                            json={**payload,
                                  "confirmation_ref":
                                  r1["confirmation_ref"]})).json()
    assert r2["outcome"] == "applied", r2
    return r2["record_id"]


async def _order(client, headers, account_id="acct-1", quantity="1",
                 idem=None, bars=None, order_type="market",
                 limit_price=None) -> dict:
    return (await client.post(f"{PT}/orders", headers=headers, json={
        "account_id": account_id, "instrument_id": "forex.eurusd",
        "side": "buy", "order_type": order_type, "quantity": quantity,
        "limit_price": limit_price,
        "idempotency_key": idem or f"k-{uuid4().hex[:8]}",
        "snapshot_ref": "snap-1", "bars": bars or _bars(),
        "window_start": "2026-09-01T00:00:00+00:00",
        "window_end": "2026-09-01T10:00:00+00:00"})).json()


# --- E1: end-to-end lifecycle ----------------------------------------------------


@pytest.mark.asyncio
async def test_e1_full_lifecycle_draft_to_settled(paper_client):
    headers = await _admin(paper_client)
    await _account(paper_client, headers)
    placed = await _order(paper_client, headers)
    assert placed["outcome"] == "registered"
    assert placed["decision"] == "pass"
    assert placed["state"] == "risk_passed"
    order_id = placed["order_id"]

    run = (await paper_client.post(
        f"{PT}/orders/{order_id}/run", headers=headers,
        json={"bars": _bars(), "cost_model": ANNEX_COSTS})).json()
    assert run["outcome"] == "filled", run
    assert run["state"] == "settled"
    for f in run["fills"]:
        assert f["fill_class"] == "paper_simulated"
    assert "paper-simulated" in run["disclaimer"]

    events = (await paper_client.get(
        f"{PT}/orders/{order_id}/events", headers=headers)).json()["events"]
    chain = [(e["from_state"], e["to_state"]) for e in events]
    assert chain == [("draft", "validated"), ("validated", "risk_passed"),
                     ("risk_passed", "executing"), ("executing", "filled"),
                     ("filled", "settled")]

    balances = (await paper_client.get(
        f"{PT}/balances", headers=headers)).json()["balances"]
    assert balances, "balance snapshot written"
    recons = (await paper_client.get(
        f"{PT}/reconciliations", headers=headers)).json()["reconciliations"]
    assert recons and recons[0]["outcome"] == "consistent"

    async with session_scope() as session:
        audits = {a for (a,) in (await session.execute(
            select(V2AuditEvent.action).where(
                V2AuditEvent.domain == "v2.paper_trading"))).all()}
    for expected in ("paper.account.created", "paper.risk.passed",
                     "paper.order.executed",
                     "paper.reconciliation.completed"):
        assert expected in audits, expected


@pytest.mark.asyncio
async def test_e1_partial_fill_voided_remainder(paper_client):
    """ANNEX-P Case A through the API: 2 fills @97.65, remainder voided."""
    headers = await _admin(paper_client)
    await _account(paper_client, headers)
    placed = await _order(paper_client, headers, quantity="5",
                          order_type="limit", limit_price="97.5")
    assert placed["decision"] == "pass"
    run = (await paper_client.post(
        f"{PT}/orders/{placed['order_id']}/run", headers=headers,
        json={"bars": _bars(), "cost_model": ANNEX_COSTS})).json()
    assert run["outcome"] == "partially_filled"
    assert run["state"] == "settled"
    assert len(run["fills"]) == 2
    assert all(f["effective_price"] == "97.65" for f in run["fills"])
    events = (await paper_client.get(
        f"{PT}/orders/{placed['order_id']}/events",
        headers=headers)).json()["events"]
    settled = [e for e in events if e["event_class"] == "order.settled"]
    assert settled and settled[0]["details"]["voided_remainder"] == "1"


# --- E2: idempotency / replay / race ----------------------------------------------


@pytest.mark.asyncio
async def test_e2_idempotency_key_reuse(paper_client):
    headers = await _admin(paper_client)
    await _account(paper_client, headers)
    first = await _order(paper_client, headers, idem="idem-1")
    second = await _order(paper_client, headers, idem="idem-1")
    assert first["outcome"] == "registered"
    assert second["outcome"] == "reused"
    assert second["order_id"] == first["order_id"]
    async with session_scope() as session:
        decisions = list((await session.execute(
            select(V2PaperRiskDecision).where(
                V2PaperRiskDecision.intent_id == first["order_id"])
        )).scalars().all())
        assert len(decisions) == 1  # exactly-once risk evaluation held
        audits = [a for (a,) in (await session.execute(
            select(V2AuditEvent.action).where(
                V2AuditEvent.action == "paper.order.reused"))).all()]
        assert audits


@pytest.mark.asyncio
async def test_e2_rerun_converges_no_second_fill_set(paper_client):
    headers = await _admin(paper_client)
    await _account(paper_client, headers)
    placed = await _order(paper_client, headers)
    run1 = (await paper_client.post(
        f"{PT}/orders/{placed['order_id']}/run", headers=headers,
        json={"bars": _bars(), "cost_model": ANNEX_COSTS})).json()
    assert run1["outcome"] == "filled"
    run2 = (await paper_client.post(
        f"{PT}/orders/{placed['order_id']}/run", headers=headers,
        json={"bars": _bars(), "cost_model": ANNEX_COSTS})).json()
    assert run2["outcome"] == "refused"  # settled: only risk_passed runs
    async with session_scope() as session:
        fills = list((await session.execute(
            select(V2PaperFill).where(
                V2PaperFill.intent_id == placed["order_id"])
        )).scalars().all())
        assert len(fills) == 1  # no second artifact set


# --- E3: failure taxonomy ---------------------------------------------------------


@pytest.mark.asyncio
async def test_e3_risk_block_limit_named_and_measured(paper_client):
    headers = await _admin(paper_client)
    await _account(paper_client, headers)
    placed = await _order(paper_client, headers, quantity="99999999")
    assert placed["decision"] == "block"
    assert placed["state"] == "risk_blocked"
    assert any(r["failing"] == "max_order_quantity"
               for r in placed["reasons"])
    async with session_scope() as session:
        d = (await session.execute(
            select(V2PaperRiskDecision).where(
                V2PaperRiskDecision.intent_id == placed["order_id"])
        )).scalar_one()
        assert d.decision == "block"
        assert d.confirmation_ref is None  # C-1d: no ref minted
        assert d.evaluated_limits["max_order_quantity"]["verdict"] == "fail"
        assert d.risk_config_version == "prc-1"


@pytest.mark.asyncio
async def test_e3_validation_rejected(paper_client):
    headers = await _admin(paper_client)
    await _account(paper_client, headers)
    r = (await paper_client.post(f"{PT}/orders", headers=headers, json={
        "account_id": "acct-1", "instrument_id": "forex.eurusd",
        "side": "hold-me", "order_type": "market", "quantity": "-1",
        "idempotency_key": "k-bad", "snapshot_ref": "s",
        "bars": []})).json()
    assert r["outcome"] == "rejected"
    failing = {x["failing"] for x in r["reasons"]}
    assert {"side", "quantity", "bars"} <= failing


@pytest.mark.asyncio
async def test_e3_expired_window_exhaustion(paper_client):
    headers = await _admin(paper_client)
    await _account(paper_client, headers)
    placed = await _order(paper_client, headers, order_type="limit",
                          limit_price="50", quantity="1")
    assert placed["decision"] == "pass"
    run = (await paper_client.post(
        f"{PT}/orders/{placed['order_id']}/run", headers=headers,
        json={"bars": _bars(), "cost_model": ANNEX_COSTS})).json()
    assert run["outcome"] == "expired"
    assert run["state"] == "expired"


@pytest.mark.asyncio
async def test_e3_quarantine_on_snapshot_tamper(paper_client):
    """S2.5/Q6: content mismatch at run => quarantined_unknown terminal."""
    headers = await _admin(paper_client)
    await _account(paper_client, headers)
    placed = await _order(paper_client, headers)
    tampered = _bars(closes=["50"] * 10)
    run = (await paper_client.post(
        f"{PT}/orders/{placed['order_id']}/run", headers=headers,
        json={"bars": tampered, "cost_model": ANNEX_COSTS})).json()
    assert run["outcome"] == "quarantined"
    assert run["state"] == "quarantined_unknown"
    async with session_scope() as session:
        audits = [a for (a,) in (await session.execute(
            select(V2AuditEvent.action).where(
                V2AuditEvent.action == "paper.order.quarantined"))).all()]
        assert audits


# --- C-1 hold seam (S2.6) ---------------------------------------------------------


HELD_BARS = None  # set per call: the SAME bars must be pinned and replayed


async def _held_order(client, headers, bars=None) -> dict:
    """Notional inside the hold band: [80k, 100k] => qty 850 @ ~100.
    The bars given here are content-pinned on the intent (S4.1) — any
    later run MUST replay the same bytes or be quarantined."""
    placed = await _order(client, headers, quantity="850", bars=bars)
    assert placed["decision"] == "hold", placed
    assert placed["state"] == "risk_hold"
    assert placed["confirmation_ref"]
    return placed


@pytest.mark.asyncio
async def test_c1_hold_confirm_then_execute(paper_client):
    headers = await _admin(paper_client)
    await _account(paper_client, headers)
    liquid_bars = _bars(liquidity="1000")  # pinned at placement (S4.1)
    held = await _held_order(paper_client, headers, bars=liquid_bars)
    confirmed = (await paper_client.post(
        f"{PT}/orders/confirm", headers=headers,
        json={"order_id": held["order_id"],
              "confirmation_ref": held["confirmation_ref"],
              "resolve_to": "confirm"})).json()
    assert confirmed["outcome"] == "applied"
    assert confirmed["state"] == "risk_passed"
    run = (await paper_client.post(
        f"{PT}/orders/{held['order_id']}/run", headers=headers,
        json={"bars": liquid_bars,  # same pinned bytes replayed
              "cost_model": ANNEX_COSTS})).json()
    assert run["outcome"] == "filled"
    async with session_scope() as session:
        d = (await session.execute(
            select(V2PaperRiskDecision).where(
                V2PaperRiskDecision.intent_id == held["order_id"])
        )).scalar_one()
        assert d.decision == "hold"  # the row NEVER mutates (C-1a)
        events = list((await session.execute(
            select(V2PaperOrderEvent).where(
                V2PaperOrderEvent.intent_id == held["order_id"])
        )).scalars().all())
        confirms = [e for e in events if e.event_class == "hold.confirmed"]
        assert len(confirms) == 1
        assert confirms[0].details["confirmation_ref"] == d.confirmation_ref


@pytest.mark.asyncio
async def test_c1_hold_cancel(paper_client):
    headers = await _admin(paper_client)
    await _account(paper_client, headers)
    held = await _held_order(paper_client, headers)
    cancelled = (await paper_client.post(
        f"{PT}/orders/confirm", headers=headers,
        json={"order_id": held["order_id"],
              "confirmation_ref": held["confirmation_ref"],
              "resolve_to": "cancel"})).json()
    assert cancelled["outcome"] == "applied"
    assert cancelled["state"] == "cancelled"
    async with session_scope() as session:
        audits = [a for (a,) in (await session.execute(
            select(V2AuditEvent.action).where(
                V2AuditEvent.action == "paper.order.hold_cancelled"))).all()]
        assert audits


@pytest.mark.asyncio
async def test_c1_four_refusal_classes(paper_client):
    """C-1b.4: double-confirm, wrong-ref, stale-after-cancel,
    not-confirmable — each typed + durably audited."""
    headers = await _admin(paper_client)
    await _account(paper_client, headers)

    # wrong-ref
    held = await _held_order(paper_client, headers)
    r = (await paper_client.post(
        f"{PT}/orders/confirm", headers=headers,
        json={"order_id": held["order_id"], "confirmation_ref": "forged",
              "resolve_to": "confirm"})).json()
    assert r["outcome"] == "refused"
    assert r["reasons"][0]["failing"] == "paper.confirmation.ref_mismatch"

    # double-confirm
    ok = (await paper_client.post(
        f"{PT}/orders/confirm", headers=headers,
        json={"order_id": held["order_id"],
              "confirmation_ref": held["confirmation_ref"],
              "resolve_to": "confirm"})).json()
    assert ok["outcome"] == "applied"
    r = (await paper_client.post(
        f"{PT}/orders/confirm", headers=headers,
        json={"order_id": held["order_id"],
              "confirmation_ref": held["confirmation_ref"],
              "resolve_to": "confirm"})).json()
    assert r["outcome"] == "refused"
    assert r["reasons"][0]["failing"] == \
        "paper.confirmation.already_consumed"

    # stale-after-cancel
    held2 = await _held_order(paper_client, headers)
    (await paper_client.post(
        f"{PT}/orders/confirm", headers=headers,
        json={"order_id": held2["order_id"],
              "confirmation_ref": held2["confirmation_ref"],
              "resolve_to": "cancel"})).json()
    r = (await paper_client.post(
        f"{PT}/orders/confirm", headers=headers,
        json={"order_id": held2["order_id"],
              "confirmation_ref": held2["confirmation_ref"],
              "resolve_to": "confirm"})).json()
    assert r["outcome"] == "refused"
    assert r["reasons"][0]["failing"] == "paper.confirmation.cancelled"

    # not-confirmable (pass decision)
    passed = await _order(paper_client, headers)
    assert passed["decision"] == "pass"
    r = (await paper_client.post(
        f"{PT}/orders/confirm", headers=headers,
        json={"order_id": passed["order_id"], "confirmation_ref": "any",
              "resolve_to": "confirm"})).json()
    assert r["outcome"] == "refused"
    assert r["reasons"][0]["failing"] == \
        "paper.confirmation.not_confirmable"

    async with session_scope() as session:
        refusals = [a for (a,) in (await session.execute(
            select(V2AuditEvent.action).where(
                V2AuditEvent.action == "paper.order.confirm_refused"))).all()]
        assert len(refusals) >= 4  # every refusal durably audited


@pytest.mark.asyncio
async def test_c1d_block_unreachable_by_confirmation(paper_client):
    """C-1d both arms: (1) confirm on blocked => not_confirmable;
    (2) forged risk_blocked->executing append refused typed."""
    headers = await _admin(paper_client)
    await _account(paper_client, headers)
    blocked = await _order(paper_client, headers, quantity="99999999")
    assert blocked["decision"] == "block"

    # arm 1: confirmation attempt
    r = (await paper_client.post(
        f"{PT}/orders/confirm", headers=headers,
        json={"order_id": blocked["order_id"], "confirmation_ref": "any",
              "resolve_to": "confirm"})).json()
    assert r["outcome"] == "refused"
    assert r["reasons"][0]["failing"] == \
        "paper.confirmation.not_confirmable"

    # arm 2: forged transition (vocabulary content assertion + append refusal)
    from app.v2.paper_trading.contracts import LEGAL_TRANSITIONS
    assert not any(f == "risk_blocked" for f, _t in LEGAL_TRANSITIONS)
    from app.v2.paper_trading.orders import append_event
    async with session_scope() as session:
        outcome = await append_event(
            session, intent_row_id=blocked["order_id"],
            from_state="risk_blocked", to_state="executing",
            event_class="execution.started", details={}, actor_id="t",
            mode="PAPER", operator_id="t", correlation_id=None,
            data_class="simulated")
        assert outcome.refused
        assert outcome.reasons[0]["failing"] == "transition"

    # run also refused via may_execute
    run = (await paper_client.post(
        f"{PT}/orders/{blocked['order_id']}/run", headers=headers,
        json={"bars": _bars(), "cost_model": ANNEX_COSTS})).json()
    assert run["outcome"] == "refused"


@pytest.mark.asyncio
async def test_cancel_semantics(paper_client):
    """Terminal-cancel refused; hold-cancel redirected to the C-1 act."""
    headers = await _admin(paper_client)
    await _account(paper_client, headers)
    placed = await _order(paper_client, headers)
    run = (await paper_client.post(
        f"{PT}/orders/{placed['order_id']}/run", headers=headers,
        json={"bars": _bars(), "cost_model": ANNEX_COSTS})).json()
    assert run["state"] == "settled"
    r = (await paper_client.post(
        f"{PT}/orders/cancel", headers=headers,
        json={"order_id": placed["order_id"]})).json()
    assert r["outcome"] == "refused"  # terminal

    held = await _held_order(paper_client, headers)
    r = (await paper_client.post(
        f"{PT}/orders/cancel", headers=headers,
        json={"order_id": held["order_id"]})).json()
    assert r["outcome"] == "refused"  # holds resolve via confirmation act
    assert "confirmation mechanism" in r["reasons"][0]["note"]


# --- T-2: mode gate / T-16: RBAC --------------------------------------------------


@pytest.mark.asyncio
async def test_t2_paper_writers_refused_outside_paper_mode(research_client):
    headers = await _admin(research_client)
    r = await research_client.post(f"{PT}/accounts", headers=headers, json={
        "action": "create", "account_id": "a", "name": "x",
        "base_currency": "USD", "initial_balance": "1"})
    assert r.status_code == 403
    assert "not permitted in this mode" in r.json()["detail"]
    r = await research_client.post(f"{PT}/orders", headers=headers, json={
        "account_id": "a", "instrument_id": "x", "side": "buy",
        "quantity": "1", "idempotency_key": "k", "snapshot_ref": "s"})
    assert r.status_code == 403


@pytest.mark.asyncio
async def test_t16_rbac_denied_and_unauthenticated(paper_client):
    headers = await _operator_headers(paper_client)
    # operator lacks all v2.paper.* (admin-only v1 surface)
    for path, body in ((f"{PT}/accounts", {"action": "create",
                                           "account_id": "a", "name": "x",
                                           "base_currency": "USD",
                                           "initial_balance": "1"}),
                       (f"{PT}/orders", {"account_id": "a",
                                         "instrument_id": "x",
                                         "side": "buy", "quantity": "1",
                                         "idempotency_key": "k",
                                         "snapshot_ref": "s"}),
                       (f"{PT}/orders/cancel", {"order_id": "x"})):
        r = await paper_client.post(path, headers=headers, json=body)
        assert r.status_code == 403
        assert r.json()["detail"] == "Permission denied"  # generic (BE-1)
    r = await paper_client.get(f"{PT}/orders")
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_envelope_and_disclaimer_on_reads(paper_client):
    headers = await _admin(paper_client)
    r = (await paper_client.get(f"{PT}/fills", headers=headers)).json()
    for key in ("mode", "correlation_id", "timestamp", "disclaimer"):
        assert key in r
    assert "never broker-confirmed" in r["disclaimer"]
