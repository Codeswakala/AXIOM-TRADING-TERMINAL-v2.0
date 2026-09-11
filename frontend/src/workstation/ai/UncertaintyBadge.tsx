/**
 * UncertaintyBadge Component (UI-008-P04)
 *
 * Renders calibrated confidence levels, uncertainty intervals, and sample counts.
 * Invariant: Never communicates confidence via color alone (includes explicit text).
 */

export type ConfidenceLevel = "HIGH" | "MODERATE" | "LIMITED" | "UNCALIBRATED";

export interface UncertaintyBadgeProps {
  confidenceLevel?: ConfidenceLevel;
  calibratedConfidence?: number | null;
  interval?: { lower: number; upper: number; confidenceLevel?: number } | null;
  sampleCount?: number | null;
  statusLabel?: string | null;
}

export function computeConfidenceLevel(
  calibratedConfidence?: number | null,
  sampleCount?: number | null,
): ConfidenceLevel {
  if (calibratedConfidence == null) return "UNCALIBRATED";
  if (sampleCount != null && sampleCount < 10) return "LIMITED";
  if (calibratedConfidence >= 0.75) return "HIGH";
  if (calibratedConfidence >= 0.5) return "MODERATE";
  return "LIMITED";
}

export function UncertaintyBadge({
  confidenceLevel,
  calibratedConfidence,
  interval,
  sampleCount,
  statusLabel,
}: UncertaintyBadgeProps) {
  const level =
    confidenceLevel ?? computeConfidenceLevel(calibratedConfidence, sampleCount);

  const levelClassMap: Record<ConfidenceLevel, string> = {
    HIGH: "ix-confidence--high",
    MODERATE: "ix-confidence--moderate",
    LIMITED: "ix-confidence--limited",
    UNCALIBRATED: "ix-confidence--uncalibrated",
  };

  const levelIconMap: Record<ConfidenceLevel, string> = {
    HIGH: "\u{25C6}\u{25C6}\u{25C6}", // 3 diamonds
    MODERATE: "\u{25C6}\u{25C6}\u{25C7}", // 2 diamonds
    LIMITED: "\u{25C6}\u{25C7}\u{25C7}", // 1 diamond
    UNCALIBRATED: "\u{25C7}\u{25C7}\u{25C7}", // 0 diamonds
  };

  const confidencePercent =
    calibratedConfidence != null ? `${(calibratedConfidence * 100).toFixed(1)}%` : null;

  return (
    <div
      className={`ix-uncertainty-badge ${levelClassMap[level]}`}
      data-testid="uncertainty-badge"
      data-ui008-confidence-level={level}
      role="group"
      aria-label={`Uncertainty and confidence: ${level}`}
    >
      <div className="ix-uncertainty-badge__level">
        <span className="ix-confidence-icon" aria-hidden="true">
          {levelIconMap[level]}
        </span>
        <span className="ix-confidence-label" data-testid="confidence-level-text">
          {level} CONFIDENCE
        </span>
        {confidencePercent && (
          <span className="ix-confidence-pct mono" data-testid="confidence-percent">
            ({confidencePercent} calibrated)
          </span>
        )}
      </div>

      {interval && (
        <div className="ix-uncertainty-badge__interval mono" data-testid="uncertainty-interval">
          <span>
            {interval.confidenceLevel ? `${(interval.confidenceLevel * 100).toFixed(0)}% CI: ` : "Interval: "}
            [{interval.lower >= 0 ? `+${interval.lower.toFixed(2)}` : interval.lower.toFixed(2)},{" "}
            {interval.upper >= 0 ? `+${interval.upper.toFixed(2)}` : interval.upper.toFixed(2)}]
          </span>
        </div>
      )}

      {sampleCount != null && (
        <div className="ix-uncertainty-badge__samples mono" data-testid="sample-count">
          <span>n={sampleCount}</span>
        </div>
      )}

      {statusLabel && (
        <div className="ix-uncertainty-badge__status" data-testid="calibration-status">
          <span className="ix-status-text">{statusLabel}</span>
        </div>
      )}
    </div>
  );
}
