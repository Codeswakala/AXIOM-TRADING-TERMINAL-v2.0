"""V2 BE-11 API/wall/scan coupons — L-4/L-7/L-8/L-9 + D-B11-MODE arm.

RBAC 401/403 battery; wording scans (identifiers + payloads); extended
banned-import law; N3 wall pair byte-unchanged + the NEW wall law
(no domain imports the bridge; bridge imports projections/engines only);
duplicate-intent idempotency arm; LIVE-mode 4xx arm.
"""

from __future__ import annotations

import ast
import socket
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.auth.security import hash_password
from app.db.models.operator import Operator
from app.db.models.v2_broker_read import V2BrokerBalance, V2BrokerSyncRun
from app.db.models.v2_paper_bridge import V2PaperBridgeDriftRun
from app.db.session import session_scope

PB = "/api/v1/v2/paper-bridge"
PASSWORD = "operator-pass-123"
UTC = timezone.utc
BACKEND = Path(__file__).resolve().parents[1]
BRIDGE_DIR = BACKEND / "app/v2/paper_bridge"
BROKER_DIR = BACKEND / "app/v2/broker_read"
PAPER_DIR = BACKEND / "app/v2/paper_trading"

REGIME = {"data_class": "simulated", "mode": "RESEARCH",
          "operator_id": "t", "correlation_id": None}
CITATION = {"value": "1.1000", "currency_unit": "USD",
            "cited_source": "operator: terminal quote panel",
            "cited_at": "2026-09-06T12:00:00+00:00"}


@pytest.fixture(autouse=True)
def _socket_guard(monkeypatch):
    def _deny(*_a, **_k):
        raise AssertionError("network attempt during BE-11 test")

    monkeypatch.setattr(socket, "getaddrinfo", _deny)
    monkeypatch.setattr(socket, "create_connection", _deny)


@pytest_asyncio.fixture
async def paper_client(prepared_db, monkeypatch):
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


async def _seed_basis_and_staleness():
    async with session_scope() as session:
        run = V2BrokerSyncRun(
            provider_id="exness_mt5_demo", scope={}, outcome="complete",
            page_counts={}, origin_basis="o", inputs_hash="h",
            result_digest="d", refusal=None, actor_id="t", **REGIME)
        run.created_at = datetime.now(UTC) - timedelta(hours=1)
        session.add(run)
        await session.flush()
        session.add(V2BrokerBalance(
            provider_id="exness_mt5_demo",
            broker_account_ext_id="476910140", balance="10000.0",
            margin_used="0.0", margin_available="10000.0",
            unrealized_pl="0.0", currency="USD", sync_run_id=run.id,
            server_hostname="ExnessKE-MT5Trial9", fetched_at_basis="b",
            **REGIME))
        session.add(V2PaperBridgeDriftRun(
            run_kind="seed", seed_name="generation_staleness",
            payload={"max_age_hours": 24, "citation": "test overlay"},
            actor_id="t", **REGIME))


def _intent_body(idem="k1", qty="100"):
    return {"account_id": "acct-1", "instrument_id": "forex.eurusd",
            "side": "buy", "quantity": qty, "idempotency_key": idem,
            "reference_price": CITATION}


# --- end-to-end + idempotency (R-3.5) --------------------------------------------


@pytest.mark.asyncio
async def test_intent_end_to_end_and_duplicate_refusal(paper_client):
    await _seed_basis_and_staleness()
    headers = await _admin(paper_client)
    r = (await paper_client.post(f"{PB}/intents", headers=headers,
                                 json=_intent_body())).json()
    assert r["outcome"] == "recorded", r
    assert r["gateway"]["decision"] == "accept_with_notes"
    assert any("deferred" in n for n in r["gateway"]["notes"])
    assert len(r["digest"]) == 64
    # duplicate => typed refusal (schema anchor surfaced as law)
    r2 = (await paper_client.post(f"{PB}/intents", headers=headers,
                                  json=_intent_body())).json()
    assert r2["outcome"] == "refused"
    assert r2["reason"] == "duplicate_intent"


