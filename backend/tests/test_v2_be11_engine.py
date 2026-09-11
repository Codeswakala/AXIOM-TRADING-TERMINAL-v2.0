"""V2 BE-11 engine coupons — L-1/L-2/L-3/L-5 (BO D-3).

Determinism x3 on pinned basis fixture + citation-priced intent
(per-world law N-O13); full fail-closed battery; drift 4-verdict arms
with crafted ledgers; refuse-to-compare until tolerances seeded.
Socket guard on every test.
"""

from __future__ import annotations

import socket
from datetime import datetime, timedelta, timezone

import pytest

from app.db.models.v2_broker_read import V2BrokerBalance, V2BrokerSyncRun
from app.db.models.v2_paper_bridge import V2PaperBridgeDriftRun
from app.db.session import session_scope
from app.v2.paper_bridge.contract import (
    DRIFT_VERDICTS,
    GATEWAY_DECISIONS,
    REFUSAL_REASONS,
    BridgeBasis,
    BridgeRefused,
)
from app.v2.paper_bridge.engine import (
    PBR_ENGINE_TUPLE,
    compute_drift,
    evaluate_intent,
    pin_basis,
    read_staleness_seed,
    read_tolerance_seeds,
    require_citation,
)

UTC = timezone.utc
REGIME = {"data_class": "simulated", "mode": "RESEARCH",
          "operator_id": "t", "correlation_id": None}


@pytest.fixture(autouse=True)
def _socket_guard(monkeypatch):
    def _deny(*_a, **_k):
        raise AssertionError("network attempt during BE-11 test")

    monkeypatch.setattr(socket, "getaddrinfo", _deny)
    monkeypatch.setattr(socket, "create_connection", _deny)


def _basis(age_hours=1.0, positions=False) -> BridgeBasis:
    return BridgeBasis(
        sync_run_id="run-fixture-1", balance="10000.0",
        margin_used="0.0", margin_available="10000.0",
        unrealized_pl="0.0", currency="USD",
        basis_age_hours=age_hours,
        staleness="stale" if age_hours > 24 else "fresh",
        positions_present=positions)


CITATION = {"value": "1.1000", "currency_unit": "USD",
            "cited_source": "operator: exness terminal quote panel",
            "cited_at": "2026-09-06T12:00:00+00:00"}
INTENT = {"account_id": "acct-1", "instrument_id": "forex.eurusd",
          "side": "buy", "quantity": "100", "idempotency_key": "k1"}


# --- L-1: engine tuple pinning ----------------------------------------------------


def test_l1_engine_tuple_pinned():
    assert PBR_ENGINE_TUPLE == ("pxs-1.0.0", "prg-1.0.0", "pbr-1.0.0")


# --- L-2: x3 determinism (per-world) -----------------------------------------------


def test_l2_gateway_decision_x3_identical():
    citation = require_citation(CITATION)
    records = [evaluate_intent(_basis(), INTENT, citation, 24.0)
               for _ in range(3)]
    assert records[0].decision == records[1].decision == records[2].decision
    assert records[0].digest == records[1].digest == records[2].digest
    assert len(records[0].digest) == 64
    assert records[0].decision == "accept_with_notes"
    assert any("deferred" in n for n in records[0].notes)  # money-units law


def test_l2_digest_moves_on_substantive_change():
    citation = require_citation(CITATION)
    a = evaluate_intent(_basis(), INTENT, citation, 24.0)
    b = evaluate_intent(_basis(), {**INTENT, "quantity": "200"},
                        citation, 24.0)
    assert a.digest != b.digest


# --- L-3: fail-closed battery -------------------------------------------------------


@pytest.mark.asyncio
async def test_l3_basis_unavailable(prepared_db):
    async with session_scope() as session:
        with pytest.raises(BridgeRefused) as exc:
            await pin_basis(session)
        assert exc.value.reason == "basis_unavailable"


def test_l3_threshold_unseeded_refuses_generation():
    citation = require_citation(CITATION)
    with pytest.raises(BridgeRefused) as exc:
        evaluate_intent(_basis(), INTENT, citation, None)
    assert exc.value.reason == "basis_staleness_threshold_unseeded"


def test_l3_stale_basis_refuses_generation():
    citation = require_citation(CITATION)
    with pytest.raises(BridgeRefused) as exc:
        evaluate_intent(_basis(age_hours=30.0), INTENT, citation, 24.0)
    assert exc.value.reason == "basis_stale"


def test_l3_uncited_price_refuses():
    for bad in (None, {}, {"value": "1.1"},
                {"value": "1.1", "currency_unit": "USD",
                 "cited_source": "", "cited_at": "x"}):
        with pytest.raises(BridgeRefused) as exc:
            require_citation(bad)
        assert exc.value.reason == "reference_price_uncited"


