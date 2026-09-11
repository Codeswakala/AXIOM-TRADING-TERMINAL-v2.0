"""V2 BE-7 queue/registry/API tests — BO-V2-BE-7-001 T-8/T-10/T-11
(U-3/U-4/U-5 budgets + conditions C1–C4 + the scan-token condition).

Socket guard on every test. Endpoint path: /api/v1/v2/research-jobs/*.
"""

from __future__ import annotations

import socket
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import select

from app.auth.security import hash_password
from app.db.models.candle import Candle
from app.db.models.operator import Operator
from app.db.models.v2_audit_event import V2AuditEvent
from app.db.models.v2_lineage_record import V2LineageRecord
from app.db.models.v2_marketdata import V2MdInstrument, V2MdSource
from app.db.models.v2_research_jobs import (
    V2CostModel,
    V2ResearchJob,
    V2ResearchJobAttempt,
    V2ResearchResult,
)
from app.db.session import session_scope
from app.v2.marketdata.seed import V2_MD_INSTRUMENT_SEED, V2_MD_SOURCE_SEED
from app.v2.temporal.validation import utc_now

RJ = "/api/v1/v2/research-jobs"
PASSWORD = "operator-pass-123"
UTC = timezone.utc
W_START = "2026-09-01T00:00:00+00:00"
W_END = "2026-09-02T00:00:00+00:00"


@pytest.fixture(autouse=True)
def _socket_guard(monkeypatch):
    def _deny(*_a, **_k):
        raise AssertionError("network attempt during BE-7 test")

    monkeypatch.setattr(socket, "getaddrinfo", _deny)
    monkeypatch.setattr(socket, "create_connection", _deny)


async def _login(client, username, password=PASSWORD):
    r = await client.post("/api/v1/auth/login",
                          json={"username": username, "password": password})
    assert r.status_code == 200, r.text
    return {"Authorization": f"Bearer {r.json()['tokens']['access_token']}"}


async def _admin(client):
    return await _login(client, "admin", "admin123")


async def _make_operator() -> str:
    async with session_scope() as session:
        op = Operator(username=f"be7-op-{uuid4().hex[:10]}",
                      hashed_password=hash_password(PASSWORD),
                      role="operator", is_active=True)
        session.add(op)
        await session.flush()
        return op.username


async def _seed_env(n_bars: int = 60) -> None:
    async with session_scope() as session:
        if not (await session.execute(select(V2MdSource))).scalars().first():
            for row in V2_MD_SOURCE_SEED:
                session.add(V2MdSource(id=str(uuid4()), created_at=utc_now(), **row))
            for row in V2_MD_INSTRUMENT_SEED:
                session.add(V2MdInstrument(id=str(uuid4()), created_at=utc_now(), **row))
        start = datetime(2026, 9, 1, tzinfo=UTC)
        for i in range(n_bars):
            px = Decimal("100") + Decimal(i % 7) - Decimal(3)
            session.add(Candle(
                id=str(uuid4()), market_class="forex", symbol="EURUSD",
                timeframe="M15", open_time=start + timedelta(minutes=15 * i),
                open=px, high=px + 1, low=px - 1, close=px,
                volume=Decimal("100"), source="live:simulated"))


COSTS = {"spread": {"value": "0.1", "unit": "price", "citation": "band-declared"},
         "commission": {"value": "0.05", "unit": "price", "citation": "band-declared"},
         "slippage": {"value": "0", "unit": "price", "citation": "band-declared"}}


async def _pipeline(client, headers) -> dict:
    """Register input + cost model + strategy; return the id triple."""
    inp = (await client.post(f"{RJ}/registry/inputs", headers=headers, json={
        "input_id": "in-1", "instrument_id": "forex.eurusd",
        "window_start": W_START, "window_end": W_END})).json()
    assert inp["outcome"] == "registered", inp
    cm = (await client.post(f"{RJ}/registry/cost-models", headers=headers,
                            json={"cost_model_id": "cm-1", "latency_ms": 100,
                                  **COSTS})).json()
    assert cm["outcome"] == "registered", cm
    st = (await client.post(f"{RJ}/registry/strategies", headers=headers, json={
        "strategy_id": "st-1", "name": "T",
        "parameters": {"rule": "threshold", "buy_below": "98",
                       "sell_above": "102", "unit_qty": "1",
                       "initial_cash": "10000"}})).json()
    assert st["outcome"] == "registered", st
    return {"input_registry_id": inp["record_id"],
            "cost_model_id": cm["record_id"],
            "strategy_version_id": st["record_id"]}