@pytest.mark.asyncio
async def test_unseeded_threshold_refuses_on_wire(paper_client):
    async with session_scope() as session:
        run = V2BrokerSyncRun(
            provider_id="exness_mt5_demo", scope={}, outcome="complete",
            page_counts={}, origin_basis="o", inputs_hash="h",
            result_digest="d", refusal=None, actor_id="t", **REGIME)
        session.add(run)
        await session.flush()
        session.add(V2BrokerBalance(
            provider_id="exness_mt5_demo",
            broker_account_ext_id="476910140", balance="10000.0",
            margin_used="0.0", margin_available="10000.0",
            unrealized_pl="0.0", currency="USD", sync_run_id=run.id,
            server_hostname="ExnessKE-MT5Trial9", fetched_at_basis="b",
            **REGIME))
    headers = await _admin(paper_client)
    r = (await paper_client.post(f"{PB}/intents", headers=headers,
                                 json=_intent_body())).json()
    assert r["outcome"] == "refused"
    assert r["reason"] == "basis_staleness_threshold_unseeded"


@pytest.mark.asyncio
async def test_evaluate_and_reads(paper_client):
    await _seed_basis_and_staleness()
    headers = await _admin(paper_client)
    posted = (await paper_client.post(f"{PB}/intents", headers=headers,
                                      json=_intent_body())).json()
    ev = (await paper_client.post(
        f"{PB}/evaluate", headers=headers,
        json={"intent_row_id": posted["intent_row_id"]})).json()
    assert ev["outcome"] == "computed"
    assert ev["gateway"]["decision"] == "accept_with_notes"
    ledger = (await paper_client.get(f"{PB}/ledger",
                                     headers=headers)).json()["ledger"]
    assert len(ledger) == 1
    assert ledger[0]["snapshot_ref"].startswith("bridge-basis:")
    drift = (await paper_client.get(f"{PB}/drift", headers=headers)).json()
    assert drift["comparison_state"] == "refuse_to_compare_unseeded"
    assert drift["staleness_seed_present"] is True
    assert drift["tolerance_seeds_present"] == 0


# --- D-B11-MODE: LIVE/other-mode 4xx ----------------------------------------------


@pytest.mark.asyncio
async def test_mode_arm_writers_refused_outside_paper(research_client):
    headers = await _admin(research_client)
    for path, body in ((f"{PB}/intents", _intent_body()),
                       (f"{PB}/evaluate", {"intent_row_id": "x"})):
        r = await research_client.post(path, headers=headers, json=body)
        assert r.status_code == 403
        assert "not permitted in this mode" in r.json()["detail"]


# --- L-9: RBAC battery ---------------------------------------------------------------


@pytest.mark.asyncio
async def test_l9_rbac_401_403_battery(paper_client):
    async with session_scope() as session:
        op = Operator(username=f"be11-op-{uuid4().hex[:10]}",
                      hashed_password=hash_password(PASSWORD),
                      role="operator", is_active=True)
        session.add(op)
        await session.flush()
        username = op.username
    headers = await _login(paper_client, username)
    for method, path, body in (
            ("post", f"{PB}/intents", _intent_body()),
            ("post", f"{PB}/evaluate", {"intent_row_id": "x"}),
            ("get", f"{PB}/ledger", None),
            ("get", f"{PB}/drift", None)):
        fn = getattr(paper_client, method)
        r = await (fn(path, headers=headers, json=body) if body is not None
                   else fn(path, headers=headers))
        assert r.status_code == 403
        assert r.json()["detail"] == "Permission denied"
        r = await (fn(path, json=body) if body is not None else fn(path))
        assert r.status_code == 401


# --- L-7: wording + banned-import scans ------------------------------------------------


