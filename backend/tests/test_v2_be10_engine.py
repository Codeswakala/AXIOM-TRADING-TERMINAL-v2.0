"""V2 BE-10 engine tests — BO-V2-BE-10-001 L4/L6/L7/L8 (verdict matrix
table-driven, determinism x3, basis law, staleness, unmapped census)."""

from __future__ import annotations

import socket
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from uuid import uuid4

import pytest

from app.db.models.v2_broker_read import V2BrokerPosition, V2BrokerSyncRun
from app.db.models.v2_marketdata import V2MdSource, V2MdSymbolMap
from app.db.models.v2_signal import V2SignalRecord
from app.db.session import session_scope
from app.v2.account_context.contract import AccountContextRefused
from app.v2.account_context.engine import (
    _posture,
    _verdict,
    compute_alignment,
)
from app.v2.temporal.validation import utc_now

UTC = timezone.utc


@pytest.fixture(autouse=True)
def _socket_guard(monkeypatch):
    def _deny(*_a, **_k):
        raise AssertionError("network attempt during BE-10 test")

    monkeypatch.setattr(socket, "getaddrinfo", _deny)
    monkeypatch.setattr(socket, "create_connection", _deny)


REGIME = {"data_class": "simulated", "mode": "RESEARCH",
          "operator_id": "t", "correlation_id": None}


async def _seed_mapping(session, pairs=(("EURUSDm", "forex.eurusd"),
                                        ("GBPUSDm", "forex.gbpusd"))):
    session.add(V2MdSource(id=str(uuid4()), source_id="exness_mt5_demo",
                           kind="import", authority="unknown",
                           mode_scope="RESEARCH", active=True,
                           created_at=utc_now()))
    for sym, iid in pairs:
        session.add(V2MdSymbolMap(id=str(uuid4()),
                                  source_id="exness_mt5_demo",
                                  source_symbol=sym, instrument_id=iid,
                                  created_at=utc_now()))


async def _seed_sync(session, positions=(), age_hours=0.0) -> str:
    run = V2BrokerSyncRun(
        provider_id="exness_mt5_demo", scope={}, outcome="complete",
        page_counts={}, origin_basis="o", inputs_hash="h",
        result_digest="d", refusal=None, actor_id="t", **REGIME)
    run.created_at = datetime.now(UTC) - timedelta(hours=age_hours)
    session.add(run)
    await session.flush()
    for ext_id, long_u, short_u in positions:
        session.add(V2BrokerPosition(
            provider_id="exness_mt5_demo", broker_account_ext_id="476910140",
            instrument_ext_id=ext_id, units_long=long_u,
            units_short=short_u, avg_price_long="1", avg_price_short="0",
            sync_run_id=run.id, server_hostname="ExnessKE-MT5Trial9",
            fetched_at_basis="b", **REGIME))
    return run.id


async def _seed_signal(session, instrument_id, direction="up",
                       state="emitted", expired=False):
    session.add(V2SignalRecord(
        family="structural", signal_type="trend", instrument_id=instrument_id,
        timeframe="H1", state=state, state_reason=None,
        payload={"direction": direction} if direction else {},
        uncertainty={}, limitations={}, source_family_refs={},
        governance_record_id=None,
        as_of=datetime.now(UTC),
        expires_at=(datetime.now(UTC) - timedelta(hours=1)) if expired
        else (datetime.now(UTC) + timedelta(hours=6)),
        **REGIME))


# --- pure verdict units (table-driven) ----------------------------------------


@pytest.mark.parametrize("posture,state,direction,mapped,expected", [
    ("long", "live", "up", True, "aligned"),
    ("short", "live", "down", True, "aligned"),
    ("long", "live", "down", True, "opposed"),
    ("short", "live", "up", True, "opposed"),
    ("long", "none", None, True, "unsignalled_holding"),
    ("flat", "live", "up", True, "signal_without_holding"),
    ("flat", "none", None, True, "flat_no_signal"),
    ("long", "indeterminate", None, True, "indeterminate"),
    ("mixed", "live", "up", True, "indeterminate"),
    ("long", "live", "up", False, "unmapped"),
    ("flat", "expired", None, True, "flat_no_signal"),
])
def test_verdict_matrix_table_driven(posture, state, direction, mapped,
                                     expected):
    assert _verdict(posture, state, direction, mapped) == expected


def test_posture_law():
    assert _posture(Decimal("1"), Decimal("0")) == "long"
    assert _posture(Decimal("0"), Decimal("2")) == "short"
    assert _posture(Decimal("1"), Decimal("1")) == "mixed"
    assert _posture(Decimal("0"), Decimal("0")) == "flat"


