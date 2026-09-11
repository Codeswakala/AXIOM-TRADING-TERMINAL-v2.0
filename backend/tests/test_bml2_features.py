"""BO-B-ML2 Phase 1 — v2 feature set tests (fail-first).

Pre-fix expectation (bml2_probe_prefix.log): collection error —
``builtin_feature_set_v2`` does not exist. Post-fix: the v2 set is causal,
market-agnostic, deterministic, warm-up-disciplined, and the combined
primary set stays within the BO's ≤12 bound.
"""

from __future__ import annotations

import math
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from app.ml.dataset.market_data_query import (
    CanonicalOHLCVRecord,
    MarketSeriesKey,
    authority_from_source,
)
from app.ml.features.definitions import (
    builtin_feature_set_v1,
    builtin_feature_set_v2,
)

KEY = MarketSeriesKey(
    market_class="crypto", provider="internal", symbol="BTCUSDT", timeframe="H1"
)
BASE = datetime(2025, 1, 1, tzinfo=timezone.utc)


def _records(n: int = 60) -> list[CanonicalOHLCVRecord]:
    out: list[CanonicalOHLCVRecord] = []
    price = 100.0
    for i in range(n):
        direction = 1 if (i // 7) % 2 == 0 else -1
        open_ = price
        close = price + direction * (0.5 + 0.1 * math.sin(i / 4.0))
        high = max(open_, close) + 0.4
        low = min(open_, close) - 0.4
        out.append(
            CanonicalOHLCVRecord(
                series_key=KEY,
                open_time=BASE + timedelta(hours=i),
                open=Decimal(str(round(open_, 4))),
                high=Decimal(str(round(high, 4))),
                low=Decimal(str(round(low, 4))),
                close=Decimal(str(round(close, 4))),
                volume=Decimal(str(100 + i % 17)),
                source="historical:real",
                ingestion_run_id=None,
                authority_classification=authority_from_source("historical:real"),
                source_record_id=f"bml2-{i:05d}",
            )
        )
        price = close
    return out


def test_bml2_feature_set_v2_exists_and_is_causal() -> None:
    features = builtin_feature_set_v2()
    assert len(features) == 8, f"expected 8 v2 features, got {len(features)}"
    for feature in features:
        assert feature.spec.causal is True
        feature.spec.assert_causal()  # raises on lookahead declaration
        assert feature.spec.feature_version == "v2"


def test_bml2_primary_feature_count_within_budget() -> None:
    combined = list(builtin_feature_set_v1()) + list(builtin_feature_set_v2())
    assert len(combined) <= 12, (
        f"primary feature set exceeds the BO bound: {len(combined)} > 12"
    )
    names = [feature.spec.feature_name for feature in combined]
    assert len(names) == len(set(names)), "duplicate feature names in the primary set"
    forbidden = {
        "symbol",
        "provider",
        "market_class",
        "symbol_id",
        "one_hot_symbol",
        "symbol_identity",
    }
    assert forbidden.isdisjoint(set(names))


def test_bml2_v2_features_deterministic_and_warmup_disciplined() -> None:
    records = _records(60)
    features = builtin_feature_set_v2()
    names = [feature.spec.feature_name for feature in features]
    def _pass() -> dict[str, list]:
        return {
            name: [feature.compute(records, i) for i in range(len(records))]
            for name, feature in zip(names, features, strict=True)
        }

    first_pass = _pass()
    second_pass = _pass()
    assert first_pass == second_pass, "v2 features are not deterministic on identical input"
    # Warm-up discipline: lookback features must be None (excluded, never
    # fabricated) until their windows are complete.
    roc = first_pass["roc_12"]
    atr = first_pass["atr_norm_14"]
    assert all(value is None for value in roc[:11]), "roc_12 must be None for indices < 12"
    assert all(value is None for value in atr[:13]), "atr_norm_14 must be None for indices < 14"
    # And populated afterwards.
    assert all(value is not None for value in roc[12:])
    assert all(value is not None for value in atr[14:])
    # Real values, not fabricated constants.
    assert len({str(value) for value in roc[12:]}) > 3
    assert len({str(value) for value in atr[14:]}) > 3


def test_bml2_time_features_bounded_and_clock_driven() -> None:
    records = _records(24)
    features = builtin_feature_set_v2()
    by_name = {feature.spec.feature_name: feature for feature in features}
    for i in range(24):
        sin = by_name["hour_sin"].compute(records, i)
        cos = by_name["hour_cos"].compute(records, i)
        assert sin is not None and cos is not None
        assert -1.0 <= float(sin) <= 1.0
        assert -1.0 <= float(cos) <= 1.0
        hour = records[i].open_time.hour
        expected_sin = round(math.sin(2 * math.pi * hour / 24), 8)
        assert abs(float(sin) - expected_sin) < 1e-6
    # Distinct hours produce distinct encodings.
    values = {float(by_name["hour_sin"].compute(records, i)) for i in range(24)}
    assert len(values) > 10


def test_bml2_structure_feature_is_event_recency_capped() -> None:
    records = _records(60)
    features = builtin_feature_set_v2()
    by_name = {feature.spec.feature_name: feature for feature in features}
    bos = by_name["structure_bos_rec"]
    values = [bos.compute(records, i) for i in range(len(records))]
    # None until the first breakout event is detectable (k=20 warm-up + event).
    assert any(value is None for value in values[:25])
    populated = [value for value in values if value is not None]
    assert populated, "structure feature never populates"
    assert all(0 <= float(value) <= 200 for value in populated), "recency must be capped at 200"
