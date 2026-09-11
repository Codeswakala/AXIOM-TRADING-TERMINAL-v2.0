"""BO-B-ML Phase 1 — real model property tests (fail-first).

Pre-fix expectation (bml_probe_prefix.log): collection error — the logistic
model module does not exist. Post-fix: determinism, real (non-degenerate)
probabilities, no-identity discipline, and explainability surfaces are pinned.
"""

from __future__ import annotations

import math

from app.ml.models.logistic_regression import (
    LogisticRegressionModel,
    PredictiveModelHarness,
)


def _rows(n: int = 40) -> tuple[list[dict[str, float]], list[int]]:
    rows = [
        {"return_1": math.sin(i / 3.0) * 0.01, "range_pct": 0.02 + 0.01 * math.cos(i / 5.0)}
        for i in range(n)
    ]
    labels = [1 if rows[i]["return_1"] + rows[i]["range_pct"] > 0.015 else 0 for i in range(n)]
    return rows, labels


def test_bml_model_is_deterministic_given_seed() -> None:
    rows, labels = _rows()
    a = LogisticRegressionModel(seed=7)
    b = LogisticRegressionModel(seed=7)
    a.fit(rows, labels)
    b.fit(rows, labels)
    assert a.coefficients == b.coefficients
    assert a.intercept == b.intercept
    pa = a.predict_proba(rows[:5])
    pb = b.predict_proba(rows[:5])
    assert pa == pb


def test_bml_model_emits_real_probabilities_not_degenerate() -> None:
    rows, labels = _rows()
    model = LogisticRegressionModel(seed=11)
    model.fit(rows, labels)
    proba = model.predict_proba(rows[:10])
    values = [float(p["class_1"]) for p in proba]
    assert all(0.0 < v < 1.0 for v in values)
    assert all(
        abs(v + float(p["class_0"]) - 1.0) < 1e-9
        for v, p in zip(values, proba, strict=True)
    )
    # Real probabilities vary with the features — they are not a constant
    # degenerate prior.
    assert len(set(round(v, 8) for v in values)) > 1
    assert "degenerate_prior" not in proba[0]


def test_bml_model_is_explainable_and_market_agnostic() -> None:
    rows, labels = _rows()
    model = LogisticRegressionModel(seed=3)
    model.fit(rows, labels)
    assert set(model.coefficients) == {"return_1", "range_pct"}
    forbidden = {
        "symbol",
        "provider",
        "market_class",
        "symbol_id",
        "one_hot_symbol",
        "symbol_identity",
    }
    assert forbidden.isdisjoint(set(model.coefficients))
    payload = model.artifact_payload()
    assert payload["framework"] == "pure-python-logistic-regression-sgd"
    assert "coefficients" in payload
    assert "scaler" in payload
    assert "seed" in payload


def test_bml_harness_extends_the_governed_harness() -> None:
    # The predictive harness inherits the governed pin-resolution harness —
    # the B-ML training path is the same pre-registration/approval machinery,
    # not a parallel ungoverned path.
    from app.ml.models.harness import BaselineModelHarness

    assert issubclass(PredictiveModelHarness, BaselineModelHarness)
