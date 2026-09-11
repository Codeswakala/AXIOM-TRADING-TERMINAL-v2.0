/**
 * AXIOM Institutional Accessibility Component — SkipLink (UI-010-P01)
 *
 * Landmark bypass link component allowing keyboard and screen-reader users
 * to immediately skip repetitive header and navigation landmarks and focus
 * the primary workspace (#main-content).
 *
 * Invariant: Pure token consumption via var(--ix-*); zero ad-hoc hex.
 */

import { forwardRef, type AnchorHTMLAttributes, type MouseEvent } from "react";
import "./SkipLink.css";

export interface SkipLinkProps extends AnchorHTMLAttributes<HTMLAnchorElement> {
  targetId?: string;
  className?: string;
}

export const SkipLink = forwardRef<HTMLAnchorElement, SkipLinkProps>(
  (
    {
      targetId = "main-content",
      children = "Skip to main content",
      className = "",
      onClick,
      ...rest
    },
    ref,
  ) => {
    const handleClick = (e: MouseEvent<HTMLAnchorElement>) => {
      onClick?.(e);
      if (!e.defaultPrevented) {
        e.preventDefault();
        const target = document.getElementById(targetId);
        if (target) {
          target.focus();
          target.scrollIntoView?.({ behavior: "smooth" });
        }
      }
    };

    return (
      <a
        ref={ref}
        href={`#${targetId}`}
        className={`ix-skip-link ${className}`}
        aria-label="Skip to main content"
        data-ui010-component="skip-link"
        onClick={handleClick}
        {...rest}
      >
        {children}
      </a>
    );
  },
);

SkipLink.displayName = "SkipLink";
