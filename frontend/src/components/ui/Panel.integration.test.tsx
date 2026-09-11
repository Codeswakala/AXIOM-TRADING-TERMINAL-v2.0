import { describe, it, expect } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { Panel } from "./Panel";
import { PanelHeader } from "./PanelHeader";
import { PanelActionBar } from "./PanelActionBar";
import { Collapsible } from "./Collapsible";
import { Button } from "./Button";
import { Badge } from "./Badge";

describe("UI-009-P03 Panel Integration & Workspace Frame Composition (T-5, AC-5)", () => {
  it("composes Panel, PanelHeader, PanelActionBar, and Collapsible into a complete workspace frame", () => {
    render(
      <Panel
        variant="raised"
        padding="md"
        header={
          <PanelHeader
            title="Institutional Market Regime Frame"
            subtitle="Governed analytical surface for real-time telemetry"
            icon={<span data-testid="regime-icon">📊</span>}
            actions={
              <Badge label="Active" variant="success" />
            }
          />
        }
        actionBar={
          <PanelActionBar align="between">
            <Button size="sm" variant="secondary">Filter View</Button>
            <Button size="sm" variant="ghost">Export Spec</Button>
          </PanelActionBar>
        }
        footer={<span>Telemetry timestamp: 2026-08-11 09:00:00 UTC</span>}
      >
        <div className="workspace-panel-body">
          <p>Primary analytical data stream.</p>
          <Collapsible title="Detailed Quant Parameters" defaultExpanded={false}>
            <div data-testid="quant-details">
              <span>Hurst Exponent: 0.62</span>
              <span>Volatility Regime: Low</span>
            </div>
          </Collapsible>
        </div>
      </Panel>,
    );

    // Header assertions
    expect(screen.getByTestId("panel-header-title")).toHaveTextContent("Institutional Market Regime Frame");
    expect(screen.getByTestId("panel-header-subtitle")).toHaveTextContent("Governed analytical surface for real-time telemetry");
    expect(screen.getByTestId("regime-icon")).toBeInTheDocument();
    expect(screen.getByText("Active")).toBeInTheDocument();

    // Action bar assertions
    expect(screen.getByRole("button", { name: /Filter View/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Export Spec/i })).toBeInTheDocument();

    // Body and Collapsible assertions
    expect(screen.getByText("Primary analytical data stream.")).toBeInTheDocument();
    expect(screen.queryByTestId("quant-details")).not.toBeInTheDocument();

    const collapsibleTrigger = screen.getByTestId("collapsible-trigger");
    fireEvent.click(collapsibleTrigger);

    expect(screen.getByTestId("quant-details")).toBeInTheDocument();
    expect(screen.getByText(/Hurst Exponent: 0.62/)).toBeInTheDocument();

    // Footer assertion
    expect(screen.getByTestId("panel-footer")).toHaveTextContent("Telemetry timestamp: 2026-08-11 09:00:00 UTC");
  });

  it("retains proper accessibility tree across composed panel hierarchy", () => {
    const { container } = render(
      <Panel
        header={
          <PanelHeader
            title="Governance Audit Log Frame"
            titleId="gov-audit-title"
            headingLevel={2}
          />
        }
      >
        <p>Audit trail events</p>
      </Panel>,
    );

    const panel = container.querySelector(".ix-panel");
    expect(panel).toHaveAttribute("role", "region");
    const heading = screen.getByTestId("panel-header-title");
    expect(heading.tagName.toLowerCase()).toBe("h2");
    expect(heading).toHaveAttribute("id", "gov-audit-title");
  });
});
