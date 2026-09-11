import { describe, it, expect, vi } from "vitest";
import { render } from "@testing-library/react";
import { useKeyboardShortcuts } from "./useKeyboardShortcuts";

function TestKeyboardShortcutsComponent({
  onOpenPalette,
  onCloseTopmost,
  enabled = true,
}: {
  onOpenPalette?: () => void;
  onCloseTopmost?: () => void;
  enabled?: boolean;
}) {
  useKeyboardShortcuts({ onOpenPalette, onCloseTopmost, enabled });
  return <div data-testid="shortcuts-target">Shortcuts Active</div>;
}

describe("useKeyboardShortcuts (UI-010-P04 / T-3, AC-4)", () => {
  it("triggers onOpenPalette on Ctrl+K and Cmd+K keydown", () => {
    const handleOpenPalette = vi.fn();
    render(<TestKeyboardShortcutsComponent onOpenPalette={handleOpenPalette} />);

    // Ctrl+K
    const ctrlKEvent = new KeyboardEvent("keydown", {
      key: "k",
      ctrlKey: true,
      bubbles: true,
      cancelable: true,
    });
    window.dispatchEvent(ctrlKEvent);
    expect(handleOpenPalette).toHaveBeenCalledTimes(1);

    // Meta+K (Cmd+K on macOS)
    const cmdKEvent = new KeyboardEvent("keydown", {
      key: "k",
      metaKey: true,
      bubbles: true,
      cancelable: true,
    });
    window.dispatchEvent(cmdKEvent);
    expect(handleOpenPalette).toHaveBeenCalledTimes(2);
  });

  it("triggers onCloseTopmost on Escape keydown", () => {
    const handleCloseTopmost = vi.fn();
    render(<TestKeyboardShortcutsComponent onCloseTopmost={handleCloseTopmost} />);

    const escapeEvent = new KeyboardEvent("keydown", {
      key: "Escape",
      bubbles: true,
      cancelable: true,
    });
    window.dispatchEvent(escapeEvent);
    expect(handleCloseTopmost).toHaveBeenCalledTimes(1);
  });

  it("does not intercept shortcuts when enabled is false", () => {
    const handleOpenPalette = vi.fn();
    const handleCloseTopmost = vi.fn();
    render(
      <TestKeyboardShortcutsComponent
        onOpenPalette={handleOpenPalette}
        onCloseTopmost={handleCloseTopmost}
        enabled={false}
      />,
    );

    const ctrlKEvent = new KeyboardEvent("keydown", {
      key: "k",
      ctrlKey: true,
      bubbles: true,
    });
    window.dispatchEvent(ctrlKEvent);
    expect(handleOpenPalette).not.toHaveBeenCalled();

    const escapeEvent = new KeyboardEvent("keydown", {
      key: "Escape",
      bubbles: true,
    });
    window.dispatchEvent(escapeEvent);
    expect(handleCloseTopmost).not.toHaveBeenCalled();
  });
});
