"""V2 BE-3 P2 tests — BO-V2-BE-3-P2-001 §4 evidence matrix (non-network).

Covers: default-deny precondition matrix, endpoint auth/identity/correlation,
budget boundary/retry-storm/auth-debit/post-exhaustion, durable audit
sequence failures (start/completion), credential boundary + import
boundaries, evidence-schema conformance, plan shape, and SQLite migration
lifecycle with interruption recovery. NO real network call occurs anywhere:
the socket guard is active for every test in this module.
"""

from __future__ import annotations

import os
import socket
import sqlite3
import subprocess
import sys
from pathlib import Path
from uuid import uuid4

import pytest
from httpx import AsyncClient
from sqlalchemy import func, select

from app.auth.security import hash_password
from app.db.models.operator import Operator
from app.db.models.v2_audit_event import V2AuditEvent
from app.db.models.v2_provider import V2MdProvider
from app.db.session import session_scope
from app.v2.marketdata.providers.contract_test import (
    MAX_ATTEMPTS,
    RETRY_ALLOCATION,
    AttemptBudget,
    build_call_plan,
)
from app.v2.marketdata.providers.credentials import (
    ABSENT,
    EnvSecretBackend,
    FileSecretBackend,
    resolve_contract_test_credential,
)
from app.v2.temporal.validation import utc_now

CT = "/api/v1/v2/marketdata/providers/twelvedata/contract-test"
PASSWORD = "operator-pass-123"
BACKEND_DIR = Path(__file__).resolve().parents[1]
PROVIDERS_DIR = BACKEND_DIR / "app" / "v2" / "marketdata" / "providers"


@pytest.fixture(autouse=True)
def _socket_guard(monkeypatch):
    """No OUTBOUND network attempt may occur in ANY P2 test (BO §2).

    Guards the outbound primitives (DNS resolution + connection
    establishment). ``socket.socket`` itself is not patched because
    asyncio's event loop uses local ``socketpair()`` for internal IPC —
    which is not network activity. Any real provider contact would require
    getaddrinfo/create_connection and dies here.
    """

    def _deny(*_a, **_k):  # pragma: no cover
        raise AssertionError("P2 test attempted outbound network access")

    monkeypatch.setattr(socket, "getaddrinfo", _deny)
    monkeypatch.setattr(socket, "create_connection", _deny)
    yield


async def _operator(role: str = "operator") -> tuple[str, str]:
    async with session_scope() as session:
        op = Operator(
            username=f"p2-{role}-{uuid4().hex[:10]}",
            hashed_password=hash_password(PASSWORD),
            role=role,
            is_active=True,
        )
        session.add(op)
        await session.flush()
        return op.id, op.username


async def _login(client: AsyncClient, username: str, password: str = PASSWORD) -> dict[str, str]:
    r = await client.post("/api/v1/auth/login", json={"username": username, "password": password})
    assert r.status_code == 200, r.text
    return {"Authorization": f"Bearer {r.json()['tokens']['access_token']}"}


async def _seed_provider(entitlement_status: str = "unverified") -> None:
    async with session_scope() as session:
        row = (
            await session.execute(
                select(V2MdProvider).where(V2MdProvider.provider_id == "twelvedata")
            )
        ).scalar_one_or_none()
        if row is None:
            session.add(
                V2MdProvider(
                    id=str(uuid4()),
                    provider_id="twelvedata",
                    display_name="Twelve Data (architecture candidate)",
                    markets=["forex", "crypto", "metal"],
                    entitlement=None,
                    entitlement_status=entitlement_status,
                    persistence_permitted=False,
                    source_status="architecture_candidate",
                    created_at=utc_now(),
                )
            )
        else:
            row.entitlement_status = entitlement_status


# ---------------------------------------------------------------------------
# Credential boundary (§3.1)
# ---------------------------------------------------------------------------


