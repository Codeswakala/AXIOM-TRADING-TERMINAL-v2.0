/**
 * AXIOM Institutional UI Component — Collapsible (UI-009-P03)
 *
 * Reusable collapsible section component.
 * Features:
 * - ARIA: aria-expanded, aria-controls, aria-labelledby
 * - Keyboard: Enter / Space triggers toggling
 * - Animation: var(--ix-motion-fast) with prefers-reduced-motion override
 * - Controlled and uncontrolled modes
 *
 * Invariant: Pure token consumption via var(--ix-*); zero ad-hoc hex.
 */

import {
  forwardRef,
  useId,
  useState,
  type HTMLAttributes,
  type KeyboardEvent,
  type ReactNode,
} from "react";
import "./Collapsible.css";

export interface CollapsibleProps extends Omit<HTMLAttributes<HTMLDivElement>, "title" | "onToggle"> {
  title: ReactNode;
  children: ReactNode;
  defaultExpanded?: boolean;
  expanded?: boolean;
  onToggle?: (expanded: boolean) => void;
  icon?: ReactNode;
  disabled?: boolean;
  className?: string;
}

export const Collapsible = forwardRef<HTMLDivElement, CollapsibleProps>(
  (
    {
      title,
      children,
      defaultExpanded = false,
      expanded: controlledExpanded,
      onToggle,
      icon,
      disabled = false,
      className = "",
      id: customId,
      ...rest
    },
    ref,
  ) => {
    const generatedId = useId();
    const baseId = customId || `ix-collapsible-${generatedId.replace(/:/g, "")}`;
    const triggerId = `${baseId}-trigger`;
    const contentId = `${baseId}-content`;

    const [uncontrolledExpanded, setUncontrolledExpanded] = useState(defaultExpanded);
    const isControlled = typeof controlledExpanded === "boolean";
    const isExpanded = isControlled ? controlledExpanded : uncontrolledExpanded;

    const handleToggle = () => {
      if (disabled) return;
      const nextExpanded = !isExpanded;
      if (!isControlled) {
        setUncontrolledExpanded(nextExpanded);
      }
      onToggle?.(nextExpanded);
    };

    const handleKeyDown = (e: KeyboardEvent<HTMLButtonElement>) => {
      if (disabled) return;
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        handleToggle();
      }
    };

    return (
      <div
        ref={ref}
        id={baseId}
        className={`ix-collapsible ${isExpanded ? "ix-collapsible--expanded" : ""} ${
          disabled ? "ix-collapsible--disabled" : ""
        } ${className}`}
        data-ui009-component="collapsible"
        data-expanded={isExpanded}
        data-disabled={disabled}
        {...rest}
      >
        <h3 className="ix-collapsible__heading">
          <button
            type="button"
            id={triggerId}
            className="ix-collapsible__trigger"
            aria-expanded={isExpanded}
            aria-controls={contentId}
            disabled={disabled}
            onClick={handleToggle}
            onKeyDown={handleKeyDown}
            data-testid="collapsible-trigger"
          >
            <span className="ix-collapsible__trigger-left">
              {icon && (
                <span className="ix-collapsible__icon" aria-hidden="true" data-testid="collapsible-icon">
                  {icon}
                </span>
              )}
              <span className="ix-collapsible__title">{title}</span>
            </span>
            <span className="ix-collapsible__caret" aria-hidden="true" data-testid="collapsible-caret">
              {isExpanded ? "\u{25B4}" : "\u{25BE}"}
            </span>
          </button>
        </h3>

        {isExpanded && (
          <div
            id={contentId}
            role="region"
            aria-labelledby={triggerId}
            className="ix-collapsible__content"
            data-testid="collapsible-content"
          >
            {children}
          </div>
        )}
      </div>
    );
  },
);

Collapsible.displayName = "Collapsible";
