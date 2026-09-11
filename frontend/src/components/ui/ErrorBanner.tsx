/**
 * AXIOM Institutional UI Component — ErrorBanner (UI-009-P05)
 *
 * Inline error and recovery notification banner primitive.
 * Enforces multi-modal status encoding (symbol + text + semantic token border).
 *
 * Invariant: Pure token consumption via var(--ix-*); zero ad-hoc hex.
 */

import { forwardRef, type HTMLAttributes } from "react";
import { Button } from "./Button";
import "./ErrorBanner.css";

export type ErrorBannerVariant = "error" | "warning";

export interface ErrorBannerAction {
  label: string;
  onClick: () => void;
}

export interface ErrorBannerProps extends HTMLAttributes<HTMLDivElement> {
  title: string;
  message: string;
  variant?: ErrorBannerVariant;
  action?: ErrorBannerAction;
  onDismiss?: () => void;
  className?: string;
}

export const ErrorBanner = forwardRef<HTMLDivElement, ErrorBannerProps>(
  (
    {
      title,
      message,
      variant = "error",
      action,
      onDismiss,
      className = "",
      ...rest
    },
    ref,
  ) => {
    const symbol = variant === "warning" ? "⚠" : "✕";

    return (
      <div
        ref={ref}
        role="alert"
        aria-live="assertive"
        className={`ix-error-banner ix-error-banner--${variant} ${className}`}
        data-ui009-component="error-banner"
        data-variant={variant}
        data-testid="error-banner"
        {...rest}
      >
        <div className="ix-error-banner__icon" aria-hidden="true" data-testid="error-banner-icon">
          {symbol}
        </div>

        <div className="ix-error-banner__content">
          <div className="ix-error-banner__header">
            <span className="ix-error-banner__badge">{variant.toUpperCase()}</span>
            <strong className="ix-error-banner__title" data-testid="error-banner-title">
              {title}
            </strong>
          </div>
          <p className="ix-error-banner__message" data-testid="error-banner-message">
            {message}
          </p>
        </div>

        {action && (
          <div className="ix-error-banner__action" data-testid="error-banner-action">
            <Button
              size="sm"
              variant={variant === "warning" ? "secondary" : "ghost"}
              onClick={action.onClick}
            >
              {action.label}
            </Button>
          </div>
        )}

        {onDismiss && (
          <button
            type="button"
            className="ix-error-banner__close-btn"
            onClick={onDismiss}
            aria-label="Dismiss notification"
            data-testid="error-banner-close-btn"
          >
            {"\u{2715}"}
          </button>
        )}
      </div>
    );
  },
);

ErrorBanner.displayName = "ErrorBanner";
