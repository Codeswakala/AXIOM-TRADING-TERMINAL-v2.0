"""BE-5 U-2 decision contracts — pure functions over V1 evaluator outputs.

BO-V2-BE-5-001 T-7. Every threshold constant below is CITED FROM the V1
service configs (BO §3: no invented numbers); the citation test asserts
equality with the live config values. Every outcome carries its
07_ML_SPEC section citation into ``decision_basis``.

Pure: no I/O, no DB, no clock reads (``as_of`` is always a parameter),
no randomness.
"""

from __future__ import annotations

from datetime import datetime, timedelta

from app.ml.calibration.service import CalibrationConfig
from app.ml.validation.service import ValidationConfig
from app.v2.research_governance.contracts import (
    PROMOTION_LADDER,
    DecisionOutcome,
)

# --- Threshold constants: citations of V1 configs (BO §3) --------------------
# The V1 configs are slotted dataclasses; the cited values are their field
# defaults (identical to instantiating the default config — asserted by the
# citation test against live instances).
_CAL_DEFAULTS = {f.name: f.default for f in __import__("dataclasses").fields(CalibrationConfig)}
_VAL_DEFAULTS = {f.name: f.default for f in __import__("dataclasses").fields(ValidationConfig)}

# app/ml/calibration/service.py::CalibrationConfig.warning_threshold_ece
CALIBRATION_ECE_WARNING: float = _CAL_DEFAULTS["warning_threshold_ece"]
# app/ml/validation/service.py::ValidationConfig.confidence_level
CONFIDENCE_LEVEL: float = _VAL_DEFAULTS["confidence_level"]
# app/ml/validation/service.py::ValidationConfig.bootstrap_samples
BOOTSTRAP_SAMPLES_MIN: int = _VAL_DEFAULTS["bootstrap_samples"]

# Significance bound derived from the cited confidence level (1 - 0.95):
SIGNIFICANCE_P_BOUND: float = round(1.0 - CONFIDENCE_LEVEL, 10)

# Freshness bounds — band-level declared bounds (disclosed in every
# outcome; a future governed change may replace them without schema change)
FRESHNESS_STALE_AFTER = timedelta(days=30)
FRESHNESS_EXPIRED_AFTER = timedelta(days=90)
CALIBRATION_STALE_AFTER = FRESHNESS_EXPIRED_AFTER

_SPEC = "docs/governance/07_ML_SPEC.md"


def _missing(report: dict, keys: tuple[str, ...]) -> list[dict]:
    return [{"missing": k} for k in keys if k not in report or report[k] in (None, {})]


# --- Eligibility (Statistical Validation + Deployment Policy) -----------------


def evaluate_eligibility(validation_report: dict) -> DecisionOutcome:
    """07_ML_SPEC 'Statistical Validation': walk-forward, out-of-sample,
    bootstrap, significance — and uncertainty, not only point estimates.
    Missing any element => ineligible with typed reasons."""
    citation = f"{_SPEC} §Statistical Validation + §Deployment Policy"
    required = ("walk_forward", "out_of_sample", "bootstrap",
                "significance", "uncertainty")
    reasons = _missing(validation_report, required)

    bootstrap = validation_report.get("bootstrap") or {}
    if not reasons and int(bootstrap.get("samples", 0)) < BOOTSTRAP_SAMPLES_MIN:
        reasons.append({
            "failing": "bootstrap.samples",
            "value": bootstrap.get("samples"),
            "required_min": BOOTSTRAP_SAMPLES_MIN,
        })
    uncertainty = validation_report.get("uncertainty") or {}
    if "uncertainty" not in [r.get("missing") for r in reasons]:
        if not uncertainty.get("interval"):
            reasons.append({"missing": "uncertainty.interval"})

    status = "eligible" if not reasons else "ineligible"
    return DecisionOutcome(
        contract="eligibility", status=status, citation=citation,
        thresholds={"bootstrap_samples_min": BOOTSTRAP_SAMPLES_MIN,
                    "confidence_level": CONFIDENCE_LEVEL},
        reasons=reasons,
        inputs_ref={"report_keys": sorted(validation_report.keys())},
    )


# --- Calibration ---------------------------------------------------------------


def evaluate_calibration(calibration_report: dict, *, as_of: datetime) -> DecisionOutcome:
    citation = f"{_SPEC} §Statistical Validation (calibration)"
    thresholds = {"ece_warning": CALIBRATION_ECE_WARNING,
                  "stale_after_days": CALIBRATION_STALE_AFTER.days}
    reasons: list = []

    ece = calibration_report.get("ece")
    if ece is None:
        reasons.append({"missing": "ece"})
        return DecisionOutcome(contract="calibration", status="miscalibrated",
                               citation=citation, thresholds=thresholds,
                               reasons=reasons)
    evaluated_at = calibration_report.get("evaluated_at")
    if evaluated_at is not None:
        evaluated = datetime.fromisoformat(evaluated_at)
        if as_of - evaluated > CALIBRATION_STALE_AFTER:
            return DecisionOutcome(contract="calibration", status="stale",
                                   citation=citation, thresholds=thresholds,
                                   reasons=[{"stale_by_days":
                                             (as_of - evaluated).days}])
    if float(ece) > CALIBRATION_ECE_WARNING:
        return DecisionOutcome(contract="calibration", status="miscalibrated",
                               citation=citation, thresholds=thresholds,
                               reasons=[{"failing": "ece", "value": ece,
                                         "bound": CALIBRATION_ECE_WARNING}])
    return DecisionOutcome(contract="calibration", status="calibrated",
                           citation=citation, thresholds=thresholds)


