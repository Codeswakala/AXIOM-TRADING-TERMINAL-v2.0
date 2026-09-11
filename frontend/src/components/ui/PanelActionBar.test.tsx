import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { PanelActionBar } from "./PanelActionBar";
import { Button } from "./Button";

describe("UI-009-P03 PanelActionBar Component (T-3, AC-3)", () => {
  it("renders action buttons inside flex layout", () => {
    render(
      <PanelActionBar>
        <Button variant="primary">Apply Filter</Button>
        <Button variant="secondary">Reset</Button>
      </PanelActionBar>,
    );

    expect(screen.getByRole("button", { name: /Apply Filter/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Reset/i })).toBeInTheDocument();
  });

  it("handles align variants (start, end, between)", () => {
    const { rerender, container } = render(
      <PanelActionBar align="start">
        <Button>Action</Button>
      </PanelActionBar>,
    );

    let bar = container.querySelector(".ix-panel-action-bar");
    expect(bar).toHaveAttribute("data-align", "start");
    expect(bar?.className).toContain("ix-panel-action-bar--align-start");

    rerender(
      <PanelActionBar align="end">
        <Button>Action</Button>
      </PanelActionBar>,
    );

    bar = container.querySelector(".ix-panel-action-bar");
    expect(bar).toHaveAttribute("data-align", "end");
    expect(bar?.className).toContain("ix-panel-action-bar--align-end");

    rerender(
      <PanelActionBar align="between">
        <Button>Action</Button>
      </PanelActionBar>,
    );

    bar = container.querySelector(".ix-panel-action-bar");
    expect(bar).toHaveAttribute("data-align", "between");
    expect(bar?.className).toContain("ix-panel-action-bar--align-between");
  });

  it("handles wrap prop and custom class names", () => {
    const { container } = render(
      <PanelActionBar wrap className="custom-action-bar">
        <Button>Action</Button>
      </PanelActionBar>,
    );

    const bar = container.querySelector(".ix-panel-action-bar");
    expect(bar).toHaveAttribute("data-wrap", "true");
    expect(bar?.className).toContain("ix-panel-action-bar--wrap");
    expect(bar?.className).toContain("custom-action-bar");
  });
});
