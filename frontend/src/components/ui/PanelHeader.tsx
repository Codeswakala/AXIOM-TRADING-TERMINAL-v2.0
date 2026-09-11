/**
 * AXIOM Institutional UI Component — PanelHeader (UI-009-P03)
 *
 * Scoped header component for workspace panels.
 * Renders title, subtitle, icon, and actions slot with strict heading hierarchy.
 *
 * Invariant: Pure token consumption via var(--ix-*); zero ad-hoc hex.
 */

import { forwardRef, type HTMLAttributes, type ReactNode } from "react";
import "./PanelHeader.css";

export interface PanelHeaderProps extends Omit<HTMLAttributes<HTMLElement>, "title"> {
  title: ReactNode;
  subtitle?: ReactNode;
  icon?: ReactNode;
  actions?: ReactNode;
  headingLevel?: 2 | 3;
  titleId?: string;
  className?: string;
}

export const PanelHeader = forwardRef<HTMLElement, PanelHeaderProps>(
  (
    {
      title,
      subtitle,
      icon,
      actions,
      headingLevel = 2,
      titleId,
      className = "",
      ...rest
    },
    ref,
  ) => {
    const HeadingTag = headingLevel === 3 ? "h3" : "h2";

    return (
      <header
        ref={ref}
        className={`ix-panel-header ${className}`}
        data-ui009-component="panel-header"
        data-heading-level={headingLevel}
        {...rest}
      >
        <div className="ix-panel-header__main">
          {icon && (
            <span className="ix-panel-header__icon" aria-hidden="true" data-testid="panel-header-icon">
              {icon}
            </span>
          )}
          <div className="ix-panel-header__titles">
            <HeadingTag id={titleId} className="ix-panel-header__title" data-testid="panel-header-title">
              {title}
            </HeadingTag>
            {subtitle && (
              <p className="ix-panel-header__subtitle" data-testid="panel-header-subtitle">
                {subtitle}
              </p>
            )}
          </div>
        </div>

        {actions && (
          <div className="ix-panel-header__actions" data-testid="panel-header-actions">
            {actions}
          </div>
        )}
      </header>
    );
  },
);

PanelHeader.displayName = "PanelHeader";
