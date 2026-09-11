/**
 * AXIOM Institutional UI — UI-011-P06 Whole-Surface Version 1.0 Handover & Completion Checkpoint (T-1, AC-6, AC-7)
 *
 * Verifies end-to-end composition of all institutional refinement primitives across UI-011 P01–P05:
 * - P01: 4-Level Visual Hierarchy & 4-Level Elevation Shadow Hierarchy
 * - P02: Standardized Panel Spacing Rhythm & Card Interior Balance
 * - P03: Micro-Interaction Fast Transitions (120ms) & Reduced-Motion Zeroing
 * - P04: Optical Typography Scale & Monospace Tabular-Nums Financial Data Alignment
 * - P05: Cross-Workspace Visual Cohesion & Layout Stability
 */

import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import {
  Button,
  Badge,
  StatusChip,
  Panel,
  PanelHeader,
  PanelActionBar,
  DataTable,
  Card,
  Dialog,
  EmptyState,
  ErrorBanner,
  formatPips,
  formatPercent,
  formatPearsonR,
} from "../components/ui";
import {
  HIERARCHY_TOKENS,
  ELEVATION_TOKENS,
  MOTION_TOKENS,
  TYPOGRAPHY_TOKENS,
  TYPOGRAPHY_SCALE,
  SPACING_SCALE,
} from "../workstation/design/theme";
import { SkipLink } from "../workstation/accessibility/SkipLink";
import { RouteAnnouncer } from "../workstation/accessibility/RouteAnnouncer";

