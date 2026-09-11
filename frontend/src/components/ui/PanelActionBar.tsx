/**
 * AXIOM Institutional UI Component — PanelActionBar (UI-009-P03)
 *
 * Horizontal action grouping bar for panel headers, bodies, or footers.
 * Supports alignment, flex wrapping, and motion restraint.
 *
 * Invariant: Pure token consumption via var(--ix-*); zero ad-hoc hex.
 */

import { forwardRef, type HTMLAttributes, type ReactNode } from "react";
import "./PanelActionBar.css";

export type PanelActionBarAlign = "start" | "end" | "between";

export interface PanelActionBarProps extends HTMLAttributes<HTMLDivElement> {
  align?: PanelActionBarAlign;
  wrap?: boolean;
  children?: ReactNode;
  className?: string;
}

export const PanelActionBar = forwardRef<HTMLDivElement, PanelActionBarProps>(
  (
    {
      align = "start",
      wrap = false,
      children,
      className = "",
      ...rest
    },
    ref,
  ) => {
    return (
      <div
        ref={ref}
        className={`ix-panel-action-bar ix-panel-action-bar--align-${align} ${
          wrap ? "ix-panel-action-bar--wrap" : ""
        } ${className}`}
        data-ui009-component="panel-action-bar"
        data-align={align}
        data-wrap={wrap}
        {...rest}
      >
        {children}
      </div>
    );
  },
);

PanelActionBar.displayName = "PanelActionBar";
