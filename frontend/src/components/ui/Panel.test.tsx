import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { Panel } from "./Panel";

describe("UI-009-P03 Panel Component (T-1, AC-1)", () => {
  it("renders header, action bar, body, and footer slots", () => {
    render(
      <Panel
        header={<h3>Market Overview Header</h3>}
        actionBar={<div>Action Bar Content</div>}
        footer={<span>Panel Footer Status</span>}
      >
        <p>Panel Body Telemetry</p>
      </Panel>,
    );

    expect(screen.getByTestId("panel-header-container")).toHaveTextContent("Market Overview Header");
    expect(screen.getByTestId("panel-action-bar-container")).toHaveTextContent("Action Bar Content");
    expect(screen.getByTestId("panel-body")).toHaveTextContent("Panel Body Telemetry");
    expect(screen.getByTestId("panel-footer")).toHaveTextContent("Panel Footer Status");
  });

  it("handles visual variants and padding options correctly", () => {
    const { rerender, container } = render(
      <Panel variant="raised" padding="sm">
        <p>Raised SM</p>
      </Panel>,
    );

    let panel = container.querySelector(".ix-panel");
    expect(panel).toHaveAttribute("data-variant", "raised");
    expect(panel).toHaveAttribute("data-padding", "sm");
    expect(panel?.className).toContain("ix-panel--raised");
    expect(panel?.className).toContain("ix-panel--padding-sm");

    rerender(
      <Panel variant="ghost" padding="lg">
        <p>Ghost LG</p>
      </Panel>,
    );

    panel = container.querySelector(".ix-panel");
    expect(panel).toHaveAttribute("data-variant", "ghost");
    expect(panel).toHaveAttribute("data-padding", "lg");
    expect(panel?.className).toContain("ix-panel--ghost");
    expect(panel?.className).toContain("ix-panel--padding-lg");
  });

  it("handles collapsible prop, toggles collapse state on toggle click, sets ARIA attributes (AC-1)", () => {
    render(
      <Panel header={<span>Collapsible Panel</span>} collapsible>
        <p>Collapsible Body Content</p>
      </Panel>,
    );

    const toggle = screen.getByTestId("panel-collapse-toggle");
    expect(toggle).toHaveAttribute("aria-expanded", "true");
    expect(screen.getByTestId("panel-body")).toHaveTextContent("Collapsible Body Content");

    fireEvent.click(toggle);

    expect(toggle).toHaveAttribute("aria-expanded", "false");
    expect(screen.queryByTestId("panel-body")).not.toBeInTheDocument();

    fireEvent.click(toggle);
    expect(toggle).toHaveAttribute("aria-expanded", "true");
    expect(screen.getByTestId("panel-body")).toBeInTheDocument();
  });

  it("supports controlled collapsed prop and onToggle callback", () => {
    const handleToggle = vi.fn();
    const { rerender } = render(
      <Panel
        header={<span>Controlled Panel</span>}
        collapsible
        collapsed={true}
        onToggle={handleToggle}
      >
        <p>Hidden Content</p>
      </Panel>,
    );

    expect(screen.queryByTestId("panel-body")).not.toBeInTheDocument();
    const toggle = screen.getByTestId("panel-collapse-toggle");
    expect(toggle).toHaveAttribute("aria-expanded", "false");

    fireEvent.click(toggle);
    expect(handleToggle).toHaveBeenCalledWith(false);

    rerender(
      <Panel
        header={<span>Controlled Panel</span>}
        collapsible
        collapsed={false}
        onToggle={handleToggle}
      >
        <p>Visible Content</p>
      </Panel>,
    );

    expect(screen.getByTestId("panel-body")).toHaveTextContent("Visible Content");
  });

  it("maintains accessible region role and aria-labelledby", () => {
    const { container } = render(
      <Panel header={<span>Accessible Header</span>} ariaLabelledBy="custom-label">
        <p>Content</p>
      </Panel>,
    );

    const panel = container.querySelector(".ix-panel");
    expect(panel).toHaveAttribute("role", "region");
    expect(panel).toHaveAttribute("aria-labelledby", "custom-label");
  });
});
