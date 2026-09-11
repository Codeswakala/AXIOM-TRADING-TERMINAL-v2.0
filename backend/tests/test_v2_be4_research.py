"""V2 BE-4 tests — BO-V2-BE-4-001 D-5 (plan §11 groups 1–6, 8; engine level).

Content-based row comparisons only — no position-based row assertions
(PGF-012 lesson). Socket guard active for every test in this module
(zero network attempts). Migration lifecycle tests live in
test_v2_be4_migration.py; API/RBAC tests in test_v2_be4_api.py.
"""

from __future__ import annotations

import json
import math
import socket
from datetime import datetime, timedelta, timezone

import pytest

from app.v2.research.chart_intelligence import (
    Annotation,
    Interpretation,
    _validate_annotation,
    _validate_interpretation,
    cie_to_json,
    compute_chart_intelligence,
)
from app.v2.research.market_context import (
    compute_market_context,
    input_content_hash,
    observations_to_json,
)
from app.v2.research.typing import (
    FAMILIES,
    TIMEFRAME_RELATIONSHIP_RULES,
    Observation,
    TypingViolation,
    validate_observation,
)
from app.v2.research.versioning import (
    ComputationVersionMismatch,
    compute_indicator_engine_hash,
    engine_versions,
    engine_versions_hash,
)

UTC = timezone.utc


@pytest.fixture(autouse=True)
def _socket_guard(monkeypatch):
    """BG-4: zero network attempts (name resolution + TCP establishment
    denied; asyncio's local socketpair untouched — accepted P2 pattern)."""

    def _deny(*_a, **_k):
        raise AssertionError("network attempt during BE-4 test")

    monkeypatch.setattr(socket, "getaddrinfo", _deny)
    monkeypatch.setattr(socket, "create_connection", _deny)


def _bars(n: int, tf_minutes: int, base: float = 100.0,
          start: datetime | None = None) -> list[dict]:
    """Deterministic labelled-synthetic wave (no randomness — BG-6)."""
    t0 = start or datetime(2026, 8, 1, tzinfo=UTC)
    out = []
    for i in range(n):
        px = base + 5 * math.sin(i / 7) + (i % 5) * 0.3
        out.append({
            "open_time": t0 + timedelta(minutes=tf_minutes * i),
            "open": px, "high": px + 0.6, "low": px - 0.6,
            "close": px + 0.2, "volume": 1000 + i,
        })
    return out


def _rich_input() -> dict[str, list[dict]]:
    return {"M15": _bars(384, 15), "H1": _bars(96, 60)}


def _canon(payload) -> str:
    return json.dumps(payload, sort_keys=True, default=str)


# ---------------------------------------------------------------------------
# Group 1 — determinism / reproducibility
# ---------------------------------------------------------------------------


def test_recompute_is_byte_identical() -> None:
    data = _rich_input()
    r1 = compute_market_context(data)
    r2 = compute_market_context(data)
    j1 = observations_to_json(r1.observations, r1.insufficient)
    j2 = observations_to_json(r2.observations, r2.insufficient)
    assert _canon(j1) == _canon(j2)

    c1 = cie_to_json(compute_chart_intelligence(j1["observations"]))
    c2 = cie_to_json(compute_chart_intelligence(j2["observations"]))
    assert _canon(c1) == _canon(c2)


def test_input_content_hash_stable_and_input_sensitive() -> None:
    data = _rich_input()
    h1 = input_content_hash(data)
    h2 = input_content_hash(_rich_input())
    assert h1 == h2  # same input ⇒ same hash

    changed = _rich_input()
    changed["M15"][0]["close"] = changed["M15"][0]["close"] + 0.0001
    assert input_content_hash(changed) != h1  # any change ⇒ new hash


def test_engine_versions_hash_canonical_serialization() -> None:
    versions = engine_versions()
    # OBS-3 pin: sorted keys, no whitespace
    expected_src = json.dumps(versions, sort_keys=True, separators=(",", ":"))
    import hashlib

    assert engine_versions_hash(versions) == hashlib.sha256(
        expected_src.encode()
    ).hexdigest()
    # key order must not matter
    reordered = dict(reversed(list(versions.items())))
    assert engine_versions_hash(reordered) == engine_versions_hash(versions)


def test_version_mismatch_is_typed_refusal() -> None:
    actual = compute_indicator_engine_hash()
    exc = ComputationVersionMismatch("indicator_engine", "0" * 64, actual)
    assert "mismatch" in str(exc)
    assert exc.component == "indicator_engine"


# ---------------------------------------------------------------------------
# Group 2 — temporal integrity
# ---------------------------------------------------------------------------


def test_no_wall_clock_in_deterministic_core() -> None:
    """Construction-token scan (path-exact P2 pattern): the MCE/CIE modules
    must not read the wall clock or randomness."""
    from pathlib import Path

    backend = Path(__file__).resolve().parents[1]
    for rel in ("app/v2/research/market_context.py",
                "app/v2/research/chart_intelligence.py",
                "app/v2/research/typing.py"):
        text = (backend / rel).read_text()
        for token in ("datetime.now(", "utcnow(", "time.time(",
                      "random.", "uuid4("):
            assert token not in text, f"{token} found in {rel}"


