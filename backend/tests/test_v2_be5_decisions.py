"""V2 BE-5 U-2 decision-contract tests — BO-V2-BE-5-001 T-7 (fail-first).

Each contract: >=1 passing and >=1 typed-refusal test. Pure functions over
V1 evaluator outputs; spec citations carried in every outcome; economic and
statistical conclusions independent. No DB, no network, no credential.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.v2.research_governance.contracts import (
    DEPLOYMENT_CLASSES,
    PROMOTION_LADDER,
    DecisionOutcome,
)
from app.v2.research_governance.decisions import (
    BOOTSTRAP_SAMPLES_MIN,
    CALIBRATION_ECE_WARNING,
    CONFIDENCE_LEVEL,
    decide_promotion,
    evaluate_calibration,
    evaluate_economic,
    evaluate_eligibility,
    evaluate_freshness,
    evaluate_statistical,
)

UTC = timezone.utc
NOW = datetime(2026, 9, 2, 12, 0, tzinfo=UTC)


def _valid_validation_report() -> dict:
    return {
        "walk_forward": {"folds": 6, "metric": "accuracy"},
        "out_of_sample": {"metric_value": 0.61},
        "bootstrap": {"samples": 200, "interval": [0.52, 0.68]},
        "significance": {"p_value": 0.01},
        "uncertainty": {"interval": [0.52, 0.68], "confidence": 0.95},
        "evaluated_at": NOW.isoformat(),
    }


def _valid_calibration_report() -> dict:
    return {"ece": 0.04, "bin_count": 10, "evaluated_at": NOW.isoformat()}


def _valid_economic_report() -> dict:
    return {
        "spread": 0.0001, "commission": 0.00007, "slippage": 0.0001,
        "latency_ms": 120, "liquidity": "normal",
        "net_expectancy": 0.0004, "evaluated_at": NOW.isoformat(),
    }


# --- thresholds are V1-config citations, not invented -----------------------


def test_threshold_constants_cite_v1_configs() -> None:
    """BO §3: thresholds are citations of the V1 configs, not invented —
    asserted against live default instances of the V1 dataclasses."""
    from app.ml.calibration.service import CalibrationConfig
    from app.ml.validation.service import ValidationConfig

    cal = CalibrationConfig()
    val = ValidationConfig()
    assert CALIBRATION_ECE_WARNING == cal.warning_threshold_ece
    assert CONFIDENCE_LEVEL == val.confidence_level
    assert BOOTSTRAP_SAMPLES_MIN == val.bootstrap_samples


# --- eligibility (07_ML_SPEC: Statistical Validation + Deployment Policy) ----


def test_eligibility_pass() -> None:
    out = evaluate_eligibility(_valid_validation_report())
    assert isinstance(out, DecisionOutcome)
    assert out.status == "eligible"
    assert "Statistical Validation" in out.citation
    assert out.reasons == []


def test_eligibility_refused_missing_bootstrap() -> None:
    report = _valid_validation_report()
    del report["bootstrap"]
    out = evaluate_eligibility(report)
    assert out.status == "ineligible"
    assert any(r["missing"] == "bootstrap" for r in out.reasons)


def test_eligibility_refused_no_uncertainty() -> None:
    """07_ML_SPEC: 'Results shall include uncertainty—not only point
    estimates' — a report without intervals is ineligible."""
    report = _valid_validation_report()
    del report["uncertainty"]
    out = evaluate_eligibility(report)
    assert out.status == "ineligible"
    assert any(r["missing"] == "uncertainty" for r in out.reasons)


def test_eligibility_refused_insufficient_bootstrap_samples() -> None:
    report = _valid_validation_report()
    report["bootstrap"]["samples"] = 10
    out = evaluate_eligibility(report)
    assert out.status == "ineligible"


def test_eligibility_report_existence_never_sufficient() -> None:
    """An empty report object exists but proves nothing (BO T-7)."""
    out = evaluate_eligibility({})
    assert out.status == "ineligible"
    assert len(out.reasons) >= 3


# --- calibration -------------------------------------------------------------


def test_calibration_pass() -> None:
    out = evaluate_calibration(_valid_calibration_report(), as_of=NOW)
    assert out.status == "calibrated"
    assert out.thresholds["ece_warning"] == CALIBRATION_ECE_WARNING


def test_calibration_miscalibrated() -> None:
    report = _valid_calibration_report()
    report["ece"] = 0.30
    out = evaluate_calibration(report, as_of=NOW)
    assert out.status == "miscalibrated"


