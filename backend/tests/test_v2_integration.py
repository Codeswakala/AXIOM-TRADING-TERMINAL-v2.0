"""V2 genuine integration tests — real database persistence, API behaviour,
triggers, migration lifecycle, and security paths (CA-01/CA-02).

Every test in this file exercises an actual async database session, a real
HTTP request against the FastAPI app, or the real Alembic migration chain.
Static/unit checks live in the test_v2_<module>.py unit files.

Covered required paths (ITRGA-ACC-V2-BE-1-INTAKE-001 §3 / DEF-BE1-02):
- V2 audit append and persisted redaction
- V2 lineage append
- audit and lineage update/delete trigger refusal (SQLite via real migration)
- two-operator list isolation (API)
- two-operator artifact lookup isolation (API)
- admin read_all path (API)
- sensitive-read audit persistence
- generic public permission denial
- safe V2 exception response (structured + internal-error containment)
- secret-classification write refusal (R-9.4)
- migration upgrade/downgrade, seed, and V2 drift-gate behaviour
"""

from __future__ import annotations

import os
import sqlite3
import subprocess
import sys
from collections.abc import AsyncIterator
from pathlib import Path
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select

from app.auth.security import hash_password
from app.db.models.operator import Operator
from app.db.models.v2_audit_event import V2AuditEvent
from app.db.models.v2_lineage_record import V2LineageRecord
from app.db.session import session_scope
from app.v2.audit.contract import V2AuditEventCreate
from app.v2.audit.repository import V2AuditRepository
from app.v2.errors.contract import AuditWriteRejectedError, V2Error, V2ErrorCode
from app.v2.lineage.contract import V2LineageRecordCreate
from app.v2.lineage.repository import V2LineageRepository

V2_PREFIX = "/api/v1/v2"
PASSWORD = "operator-pass-123"

BACKEND_DIR = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


async def _create_operator(role: str = "operator") -> tuple[str, str]:
    """Create an operator in the live test DB. Returns (id, username)."""
    async with session_scope() as session:
        operator = Operator(
            username=f"v2it-{role}-{uuid4().hex[:10]}",
            hashed_password=hash_password(PASSWORD),
            role=role,
            is_active=True,
        )
        session.add(operator)
        await session.flush()
        return operator.id, operator.username


