/**
 * AXIOM Institutional UI — UI-010-P03 Feedback States Standardization Tests (T-2, AC-1, AC-2)
 *
 * Verifies harmonization of Skeleton (aria-busy), EmptyState (role="status"),
 * ErrorBanner (role="alert"), and Toast/ToastStack across representative workspaces.
 */

import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { EmptyState, ErrorBanner, Skeleton, Toast } from "../components/ui";
import { ResearchAdvisorySignalPanel } from "../pages/InstitutionalIntelligencePage";

describe("UI-010-P03 Feedback States Standardization (T-2, AC-1, AC-2)", () => {
  it("AC-1: EmptyState primitive renders honest role='status', aria-live='polite', and h3 title", () => {
    render(
      <EmptyState
        title="No Research Reports Available"
        description="Select a different filter or generate new intelligence."
        variant="default"
      />,
    );

    const statusElement = screen.getByRole("status");
    expect(statusElement).toBeInTheDocument();
    expect(statusElement).toHaveAttribute("aria-live", "polite");
    expect(statusElement).toHaveAttribute("aria-label", "No Research Reports Available");

    const heading = screen.getByRole("heading", { level: 3, name: "No Research Reports Available" });
    expect(heading).toBeInTheDocument();
    expect(screen.getByText("Select a different filter or generate new intelligence.")).toBeInTheDocument();
  });

  it("AC-2: Skeleton primitive renders loading state with role='status' and aria-busy='true'", () => {
    render(<Skeleton variant="rect" height="120px" aria-label="Loading intelligence metrics" />);

    const loadingElement = screen.getByLabelText("Loading intelligence metrics");
    expect(loadingElement).toHaveAttribute("role", "status");
    expect(loadingElement).toHaveAttribute("aria-busy", "true");
    expect(screen.getByText("Loading…")).toBeInTheDocument();
  });

  it("AC-2: ErrorBanner primitive renders error state with role='alert' and aria-live='assertive'", () => {
    render(
      <ErrorBanner
        title="Read Seam Connection Failure"
        message="Unable to fetch governed artifacts from persistence store."
      />,
    );

    const alertElement = screen.getByRole("alert");
    expect(alertElement).toBeInTheDocument();
    expect(alertElement).toHaveAttribute("aria-live", "assertive");
    expect(screen.getByTestId("error-banner-title")).toHaveTextContent("Read Seam Connection Failure");
    expect(screen.getByTestId("error-banner-message")).toHaveTextContent("Unable to fetch governed artifacts from persistence store.");
  });

  it("AC-2: Toast primitive distinguishes polite status notifications from assertive alerts", () => {
    const { unmount } = render(
      <Toast
        id="toast-info-1"
        title="Preference Saved"
        description="Workspace presentation layout updated."
        variant="info"
        onDismiss={() => {}}
      />,
    );

    const infoToast = screen.getByTestId("toast-container");
    expect(infoToast).toHaveAttribute("role", "status");
    expect(infoToast).toHaveAttribute("aria-live", "polite");

    unmount();

    render(
      <Toast
        id="toast-err-1"
        title="Ingestion Degraded"
        description="CSV feed checksum mismatch detected."
        variant="error"
        onDismiss={() => {}}
      />,
    );

    const errorToast = screen.getByTestId("toast-container");
    expect(errorToast).toHaveAttribute("role", "alert");
    expect(errorToast).toHaveAttribute("aria-live", "assertive");
  });

  it("AC-2: ResearchAdvisorySignalPanel harmonizes loading, empty, and error feedback states", () => {
    // 1. Loading branch
    const { rerender } = render(
      <ResearchAdvisorySignalPanel signals={[]} loading={true} error={null} />,
    );
    expect(screen.getByLabelText("Loading existing advisory records")).toHaveAttribute("aria-busy", "true");

    // 2. Empty branch
    rerender(
      <ResearchAdvisorySignalPanel signals={[]} loading={false} error={null} />,
    );
    expect(screen.getByRole("status", { name: "No Advisory Signals" })).toBeInTheDocument();
    expect(screen.getByText("No existing advisory signals returned by the read API.")).toBeInTheDocument();

    // 3. Error branch
    rerender(
      <ResearchAdvisorySignalPanel signals={[]} loading={false} error="Advisory feed timeout (504)" />,
    );
    expect(screen.getByRole("alert")).toBeInTheDocument();
    expect(screen.getByText("Advisory feed timeout (504)")).toBeInTheDocument();
  });
});
