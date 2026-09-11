/**
 * AXIOM Institutional Accessibility — SrOnly (UI-010-P05)
 *
 * Screen-reader-only text wrapper utility (WCAG 1.3.1 / 4.1.3).
 * Visually hidden via clip path but readable by screen readers.
 *
 * Invariant: Zero layout impact; pure assistive element.
 */

import type { ReactNode } from "react";

export interface SrOnlyProps {
  children: ReactNode;
  className?: string;
  as?: "span" | "div" | "p";
}

export function SrOnly({ children, className = "", as: Component = "span" }: SrOnlyProps) {
  return (
    <Component className={`ix-sr-only ${className}`} data-ui010-component="sr-only">
      {children}
    </Component>
  );
}
