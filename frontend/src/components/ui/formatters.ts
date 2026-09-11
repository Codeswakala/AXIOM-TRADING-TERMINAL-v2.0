/**
 * AXIOM Institutional Design System — Uncertainty & Numeric Formatters (UI-009-P04)
 *
 * Pure, deterministic statistical and numeric formatting helpers for data tables and metrics.
 * Non-actuating, presentation-only.
 */

export interface UncertaintyIntervalParams {
  lower: number;
  upper: number;
  confidence?: number;
  decimals?: number;
}

/**
 * Formats a bounded uncertainty confidence interval.
 * Example: formatUncertaintyInterval({ lower: -0.15, upper: 0.22, confidence: 0.95 }) -> "95% CI [-0.15, +0.22]"
 */
export function formatUncertaintyInterval({
  lower,
  upper,
  confidence = 0.95,
  decimals = 2,
}: UncertaintyIntervalParams): string {
  if (typeof lower !== "number" || typeof upper !== "number" || isNaN(lower) || isNaN(upper)) {
    return "CI [—, —]";
  }

  const confPct = Math.round(confidence * 100);
  const formatVal = (val: number) => {
    const fixed = val.toFixed(decimals);
    return val > 0 ? `+${fixed}` : fixed;
  };

  if (lower === upper) {
    return `${confPct}% CI [${formatVal(lower)}]`;
  }

  return `${confPct}% CI [${formatVal(lower)}, ${formatVal(upper)}]`;
}

/**
 * Formats sample count descriptor.
 * Example: formatSampleCount(120) -> "n=120"
 */
export function formatSampleCount(n: number): string {
  if (typeof n !== "number" || isNaN(n) || n < 0) {
    return "n=0";
  }
  return `n=${Math.round(n)}`;
}

/**
 * Formats Pearson correlation coefficient.
 * Example: formatPearsonR(0.73) -> "r=0.73"
 */
export function formatPearsonR(r: number, decimals = 2): string {
  if (typeof r !== "number" || isNaN(r)) {
    return "r=—";
  }
  const clamped = Math.max(-1, Math.min(1, r));
  const fixed = clamped.toFixed(decimals);
  return `r=${fixed}`;
}

/**
 * Formats pips difference for currency / forex metrics.
 * Example: formatPips(14.2) -> "+14.2 pips"
 */
export function formatPips(value: number, decimals = 1): string {
  if (typeof value !== "number" || isNaN(value)) {
    return "— pips";
  }
  const prefix = value > 0 ? "+" : "";
  return `${prefix}${value.toFixed(decimals)} pips`;
}

/**
 * Formats percentage value.
 * Example: formatPercent(12.5) -> "12.5%"
 */
export function formatPercent(value: number, decimals = 1): string {
  if (typeof value !== "number" || isNaN(value)) {
    return "—%";
  }
  return `${value.toFixed(decimals)}%`;
}
