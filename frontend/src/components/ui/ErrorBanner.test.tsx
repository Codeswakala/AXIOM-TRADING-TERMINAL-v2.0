import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { ErrorBanner } from "./ErrorBanner";

describe("UI-009-P05 ErrorBanner Component (T-5, AC-5, U-3)", () => {
  it("renders error banner with role='alert', symbol, title, and message", () => {
    render(
      <ErrorBanner
        variant="error"
        title="Connection Interrupted"
        message="Unable to reach telemetry service. Check authentication token."
      />,
    );

    const banner = screen.getByRole("alert");
    expect(banner).toBeInTheDocument();
    expect(banner).toHaveAttribute("aria-live", "assertive");
    expect(screen.getByTestId("error-banner-icon")).toHaveTextContent("✕");
    expect(screen.getByTestId("error-banner-title")).toHaveTextContent("Connection Interrupted");
    expect(screen.getByTestId("error-banner-message")).toHaveTextContent("Unable to reach telemetry service.");
  });

  it("renders warning variant with appropriate symbol", () => {
    render(
      <ErrorBanner
        variant="warning"
        title="Stale Telemetry Feed"
        message="Market data has not updated in 60 seconds."
      />,
    );

    expect(screen.getByTestId("error-banner-icon")).toHaveTextContent("⚠");
    expect(screen.getByTestId("error-banner-title")).toHaveTextContent("Stale Telemetry Feed");
  });

  it("triggers action onClick when action button is pressed", () => {
    const handleRetry = vi.fn();
    render(
      <ErrorBanner
        title="Request Failed"
        message="Transient error occurred."
        action={{ label: "Retry Connection", onClick: handleRetry }}
      />,
    );

    const actionBtn = screen.getByRole("button", { name: /Retry Connection/i });
    expect(actionBtn).toBeInTheDocument();

    fireEvent.click(actionBtn);
    expect(handleRetry).toHaveBeenCalledTimes(1);
  });

  it("triggers onDismiss when close button is clicked", () => {
    const handleDismiss = vi.fn();
    render(
      <ErrorBanner
        title="Dismissible Notice"
        message="Notice body text."
        onDismiss={handleDismiss}
      />,
    );

    const closeBtn = screen.getByTestId("error-banner-close-btn");
    fireEvent.click(closeBtn);

    expect(handleDismiss).toHaveBeenCalledTimes(1);
  });
});
