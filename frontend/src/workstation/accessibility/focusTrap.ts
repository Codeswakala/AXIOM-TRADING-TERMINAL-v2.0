/**
 * AXIOM Institutional Accessibility — Focus Trap & Restoration Helpers (UI-010-P04)
 *
 * Provides utilities for accessible modal focus trapping (WCAG 2.4.3)
 * and trigger focus restoration on overlay dismissal (WCAG 2.4.3 / 2.1.1).
 *
 * Invariant: Zero side effects; pure DOM focus management.
 */

const FOCUSABLE_SELECTOR =
  'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"]):not([disabled])';

/**
 * Returns all currently focusable elements within a container element.
 */
export function getFocusableElements(container: HTMLElement): HTMLElement[] {
  const elements = container.querySelectorAll<HTMLElement>(FOCUSABLE_SELECTOR);
  return Array.from(elements).filter(
    (el) => el.offsetParent !== null || el.offsetWidth > 0 || el.offsetHeight > 0,
  );
}

/**
 * Traps Tab and Shift+Tab keyboard navigation within a container.
 */
export function trapFocus(container: HTMLElement, event: KeyboardEvent): void {
  if (event.key !== "Tab") return;

  const focusables = getFocusableElements(container);
  if (focusables.length === 0) {
    event.preventDefault();
    return;
  }

  const firstElement = focusables[0];
  const lastElement = focusables[focusables.length - 1];

  if (event.shiftKey) {
    if (document.activeElement === firstElement || document.activeElement === container) {
      event.preventDefault();
      lastElement?.focus();
    }
  } else {
    if (document.activeElement === lastElement) {
      event.preventDefault();
      firstElement?.focus();
    }
  }
}

/**
 * Restores focus to a target element, or gracefully falls back.
 */
export function restoreFocus(target: HTMLElement | null, fallback: HTMLElement | null = null): void {
  if (target && document.contains(target)) {
    target.focus();
    return;
  }
  if (fallback && document.contains(fallback)) {
    fallback.focus();
    return;
  }
  document.body?.focus();
}
