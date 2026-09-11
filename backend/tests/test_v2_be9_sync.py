"""V2 BE-9 sync/reconcile/API tests — BO-V2-BE-9-001 T-2/T-10/T-12/T-13/T-15.

Fixture provider (MetaTrader5-shaped, zero network); recorded practice-
environment payload fixtures (BE-3 P1 fixture law). Socket guard on every
test. The binding assertion is bypassed at the fixture seam ONLY (the
fixture pins its own provenance; the real leg's binding gate is unit-
tested in test_v2_be9_contract).
"""

from __future__ import annotations

import socket
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select

from app.auth.security import hash_password
from app.db.models.operator import Operator
from app.db.models.v2_audit_event import V2AuditEvent
from app.db.models.v2_broker_read import (
    V2BrokerDiscrepancy,
    V2BrokerFill,
    V2BrokerReconcileRun,
    V2BrokerSyncRun,
)
from app.db.session import session_scope
from app.v2.broker_read.contract import (
    BrokerAccountsPage,
    BrokerInstrumentsPage,
    BrokerOrdersPage,
    BrokerPositionsPage,
    BrokerRefused,
    BrokerSummaryPage,
    BrokerTransactionsPage,
    PageProvenance,
)

BR = "/api/v1/v2/broker"
PASSWORD = "operator-pass-123"


@pytest.fixture(autouse=True)
def _socket_guard(monkeypatch):
    def _deny(*_a, **_k):
        raise AssertionError("network attempt during BE-9 test")

    monkeypatch.setattr(socket, "getaddrinfo", _deny)
    monkeypatch.setattr(socket, "create_connection", _deny)


def _prov(**kw) -> PageProvenance:
    base = {"provider_id": "exness_mt5_demo",
            "server_hostname": "Exness-MT5Trial9",
            "account_number": "111222", "environment": "practice",
            "fetch_basis": "server_time",
            "fetched_at": "2026-09-05T10:00:00+00:00"}
    base.update(kw)
    return PageProvenance(**base)


class FixtureProvider:
    """Recorded practice-environment payloads; deterministic; no network."""

    def __init__(self, balance="10000.00", fail_page=None,
                 terminal_down=False, extra_fill=False):
        self.balance = balance
        self.fail_page = fail_page
        self.terminal_down = terminal_down
        self.extra_fill = extra_fill

    def _gate(self, name):
        if self.terminal_down:
            raise BrokerRefused("broker.terminal.unavailable", [
                {"failing": "terminal", "note": "fixture: E-ENV-1 regime"}])
        if self.fail_page == name:
            raise BrokerRefused("broker.payload.invalid", [
                {"failing": name, "note": "fixture: truncated page"}])

    async def read_accounts(self):
        self._gate("accounts")
        return BrokerAccountsPage(records=(
            {"broker_account_ext_id": "111222", "alias": "demo-std",
             "currency": "USD", "environment": "practice",
             "read_only_login": True},), provenance=_prov())

    async def read_account_summary(self):
        self._gate("balances")
        return BrokerSummaryPage(records=(
            {"broker_account_ext_id": "111222", "balance": self.balance,
             "margin_used": "0", "margin_available": self.balance,
             "unrealized_pl": "0", "currency": "USD"},),
            provenance=_prov())

    async def read_positions(self):
        self._gate("positions")
        return BrokerPositionsPage(records=(
            {"broker_account_ext_id": "111222",
             "instrument_ext_id": "EURUSD", "units_long": "1",
             "units_short": "0", "avg_price_long": "1.1000",
             "avg_price_short": "0", "position_ext_id": "500001"},),
            provenance=_prov())

    async def read_orders(self):
        self._gate("orders")
        return BrokerOrdersPage(records=(), provenance=_prov())

    async def read_transactions(self, window_start, window_end, page_index):
        self._gate("fills")
        records = [{"transaction_ext_id": "900001",
                    "broker_account_ext_id": "111222",
                    "tx_type_ext": "deal_buy",
                    "instrument_ext_id": "EURUSD", "units": "1",
                    "price": "1.1000",
                    "tx_time_ext": "2026-09-05T09:00:00+00:00"}]
        if self.extra_fill:
            records.append({"transaction_ext_id": "900002",
                            "broker_account_ext_id": "111222",
                            "tx_type_ext": "deal_sell",
                            "instrument_ext_id": "EURUSD", "units": "1",
                            "price": "1.2000",
                            "tx_time_ext": "2026-09-05T09:30:00+00:00"})
        # only the first window carries fills in the fixture
        if page_index > 0:
            records = []
        return BrokerTransactionsPage(
            records=tuple(records),
            provenance=_prov(window_start=window_start,
                             window_end=window_end,
                             page_index=page_index))

    async def read_instrument_permissions(self):
        self._gate("instrument_permissions")
        return BrokerInstrumentsPage(records=(
            {"broker_account_ext_id": "111222",
             "instrument_ext_id": "EURUSD",
             "visibility": {"visible": True,
                            "trade_mode": "SYMBOL_TRADE_MODE_FULL"},
             "display_name": "Euro vs US Dollar"},), provenance=_prov())


