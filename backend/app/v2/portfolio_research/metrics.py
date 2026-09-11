"""BE-6 U-2 risk metrics — pure deterministic functions (BO T-8/T-11).

No wall clock, no randomness, no sampling, no I/O. Every output carries
the full risk-metric contract; insufficiency is typed, never fabricated.
Confidence level cited from the established V1 config value
(ValidationConfig.confidence_level = 0.95 — the standing citation).
"""

from __future__ import annotations

import math

# Cited constant (app/ml/validation/service.py::ValidationConfig.confidence_level)
# — extracted the same way BE-5's decisions.py extracts it.
from dataclasses import fields as _dc_fields

from app.ml.validation.service import ValidationConfig as _VC
from app.v2.portfolio_research.contracts import (
    MetricResult,
    insufficient_result,
)

CONFIDENCE_LEVEL: float = {
    f.name: f.default for f in _dc_fields(_VC)
}["confidence_level"]

# z-score for the one-sided cited confidence level (0.95). Closed-form
# constant, not sampled; declared in the method citation.
_Z_95 = 1.6448536269514722

_SPECREF = "AXIOM-V2-BE-6-DA-PLAN-001 Part 2"


def _chi2_bounds(df: int, confidence: float) -> tuple[float, float]:
    """Two-sided chi-square quantiles via the Wilson–Hilferty closed-form
    approximation (deterministic; no scipy dependency). Accuracy declared
    in the citation; adequate for CI bracketing at research tier."""
    alpha = 1.0 - confidence
    z_low, z_high = _norm_ppf(alpha / 2.0), _norm_ppf(1.0 - alpha / 2.0)

    def wh(z: float) -> float:
        return df * (1.0 - 2.0 / (9.0 * df) + z * math.sqrt(2.0 / (9.0 * df))) ** 3

    return wh(z_low), wh(z_high)


def _norm_ppf(p: float) -> float:
    """Acklam's rational approximation of the standard normal inverse CDF
    (deterministic closed form; max abs error ~1.15e-9; cited)."""
    a = [-3.969683028665376e+01, 2.209460984245205e+02,
         -2.759285104469687e+02, 1.383577518672690e+02,
         -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02,
         -1.556989798598866e+02, 6.680131188771972e+01,
         -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01,
         -2.400758277161838e+00, -2.549732539343734e+00,
         4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01,
         2.445134137142996e+00, 3.754408661907416e+00]
    plow, phigh = 0.02425, 1 - 0.02425
    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
               ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    if p > phigh:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
               ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    q = p - 0.5
    r = q * q
    return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / \
           (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)


# --- Exposures --------------------------------------------------------------------


def compute_exposures(allocations: list[dict]) -> MetricResult:
    citation = f"gross=Σ|w|, net=Σw over declared weights ({_SPECREF})"
    if not allocations:
        return insufficient_result("exposures", "weight-aggregation",
                                   citation, {"allocations": 1},
                                   {"allocations": 0})
    per = {a["instrument_id"]: float(a["weight"]) for a in allocations}
    return MetricResult(
        metric="exposures", method="weight-aggregation",
        method_citation=citation,
        inputs={"allocation_count": len(allocations)},
        value={"per_instrument": per,
               "gross": sum(abs(w) for w in per.values()),
               "net": sum(per.values())},
        uncertainty={"basis": "deterministic"},
        limitations={"scope": "long-only v1; gross==net by construction"},
        time_basis={"basis": "allocation-declaration"},
    )


# --- Concentration ------------------------------------------------------------------


def compute_concentration(allocations: list[dict], *, top_n: int = 3) -> MetricResult:
    citation = f"HHI=Σw²; top-N share=Σ of N largest weights ({_SPECREF})"
    if not allocations:
        return insufficient_result("concentration", "hhi-topn", citation,
                                   {"allocations": 1}, {"allocations": 0})
    weights = sorted((float(a["weight"]) for a in allocations), reverse=True)
    return MetricResult(
        metric="concentration", method="hhi-topn",
        method_citation=citation,
        inputs={"allocation_count": len(weights), "top_n": top_n},
        value={"hhi": sum(w * w for w in weights),
               "top_n": top_n,
               "top_n_share": sum(weights[:top_n])},
        uncertainty={"basis": "deterministic"},
        limitations={"scope": "weight-based; no covariance adjustment"},
        time_basis={"basis": "allocation-declaration"},
    )


# --- Volatility ----------------------------------------------------------------------


def compute_volatility(log_returns: list[float]) -> MetricResult:
    citation = (
        "sample stdev of log returns; CI via chi-square bounds"
        f" (Wilson–Hilferty closed form) at confidence={CONFIDENCE_LEVEL}"
        " cited from ValidationConfig.confidence_level"
    )
    n = len(log_returns)
    if n < 2:
        return insufficient_result("volatility", "sample-stdev", citation,
                                   {"observations": 2}, {"observations": n})
    mean = sum(log_returns) / n
    var = sum((r - mean) ** 2 for r in log_returns) / (n - 1)
    sd = math.sqrt(var)
    df = n - 1
    chi_lo, chi_hi = _chi2_bounds(df, CONFIDENCE_LEVEL)
    ci = (math.sqrt(df * var / chi_hi), math.sqrt(df * var / chi_lo))
    return MetricResult(
        metric="volatility", method="sample-stdev",
        method_citation=citation,
        inputs={"observations": n},
        value={"stdev": sd, "variance": var, "observations": n},
        uncertainty={"interval": [ci[0], ci[1]],
                     "confidence": CONFIDENCE_LEVEL,
                     "method": "chi-square (Wilson–Hilferty approx)"},
        limitations={"scope": "per-period stdev; no annualization claimed;"
                              " iid assumption declared"},
        time_basis={"observations": n, "basis": "log-return series"},
    )