# --- integration (fixtures on the standing tables) -------------------------------


@pytest.mark.asyncio
async def test_l4_no_basis_typed_refusal(prepared_db):
    async with session_scope() as session:
        await _seed_mapping(session)
    async with session_scope() as session:
        with pytest.raises(AccountContextRefused) as exc:
            await compute_alignment(session)
        assert exc.value.refusal_class == "account_context.no_basis"


@pytest.mark.asyncio
async def test_mapping_artifact_absent_typed(prepared_db):
    async with session_scope() as session:
        await _seed_sync(session)
    async with session_scope() as session:
        with pytest.raises(AccountContextRefused) as exc:
            await compute_alignment(session)
        assert exc.value.refusal_class == \
            "account_context.mapping_artifact_absent"


@pytest.mark.asyncio
async def test_full_matrix_and_l6_unmapped_visible(prepared_db):
    async with session_scope() as session:
        await _seed_mapping(session)  # EURUSDm + GBPUSDm mapped
        await _seed_sync(session, positions=(
            ("EURUSDm", "1", "0"),     # long + up-signal => aligned
            ("GBPUSDm", "0", "2"),     # short + no signal => unsignalled
            ("XAUUSDm", "1", "0"),     # UNMAPPED (not seeded here) => visible
        ))
        await _seed_signal(session, "forex.eurusd", "up")
    async with session_scope() as session:
        m = await compute_alignment(session)
    verdicts = {r.instrument_ext_id: r.verdict for r in m.rows}
    assert verdicts["EURUSDm"] == "aligned"
    assert verdicts["GBPUSDm"] == "unsignalled_holding"
    assert verdicts["XAUUSDm"] == "unmapped"      # L6: never filtered
    assert m.unmapped_count == 1
    assert m.staleness == "fresh" and m.banner is None


@pytest.mark.asyncio
async def test_signal_without_holding_row(prepared_db):
    async with session_scope() as session:
        await _seed_mapping(session)
        await _seed_sync(session, positions=())  # flat book
        await _seed_signal(session, "forex.gbpusd", "down")
    async with session_scope() as session:
        m = await compute_alignment(session)
    verdicts = {r.instrument_ext_id: r.verdict for r in m.rows}
    assert verdicts["GBPUSDm"] == "signal_without_holding"


@pytest.mark.asyncio
async def test_expired_signal_is_not_live(prepared_db):
    async with session_scope() as session:
        await _seed_mapping(session)
        await _seed_sync(session, positions=(("EURUSDm", "1", "0"),))
        await _seed_signal(session, "forex.eurusd", "up", expired=True)
    async with session_scope() as session:
        m = await compute_alignment(session)
    row = {r.instrument_ext_id: r for r in m.rows}["EURUSDm"]
    assert row.signal_state == "expired"
    assert row.verdict == "unsignalled_holding"


@pytest.mark.asyncio
async def test_l7_digest_deterministic_x3(prepared_db):
    async with session_scope() as session:
        await _seed_mapping(session)
        await _seed_sync(session, positions=(("EURUSDm", "1", "0"),))
        await _seed_signal(session, "forex.eurusd", "up")
    digests = []
    for _ in range(3):
        async with session_scope() as session:
            m = await compute_alignment(session)
            digests.append(m.digest)
    assert digests[0] == digests[1] == digests[2]
    assert len(digests[0]) == 64


@pytest.mark.asyncio
async def test_l8_stale_basis_banner(prepared_db):
    async with session_scope() as session:
        await _seed_mapping(session)
        await _seed_sync(session, positions=(("EURUSDm", "1", "0"),),
                         age_hours=30.0)
    async with session_scope() as session:
        m = await compute_alignment(session)
    assert m.staleness == "stale"
    assert m.banner and "last-good" in m.banner
    assert m.rows  # still answers — never silently fresh, never mute


@pytest.mark.asyncio
async def test_basis_is_newest_complete_only(prepared_db):
    """A newer FAILED run never becomes the basis."""
    async with session_scope() as session:
        await _seed_mapping(session)
        good = await _seed_sync(session, positions=(("EURUSDm", "1", "0"),),
                                age_hours=2.0)
        bad = V2BrokerSyncRun(
            provider_id="exness_mt5_demo", scope={}, outcome="failed",
            page_counts={}, origin_basis="o", inputs_hash="h",
            result_digest="", refusal={"class": "broker.unavailable"},
            actor_id="t", **REGIME)
        session.add(bad)
    async with session_scope() as session:
        m = await compute_alignment(session)
    assert m.basis_sync_run_id == good