async def _login(client: AsyncClient, username: str, password: str = PASSWORD) -> dict[str, str]:
    response = await client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": password},
    )
    assert response.status_code == 200, response.text
    token = response.json()["tokens"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


async def _admin_headers(client: AsyncClient) -> dict[str, str]:
    return await _login(client, "admin", "admin123")


async def _append_lineage(operator_id: str, artifact_type: str, artifact_id: str) -> str:
    async with session_scope() as session:
        record = await V2LineageRepository(session).append(
            V2LineageRecordCreate(
                artifact_type=artifact_type,
                artifact_id=artifact_id,
                source_artifact_ids=None,
                computation_version="v1",
                input_snapshot_id=None,
                operator_id=operator_id,
                mode="RESEARCH",
            )
        )
        return record.id


# ---------------------------------------------------------------------------
# 1–2. Audit/lineage append and persisted redaction (real DB)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_audit_append_persists_and_redacts_details(async_client: AsyncClient) -> None:
    """Audit append writes a row and stores redacted — not raw — details."""
    operator_id, _ = await _create_operator()
    async with session_scope() as session:
        created = await V2AuditRepository(session).append(
            V2AuditEventCreate(
                domain="v2.test",
                action="integration.append",
                actor_id=operator_id,
                actor_type="operator",
                mode="RESEARCH",
                operator_id=operator_id,
                classification="internal",
                details={"note": "password=SuperSecret123 attached"},
            )
        )
        event_id = created.id

    async with session_scope() as session:
        row = (
            await session.execute(select(V2AuditEvent).where(V2AuditEvent.id == event_id))
        ).scalar_one()
        assert row.action == "integration.append"
        stored = str(row.details)
        assert "SuperSecret123" not in stored
        assert "[REDACTED]" in stored


@pytest.mark.asyncio
async def test_lineage_append_persists_record(async_client: AsyncClient) -> None:
    operator_id, _ = await _create_operator()
    record_id = await _append_lineage(operator_id, "dataset_snapshot", f"ds-{uuid4().hex[:8]}")
    async with session_scope() as session:
        row = (
            await session.execute(
                select(V2LineageRecord).where(V2LineageRecord.id == record_id)
            )
        ).scalar_one()
        assert row.operator_id == operator_id
        assert row.mode == "RESEARCH"
        assert row.created_at.tzinfo is not None or row.created_at is not None


# ---------------------------------------------------------------------------
# 3. Secret-classification write refusal (R-9.4)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_audit_write_rejects_secret_classification(async_client: AsyncClient) -> None:
    """classification='secret' is refused; refusal does not echo any value."""
    operator_id, _ = await _create_operator()
    with pytest.raises(AuditWriteRejectedError) as excinfo:
        async with session_scope() as session:
            await V2AuditRepository(session).append(
                V2AuditEventCreate(
                    domain="v2.test",
                    action="integration.secret",
                    actor_id=operator_id,
                    actor_type="operator",
                    mode="RESEARCH",
                    operator_id=operator_id,
                    classification="secret",
                    details={"value": "top-secret-material"},
                )
            )
    assert "top-secret-material" not in str(excinfo.value)
    assert excinfo.value.code == V2ErrorCode.VALIDATION_FAILED


@pytest.mark.asyncio
async def test_audit_write_rejects_unredactable_secret_keys(async_client: AsyncClient) -> None:
    """Secret material embedded in dict keys cannot be redacted → refused."""
    operator_id, _ = await _create_operator()
    with pytest.raises(AuditWriteRejectedError) as excinfo:
        async with session_scope() as session:
            await V2AuditRepository(session).append(
                V2AuditEventCreate(
                    domain="v2.test",
                    action="integration.secret-key",
                    actor_id=operator_id,
                    actor_type="operator",
                    mode="RESEARCH",
                    operator_id=operator_id,
                    classification="internal",
                    details={"api_key=AKIA123SECRET": "present"},
                )
            )
    assert "AKIA123SECRET" not in str(excinfo.value)


@pytest.mark.asyncio
async def test_audit_write_rejects_unknown_classification(async_client: AsyncClient) -> None:
    operator_id, _ = await _create_operator()
    with pytest.raises(AuditWriteRejectedError):
        async with session_scope() as session:
            await V2AuditRepository(session).append(
                V2AuditEventCreate(
                    domain="v2.test",
                    action="integration.unknown",
                    actor_id=operator_id,
                    actor_type="operator",
                    mode="RESEARCH",
                    operator_id=operator_id,
                    classification="ultra",
                )
            )


# ---------------------------------------------------------------------------
# 4–5. Two-operator isolation: list and artifact lookup (API level)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_two_operator_lineage_list_isolation(async_client: AsyncClient) -> None:
    """Operator A's list never contains Operator B's lineage records."""
    a_id, a_name = await _create_operator()
    b_id, b_name = await _create_operator()
    a_artifact = f"art-a-{uuid4().hex[:8]}"
    b_artifact = f"art-b-{uuid4().hex[:8]}"
    await _append_lineage(a_id, "research_note", a_artifact)
    await _append_lineage(b_id, "research_note", b_artifact)

    headers_a = await _login(async_client, a_name)
    response = await async_client.get(f"{V2_PREFIX}/lineage", headers=headers_a)
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["scope"] == "operator"
    returned_operators = {r["operator_id"] for r in body["records"]}
    assert returned_operators <= {a_id}
    returned_artifacts = {r["artifact_id"] for r in body["records"]}
    assert b_artifact not in returned_artifacts


@pytest.mark.asyncio
async def test_two_operator_artifact_lookup_isolation(async_client: AsyncClient) -> None:
    """Operator A cannot retrieve Operator B's record via direct artifact path."""
    a_id, a_name = await _create_operator()
    b_id, b_name = await _create_operator()
    b_artifact = f"art-b-{uuid4().hex[:8]}"
    await _append_lineage(b_id, "research_note", b_artifact)

    headers_a = await _login(async_client, a_name)
    response = await async_client.get(
        f"{V2_PREFIX}/lineage/research_note/{b_artifact}", headers=headers_a
    )
    assert response.status_code == 200, response.text
    body = response.json()
    # No disclosure: the protected record is simply absent for A.
    assert body["records"] == []
    assert body["total"] == 0

    # Owner B still retrieves it.
    headers_b = await _login(async_client, b_name)
    response_b = await async_client.get(
        f"{V2_PREFIX}/lineage/research_note/{b_artifact}", headers=headers_b
    )
    assert response_b.status_code == 200
    assert response_b.json()["total"] == 1


@pytest.mark.asyncio
async def test_two_operator_audit_list_isolation(async_client: AsyncClient) -> None:
    a_id, a_name = await _create_operator()
    b_id, b_name = await _create_operator()
    async with session_scope() as session:
        await V2AuditRepository(session).append(
            V2AuditEventCreate(
                domain="v2.test",
                action="isolation.b-event",
                actor_id=b_id,
                actor_type="operator",
                mode="RESEARCH",
                operator_id=b_id,
                classification="internal",
            )
        )
    headers_a = await _login(async_client, a_name)
    response = await async_client.get(f"{V2_PREFIX}/audit", headers=headers_a)
    assert response.status_code == 200
    body = response.json()
    assert {e["operator_id"] for e in body["events"]} <= {a_id}


# ---------------------------------------------------------------------------
# 6. Admin read_all path
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_admin_read_all_lineage_and_operator_denied(async_client: AsyncClient) -> None:
    """Admin read_all returns cross-operator records; plain operator gets 403."""
    a_id, a_name = await _create_operator()
    b_id, _ = await _create_operator()
    await _append_lineage(a_id, "research_note", f"art-{uuid4().hex[:8]}")
    await _append_lineage(b_id, "research_note", f"art-{uuid4().hex[:8]}")

    admin = await _admin_headers(async_client)
    response = await async_client.get(f"{V2_PREFIX}/lineage/all", headers=admin)
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["scope"] == "all"
    operators_seen = {r["operator_id"] for r in body["records"]}
    assert {a_id, b_id} <= operators_seen

    headers_a = await _login(async_client, a_name)
    denied = await async_client.get(f"{V2_PREFIX}/lineage/all", headers=headers_a)
    assert denied.status_code == 403


@pytest.mark.asyncio
async def test_admin_read_all_audit(async_client: AsyncClient) -> None:
    admin = await _admin_headers(async_client)
    response = await async_client.get(f"{V2_PREFIX}/audit/all", headers=admin)
    assert response.status_code == 200, response.text
    assert response.json()["scope"] == "all"


# ---------------------------------------------------------------------------
# 7. Sensitive-read audit persistence
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_sensitive_read_creates_persisted_audit_event(async_client: AsyncClient) -> None:
    """Reading lineage produces a persisted audit record of the read itself."""
    a_id, a_name = await _create_operator()
    headers = await _login(async_client, a_name)
    response = await async_client.get(f"{V2_PREFIX}/lineage", headers=headers)
    assert response.status_code == 200

    async with session_scope() as session:
        rows = (
            await session.execute(
                select(V2AuditEvent).where(
                    V2AuditEvent.operator_id == a_id,
                    V2AuditEvent.action == "lineage.read_own",
                )
            )
        ).scalars().all()
        assert rows, "sensitive read was not audited"
        assert rows[0].domain == "v2.lineage"
        assert rows[0].classification == "confidential"


# ---------------------------------------------------------------------------
# 8. Classification/clearance enforcement through the API (DEF-BE1-03)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_confidential_details_redacted_for_operator_visible_to_admin(
    async_client: AsyncClient,
) -> None:
    """Operator clearance is internal: confidential details are redacted in
    the operator's own reads while admin clearance sees them."""
    a_id, a_name = await _create_operator()
    marker = f"detail-{uuid4().hex[:8]}"
    async with session_scope() as session:
        await V2AuditRepository(session).append(
            V2AuditEventCreate(
                domain="v2.test",
                action="classified.event",
                actor_id=a_id,
                actor_type="operator",
                mode="RESEARCH",
                operator_id=a_id,
                classification="confidential",
                details={"marker": marker},
            )
        )

    headers_a = await _login(async_client, a_name)
    own = await async_client.get(f"{V2_PREFIX}/audit", headers=headers_a)
    assert own.status_code == 200
    own_events = [e for e in own.json()["events"] if e["action"] == "classified.event"]
    assert own_events, "operator's own event missing from list"
    assert own_events[0]["details"].get("_redacted") is True
    assert marker not in str(own_events[0]["details"])

    admin = await _admin_headers(async_client)
    all_events = await async_client.get(
        f"{V2_PREFIX}/audit/all", headers=admin, params={"limit": 100}
    )
    assert all_events.status_code == 200
    admin_view = [
        e for e in all_events.json()["events"] if e["action"] == "classified.event"
    ]
    assert admin_view, "admin view missing the event"
    assert admin_view[0]["details"].get("marker") == marker


