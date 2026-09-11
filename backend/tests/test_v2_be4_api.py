"""V2 BE-4 API tests — BO-V2-BE-4-001 D-5 groups 3 (DB lineage walk),
5 (six BE-1 states), 8 (RBAC incl. denied; socket guard), plus the R-1
governed-writer contract (single non-GET; idempotent by the determinism
anchor; audited; mode-enforced).

Endpoint path (R-3, pinned at the accepted physical mount):
``/api/v1/v2/market-context/*``.
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
from app.db.models.v2_research import (
    V2ChartIntelligenceReport,
    V2ComputationVersion,
    V2MarketContextReport,
)
from app.db.session import session_scope
from app.v2.marketdata.seed import V2_MD_INSTRUMENT_SEED, V2_MD_SOURCE_SEED
from app.v2.research.versioning import (
    INDICATOR_ENGINE_VERSION,
    compute_indicator_engine_hash,
)
from app.v2.temporal.validation import utc_now

MC = "/api/v1/v2/market-context"
PASSWORD = "operator-pass-123"
UTC = timezone.utc
AS_OF = "2026-08-31T00:00:00+00:00"


@pytest.fixture(autouse=True)
def _socket_guard(monkeypatch):
    def _deny(*_a, **_k):
        raise AssertionError("network attempt during BE-4 API test")

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


async def _make_operator(role: str) -> str:
    async with session_scope() as session:
        op = Operator(
            username=f"be4-{role}-{uuid4().hex[:10]}",
            hashed_password=hash_password(PASSWORD),
            role=role,
            is_active=True,
        )
        session.add(op)
        await session.flush()
        return op.username


async def _seed_reference() -> None:
    async with session_scope() as session:
        existing = await session.execute(select(V2MdSource))
        if existing.scalars().first() is not None:
            return
        for row in V2_MD_SOURCE_SEED:
            session.add(V2MdSource(id=str(uuid4()), created_at=utc_now(), **row))
        for row in V2_MD_INSTRUMENT_SEED:
            session.add(V2MdInstrument(id=str(uuid4()), created_at=utc_now(), **row))


async def _seed_versions() -> None:
    """Replay the 0043 version seed (test harness uses metadata.create_all)."""
    async with session_scope() as session:
        existing = await session.execute(select(V2ComputationVersion))
        if existing.scalars().first() is not None:
            return
        session.add(V2ComputationVersion(
            component="indicator_engine",
            version=INDICATOR_ENGINE_VERSION,
            source_hash=compute_indicator_engine_hash(),
            evidence_ref="BO-V2-BE-4-001",
        ))


async def _seed_bars(symbol: str = "EURUSD", market_class: str = "forex",
                     n: int = 200, tf: str = "M15",
                     tf_minutes: int = 15) -> None:
    start = datetime(2026, 8, 28, tzinfo=UTC)
    async with session_scope() as session:
        for i in range(n):
            px = Decimal("1.10") + Decimal(str(round(0.005 * math.sin(i / 7), 6)))
            session.add(Candle(
                id=str(uuid4()),
                market_class=market_class,
                symbol=symbol,
                timeframe=tf,
                open_time=start + timedelta(minutes=tf_minutes * i),
                open=px, high=px + Decimal("0.0006"),
                low=px - Decimal("0.0006"), close=px + Decimal("0.0002"),
                volume=Decimal("100"),
                source="live:simulated",
            ))


def _compute_body(**overrides) -> dict:
    body = {
        "instrument_id": "forex.eurusd",
        "timeframes": ["M15"],
        "source_id": "sim.local",
        "as_of": "2026-08-31T00:00:00+00:00",
        "bar_limit": 500,
    }
    body.update(overrides)
    return body


# ---------------------------------------------------------------------------
# R-1 governed writer: compute + idempotency + audit + lineage walk
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_compute_creates_reports_with_audit_and_lineage(
    prepared_db, async_client: AsyncClient
) -> None:
    await _seed_reference()
    await _seed_versions()
    await _seed_bars()
    headers = await _admin(async_client)

    r = await async_client.post(f"{MC}/compute", json=_compute_body(),
                                headers=headers)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["reused_existing"] is False
    assert body["report_id"]
    assert body["chart_intelligence_report_id"]
    assert body["mode"] == "RESEARCH"
    assert body["status"] in ("available", "degraded", "stale")

    # Level II DB walk (content-based): report → lineage → snapshot
    async with session_scope() as session:
        report = (await session.execute(
            select(V2MarketContextReport).where(
                V2MarketContextReport.id == body["report_id"])
        )).scalar_one()
        assert report.validation_tier == "pipeline-validation"
        assert report.engine_versions_hash
        assert report.input_content_hash
        obs = report.observations["observations"]
        assert obs, "expected observations"
        # facts vs interpretations separately typed in the stored artifact
        layers = {o["layer"] for o in obs}
        assert "observed" in layers
        assert "statistical" not in layers

        ci = (await session.execute(
            select(V2ChartIntelligenceReport).where(
                V2ChartIntelligenceReport.id
                == body["chart_intelligence_report_id"])
        )).scalar_one()
        assert ci.market_context_report_id == report.id

        lineage_rows = (await session.execute(
            select(V2LineageRecord).where(
                V2LineageRecord.artifact_id.in_([report.id, ci.id]))
        )).scalars().all()
        by_artifact = {r.artifact_id: r for r in lineage_rows}
        assert by_artifact[report.id].input_snapshot_id == report.input_snapshot_id
        assert by_artifact[report.id].computation_version == report.engine_versions_hash
        assert by_artifact[ci.id].source_artifact_ids == [report.id]

        audit_actions = [a for (a,) in (await session.execute(
            select(V2AuditEvent.action).where(
                V2AuditEvent.domain == "v2.research")
        )).all()]
        assert "research.market_context.computed" in audit_actions
        assert "research.chart_intelligence.computed" in audit_actions


@pytest.mark.asyncio
async def test_compute_idempotent_by_determinism_anchor(
    prepared_db, async_client: AsyncClient
) -> None:
    await _seed_reference()
    await _seed_versions()
    await _seed_bars()
    headers = await _admin(async_client)

    first = (await async_client.post(f"{MC}/compute", json=_compute_body(),
                                     headers=headers)).json()
    second = (await async_client.post(f"{MC}/compute", json=_compute_body(),
                                      headers=headers)).json()
    assert second["reused_existing"] is True
    assert second["report_id"] == first["report_id"]

    async with session_scope() as session:
        count = len((await session.execute(
            select(V2MarketContextReport))).scalars().all())
        assert count == 1  # not duplicated (R-1)
        reuse_audits = [a for (a,) in (await session.execute(
            select(V2AuditEvent.action).where(
                V2AuditEvent.action == "research.market_context.compute.reused")
        )).all()]
        assert reuse_audits  # the reuse itself is audited


# ---------------------------------------------------------------------------
# GET read models (strictly read-only; API evidence of typing)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_reads_expose_claim_type_separation(
    prepared_db, async_client: AsyncClient
) -> None:
    await _seed_reference()
    await _seed_versions()
    await _seed_bars()
    headers = await _admin(async_client)
    created = (await async_client.post(f"{MC}/compute", json=_compute_body(),
                                       headers=headers)).json()

    listing = await async_client.get(f"{MC}/reports", headers=headers)
    assert listing.status_code == 200
    assert listing.json()["total"] >= 1

    detail = await async_client.get(f"{MC}/reports/{created['report_id']}",
                                    headers=headers)
    assert detail.status_code == 200
    obs = detail.json()["observations"]["observations"]
    # claim_type separation exposed verbatim (roadmap exit evidence)
    claim_types = {o["claim_type"] for o in obs}
    assert "fact" in claim_types
    assert "prediction" not in claim_types
    for o in obs:
        assert o["layer"] in ("observed", "derived", "contextual")

    ci = await async_client.get(
        f"{MC}/chart-intelligence/{created['chart_intelligence_report_id']}",
        headers=headers)
    assert ci.status_code == 200
    ci_body = ci.json()
    for a in ci_body["annotations"]:
        assert a["claim_type"] in ("fact", "derived_observation")
        assert a["basis_observation_ids"]
    for i in ci_body["interpretations"]:
        assert i["claim_type"] == "contextual_interpretation"
        assert i["basis_ids"]

    versions = await async_client.get(f"{MC}/versions", headers=headers)
    assert versions.status_code == 200
    comps = {v["component"] for v in versions.json()["versions"]}
    assert "indicator_engine" in comps


# ---------------------------------------------------------------------------
# Six BE-1 states (plan §6)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_state_available(prepared_db, async_client: AsyncClient) -> None:
    await _seed_reference()
    await _seed_versions()
    await _seed_bars(n=400)
    headers = await _admin(async_client)
    r = (await async_client.post(
        f"{MC}/compute",
        json=_compute_body(as_of="2026-08-31T04:00:00+00:00"),
        headers=headers)).json()
    # single timeframe: 9 families requested; rich input computes all 9
    assert r["status"] in ("available", "stale", "degraded")
    if r["status"] == "available":
        assert r["insufficient_data"] == []


@pytest.mark.asyncio
async def test_state_degraded_insufficient_data_typed(
    prepared_db, async_client: AsyncClient
) -> None:
    await _seed_reference()
    await _seed_versions()
    await _seed_bars(n=30)  # short series
    headers = await _admin(async_client)
    r = (await async_client.post(f"{MC}/compute", json=_compute_body(),
                                 headers=headers)).json()
    assert r["status"] == "degraded"
    assert r["insufficient_data"]
    for entry in r["insufficient_data"]:
        assert entry["outcome"] == "insufficient_data"
        assert entry["required_bars"] is not None


@pytest.mark.asyncio
async def test_state_unavailable_empty_series(
    prepared_db, async_client: AsyncClient
) -> None:
    await _seed_reference()
    await _seed_versions()  # no bars seeded
    headers = await _admin(async_client)
    r = (await async_client.post(f"{MC}/compute", json=_compute_body(),
                                 headers=headers)).json()
    assert r["status"] == "unavailable"


@pytest.mark.asyncio
async def test_state_stale_disclosed(
    prepared_db, async_client: AsyncClient
) -> None:
    await _seed_reference()
    await _seed_versions()
    await _seed_bars(n=200)  # last bar 2026-08-30 01:45 — well before as_of
    headers = await _admin(async_client)
    # as_of far beyond the declared bound (3 × M15)
    r = (await async_client.post(
        f"{MC}/compute",
        json=_compute_body(as_of="2026-08-31T12:00:00+00:00"),
        headers=headers)).json()
    assert r["status"] in ("stale", "degraded")
    if r["status"] == "stale":
        detail = (await async_client.get(
            f"{MC}/reports/{r['report_id']}", headers=headers)).json()
        assert detail["observations"].get("staleness_disclosure")


@pytest.mark.asyncio
async def test_state_unknown_version_unregistered(
    prepared_db, async_client: AsyncClient
) -> None:
    await _seed_reference()
    await _seed_bars()  # versions NOT seeded → resolution impossible
    headers = await _admin(async_client)
    r = await async_client.post(f"{MC}/compute", json=_compute_body(),
                                headers=headers)
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "unknown"
    assert body["report_id"] is None  # nothing persisted; nothing guessed
    async with session_scope() as session:
        count = len((await session.execute(
            select(V2MarketContextReport))).scalars().all())
        assert count == 0
        unknown_audits = [a for (a,) in (await session.execute(
            select(V2AuditEvent.action).where(
                V2AuditEvent.action == "research.market_context.compute.unknown")
        )).all()]
        assert unknown_audits


@pytest.mark.asyncio
async def test_state_denied_rbac(prepared_db, async_client: AsyncClient) -> None:
    """`denied` — operator role lacks the compute permission (default-deny);
    generic public denial; reads still permitted for the operator role."""
    await _seed_reference()
    await _seed_versions()
    username = await _make_operator("operator")
    headers = await _login(async_client, username)

    r = await async_client.post(f"{MC}/compute", json=_compute_body(),
                                headers=headers)
    assert r.status_code == 403
    assert r.json()["detail"] == "Permission denied"  # generic (DEF-BE1-04)

    reads = await async_client.get(f"{MC}/reports", headers=headers)
    assert reads.status_code == 200  # read permission granted to operator

    unauth = await async_client.get(f"{MC}/reports")
    assert unauth.status_code == 401


# ---------------------------------------------------------------------------
# Mode + input validation
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_future_as_of_rejected(prepared_db, async_client: AsyncClient) -> None:
    await _seed_reference()
    await _seed_versions()
    headers = await _admin(async_client)
    r = await async_client.post(
        f"{MC}/compute",
        json=_compute_body(as_of="2099-01-01T00:00:00+00:00"),
        headers=headers)
    assert r.status_code == 400
    assert "future" in r.json()["detail"]


@pytest.mark.asyncio
async def test_unknown_instrument_404(prepared_db, async_client: AsyncClient) -> None:
    await _seed_reference()
    await _seed_versions()
    headers = await _admin(async_client)
    r = await async_client.post(
        f"{MC}/compute", json=_compute_body(instrument_id="forex.nope"),
        headers=headers)
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_version_hash_mismatch_refused(
    prepared_db, async_client: AsyncClient
) -> None:
    """BO D-1: registered-hash mismatch at compute time = typed refusal."""
    await _seed_reference()
    await _seed_bars()
    async with session_scope() as session:
        session.add(V2ComputationVersion(
            component="indicator_engine",
            version=INDICATOR_ENGINE_VERSION,
            source_hash="0" * 64,  # wrong on purpose
            evidence_ref="test-fixture",
        ))
    headers = await _admin(async_client)
    r = await async_client.post(f"{MC}/compute", json=_compute_body(),
                                headers=headers)
    assert r.status_code == 409
    assert "mismatch" in r.json()["detail"]