@pytest_asyncio.fixture
async def broker_client(prepared_db, monkeypatch):
    monkeypatch.setenv("AXIOM_V2_MODE", "RESEARCH")
    from app.core.config import clear_settings_cache
    from app.main import create_app
    from app.v2.broker_read.api import _TEST_PROVIDER

    clear_settings_cache()
    _TEST_PROVIDER["instance"] = FixtureProvider()
    application = create_app()
    transport = ASGITransport(app=application)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        async with application.router.lifespan_context(application):
            yield ac
    _TEST_PROVIDER["instance"] = None


async def _login(client, username, password=PASSWORD):
    r = await client.post("/api/v1/auth/login",
                          json={"username": username, "password": password})
    assert r.status_code == 200, r.text
    return {"Authorization": f"Bearer {r.json()['tokens']['access_token']}"}


async def _admin(client):
    return await _login(client, "admin", "admin123")


def _set_provider(**kw):
    from app.v2.broker_read.api import _TEST_PROVIDER
    _TEST_PROVIDER["instance"] = FixtureProvider(**kw)


# --- T-15/T-10: sync law ------------------------------------------------------------


@pytest.mark.asyncio
async def test_sync_complete_and_projections_land(broker_client):
    headers = await _admin(broker_client)
    r = (await broker_client.post(f"{BR}/sync", headers=headers,
                                  json={})).json()
    assert r["outcome"] == "complete", r
    assert len(r["result_digest"]) == 64
    accounts = (await broker_client.get(
        f"{BR}/accounts", headers=headers)).json()
    assert accounts["accounts"][0]["read_only_login"] is True
    assert accounts["accounts"][0]["environment"] == "practice"
    assert accounts["staleness"] == "fresh"
    fills = (await broker_client.get(f"{BR}/fills",
                                     headers=headers)).json()["fills"]
    assert len(fills) == 1 and fills[0]["transaction_ext_id"] == "900001"


@pytest.mark.asyncio
async def test_t10_replay_x3_equal_digests_and_fill_dedupe(broker_client):
    headers = await _admin(broker_client)
    digests = []
    for _ in range(3):
        r = (await broker_client.post(f"{BR}/sync", headers=headers,
                                      json={})).json()
        assert r["outcome"] == "complete"
        digests.append(r["result_digest"])
    assert digests[0] == digests[1] == digests[2]  # x3 replay law
    async with session_scope() as session:
        fills = list((await session.execute(
            select(V2BrokerFill))).scalars().all())
        assert len(fills) == 1  # anchor dedupe across three runs
        runs = list((await session.execute(
            select(V2BrokerSyncRun))).scalars().all())
        assert len(runs) == 3   # three lineage rows, one artifact set
        reused = [a for (a,) in (await session.execute(
            select(V2AuditEvent.action).where(
                V2AuditEvent.action == "broker.fill.reused"))).all()]
        assert reused


@pytest.mark.asyncio
async def test_t15_partial_page_lands_nothing(broker_client):
    headers = await _admin(broker_client)
    _set_provider(fail_page="positions")
    r = (await broker_client.post(f"{BR}/sync", headers=headers,
                                  json={})).json()
    assert r["outcome"] in ("partial_refused", "failed")
    assert r["refusal_class"] == "broker.payload.invalid"
    async with session_scope() as session:
        fills = list((await session.execute(
            select(V2BrokerFill))).scalars().all())
        assert fills == []  # a half-fetched page cannot half-land
        run = (await session.execute(
            select(V2BrokerSyncRun))).scalars().first()
        assert run.outcome in ("partial_refused", "failed")
        assert run.refusal["class"] == "broker.payload.invalid"


@pytest.mark.asyncio
async def test_e_env1_terminal_unavailable_typed(broker_client):
    headers = await _admin(broker_client)
    _set_provider(terminal_down=True)
    r = (await broker_client.post(f"{BR}/sync", headers=headers,
                                  json={})).json()
    assert r["outcome"] == "failed"
    assert r["refusal_class"] == "broker.terminal.unavailable"
    health = (await broker_client.get(f"{BR}/health",
                                      headers=headers)).json()
    assert health["terminal"] == "not_running"
    assert health["status"] == "terminal_down"
    assert health["last_refusal_class"] == "broker.terminal.unavailable"