# --- Drawdown ---------------------------------------------------------------------------


def compute_drawdown(values: list[float]) -> MetricResult:
    citation = f"max peak-to-trough decline over the window ({_SPECREF})"
    if len(values) < 2:
        return insufficient_result("drawdown", "peak-trough", citation,
                                   {"observations": 2},
                                   {"observations": len(values)})
    peak = values[0]
    max_dd = 0.0
    peak_at_max = trough_at_max = values[0]
    for v in values:
        peak = max(peak, v)
        dd = (v - peak) / peak
        if dd < max_dd:
            max_dd, peak_at_max, trough_at_max = dd, peak, v
    return MetricResult(
        metric="drawdown", method="peak-trough",
        method_citation=citation,
        inputs={"observations": len(values)},
        value={"max_drawdown": max_dd, "peak_value": peak_at_max,
               "trough_value": trough_at_max},
        uncertainty={"basis": "deterministic over the window"},
        limitations={"note": "window-dependence: result is a property of"
                             " the declared window only"},
        time_basis={"observations": len(values), "basis": "value series"},
    )


# --- VaR (both methods, reported separately, never merged) --------------------------------


VAR_MIN_OBSERVATIONS = 5


def compute_var(log_returns: list[float], *, confidence: float) -> dict[str, MetricResult]:
    n = len(log_returns)
    hist_citation = (
        "historical VaR = -(empirical lower quantile of returns) at"
        f" confidence={confidence}; order-statistic method ({_SPECREF})"
    )
    para_citation = (
        "parametric-normal VaR = -(mean - z*stdev),"
        f" z={_Z_95} at confidence={confidence}; normality ASSUMED ({_SPECREF})"
    )
    if n < VAR_MIN_OBSERVATIONS:
        return {
            "historical": insufficient_result(
                "var_historical", "empirical-quantile", hist_citation,
                {"observations": VAR_MIN_OBSERVATIONS}, {"observations": n}),
            "parametric_normal": insufficient_result(
                "var_parametric_normal", "normal-quantile", para_citation,
                {"observations": VAR_MIN_OBSERVATIONS}, {"observations": n}),
        }
    sorted_r = sorted(log_returns)
    q_index = int(math.floor((1.0 - confidence) * n))
    hist_var = -sorted_r[q_index]
    mean = sum(log_returns) / n
    sd = math.sqrt(sum((r - mean) ** 2 for r in log_returns) / (n - 1))
    para_var = -(mean - _Z_95 * sd)
    historical = MetricResult(
        metric="var_historical", method="empirical-quantile",
        method_citation=hist_citation,
        inputs={"observations": n, "confidence": confidence},
        value={"var": hist_var, "quantile_index": q_index},
        uncertainty={"method": "order-statistic interval",
                     "interval": [-sorted_r[min(q_index + 1, n - 1)],
                                  -sorted_r[max(q_index - 1, 0)]]},
        limitations={"note": "empirical; window-dependent; no tail model"},
        time_basis={"observations": n, "basis": "log-return series"},
    )
    parametric = MetricResult(
        metric="var_parametric_normal", method="normal-quantile",
        method_citation=para_citation,
        inputs={"observations": n, "confidence": confidence},
        value={"var": para_var, "mean": mean, "stdev": sd},
        uncertainty={"basis": "closed-form given normality"},
        limitations={"assumption": "returns NORMALLY distributed —"
                                   " declared, not verified"},
        time_basis={"observations": n, "basis": "log-return series"},
    )
    return {"historical": historical, "parametric_normal": parametric}


# --- Factor shares (grouping, not regression) ------------------------------------------------


def compute_factor_shares(allocations: list[dict],
                          market_classes: dict[str, str]) -> MetricResult:
    citation = (
        "market-class weight grouping (grouping, not regression) —"
        f" regression-based factors are future-band ({_SPECREF})"
    )
    if not allocations:
        return insufficient_result("factor_shares", "market-class grouping",
                                   citation, {"allocations": 1},
                                   {"allocations": 0})
    shares: dict[str, float] = {}
    unknown_ids: list[str] = []
    for a in allocations:
        cls = market_classes.get(a["instrument_id"])
        if cls is None:
            cls = "unknown"
            unknown_ids.append(a["instrument_id"])
        shares[cls] = shares.get(cls, 0.0) + float(a["weight"])
    return MetricResult(
        metric="factor_shares", method="market-class grouping",
        method_citation=citation,
        inputs={"allocation_count": len(allocations)},
        value={"shares": shares},
        uncertainty={"basis": "deterministic"},
        limitations={"scope": "grouping, not regression",
                     **({"unknown_instruments": unknown_ids}
                        if unknown_ids else {})},
        time_basis={"basis": "allocation-declaration"},
    )