async def _submitted(client, headers, ids, result_class="backtest") -> str:
    r = (await client.post(f"{RJ}/jobs/submit", headers=headers, json={
        "authorization_ref": "BO-V2-BE-7-001",
        "inputs": {**ids, "result_class": result_class}})).json()
    assert r["outcome"] == "registered", r
    return r["job_id"]


# --- U-3: registration (7 tests) ------------------------------------------------


@pytest.mark.asyncio
async def test_input_registration_and_content_dedupe(prepared_db, async_client):
    await _seed_env()
    headers = await _admin(async_client)
    first = (await async_client.post(f"{RJ}/registry/inputs", headers=headers,
             json={"input_id": "in-d", "instrument_id": "forex.eurusd",
                   "window_start": W_START, "window_end": W_END})).json()
    assert first["outcome"] == "registered"
    again = (await async_client.post(f"{RJ}/registry/inputs", headers=headers,
             json={"input_id": "in-OTHER", "instrument_id": "forex.eurusd",
                   "window_start": W_START, "window_end": W_END})).json()
    assert again["outcome"] == "reused"                 # content-addressed
    assert again["record_id"] == first["record_id"]


@pytest.mark.asyncio
async def test_input_refused_bad_window_durably_audited(prepared_db, async_client):
    await _seed_env()
    headers = await _admin(async_client)
    r = (await async_client.post(f"{RJ}/registry/inputs", headers=headers,
         json={"input_id": "in-bad", "instrument_id": "forex.eurusd",
               "window_start": W_END, "window_end": W_START})).json()
    assert r["outcome"] == "refused"
    async with session_scope() as session:
        audits = [a for (a,) in (await session.execute(
            select(V2AuditEvent.action).where(
                V2AuditEvent.action == "input.refused"))).all()]
        assert audits  # durable despite refusal (C-1 law)


@pytest.mark.asyncio
async def test_cost_model_requires_citations(prepared_db, async_client):
    await _seed_env()
    headers = await _admin(async_client)
    bad = dict(COSTS)
    bad["spread"] = {"value": "0.1", "unit": "price"}  # no citation
    r = (await async_client.post(f"{RJ}/registry/cost-models", headers=headers,
         json={"cost_model_id": "cm-x", "latency_ms": 0, **bad})).json()
    assert r["outcome"] == "refused"
    assert any("citation" in str(x) for x in r["reasons"])


@pytest.mark.asyncio
async def test_cost_model_unknown_unit_refused_f1(prepared_db, async_client):
    """CR-V2-BE-7-001 F-1: unit outside COST_UNITS_V1 is refused TYPED at
    registration with a durable audit and NO row written — an unknown unit
    can never reach apply_costs as an untyped engine failure."""
    await _seed_env()
    headers = await _admin(async_client)
    bad = dict(COSTS)
    bad["spread"] = {"value": "0.1", "unit": "bogus",
                     "citation": "band-declared"}
    r = (await async_client.post(f"{RJ}/registry/cost-models", headers=headers,
         json={"cost_model_id": "cm-f1", "latency_ms": 0, **bad})).json()
    assert r["outcome"] == "refused"
    assert any("spread.unit" in str(x) for x in r["reasons"])
    assert any("'price'" in str(x) and "'fraction'" in str(x)
               for x in r["reasons"])
    async with session_scope() as session:
        rows = (await session.execute(
            select(V2CostModel).where(
                V2CostModel.cost_model_id == "cm-f1"))).scalars().all()
        assert rows == []  # refusal writes NO row
        audits = [a for (a,) in (await session.execute(
            select(V2AuditEvent.action).where(
                V2AuditEvent.action == "cost_model.refused"))).all()]
        assert audits  # durable despite refusal (C-1 law)


@pytest.mark.asyncio
async def test_strategy_unregistered_rule_refused(prepared_db, async_client):
    await _seed_env()
    headers = await _admin(async_client)
    r = (await async_client.post(f"{RJ}/registry/strategies", headers=headers,
         json={"strategy_id": "st-x", "name": "X",
               "parameters": {"rule": "arbitrary_python"}})).json()
    assert r["outcome"] == "refused"
    assert any("rule" in str(x) for x in r["reasons"])