def test_l3_policy_refusals_are_state_records():
    """Over-margin + currency mismatch => refused_under_policy record
    (a STATE, not an exception — the gateway records, never executes)."""
    citation = require_citation({**CITATION, "currency_unit": "EUR"})
    record = evaluate_intent(
        _basis(), {**INTENT, "quantity": "1000000"}, citation, 24.0)
    assert record.decision == "refused_under_policy"
    assert "citation_currency_differs_from_basis" in record.reasons
    assert "notional_exceeds_available_margin" in record.reasons


# --- L-5: drift arms x4 + refuse-to-compare -----------------------------------------


TOLS = [{"name": "balance", "value": "1.00", "unit": "USD",
         "citation": "operator-seeded fixture"}]


def test_l5_refuse_to_compare_unseeded():
    verdict, findings = compute_drift({"balance": "100"},
                                      {"balance": "100"}, [])
    assert verdict == "uncomputable"
    assert "refuse-to-compare" in findings[0]["note"]


def test_l5_within_tolerance():
    verdict, _ = compute_drift({"balance": "100.50"},
                               {"balance": "100.00"}, TOLS)
    assert verdict == "within_tolerance"


def test_l5_drift_minor():
    verdict, _ = compute_drift({"balance": "101.50"},
                               {"balance": "100.00"}, TOLS)
    assert verdict == "drift_minor"  # delta 1.50 in (tol, 2*tol]


def test_l5_drift_major():
    verdict, findings = compute_drift({"balance": "105.00"},
                                      {"balance": "100.00"}, TOLS)
    assert verdict == "drift_major"
    assert findings[0]["delta"] == "5.00"  # 2dp law


def test_l5_unseeded_field_uncomputable():
    verdict, _ = compute_drift({"balance": "100", "equity": "100"},
                               {"balance": "100", "equity": "100"}, TOLS)
    assert verdict == "uncomputable"  # equity has no seeded tolerance


def test_l5_malformed_seed_uncomputable():
    verdict, _ = compute_drift({"balance": "100"}, {"balance": "100"},
                               [{"name": "balance", "value": "1"}])
    assert verdict == "uncomputable"  # citation chassis incomplete


# --- seed-read law (empty-forced integration) ----------------------------------------


@pytest.mark.asyncio
async def test_seed_slots_ship_empty_forced(prepared_db):
    async with session_scope() as session:
        assert await read_tolerance_seeds(session) == []
        assert await read_staleness_seed(session) is None


@pytest.mark.asyncio
async def test_seeded_overlay_arms_the_slots(prepared_db):
    """A future operator overlay = seed-kind rows; the reads arm."""
    async with session_scope() as session:
        session.add(V2PaperBridgeDriftRun(
            run_kind="seed", seed_name="drift_tolerance",
            payload={"name": "balance", "value": "1.00", "unit": "USD",
                     "citation": "operator overlay fixture"},
            actor_id="t", **REGIME))
        session.add(V2PaperBridgeDriftRun(
            run_kind="seed", seed_name="generation_staleness",
            payload={"max_age_hours": 24, "citation": "operator overlay"},
            actor_id="t", **REGIME))
    async with session_scope() as session:
        assert len(await read_tolerance_seeds(session)) == 1
        assert await read_staleness_seed(session) == 24.0


# --- consistency ARM + basis integration ----------------------------------------------


@pytest.mark.asyncio
async def test_basis_pinned_from_newest_complete_run(prepared_db):
    async with session_scope() as session:
        run = V2BrokerSyncRun(
            provider_id="exness_mt5_demo", scope={}, outcome="complete",
            page_counts={}, origin_basis="o", inputs_hash="h",
            result_digest="d", refusal=None, actor_id="t", **REGIME)
        run.created_at = datetime.now(UTC) - timedelta(hours=2)
        session.add(run)
        await session.flush()
        session.add(V2BrokerBalance(
            provider_id="exness_mt5_demo",
            broker_account_ext_id="476910140", balance="10000.0",
            margin_used="0.0", margin_available="10000.0",
            unrealized_pl="0.0", currency="USD", sync_run_id=run.id,
            server_hostname="ExnessKE-MT5Trial9", fetched_at_basis="b",
            **REGIME))
        run_id = run.id
    async with session_scope() as session:
        basis = await pin_basis(session)
    assert basis.sync_run_id == run_id
    assert basis.balance == "10000.0"
    assert basis.positions_present is False
    assert basis.staleness == "fresh"


def test_vocabulary_closed_sets():
    assert GATEWAY_DECISIONS == ("accept_with_notes", "deferred",
                                 "refused_under_policy")
    assert REFUSAL_REASONS == (
        "basis_unavailable", "basis_stale", "reference_price_uncited",
        "duplicate_intent", "basis_staleness_threshold_unseeded")
    assert DRIFT_VERDICTS == ("within_tolerance", "drift_minor",
                              "drift_major", "uncomputable")
