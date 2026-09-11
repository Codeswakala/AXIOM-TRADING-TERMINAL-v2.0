import "./TerminalMultiPane.css";

export interface TerminalGovernanceBadgeProps {
  compact?: boolean;
  className?: string;
}

/**
 * TerminalGovernanceBadge
 *
 * Compact, prominent, and strictly non-actuating governance indicator.
 * Displays: GATE: CLOSED · RESEARCH-ONLY · NON-ACTUATING
 *
 * Adheres to:
 * - T-1: Zero actuation
 * - Plan §J: Prominent Governance & Research status indicators
 * - SAL-2 (Internal) presentation surface
 */
export function TerminalGovernanceBadge({
  compact = false,
  className = "",
}: TerminalGovernanceBadgeProps) {
  return (
    <div
      className={`terminal-governance-badge ${compact ? "compact" : ""} ${className}`}
      role="status"
      aria-label="Governance Gate Status: Closed · Research-Only Non-Actuating"
      data-testid="terminal-governance-badge"
    >
      <span className="terminal-gov-gate" data-testid="terminal-gov-gate">
        <span className="terminal-gov-dot" aria-hidden="true" />
        GATE: CLOSED
      </span>
      <span className="terminal-gov-separator" aria-hidden="true">
        ·
      </span>
      <span className="terminal-gov-posture" data-testid="terminal-gov-posture">
        RESEARCH-ONLY · NON-ACTUATING
      </span>
    </div>
  );
}
