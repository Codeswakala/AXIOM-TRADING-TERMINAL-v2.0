"""V2 BE-2 unit tests — contracts, guards, fingerprints, seed manifest,
verification hashing. Pure unit level; integration lives in
test_v2_marketdata_integration.py.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from decimal import Decimal
from types import SimpleNamespace

import pytest

from app.v2.errors.contract import V2Error
from app.v2.marketdata.integrity import (
    check_future_data,
    check_gaps,
    check_ordering,
    check_stale_transition,
    compute_fingerprint,
    unmapped_symbol_finding,
    verification_mismatch_finding,
)
from app.v2.marketdata.provenance import (
    ACTIVE_AUTHORITY_VALUES,
    AUTHORITY_DISPLAY_LABELS,
    AUTHORITY_HISTORICAL_IMPORTED,
    build_provenance,
    compute_freshness,
    map_v1_source_marker,
    timeframe_seconds,
)
from app.v2.marketdata.seed import (
    SEED_MANIFEST_HASH,
    V2_MD_INSTRUMENT_SEED,
    V2_MD_SOURCE_SEED,
    V2_MD_SYMBOL_MAP_SEED,
    compute_seed_manifest_hash,
)
from app.v2.marketdata.verification import (
    VerificationScopeItem,
    compute_content_hash,
    validate_scope,
)

UTC = timezone.utc


class TestActiveAuthorityGuard:
    """BO-V2-BE-2-001 §3.2 — active vocabulary is constitutionally bounded."""

    def test_active_set_is_exactly_the_authorized_pair_plus_unknown(self):
        assert ACTIVE_AUTHORITY_VALUES == {"seed:synthetic", "live:simulated", "unknown"}

    def test_reserved_historical_imported_is_refused(self):
        with pytest.raises(V2Error):
            build_provenance(
                source_kind="import",
                authority=AUTHORITY_HISTORICAL_IMPORTED,
                source_id="import.future",
                as_of=None,
            )

    def test_arbitrary_authority_is_refused(self):
        with pytest.raises(V2Error):
            build_provenance(
                source_kind="simulator",
                authority="live:real",
                source_id="sim.local",
                as_of=None,
            )

    def test_active_authorities_build_with_mandatory_label(self):
        for authority in ACTIVE_AUTHORITY_VALUES:
            p = build_provenance(
                source_kind="simulator",
                authority=authority,
                source_id="sim.local",
                as_of=datetime.now(UTC),
            )
            assert p.display_label == AUTHORITY_DISPLAY_LABELS[authority]

    def test_v1_marker_mapping_is_truthful(self):
        assert map_v1_source_marker("live:simulated")[2] == "live:simulated"
        assert map_v1_source_marker("seed:synthetic")[2] == "seed:synthetic"
        # Unrecognized markers surface as unknown — never guessed.
        assert map_v1_source_marker("mystery:feed")[2] == "unknown"
        assert map_v1_source_marker(None)[2] == "unknown"


class TestFreshness:
    def test_fresh_within_two_periods(self):
        last = datetime.now(UTC) - timedelta(seconds=90)
        assert compute_freshness(last, "M1") in ("fresh", "stale")  # boundary-safe
        assert compute_freshness(datetime.now(UTC), "M1") == "fresh"

    def test_stale_and_expired(self):
        now = datetime.now(UTC)
        assert compute_freshness(now - timedelta(minutes=5), "M1", now=now) == "stale"
        assert compute_freshness(now - timedelta(minutes=30), "M1", now=now) == "expired"

    def test_unknown_when_no_data(self):
        assert compute_freshness(None, "M1") == "unknown"

    def test_naive_datetime_rejected(self):
        with pytest.raises(Exception):
            compute_freshness(datetime(2026, 8, 24, 12, 0, 0), "M1")

    def test_unsupported_timeframe_rejected(self):
        with pytest.raises(V2Error):
            timeframe_seconds("M7")


class TestFingerprints:
    def test_deterministic(self):
        a = compute_fingerprint("s", "gap", "2026-08-24T00:00:00+00:00")
        b = compute_fingerprint("s", "gap", "2026-08-24T00:00:00+00:00")
        assert a == b

    def test_distinct_per_type_and_key(self):
        base = compute_fingerprint("s", "gap", "k")
        assert compute_fingerprint("s", "duplicate", "k") != base
        assert compute_fingerprint("s", "gap", "k2") != base
        assert compute_fingerprint("s2", "gap", "k") != base

    def test_unknown_type_rejected(self):
        with pytest.raises(ValueError):
            compute_fingerprint("s", "not_a_type", "k")


class TestIntegrityValidators:
    def _times(self, *minutes: int) -> list[datetime]:
        base = datetime(2026, 8, 24, 10, 0, tzinfo=UTC)
        return [base + timedelta(minutes=m) for m in minutes]

    def test_ordering_clean(self):
        assert check_ordering("s", self._times(0, 1, 2, 3)) == []

    def test_out_of_order_detected(self):
        findings = check_ordering("s", self._times(0, 2, 1, 3))
        assert any(f.exception_type == "out_of_order" for f in findings)

    def test_duplicate_detected(self):
        findings = check_ordering("s", self._times(0, 1, 1, 2))
        assert any(f.exception_type == "duplicate" for f in findings)

    def test_gap_fingerprint_stable_within_same_coverage(self):
        """DEL-003: same coverage end → identical fingerprints (no-op re-detect)."""
        f1 = check_gaps("s", "M1", self._times(0, 1, 4))
        f2 = check_gaps("s", "M1", self._times(0, 1, 4))
        assert len(f1) == 2  # minutes 2 and 3 missing
        assert {f.fingerprint for f in f1} == {f.fingerprint for f in f2}

    def test_gap_fingerprint_changes_when_coverage_advances(self):
        """DEL-003: coverage-end state basis — the SAME missing period gets a
        NEW fingerprint after new bars advance coverage (explicit recorded
        state transition), and detail records the coverage end."""
        before = check_gaps("s", "M1", self._times(0, 1, 4))
        after = check_gaps("s", "M1", self._times(0, 1, 4, 5))
        # same missing periods (minutes 2, 3) in both detections
        missing_before = {f.detail["missing_period_start"] for f in before}
        missing_after = {f.detail["missing_period_start"] for f in after}
        assert missing_before == missing_after
        # but fingerprints differ because coverage end moved 10:04 → 10:05
        assert {f.fingerprint for f in before}.isdisjoint(
            {f.fingerprint for f in after}
        )
        assert all(f.detail["coverage_end"].endswith("10:05:00+00:00") for f in after)

    def test_future_data_detected(self):
        now = datetime(2026, 8, 24, 10, 0, tzinfo=UTC)
        f = check_future_data("s", now + timedelta(minutes=5), now=now)
        assert f is not None and f.exception_type == "future_data"
        assert check_future_data("s", now - timedelta(minutes=5), now=now) is None

    def test_stale_transition_edges_only(self):
        assert check_stale_transition("s", "fresh", "fresh", episode_boundary="b") is None
        assert check_stale_transition("s", "stale", "fresh", episode_boundary="b") is None
        f = check_stale_transition("s", "fresh", "stale", episode_boundary="b1")
        assert f is not None and f.exception_type == "stale"
        # New episode boundary → new fingerprint (episode semantics)
        f2 = check_stale_transition("s", "fresh", "stale", episode_boundary="b2")
        assert f2.fingerprint != f.fingerprint

    def test_unmapped_and_mismatch_findings(self):
        u = unmapped_symbol_finding("sim.local", "ZZZUSD")
        assert u.exception_type == "unmapped_symbol"
        m = verification_mismatch_finding("mdv-1", "aaa", "bbb")
        assert m.exception_type == "verification_mismatch"
        assert "aaa" in m.detail["expected_hash"]


class TestSeedManifest:
    """Plan C.4 — closed, versioned, hash-manifested seed inventory."""

    def test_manifest_hash_is_deterministic_and_current(self):
        assert compute_seed_manifest_hash() == SEED_MANIFEST_HASH
        assert len(SEED_MANIFEST_HASH) == 64

    def test_exactly_two_sources_no_reserved_seeded(self):
        assert len(V2_MD_SOURCE_SEED) == 2
        ids = {s["source_id"] for s in V2_MD_SOURCE_SEED}
        assert ids == {"sim.local", "seed.local"}
        assert all(s["kind"] != "reserved" for s in V2_MD_SOURCE_SEED)
        assert all(
            s["authority"] in ("seed:synthetic", "live:simulated") for s in V2_MD_SOURCE_SEED
        )

    def test_instruments_match_v1_simulator_universe(self):
        symbols = {i["display_symbol"] for i in V2_MD_INSTRUMENT_SEED}
        # Exactly the V1 LiveMarketService._base_price defaults set
        assert symbols == {
            "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "USDCHF",
            "NZDUSD", "EURGBP", "BTCUSD", "ETHUSD", "SOLUSD", "XAUUSD",
        }

    def test_mappings_cover_source_x_instrument(self):
        assert len(V2_MD_SYMBOL_MAP_SEED) == len(V2_MD_SOURCE_SEED) * len(
            V2_MD_INSTRUMENT_SEED
        )


def _row(symbol: str, minute: int, close: str = "1.1") -> SimpleNamespace:
    return SimpleNamespace(
        market_class="forex",
        symbol=symbol,
        timeframe="M1",
        open_time=datetime(2026, 8, 24, 10, minute, tzinfo=UTC),
        open=Decimal("1.0"),
        high=Decimal("1.2"),
        low=Decimal("0.9"),
        close=Decimal(close),
        volume=Decimal("100"),
    )


class TestVerificationHashing:
    def test_hash_deterministic_and_order_independent(self):
        rows = [_row("EURUSD", 0), _row("EURUSD", 1), _row("EURUSD", 2)]
        assert compute_content_hash(rows) == compute_content_hash(list(reversed(rows)))

    def test_hash_changes_on_any_value_change(self):
        rows = [_row("EURUSD", 0), _row("EURUSD", 1)]
        tampered = [_row("EURUSD", 0), _row("EURUSD", 1, close="9.9")]
        assert compute_content_hash(rows) != compute_content_hash(tampered)

    def test_empty_scope_rejected(self):
        with pytest.raises(V2Error):
            validate_scope([], datetime.now(UTC))

    def test_oversized_scope_rejected(self):
        items = [
            VerificationScopeItem(f"forex.x{i}", "M1", "sim.local") for i in range(21)
        ]
        with pytest.raises(V2Error):
            validate_scope(items, datetime.now(UTC))

    def test_naive_as_of_rejected(self):
        with pytest.raises(Exception):
            validate_scope(
                [VerificationScopeItem("forex.eurusd", "M1", "sim.local")],
                datetime(2026, 8, 24, 12, 0),
            )
