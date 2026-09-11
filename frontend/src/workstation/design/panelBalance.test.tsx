import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import {
  Panel,
  PanelHeader,
  PanelActionBar,
  Card,
  Button,
  StatusChip,
} from "../../components/ui";

describe("Panel Balance & Workspace Frame Harmonization (UI-011-P02 / T-1, T-2, AC-1, AC-2, AC-3)", () => {
  it("AC-1: renders Panel with standardized header, body, action bar, and footer slots", () => {
    render(
      <Panel
        padding="md"
        header={
          <PanelHeader
            title="Calibrated Market Panel"
            subtitle="Governed research overview"
            headingLevel={2}
          />
        }
        actionBar={
          <PanelActionBar align="between">
            <Button size="sm" variant="secondary">Filter Context</Button>
            <StatusChip level="HIGH" label="Calibrated" />
          </PanelActionBar>
        }
        footer={<span>Level 1 Mission-Critical Telemetry Frame</span>}
      >
        <p>Panel interior content verifying balanced spacing rhythm.</p>
      </Panel>,
    );

    expect(screen.getByTestId("panel-header-container")).toBeInTheDocument();
    expect(screen.getByTestId("panel-action-bar-container")).toBeInTheDocument();
    expect(screen.getByTestId("panel-body")).toBeInTheDocument();
    expect(screen.getByTestId("panel-footer")).toBeInTheDocument();
    expect(screen.getByRole("heading", { level: 2, name: "Calibrated Market Panel" })).toBeInTheDocument();
  });

  it("AC-2 & AC-3: renders Card with default and raised elevation classes", () => {
    const { rerender } = render(
      <Card header={<h4>Scenario Factor Attribution</h4>}>
        <p>Default card interior.</p>
      </Card>,
    );

    const card = screen.getByText("Default card interior.").closest(".ix-card");
    expect(card).toBeInTheDocument();
    expect(card).not.toHaveClass("ix-card--raised");

    rerender(
      <Card variant="raised" header={<h4>Scenario Factor Attribution</h4>}>
        <p>Raised card interior.</p>
      </Card>,
    );
    const raisedCard = screen.getByText("Raised card interior.").closest(".ix-card");
    expect(raisedCard).toHaveClass("ix-card--raised");
  });

  it("AC-3: applies raised elevation class to Panel", () => {
    render(
      <Panel
        variant="raised"
        header={<PanelHeader title="Raised Focus Panel" headingLevel={3} />}
      >
        <p>Raised panel body.</p>
      </Panel>,
    );

    const panel = screen.getByText("Raised panel body.").closest(".ix-panel");
    expect(panel).toHaveClass("ix-panel--raised");
    expect(panel).toHaveAttribute("data-variant", "raised");
  });
});
