import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { EmptyState } from "./EmptyState";

describe("EmptyState (UI-010-P03)", () => {
  it("renders with required title as h3 and role='status' with aria-live='polite'", () => {
    render(<EmptyState title="No reports available" />);

    const statusEl = screen.getByRole("status");
    expect(statusEl).toBeInTheDocument();
    expect(statusEl).toHaveAttribute("aria-live", "polite");
    expect(statusEl).toHaveAttribute("aria-label", "No reports available");

    const heading = screen.getByRole("heading", { level: 3, name: "No reports available" });
    expect(heading).toBeInTheDocument();
    expect(heading).toHaveClass("ix-empty-state__title");
  });

  it("renders description and custom icon when provided", () => {
    render(
      <EmptyState
        title="Empty Workspace"
        description="There are currently no active artifacts in this view."
        icon={<span data-testid="custom-icon">◈</span>}
      />,
    );

    expect(screen.getByText("There are currently no active artifacts in this view.")).toBeInTheDocument();
    expect(screen.getByTestId("custom-icon")).toBeInTheDocument();
  });

  it("renders action button and handles click callback", () => {
    const handleRetry = vi.fn();
    render(
      <EmptyState
        title="No data found"
        action={{
          label: "Retry Query",
          onClick: handleRetry,
        }}
      />,
    );

    const button = screen.getByRole("button", { name: "Retry Query" });
    expect(button).toBeInTheDocument();
    fireEvent.click(button);
    expect(handleRetry).toHaveBeenCalledTimes(1);
  });

  it("does not render action button when action prop is omitted", () => {
    render(<EmptyState title="Inert state" />);
    expect(screen.queryByRole("button")).not.toBeInTheDocument();
  });

  it("renders compact variant with correct data attributes", () => {
    render(
      <EmptyState
        title="Compact Empty"
        variant="compact"
        description="Subtle empty state"
      />,
    );

    const el = screen.getByTestId("empty-state");
    expect(el).toHaveClass("ix-empty-state--compact");
    expect(el).toHaveAttribute("data-variant", "compact");
  });

  it("supports disabled action button", () => {
    const handleClick = vi.fn();
    render(
      <EmptyState
        title="Action disabled"
        action={{
          label: "Sync Disabled",
          onClick: handleClick,
          disabled: true,
        }}
      />,
    );

    const button = screen.getByRole("button", { name: "Sync Disabled" });
    expect(button).toBeDisabled();
    fireEvent.click(button);
    expect(handleClick).not.toHaveBeenCalled();
  });
});