# --- T-12/T-13: reconciliation + discrepancies ---------------------------------------


@pytest.mark.asyncio
async def test_t12_clean_run_evidenced(broker_client):
    headers = await _admin(broker_client)
    sync = (await broker_client.post(f"{BR}/sync", headers=headers,
                                     json={})).json()
    rec = (await broker_client.post(
        f"{BR}/reconcile", headers=headers,
        json={"sync_run_id": sync["sync_run_id"]})).json()
    assert rec["outcome"] == "clean"
    assert rec["discrepancy_count"] == 0
    assert len(rec["broker_side_digest"]) == 64
    assert len(rec["projection_side_digest"]) == 64
    async with session_scope() as session:
        row = (await session.execute(
            select(V2BrokerReconcileRun))).scalars().first()
        assert row.outcome == "clean"
        assert row.discrepancy_count == 0
        assert row.broker_side_digest and row.projection_side_digest


@pytest.mark.asyncio
async def test_t13_seeded_mismatch_detected_and_lifecycle(broker_client):
    headers = await _admin(broker_client)
    sync = (await broker_client.post(f"{BR}/sync", headers=headers,
                                     json={})).json()
    # broker side moves: balance changed + a new fill AXIOM lacks
    _set_provider(balance="10500.00", extra_fill=True)
    rec = (await broker_client.post(
        f"{BR}/reconcile", headers=headers,
        json={"sync_run_id": sync["sync_run_id"]})).json()
    assert rec["outcome"] == "discrepant"
    assert rec["discrepancy_count"] >= 2  # amount_mismatch + missing_in_axiom
    async with session_scope() as session:
        classes = {d.discrepancy_class for d in (await session.execute(
            select(V2BrokerDiscrepancy))).scalars().all()}
        assert "amount_mismatch" in classes
        assert "missing_in_axiom" in classes
        disc_id = (await session.execute(
            select(V2BrokerDiscrepancy))).scalars().first().discrepancy_id

    # lifecycle: detected -> triaged -> owned -> dismissed_with_reason
    for to_state, extra in (("triaged", {}), ("owned", {}),
                            ("dismissed_with_reason",
                             {"reason": "demo-account fixture variance"})):
        r = (await broker_client.post(
            f"{BR}/discrepancies/transition", headers=headers,
            json={"discrepancy_id": disc_id, "to_state": to_state,
                  **extra})).json()
        assert r["outcome"] == "applied", (to_state, r)

    # refusals: illegal jump + dismissal without reason
    r = (await broker_client.post(
        f"{BR}/discrepancies/transition", headers=headers,
        json={"discrepancy_id": disc_id, "to_state": "owned"})).json()
    assert r["outcome"] == "refused"  # terminal already

    async with session_scope() as session:
        audits = {a for (a,) in (await session.execute(
            select(V2AuditEvent.action).where(
                V2AuditEvent.domain == "v2.broker_read"))).all()}
    for expected in ("broker.discrepancy.triaged",
                     "broker.discrepancy.owned",
                     "broker.discrepancy.dismissed_with_reason",
                     "broker.discrepancy.transition_refused"):
        assert expected in audits, expected


@pytest.mark.asyncio
async def test_t13_dismissal_without_reason_refused(broker_client):
    headers = await _admin(broker_client)
    sync = (await broker_client.post(f"{BR}/sync", headers=headers,
                                     json={})).json()
    _set_provider(balance="9999.99")
    (await broker_client.post(
        f"{BR}/reconcile", headers=headers,
        json={"sync_run_id": sync["sync_run_id"]})).json()
    async with session_scope() as session:
        disc_id = (await session.execute(
            select(V2BrokerDiscrepancy))).scalars().first().discrepancy_id
    for to_state in ("triaged", "owned"):
        (await broker_client.post(
            f"{BR}/discrepancies/transition", headers=headers,
            json={"discrepancy_id": disc_id, "to_state": to_state})).json()
    r = (await broker_client.post(
        f"{BR}/discrepancies/transition", headers=headers,
        json={"discrepancy_id": disc_id,
              "to_state": "dismissed_with_reason"})).json()
    assert r["outcome"] == "refused"
    assert r["reasons"][0]["failing"] == "reason"


# --- Q7: degraded reads / staleness ---------------------------------------------------


