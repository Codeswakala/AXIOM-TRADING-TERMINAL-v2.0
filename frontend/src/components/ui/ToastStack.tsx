/**
 * AXIOM Institutional UI Component — ToastStack (UI-009-P05)
 *
 * Container rendering a stack of active toast notifications with accessibility regions.
 *
 * Invariant: Pure token consumption via var(--ix-*); zero ad-hoc hex.
 */

import { Toast, type ToastProps } from "./Toast";
import "./Toast.css";

export interface ToastStackProps {
  toasts: ToastProps[];
  onDismiss?: (id: string) => void;
  className?: string;
}

export function ToastStack({
  toasts,
  onDismiss,
  className = "",
}: ToastStackProps) {
  if (toasts.length === 0) return null;

  return (
    <div
      role="region"
      aria-label="Notifications"
      className={`ix-toast-stack ${className}`}
      data-ui009-component="toast-stack"
    >
      {toasts.map((toast, index) => {
        const toastId = toast.id || `toast-${index}`;
        return (
          <Toast
            key={toastId}
            {...toast}
            id={toastId}
            onDismiss={() => {
              toast.onDismiss?.();
              onDismiss?.(toastId);
            }}
          />
        );
      })}
    </div>
  );
}
