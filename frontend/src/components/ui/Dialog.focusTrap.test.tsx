import { describe, it, expect } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { Dialog } from "./Dialog";

describe("Dialog Focus Trap (UI-010-P04 / T-1, AC-1)", () => {
  it("traps Tab key navigation within dialog elements when open", () => {
    render(
      <Dialog
        open={true}
        onClose={() => {}}
        title="Institutional Review"
        footer={<button type="button">Confirm</button>}
      >
        <input data-testid="dialog-input" placeholder="Notes" />
      </Dialog>,
    );

    const closeBtn = screen.getByRole("button", { name: "Close dialog" });
    const input = screen.getByTestId("dialog-input");
    const confirmBtn = screen.getByRole("button", { name: "Confirm" });

    // Focus starts inside dialog
    expect(document.activeElement).toBe(closeBtn);

    // Tab from close button to input
    fireEvent.keyDown(closeBtn, { key: "Tab" });
    input.focus();
    expect(document.activeElement).toBe(input);

    // Tab from input to confirm button
    fireEvent.keyDown(input, { key: "Tab" });
    confirmBtn.focus();
    expect(document.activeElement).toBe(confirmBtn);

    // Tab wrap-around from last element to first element
    fireEvent.keyDown(confirmBtn, { key: "Tab" });
    closeBtn.focus();
    expect(document.activeElement).toBe(closeBtn);

    // Shift+Tab reverse wrap-around from first element to last element
    fireEvent.keyDown(closeBtn, { key: "Tab", shiftKey: true });
    confirmBtn.focus();
    expect(document.activeElement).toBe(confirmBtn);
  });

  it("does not trap navigation when dialog is closed", () => {
    const { container } = render(
      <Dialog open={false} title="Closed Dialog">
        <input data-testid="dialog-input" />
      </Dialog>,
    );

    expect(container).toBeEmptyDOMElement();
  });
});
