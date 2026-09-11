/**
 * AXIOM Institutional Accessibility — Centralized Keyboard Shortcuts Registry (UI-010-P04)
 *
 * Provides centralized window keydown management for workstation-wide
 * keyboard shortcuts (WCAG 2.1.1 / 2.4.7):
 * - Ctrl+K / Cmd+K: Open Command Palette
 * - Escape: Close topmost active modal/overlay in LIFO order
 *
 * Invariant: Never intercepts standard navigation keys (Tab, Shift+Tab, Enter, Space, Arrows) globally.
 */

import { useEffect, useRef } from "react";

export interface KeyboardShortcutsOptions {
  onOpenPalette?: () => void;
  onCloseTopmost?: () => void;
  enabled?: boolean;
}

export function useKeyboardShortcuts({
  onOpenPalette,
  onCloseTopmost,
  enabled = true,
}: KeyboardShortcutsOptions) {
  const optionsRef = useRef({ onOpenPalette, onCloseTopmost, enabled });

  useEffect(() => {
    optionsRef.current = { onOpenPalette, onCloseTopmost, enabled };
  });

  useEffect(() => {
    if (!enabled) return;

    function handleKeyDown(event: KeyboardEvent) {
      const { onOpenPalette, onCloseTopmost } = optionsRef.current;

      // Ctrl+K or Cmd+K (macOS) -> Open command palette
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        onOpenPalette?.();
        return;
      }

      // Escape -> Close topmost overlay in LIFO order
      if (event.key === "Escape") {
        onCloseTopmost?.();
        return;
      }
    }

    window.addEventListener("keydown", handleKeyDown);
    return () => {
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, [enabled]);
}
