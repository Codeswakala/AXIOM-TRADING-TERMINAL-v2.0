"""V2 BE-2 integration tests — real DB/API paths (BO-V2-BE-2-001 §4).

Covers: seed-matches-manifest; mandatory provenance; pure-GET repetition;
W-1 idempotency + fingerprint dedup; W-2 create/re-verify/match/mismatch +
reconstructive:false + audit + lineage; operator isolation; admin read_all +
sensitive-read audit; generic denial; failure states; migration lifecycle
with triggers/seeds/mutation refusal/drift gate/downgrade/re-upgrade.
"""

from __future__ import annotations

import os
import sqlite3
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path
from uuid import uuid4

import pytest
from httpx import AsyncClient
from sqlalchemy import func, select

from app.auth.security import hash_password
from app.db.models.candle import Candle
from app.db.models.operator import Operator
from app.db.models.v2_audit_event import V2AuditEvent
from app.db.models.v2_lineage_record import V2LineageRecord
from app.db.models.v2_marketdata import (
    V2MdAsOfVerification,
    V2MdInstrument,
    V2MdIntegrityException,
    V2MdSeries,
    V2MdSource,
    V2MdSymbolMap,
)
from app.db.session import session_scope
from app.v2.marketdata.seed import (
    SEED_MANIFEST_HASH,
    V2_MD_INSTRUMENT_SEED,
    V2_MD_SOURCE_SEED,
    V2_MD_SYMBOL_MAP_SEED,
    compute_seed_manifest_hash,
)

MD = "/api/v1/v2/marketdata"
PASSWORD = "operator-pass-123"
UTC = timezone.utc
BACKEND_DIR = Path(__file__).resolve().parents[1]


