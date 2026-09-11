"""V2 BE-3 P1 integration tests — read-only status APIs, no-write-path proof,
reserved source unemittable, default deny, migration lifecycle with
status-history trigger refusal (BO-V2-BE-3-P1-001 §4).
"""

from __future__ import annotations

import os
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
from app.db.models.v2_provider import V2MdProvider, V2MdProviderStatusHistory
from app.db.session import session_scope
from app.v2.temporal.validation import utc_now

MD = "/api/v1/v2/marketdata"
PASSWORD = "operator-pass-123"
BACKEND_DIR = Path(__file__).resolve().parents[1]


async def _operator(role: str = "operator") -> tuple[str, str]:
    async with session_scope() as session:
        op = Operator(
            username=f"be3-{role}-{uuid4().hex[:10]}",
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


async def _seed_provider() -> None:
    """Replay the migration's provider seed into the metadata-created test DB."""
    async with session_scope() as session:
        existing = await session.execute(select(func.count()).select_from(V2MdProvider))
        if int(existing.scalar_one()) > 0:
            return
        session.add(
            V2MdProvider(
                id=str(uuid4()),
                provider_id="twelvedata",
                display_name="Twelve Data (architecture candidate)",
                markets=["forex", "crypto", "metal"],
                entitlement=None,
                entitlement_status="unverified",
                persistence_permitted=False,
                source_status="architecture_candidate",
                created_at=utc_now(),
            )
        )
        session.add(
            V2MdProviderStatusHistory(
                id=str(uuid4()),
                provider_id="twelvedata",
                from_status=None,
                to_status="architecture_candidate",
                authority_ref="BO-V2-BE-3-P1-001",
                evidence_ref="AXIOM-V2-BE-3-DA-PLAN-001 v3.0.0",
                operator_id=None,
                created_at=utc_now(),
            )
        )


@pytest.mark.asyncio
async def test_provider_registry_truthful_and_read_only(async_client: AsyncClient) -> None:
    """Registry reports architecture_candidate/unverified; adapter existence
    changes nothing; there is no mutation endpoint."""
    await _seed_provider()
    _, name = await _operator()
    h = await _login(async_client, name)

    r = await async_client.get(f"{MD}/providers", headers=h)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["total"] == 1
    provider = body["providers"][0]
    assert provider["provider_id"] == "twelvedata"
    assert provider["source_status"] == "architecture_candidate"
    assert provider["entitlement_status"] == "unverified"
    assert provider["persistence_permitted"] is False
    assert {"mode", "correlation_id", "timestamp"} <= set(body)

    # No transition/write endpoint exists on the provider surface
    for method, path in (
        ("post", f"{MD}/providers"),
        ("put", f"{MD}/providers/twelvedata"),
        ("patch", f"{MD}/providers/twelvedata"),
        ("delete", f"{MD}/providers/twelvedata"),
        ("post", f"{MD}/providers/twelvedata/promote"),
        ("post", f"{MD}/providers/twelvedata/status"),
    ):
        resp = await getattr(async_client, method)(path, headers=h)
        assert resp.status_code in (404, 405), f"{method} {path} -> {resp.status_code}"


@pytest.mark.asyncio
async def test_provider_history_admin_only_and_audited(async_client: AsyncClient) -> None:
    await _seed_provider()
    _, name = await _operator()
    h = await _login(async_client, name)

    denied = await async_client.get(f"{MD}/providers/twelvedata/history", headers=h)
    assert denied.status_code == 403
    assert denied.json()["detail"] == "Permission denied"
    assert "v2." not in denied.text

    admin = await _login(async_client, "admin", "admin123")
    r = await async_client.get(f"{MD}/providers/twelvedata/history", headers=admin)
    assert r.status_code == 200, r.text
    history = r.json()["history"]
    assert len(history) == 1  # genesis row only in P1
    assert history[0]["to_status"] == "architecture_candidate"
    assert history[0]["from_status"] is None
    assert history[0]["authority_ref"] == "BO-V2-BE-3-P1-001"

    async with session_scope() as session:
        audits = (
            await session.execute(
                select(V2AuditEvent).where(V2AuditEvent.action == "provider.history_read")
            )
        ).scalars().all()
        assert audits


@pytest.mark.asyncio
async def test_reserved_provider_source_never_emitted_as_provider(
    async_client: AsyncClient,
) -> None:
    """The inactive reserved 'twelvedata' source row surfaces as honest
    unknown — no provider authority vocabulary exists anywhere in responses."""
    from app.db.models.v2_marketdata import V2MdSource

    async with session_scope() as session:
        existing = await session.execute(
            select(V2MdSource).where(V2MdSource.source_id == "twelvedata")
        )
        if existing.scalar_one_or_none() is None:
            session.add(
                V2MdSource(
                    id=str(uuid4()),
                    source_id="twelvedata",
                    kind="reserved",
                    authority="unknown",
                    mode_scope="RESEARCH",
                    active=False,
                    created_at=utc_now(),
                )
            )

    _, name = await _operator()
    h = await _login(async_client, name)
    r = await async_client.get(f"{MD}/sources", headers=h)
    assert r.status_code == 200
    assert "live:provider" not in r.text
    td = [s for s in r.json()["sources"] if s["source_id"] == "twelvedata"]
    assert td and td[0]["authority"] == "unknown" and td[0]["active"] is False


@pytest.mark.asyncio
async def test_provider_apis_default_deny(async_client: AsyncClient) -> None:
    await _seed_provider()
    _, name = await _operator(role="unprivileged")
    h = await _login(async_client, name)
    for path in (f"{MD}/providers", f"{MD}/providers/twelvedata/history"):
        r = await async_client.get(path, headers=h)
        assert r.status_code == 403, f"{path} -> {r.status_code}"
        assert r.json()["detail"] == "Permission denied"


@pytest.mark.asyncio
async def test_no_application_write_path_to_history(async_client: AsyncClient) -> None:
    """Static proof: no repository/service exposes a history append; the
    only V2MdProviderStatusHistory constructor calls live in the migration
    and test seeds."""
    import inspect

    import app.v2.marketdata.api.providers as providers_api

    src = inspect.getsource(providers_api)
    assert "session.add" not in src
    assert "insert(" not in src
    # and the marketdata package has no status-transition module
    providers_pkg = Path(providers_api.__file__).resolve().parents[1] / "providers"
    for py in providers_pkg.rglob("*.py"):
        text = py.read_text()
        assert "V2MdProviderStatusHistory(" not in text, f"write path in {py.name}"


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


def test_be3_migration_lifecycle(tmp_path: Path) -> None:
    db_file = tmp_path / "be3_migration_verify.db"
    db_url = f"sqlite+aiosqlite:///{db_file}"

    # BE-3 P1 generational scope: assert at the P1 revision (20260824_0040),
    # not head — the P2 entitlement migration (20260825_0041) legitimately
    # changes entitlement_status afterwards and has its own lifecycle test.
    upgrade = _run_alembic(["upgrade", "20260824_0040"], db_url)
    assert upgrade.returncode == 0, f"upgrade failed:\n{upgrade.stderr}"

    conn = sqlite3.connect(db_file)
    try:
        cur = conn.cursor()
        tables = {
            r[0]
            for r in cur.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'v2_md_provider%'"
            )
        }
        assert tables == {"v2_md_provider", "v2_md_provider_status_history"}, tables

        triggers = {
            r[0]
            for r in cur.execute(
                "SELECT name FROM sqlite_master WHERE type='trigger'"
                " AND name LIKE 'v2_md_provider%'"
            )
        }
        assert triggers == {
            "v2_md_provider_hist_immutable_update",
            "v2_md_provider_hist_immutable_delete",
            "v2_md_provider_immutable_update",
            "v2_md_provider_immutable_delete",
        }, triggers

        # seeds: one provider, one genesis history row, td source + 12 maps, 3 perms
        assert cur.execute("SELECT COUNT(*) FROM v2_md_provider").fetchone()[0] == 1
        assert (
            cur.execute("SELECT COUNT(*) FROM v2_md_provider_status_history").fetchone()[0] == 1
        )
        row = cur.execute(
            "SELECT provider_id, source_status, entitlement_status, persistence_permitted"
            " FROM v2_md_provider"
        ).fetchone()
        assert row == ("twelvedata", "architecture_candidate", "unverified", 0)
        assert (
            cur.execute(
                "SELECT COUNT(*) FROM v2_md_symbol_map WHERE source_id='twelvedata'"
            ).fetchone()[0]
            == 12
        )
        td_source = cur.execute(
            "SELECT kind, authority, active FROM v2_md_source WHERE source_id='twelvedata'"
        ).fetchone()
        assert td_source == ("reserved", "unknown", 0)
        # DEL-004 restored: at revision 20260824_0040 the P2 permission is
        # ABSENT — the historical 0038 seed is revision-local, so exactly the
        # three P1 provider permissions exist. Prove absence explicitly.
        assert (
            cur.execute(
                "SELECT COUNT(*) FROM v2_permission"
                " WHERE permission LIKE 'v2.marketdata.provider%'"
            ).fetchone()[0]
            == 3
        )
        assert (
            cur.execute(
                "SELECT COUNT(*) FROM v2_permission"
                " WHERE permission = 'v2.marketdata.provider.contract_test'"
            ).fetchone()[0]
            == 0
        ), "P2 permission must not exist at P1 revision (DEL-004)"

        # status CHECK refusal
        with pytest.raises(sqlite3.IntegrityError):
            cur.execute(
                "INSERT INTO v2_md_provider (id, provider_id, display_name, markets,"
                " entitlement_status, persistence_permitted, source_status, created_at)"
                " VALUES ('x','rogue','R','[]','unverified',0,'fully_live',"
                "'2026-08-24 00:00:00+00:00')"
            )

        # DEL-001: registry mutation refusal — status/entitlement/persistence
        for sql in (
            "UPDATE v2_md_provider SET source_status='integrated'"
            " WHERE provider_id='twelvedata'",
            "UPDATE v2_md_provider SET entitlement_status='verified'"
            " WHERE provider_id='twelvedata'",
            "UPDATE v2_md_provider SET persistence_permitted=1"
            " WHERE provider_id='twelvedata'",
            "DELETE FROM v2_md_provider WHERE provider_id='twelvedata'",
        ):
            with pytest.raises(sqlite3.DatabaseError, match="immutable"):
                cur.execute(sql)

        # history trigger refusal (genesis row immutable)
        hist_id = cur.execute(
            "SELECT id FROM v2_md_provider_status_history LIMIT 1"
        ).fetchone()[0]
        with pytest.raises(sqlite3.DatabaseError, match="immutable"):
            cur.execute(
                "UPDATE v2_md_provider_status_history SET to_status='integrated'"
                f" WHERE id='{hist_id}'"
            )
        with pytest.raises(sqlite3.DatabaseError, match="immutable"):
            cur.execute(f"DELETE FROM v2_md_provider_status_history WHERE id='{hist_id}'")
    finally:
        conn.close()

    # drift gate
    check = _run_alembic(["check"], db_url)
    drift = (check.stdout + check.stderr).lower()
    assert "v2_md_provider" not in drift, "BE-3 drift detected"

    # downgrade removes BE-3 objects; BE-2 intact
    downgrade = _run_alembic(["downgrade", "20260824_0039"], db_url)
    assert downgrade.returncode == 0, f"downgrade failed:\n{downgrade.stderr}"
    conn = sqlite3.connect(db_file)
    try:
        cur = conn.cursor()
        assert (
            cur.execute(
                "SELECT COUNT(*) FROM sqlite_master WHERE type='table'"
                " AND name LIKE 'v2_md_provider%'"
            ).fetchone()[0]
            == 0
        )
        assert (
            cur.execute(
                "SELECT COUNT(*) FROM v2_md_symbol_map WHERE source_id='twelvedata'"
            ).fetchone()[0]
            == 0
        )
        assert (
            cur.execute(
                "SELECT COUNT(*) FROM v2_permission"
                " WHERE permission LIKE 'v2.marketdata.provider%'"
            ).fetchone()[0]
            == 0
        )
        # BE-2 objects intact
        assert (
            cur.execute(
                "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name LIKE 'v2_md_%'"
            ).fetchone()[0]
            == 6
        )
    finally:
        conn.close()

    reupgrade = _run_alembic(["upgrade", "20260824_0040"], db_url)
    assert reupgrade.returncode == 0, f"re-upgrade failed:\n{reupgrade.stderr}"