class TestCredentialBoundary:
    def test_placeholder_and_empty_are_absent(self, monkeypatch):
        for value in ("", "TD_TEST_KEY_PLACEHOLDER", "placeholder", "none"):
            monkeypatch.setenv("AXIOM_TD_API_KEY", value)
            assert EnvSecretBackend().resolve().state == "absent"

    def test_missing_env_is_absent(self, monkeypatch):
        monkeypatch.delenv("AXIOM_TD_API_KEY", raising=False)
        monkeypatch.delenv("AXIOM_TD_API_KEY_FILE", raising=False)
        assert resolve_contract_test_credential() is ABSENT or (
            resolve_contract_test_credential().state == "absent"
        )

    def test_present_value_never_in_repr_or_str(self, monkeypatch):
        monkeypatch.setenv("AXIOM_TD_API_KEY", "REALLOOKING-SECRET-123")
        resolved = EnvSecretBackend().resolve()
        assert resolved.state == "present"
        assert "REALLOOKING-SECRET-123" not in repr(resolved)
        assert "REALLOOKING-SECRET-123" not in str(resolved)

    def test_file_backend(self, monkeypatch, tmp_path):
        monkeypatch.delenv("AXIOM_TD_API_KEY", raising=False)
        secret_file = tmp_path / "td.key"
        secret_file.write_text("FILE-SECRET-456\n")
        monkeypatch.setenv("AXIOM_TD_API_KEY_FILE", str(secret_file))
        resolved = FileSecretBackend().resolve()
        assert resolved.state == "present"
        assert "FILE-SECRET-456" not in repr(resolved)

    def test_no_module_global_holds_a_secret(self, monkeypatch):
        monkeypatch.setenv("AXIOM_TD_API_KEY", "GLOBALS-CHECK-789")
        import app.v2.marketdata.providers.credentials as credmod

        resolve_contract_test_credential()
        for name, value in vars(credmod).items():
            if isinstance(value, str):
                assert "GLOBALS-CHECK-789" not in value, name

    def test_import_boundary_only_credentials_module_resolves(self):
        """§3.1: no credential resolution outside the credentials module."""
        offenders = []
        for py in (BACKEND_DIR / "app").rglob("*.py"):
            rel = py.relative_to(BACKEND_DIR)
            text = py.read_text()
            if "AXIOM_TD_API_KEY" in text and py.name != "credentials.py":
                offenders.append(str(rel))
        assert offenders == [], offenders


# ---------------------------------------------------------------------------
# Transport boundary (§3.2)
# ---------------------------------------------------------------------------


class TestTransportBoundary:
    def test_unauthorized_construction_refused(self):
        from app.v2.errors.contract import V2Error
        from app.v2.marketdata.providers.transport import NetworkTransport

        with pytest.raises(V2Error):
            NetworkTransport(object())

    def test_construction_token_referenced_only_by_endpoint_chain(self):
        """DEL-003 corrected: exact PATHS, not basenames. The ONLY authorized
        references are the transport module (defines the token) and the
        authenticated API endpoint module (constructs the transport). The
        providers/contract_test.py runner module must NOT reference it —
        construction happens only inside the endpoint dependency chain."""
        allowed = {
            "app/v2/marketdata/providers/transport.py",
            "app/v2/marketdata/api/contract_test.py",
        }
        offenders = []
        referencing = []
        for py in (BACKEND_DIR / "app").rglob("*.py"):
            rel = py.relative_to(BACKEND_DIR).as_posix()
            if "construction_token" in py.read_text():
                referencing.append(rel)
                if rel not in allowed:
                    offenders.append(rel)
        assert offenders == [], offenders
        # positive assertion: the full authorized chain is present
        assert set(referencing) == allowed, referencing

    def test_non_p2_provider_modules_still_transport_free(self):
        """P1 static scan preserved: only transport.py may import httpx."""
        forbidden = ("import httpx", "from httpx", "import aiohttp", "import websockets",
                     "import socket", "from socket")
        offenders = []
        for py in PROVIDERS_DIR.rglob("*.py"):
            if py.name == "transport.py":
                continue
            text = py.read_text()
            for marker in forbidden:
                if marker in text:
                    offenders.append(f"{py.name}: {marker}")
        assert offenders == [], offenders

    def test_off_host_planned_request_refused(self):
        from app.v2.errors.contract import V2Error
        from app.v2.marketdata.providers.contract import PlannedRequest
        from app.v2.marketdata.providers.transport import NetworkTransport, construction_token

        transport = NetworkTransport(construction_token())
        rogue = PlannedRequest(host="evil.example.com", path="/x", params={})
        with pytest.raises(V2Error):
            transport.execute(rogue, apikey="k")


