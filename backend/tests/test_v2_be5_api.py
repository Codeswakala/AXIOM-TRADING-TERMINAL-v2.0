"""V2 BE-5 API tests — BO-V2-BE-5-001 T-8/T-12 (writers, states, RBAC).

Socket guard active on every test (no network). Endpoint path:
``/api/v1/v2/research-governance/*``.
"""

from __future__ import annotations

import socket
from uuid import uuid4

import pytest
from httpx import AsyncClient
from sqlalchemy import select

from app.auth.security import hash_password
from app.db.models.operator import Operator
from app.db.models.v2_audit_event import V2AuditEvent
from app.db.models.v2_lineage_record import V2LineageRecord
from app.db.models.v2_research_governance import (
    V2MlGovernanceRecord,
    V2MlLifecycleEvent,
)
from app.db.models.v2_signal import V2SignalRecord, V2SignalStateEvent
from app.db.session import session_scope

RG = "/api/v1/v2/research-governance"
PASSWORD = "operator-pass-123"


@pytest.fixture(autouse=True)
def _socket_guard(monkeypatch):
    def _deny(*_a, **_k):
        raise AssertionError("network attempt during BE-5 test")

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


async def _make_operator(role: str = "operator") -> str:
    async with session_scope() as session:
        op = Operator(
            username=f"be5-{role}-{uuid4().hex[:10]}",
            hashed_password=hash_password(PASSWORD),
            role=role, is_active=True,
        )
        session.add(op)
        await session.flush()
        return op.username


async def _seed_governance(*, eligibility="eligible", deployment="research",
                           rollback="1.0.0", seq=1,
                           artifact_id: str | None = None,
                           model_type="classifier",
                           instrument_class="forex") -> str:
    async with session_scope() as session:
        rec = V2MlGovernanceRecord(
            model_artifact_id=artifact_id or str(uuid4()),
            record_seq=seq,
            registry_version="1.0",
            model_type=model_type,
            instrument_class=instrument_class,
            eligibility_status=eligibility,
            calibration_status="calibrated",
            freshness_status="fresh",
            economic_status="viable",
            statistical_status="significant",
            deployment_class=deployment,
            rollback_target_version=rollback,
            data_class="synthetic",
            evidence_refs={"reports": []},
            mode="RESEARCH",
            operator_id="seed",
        )
        session.add(rec)
        await session.flush()
        return rec.id


def _emit_body(**over) -> dict:
    body = {
        "family": "structural",
        "signal_type": "bos",
        "instrument_id": "forex.eurusd",
        "timeframe": "M15",
        "payload": {"direction": "up"},
        "limitations": {"scope": "pipeline-validation"},
        "source_family_refs": {"ids": ["obs-0001"]},
        "data_class": "synthetic",
        "as_of": "2026-09-02T10:00:00+00:00",
    }
    body.update(over)
    return body


# --- signal emission (T-8) ------------------------------------------------------


@pytest.mark.asyncio
async def test_structural_signal_emitted(prepared_db, async_client: AsyncClient) -> None:
    headers = await _admin(async_client)
    r = await async_client.post(f"{RG}/signals/emit", json=_emit_body(),
                                headers=headers)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["state"] == "emitted"
    assert body["reasons"] == []
    async with session_scope() as session:
        rec = (await session.execute(select(V2SignalRecord))).scalar_one()
        assert rec.family == "structural"
        assert rec.payload == {"direction": "up"}
        assert rec.uncertainty == {"basis": "deterministic"}
        events = (await session.execute(
            select(V2SignalStateEvent))).scalars().all()
        assert [e.to_state for e in events] == ["emitted"]
        audits = [a for (a,) in (await session.execute(
            select(V2AuditEvent.action).where(
                V2AuditEvent.domain == "v2.research_governance"))).all()]
        assert "signal.emitted" in audits
        lineage = (await session.execute(
            select(V2LineageRecord).where(
                V2LineageRecord.artifact_type == "signal_record"))).scalars().all()
        assert lineage and lineage[0].computation_version == "sge-1.0.0"


@pytest.mark.asyncio
async def test_predictive_without_governance_refused_permanent(
    prepared_db, async_client: AsyncClient
) -> None:
    headers = await _admin(async_client)
    r = await async_client.post(
        f"{RG}/signals/emit",
        json=_emit_body(family="predictive",
                        uncertainty={"interval": [0.4, 0.6]}),
        headers=headers)
    assert r.status_code == 200  # a refusal is a RECORD, not an HTTP error
    body = r.json()
    assert body["state"] == "refused"
    assert any(x.get("failing") == "governance_record_id" for x in body["reasons"])
    async with session_scope() as session:
        rec = (await session.execute(select(V2SignalRecord))).scalar_one()
        assert rec.state == "refused"       # permanent typed record
        assert rec.payload is None          # nothing fabricated
        assert rec.state_reason is not None