@pytest.mark.asyncio
async def test_strategy_forbidden_parameter_keys_refused(prepared_db, async_client):
    await _seed_env()
    headers = await _admin(async_client)
    r = (await async_client.post(f"{RJ}/registry/strategies", headers=headers,
         json={"strategy_id": "st-y", "name": "Y",
               "parameters": {"rule": "threshold", "broker": "x"}})).json()
    assert r["outcome"] == "refused"


@pytest.mark.asyncio
async def test_strategy_versioning_supersede(prepared_db, async_client):
    await _seed_env()
    headers = await _admin(async_client)
    p = {"rule": "threshold", "buy_below": "98", "sell_above": "102"}
    first = (await async_client.post(f"{RJ}/registry/strategies",
             headers=headers, json={"strategy_id": "st-v", "name": "V1",
                                    "parameters": p})).json()
    second = (await async_client.post(f"{RJ}/registry/strategies",
              headers=headers, json={"strategy_id": "st-v", "name": "V2",
                                     "parameters": p})).json()
    assert first["outcome"] == second["outcome"] == "registered"
    assert first["record_id"] != second["record_id"]


@pytest.mark.asyncio
async def test_historical_real_data_class_refused(prepared_db, async_client):
    await _seed_env()
    headers = await _admin(async_client)
    r = (await async_client.post(f"{RJ}/registry/inputs", headers=headers,
         json={"input_id": "in-hr", "instrument_id": "forex.eurusd",
               "window_start": W_START, "window_end": W_END,
               "data_class": "historical_real"})).json()
    assert r["outcome"] == "refused"


# --- U-4: queue + runner (12 tests) -------------------------------------------------


@pytest.mark.asyncio
async def test_submit_run_succeed_full_lineage(prepared_db, async_client):
    await _seed_env()
    headers = await _admin(async_client)
    ids = await _pipeline(async_client, headers)
    job_id = await _submitted(async_client, headers, ids)
    run = (await async_client.post(f"{RJ}/jobs/run", headers=headers,
                                   json={"job_id": job_id})).json()
    assert run["job_state"] == "succeeded", run
    assert run["result_id"] and run["reused"] is False
    async with session_scope() as session:
        result = (await session.execute(select(V2ResearchResult))).scalar_one()
        assert result.result_class == "backtest"
        assert "NOT live or future performance" in result.summary[
            "performance_disclaimer"]
        lineage = (await session.execute(
            select(V2LineageRecord).where(
                V2LineageRecord.artifact_type == "research_result"
            ))).scalars().all()
        assert lineage and lineage[0].input_snapshot_id == result.inputs_hash
        attempts = (await session.execute(
            select(V2ResearchJobAttempt))).scalars().all()
        assert [a.outcome for a in attempts] == ["succeeded"]


@pytest.mark.asyncio
async def test_retry_idempotent_no_double_apply(prepared_db, async_client):
    """P-10/T-10: re-running a succeeded pipeline returns the SAME artifact."""
    await _seed_env()
    headers = await _admin(async_client)
    ids = await _pipeline(async_client, headers)
    j1 = await _submitted(async_client, headers, ids)
    r1 = (await async_client.post(f"{RJ}/jobs/run", headers=headers,
                                  json={"job_id": j1})).json()
    # a second job over the identical triple (duplicate-submit race)
    j2 = await _submitted(async_client, headers, ids)
    r2 = (await async_client.post(f"{RJ}/jobs/run", headers=headers,
                                  json={"job_id": j2})).json()
    assert r2["reused"] is True                       # anchor collision
    assert r2["result_id"] == r1["result_id"]         # no double-apply
    async with session_scope() as session:
        count = len((await session.execute(
            select(V2ResearchResult))).scalars().all())
        assert count == 1
        reuse_audits = [a for (a,) in (await session.execute(
            select(V2AuditEvent.action).where(
                V2AuditEvent.action == "result.reused"))).all()]
        assert reuse_audits


