/**
 * AXIOM Atomic Component — Card (UI-009-P02)
 *
 * Scoped container primitive with header, body, and footer slots.
 * Variants: default, raised, interactive.
 */

import { forwardRef, type HTMLAttributes, type ReactNode } from "react";
import "./Card.css";

export type CardVariant = "default" | "raised" | "interactive";

export interface CardProps extends HTMLAttributes<HTMLDivElement> {
  variant?: CardVariant;
  header?: ReactNode;
  footer?: ReactNode;
  children?: ReactNode;
  className?: string;
  onClick?: () => void;
}

export const Card = forwardRef<HTMLDivElement, CardProps>(
  (
    {
      variant = "default",
      header,
      footer,
      children,
      className = "",
      onClick,
      ...rest
    },
    ref,
  ) => {
    const isInteractive = variant === "interactive" || Boolean(onClick);

    return (
      <div
        ref={ref}
        className={`ix-card ix-card--${variant} ${isInteractive ? "ix-card--clickable" : ""} ${className}`}
        data-ui009-component="card"
        data-variant={variant}
        role={isInteractive ? "button" : undefined}
        tabIndex={isInteractive ? 0 : undefined}
        onClick={onClick}
        onKeyDown={
          isInteractive && onClick
            ? (e) => {
                if (e.key === "Enter" || e.key === " ") {
                  e.preventDefault();
                  onClick();
                }
              }
            : undefined
        }
        {...rest}
      >
        {header && <div className="ix-card__header" data-testid="card-header">{header}</div>}
        {children && <div className="ix-card__body" data-testid="card-body">{children}</div>}
        {footer && <div className="ix-card__footer" data-testid="card-footer">{footer}</div>}
      </div>
    );
  },
);

Card.displayName = "Card";