@pytest.mark.asyncio
async def test_predictive_with_eligible_governance_emitted(
    prepared_db, async_client: AsyncClient
) -> None:
    gov_id = await _seed_governance()
    headers = await _admin(async_client)
    r = await async_client.post(
        f"{RG}/signals/emit",
        json=_emit_body(family="predictive", governance_record_id=gov_id,
                        uncertainty={"interval": [0.4, 0.6],
                                     "confidence": 0.95}),
        headers=headers)
    assert r.json()["state"] == "emitted"


@pytest.mark.asyncio
async def test_predictive_ineligible_governance_refused(
    prepared_db, async_client: AsyncClient
) -> None:
    gov_id = await _seed_governance(eligibility="ineligible")
    headers = await _admin(async_client)
    r = await async_client.post(
        f"{RG}/signals/emit",
        json=_emit_body(family="predictive", governance_record_id=gov_id,
                        uncertainty={"interval": [0.4, 0.6]}),
        headers=headers)
    body = r.json()
    assert body["state"] == "refused"
    assert any("eligibility" in str(x) for x in body["reasons"])


@pytest.mark.asyncio
async def test_predictive_without_uncertainty_refused(
    prepared_db, async_client: AsyncClient
) -> None:
    gov_id = await _seed_governance()
    headers = await _admin(async_client)
    r = await async_client.post(
        f"{RG}/signals/emit",
        json=_emit_body(family="predictive", governance_record_id=gov_id),
        headers=headers)
    assert r.json()["state"] == "refused"


@pytest.mark.asyncio
async def test_historical_real_data_class_refused_first_landing(
    prepared_db, async_client: AsyncClient
) -> None:
    """Data honesty: historical_real unreachable until the corpus track."""
    headers = await _admin(async_client)
    r = await async_client.post(
        f"{RG}/signals/emit", json=_emit_body(data_class="historical_real"),
        headers=headers)
    body = r.json()
    assert body["state"] == "refused"
    assert any(x.get("failing") == "data_class" for x in body["reasons"])


@pytest.mark.asyncio
async def test_empty_source_refs_refused(prepared_db, async_client: AsyncClient) -> None:
    headers = await _admin(async_client)
    r = await async_client.post(
        f"{RG}/signals/emit", json=_emit_body(source_family_refs={}),
        headers=headers)
    assert r.json()["state"] == "refused"


@pytest.mark.asyncio
async def test_future_as_of_rejected(prepared_db, async_client: AsyncClient) -> None:
    headers = await _admin(async_client)
    r = await async_client.post(
        f"{RG}/signals/emit",
        json=_emit_body(as_of="2099-01-01T00:00:00+00:00"), headers=headers)
    assert r.status_code == 400


# --- promotion writer (T-7 at the API tier; P-1 row versioning) -------------------


@pytest.mark.asyncio
async def test_promotion_creates_versioned_row(
    prepared_db, async_client: AsyncClient
) -> None:
    gov_id = await _seed_governance()
    headers = await _admin(async_client)
    r = await async_client.post(
        f"{RG}/governance/promote",
        json={"governance_record_id": gov_id, "target_class": "shadow"},
        headers=headers)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["decision"] == "allowed"
    assert body["new_record_id"]
    async with session_scope() as session:
        rows = (await session.execute(
            select(V2MlGovernanceRecord).order_by(
                V2MlGovernanceRecord.record_seq))).scalars().all()
        assert len(rows) == 2                      # P-1: new row, no mutation
        assert rows[0].deployment_class == "research"  # original untouched
        assert rows[1].deployment_class == "shadow"
        assert rows[1].record_seq == rows[0].record_seq + 1
        assert rows[1].supersedes == rows[0].id  # backlink
        events = (await session.execute(
            select(V2MlLifecycleEvent))).scalars().all()
        assert any(e.event_type == "promoted" for e in events)
        promoted = [e for e in events if e.event_type == "promoted"][0]
        assert "Deployment Policy" in promoted.decision_basis["spec_citation"]


