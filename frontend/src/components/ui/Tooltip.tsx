/**
 * AXIOM Atomic Component — Tooltip (UI-009-P02)
 *
 * Scoped, accessible tooltip component triggered by hover or focus.
 * Keyboard: Dismissible via Escape key.
 * ARIA: role="tooltip" / aria-describedby.
 * Respects @media (prefers-reduced-motion: reduce).
 */

import { useState, useRef, type ReactNode, type KeyboardEvent } from "react";
import "./Tooltip.css";

export type TooltipPlacement = "top" | "bottom" | "left" | "right";

export interface TooltipProps {
  content: ReactNode;
  placement?: TooltipPlacement;
  delay?: number;
  children: ReactNode;
  className?: string;
}

export function Tooltip({
  content,
  placement = "top",
  delay = 200,
  children,
  className = "",
}: TooltipProps) {
  const [isVisible, setIsVisible] = useState(false);
  const timeoutRef = useRef<number | null>(null);
  const tooltipId = useRef(`ix-tooltip-${Math.random().toString(36).substring(2, 9)}`).current;

  function showTooltip() {
    if (timeoutRef.current) window.clearTimeout(timeoutRef.current);
    timeoutRef.current = window.setTimeout(() => {
      setIsVisible(true);
    }, delay);
  }

  function hideTooltip() {
    if (timeoutRef.current) {
      window.clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }
    setIsVisible(false);
  }

  function handleKeyDown(event: KeyboardEvent<HTMLElement>) {
    if (event.key === "Escape") {
      hideTooltip();
    }
  }

  return (
    <div
      className={`ix-tooltip-container ${className}`}
      onMouseEnter={showTooltip}
      onMouseLeave={hideTooltip}
      onFocus={showTooltip}
      onBlur={hideTooltip}
      onKeyDown={handleKeyDown}
      data-ui009-component="tooltip"
    >
      <div className="ix-tooltip-trigger" aria-describedby={isVisible ? tooltipId : undefined}>
        {children}
      </div>

      {isVisible && (
        <div
          id={tooltipId}
          role="tooltip"
          className={`ix-tooltip ix-tooltip--${placement}`}
          data-testid="tooltip-content"
        >
          {content}
        </div>
      )}
    </div>
  );
}
