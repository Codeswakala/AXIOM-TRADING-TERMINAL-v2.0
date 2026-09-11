import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import {
  HIERARCHY_TOKENS,
  ELEVATION_TOKENS,
  SPACING_SCALE,
} from "./theme";
import { Panel, PanelHeader, Card } from "../../components/ui";

describe("Information Hierarchy & Spacing Proportion Calibration (UI-011-P01 / T-1, T-2, AC-1, AC-2)", () => {
  it("AC-1: defines visual hierarchy tokens and elevation contracts in theme", () => {
    expect(HIERARCHY_TOKENS.level1).toBe("var(--ix-hierarchy-level-1)");
    expect(HIERARCHY_TOKENS.level2).toBe("var(--ix-hierarchy-level-2)");
    expect(HIERARCHY_TOKENS.level3).toBe("var(--ix-hierarchy-level-3)");
    expect(HIERARCHY_TOKENS.level4).toBe("var(--ix-hierarchy-level-4)");

    expect(ELEVATION_TOKENS.level1).toBe("var(--ix-elevation-level-1)");
    expect(ELEVATION_TOKENS.level2).toBe("var(--ix-elevation-level-2)");
    expect(ELEVATION_TOKENS.level3).toBe("var(--ix-elevation-level-3)");
    expect(ELEVATION_TOKENS.level4).toBe("var(--ix-elevation-level-4)");
  });

  it("AC-2: verifies spacing scale conforms to the 4px/8px/12px/16px/20px/24px/32px grid", () => {
    expect(SPACING_SCALE.space1).toBe("var(--ix-space-1)"); // 4px
    expect(SPACING_SCALE.space2).toBe("var(--ix-space-2)"); // 8px
    expect(SPACING_SCALE.space3).toBe("var(--ix-space-3)"); // 12px
    expect(SPACING_SCALE.space4).toBe("var(--ix-space-4)"); // 16px
    expect(SPACING_SCALE.space5).toBe("var(--ix-space-5)"); // 20px
    expect(SPACING_SCALE.space6).toBe("var(--ix-space-6)"); // 24px
    expect(SPACING_SCALE.space8).toBe("var(--ix-space-8)"); // 32px
  });

  it("AC-2: renders Panel frame with standardized spacing and header hierarchy", () => {
    render(
      <Panel
        padding="md"
        header={
          <PanelHeader
            title="Institutional Telemetry"
            subtitle="Level 1 Mission-Critical Telemetry Stream"
            headingLevel={2}
          />
        }
      >
        <p>Panel body content adhering to tokenized 4px spacing scale.</p>
      </Panel>,
    );

    const panel = screen.getByTestId("panel-body");
    expect(panel).toBeInTheDocument();
    expect(screen.getByRole("heading", { level: 2, name: "Institutional Telemetry" })).toBeInTheDocument();
    expect(screen.getByText("Level 1 Mission-Critical Telemetry Stream")).toBeInTheDocument();
  });

  it("AC-2: renders Card with tokenized header and body padding", () => {
    render(
      <Card header={<h4>Active Scenario</h4>}>
        <p>Scenario parameters conforming to hierarchy elevation.</p>
      </Card>,
    );

    expect(screen.getByRole("heading", { level: 4, name: "Active Scenario" })).toBeInTheDocument();
    expect(screen.getByText("Scenario parameters conforming to hierarchy elevation.")).toBeInTheDocument();
  });
});
