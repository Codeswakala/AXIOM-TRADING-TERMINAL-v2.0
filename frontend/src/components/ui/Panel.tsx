/**
 * AXIOM Institutional UI Component — Panel (UI-009-P03)
 *
 * Unified workspace panel frame primitive.
 * Supports header and actionBar slots, customizable padding,
 * collapsible states (accessible with ARIA), and visual variants.
 *
 * Invariant: Pure token consumption via var(--ix-*); zero ad-hoc hex.
 */

import { forwardRef, useId, useState, type HTMLAttributes, type ReactNode } from "react";
import "./Panel.css";

export type PanelVariant = "default" | "raised" | "ghost";
export type PanelPadding = "none" | "sm" | "md" | "lg";

export interface PanelProps extends HTMLAttributes<HTMLDivElement> {
  variant?: PanelVariant;
  padding?: PanelPadding;
  header?: ReactNode;
  actionBar?: ReactNode;
  footer?: ReactNode;
  collapsible?: boolean;
  defaultCollapsed?: boolean;
  collapsed?: boolean;
  onToggle?: (collapsed: boolean) => void;
  ariaLabelledBy?: string;
  children?: ReactNode;
  className?: string;
}

export const Panel = forwardRef<HTMLDivElement, PanelProps>(
  (
    {
      variant = "default",
      padding = "md",
      header,
      actionBar,
      footer,
      collapsible = false,
      defaultCollapsed = false,
      collapsed: controlledCollapsed,
      onToggle,
      ariaLabelledBy,
      children,
      className = "",
      id: customId,
      ...rest
    },
    ref,
  ) => {
    const generatedId = useId();
    const panelId = customId || `ix-panel-${generatedId.replace(/:/g, "")}`;
    const headerId = `${panelId}-header`;
    const bodyId = `${panelId}-body`;

    const [uncontrolledCollapsed, setUncontrolledCollapsed] = useState(defaultCollapsed);
    const isControlled = typeof controlledCollapsed === "boolean";
    const isCollapsed = isControlled ? controlledCollapsed : uncontrolledCollapsed;

    const handleToggle = () => {
      const nextCollapsed = !isCollapsed;
      if (!isControlled) {
        setUncontrolledCollapsed(nextCollapsed);
      }
      onToggle?.(nextCollapsed);
    };

    const hasAriaLabel = Boolean(rest["aria-label"]);
    const effectiveAriaLabelledBy = ariaLabelledBy || (!hasAriaLabel && header ? headerId : undefined);

    return (
      <div
        ref={ref}
        id={panelId}
        role="region"
        aria-labelledby={effectiveAriaLabelledBy}
        className={`ix-panel ix-panel--${variant} ix-panel--padding-${padding} ${
          isCollapsed ? "ix-panel--collapsed" : ""
        } ${className}`}
        data-ui009-component="panel"
        data-variant={variant}
        data-padding={padding}
        data-collapsed={isCollapsed}
        {...rest}
      >
        {(header || collapsible) && (
          <div className="ix-panel__header-container" id={headerId} data-testid="panel-header-container">
            <div className="ix-panel__header-content">{header}</div>
            {collapsible && (
              <button
                type="button"
                className="ix-panel__collapse-toggle"
                aria-expanded={!isCollapsed}
                aria-controls={bodyId}
                aria-label={isCollapsed ? "Expand panel" : "Collapse panel"}
                onClick={handleToggle}
                data-testid="panel-collapse-toggle"
              >
                <span className="ix-panel__collapse-caret" aria-hidden="true">
                  {isCollapsed ? "\u{25BE}" : "\u{25B4}"}
                </span>
              </button>
            )}
          </div>
        )}

        {!isCollapsed && actionBar && (
          <div className="ix-panel__action-bar-container" data-testid="panel-action-bar-container">
            {actionBar}
          </div>
        )}

        {!isCollapsed && children && (
          <div id={bodyId} className="ix-panel__body" data-testid="panel-body">
            {children}
          </div>
        )}

        {!isCollapsed && footer && (
          <div className="ix-panel__footer" data-testid="panel-footer">
            {footer}
          </div>
        )}
      </div>
    );
  },
);

Panel.displayName = "Panel";
