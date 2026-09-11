/**
 * AXIOM Institutional UI Component — EmptyState (UI-010-P03)
 *
 * Accessible, honest empty state primitive.
 * Displays title (<h3>), optional description, icon, and recovery action.
 * Communicates honest state with role="status" and aria-live="polite".
 *
 * Invariant: Pure token consumption via var(--ix-*); zero ad-hoc hex.
 */

import { forwardRef, type HTMLAttributes, type ReactNode } from "react";
import { Button, type ButtonVariant } from "./Button";
import "./EmptyState.css";

export type EmptyStateVariant = "default" | "compact";

export interface EmptyStateAction {
  label: string;
  onClick: () => void;
  disabled?: boolean;
  variant?: ButtonVariant;
}

export interface EmptyStateProps extends Omit<HTMLAttributes<HTMLDivElement>, "title"> {
  title: string;
  description?: string;
  icon?: ReactNode;
  action?: EmptyStateAction;
  variant?: EmptyStateVariant;
  className?: string;
}

export const EmptyState = forwardRef<HTMLDivElement, EmptyStateProps>(
  (
    {
      title,
      description,
      icon,
      action,
      variant = "default",
      className = "",
      ...rest
    },
    ref,
  ) => {
    const ariaLabel = rest["aria-label"] || title || "Empty state";

    return (
      <div
        ref={ref}
        role="status"
        aria-live="polite"
        aria-label={ariaLabel}
        className={`ix-empty-state ix-empty-state--${variant} ${className}`}
        data-ui010-component="empty-state"
        data-variant={variant}
        data-testid="empty-state"
        {...rest}
      >
        {icon && (
          <div className="ix-empty-state__icon" aria-hidden="true" data-testid="empty-state-icon">
            {icon}
          </div>
        )}

        <div className="ix-empty-state__content">
          <h3 className="ix-empty-state__title" data-testid="empty-state-title">
            {title}
          </h3>
          {description && (
            <p className="ix-empty-state__description" data-testid="empty-state-description">
              {description}
            </p>
          )}
        </div>

        {action && (
          <div className="ix-empty-state__action" data-testid="empty-state-action">
            <Button
              size={variant === "compact" ? "sm" : "md"}
              variant={action.variant || "secondary"}
              onClick={action.onClick}
              disabled={action.disabled}
            >
              {action.label}
            </Button>
          </div>
        )}
      </div>
    );
  },
);

EmptyState.displayName = "EmptyState";