# --- Freshness -------------------------------------------------------------------


def evaluate_freshness(last_evaluated: datetime | None, *, as_of: datetime) -> DecisionOutcome:
    """07_ML_SPEC §Drift Monitoring + §Continuous Learning. ``unknown`` is
    an allowed typed outcome — never guessed over."""
    citation = f"{_SPEC} §Drift Monitoring + §Continuous Learning"
    thresholds = {"stale_after_days": FRESHNESS_STALE_AFTER.days,
                  "expired_after_days": FRESHNESS_EXPIRED_AFTER.days}
    if last_evaluated is None:
        return DecisionOutcome(contract="freshness", status="unknown",
                               citation=citation, thresholds=thresholds,
                               reasons=[{"missing": "last_evaluated"}])
    age = as_of - last_evaluated
    if age > FRESHNESS_EXPIRED_AFTER:
        status = "expired"
    elif age > FRESHNESS_STALE_AFTER:
        status = "stale"
    else:
        status = "fresh"
    return DecisionOutcome(contract="freshness", status=status,
                           citation=citation, thresholds=thresholds,
                           inputs_ref={"age_days": age.days})


# --- Economic (independent of statistical) ----------------------------------------


def evaluate_economic(economic_report: dict) -> DecisionOutcome:
    """07_ML_SPEC §Economic Validation: spread/commission/slippage/latency/
    liquidity all required; 'statistically significant yet economically
    unusable' — this outcome NEVER reads statistical state."""
    citation = f"{_SPEC} §Economic Validation"
    required = ("spread", "commission", "slippage", "latency_ms", "liquidity")
    reasons = _missing(economic_report, required)
    if reasons:
        return DecisionOutcome(contract="economic", status="unevaluated",
                               citation=citation, reasons=reasons)
    net = economic_report.get("net_expectancy")
    if net is None:
        return DecisionOutcome(contract="economic", status="unevaluated",
                               citation=citation,
                               reasons=[{"missing": "net_expectancy"}])
    status = "viable" if float(net) > 0 else "unviable"
    return DecisionOutcome(contract="economic", status=status,
                           citation=citation,
                           inputs_ref={"net_expectancy": net})


# --- Statistical -----------------------------------------------------------------


def evaluate_statistical(validation_report: dict) -> DecisionOutcome:
    citation = f"{_SPEC} §Statistical Validation"
    significance = validation_report.get("significance") or {}
    p_value = significance.get("p_value")
    if p_value is None:
        return DecisionOutcome(contract="statistical", status="unevaluated",
                               citation=citation,
                               reasons=[{"missing": "significance.p_value"}])
    status = ("significant" if float(p_value) <= SIGNIFICANCE_P_BOUND
              else "not_significant")
    return DecisionOutcome(contract="statistical", status=status,
                           citation=citation,
                           thresholds={"p_bound": SIGNIFICANCE_P_BOUND},
                           inputs_ref={"p_value": p_value})


# --- Promotion ladder + rollback ---------------------------------------------------


_PASSING = {
    "eligibility_status": "eligible",
    "calibration_status": "calibrated",
    "freshness_status": "fresh",
    "economic_status": "viable",
    "statistical_status": "significant",
}

# Permitted single-step transitions (BO T-7; skipping refused).
_ALLOWED_TRANSITIONS = {
    ("research", "shadow"),
    ("shadow", "champion"),
    ("shadow", "challenger"),
    ("champion", "retired"),
    ("challenger", "retired"),
    ("challenger", "champion"),
    ("shadow", "retired"),
}


def decide_promotion(
    *, statuses: dict, current_class: str, target_class: str,
    rollback_target_version: str | None, mode: str,
) -> DecisionOutcome:
    """The ONLY path to a deployment-class change. All five statuses
    passing AND rollback target set AND RESEARCH mode AND a permitted
    single-step transition; every other path = refused (permanent typed
    event upstream)."""
    citation = f"{_SPEC} §Deployment Policy + §Model Registry (rollback)"
    reasons: list = []
    if mode != "RESEARCH":
        reasons.append({"failing": "mode", "value": mode,
                        "required": "RESEARCH"})
    for key, required in _PASSING.items():
        if statuses.get(key) != required:
            reasons.append({"failing": key, "value": statuses.get(key),
                            "required": required})
    if target_class != "retired" and not rollback_target_version:
        reasons.append({"failing": "rollback_target_version",
                        "value": None,
                        "required": "set and resolvable"})
    if current_class not in PROMOTION_LADDER or target_class not in PROMOTION_LADDER:
        reasons.append({"failing": "class_vocabulary"})
    elif (current_class, target_class) not in _ALLOWED_TRANSITIONS:
        reasons.append({"failing": "ladder_transition",
                        "value": f"{current_class}->{target_class}",
                        "required": "single permitted step"})
    status = "allowed" if not reasons else "refused"
    return DecisionOutcome(contract="promotion", status=status,
                           citation=citation, reasons=reasons,
                           inputs_ref={"from": current_class,
                                       "to": target_class})