@pytest.mark.asyncio
async def test_rerun_succeeded_job_returns_existing(prepared_db, async_client):
    await _seed_env()
    headers = await _admin(async_client)
    ids = await _pipeline(async_client, headers)
    job_id = await _submitted(async_client, headers, ids)
    first = (await async_client.post(f"{RJ}/jobs/run", headers=headers,
                                     json={"job_id": job_id})).json()
    again = (await async_client.post(f"{RJ}/jobs/run", headers=headers,
                                     json={"job_id": job_id})).json()
    assert again["job_state"] == "succeeded"
    assert again["result_id"] == first["result_id"]
    async with session_scope() as session:
        job = (await session.execute(select(V2ResearchJob))).scalar_one()
        assert job.attempt_count == 1  # the no-op rerun did not burn an attempt


@pytest.mark.asyncio
async def test_cancel_queued_then_terminal_refusal(prepared_db, async_client):
    await _seed_env()
    headers = await _admin(async_client)
    ids = await _pipeline(async_client, headers)
    job_id = await _submitted(async_client, headers, ids)
    c1 = (await async_client.post(f"{RJ}/jobs/cancel", headers=headers,
          json={"job_id": job_id, "reason": "operator abort"})).json()
    assert c1["outcome"] == "registered"
    c2 = (await async_client.post(f"{RJ}/jobs/cancel", headers=headers,
          json={"job_id": job_id, "reason": "again"})).json()
    assert c2["outcome"] == "refused"                 # terminal-refusal
    assert any("terminal" in str(x) for x in c2["reasons"])
    async with session_scope() as session:
        attempts = (await session.execute(
            select(V2ResearchJobAttempt))).scalars().all()
        assert [a.outcome for a in attempts] == ["cancelled"]
        audits = [a for (a,) in (await session.execute(
            select(V2AuditEvent.action).where(V2AuditEvent.action.in_(
                ["job.cancelled", "job.cancel.refused"])))).all()]
        assert set(audits) == {"job.cancelled", "job.cancel.refused"}


@pytest.mark.asyncio
async def test_submit_nonmanual_schedule_refused_c4(prepared_db, async_client):
    await _seed_env()
    headers = await _admin(async_client)
    ids = await _pipeline(async_client, headers)
    r = (await async_client.post(f"{RJ}/jobs/submit", headers=headers, json={
        "authorization_ref": "BO-V2-BE-7-001",
        "inputs": {**ids, "result_class": "backtest"},
        "schedule": {"kind": "cron", "expr": "* * * * *"}})).json()
    assert r["outcome"] == "refused"
    assert any(x.get("failing") == "schedule.kind" for x in r["reasons"])
    async with session_scope() as session:
        audits = [a for (a,) in (await session.execute(
            select(V2AuditEvent.action).where(
                V2AuditEvent.action == "job.submit.refused"))).all()]
        assert audits  # durably audited (C4)


@pytest.mark.asyncio
async def test_submit_paper_live_result_class_refused_p9(prepared_db, async_client):
    await _seed_env()
    headers = await _admin(async_client)
    ids = await _pipeline(async_client, headers)
    for banned in ("paper", "live"):
        r = (await async_client.post(f"{RJ}/jobs/submit", headers=headers,
             json={"authorization_ref": "BO-V2-BE-7-001",
                   "inputs": {**ids, "result_class": banned}})).json()
        # submission passes shape checks; the CONSTRUCTION point refuses:
        if r["outcome"] == "registered":
            run = (await async_client.post(f"{RJ}/jobs/run", headers=headers,
                   json={"job_id": r["job_id"]})).json()
            assert run["job_state"] == "failed"
            assert any("result_class" in str(x) for x in run["reasons"])


@pytest.mark.asyncio
async def test_submit_missing_authorization_refused(prepared_db, async_client):
    await _seed_env()
    headers = await _admin(async_client)
    ids = await _pipeline(async_client, headers)
    r = await async_client.post(f"{RJ}/jobs/submit", headers=headers, json={
        "authorization_ref": "", "inputs": {**ids, "result_class": "backtest"}})
    assert r.status_code == 422 or r.json()["outcome"] == "refused"