# ---------------------------------------------------------------------------
# Budget (§3.6)
# ---------------------------------------------------------------------------


class TestAttemptBudget:
    def test_debit_sequence_and_exhaustion(self):
        budget = AttemptBudget(3)
        assert budget.debit() == 1
        assert budget.debit() == 2
        assert budget.debit() == 3
        assert budget.debit() is None  # atomic refusal
        assert budget.remaining == 0

    def test_fixed_allocation_totals_exactly_35(self):
        plan = build_call_plan()
        total = 0
        for call in plan:
            total += 1 + RETRY_ALLOCATION[call.request_class]
        assert total == MAX_ATTEMPTS == 35

    def test_plan_shape_16_calls_all_classes(self):
        plan = build_call_plan()
        assert len(plan) == 16
        by_class: dict[str, int] = {}
        for c in plan:
            by_class[c.request_class] = by_class.get(c.request_class, 0) + 1
        assert by_class == {
            "AUTH": 2, "BARS-DEEP": 3, "SYMBOL-SWEEP": 9, "QUOTE": 1, "SYMBOLS-NEG": 1
        }
        # all 12 canonical instruments live-exercised
        instruments = {c.instrument_id for c in plan if c.instrument_id}
        assert len(instruments) == 12 + 0 if "forex.eurusd" in instruments else False

    def test_retry_storm_cannot_exceed_cap(self):
        """Worst case: every attempt fails and retries max out — the token
        gate bounds total debits at 35."""
        budget = AttemptBudget(35)
        attempts = 0
        for call in build_call_plan():
            for _ in range(RETRY_ALLOCATION[call.request_class] + 1):
                if budget.debit() is None:
                    break
                attempts += 1
        assert attempts == 35
        assert budget.debit() is None


# ---------------------------------------------------------------------------
# Endpoint: auth, default-deny preconditions, audit sequence (§§3.3–3.5)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_endpoint_denied_for_operator_and_unprivileged(async_client: AsyncClient) -> None:
    for role in ("operator", "unprivileged"):
        _, name = await _operator(role=role)
        h = await _login(async_client, name)
        r = await async_client.post(CT, headers=h)
        assert r.status_code == 403, f"{role} -> {r.status_code}"
        assert r.json()["detail"] == "Permission denied"
        assert "v2." not in r.text


@pytest.mark.asyncio
async def test_endpoint_requires_authentication(async_client: AsyncClient) -> None:
    r = await async_client.post(CT)
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_precondition_default_deny_matrix(async_client: AsyncClient, monkeypatch) -> None:
    """All five preconditions absent → refusal names every failed gate,
    refusal audit persisted, zero network attempts (socket guard proves)."""
    await _seed_provider(entitlement_status="unverified")
    admin = await _login(async_client, "admin", "admin123")
    monkeypatch.delenv("AXIOM_TD_P2_AUTHORITY_REF", raising=False)
    monkeypatch.delenv("AXIOM_TD_CONTRACT_TEST_ENABLED", raising=False)
    monkeypatch.delenv("AXIOM_TD_API_KEY", raising=False)
    monkeypatch.delenv("AXIOM_TD_API_KEY_FILE", raising=False)

    r = await async_client.post(CT, headers=admin)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["run_state"] == "refused"
    assert set(body["refusal_reasons"]) == {
        "authority_ref", "entitlement_verified", "secret_present", "enablement_flag"
    }
    assert body["calls"] == []
    assert {"mode", "correlation_id", "timestamp"} <= set(body)

    async with session_scope() as session:
        refusals = (
            await session.execute(
                select(V2AuditEvent).where(
                    V2AuditEvent.action == "provider.contract_test.refused"
                )
            )
        ).scalars().all()
        assert refusals
        assert "failed_preconditions" in (refusals[-1].details or {})