# Action-verb class only. NOTE: `V2PaperOrderIntent` (the standing BE-8
# model NOUN — an intent RECORD) is lawful; the banned OrderIntent is the
# V1 BrokerPort mutation shape, covered by the import scan (no
# external_integration import can enter the bridge graph).
BANNED_VERBS = ("order_send", "ordersend", "place_order", "submit_order",
                "cancel_order", "modify_order", "trade_action",
                "from app.external_integration")


def test_l7_identifier_and_payload_verb_scan():
    """D-B11-NAMING (DDL identifiers) + D-B10-SCAN (band code)."""
    # DDL identifiers of the band's table
    from app.db.models.v2_paper_bridge import V2PaperBridgeDriftRun as T
    idents = [c.name for c in T.__table__.columns] + [T.__tablename__]
    for ident in idents:
        low = ident.lower()
        for verb in ("buy", "sell", "submit", "execute", "place"):
            assert verb not in low, f"{verb} in DDL identifier {ident}"
    # band code (docstrings stripped)
    for f in BRIDGE_DIR.rglob("*.py"):
        tree = ast.parse(f.read_text())
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.ClassDef,
                                 ast.FunctionDef, ast.AsyncFunctionDef)):
                body = node.body
                if (body and isinstance(body[0], ast.Expr)
                        and isinstance(body[0].value, ast.Constant)
                        and isinstance(body[0].value.value, str)):
                    body[0].value.value = ""
        code = ast.unparse(tree).lower()
        for verb in BANNED_VERBS:
            assert verb not in code, f"{verb} in {f.name}"


def test_l7_banned_import_scan_bridge():
    """No providers / MT5 / terminal / vault / network in the bridge."""
    banned = ("providers.exness_mt5", "broker_read.vault", "metatrader",
              "requests", "httpx", "urllib", "socket", "aiohttp")
    for f in BRIDGE_DIR.rglob("*.py"):
        tree = ast.parse(f.read_text())
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module]
            for name in names:
                low = name.lower()
                for token in banned:
                    assert token not in low, f"{f.name}: {name}"


# --- L-8: wall laws ---------------------------------------------------------------------


def test_l8_n3_wall_pair_byte_unchanged():
    """The BE-9 wall tests remain byte-identical to their frozen pins."""
    import hashlib
    pins = {
        "tests/test_v2_be9_boundaries.py":
            "9ba9fd8290d5861911582a5286752c7ed5aee71c06e56acb9f4ac4337355f91f",
        "tests/test_v2_be8_boundaries.py": None,  # presence-only check
    }
    sha = hashlib.sha256(
        (BACKEND / "tests/test_v2_be9_boundaries.py").read_bytes()
    ).hexdigest()
    assert sha == pins["tests/test_v2_be9_boundaries.py"]
    assert (BACKEND / "tests/test_v2_be8_boundaries.py").exists()


def test_l8_new_wall_law_no_domain_imports_bridge():
    """Neither broker_read nor paper_trading imports paper_bridge."""
    for domain in (BROKER_DIR, PAPER_DIR):
        for f in domain.rglob("*.py"):
            tree = ast.parse(f.read_text())
            for node in ast.walk(tree):
                names = []
                if isinstance(node, ast.Import):
                    names = [a.name for a in node.names]
                elif isinstance(node, ast.ImportFrom) and node.module:
                    names = [node.module]
                for name in names:
                    assert "paper_bridge" not in name, f"{f}: {name}"


def test_l8_bridge_imports_projections_and_engines_only():
    """The bridge's cross-domain imports name models/engines only —
    never the broker adapter leg, never the paper API surface."""
    allowed_prefixes = (
        "app.db.models", "app.db.session", "app.v2.paper_bridge",
        "app.v2.rbac", "app.v2.identifiers", "app.v2.temporal",
        "app.db.base",
    )
    for f in BRIDGE_DIR.rglob("*.py"):
        tree = ast.parse(f.read_text())
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module]
            for name in names:
                if not name.startswith("app."):
                    continue
                assert name.startswith(allowed_prefixes), f"{f.name}: {name}"