@pytest.mark.asyncio
async def test_submit_draft_strategy_refused(prepared_db, async_client):
    await _seed_env()
    headers = await _admin(async_client)
    ids = await _pipeline(async_client, headers)
    draft = (await async_client.post(f"{RJ}/registry/strategies",
             headers=headers, json={
                 "strategy_id": "st-d", "name": "D",
                 "parameters": {"rule": "threshold"},
                 "lifecycle_state": "draft"})).json()
    r = (await async_client.post(f"{RJ}/jobs/submit", headers=headers, json={
        "authorization_ref": "BO-V2-BE-7-001",
        "inputs": {**ids, "strategy_version_id": draft["record_id"],
                   "result_class": "backtest"}})).json()
    assert r["outcome"] == "refused"
    assert any("lifecycle_state" in str(x) for x in r["reasons"])


@pytest.mark.asyncio
async def test_submit_superseded_strategy_refused(prepared_db, async_client):
    await _seed_env()
    headers = await _admin(async_client)
    ids = await _pipeline(async_client, headers)
    p = {"rule": "threshold", "buy_below": "98", "sell_above": "102"}
    await async_client.post(f"{RJ}/registry/strategies", headers=headers,
                            json={"strategy_id": "st-1", "name": "gen2",
                                  "parameters": p})  # supersedes st-1 gen1
    r = (await async_client.post(f"{RJ}/jobs/submit", headers=headers, json={
        "authorization_ref": "BO-V2-BE-7-001",
        "inputs": {**ids, "result_class": "backtest"}})).json()
    assert r["outcome"] == "refused"
    assert any("superseded" in str(x) for x in r["reasons"])


@pytest.mark.asyncio
async def test_c1_submission_fields_write_once(prepared_db, async_client):
    """C1: no writer path updates owner/authorization_ref/inputs/schedule."""
    await _seed_env()
    headers = await _admin(async_client)
    ids = await _pipeline(async_client, headers)
    job_id = await _submitted(async_client, headers, ids)
    async with session_scope() as session:
        before = (await session.execute(
            select(V2ResearchJob).where(V2ResearchJob.id == job_id)
        )).scalar_one()
        snapshot = (before.owner, before.authorization_ref,
                    dict(before.inputs), dict(before.schedule))
    await async_client.post(f"{RJ}/jobs/run", headers=headers,
                            json={"job_id": job_id})
    async with session_scope() as session:
        after = (await session.execute(
            select(V2ResearchJob).where(V2ResearchJob.id == job_id)
        )).scalar_one()
        assert (after.owner, after.authorization_ref, dict(after.inputs),
                dict(after.schedule)) == snapshot  # write-once held
        assert after.job_state == "succeeded"      # mutable set moved


@pytest.mark.asyncio
async def test_c2_mutable_set_constant_exact(prepared_db, async_client):
    from app.v2.research_jobs.contracts import JOB_MUTABLE_COLUMNS
    from app.v2.research_jobs.runner import JOB_UPDATE_COLUMNS

    assert JOB_MUTABLE_COLUMNS == frozenset(
        {"job_state", "attempt_count", "output_ref", "failure"})
    assert JOB_UPDATE_COLUMNS == JOB_MUTABLE_COLUMNS


@pytest.mark.asyncio
async def test_leakage_refusal_fails_job_typed(prepared_db, async_client):
    """A tampered registry hash (G-5) fails the job with typed reasons."""
    await _seed_env()
    headers = await _admin(async_client)
    ids = await _pipeline(async_client, headers)
    # corrupt the stored content hash (guard dropped for test setup)
    async with session_scope() as session:
        from sqlalchemy import text
        await session.execute(text(
            "DROP TRIGGER IF EXISTS v2_backtest_input_immutable_update"))
        await session.execute(text(
            "UPDATE v2_backtest_input SET content_hash = :h"),
            {"h": "0" * 64})
    job_id = await _submitted(async_client, headers, ids)
    run = (await async_client.post(f"{RJ}/jobs/run", headers=headers,
                                   json={"job_id": job_id})).json()
    assert run["job_state"] == "failed"
    assert any("G-5" in str(x) for x in run["reasons"])


# --- U-5: API surface + scans (6 tests) ------------------------------------------------