@pytest.mark.asyncio
async def test_each_precondition_independently_blocks(
    async_client: AsyncClient, monkeypatch
) -> None:
    """Satisfy four gates, leave one failing — every single gate blocks."""
    admin = await _login(async_client, "admin", "admin123")

    async def run_with(authority=True, entitlement=True, secret=True, flag=True):
        await _seed_provider(entitlement_status="verified" if entitlement else "unverified")
        if authority:
            monkeypatch.setenv("AXIOM_TD_P2_AUTHORITY_REF", "BO-V2-BE-3-P2-001")
        else:
            monkeypatch.delenv("AXIOM_TD_P2_AUTHORITY_REF", raising=False)
        if secret:
            monkeypatch.setenv("AXIOM_TD_API_KEY", "P2-TEST-ONLY-VALUE")
        else:
            monkeypatch.delenv("AXIOM_TD_API_KEY", raising=False)
        if flag:
            monkeypatch.setenv("AXIOM_TD_CONTRACT_TEST_ENABLED", "true")
        else:
            monkeypatch.delenv("AXIOM_TD_CONTRACT_TEST_ENABLED", raising=False)
        r = await async_client.post(CT, headers=admin)
        return r.json()

    for missing, kwargs in (
        ("authority_ref", dict(authority=False)),
        ("entitlement_verified", dict(entitlement=False)),
        ("secret_present", dict(secret=False)),
        ("enablement_flag", dict(flag=False)),
    ):
        body = await run_with(**kwargs)
        assert body["run_state"] == "refused", missing
        assert missing in body["refusal_reasons"], missing


@pytest.mark.asyncio
async def test_full_run_with_mock_transport_durable_sequence(
    async_client: AsyncClient, monkeypatch
) -> None:
    """All gates satisfied; transport mocked (no network). Verifies the
    durable audit sequence, evidence schema, budget accounting, and that no
    payload body appears anywhere in evidence."""
    await _seed_provider(entitlement_status="verified")
    admin = await _login(async_client, "admin", "admin123")
    monkeypatch.setenv("AXIOM_TD_P2_AUTHORITY_REF", "BO-V2-BE-3-P2-001")
    monkeypatch.setenv("AXIOM_TD_API_KEY", "P2-MOCKRUN-SECRET-XYZ")
    monkeypatch.setenv("AXIOM_TD_CONTRACT_TEST_ENABLED", "true")

    from app.v2.marketdata.providers import transport as transport_mod

    ok_body = (
        b'{"meta":{"symbol":"EUR/USD","interval":"1min"},"values":['
        b'{"datetime":"2026-08-20 10:00:00","open":"1.1","high":"1.2",'
        b'"low":"1.0","close":"1.15"}],"status":"ok"}'
    )

    def mock_execute(self, planned, *, apikey):
        # correct symbol echo per request
        symbol = planned.params.get("symbol", "EUR/USD")
        if symbol == "ZZZ/ZZZ" or apikey == "":
            body = b'{"code":401,"message":"error","status":"error"}'
        elif planned.path == "/quote":
            body = b'{"symbol":"EUR/USD","datetime":"2026-08-20 10:05:00","close":"1.10150"}'
        else:
            body = ok_body.replace(b"EUR/USD", symbol.encode())
        return transport_mod.TransportResult(status_code=200, body=body, latency_ms=12.3)

    monkeypatch.setattr(transport_mod.NetworkTransport, "execute", mock_execute)

    r = await async_client.post(CT, headers=admin)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["run_state"] == "completed"
    assert body["completed"] == 16
    assert body["indeterminate_after_start"] == 0
    # evidence schema conformance: no payload text, secret absent
    text = r.text
    assert "P2-MOCKRUN-SECRET-XYZ" not in text
    assert "1.10150" not in str([c["body_sha256"] for c in body["calls"]])
    for call in body["calls"]:
        assert set(call) == {
            "request_class", "instrument_id", "redacted_request", "response_status",
            "body_sha256", "schema_verdict", "error_category", "attempt_number",
            "budget_remaining", "call_state", "latency_ms",
        }
        # stronger than redaction: the planner NEVER carries the key —
        # it is injected only at transport execution, so no apikey param
        # (redacted or otherwise) can appear in evidence at all
        assert "apikey" not in call["redacted_request"]
        assert call["redacted_request"].startswith("https://api.twelvedata.com/")

    # durable sequence: one start per attempt, one completion per completed call
    async with session_scope() as session:
        starts = (
            await session.execute(
                select(func.count()).select_from(V2AuditEvent).where(
                    V2AuditEvent.action == "provider.contract_test.call_started"
                )
            )
        ).scalar_one()
        completes = (
            await session.execute(
                select(func.count()).select_from(V2AuditEvent).where(
                    V2AuditEvent.action == "provider.contract_test.call_completed"
                )
            )
        ).scalar_one()
        assert int(starts) == 16
        assert int(completes) == 16
        run_events = (
            await session.execute(
                select(V2AuditEvent).where(
                    V2AuditEvent.action == "provider.contract_test.complete"
                )
            )
        ).scalars().all()
        assert run_events and run_events[-1].details["completed"] == 16