@pytest.mark.asyncio
async def test_q7_no_data_and_last_good_banner(broker_client):
    headers = await _admin(broker_client)
    accounts = (await broker_client.get(
        f"{BR}/accounts", headers=headers)).json()
    assert accounts["staleness"] == "no_data"  # nothing has ever landed
    (await broker_client.post(f"{BR}/sync", headers=headers, json={}))
    _set_provider(terminal_down=True)  # provider dies AFTER a good sync
    (await broker_client.post(f"{BR}/sync", headers=headers, json={}))
    accounts = (await broker_client.get(
        f"{BR}/accounts", headers=headers)).json()
    assert accounts["accounts"]  # last-good still served
    health = (await broker_client.get(f"{BR}/health",
                                      headers=headers)).json()
    assert health["status"] == "terminal_down"  # health tells the truth


# --- T-4/T-8: RBAC + census + blindness ------------------------------------------------


@pytest.mark.asyncio
async def test_rbac_denied_and_unauthenticated(broker_client):
    async with session_scope() as session:
        op = Operator(username=f"be9-op-{uuid4().hex[:10]}",
                      hashed_password=hash_password(PASSWORD),
                      role="operator", is_active=True)
        session.add(op)
        await session.flush()
        username = op.username
    headers = await _login(broker_client, username)
    for path, body in ((f"{BR}/sync", {}),
                       (f"{BR}/discrepancies/transition",
                        {"discrepancy_id": "x", "to_state": "triaged"}),
                       (f"{BR}/vault", {"action": "unlock"})):
        r = await broker_client.post(path, headers=headers, json=body)
        assert r.status_code == 403
        assert r.json()["detail"] == "Permission denied"  # generic (BE-1)
    r = await broker_client.get(f"{BR}/accounts", headers=headers)
    assert r.status_code == 403  # admin-only v1 surface
    r = await broker_client.get(f"{BR}/accounts")
    assert r.status_code == 401


def test_t4_api_surface_census_exact():
    from app.v2.broker_read.api import router

    posts, gets, others = set(), set(), set()
    for route in router.routes:
        methods = route.methods - {"HEAD", "OPTIONS"}
        if "POST" in methods:
            posts.add(route.path)
        if "GET" in methods:
            gets.add(route.path)
        for m in methods - {"POST", "GET"}:
            others.add((m, route.path))
    assert posts == {"/broker/sync", "/broker/reconcile",
                     "/broker/discrepancies/transition", "/broker/vault"}
    assert gets == {"/broker/accounts", "/broker/balances",
                    "/broker/positions", "/broker/orders", "/broker/fills",
                    "/broker/instrument-permissions",
                    "/broker/discrepancies", "/broker/health"}
    assert others == set()  # zero PUT/PATCH/DELETE (T-4)


@pytest.mark.asyncio
async def test_t8_payload_echo_canary(broker_client):
    """A provider-smuggled token lands ONLY in the lawful projection row —
    never in health output or audit rows."""
    canary = "smuggled-canary-7c2fa91d"
    headers = await _admin(broker_client)

    class SmugglingProvider(FixtureProvider):
        async def read_orders(self):
            return BrokerOrdersPage(records=(
                {"order_ext_id": "666", "broker_account_ext_id": "111222",
                 "order_state_ext": "placed",
                 "payload": {"note": canary}},), provenance=_prov())

    from app.v2.broker_read.api import _TEST_PROVIDER
    _TEST_PROVIDER["instance"] = SmugglingProvider()
    r = (await broker_client.post(f"{BR}/sync", headers=headers,
                                  json={})).json()
    assert r["outcome"] == "complete"
    assert canary not in str(r)  # sync response never echoes payloads
    health = (await broker_client.get(f"{BR}/health",
                                      headers=headers)).json()
    assert canary not in str(health)
    async with session_scope() as session:
        audits = list((await session.execute(
            select(V2AuditEvent).where(
                V2AuditEvent.domain == "v2.broker_read"))).scalars().all())
        for a in audits:
            assert canary not in str(a.details)
    orders = (await broker_client.get(f"{BR}/orders",
                                      headers=headers)).json()
    assert canary in str(orders["orders"])  # the ONE lawful site


@pytest.mark.asyncio
async def test_vault_act_records_no_material(broker_client):
    headers = await _admin(broker_client)
    r = (await broker_client.post(f"{BR}/vault", headers=headers,
                                  json={"action": "unlock"})).json()
    assert r["outcome"] == "recorded"
    async with session_scope() as session:
        audits = [a for (a,) in (await session.execute(
            select(V2AuditEvent.action).where(V2AuditEvent.action
                   == "broker.vault.unlock_requested"))).all()]
        assert audits