def test_calibration_stale() -> None:
    report = _valid_calibration_report()
    report["evaluated_at"] = (NOW - timedelta(days=120)).isoformat()
    out = evaluate_calibration(report, as_of=NOW)
    assert out.status == "stale"


def test_calibration_refused_missing_ece() -> None:
    out = evaluate_calibration({"evaluated_at": NOW.isoformat()}, as_of=NOW)
    assert out.status == "miscalibrated"
    assert any("missing" in r for r in out.reasons)


# --- freshness ---------------------------------------------------------------


def test_freshness_fresh() -> None:
    out = evaluate_freshness(NOW - timedelta(days=2), as_of=NOW)
    assert out.status == "fresh"


def test_freshness_stale_then_expired() -> None:
    stale = evaluate_freshness(NOW - timedelta(days=45), as_of=NOW)
    assert stale.status == "stale"
    expired = evaluate_freshness(NOW - timedelta(days=200), as_of=NOW)
    assert expired.status == "expired"


def test_freshness_unknown_is_typed() -> None:
    out = evaluate_freshness(None, as_of=NOW)
    assert out.status == "unknown"  # allowed state, never guessed


# --- economic (independent of statistical — 07_ML_SPEC Economic Validation) --


def test_economic_viable() -> None:
    out = evaluate_economic(_valid_economic_report())
    assert out.status == "viable"
    assert "Economic Validation" in out.citation


def test_economic_unviable() -> None:
    report = _valid_economic_report()
    report["net_expectancy"] = -0.0002
    out = evaluate_economic(report)
    assert out.status == "unviable"


def test_economic_refused_missing_cost_inputs() -> None:
    out = evaluate_economic({"net_expectancy": 0.01})
    assert out.status == "unevaluated"
    assert any(r["missing"] == "spread" for r in out.reasons)


def test_economic_and_statistical_are_independent() -> None:
    """A model may be statistically significant yet economically unusable
    — both conclusions reported independently (07_ML_SPEC)."""
    stat = evaluate_statistical(_valid_validation_report())
    econ = evaluate_economic(
        {**_valid_economic_report(), "net_expectancy": -0.01})
    assert stat.status == "significant"
    assert econ.status == "unviable"  # neither overrides the other


# --- statistical -------------------------------------------------------------


def test_statistical_significant_and_not() -> None:
    assert evaluate_statistical(_valid_validation_report()).status == "significant"
    weak = _valid_validation_report()
    weak["significance"]["p_value"] = 0.4
    assert evaluate_statistical(weak).status == "not_significant"


# --- promotion ladder + rollback ----------------------------------------------


def _passing_statuses() -> dict:
    return {
        "eligibility_status": "eligible", "calibration_status": "calibrated",
        "freshness_status": "fresh", "economic_status": "viable",
        "statistical_status": "significant",
    }


def test_promotion_ladder_vocabulary() -> None:
    assert PROMOTION_LADDER == ("research", "shadow", "champion", "challenger", "retired")
    assert set(DEPLOYMENT_CLASSES) == set(PROMOTION_LADDER)


def test_promotion_allowed_all_passing() -> None:
    out = decide_promotion(
        statuses=_passing_statuses(), current_class="research",
        target_class="shadow", rollback_target_version="1.0.0",
        mode="RESEARCH")
    assert out.status == "allowed"


def test_promotion_refused_not_all_passing() -> None:
    statuses = _passing_statuses()
    statuses["economic_status"] = "unviable"
    out = decide_promotion(
        statuses=statuses, current_class="research", target_class="shadow",
        rollback_target_version="1.0.0", mode="RESEARCH")
    assert out.status == "refused"
    assert any(r.get("failing") == "economic_status" for r in out.reasons)


def test_promotion_refused_without_rollback_target() -> None:
    """07_ML_SPEC Deployment Policy: rollback availability required."""
    out = decide_promotion(
        statuses=_passing_statuses(), current_class="research",
        target_class="shadow", rollback_target_version=None, mode="RESEARCH")
    assert out.status == "refused"
    assert any("rollback" in str(r) for r in out.reasons)


def test_promotion_refused_wrong_mode() -> None:
    out = decide_promotion(
        statuses=_passing_statuses(), current_class="research",
        target_class="shadow", rollback_target_version="1.0.0", mode="LIVE")
    assert out.status == "refused"


def test_promotion_refused_ladder_skip() -> None:
    """research → champion directly skips shadow: refused."""
    out = decide_promotion(
        statuses=_passing_statuses(), current_class="research",
        target_class="champion", rollback_target_version="1.0.0",
        mode="RESEARCH")
    assert out.status == "refused"