# ---------------------------------------------------------------------------
# 9. Generic public permission denial (DEF-BE1-04)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_permission_denial_is_generic_and_leaks_no_vocabulary(
    async_client: AsyncClient,
) -> None:
    """Denied responses carry only 'Permission denied' — no permission names."""
    _, unpriv_name = await _create_operator(role="unprivileged")
    headers = await _login(async_client, unpriv_name)

    for route in ("/mode", "/capabilities", "/audit", "/lineage", "/errors"):
        response = await async_client.get(f"{V2_PREFIX}{route}", headers=headers)
        assert response.status_code == 403, f"{route} -> {response.status_code}"
        body_text = response.text
        assert response.json()["detail"] == "Permission denied"
        assert "v2." not in body_text, f"permission vocabulary leaked on {route}"
        assert "read_all" not in body_text

    _, op_name = await _create_operator()
    op_headers = await _login(async_client, op_name)
    for route in ("/audit/all", "/lineage/all"):
        response = await async_client.get(f"{V2_PREFIX}{route}", headers=op_headers)
        assert response.status_code == 403
        assert response.json()["detail"] == "Permission denied"
        assert "v2." not in response.text


# ---------------------------------------------------------------------------
# 10. Mode integrity through the API
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_mode_endpoint_ignores_client_injection_headers(
    async_client: AsyncClient,
) -> None:
    """Client headers/query cannot alter the effective mode."""
    _, op_name = await _create_operator()
    headers = await _login(async_client, op_name)
    headers.update({"X-AXIOM-MODE": "LIVE", "X-Mode": "PAPER"})
    response = await async_client.get(
        f"{V2_PREFIX}/mode", headers=headers, params={"mode": "LIVE"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["mode"] in ("RESEARCH", "SIMULATION")
    assert body["mode"] != "LIVE"
    assert body["immutable_at_runtime"] is True
    assert body["source"] == "AXIOM_V2_MODE"


# ---------------------------------------------------------------------------
# 11. Response envelope contract (DEF-BE1-06)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_all_v2_endpoints_include_mode_correlation_timestamp(
    async_client: AsyncClient,
) -> None:
    _, op_name = await _create_operator()
    headers = await _login(async_client, op_name)
    for route in ("/mode", "/capabilities", "/audit", "/lineage", "/errors"):
        response = await async_client.get(f"{V2_PREFIX}{route}", headers=headers)
        assert response.status_code == 200, f"{route} -> {response.status_code}"
        body = response.json()
        assert "mode" in body, route
        assert "correlation_id" in body, route
        assert "timestamp" in body, route


# ---------------------------------------------------------------------------
# 12. Safe V2 exception responses (DEF-BE1-05)
# ---------------------------------------------------------------------------


@pytest_asyncio.fixture
async def error_probe_client() -> AsyncIterator[AsyncClient]:
    """App instance with test-only V2-path routes that raise exceptions.

    Isolation law (ITRGA-CB-V2-0047-SUITE-ISOLATION-001): create_app()
    registers a SPA catch-all route (`/{full_path:path}`, endpoint name
    `spa_fallback`) ONLY when frontend/dist/index.html exists — mandatory
    on the operator terminal workstation, absent on CI. Starlette matches
    in registration order, so the catch-all (registered inside
    create_app()) would shadow the probe routes added below and serve
    index.html with HTTP 200 instead of propagating the raise. The probe
    app is a throwaway instance, so we neutralize any registered
    spa_fallback route ON THIS INSTANCE ONLY — create_app() and the SPA
    fallback semantics (contracted product behavior for the terminal UI)
    are untouched. This makes both DEF-BE1-05 tests deterministic with
    the dist present AND absent (R-1/R-2 of the brief).
    """
    from app.core.config import clear_settings_cache
    from app.main import create_app

    clear_settings_cache()
    application = create_app()

    application.router.routes[:] = [
        route
        for route in application.router.routes
        if getattr(route, "name", None) != "spa_fallback"
    ]

    @application.get("/api/v1/v2/_test/raise-v2error", include_in_schema=False)
    async def _raise_v2_error():  # pragma: no cover - exercised via HTTP
        raise V2Error(code=V2ErrorCode.DATA_UNAVAILABLE, detail="Data unavailable", status_code=503)

    @application.get("/api/v1/v2/_test/raise-internal", include_in_schema=False)
    async def _raise_internal():  # pragma: no cover - exercised via HTTP
        raise RuntimeError("internal-detail-that-must-not-leak")

    transport = ASGITransport(app=application)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        async with application.router.lifespan_context(application):
            yield ac


@pytest.mark.asyncio
async def test_v2_error_returns_structured_safe_contract(
    error_probe_client: AsyncClient,
) -> None:
    response = await error_probe_client.get("/api/v1/v2/_test/raise-v2error")
    assert response.status_code == 503
    body = response.json()
    assert body["error_code"] == "data.unavailable"
    assert body["detail"] == "Data unavailable"
    assert "correlation_id" in body
    assert "timestamp" in body


@pytest.mark.asyncio
async def test_v2_internal_error_is_contained_and_safe(
    error_probe_client: AsyncClient,
) -> None:
    """Unhandled exceptions on V2 routes return the safe internal contract:
    no stack trace, no exception detail, no internal vocabulary."""
    response = await error_probe_client.get("/api/v1/v2/_test/raise-internal")
    assert response.status_code == 500
    body = response.json()
    assert body["error_code"] == "internal.error"
    assert body["detail"] == "Internal server error"
    text = response.text
    assert "internal-detail-that-must-not-leak" not in text
    assert "RuntimeError" not in text
    assert "Traceback" not in text


# ---------------------------------------------------------------------------
# 13. Migration lifecycle, seeds, triggers, mutation refusal, drift gate
#     (real Alembic chain on a dedicated file-based SQLite database)
# ---------------------------------------------------------------------------


def _run_alembic(args: list[str], db_url: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["AXIOM_DATABASE_URL"] = db_url
    env.setdefault("AXIOM_ENVIRONMENT", "testing")
    env.setdefault("AXIOM_ALLOW_INSECURE_DEV", "true")
    env.setdefault("AXIOM_JWT_SECRET_KEY", "test-secret-key-at-least-32-chars-long!!")
    return subprocess.run(
        [sys.executable, "-m", "alembic", *args],
        cwd=BACKEND_DIR,
        env=env,
        capture_output=True,
        text=True,
        timeout=600,
    )


def test_migration_lifecycle_triggers_seeds_mutation_refusal_and_drift_gate(
    tmp_path: Path,
) -> None:
    db_file = tmp_path / "v2_migration_verify.db"
    db_url = f"sqlite+aiosqlite:///{db_file}"

    # -- upgrade to head ----------------------------------------------------
    # Generational scope: pin to the pre-transition head (20260825_0041) —
    # the 0042 transition migration refuses without its authority gate by
    # design (BO-V2-BE-3-P2-TRANS-001) and has its own lifecycle tests.
    upgrade = _run_alembic(["upgrade", "20260825_0041"], db_url)
    assert upgrade.returncode == 0, f"upgrade failed:\n{upgrade.stderr}"

    conn = sqlite3.connect(db_file)
    try:
        cur = conn.cursor()

        # V2 tables exist
        # BE-1 object scope: BE-2 (20260824_0039) adds v2_md_* tables at
        # head; this BE-1 test asserts only the BE-1 set is present.
        tables = {
            row[0]
            for row in cur.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
                " AND name LIKE 'v2_%' AND name NOT LIKE 'v2_md_%'"
            )
        }
        assert tables == {
            "v2_audit_event",
            "v2_lineage_record",
            "v2_capability_record",
            "v2_permission",
        }, tables

        # Immutability triggers exist
        triggers = {
            row[0]
            for row in cur.execute(
                "SELECT name FROM sqlite_master WHERE type='trigger'"
                " AND name LIKE 'v2_%' AND name NOT LIKE 'v2_md_%'"
            )
        }
        assert triggers == {
            "v2_audit_immutable_update",
            "v2_audit_immutable_delete",
            "v2_lineage_immutable_update",
            "v2_lineage_immutable_delete",
        }, triggers

        # Seeds are present
        cap_count = cur.execute("SELECT COUNT(*) FROM v2_capability_record").fetchone()[0]
        perm_count = cur.execute("SELECT COUNT(*) FROM v2_permission").fetchone()[0]
        assert cap_count > 0
        assert perm_count > 0

        # -- mutation refusal: audit ---------------------------------------
        cur.execute(
            "INSERT INTO v2_audit_event (id, correlation_id, actor_id, actor_type,"
            " domain, action, mode, classification, created_at)"
            " VALUES ('t-audit-1', 'c-1', 'op-1', 'operator', 'v2.test', 'trigger.test',"
            " 'RESEARCH', 'internal', '2026-08-24 00:00:00+00:00')"
        )
        conn.commit()
        with pytest.raises(sqlite3.DatabaseError, match="immutable"):
            cur.execute("UPDATE v2_audit_event SET action='tampered' WHERE id='t-audit-1'")
        with pytest.raises(sqlite3.DatabaseError, match="immutable"):
            cur.execute("DELETE FROM v2_audit_event WHERE id='t-audit-1'")

        # -- mutation refusal: lineage ---------------------------------------
        cur.execute(
            "INSERT INTO v2_lineage_record (id, artifact_type, artifact_id,"
            " operator_id, mode, created_at)"
            " VALUES ('t-lin-1', 'research_note', 'art-1', 'op-1', 'RESEARCH',"
            " '2026-08-24 00:00:00+00:00')"
        )
        conn.commit()
        with pytest.raises(sqlite3.DatabaseError, match="immutable"):
            cur.execute("UPDATE v2_lineage_record SET artifact_id='tampered' WHERE id='t-lin-1'")
        with pytest.raises(sqlite3.DatabaseError, match="immutable"):
            cur.execute("DELETE FROM v2_lineage_record WHERE id='t-lin-1'")
    finally:
        conn.close()

    # -- drift gate: no V2 operation may appear in alembic check ------------
    # Inherited V1 drift is a documented baseline and may cause a non-zero
    # exit; the BE-1 gate is that NO V2 table/index/column operation appears.
    check = _run_alembic(["check"], db_url)
    drift_output = (check.stdout + check.stderr).lower()
    assert "v2_audit_event" not in drift_output
    assert "v2_lineage_record" not in drift_output
    assert "v2_capability_record" not in drift_output
    assert "v2_permission" not in drift_output
    assert "ix_v2_" not in drift_output

    # -- downgrade removes tables and triggers ------------------------------
    downgrade = _run_alembic(["downgrade", "20260717_0037"], db_url)
    assert downgrade.returncode == 0, f"downgrade failed:\n{downgrade.stderr}"

    conn = sqlite3.connect(db_file)
    try:
        cur = conn.cursor()
        tables_after = {
            row[0]
            for row in cur.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'v2_%'"
            )
        }
        assert tables_after == set(), tables_after
        triggers_after = {
            row[0]
            for row in cur.execute(
                "SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE 'v2_%'"
            )
        }
        assert triggers_after == set(), triggers_after
    finally:
        conn.close()

    # -- re-upgrade works ----------------------------------------------------
    reupgrade = _run_alembic(["upgrade", "20260825_0041"], db_url)
    assert reupgrade.returncode == 0, f"re-upgrade failed:\n{reupgrade.stderr}"
