import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { PanelHeader } from "./PanelHeader";

describe("UI-009-P03 PanelHeader Component (T-2, AC-2)", () => {
  it("renders title, subtitle, icon, and actions slot", () => {
    render(
      <PanelHeader
        title="Regime Detection Engine"
        subtitle="Real-time market state classification"
        icon={<span data-testid="test-icon">icon</span>}
        actions={<button>Configure</button>}
      />,
    );

    expect(screen.getByTestId("panel-header-title")).toHaveTextContent("Regime Detection Engine");
    expect(screen.getByTestId("panel-header-subtitle")).toHaveTextContent("Real-time market state classification");
    expect(screen.getByTestId("panel-header-icon")).toBeInTheDocument();
    expect(screen.getByTestId("panel-header-actions")).toHaveTextContent("Configure");
  });

  it("respects headingLevel prop (h2 vs h3) and titleId", () => {
    const { rerender } = render(
      <PanelHeader
        title="Level 2 Heading"
        headingLevel={2}
        titleId="regime-h2"
      />,
    );

    let titleEl = screen.getByTestId("panel-header-title");
    expect(titleEl.tagName.toLowerCase()).toBe("h2");
    expect(titleEl).toHaveAttribute("id", "regime-h2");

    rerender(
      <PanelHeader
        title="Level 3 Heading"
        headingLevel={3}
        titleId="regime-h3"
      />,
    );

    titleEl = screen.getByTestId("panel-header-title");
    expect(titleEl.tagName.toLowerCase()).toBe("h3");
    expect(titleEl).toHaveAttribute("id", "regime-h3");
  });

  it("renders data attributes and custom class names", () => {
    const { container } = render(
      <PanelHeader
        title="Custom Header"
        className="custom-panel-header-cls"
      />,
    );

    const header = container.querySelector(".ix-panel-header");
    expect(header).toHaveAttribute("data-ui009-component", "panel-header");
    expect(header?.className).toContain("custom-panel-header-cls");
  });

  it("renders gracefully without optional icon, subtitle, or actions", () => {
    render(<PanelHeader title="Minimal Panel Header" />);

    expect(screen.getByTestId("panel-header-title")).toHaveTextContent("Minimal Panel Header");
    expect(screen.queryByTestId("panel-header-subtitle")).not.toBeInTheDocument();
    expect(screen.queryByTestId("panel-header-icon")).not.toBeInTheDocument();
    expect(screen.queryByTestId("panel-header-actions")).not.toBeInTheDocument();
  });
});
