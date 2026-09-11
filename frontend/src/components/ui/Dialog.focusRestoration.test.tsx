import { describe, it, expect } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { useState, useRef } from "react";
import { Dialog } from "./Dialog";

function DialogTriggerWrapper() {
  const [open, setOpen] = useState(false);
  const triggerRef = useRef<HTMLButtonElement>(null);

  return (
    <div>
      <button
        ref={triggerRef}
        type="button"
        data-testid="open-trigger"
        onClick={() => setOpen(true)}
      >
        Open Dialog
      </button>
      <Dialog
        open={open}
        onClose={() => setOpen(false)}
        title="Restoration Test Dialog"
        finalFocusRef={triggerRef}
      >
        <p>Dialog content body</p>
      </Dialog>
    </div>
  );
}

describe("Dialog Focus Restoration (UI-010-P04 / T-2, AC-2)", () => {
  it("restores focus to trigger button upon close via Escape key", () => {
    render(<DialogTriggerWrapper />);

    const trigger = screen.getByTestId("open-trigger");
    trigger.focus();
    expect(document.activeElement).toBe(trigger);

    // Open dialog
    fireEvent.click(trigger);
    const closeBtn = screen.getByRole("button", { name: "Close dialog" });
    expect(screen.getByRole("dialog")).toBeInTheDocument();

    // Press Escape to dismiss
    fireEvent.keyDown(closeBtn, { key: "Escape" });
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    expect(document.activeElement).toBe(trigger);
  });

  it("restores focus to trigger button upon close via close button click", () => {
    render(<DialogTriggerWrapper />);

    const trigger = screen.getByTestId("open-trigger");
    trigger.focus();

    fireEvent.click(trigger);
    const closeBtn = screen.getByRole("button", { name: "Close dialog" });

    fireEvent.click(closeBtn);
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    expect(document.activeElement).toBe(trigger);
  });
});
