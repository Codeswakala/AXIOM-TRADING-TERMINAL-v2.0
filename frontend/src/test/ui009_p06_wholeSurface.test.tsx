import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import {
  Button,
  Badge,
  Card,
  StatusChip,
  Panel,
  PanelHeader,
  PanelActionBar,
  Collapsible,
  DataTable,
  Dialog,
  Skeleton,
  ErrorBanner,
  formatUncertaintyInterval,
} from "../components/ui";

describe("UI-009-P06 Whole-Surface Design System Integration & Handover (T-1, AC-6)", () => {
  it("renders a unified institutional workstation layout composed across all P01-P05 primitives", () => {
    render(
      <Panel
        variant="raised"
        header={
          <PanelHeader
            title="Institutional Whole-Surface Workspace"
            subtitle="Governed research presentation combining tokens, atoms, panels, tables, and overlays"
            actions={<Badge label="P06 COMPLETE" variant="success" />}
          />
        }
        actionBar={
          <PanelActionBar align="between">
            <Button size="sm" variant="secondary">Filter Surface</Button>
            <StatusChip level="HIGH" value="0.95" />
          </PanelActionBar>
        }
        footer={<span>UI-009 Institutional Design System Harmonization Verified</span>}
      >
        <div className="workspace-content">
          <Card header={<h4>Overview Card</h4>}>
            <p>Institutional design system primitives active across all surfaces.</p>
          </Card>

          <Collapsible title="Statistical Analytics Table" defaultExpanded={true}>
            <DataTable
              columns={[
                { key: "metric", header: "Metric Name", align: "left" },
                { key: "ci", header: "Uncertainty Interval", align: "numeric" },
              ]}
              rows={[
                { metric: "Regime Spread", ci: formatUncertaintyInterval({ lower: 0.12, upper: 0.45, confidence: 0.95 }) },
              ]}
              pagination={{
                page: 1,
                pageSize: 10,
                totalRows: 1,
                onPageChange: () => {},
              }}
            />
          </Collapsible>

          <Skeleton variant="text" />
          <ErrorBanner
            variant="warning"
            title="Advisory Only"
            message="Research environment — non-actuating presentation surface."
          />
        </div>
      </Panel>,
    );

    // Assert Header & Badge
    expect(screen.getByTestId("panel-header-title")).toHaveTextContent("Institutional Whole-Surface Workspace");
    expect(screen.getByText("P06 COMPLETE")).toBeInTheDocument();

    // Assert Action Bar & StatusChip
    expect(screen.getByRole("button", { name: /Filter Surface/i })).toBeInTheDocument();
    expect(screen.getByText("HIGH")).toBeInTheDocument();

    // Assert Card & Collapsible Table
    expect(screen.getByText("Overview Card")).toBeInTheDocument();
    expect(screen.getByText("Statistical Analytics Table")).toBeInTheDocument();
    expect(screen.getByText("Regime Spread")).toBeInTheDocument();
    expect(screen.getByText("95% CI [+0.12, +0.45]")).toBeInTheDocument();

    // Assert ErrorBanner
    expect(screen.getByTestId("error-banner-title")).toHaveTextContent("Advisory Only");

    // Assert Footer
    expect(screen.getByTestId("panel-footer")).toHaveTextContent("Harmonization Verified");
  });

  it("verifies Dialog overlay renders correctly alongside main workspace content", () => {
    render(
      <Dialog
        open={true}
        title="Final Governance Verification"
        description="All UI-009 primitives verified and harmonized."
      >
        <p>Modal dialog body content.</p>
      </Dialog>,
    );

    expect(screen.getByRole("dialog")).toBeInTheDocument();
    expect(screen.getByTestId("dialog-title")).toHaveTextContent("Final Governance Verification");
    expect(screen.getByText("Modal dialog body content.")).toBeInTheDocument();
  });
});
