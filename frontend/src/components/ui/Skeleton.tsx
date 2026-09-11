/**
 * AXIOM Institutional UI Component — Skeleton (UI-009-P05)
 *
 * Accessible loading placeholder primitive.
 * Supports text, rectangular, and circular variants with configurable dimensions.
 *
 * Invariant: Pure token consumption via var(--ix-*); zero ad-hoc hex.
 */

import { forwardRef, type HTMLAttributes } from "react";
import "./Skeleton.css";

export type SkeletonVariant = "text" | "rect" | "circle";

export interface SkeletonProps extends HTMLAttributes<HTMLDivElement> {
  variant?: SkeletonVariant;
  width?: string;
  height?: string;
  count?: number;
  className?: string;
}

export const Skeleton = forwardRef<HTMLDivElement, SkeletonProps>(
  (
    {
      variant = "text",
      width,
      height,
      count = 1,
      className = "",
      style,
      ...rest
    },
    ref,
  ) => {
    if (count <= 0) return null;

    const items = Array.from({ length: count });

    const computedStyle = {
      width,
      height,
      ...style,
    };

    if (count === 1) {
      return (
        <div
          ref={ref}
          role="status"
          aria-busy="true"
          aria-label="Loading"
          className={`ix-skeleton ix-skeleton--${variant} ${className}`}
          style={computedStyle}
          data-ui009-component="skeleton"
          data-variant={variant}
          {...rest}
        >
          <span className="ix-skeleton__sr-only">Loading…</span>
        </div>
      );
    }

    return (
      <div
        ref={ref}
        role="status"
        aria-busy="true"
        aria-label="Loading"
        className={`ix-skeleton-group ${className}`}
        data-ui009-component="skeleton-group"
        {...rest}
      >
        {items.map((_, idx) => (
          <div
            key={`skeleton-item-${idx}`}
            className={`ix-skeleton ix-skeleton--${variant}`}
            style={computedStyle}
            data-variant={variant}
            data-testid="skeleton-item"
          />
        ))}
        <span className="ix-skeleton__sr-only">Loading…</span>
      </div>
    );
  },
);

Skeleton.displayName = "Skeleton";
