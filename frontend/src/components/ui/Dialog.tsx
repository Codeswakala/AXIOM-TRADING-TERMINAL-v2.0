/**
 * AXIOM Institutional UI Component — Dialog (UI-009-P05)
 *
 * Accessible modal overlay primitive with focus trap, backdrop dismissal,
 * keyboard escape support, ARIA attributes, and size variants.
 *
 * Invariant: Pure token consumption via var(--ix-*); zero ad-hoc hex.
 */

import {
  useEffect,
  useId,
  useRef,
  type KeyboardEvent,
  type MouseEvent,
  type ReactNode,
} from "react";
import "./Dialog.css";

export type DialogSize = "sm" | "md" | "lg" | "full";

export interface DialogProps {
  open: boolean;
  onClose?: () => void;
  title: ReactNode;
  description?: ReactNode;
  children: ReactNode;
  footer?: ReactNode;
  size?: DialogSize;
  backdropClose?: boolean;
  className?: string;
  id?: string;
  initialFocusRef?: { current: HTMLElement | null };
  finalFocusRef?: { current: HTMLElement | null };
}

export function Dialog({
  open,
  onClose,
  title,
  description,
  children,
  footer,
  size = "md",
  backdropClose = true,
  className = "",
  id: customId,
  initialFocusRef,
  finalFocusRef,
}: DialogProps) {
  const generatedId = useId();
  const dialogId = customId || `ix-dialog-${generatedId.replace(/:/g, "")}`;
  const titleId = `${dialogId}-title`;
  const descId = `${dialogId}-desc`;

  const dialogRef = useRef<HTMLDivElement>(null);
  const previouslyFocusedElementRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (open) {
      previouslyFocusedElementRef.current = document.activeElement as HTMLElement | null;

      // Focus initial focus target or first focusable element
      if (initialFocusRef?.current) {
        initialFocusRef.current.focus();
      } else {
        const focusable = dialogRef.current?.querySelectorAll<HTMLElement>(
          'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"]):not([disabled])',
        );
        if (focusable && focusable.length > 0) {
          focusable[0]?.focus();
        } else {
          dialogRef.current?.focus();
        }
      }
    } else {
      if (finalFocusRef?.current && document.contains(finalFocusRef.current)) {
        finalFocusRef.current.focus();
      } else if (previouslyFocusedElementRef.current && document.contains(previouslyFocusedElementRef.current)) {
        previouslyFocusedElementRef.current.focus();
      }
      previouslyFocusedElementRef.current = null;
    }
  }, [open, initialFocusRef, finalFocusRef]);

  // Focus trap and Escape key listener
  const handleKeyDown = (e: KeyboardEvent<HTMLDivElement>) => {
    if (e.key === "Escape" && onClose) {
      e.preventDefault();
      e.stopPropagation();
      onClose();
      return;
    }

    if (e.key === "Tab" && dialogRef.current) {
      const focusables = dialogRef.current.querySelectorAll<HTMLElement>(
        'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"]):not([disabled])',
      );
      if (focusables.length === 0) {
        e.preventDefault();
        return;
      }

      const firstElement = focusables[0];
      const lastElement = focusables[focusables.length - 1];

      if (e.shiftKey) {
        if (document.activeElement === firstElement || document.activeElement === dialogRef.current) {
          e.preventDefault();
          lastElement?.focus();
        }
      } else {
        if (document.activeElement === lastElement) {
          e.preventDefault();
          firstElement?.focus();
        }
      }
    }
  };

  const handleBackdropClick = (e: MouseEvent<HTMLDivElement>) => {
    if (e.target === e.currentTarget && backdropClose && onClose) {
      onClose();
    }
  };

  if (!open) return null;

  return (
    <div
      className="ix-dialog-overlay"
      onClick={handleBackdropClick}
      data-testid="dialog-backdrop"
    >
      <div
        ref={dialogRef}
        id={dialogId}
        role="dialog"
        aria-modal="true"
        aria-labelledby={titleId}
        aria-describedby={description ? descId : undefined}
        tabIndex={-1}
        className={`ix-dialog ix-dialog--${size} ${className}`}
        data-ui009-component="dialog"
        data-size={size}
        data-open={open}
        onKeyDown={handleKeyDown}
        data-testid="dialog-container"
      >
        <div className="ix-dialog__header" data-testid="dialog-header">
          <div className="ix-dialog__titles">
            <h2 id={titleId} className="ix-dialog__title" data-testid="dialog-title">
              {title}
            </h2>
            {description && (
              <p id={descId} className="ix-dialog__description" data-testid="dialog-description">
                {description}
              </p>
            )}
          </div>
          {onClose && (
            <button
              type="button"
              className="ix-dialog__close-btn"
              onClick={onClose}
              aria-label="Close dialog"
              data-testid="dialog-close-button"
            >
              {"\u{2715}"}
            </button>
          )}
        </div>

        <div className="ix-dialog__body" data-testid="dialog-body">
          {children}
        </div>

        {footer && (
          <div className="ix-dialog__footer" data-testid="dialog-footer">
            {footer}
          </div>
        )}
      </div>
    </div>
  );
}