def test_computation_is_pure_function_of_input() -> None:
    """Same bars, different call times ⇒ identical output (no hidden
    now() dependency)."""
    data = _rich_input()
    j1 = observations_to_json(*(lambda r: (r.observations, r.insufficient))(
        compute_market_context(data)))
    j2 = observations_to_json(*(lambda r: (r.observations, r.insufficient))(
        compute_market_context({k: list(v) for k, v in data.items()})))
    assert _canon(j1) == _canon(j2)


# ---------------------------------------------------------------------------
# Group 3 — lineage (engine level; DB walk in the API tests)
# ---------------------------------------------------------------------------


def test_every_output_traceable_to_basis() -> None:
    r = compute_market_context(_rich_input())
    by_id = {o.observation_id: o for o in r.observations}
    for obs in r.observations:
        if obs.layer == "observed":
            assert obs.indicator_basis is not None
            assert obs.indicator_basis["indicator_id"]
            assert obs.indicator_basis["engine"]
        else:
            assert obs.contributing_observation_ids
            for cid in obs.contributing_observation_ids:
                assert cid in by_id, f"dangling contribution {cid}"


def test_cie_outputs_reference_resolvable_bases() -> None:
    r = compute_market_context(_rich_input())
    body = observations_to_json(r.observations, r.insufficient)
    ci = compute_chart_intelligence(body["observations"])
    obs_ids = {o["observation_id"] for o in body["observations"]}
    ann_ids = {a.annotation_id for a in ci.annotations}
    for a in ci.annotations:
        assert set(a.basis_observation_ids) <= obs_ids
    for i in ci.interpretations:
        assert i.basis_ids
        assert set(i.basis_ids) <= (obs_ids | ann_ids)


# ---------------------------------------------------------------------------
# Group 4 — typing (layer/claim CHECK semantics; cross-TF rule; R-4 table)
# ---------------------------------------------------------------------------


def test_all_ten_families_emitted_on_rich_input() -> None:
    r = compute_market_context(_rich_input())
    assert r.status == "available"
    assert sorted({o.family for o in r.observations}) == sorted(FAMILIES)
    assert r.families_computed == 10


def test_zero_prediction_or_statistical_emissions() -> None:
    r = compute_market_context(_rich_input())
    assert all(o.layer != "statistical" for o in r.observations)
    assert all(o.claim_type != "prediction" for o in r.observations)


def test_layer_claim_coupling_enforced() -> None:
    bad = Observation(
        observation_id="x-1", family="prevailing_trend", timeframe="H1",
        layer="observed", claim_type="contextual_interpretation",
        statement={}, indicator_basis={"indicator_id": "SMA20"},
    )
    with pytest.raises(TypingViolation, match="coupling"):
        validate_observation(bad, known_ids=frozenset(), known_timeframes={})


def test_prediction_emission_refused() -> None:
    bad = Observation(
        observation_id="x-2", family="prevailing_trend", timeframe="H1",
        layer="statistical", claim_type="prediction",
        statement={}, contributing_observation_ids=("a",),
    )
    with pytest.raises(TypingViolation, match="no statistical/prediction"):
        validate_observation(bad, known_ids=frozenset({"a"}),
                             known_timeframes={"a": "H1"})


def test_cross_timeframe_fact_refused() -> None:
    """Plan §2: a cross-timeframe element may never claim fact/observed."""
    bad = Observation(
        observation_id="x-3", family="prevailing_trend", timeframe="M15+H1",
        layer="observed", claim_type="fact",
        statement={}, indicator_basis={"indicator_id": "SMA20"},
        contributing_observation_ids=("a", "b"),
    )
    with pytest.raises(TypingViolation, match="cross-timeframe"):
        validate_observation(
            bad, known_ids=frozenset({"a", "b"}),
            known_timeframes={"a": "M15", "b": "H1"},
        )


def test_unresolvable_contribution_refused() -> None:
    bad = Observation(
        observation_id="x-4", family="momentum_state", timeframe="H1",
        layer="derived", claim_type="derived_observation",
        statement={}, contributing_observation_ids=("ghost",),
    )
    with pytest.raises(TypingViolation, match="unresolvable"):
        validate_observation(bad, known_ids=frozenset(), known_timeframes={})


def test_r4_rule_table_every_permitted_class() -> None:
    """R-4: every permitted class validates at its pinned (layer, claim)."""
    known = frozenset({"a", "b"})
    tfs = {"a": "M15", "b": "H1"}
    for rel_class, (layer, claim) in TIMEFRAME_RELATIONSHIP_RULES.items():
        ok = Observation(
            observation_id=f"rel-{rel_class}", family="timeframe_relationships",
            timeframe="M15+H1", layer=layer, claim_type=claim,
            statement={"relationship_class": rel_class},
            contributing_observation_ids=("a", "b"),
            relationship_class=rel_class,
        )
        validate_observation(ok, known_ids=known, known_timeframes=tfs)


