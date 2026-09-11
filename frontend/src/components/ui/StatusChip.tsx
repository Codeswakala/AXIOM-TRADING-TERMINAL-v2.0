/**
 * AXIOM Atomic Component — StatusChip (UI-009-P02)
 *
 * Discrete confidence/status indicator reusing the UncertaintyBadge pattern.
 * Levels: HIGH, MODERATE, LIMITED, UNCALIBRATED.
 * Invariant: Never communicates confidence by color alone (renders text + diamonds + %).
 */

import "./StatusChip.css";

export type StatusChipLevel = "HIGH" | "MODERATE" | "LIMITED" | "UNCALIBRATED";

export interface StatusChipProps {
  level: StatusChipLevel;
  value?: string | number | null;
  label?: string;
  className?: string;
}

export function StatusChip({
  level,
  value,
  label,
  className = "",
}: StatusChipProps) {
  const iconMap: Record<StatusChipLevel, string> = {
    HIGH: "\u{25C6}\u{25C6}\u{25C6}",
    MODERATE: "\u{25C6}\u{25C6}\u{25C7}",
    LIMITED: "\u{25C6}\u{25C7}\u{25C7}",
    UNCALIBRATED: "\u{25C7}\u{25C7}\u{25C7}",
  };

  const formattedValue =
    typeof value === "number" ? `${(value * 100).toFixed(1)}%` : value ? String(value) : null;

  return (
    <span
      className={`ix-status-chip ix-status-chip--${level.toLowerCase()} ${className}`}
      data-ui009-component="status-chip"
      data-level={level}
      role="status"
      aria-label={`Status: ${level}${formattedValue ? `, ${formattedValue}` : ""}`}
    >
      <span className="ix-status-chip__icon" aria-hidden="true">
        {iconMap[level]}
      </span>
      <span className="ix-status-chip__level">{label ?? level}</span>
      {formattedValue && (
        <span className="ix-status-chip__value mono">({formattedValue})</span>
      )}
    </span>
  );
}
