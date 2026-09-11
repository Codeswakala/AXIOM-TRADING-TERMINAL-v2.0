/**
 * AXIOM Institutional UI Component — Toast (UI-009-P05)
 *
 * Accessible feedback notification primitive.
 * Enforces multi-modal status encoding (symbol + text label + token color).
 *
 * Invariant: Pure token consumption via var(--ix-*); zero ad-hoc hex.
 */

import {
  useEffect,
  type KeyboardEvent,
  type ReactNode,
} from "react";
import "./Toast.css";

export type ToastVariant = "info" | "success" | "warning" | "error";

export interface ToastProps {
  id?: string;
  variant: ToastVariant;
  title: string;
  description?: string;
  icon?: ReactNode;
  onDismiss?: () => void;
  autoDismissMs?: number;
  className?: string;
}

const DEFAULT_SYMBOLS: Record<ToastVariant, string> = {
  info: "ℹ",
  success: "✓",
  warning: "⚠",
  error: "✕",
};

export function Toast({
  id,
  variant = "info",
  title,
  description,
  icon,
  onDismiss,
  autoDismissMs,
  className = "",
}: ToastProps) {
  useEffect(() => {
    if (!autoDismissMs || autoDismissMs <= 0 || !onDismiss) return;

    const timer = setTimeout(() => {
      onDismiss();
    }, autoDismissMs);

    return () => clearTimeout(timer);
  }, [autoDismissMs, onDismiss]);

  const handleKeyDown = (e: KeyboardEvent<HTMLDivElement>) => {
    if (e.key === "Escape" && onDismiss) {
      e.preventDefault();
      onDismiss();
    }
  };

  const isAlert = variant === "warning" || variant === "error";
  const role = isAlert ? "alert" : "status";
  const ariaLive = isAlert ? "assertive" : "polite";

  const displayIcon = icon ?? DEFAULT_SYMBOLS[variant];

  return (
    <div
      id={id}
      role={role}
      aria-live={ariaLive}
      aria-atomic="true"
      tabIndex={0}
      onKeyDown={handleKeyDown}
      className={`ix-toast ix-toast--${variant} ${className}`}
      data-ui009-component="toast"
      data-variant={variant}
      data-testid="toast-container"
    >
      <div className="ix-toast__symbol" aria-hidden="true" data-testid="toast-symbol">
        {displayIcon}
      </div>

      <div className="ix-toast__content">
        <div className="ix-toast__header">
          <span className="ix-toast__badge">{variant.toUpperCase()}</span>
          <strong className="ix-toast__title" data-testid="toast-title">
            {title}
          </strong>
        </div>
        {description && (
          <p className="ix-toast__description" data-testid="toast-description">
            {description}
          </p>
        )}
      </div>

      {onDismiss && (
        <button
          type="button"
          className="ix-toast__close-btn"
          onClick={onDismiss}
          aria-label="Dismiss notification"
          data-testid="toast-close-button"
        >
          {"\u{2715}"}
        </button>
      )}
    </div>
  );
}
