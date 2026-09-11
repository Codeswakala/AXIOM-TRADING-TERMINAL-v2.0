/**
 * AXIOM Atomic Component — Input (UI-009-P02)
 *
 * Scoped, accessible form input primitive.
 * Supports: text, search, number, password, email.
 * States: default, focus, disabled, error, loading.
 * ARIA: aria-invalid, aria-describedby linking error and helper text.
 */

import { forwardRef, type InputHTMLAttributes, type ReactNode } from "react";
import "./Input.css";

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  helperText?: string;
  error?: string | null;
  leadingIcon?: ReactNode;
  trailingIcon?: ReactNode;
  loading?: boolean;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  (
    {
      label,
      helperText,
      error,
      leadingIcon,
      trailingIcon,
      loading = false,
      disabled = false,
      id,
      className = "",
      type = "text",
      ...rest
    },
    ref,
  ) => {
    const inputId = id ?? (label ? `ix-input-${label.toLowerCase().replace(/\s+/g, "-")}` : undefined);
    const helperId = inputId ? `${inputId}-helper` : undefined;
    const errorId = inputId ? `${inputId}-error` : undefined;

    const describedBy = [error ? errorId : null, helperText ? helperId : null]
      .filter(Boolean)
      .join(" ") || undefined;

    return (
      <div
        className={`ix-input-wrapper ${error ? "ix-input-wrapper--error" : ""} ${disabled ? "ix-input-wrapper--disabled" : ""}`}
        data-ui009-component="input"
      >
        {label && (
          <label htmlFor={inputId} className="ix-input-label">
            {label}
          </label>
        )}

        <div className="ix-input-box">
          {leadingIcon && (
            <span className="ix-input-icon ix-input-icon--leading" aria-hidden="true">
              {leadingIcon}
            </span>
          )}

          <input
            ref={ref}
            id={inputId}
            type={type}
            className={`ix-input ${className}`}
            disabled={disabled || loading}
            aria-invalid={Boolean(error)}
            aria-describedby={describedBy}
            data-testid="ui-input"
            {...rest}
          />

          {loading && (
            <span className="ix-input-spinner" aria-hidden="true" data-testid="input-spinner">
              {"\u{25CB}"}
            </span>
          )}

          {!loading && trailingIcon && (
            <span className="ix-input-icon ix-input-icon--trailing" aria-hidden="true">
              {trailingIcon}
            </span>
          )}
        </div>

        {error && (
          <p id={errorId} className="ix-input-error" role="alert" data-testid="input-error-msg">
            {error}
          </p>
        )}

        {!error && helperText && (
          <p id={helperId} className="ix-input-helper" data-testid="input-helper-msg">
            {helperText}
          </p>
        )}
      </div>
    );
  },
);

Input.displayName = "Input";
