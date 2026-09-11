import "./TerminalMultiPane.css";

export interface UncertaintyInterval {
  lower?: number | null;
  upper?: number | null;
  method?: string | null;
  confidence_level?: number | null;
  [key: string]: unknown;
}

export interface CalibratedConfidenceBadgeProps {
  confidence: number | null | undefined;
  uncertainty?: UncertaintyInterval | null;
  className?: string;
  testId?: string;
}

export interface MetricWithIntervalProps {
  label: string;
  value: number | null | undefined;
  uncertainty?: UncertaintyInterval | null;
  isPercentage?: boolean;
  precision?: number;
  className?: string;
  testId?: string;
}

/**
 * CalibratedConfidenceBadge
 *
 * Single Canonical Component for rendering Calibrated Confidence across the platform (B-CONV2-1).
 * Strictly enforces point-estimate bracketing (lower <= confidence <= upper) per CA-P04-5
 * and renders explicit [Uncertainty: Unavailable] when bounds are absent or invalid.
 */
export function CalibratedConfidenceBadge({
  confidence,
  uncertainty,
  className = "",
  testId,
}: CalibratedConfidenceBadgeProps) {
  if (confidence === null || confidence === undefined || isNaN(confidence)) {
    return (
      <span className={`metric-value-uncertainty mono ${className}`} data-testid={testId}>
        Unavailable · [Uncertainty: Unavailable]
      </span>
    );
  }

  const confVal = confidence > 1 ? confidence / 100 : confidence;
  const confPct = `${(confVal * 100).toFixed(1)}%`;

  const low = uncertainty?.lower != null ? Number(uncertainty.lower) : null;
  const up = uncertainty?.upper != null ? Number(uncertainty.upper) : null;

  const normLow = low !== null ? (low > 1 ? low / 100 : low) : null;
  const normUp = up !== null ? (up > 1 ? up / 100 : up) : null;

  // CA-P04-5: Strict bracketing validation
  const isBracketed =
    normLow !== null &&
    normUp !== null &&
    normLow <= confVal &&
    confVal <= normUp;

  let text: string;
  if (isBracketed && normLow !== null && normUp !== null) {
    const lowPct = `${(normLow * 100).toFixed(1)}%`;
    const upPct = `${(normUp * 100).toFixed(1)}%`;
    const method = uncertainty?.method ? uncertainty.method.replace(/_/g, " ") : "Wilson";
    const methodLabel = method.toLowerCase().includes("wilson") ? "Wilson" : "CI";
    text = `${confPct} · ${methodLabel}: [${lowPct} – ${upPct}]`;
  } else {
    text = `${confPct} · [Uncertainty: Unavailable]`;
  }

  return (
    <span
      className={`metric-value-uncertainty mono font-bold ${className}`}
      data-testid={testId}
      title={isBracketed ? "Statistically validated confidence interval" : "Uncertainty interval unavailable"}
    >
      {text}
    </span>
  );
}

/**
 * MetricWithInterval
 *
 * Single Canonical Component for rendering server-evaluated statistical risk metrics,
 * drawdowns, volatility, and stress losses with uncertainty intervals (B-CONV2-1 / B-P05-2).
 */
export function MetricWithInterval({
  label,
  value,
  uncertainty,
  isPercentage = true,
  precision = 1,
  className = "",
  testId,
}: MetricWithIntervalProps) {
  if (value === null || value === undefined || isNaN(value)) {
    return (
      <div className={`risk-metric-box ${className}`} data-testid={testId}>
        <span className="box-lbl">{label}</span>
        <span className="box-val mono font-bold" data-testid={testId ? `${testId}-val` : undefined}>
          Unavailable
        </span>
        <span className="box-unc mono" data-testid={testId ? `${testId}-unc` : undefined}>
          [Uncertainty: Unavailable]
        </span>
      </div>
    );
  }

  const absVal = Math.abs(value);
  const valText = isPercentage
    ? `${(value * 100).toFixed(precision)}%`
    : value.toFixed(precision === 1 ? 4 : precision);

  const low = uncertainty?.lower != null ? Number(uncertainty.lower) : null;
  const up = uncertainty?.upper != null ? Number(uncertainty.upper) : null;

  // CA-P04-5 & B-P05-2: Interval is valid only if lower <= value <= upper (or absolute values if signed)
  const isBracketed =
    low !== null &&
    up !== null &&
    ((low <= value && value <= up) || (low <= absVal && absVal <= up));

  let uncText = "[Uncertainty: Unavailable]";
  if (isBracketed && low !== null && up !== null) {
    const lowText = isPercentage ? `${(low * 100).toFixed(precision)}%` : low.toFixed(2);
    const upText = isPercentage ? `${(up * 100).toFixed(precision)}%` : up.toFixed(2);
    uncText = `CI: [${lowText} – ${upText}]`;
  }

  return (
    <div className={`risk-metric-box ${className}`} data-testid={testId}>
      <span className="box-lbl">{label}</span>
      <span className="box-val mono font-bold" data-testid={testId ? `${testId}-val` : undefined}>
        {valText}
      </span>
      <span
        className={`box-unc mono ${!isBracketed ? "warning" : ""}`}
        data-testid={testId ? `${testId}-unc` : undefined}
      >
        {uncText}
      </span>
    </div>
  );
}