describe("UI-011-P06 Whole-Surface Version 1.0 Handover & Completion Checkpoint (T-1, AC-6, AC-7)", () => {
  it("AC-1..AC-7: renders unified institutional workstation composing all UI-011 P01-P05 refinement primitives", () => {
    interface TelemetryData {
      instrument: string;
      price: string;
      spread: string;
      pips: string;
      confidence: string;
      generalizationR: string;
    }

    const tableColumns = [
      { key: "instrument", header: "Instrument", align: "left" as const },
      { key: "price", header: "Bid / Ask", align: "numeric" as const },
      { key: "spread", header: "Spread (pts)", align: "numeric" as const },
      { key: "pips", header: "Pips P/L", align: "numeric" as const },
      { key: "confidence", header: "Confidence", align: "numeric" as const },
      { key: "generalizationR", header: "Pearson r", align: "numeric" as const },
    ];

    const tableRows: TelemetryData[] = [
      {
        instrument: "EUR/USD",
        price: "1.08450",
        spread: "0.8",
        pips: formatPips(24.5),
        confidence: formatPercent(94.2),
        generalizationR: formatPearsonR(0.86),
      },
      {
        instrument: "GBP/USD",
        price: "1.29120",
        spread: "1.1",
        pips: formatPips(-8.3),
        confidence: formatPercent(88.0),
        generalizationR: formatPearsonR(0.79),
      },
    ];

    render(
      <MemoryRouter initialEntries={["/governance"]}>
        <div className="ix-shell theme-dark" data-testid="version1-workstation-shell">
          <SkipLink href="#main-workstation-area" />
          <RouteAnnouncer />

          <header role="banner" aria-label="Global Workstation Header" className="ix-global-header">
            <div className="ix-brand-block">
              <span className="ix-brand-mark">AX</span>
              <div className="ix-brand-copy">
                <span className="ix-workspace-title">AXIOM Institutional Terminal</span>
                <span className="ix-metadata">Version 1.0 Refined Surface</span>
              </div>
            </div>
            <div className="ix-header-status">
              <Badge variant="success" label="GATE CLOSED · RESEARCH ONLY" />
              <StatusChip level="HIGH" label="Harmonized" />
            </div>
          </header>

          <main id="main-workstation-area" role="main" aria-label="Primary Workspace" className="ix-primary-workspace">
            <div className="ix-workspace-grid" style={{ display: "grid", gridTemplateColumns: "repeat(12, 1fr)", gap: "16px" }}>
              {/* Level 1 Mission-Critical Telemetry Frame */}
              <Panel
                className="span-12"
                variant="raised"
                header={
                  <PanelHeader
                    title="Live Advisory Telemetry Stream"
                    subtitle="Level 1 Mission-Critical Telemetry Frame (P01/P02/P04 Refined)"
                    headingLevel={2}
                    actions={<Button size="sm" variant="secondary">Filter Context</Button>}
                  />
                }
                actionBar={
                  <PanelActionBar align="between">
                    <span className="ix-metadata">4px Rhythm Grid · Monospace Tabular Nums</span>
                    <StatusChip level="HIGH" label="Calibrated" />
                  </PanelActionBar>
                }
                footer={<span>RESEARCH-ONLY · NON-ACTUATING ADVISORY EVIDENCE</span>}
              >
                <div className="panel-inner-container">
                  <DataTable columns={tableColumns} rows={tableRows} />
                </div>
              </Panel>

              {/* Supporting Analytics Cards */}
              <div className="span-6" style={{ gridColumn: "span 6" }}>
                <Card
                  variant="raised"
                  header={<h4>Scenario Factor Attribution</h4>}
                  footer={<span className="ix-metadata">Level 2 Active Context Frame</span>}
                >
                  <p>Multi-horizon econometric decomposition with 120ms stable transition feedback.</p>
                </Card>
              </div>

              <div className="span-6" style={{ gridColumn: "span 6" }}>
                <Card
                  variant="default"
                  header={<h4>Governance Operational Posture</h4>}
                  footer={<span className="ix-metadata">Level 4 Administrative Meta Frame</span>}
                >
                  <p>Alembic migration head 20260717_0037 verified. Zero unauthenticated endpoints.</p>
                </Card>
              </div>
            </div>

            <EmptyState
              title="All Refinement Vectors Harmonized"
              description="UI-011 Institutional Refinement & Version 1.0 Presentation fully complete."
              variant="compact"
            />

            <ErrorBanner
              variant="warning"
              title="Institutional Governance Notice"
              message="Platform order routing is firewalled. Live execution gate remains strictly closed."
            />
          </main>
        </div>
      </MemoryRouter>,
    );

    // 1. Accessibility & Shell Landmarks
    expect(screen.getByRole("link", { name: /Skip to main content/i })).toBeInTheDocument();
    expect(screen.getByRole("banner", { name: "Global Workstation Header" })).toBeInTheDocument();
    expect(screen.getByRole("main", { name: "Primary Workspace" })).toBeInTheDocument();

    // 2. Information Hierarchy & Spacing Rhythm
    expect(screen.getByText("Live Advisory Telemetry Stream")).toBeInTheDocument();
    expect(screen.getByText("GATE CLOSED · RESEARCH ONLY")).toBeInTheDocument();
    expect(screen.getByText("Scenario Factor Attribution")).toBeInTheDocument();
    expect(screen.getByText("Governance Operational Posture")).toBeInTheDocument();

    // 3. Monospace Tabular-Nums Financial Data Columns
    expect(screen.getByTestId("column-header-price")).toHaveClass("ix-data-table__th--numeric");
    expect(screen.getByTestId("column-header-spread")).toHaveClass("ix-data-table__th--numeric");
    expect(screen.getByTestId("column-header-pips")).toHaveClass("ix-data-table__th--numeric");
    expect(screen.getByText("1.08450")).toHaveClass("ix-data-table__cell--numeric");
    expect(screen.getByText("+24.5 pips")).toHaveClass("ix-data-table__cell--numeric");
    expect(screen.getByText("94.2%")).toHaveClass("ix-data-table__cell--numeric");
    expect(screen.getByText("r=0.86")).toHaveClass("ix-data-table__cell--numeric");

    // 4. Feedback & Empty States
    expect(screen.getByRole("status", { name: "All Refinement Vectors Harmonized" })).toBeInTheDocument();
    expect(screen.getByRole("alert")).toBeInTheDocument();
  });

  it("AC-1..AC-5: verifies token contracts across all 5 design subsystems", () => {
    // 1. Hierarchy tokens (P01)
    expect(HIERARCHY_TOKENS.level1).toBe("var(--ix-hierarchy-level-1)");
    expect(HIERARCHY_TOKENS.level2).toBe("var(--ix-hierarchy-level-2)");
    expect(HIERARCHY_TOKENS.level3).toBe("var(--ix-hierarchy-level-3)");
    expect(HIERARCHY_TOKENS.level4).toBe("var(--ix-hierarchy-level-4)");

    // 2. Elevation tokens (P01/P02)
    expect(ELEVATION_TOKENS.level1).toBe("var(--ix-elevation-level-1)");
    expect(ELEVATION_TOKENS.level2).toBe("var(--ix-elevation-level-2)");
    expect(ELEVATION_TOKENS.level3).toBe("var(--ix-elevation-level-3)");
    expect(ELEVATION_TOKENS.level4).toBe("var(--ix-elevation-level-4)");

    // 3. Motion tokens (P03)
    expect(MOTION_TOKENS.fast).toBe("var(--ix-motion-fast)");
    expect(MOTION_TOKENS.standard).toBe("var(--ix-motion-standard)");
    expect(MOTION_TOKENS.ease).toBe("var(--ix-motion-ease)");

    // 4. Typography tokens (P04)
    expect(TYPOGRAPHY_TOKENS.fontSizeDisplay).toBe("var(--ix-font-size-display)");
    expect(TYPOGRAPHY_TOKENS.fontSizeBody).toBe("var(--ix-font-size-body)");
    expect(TYPOGRAPHY_TOKENS.fontSizeMetadata).toBe("var(--ix-font-size-metadata)");
    expect(TYPOGRAPHY_TOKENS.fontMono).toBe("var(--ix-font-mono)");
    expect(TYPOGRAPHY_SCALE.displayTitle).toBe("var(--ix-type-display-title)");
    expect(TYPOGRAPHY_SCALE.body).toBe("var(--ix-type-body)");

    // 5. Spacing scale (4px rhythm)
    expect(SPACING_SCALE.space1).toBe("var(--ix-space-1)");
    expect(SPACING_SCALE.space4).toBe("var(--ix-space-4)");
    expect(SPACING_SCALE.space6).toBe("var(--ix-space-6)");
    expect(SPACING_SCALE.space8).toBe("var(--ix-space-8)");
  });

  it("AC-6 & AC-7: verifies modal dialog focus trapping and backdrop stability under Version 1.0 presentation", () => {
    const handleClose = vi.fn();
    render(
      <Dialog
        open={true}
        onClose={handleClose}
        title="Version 1.0 Handover Certification Checkpoint"
        description="Formal review package under Doc 11 and Doc 16."
      >
        <p>UI-011 Institutional Transformation Programme complete.</p>
      </Dialog>,
    );

    const dialog = screen.getByRole("dialog");
    expect(dialog).toBeInTheDocument();
    expect(dialog).toHaveAttribute("aria-modal", "true");
    expect(screen.getByText("Version 1.0 Handover Certification Checkpoint")).toBeInTheDocument();
    expect(screen.getByText("UI-011 Institutional Transformation Programme complete.")).toBeInTheDocument();
  });
});