@pytest.mark.asyncio
async def test_completion_audit_failure_hard_stop_and_indeterminate(
    async_client: AsyncClient, monkeypatch, tmp_path
) -> None:
    """§3.5.5: completion-audit failure → indeterminate call, hard stop,
    independent incident marker written."""
    await _seed_provider(entitlement_status="verified")
    admin = await _login(async_client, "admin", "admin123")
    monkeypatch.setenv("AXIOM_TD_P2_AUTHORITY_REF", "BO-V2-BE-3-P2-001")
    monkeypatch.setenv("AXIOM_TD_API_KEY", "P2-INCIDENT-TEST")
    monkeypatch.setenv("AXIOM_TD_CONTRACT_TEST_ENABLED", "true")
    monkeypatch.setenv("AXIOM_TD_INCIDENT_DIR", str(tmp_path))

    import app.v2.marketdata.api.contract_test as ct_mod
    from app.v2.marketdata.providers import transport as transport_mod

    def mock_execute(self, planned, *, apikey):
        return transport_mod.TransportResult(
            status_code=200,
            body=b'{"meta":{"symbol":"EUR/USD","interval":"1min"},"values":[],"status":"ok"}',
            latency_ms=1.0,
        )

    monkeypatch.setattr(transport_mod.NetworkTransport, "execute", mock_execute)

    real_audit = ct_mod._durable_audit
    call_count = {"n": 0}

    async def failing_audit(session, *, action, **kwargs):
        if action == "provider.contract_test.call_completed":
            call_count["n"] += 1
            raise RuntimeError("simulated audit sink failure")
        return await real_audit(session, action=action, **kwargs)

    monkeypatch.setattr(ct_mod, "_durable_audit", failing_audit)

    r = await async_client.post(CT, headers=admin)
    assert r.status_code == 200
    body = r.json()
    assert body["run_state"] == "aborted"
    assert body["indeterminate_after_start"] == 1
    assert call_count["n"] == 1  # hard stop: no second completion attempt
    # only ONE call was attempted before the stop
    assert len(body["calls"]) == 1
    markers = list(tmp_path.glob("axiom_p2_incident_*.marker"))
    assert markers and "completion_audit_failed" in markers[0].read_text()


