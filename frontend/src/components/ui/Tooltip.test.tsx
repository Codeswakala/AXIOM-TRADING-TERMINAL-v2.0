import { describe, it, expect } from "vitest";
import { render, screen, fireEvent, act } from "@testing-library/react";
import { Tooltip } from "./Tooltip";

describe("UI-009-P02 Tooltip Component (T-7, AC-7)", () => {
  it("renders trigger and shows tooltip on focus / hover", async () => {
    render(
      <Tooltip content="Tooltip explanation text" delay={0}>
        <button type="button">Hover Target</button>
      </Tooltip>,
    );

    const btn = screen.getByText("Hover Target");
    expect(screen.queryByRole("tooltip")).not.toBeInTheDocument();

    act(() => {
      fireEvent.focus(btn);
    });

    const tooltip = await screen.findByRole("tooltip");
    expect(tooltip).toBeInTheDocument();
    expect(tooltip).toHaveTextContent("Tooltip explanation text");
  });

  it("dismisses tooltip on Escape key press", async () => {
    render(
      <Tooltip content="Tooltip to dismiss" delay={0}>
        <button type="button">Target</button>
      </Tooltip>,
    );

    const btn = screen.getByText("Target");
    act(() => {
      fireEvent.focus(btn);
    });

    const tooltip = await screen.findByRole("tooltip");
    expect(tooltip).toBeInTheDocument();

    const container = screen.getByText("Target").closest(".ix-tooltip-container")!;
    act(() => {
      fireEvent.keyDown(container, { key: "Escape", code: "Escape" });
    });

    expect(screen.queryByRole("tooltip")).not.toBeInTheDocument();
  });
});