@pytest.mark.asyncio
async def test_promotion_refused_without_rollback(
    prepared_db, async_client: AsyncClient
) -> None:
    gov_id = await _seed_governance(rollback=None)
    headers = await _admin(async_client)
    r = await async_client.post(
        f"{RG}/governance/promote",
        json={"governance_record_id": gov_id, "target_class": "shadow"},
        headers=headers)
    body = r.json()
    assert body["decision"] == "refused"
    async with session_scope() as session:
        rows = (await session.execute(
            select(V2MlGovernanceRecord))).scalars().all()
        assert len(rows) == 1  # zero side effects on the record set
        events = (await session.execute(
            select(V2MlLifecycleEvent))).scalars().all()
        assert [e.event_type for e in events] == ["refused"]  # permanent typed
        audits = [a for (a,) in (await session.execute(
            select(V2AuditEvent.action).where(
                V2AuditEvent.action == "ml.promotion.refused"))).all()]
        assert audits


@pytest.mark.asyncio
async def test_champion_scope_at_most_one(
    prepared_db, async_client: AsyncClient
) -> None:
    """P-3: at most one champion per (model_type, instrument_class)."""
    headers = await _admin(async_client)
    # existing champion in the same scope
    await _seed_governance(deployment="champion",
                           model_type="classifier", instrument_class="forex")
    # candidate at shadow in the same scope
    candidate = await _seed_governance(deployment="shadow",
                                       model_type="classifier",
                                       instrument_class="forex")
    r = await async_client.post(
        f"{RG}/governance/promote",
        json={"governance_record_id": candidate, "target_class": "champion"},
        headers=headers)
    body = r.json()
    assert body["decision"] == "refused"
    assert any(x.get("failing") == "champion_scope" for x in body["reasons"])


@pytest.mark.asyncio
async def test_promotion_refused_ladder_skip(
    prepared_db, async_client: AsyncClient
) -> None:
    gov_id = await _seed_governance()  # research
    headers = await _admin(async_client)
    r = await async_client.post(
        f"{RG}/governance/promote",
        json={"governance_record_id": gov_id, "target_class": "champion"},
        headers=headers)
    assert r.json()["decision"] == "refused"


# --- reads + RBAC (T-8/T-12) -------------------------------------------------------


@pytest.mark.asyncio
async def test_reads_and_rbac(prepared_db, async_client: AsyncClient) -> None:
    await _seed_governance()
    admin = await _admin(async_client)
    operator = await _login(async_client, await _make_operator())

    # reads permitted for both roles
    for headers in (admin, operator):
        assert (await async_client.get(f"{RG}/governance",
                                       headers=headers)).status_code == 200
        assert (await async_client.get(f"{RG}/signals",
                                       headers=headers)).status_code == 200
        assert (await async_client.get(f"{RG}/diagnostics",
                                       headers=headers)).status_code == 200

    # writers denied for the operator role (default-deny; generic message)
    for path, body in (
        (f"{RG}/signals/emit", _emit_body()),
        (f"{RG}/governance/promote",
         {"governance_record_id": "x", "target_class": "shadow"}),
    ):
        r = await async_client.post(path, json=body, headers=operator)
        assert r.status_code == 403
        assert r.json()["detail"] == "Permission denied"

    # unauthenticated
    assert (await async_client.get(f"{RG}/governance")).status_code == 401


@pytest.mark.asyncio
async def test_governance_list_current_only_projection(
    prepared_db, async_client: AsyncClient
) -> None:
    artifact = str(uuid4())
    await _seed_governance(artifact_id=artifact, seq=1)
    headers = await _admin(async_client)
    r = await async_client.get(
        f"{RG}/governance", params={"model_artifact_id": artifact},
        headers=headers)
    body = r.json()
    assert body["total"] == 1
    assert body["records"][0]["record_seq"] == 1


@pytest.mark.asyncio
async def test_predictive_superseded_generation_refused(
    prepared_db, async_client: AsyncClient
) -> None:
    """C-1 currency projection: a governance row with a successor
    generation (greater record_seq) is not current — predictive emission
    against it is refused."""
    artifact = str(uuid4())
    old = await _seed_governance(artifact_id=artifact, seq=1)
    await _seed_governance(artifact_id=artifact, seq=2)
    headers = await _admin(async_client)
    r = await async_client.post(
        f"{RG}/signals/emit",
        json=_emit_body(family="predictive", governance_record_id=old,
                        uncertainty={"interval": [0.4, 0.6]}),
        headers=headers)
    body = r.json()
    assert body["state"] == "refused"
    assert any("superseded" in str(x) for x in body["reasons"])
