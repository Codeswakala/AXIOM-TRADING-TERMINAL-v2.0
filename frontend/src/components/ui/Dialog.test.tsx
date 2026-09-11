import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { Dialog } from "./Dialog";

describe("UI-009-P05 Dialog Component (T-1, AC-1)", () => {
  it("renders open dialog with title, description, body, and footer", () => {
    const handleClose = vi.fn();
    render(
      <Dialog
        open={true}
        onClose={handleClose}
        title="Confirm Model Calibration"
        description="Verify parameter bounds before proceeding with research validation."
        footer={<button>Proceed</button>}
      >
        <p>Dialog inner body content</p>
      </Dialog>,
    );

    const dialog = screen.getByRole("dialog");
    expect(dialog).toBeInTheDocument();
    expect(dialog).toHaveAttribute("aria-modal", "true");
    expect(screen.getByTestId("dialog-title")).toHaveTextContent("Confirm Model Calibration");
    expect(screen.getByTestId("dialog-description")).toHaveTextContent("Verify parameter bounds");
    expect(screen.getByText("Dialog inner body content")).toBeInTheDocument();
    expect(screen.getByText("Proceed")).toBeInTheDocument();
  });

  it("does not render in DOM when open is false", () => {
    render(
      <Dialog open={false} title="Hidden Modal">
        <p>Hidden Content</p>
      </Dialog>,
    );

    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });

  it("closes dialog when Escape key is pressed (AC-1)", () => {
    const handleClose = vi.fn();
    render(
      <Dialog open={true} onClose={handleClose} title="Escape Test Dialog">
        <p>Press Escape to dismiss</p>
      </Dialog>,
    );

    const dialog = screen.getByRole("dialog");
    fireEvent.keyDown(dialog, { key: "Escape" });

    expect(handleClose).toHaveBeenCalledTimes(1);
  });

  it("closes dialog when backdrop is clicked if backdropClose is true", () => {
    const handleClose = vi.fn();
    render(
      <Dialog open={true} onClose={handleClose} backdropClose={true} title="Backdrop Test Dialog">
        <p>Click outside</p>
      </Dialog>,
    );

    const backdrop = screen.getByTestId("dialog-backdrop");
    fireEvent.click(backdrop);

    expect(handleClose).toHaveBeenCalledTimes(1);
  });

  it("does not close on backdrop click when backdropClose is false", () => {
    const handleClose = vi.fn();
    render(
      <Dialog open={true} onClose={handleClose} backdropClose={false} title="Modal Locked Dialog">
        <p>Click outside locked</p>
      </Dialog>,
    );

    const backdrop = screen.getByTestId("dialog-backdrop");
    fireEvent.click(backdrop);

    expect(handleClose).not.toHaveBeenCalled();
  });

  it("handles size variants correctly", () => {
    const { rerender } = render(
      <Dialog open={true} size="sm" title="Small Dialog">
        <p>Body</p>
      </Dialog>,
    );

    let container = screen.getByTestId("dialog-container");
    expect(container.className).toContain("ix-dialog--sm");
    expect(container).toHaveAttribute("data-size", "sm");

    rerender(
      <Dialog open={true} size="lg" title="Large Dialog">
        <p>Body</p>
      </Dialog>,
    );

    container = screen.getByTestId("dialog-container");
    expect(container.className).toContain("ix-dialog--lg");
    expect(container).toHaveAttribute("data-size", "lg");
  });

  it("traps focus on Tab and Shift+Tab navigation within dialog (AC-1)", () => {
    render(
      <Dialog
        open={true}
        title="Focus Trap Dialog"
        onClose={vi.fn()}
        footer={<button data-testid="footer-btn">Submit</button>}
      >
        <button data-testid="body-btn-1">Button 1</button>
        <button data-testid="body-btn-2">Button 2</button>
      </Dialog>,
    );

    const closeBtn = screen.getByTestId("dialog-close-button");
    const footerBtn = screen.getByTestId("footer-btn");

    const dialog = screen.getByRole("dialog");

    // Focus last element (footerBtn) and press Tab -> should wrap to first element (closeBtn)
    footerBtn.focus();
    expect(document.activeElement).toBe(footerBtn);
    fireEvent.keyDown(dialog, { key: "Tab", shiftKey: false });
    expect(document.activeElement).toBe(closeBtn);

    // Focus first element (closeBtn) and press Shift+Tab -> should wrap to last element (footerBtn)
    closeBtn.focus();
    expect(document.activeElement).toBe(closeBtn);
    fireEvent.keyDown(dialog, { key: "Tab", shiftKey: true });
    expect(document.activeElement).toBe(footerBtn);
  });
});