@pytest.mark.asyncio
async def test_transport_failure_gets_durable_completion_every_attempt(
    async_client: AsyncClient, monkeypatch
) -> None:
    """DEL-002: every started attempt — including each retry — receives a
    durable completion event with a deterministic error category; final
    attempt accounting is exact."""
    await _seed_provider(entitlement_status="verified")
    admin = await _login(async_client, "admin", "admin123")
    monkeypatch.setenv("AXIOM_TD_P2_AUTHORITY_REF", "BO-V2-BE-3-P2-001")
    monkeypatch.setenv("AXIOM_TD_API_KEY", "P2-RETRYFAIL-TEST")
    monkeypatch.setenv("AXIOM_TD_CONTRACT_TEST_ENABLED", "true")

    from app.v2.marketdata.providers import transport as transport_mod

    class FakeTimeout(Exception):
        pass

    FakeTimeout.__name__ = "ConnectTimeout"

    def always_fail(self, planned, *, apikey):
        raise FakeTimeout("simulated timeout")

    monkeypatch.setattr(transport_mod.NetworkTransport, "execute", always_fail)

    r = await async_client.post(CT, headers=admin)
    assert r.status_code == 200, r.text
    body = r.json()
    # every attempt is transport_failure/completed; none silently dropped
    assert all(c["schema_verdict"] == "transport_failure" for c in body["calls"])
    assert all(c["call_state"] == "completed" for c in body["calls"])
    assert all(c["error_category"] == "transport:timeout" for c in body["calls"])
    total_attempts = len(body["calls"])
    # worst-case allocation consumed exactly: bounded by the 35 gate
    assert total_attempts == 35
    assert body["indeterminate_after_start"] == 0

    # audit pairing: every call_started has a call_completed (durable)
    async with session_scope() as session:
        starts = (
            await session.execute(
                select(func.count()).select_from(V2AuditEvent).where(
                    V2AuditEvent.action == "provider.contract_test.call_started"
                )
            )
        ).scalar_one()
        completes = (
            await session.execute(
                select(func.count()).select_from(V2AuditEvent).where(
                    V2AuditEvent.action == "provider.contract_test.call_completed"
                )
            )
        ).scalar_one()
        assert int(starts) == int(completes) == 35


@pytest.mark.asyncio
async def test_start_audit_failure_means_no_network_attempt(
    async_client: AsyncClient, monkeypatch, tmp_path
) -> None:
    """§3.5.3: no durable start → no attempt; transport never invoked."""
    await _seed_provider(entitlement_status="verified")
    admin = await _login(async_client, "admin", "admin123")
    monkeypatch.setenv("AXIOM_TD_P2_AUTHORITY_REF", "BO-V2-BE-3-P2-001")
    monkeypatch.setenv("AXIOM_TD_API_KEY", "P2-STARTFAIL-TEST")
    monkeypatch.setenv("AXIOM_TD_CONTRACT_TEST_ENABLED", "true")
    monkeypatch.setenv("AXIOM_TD_INCIDENT_DIR", str(tmp_path))

    import app.v2.marketdata.api.contract_test as ct_mod
    from app.v2.marketdata.providers import transport as transport_mod

    transport_calls = {"n": 0}

    def counting_execute(self, planned, *, apikey):  # pragma: no cover
        transport_calls["n"] += 1
        raise AssertionError("transport must not be invoked")

    monkeypatch.setattr(transport_mod.NetworkTransport, "execute", counting_execute)

    real_audit = ct_mod._durable_audit

    async def failing_audit(session, *, action, **kwargs):
        if action == "provider.contract_test.call_started":
            raise RuntimeError("simulated start-audit failure")
        return await real_audit(session, action=action, **kwargs)

    monkeypatch.setattr(ct_mod, "_durable_audit", failing_audit)

    r = await async_client.post(CT, headers=admin)
    body = r.json()
    assert body["run_state"] == "aborted"
    assert transport_calls["n"] == 0  # NO network attempt occurred
    assert body["calls"][0]["call_state"] == "refused-before-call"
    assert body["calls"][0]["schema_verdict"] == "start_audit_failed"


