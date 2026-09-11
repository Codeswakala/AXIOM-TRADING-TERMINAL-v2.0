/**
 * AXIOM Atomic Component — Badge (UI-009-P02)
 *
 * Scoped badge primitive with semantic color roles and mandatory text labels.
 * Invariant: Never communicates status by color alone (always renders text/icon).
 */

import type { ReactNode } from "react";
import "./Badge.css";

export type BadgeVariant = "neutral" | "info" | "success" | "warning" | "critical" | "accent";
export type BadgeSize = "sm" | "md";

export interface BadgeProps {
  label?: string;
  children?: ReactNode;
  variant?: BadgeVariant;
  size?: BadgeSize;
  icon?: ReactNode;
  className?: string;
}

export function Badge({
  label,
  children,
  variant = "neutral",
  size = "md",
  icon,
  className = "",
}: BadgeProps) {
  const displayText = label ?? (typeof children === "string" ? children : undefined);

  return (
    <span
      className={`ix-badge ix-badge--${variant} ix-badge--${size} ${className}`}
      data-ui009-component="badge"
      data-variant={variant}
      data-size={size}
    >
      {icon && <span className="ix-badge__icon" aria-hidden="true">{icon}</span>}
      <span className="ix-badge__label">{displayText ?? children}</span>
    </span>
  );
}