async def _operator(role: str = "operator") -> tuple[str, str]:
    async with session_scope() as session:
        op = Operator(
            username=f"be2-{role}-{uuid4().hex[:10]}",
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


async def _admin(client: AsyncClient) -> dict[str, str]:
    return await _login(client, "admin", "admin123")


async def _seed_reference_data() -> None:
    """Insert the BE-2 reference seed into the test DB (schema comes from
    metadata.create_all in the test harness, so the migration seed step must
    be replayed here from the same manifest module)."""
    from app.v2.temporal.validation import utc_now

    async with session_scope() as session:
        existing = await session.execute(select(func.count()).select_from(V2MdSource))
        if int(existing.scalar_one()) > 0:
            return
        for row in V2_MD_SOURCE_SEED:
            session.add(V2MdSource(id=str(uuid4()), created_at=utc_now(), **row))
        for row in V2_MD_INSTRUMENT_SEED:
            session.add(V2MdInstrument(id=str(uuid4()), created_at=utc_now(), **row))
        for row in V2_MD_SYMBOL_MAP_SEED:
            session.add(V2MdSymbolMap(id=str(uuid4()), created_at=utc_now(), **row))


async def _insert_bars(
    symbol: str,
    market_class: str,
    *,
    minutes: list[int],
    source: str = "live:simulated",
    base: str = "1.10000",
) -> None:
    async with session_scope() as session:
        for m in minutes:
            session.add(
                Candle(
                    id=str(uuid4()),
                    market_class=market_class,
                    symbol=symbol,
                    timeframe="M1",
                    open_time=datetime(2026, 8, 24, 10, 0, tzinfo=UTC) + timedelta(minutes=m),
                    open=Decimal(base),
                    high=Decimal(base) + Decimal("0.001"),
                    low=Decimal(base) - Decimal("0.001"),
                    close=Decimal(base),
                    volume=Decimal("100"),
                    source=source,
                )
            )


async def _count(model) -> int:
    async with session_scope() as session:
        result = await session.execute(select(func.count()).select_from(model))
        return int(result.scalar_one())


# ---------------------------------------------------------------------------
# Seed / reference data
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_seed_matches_manifest_and_hash(async_client: AsyncClient) -> None:
    """DB reference contents match the versioned seed module + manifest hash."""
    await _seed_reference_data()
    assert compute_seed_manifest_hash() == SEED_MANIFEST_HASH
    async with session_scope() as session:
        sources = (await session.execute(select(V2MdSource))).scalars().all()
        instruments = (await session.execute(select(V2MdInstrument))).scalars().all()
        maps = (await session.execute(select(V2MdSymbolMap))).scalars().all()
    assert {s.source_id for s in sources} == {r["source_id"] for r in V2_MD_SOURCE_SEED}
    assert {i.instrument_id for i in instruments} == {
        r["instrument_id"] for r in V2_MD_INSTRUMENT_SEED
    }
    assert len(maps) == len(V2_MD_SYMBOL_MAP_SEED)
    # No reserved/import source seeded; all active authorities authorized-only
    assert all(s.kind in ("simulator", "seed") for s in sources)
    assert all(s.authority in ("seed:synthetic", "live:simulated") for s in sources)


@pytest.mark.asyncio
async def test_reference_reads_and_provenance_mandatory(async_client: AsyncClient) -> None:
    await _seed_reference_data()
    _, name = await _operator()
    h = await _login(async_client, name)

    r = await async_client.get(f"{MD}/instruments", headers=h)
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == len(V2_MD_INSTRUMENT_SEED)
    assert {"mode", "correlation_id", "timestamp"} <= set(body)

    r2 = await async_client.get(f"{MD}/sources", headers=h)
    assert r2.status_code == 200
    for s in r2.json()["sources"]:
        assert s["display_label"]  # mandatory label
        assert s["authority"] in ("seed:synthetic", "live:simulated")


# ---------------------------------------------------------------------------
# Bars: provenance, availability, gaps disclosed, failure states
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_bars_response_carries_mandatory_provenance(async_client: AsyncClient) -> None:
    await _seed_reference_data()
    await _insert_bars("EURUSD", "forex", minutes=[0, 1, 2])
    _, name = await _operator()
    h = await _login(async_client, name)
    r = await async_client.get(f"{MD}/series/forex.eurusd/M1/bars", headers=h)
    assert r.status_code == 200
    body = r.json()
    prov = body["provenance"]
    assert prov["authority"] == "live:simulated"
    assert prov["display_label"] == "SIMULATED"
    assert prov["source_id"] == "sim.local"
    assert body["availability"] == "available"
    assert body["total"] == 3
    assert body["gaps_disclosed"] == []


@pytest.mark.asyncio
async def test_bars_gaps_disclosed_never_filled(async_client: AsyncClient) -> None:
    await _seed_reference_data()
    await _insert_bars("GBPUSD", "forex", minutes=[0, 1, 4], base="1.27000")
    _, name = await _operator()
    h = await _login(async_client, name)
    r = await async_client.get(f"{MD}/series/forex.gbpusd/M1/bars", headers=h)
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 3  # gaps NOT filled
    assert len(body["gaps_disclosed"]) == 2  # minutes 2 and 3 disclosed
    assert body["availability"] == "partial"


@pytest.mark.asyncio
async def test_bars_failure_states(async_client: AsyncClient) -> None:
    await _seed_reference_data()
    _, name = await _operator()
    h = await _login(async_client, name)

    # empty series → honest empty, not fabrication
    r = await async_client.get(f"{MD}/series/forex.usdchf/M1/bars", headers=h)
    assert r.status_code == 200
    assert r.json()["availability"] == "empty"
    assert r.json()["bars"] == []

    # unknown instrument → 404 generic
    r2 = await async_client.get(f"{MD}/series/forex.zzz/M1/bars", headers=h)
    assert r2.status_code == 404

    # unknown source → 404 generic
    r3 = await async_client.get(
        f"{MD}/series/forex.eurusd/M1/bars", headers=h, params={"source_id": "vendor.x"}
    )
    assert r3.status_code == 404

    # future as_of refused
    future = (datetime.now(UTC) + timedelta(days=1)).isoformat()
    r4 = await async_client.get(
        f"{MD}/series/forex.eurusd/M1/bars", headers=h, params={"as_of": future}
    )
    assert r4.status_code == 400

    # invalid timeframe refused via V2 error contract
    r5 = await async_client.get(f"{MD}/series/forex.eurusd/M7/bars", headers=h)
    assert r5.status_code in (400, 422)


# ---------------------------------------------------------------------------
# Pure-GET repetition (D.0 Rule 1)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_pure_get_repetition_creates_zero_state(async_client: AsyncClient) -> None:
    """N identical GETs across every read endpoint → zero BE-2 domain writes."""
    await _seed_reference_data()
    await _insert_bars("USDJPY", "forex", minutes=[0, 1, 5], base="150.000")
    _, name = await _operator()
    h = await _login(async_client, name)

    before = (
        await _count(V2MdSeries),
        await _count(V2MdIntegrityException),
        await _count(V2MdAsOfVerification),
    )
    for _ in range(5):
        for path in (
            f"{MD}/instruments",
            f"{MD}/sources",
            f"{MD}/series",
            f"{MD}/series/forex.usdjpy/M1/bars",  # has a gap → still no writes
            f"{MD}/integrity/exceptions",
            f"{MD}/verification",
        ):
            r = await async_client.get(path, headers=h)
            assert r.status_code == 200, f"{path} -> {r.status_code}"
    after = (
        await _count(V2MdSeries),
        await _count(V2MdIntegrityException),
        await _count(V2MdAsOfVerification),
    )
    assert before == after, "GET endpoints mutated BE-2 state"


# ---------------------------------------------------------------------------
# W-1 catalog refresh: idempotency + fingerprint dedup
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_w1_catalog_refresh_idempotent_and_deduplicated(
    async_client: AsyncClient,
) -> None:
    await _seed_reference_data()
    await _insert_bars("AUDUSD", "forex", minutes=[0, 1, 4], base="0.66000")  # gap
    admin = await _admin(async_client)

    r1 = await async_client.post(f"{MD}/catalog/refresh", headers=admin)
    assert r1.status_code == 200, r1.text
    b1 = r1.json()
    assert b1["series_created"] >= 1
    assert b1["exceptions_appended"] >= 2  # two missing periods

    # identical re-run: nothing new appended, dedup counted
    r2 = await async_client.post(f"{MD}/catalog/refresh", headers=admin)
    b2 = r2.json()
    assert b2["series_created"] == 0
    assert b2["exceptions_appended"] == 0
    assert b2["exceptions_deduplicated"] >= 2
    assert b2["series_unchanged"] >= 1

    # exception rows are unique by fingerprint
    async with session_scope() as session:
        rows = (
            (await session.execute(select(V2MdIntegrityException))).scalars().all()
        )
        fingerprints = [r.fingerprint for r in rows]
        assert len(fingerprints) == len(set(fingerprints))

    # audit event persisted for the refresh
    async with session_scope() as session:
        audits = (
            await session.execute(
                select(V2AuditEvent).where(V2AuditEvent.action == "catalog.refresh")
            )
        ).scalars().all()
        assert len(audits) >= 2


@pytest.mark.asyncio
async def test_w1_denied_for_plain_operator(async_client: AsyncClient) -> None:
    await _seed_reference_data()
    _, name = await _operator()
    h = await _login(async_client, name)
    r = await async_client.post(f"{MD}/catalog/refresh", headers=h)
    assert r.status_code == 403
    assert r.json()["detail"] == "Permission denied"
    assert "v2." not in r.text


# ---------------------------------------------------------------------------
# W-2 verification: create / re-verify / mismatch / contract truthfulness
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_w2_verification_lifecycle_match_and_mismatch(
    async_client: AsyncClient,
) -> None:
    await _seed_reference_data()
    await _insert_bars("NZDUSD", "forex", minutes=[0, 1, 2], base="0.61000")
    op_id, name = await _operator()
    h = await _login(async_client, name)

    as_of = datetime.now(UTC).isoformat()
    create = await async_client.post(
        f"{MD}/verification",
        headers=h,
        json={
            "scope": [
                {"instrument_id": "forex.nzdusd", "timeframe": "M1", "source_id": "sim.local"}
            ],
            "as_of": as_of,
        },
    )
    assert create.status_code == 200, create.text
    record = create.json()["record"]
    vid = record["verification_id"]

    # truthful contract: verification-only, not reconstructive
    assert record["reconstructive"] is False
    assert record["capability"] == "verification-only"
    assert record["row_count"] == 3

    # lineage + audit persisted
    async with session_scope() as session:
        lineage = (
            await session.execute(
                select(V2LineageRecord).where(V2LineageRecord.artifact_id == vid)
            )
        ).scalars().all()
        assert lineage and lineage[0].artifact_type == "md_asof_verification"
        audits = (
            await session.execute(
                select(V2AuditEvent).where(
                    V2AuditEvent.action == "verification.create",
                    V2AuditEvent.resource_id == vid,
                )
            )
        ).scalars().all()
        assert audits

    # re-verify: match
    verify1 = await async_client.post(f"{MD}/verification/{vid}/verify", headers=h)
    assert verify1.status_code == 200
    assert verify1.json()["match"] is True
    assert verify1.json()["reconstructive"] is False

    # tamper with an underlying V1 row (simulating store mutation)
    async with session_scope() as session:
        row = (
            await session.execute(
                select(Candle).where(Candle.symbol == "NZDUSD").limit(1)
            )
        ).scalars().first()
        row.close = Decimal("9.99999")
        await session.flush()

    # re-verify: mismatch detected + one deduplicated exception
    verify2 = await async_client.post(f"{MD}/verification/{vid}/verify", headers=h)
    assert verify2.status_code == 200
    assert verify2.json()["match"] is False

    verify3 = await async_client.post(f"{MD}/verification/{vid}/verify", headers=h)
    assert verify3.json()["match"] is False

    async with session_scope() as session:
        mismatches = (
            await session.execute(
                select(V2MdIntegrityException).where(
                    V2MdIntegrityException.exception_type == "verification_mismatch",
                    V2MdIntegrityException.series_ref == f"verification:{vid}",
                )
            )
        ).scalars().all()
        assert len(mismatches) == 1  # first-detection edge only; repeats deduplicated


@pytest.mark.asyncio
async def test_w2_rejects_future_as_of_and_bad_scope(async_client: AsyncClient) -> None:
    await _seed_reference_data()
    _, name = await _operator()
    h = await _login(async_client, name)
    future = (datetime.now(UTC) + timedelta(days=1)).isoformat()
    r = await async_client.post(
        f"{MD}/verification",
        headers=h,
        json={
            "scope": [
                {"instrument_id": "forex.eurusd", "timeframe": "M1", "source_id": "sim.local"}
            ],
            "as_of": future,
        },
    )
    assert r.status_code == 400
    r2 = await async_client.post(
        f"{MD}/verification",
        headers=h,
        json={
            "scope": [
                {"instrument_id": "forex.nope", "timeframe": "M1", "source_id": "sim.local"}
            ],
            "as_of": datetime.now(UTC).isoformat(),
        },
    )
    assert r2.status_code == 404


# ---------------------------------------------------------------------------
# Isolation / admin read_all / sensitive-read audit / denial
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_verification_two_operator_isolation_and_admin_read_all(
    async_client: AsyncClient,
) -> None:
    await _seed_reference_data()
    await _insert_bars("EURGBP", "forex", minutes=[0, 1], base="0.86000")
    a_id, a_name = await _operator()
    b_id, b_name = await _operator()
    ha = await _login(async_client, a_name)
    hb = await _login(async_client, b_name)

    payload = {
        "scope": [
            {"instrument_id": "forex.eurgbp", "timeframe": "M1", "source_id": "sim.local"}
        ],
        "as_of": datetime.now(UTC).isoformat(),
    }
    created = await async_client.post(f"{MD}/verification", headers=ha, json=payload)
    vid = created.json()["record"]["verification_id"]

    # B cannot list or fetch A's record
    lb = await async_client.get(f"{MD}/verification", headers=hb)
    assert vid not in {r["verification_id"] for r in lb.json()["records"]}
    gb = await async_client.get(f"{MD}/verification/{vid}", headers=hb)
    assert gb.status_code == 404  # no disclosure

    # B cannot re-verify A's record
    vb = await async_client.post(f"{MD}/verification/{vid}/verify", headers=hb)
    assert vb.status_code == 404

    # operator denied read_all with generic message
    denied = await async_client.get(f"{MD}/verification/all", headers=ha)
    assert denied.status_code == 403
    assert denied.json()["detail"] == "Permission denied"

    # admin read_all sees it; sensitive read audited
    admin = await _admin(async_client)
    all_r = await async_client.get(f"{MD}/verification/all", headers=admin)
    assert all_r.status_code == 200
    assert vid in {r["verification_id"] for r in all_r.json()["records"]}
    assert all_r.json()["reconstructive"] is False
    async with session_scope() as session:
        audits = (
            await session.execute(
                select(V2AuditEvent).where(
                    V2AuditEvent.action == "verification.read_all"
                )
            )
        ).scalars().all()
        assert audits


@pytest.mark.asyncio
async def test_integrity_exceptions_two_operator_isolation_and_admin_all(
    async_client: AsyncClient,
) -> None:
    """DEL-002: SAL-3 exception records are operator-owned; a second
    operator's read returns none of them; admin /all sees them and the
    sensitive read is audited."""
    await _seed_reference_data()
    await _insert_bars("USDCAD", "forex", minutes=[0, 1, 4], base="1.36000")  # gap
    admin = await _admin(async_client)
    # W-1 as admin → exception rows owned by the admin actor
    r = await async_client.post(f"{MD}/catalog/refresh", headers=admin)
    assert r.status_code == 200 and r.json()["exceptions_appended"] >= 2

    # a plain operator sees ZERO admin-owned exception records
    _, name = await _operator()
    h = await _login(async_client, name)
    own = await async_client.get(f"{MD}/integrity/exceptions", headers=h)
    assert own.status_code == 200
    assert own.json()["total"] == 0
    assert own.json()["exceptions"] == []

    # operator denied /all with generic message
    denied = await async_client.get(f"{MD}/integrity/exceptions/all", headers=h)
    assert denied.status_code == 403
    assert denied.json()["detail"] == "Permission denied"

    # admin /all sees the records; audit row persisted
    alla = await async_client.get(f"{MD}/integrity/exceptions/all", headers=admin)
    assert alla.status_code == 200 and alla.json()["total"] >= 2
    assert all("operator_id" in e for e in alla.json()["exceptions"])
    async with session_scope() as session:
        audits = (
            await session.execute(
                select(V2AuditEvent).where(V2AuditEvent.action == "integrity.read_all")
            )
        ).scalars().all()
        assert audits

    # series availability still honest for non-owners (non-disclosing flags)
    series = await async_client.get(f"{MD}/series", headers=h)
    cad = [x for x in series.json()["series"] if x["instrument_id"] == "forex.usdcad"]
    assert cad and cad[0]["availability"] == "partial"


@pytest.mark.asyncio
async def test_active_authority_enforced_at_db_and_sources_api(
    async_client: AsyncClient,
) -> None:
    """DEL-001: (a) DB CHECK refuses an ACTIVE source with reserved
    vocabulary; (b) an inactive reserved source is never emitted with
    reserved authority by the sources API — it surfaces as honest unknown."""
    await _seed_reference_data()
    from sqlalchemy.exc import IntegrityError

    from app.v2.temporal.validation import utc_now

    # (a) active + historical:imported → refused by ck_v2_md_source_active_authority
    with pytest.raises(IntegrityError):
        async with session_scope() as session:
            session.add(
                V2MdSource(
                    id=str(uuid4()),
                    source_id="import.rogue",
                    kind="import",
                    authority="historical:imported",
                    mode_scope="RESEARCH",
                    active=True,
                    created_at=utc_now(),
                )
            )
            await session.flush()

    # (b) INACTIVE reserved row is storable (taxonomy stability) but the API
    # must not emit its reserved vocabulary
    async with session_scope() as session:
        session.add(
            V2MdSource(
                id=str(uuid4()),
                source_id="import.reserved",
                kind="import",
                authority="historical:imported",
                mode_scope="RESEARCH",
                active=False,
                created_at=utc_now(),
            )
        )
        await session.flush()

    _, name = await _operator()
    h = await _login(async_client, name)
    r = await async_client.get(f"{MD}/sources", headers=h)
    assert r.status_code == 200
    body_text = r.text
    assert "historical:imported" not in body_text
    reserved = [x for x in r.json()["sources"] if x["source_id"] == "import.reserved"]
    assert reserved and reserved[0]["authority"] == "unknown"
    assert reserved[0]["active"] is False
    # active rows still emit their approved vocabulary
    sim = [x for x in r.json()["sources"] if x["source_id"] == "sim.local"]
    assert sim and sim[0]["authority"] == "live:simulated"


@pytest.mark.asyncio
async def test_unprivileged_role_default_deny_all_endpoints(
    async_client: AsyncClient,
) -> None:
    await _seed_reference_data()
    _, name = await _operator(role="unprivileged")
    h = await _login(async_client, name)
    for path in (
        f"{MD}/instruments",
        f"{MD}/sources",
        f"{MD}/series",
        f"{MD}/integrity/exceptions",
        f"{MD}/verification",
    ):
        r = await async_client.get(path, headers=h)
        assert r.status_code == 403, f"{path} -> {r.status_code}"
        assert r.json()["detail"] == "Permission denied"
        assert "v2." not in r.text


# ---------------------------------------------------------------------------
# Migration lifecycle: upgrade/seeds/triggers/mutation refusal/drift/downgrade
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


def test_be2_migration_lifecycle(tmp_path: Path) -> None:
    db_file = tmp_path / "be2_migration_verify.db"
    db_url = f"sqlite+aiosqlite:///{db_file}"

    # Generational scope: pin to the pre-transition head (20260825_0041);
    # 0042 refuses without its authority gate by design.
    upgrade = _run_alembic(["upgrade", "20260825_0041"], db_url)
    assert upgrade.returncode == 0, f"upgrade failed:\n{upgrade.stderr}"

    conn = sqlite3.connect(db_file)
    try:
        cur = conn.cursor()
        # BE-2 object scope: BE-3 (20260824_0040) adds v2_md_provider*
        # tables at head; this BE-2 test asserts only the BE-2 set.
        tables = {
            r[0]
            for r in cur.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
                " AND name LIKE 'v2_md_%' AND name NOT LIKE 'v2_md_provider%'"
            )
        }
        assert tables == {
            "v2_md_instrument",
            "v2_md_symbol_map",
            "v2_md_source",
            "v2_md_series",
            "v2_md_integrity_exception",
            "v2_md_asof_verification",
        }, tables

        triggers = {
            r[0]
            for r in cur.execute(
                "SELECT name FROM sqlite_master WHERE type='trigger'"
                " AND name LIKE 'v2_md_%' AND name NOT LIKE 'v2_md_provider%'"
            )
        }
        assert triggers == {
            "v2_md_integrity_immutable_update",
            "v2_md_integrity_immutable_delete",
            "v2_md_verification_immutable_update",
            "v2_md_verification_immutable_delete",
        }, triggers

        # seeds present and exactly the manifest inventory
        n_src = cur.execute(
            "SELECT COUNT(*) FROM v2_md_source WHERE source_id != 'twelvedata'"
        ).fetchone()[0]
        n_inst = cur.execute("SELECT COUNT(*) FROM v2_md_instrument").fetchone()[0]
        n_map = cur.execute(
            "SELECT COUNT(*) FROM v2_md_symbol_map WHERE source_id != 'twelvedata'"
        ).fetchone()[0]
        assert n_src == len(V2_MD_SOURCE_SEED)
        assert n_inst == len(V2_MD_INSTRUMENT_SEED)
        assert n_map == len(V2_MD_SYMBOL_MAP_SEED)
        # BE-2 permission rows seeded
        n_perm = cur.execute(
            "SELECT COUNT(*) FROM v2_permission WHERE permission LIKE 'v2.marketdata%'"
            " AND permission NOT LIKE 'v2.marketdata.provider%'"
        ).fetchone()[0]
        assert n_perm == 6

        # CHECK constraint enforcement: invalid authority refused
        with pytest.raises(sqlite3.IntegrityError):
            cur.execute(
                "INSERT INTO v2_md_source (id, source_id, kind, authority, mode_scope,"
                " active, created_at) VALUES ('x','bad.src','simulator','live:real',"
                "'RESEARCH',1,'2026-08-24 00:00:00+00:00')"
            )
        # DEL-001: ACTIVE source with reserved vocabulary refused
        with pytest.raises(sqlite3.IntegrityError):
            cur.execute(
                "INSERT INTO v2_md_source (id, source_id, kind, authority, mode_scope,"
                " active, created_at) VALUES ('y','rogue.src','import',"
                "'historical:imported','RESEARCH',1,'2026-08-24 00:00:00+00:00')"
            )
        # inactive reserved row permitted (taxonomy stability)
        cur.execute(
            "INSERT INTO v2_md_source (id, source_id, kind, authority, mode_scope,"
            " active, created_at) VALUES ('z','reserved.src','import',"
            "'historical:imported','RESEARCH',0,'2026-08-24 00:00:00+00:00')"
        )
        conn.commit()

        # mutation refusal on append-only tables
        cur.execute(
            "INSERT INTO v2_md_integrity_exception (id, series_ref, operator_id,"
            " exception_type, fingerprint, observed_at, mode, created_at) VALUES"
            " ('e1','s1','op-1','gap','fp1','2026-08-24 00:00:00+00:00','RESEARCH',"
            "'2026-08-24 00:00:00+00:00')"
        )
        conn.commit()
        with pytest.raises(sqlite3.DatabaseError, match="immutable"):
            cur.execute("UPDATE v2_md_integrity_exception SET series_ref='x' WHERE id='e1'")
        with pytest.raises(sqlite3.DatabaseError, match="immutable"):
            cur.execute("DELETE FROM v2_md_integrity_exception WHERE id='e1'")

        cur.execute(
            "INSERT INTO v2_md_asof_verification (id, verification_id, scope, as_of,"
            " content_hash, row_count, source_ids, mode, created_by_operator_id,"
            " created_at) VALUES ('v1','mdv-1','{}','2026-08-24 00:00:00+00:00','h',0,"
            "'[]','RESEARCH','op-1','2026-08-24 00:00:00+00:00')"
        )
        conn.commit()
        with pytest.raises(sqlite3.DatabaseError, match="immutable"):
            cur.execute("UPDATE v2_md_asof_verification SET content_hash='x' WHERE id='v1'")
        with pytest.raises(sqlite3.DatabaseError, match="immutable"):
            cur.execute("DELETE FROM v2_md_asof_verification WHERE id='v1'")

        # fingerprint uniqueness at DB level
        with pytest.raises(sqlite3.IntegrityError):
            cur.execute(
                "INSERT INTO v2_md_integrity_exception (id, series_ref, operator_id,"
                " exception_type, fingerprint, observed_at, mode, created_at) VALUES"
                " ('e2','s1','op-1','gap','fp1','2026-08-24 00:00:00+00:00','RESEARCH',"
                "'2026-08-24 00:00:00+00:00')"
            )
    finally:
        conn.close()

    # drift gate: no V2 operation may appear (inherited V1 drift only)
    check = _run_alembic(["check"], db_url)
    drift = (check.stdout + check.stderr).lower()
    for name in (
        "v2_md_instrument",
        "v2_md_symbol_map",
        "v2_md_source",
        "v2_md_series",
        "v2_md_integrity_exception",
        "v2_md_asof_verification",
        "ix_v2_md_",
    ):
        assert name not in drift, f"V2 drift detected: {name}"

    # downgrade removes everything; BE-1 head restored
    downgrade = _run_alembic(["downgrade", "20260823_0038"], db_url)
    assert downgrade.returncode == 0, f"downgrade failed:\n{downgrade.stderr}"
    conn = sqlite3.connect(db_file)
    try:
        cur = conn.cursor()
        tables_after = {
            r[0]
            for r in cur.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'v2_md_%'"
            )
        }
        assert tables_after == set()
        triggers_after = {
            r[0]
            for r in cur.execute(
                "SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE 'v2_md_%'"
            )
        }
        assert triggers_after == set()
        n_perm_after = cur.execute(
            "SELECT COUNT(*) FROM v2_permission WHERE permission LIKE 'v2.marketdata%'"
        ).fetchone()[0]
        assert n_perm_after == 0
        # BE-1 tables untouched
        be1 = cur.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name LIKE 'v2_%'"
        ).fetchone()[0]
        assert be1 >= 4
    finally:
        conn.close()

    reupgrade = _run_alembic(["upgrade", "20260825_0041"], db_url)
    assert reupgrade.returncode == 0, f"re-upgrade failed:\n{reupgrade.stderr}"