@pytest.mark.asyncio
async def test_final_audit_failure_never_reports_completed(
    async_client: AsyncClient, monkeypatch, tmp_path
) -> None:
    """DEL-005: if the final `provider.contract_test.complete` audit cannot
    be durably committed, the run must NOT claim completed — it returns an
    audit-incomplete aborted state, fires the independent incident marker,
    and exposes only safe non-payload information."""
    await _seed_provider(entitlement_status="verified")
    admin = await _login(async_client, "admin", "admin123")
    monkeypatch.setenv("AXIOM_TD_P2_AUTHORITY_REF", "BO-V2-BE-3-P2-001")
    monkeypatch.setenv("AXIOM_TD_API_KEY", "P2-FINALAUDIT-TEST")
    monkeypatch.setenv("AXIOM_TD_CONTRACT_TEST_ENABLED", "true")
    monkeypatch.setenv("AXIOM_TD_INCIDENT_DIR", str(tmp_path))

    import app.v2.marketdata.api.contract_test as ct_mod
    from app.v2.marketdata.providers import transport as transport_mod

    def mock_execute(self, planned, *, apikey):
        symbol = planned.params.get("symbol", "EUR/USD")
        if symbol == "ZZZ/ZZZ" or apikey == "":
            body = b'{"code":401,"message":"error","status":"error"}'
        elif planned.path == "/quote":
            body = (
                b'{"symbol":"EUR/USD","datetime":"2026-08-20 10:05:00",'
                b'"close":"1.10150"}'
            )
        else:
            body = (
                b'{"meta":{"symbol":"' + symbol.encode() + b'","interval":"1min"},'
                b'"values":[{"datetime":"2026-08-20 10:00:00","open":"1.1",'
                b'"high":"1.2","low":"1.0","close":"1.15"}],"status":"ok"}'
            )
        return transport_mod.TransportResult(status_code=200, body=body, latency_ms=1.0)

    monkeypatch.setattr(transport_mod.NetworkTransport, "execute", mock_execute)

    real_audit = ct_mod._durable_audit

    async def failing_final_audit(session, *, action, **kwargs):
        if action == "provider.contract_test.complete":
            raise RuntimeError("simulated final-audit sink failure")
        return await real_audit(session, action=action, **kwargs)

    monkeypatch.setattr(ct_mod, "_durable_audit", failing_final_audit)

    r = await async_client.post(CT, headers=admin)
    assert r.status_code == 200, r.text
    body = r.json()
    # fail-closed: never "completed"
    assert body["run_state"] == "aborted:final-audit-incomplete"
    assert body["run_state"] != "completed"
    # all 16 calls themselves executed and are individually accounted
    assert body["completed"] == 16
    # independent incident channel fired
    markers = list(tmp_path.glob("axiom_p2_incident_*.marker"))
    assert markers and "complete_audit_failed" in markers[0].read_text()
    # safe non-payload response only
    assert "P2-FINALAUDIT-TEST" not in r.text


# ---------------------------------------------------------------------------
# Migration lifecycle + interruption recovery (§3.8)
# ---------------------------------------------------------------------------


