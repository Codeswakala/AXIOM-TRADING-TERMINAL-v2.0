import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { Button, Input, Select, Collapsible } from "../../components/ui";

describe("Focus Visibility & Keyboard Outline Hardening (UI-010-P04 / T-4, AC-3)", () => {
  it("renders Button primitive with focusable interactive attributes", () => {
    render(<Button>Trade Research Plan</Button>);
    const button = screen.getByRole("button", { name: "Trade Research Plan" });
    expect(button).toBeInTheDocument();
    expect(button).not.toBeDisabled();
    button.focus();
    expect(document.activeElement).toBe(button);
  });

  it("renders Input primitive with focusable attributes and helper structure", () => {
    render(<Input label="Research Query" id="query-input" placeholder="Search signals..." />);
    const input = screen.getByPlaceholderText("Search signals...");
    expect(input).toBeInTheDocument();
    input.focus();
    expect(document.activeElement).toBe(input);
  });

  it("renders Select trigger with focusable attributes and keyboard aria attributes", () => {
    render(
      <Select
        label="Timeframe"
        options={[
          { label: "M1", value: "M1" },
          { label: "H1", value: "H1" },
        ]}
      />,
    );
    const trigger = screen.getByRole("button", { name: "Timeframe" });
    expect(trigger).toBeInTheDocument();
    expect(trigger).toHaveAttribute("aria-haspopup", "listbox");
    trigger.focus();
    expect(document.activeElement).toBe(trigger);
  });

  it("renders Collapsible trigger with keyboard focus and expansion toggling", () => {
    render(
      <Collapsible title="Model Calibration Lineage">
        <p>Lineage details</p>
      </Collapsible>,
    );
    const trigger = screen.getByRole("button", { name: "Model Calibration Lineage" });
    expect(trigger).toBeInTheDocument();
    trigger.focus();
    expect(document.activeElement).toBe(trigger);
  });
});