@pytest.mark.asyncio
async def test_rbac_denied_and_reads(prepared_db, async_client):
    await _seed_env()
    admin = await _admin(async_client)
    operator = await _login(async_client, await _make_operator())
    for headers in (admin, operator):
        assert (await async_client.get(f"{RJ}/jobs",
                                       headers=headers)).status_code == 200
        assert (await async_client.get(f"{RJ}/results",
                                       headers=headers)).status_code == 200
    for path, body in (
        (f"{RJ}/registry/inputs",
         {"input_id": "x", "instrument_id": "forex.eurusd",
          "window_start": W_START, "window_end": W_END}),
        (f"{RJ}/jobs/submit",
         {"authorization_ref": "x", "inputs": {}}),
        (f"{RJ}/jobs/cancel", {"job_id": "x", "reason": "r"}),
    ):
        r = await async_client.post(path, json=body, headers=operator)
        assert r.status_code == 403
        assert r.json()["detail"] == "Permission denied"
    assert (await async_client.get(f"{RJ}/jobs")).status_code == 401


@pytest.mark.asyncio
async def test_c3_no_generic_job_update_endpoint(prepared_db, async_client):
    """C3: the API exposes no PATCH/PUT and no generic job-update path."""
    from fastapi.routing import APIRoute

    from app.v2.research_jobs.api import router

    for route in router.routes:
        if isinstance(route, APIRoute):
            assert not ({"PUT", "PATCH", "DELETE"} & route.methods), route.path
            if "POST" in route.methods:
                assert route.path in (
                    "/research-jobs/registry/inputs",
                    "/research-jobs/registry/cost-models",
                    "/research-jobs/registry/strategies",
                    "/research-jobs/jobs/submit",
                    "/research-jobs/jobs/run",
                    "/research-jobs/jobs/cancel"), route.path


def test_allow_list_constants_part_10_1():
    from app.v2.research_jobs.contracts import (
        RUNNER_INSERT_TABLES,
        RUNNER_UPDATE_TABLES,
    )
    from app.v2.research_jobs.runner import WRITABLE_TABLES

    assert WRITABLE_TABLES["insert"] == RUNNER_INSERT_TABLES == frozenset(
        {"v2_research_result", "v2_research_job_attempt",
         "v2_audit_event", "v2_lineage_record"})
    assert WRITABLE_TABLES["update"] == RUNNER_UPDATE_TABLES == frozenset(
        {"v2_research_job"})


def test_import_scan_no_execution_adapter_reachable():
    """T-11 + scan-token condition: the band's module graph must not reach
    execution/broker/order/adapter/trading_intelligence modules."""
    import ast
    from pathlib import Path

    base = Path(__file__).resolve().parents[1] / "app/v2/research_jobs"
    banned_tokens = ("execution", "broker", "order", "adapter",
                     "trading_intelligence", "market.live",
                     "app.market", "paper", "live_service")
    allowed_exceptions = ("execution_research",)  # V1 read-only lineage name
    for f in base.glob("*.py"):
        tree = ast.parse(f.read_text())
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module]
            for name in names:
                low = name.lower()
                if any(low.startswith(a) or a in low
                       for a in allowed_exceptions):
                    continue
                for token in banned_tokens:
                    assert token not in low, f"{f.name} imports {name}"


def test_construction_token_scan():
    """No paper/live/order construction vocabulary in band modules."""
    from pathlib import Path

    base = Path(__file__).resolve().parents[1] / "app/v2/research_jobs"
    for f in base.glob("*.py"):
        text = f.read_text().lower()
        for token in ("place_order", "submit_order", "broker_",
                      "account_id", "paper_trade", "live_trade"):
            assert token not in text, f"{token} in {f.name}"


@pytest.mark.asyncio
async def test_attempts_read_and_result_listing(prepared_db, async_client):
    await _seed_env()
    headers = await _admin(async_client)
    ids = await _pipeline(async_client, headers)
    job_id = await _submitted(async_client, headers, ids)
    await async_client.post(f"{RJ}/jobs/run", headers=headers,
                            json={"job_id": job_id})
    attempts = (await async_client.get(f"{RJ}/jobs/{job_id}/attempts",
                                       headers=headers)).json()
    assert attempts["total"] == 1
    assert attempts["attempts"][0]["outcome"] == "succeeded"
    results = (await async_client.get(
        f"{RJ}/results", params={"result_class": "backtest"},
        headers=headers)).json()
    assert results["total"] == 1
    assert results["results"][0]["result_class"] == "backtest"
    assert "performance_disclaimer" in results["results"][0]["summary"]