def _run_alembic(args: list[str], db_url: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["AXIOM_DATABASE_URL"] = db_url
    env.setdefault("AXIOM_ENVIRONMENT", "testing")
    env.setdefault("AXIOM_ALLOW_INSECURE_DEV", "true")
    env.setdefault("AXIOM_JWT_SECRET_KEY", "test-secret-key-at-least-32-chars-long!!")
    return subprocess.run(
        [sys.executable, "-m", "alembic", *args],
        cwd=BACKEND_DIR, env=env, capture_output=True, text=True, timeout=600,
    )


def test_p2_entitlement_migration_lifecycle_and_recovery(tmp_path: Path) -> None:
    db_file = tmp_path / "p2_migration.db"
    db_url = f"sqlite+aiosqlite:///{db_file}"

    # Generational scope: pin to this band's own head (20260825_0041);
    # the 0042 transition migration has its own test module.
    upgrade = _run_alembic(["upgrade", "20260825_0041"], db_url)
    assert upgrade.returncode == 0, upgrade.stderr

    conn = sqlite3.connect(db_file)
    try:
        cur = conn.cursor()
        # entitlement recorded; status/persistence unchanged
        row = cur.execute(
            "SELECT entitlement_status, source_status, persistence_permitted,"
            " entitlement FROM v2_md_provider WHERE provider_id='twelvedata'"
        ).fetchone()
        assert row[0] == "verified"
        assert row[1] == "architecture_candidate"  # NO promotion
        assert row[2] == 0  # persistence still false
        assert "ITRGA-DET-V2-BE-3-P2-ENT-001" in row[3]
        assert '"api_credits_per_day": 800' in row[3] or '"api_credits_per_day":800' in row[3]

        # no history append (P1 genesis row only)
        n_hist = cur.execute(
            "SELECT COUNT(*) FROM v2_md_provider_status_history"
        ).fetchone()[0]
        assert n_hist == 1

        # guard restored: registry immutable again (both triggers)
        trigs = {
            r[0] for r in cur.execute(
                "SELECT name FROM sqlite_master WHERE type='trigger'"
                " AND name LIKE 'v2_md_provider_immutable%'"
            )
        }
        assert trigs == {
            "v2_md_provider_immutable_update", "v2_md_provider_immutable_delete"
        }
        with pytest.raises(sqlite3.DatabaseError, match="immutable"):
            cur.execute(
                "UPDATE v2_md_provider SET entitlement_status='expired'"
                " WHERE provider_id='twelvedata'"
            )
        with pytest.raises(sqlite3.DatabaseError, match="immutable"):
            cur.execute("DELETE FROM v2_md_provider WHERE provider_id='twelvedata'")
    finally:
        conn.close()

    # drift gate: no P2 operations
    check = _run_alembic(["check"], db_url)
    drift = (check.stdout + check.stderr).lower()
    assert "v2_md_provider" not in drift

    # downgrade restores P1 entitlement state + guard
    downgrade = _run_alembic(["downgrade", "20260824_0040"], db_url)
    assert downgrade.returncode == 0, downgrade.stderr
    conn = sqlite3.connect(db_file)
    try:
        cur = conn.cursor()
        row = cur.execute(
            "SELECT entitlement_status, entitlement FROM v2_md_provider"
            " WHERE provider_id='twelvedata'"
        ).fetchone()
        assert row == ("unverified", None)
        with pytest.raises(sqlite3.DatabaseError, match="immutable"):
            cur.execute(
                "UPDATE v2_md_provider SET entitlement_status='verified'"
                " WHERE provider_id='twelvedata'"
            )
    finally:
        conn.close()

    # re-upgrade
    reup = _run_alembic(["upgrade", "20260825_0041"], db_url)
    assert reup.returncode == 0, reup.stderr


def test_p2_migration_interruption_detection(tmp_path: Path) -> None:
    """§3.8 interruption safety: simulate a failed run that left the guard
    absent — the verify helper detects it and refuses to certify."""
    db_file = tmp_path / "p2_interrupt.db"
    db_url = f"sqlite+aiosqlite:///{db_file}"
    assert _run_alembic(["upgrade", "20260825_0041"], db_url).returncode == 0

    conn = sqlite3.connect(db_file)
    conn.execute("DROP TRIGGER v2_md_provider_immutable_update")
    conn.commit()
    conn.close()

    # _verify_guard_present must detect the missing guard
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "p2mig", BACKEND_DIR / "alembic" / "versions" / "20260825_0041_v2_be3_p2_entitlement.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    from sqlalchemy import create_engine

    engine = create_engine(f"sqlite:///{db_file}")
    with engine.connect() as bind:
        with pytest.raises(RuntimeError, match="NOT restored"):
            module._verify_guard_present(bind)
