import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { Toast } from "./Toast";
import { ToastStack } from "./ToastStack";

describe("UI-009-P05 Toast & ToastStack Component (T-4, AC-4, U-3)", () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it("renders info and success toasts with role='status' and aria-live='polite'", () => {
    render(
      <Toast
        variant="info"
        title="Analysis Completed"
        description="Regime classification finished with 120 samples."
      />,
    );

    const toast = screen.getByRole("status");
    expect(toast).toBeInTheDocument();
    expect(toast).toHaveAttribute("aria-live", "polite");
    expect(screen.getByTestId("toast-title")).toHaveTextContent("Analysis Completed");
    expect(screen.getByTestId("toast-description")).toHaveTextContent("Regime classification finished");
    expect(screen.getByTestId("toast-symbol")).toHaveTextContent("ℹ");
  });

  it("renders warning and error toasts with role='alert' and aria-live='assertive'", () => {
    render(
      <Toast
        variant="error"
        title="Refusal Recorded"
        description="External LLM integration is constitutionally prohibited."
      />,
    );

    const toast = screen.getByRole("alert");
    expect(toast).toBeInTheDocument();
    expect(toast).toHaveAttribute("aria-live", "assertive");
    expect(screen.getByTestId("toast-title")).toHaveTextContent("Refusal Recorded");
    expect(screen.getByTestId("toast-symbol")).toHaveTextContent("✕");
  });

  it("triggers onDismiss on close button click and on Escape key press", () => {
    const handleDismiss = vi.fn();
    render(
      <Toast
        variant="warning"
        title="Low Sample Size"
        onDismiss={handleDismiss}
      />,
    );

    const toast = screen.getByRole("alert");

    // Escape key
    fireEvent.keyDown(toast, { key: "Escape" });
    expect(handleDismiss).toHaveBeenCalledTimes(1);

    // Close button click
    const closeBtn = screen.getByTestId("toast-close-button");
    fireEvent.click(closeBtn);
    expect(handleDismiss).toHaveBeenCalledTimes(2);
  });

  it("auto-dismisses when autoDismissMs is provided", () => {
    const handleDismiss = vi.fn();
    render(
      <Toast
        variant="success"
        title="Saved Successfully"
        autoDismissMs={3000}
        onDismiss={handleDismiss}
      />,
    );

    expect(handleDismiss).not.toHaveBeenCalled();
    vi.advanceTimersByTime(3000);
    expect(handleDismiss).toHaveBeenCalledTimes(1);
  });

  it("renders a stack of toasts inside an accessible notification region", () => {
    const toasts = [
      { id: "t1", variant: "info" as const, title: "Notification 1" },
      { id: "t2", variant: "success" as const, title: "Notification 2" },
    ];

    render(<ToastStack toasts={toasts} />);

    const region = screen.getByRole("region", { name: "Notifications" });
    expect(region).toBeInTheDocument();
    expect(screen.getByText("Notification 1")).toBeInTheDocument();
    expect(screen.getByText("Notification 2")).toBeInTheDocument();
  });
});
