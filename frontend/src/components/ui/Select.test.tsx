import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { Select } from "./Select";

describe("UI-009-P02 Select Component (T-3, AC-3)", () => {
  const options = [
    { value: "1H", label: "1 Hour" },
    { value: "4H", label: "4 Hours" },
    { value: "1D", label: "1 Day" },
  ];

  it("renders select trigger with placeholder or selected label", () => {
    render(<Select label="Timeframe" options={options} value="4H" />);
    expect(screen.getByTestId("select-trigger")).toHaveTextContent("4 Hours");
  });

  it("opens dropdown listbox on click (AC-3)", () => {
    render(<Select label="Timeframe" options={options} value="1H" />);
    const trigger = screen.getByTestId("select-trigger");

    expect(screen.queryByTestId("select-dropdown")).not.toBeInTheDocument();
    fireEvent.click(trigger);

    expect(screen.getByTestId("select-dropdown")).toBeInTheDocument();
    expect(screen.getAllByRole("option")).toHaveLength(3);
  });

  it("selects option and triggers onChange", () => {
    const handleChange = vi.fn();
    render(<Select label="Timeframe" options={options} onChange={handleChange} />);
    const trigger = screen.getByTestId("select-trigger");

    fireEvent.click(trigger);
    const opt = screen.getByTestId("select-option-1D");
    fireEvent.click(opt);

    expect(handleChange).toHaveBeenCalledWith("1D");
    expect(screen.queryByTestId("select-dropdown")).not.toBeInTheDocument();
  });

  it("handles keyboard navigation (ArrowDown, Enter, Escape)", () => {
    const handleChange = vi.fn();
    render(<Select label="Timeframe" options={options} onChange={handleChange} />);
    const trigger = screen.getByTestId("select-trigger");

    // Press ArrowDown to open
    fireEvent.keyDown(trigger, { key: "ArrowDown", code: "ArrowDown" });
    expect(screen.getByTestId("select-dropdown")).toBeInTheDocument();

    // Press Escape to close
    fireEvent.keyDown(trigger, { key: "Escape", code: "Escape" });
    expect(screen.queryByTestId("select-dropdown")).not.toBeInTheDocument();
  });
});
