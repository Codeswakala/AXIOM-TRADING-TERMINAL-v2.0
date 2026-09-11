import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { Collapsible } from "./Collapsible";

describe("UI-009-P03 Collapsible Component (T-4, AC-4)", () => {
  it("renders collapsed by default and expands on trigger click (AC-4)", () => {
    render(
      <Collapsible title="Model Calibration Parameters">
        <p>Calibration details and hyperparameter tables.</p>
      </Collapsible>,
    );

    const trigger = screen.getByTestId("collapsible-trigger");
    expect(trigger).toHaveAttribute("aria-expanded", "false");
    expect(screen.queryByTestId("collapsible-content")).not.toBeInTheDocument();

    fireEvent.click(trigger);

    expect(trigger).toHaveAttribute("aria-expanded", "true");
    expect(screen.getByTestId("collapsible-content")).toHaveTextContent(
      "Calibration details and hyperparameter tables.",
    );

    fireEvent.click(trigger);
    expect(trigger).toHaveAttribute("aria-expanded", "false");
    expect(screen.queryByTestId("collapsible-content")).not.toBeInTheDocument();
  });

  it("supports keyboard navigation with Enter and Space keys (AC-4)", () => {
    render(
      <Collapsible title="Keyboard Accessible Section">
        <p>Accessible panel contents.</p>
      </Collapsible>,
    );

    const trigger = screen.getByTestId("collapsible-trigger");

    // Enter key
    fireEvent.keyDown(trigger, { key: "Enter" });
    expect(trigger).toHaveAttribute("aria-expanded", "true");
    expect(screen.getByTestId("collapsible-content")).toBeInTheDocument();

    // Space key
    fireEvent.keyDown(trigger, { key: " " });
    expect(trigger).toHaveAttribute("aria-expanded", "false");
    expect(screen.queryByTestId("collapsible-content")).not.toBeInTheDocument();
  });

  it("handles disabled state where trigger is not togglable", () => {
    const handleToggle = vi.fn();
    render(
      <Collapsible title="Disabled Section" disabled onToggle={handleToggle}>
        <p>Locked contents.</p>
      </Collapsible>,
    );

    const trigger = screen.getByTestId("collapsible-trigger");
    expect(trigger).toBeDisabled();

    fireEvent.click(trigger);
    expect(handleToggle).not.toHaveBeenCalled();
    expect(screen.queryByTestId("collapsible-content")).not.toBeInTheDocument();

    fireEvent.keyDown(trigger, { key: "Enter" });
    expect(handleToggle).not.toHaveBeenCalled();
  });

  it("supports controlled expanded prop and onToggle callback", () => {
    const handleToggle = vi.fn();
    const { rerender } = render(
      <Collapsible
        title="Controlled Section"
        expanded={false}
        onToggle={handleToggle}
      >
        <p>Controlled contents.</p>
      </Collapsible>,
    );

    expect(screen.queryByTestId("collapsible-content")).not.toBeInTheDocument();
    const trigger = screen.getByTestId("collapsible-trigger");

    fireEvent.click(trigger);
    expect(handleToggle).toHaveBeenCalledWith(true);

    rerender(
      <Collapsible
        title="Controlled Section"
        expanded={true}
        onToggle={handleToggle}
      >
        <p>Controlled contents.</p>
      </Collapsible>,
    );

    expect(screen.getByTestId("collapsible-content")).toBeInTheDocument();
  });
});
