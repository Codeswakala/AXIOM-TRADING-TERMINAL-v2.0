/**
 * AXIOM Atomic Component — Button (UI-009-P02)
 *
 * Scoped, accessible button primitive consuming 5-tier design tokens.
 * Variants: primary, secondary, ghost, destructive (danger).
 * Sizes: sm, md, lg.
 * States: default, hover, focus, active, disabled, loading.
 *
 * Invariant: 100% tokenized via var(--ix-*); zero ad-hoc hex.
 */

import { forwardRef, type ButtonHTMLAttributes, type ReactNode } from "react";
import "./Button.css";

export type ButtonVariant = "primary" | "secondary" | "ghost" | "destructive";
export type ButtonSize = "sm" | "md" | "lg";

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  loading?: boolean;
  icon?: ReactNode;
  iconPosition?: "left" | "right";
  children?: ReactNode;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = "primary",
      size = "md",
      loading = false,
      disabled = false,
      icon,
      iconPosition = "left",
      children,
      className = "",
      type = "button",
      ...rest
    },
    ref,
  ) => {
    const isEffectivelyDisabled = disabled || loading;

    return (
      <button
        ref={ref}
        type={type}
        className={`ix-button ix-button--${variant} ix-button--${size} ${loading ? "ix-button--loading" : ""} ${className}`}
        disabled={isEffectivelyDisabled}
        aria-busy={loading}
        data-ui009-component="button"
        data-variant={variant}
        data-size={size}
        {...rest}
      >
        {loading && (
          <span className="ix-button__spinner" aria-hidden="true" data-testid="button-spinner">
            {"\u{25CB}"}
          </span>
        )}
        {!loading && icon && iconPosition === "left" && (
          <span className="ix-button__icon ix-button__icon--left" aria-hidden="true">
            {icon}
          </span>
        )}
        {children && <span className="ix-button__text">{children}</span>}
        {!loading && icon && iconPosition === "right" && (
          <span className="ix-button__icon ix-button__icon--right" aria-hidden="true">
            {icon}
          </span>
        )}
      </button>
    );
  },
);

Button.displayName = "Button";