def test_r4_refusal_cases_per_class_boundary() -> None:
    """R-4: at least one refusal case per class boundary."""
    known = frozenset({"a", "b"})
    tfs = {"a": "M15", "b": "H1"}
    # (1) unknown class refused
    with pytest.raises(TypingViolation, match="unpermitted"):
        validate_observation(Observation(
            observation_id="rx-1", family="timeframe_relationships",
            timeframe="M15+H1", layer="derived",
            claim_type="derived_observation", statement={},
            contributing_observation_ids=("a", "b"),
            relationship_class="order_flow_inference",
        ), known_ids=known, known_timeframes=tfs)
    # (2) derived-class stated as contextual refused (wrong pinned pair)
    with pytest.raises(TypingViolation, match="requires"):
        validate_observation(Observation(
            observation_id="rx-2", family="timeframe_relationships",
            timeframe="M15+H1", layer="contextual",
            claim_type="contextual_interpretation", statement={},
            contributing_observation_ids=("a", "b"),
            relationship_class="trend_alignment",
        ), known_ids=known, known_timeframes=tfs)
    # (3) contextual-class stated as derived refused
    with pytest.raises(TypingViolation, match="requires"):
        validate_observation(Observation(
            observation_id="rx-3", family="timeframe_relationships",
            timeframe="M15+H1", layer="derived",
            claim_type="derived_observation", statement={},
            contributing_observation_ids=("a", "b"),
            relationship_class="higher_tf_context",
        ), known_ids=known, known_timeframes=tfs)
    # (4) single-timeframe relationship refused
    with pytest.raises(TypingViolation, match="span more than one"):
        validate_observation(Observation(
            observation_id="rx-4", family="timeframe_relationships",
            timeframe="H1", layer="derived",
            claim_type="derived_observation", statement={},
            contributing_observation_ids=("b",),
            relationship_class="trend_alignment",
        ), known_ids=frozenset({"b"}), known_timeframes={"b": "H1"})


def test_annotation_and_interpretation_typing() -> None:
    # annotation with prediction claim refused
    with pytest.raises(TypingViolation, match="annotation claim_type"):
        _validate_annotation(Annotation(
            annotation_id="a1", kind="level", claim_type="prediction",
            geometry={}, basis_observation_ids=("o1",),
        ), frozenset({"o1"}))
    # interpretation with empty basis refused (plan §4)
    with pytest.raises(TypingViolation, match="empty basis"):
        _validate_interpretation(Interpretation(
            interpretation_id="i1", claim_type="contextual_interpretation",
            text_statement={}, basis_ids=(),
        ), frozenset())
    # interpretation claiming fact refused
    with pytest.raises(TypingViolation, match="must be contextual"):
        _validate_interpretation(Interpretation(
            interpretation_id="i2", claim_type="fact",
            text_statement={}, basis_ids=("o1",),
        ), frozenset({"o1"}))


# ---------------------------------------------------------------------------
# Group 5 — typed outcomes (engine-level; API states in test_v2_be4_api)
# ---------------------------------------------------------------------------


def test_insufficient_data_is_typed_outcome() -> None:
    r = compute_market_context({"H1": _bars(30, 60)})  # short series
    assert r.status == "degraded"
    assert r.insufficient, "expected typed insufficient_data entries"
    for entry in r.insufficient:
        assert entry["outcome"] == "insufficient_data"
        assert entry["family"] in FAMILIES
        assert entry["required_bars"] is not None
        assert entry["available_bars"] == 30


def test_empty_input_is_unavailable() -> None:
    r = compute_market_context({"H1": []})
    assert r.status == "unavailable"
    assert r.observations == []


def test_single_timeframe_has_no_relationships() -> None:
    r = compute_market_context({"H1": _bars(96, 60)})
    assert all(o.family != "timeframe_relationships" for o in r.observations)
    assert r.families_requested == 9  # relationships not requested


# ---------------------------------------------------------------------------
# Group 6 — liquidity disclosure + session label honesty (band controls)
# ---------------------------------------------------------------------------


def test_liquidity_disclosure_propagated_verbatim() -> None:
    from app.services.indicator_registry import INDICATOR_REGISTRY

    r = compute_market_context(_rich_input())
    liq = [o for o in r.observations
           if o.family == "liquidity_context" and o.layer == "contextual"]
    assert liq
    expected = INDICATOR_REGISTRY["OBPATTERN"].disclosure
    if expected:
        for o in liq:
            assert o.statement["disclosure"] == expected


def test_session_context_label_only_disclosure() -> None:
    r = compute_market_context(_rich_input())
    sess = [o for o in r.observations if o.family == "session_context"]
    assert sess
    for o in sess:
        assert "no venue claim" in o.statement["disclosure"]
