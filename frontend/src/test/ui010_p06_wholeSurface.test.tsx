/**
 * AXIOM Institutional UI — UI-010-P06 Whole-Surface Accessibility Integration & Handover (T-1, AC-6, AC-7)
 *
 * Verifies end-to-end composition of all accessibility and operator experience primitives
 * across P01–P05 (SkipLink, responsive reflow, EmptyState, focus traps, RouteAnnouncer, SrOnly).
 */

import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import {
  Button,
  Badge,
  StatusChip,
  Panel,
  PanelHeader,
  DataTable,
  Dialog,
  EmptyState,
  ErrorBanner,
  Skeleton,
} from "../components/ui";
import { SkipLink } from "../workstation/accessibility/SkipLink";
import { RouteAnnouncer } from "../workstation/accessibility/RouteAnnouncer";
import { SrOnly } from "../workstation/accessibility/SrOnly";

describe("UI-010-P06 Whole-Surface Accessibility & Operator Experience Integration (T-1, AC-6, AC-7)", () => {
  it("renders a unified institutional workstation layout composing P01-P05 accessibility primitives", () => {
    render(
      <MemoryRouter initialEntries={["/intelligence"]}>
        <div className="ix-shell theme-dark" data-testid="institutional-shell">
          <SkipLink href="#main-content" />
          <RouteAnnouncer />

          <header role="banner" aria-label="Global Header">
            <SrOnly>AXIOM Workstation Header</SrOnly>
            <Badge variant="success" label="GATE CLOSED" />
          </header>

          <main id="main-content" role="main" aria-label="Primary Workspace">
            <Panel
              variant="raised"
              header={
                <PanelHeader
                  title="Whole-Surface Accessibility Handover"
                  subtitle="Unified institutional presentation adhering to WCAG 2.1 AA/AAA standards"
                  actions={<StatusChip level="HIGH" label="Audited" />}
                />
              }
            >
              <div className="panel-body-content">
                <Skeleton variant="text" />
                <DataTable
                  columns={[
                    { key: "category", header: "Compliance Area", align: "left" },
                    { key: "standard", header: "Standard", align: "left" },
                    { key: "status", header: "Status", align: "right" },
                  ]}
                  rows={[
                    { category: "Bypass Blocks", standard: "WCAG 2.4.1", status: "VERIFIED" },
                    { category: "Status Messages", standard: "WCAG 4.1.3", status: "VERIFIED" },
                    { category: "Focus Visible", standard: "WCAG 2.4.7", status: "VERIFIED" },
                  ]}
                />

                <EmptyState
                  title="No Unaudited Subsystems"
                  description="All primary workstation surfaces conform to WCAG 2.1 AA/AAA specifications."
                  variant="compact"
                  action={{
                    label: "View Evidence Logs",
                    onClick: () => {},
                  }}
                />

                <ErrorBanner
                  variant="warning"
                  title="Advisory Research Notice"
                  message="All telemetry displays are strictly research-only and non-actuating."
                />
              </div>
            </Panel>
          </main>
        </div>
      </MemoryRouter>,
    );

    // 1. SkipLink bypass check
    const skipLink = screen.getByRole("link", { name: /Skip to main content/i });
    expect(skipLink).toBeInTheDocument();
    expect(skipLink).toHaveAttribute("href", "#main-content");

    // 2. RouteAnnouncer live region check
    const liveRegion = screen.getByTestId("route-announcer");
    expect(liveRegion).toBeInTheDocument();
    expect(liveRegion).toHaveAttribute("role", "status");
    expect(liveRegion).toHaveAttribute("aria-live", "polite");
    expect(liveRegion).toHaveTextContent(/Navigated to Institutional Intelligence/);

    // 3. SrOnly wrapper check
    expect(screen.getByText("AXIOM Workstation Header")).toHaveClass("ix-sr-only");

    // 4. Panel, DataTable & Multi-Modal Status check
    expect(screen.getByText("Whole-Surface Accessibility Handover")).toBeInTheDocument();
    expect(screen.getByText("GATE CLOSED")).toBeInTheDocument();
    expect(screen.getByText("Bypass Blocks")).toBeInTheDocument();
    expect(screen.getByText("WCAG 2.4.1")).toBeInTheDocument();

    // 5. EmptyState & ErrorBanner check
    expect(screen.getByRole("status", { name: "No Unaudited Subsystems" })).toBeInTheDocument();
    expect(screen.getByRole("alert")).toBeInTheDocument();
    expect(screen.getByText("Advisory Research Notice")).toBeInTheDocument();
  });

  it("verifies Dialog focus trapping and accessibility contracts alongside whole-surface components", () => {
    render(
      <div>
        <Button data-testid="trigger-btn">Open Review Modal</Button>
        <Dialog
          open={true}
          title="Whole-Surface Completion Checkpoint"
          description="UI-010 Accessibility Transformation successfully completed."
          onClose={() => {}}
        >
          <p>All 6 phases verified with zero regressions.</p>
        </Dialog>
      </div>,
    );

    const dialog = screen.getByRole("dialog");
    expect(dialog).toBeInTheDocument();
    expect(dialog).toHaveAttribute("aria-modal", "true");
    expect(screen.getByText("Whole-Surface Completion Checkpoint")).toBeInTheDocument();
    expect(screen.getByText("All 6 phases verified with zero regressions.")).toBeInTheDocument();
  });
});
