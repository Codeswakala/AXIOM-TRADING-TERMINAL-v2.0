import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { Input } from "./Input";

describe("UI-009-P02 Input Component (T-2, AC-2)", () => {
  it("renders input with label and helper text", () => {
    render(<Input label="Search Query" helperText="Enter keyword to search documentation" />);
    expect(screen.getByLabelText("Search Query")).toBeInTheDocument();
    expect(screen.getByTestId("input-helper-msg")).toHaveTextContent("Enter keyword to search documentation");
  });

  it("handles error state and sets aria-invalid and error message", () => {
    render(<Input label="Security Token" error="Invalid format" />);
    const input = screen.getByLabelText("Security Token");
    expect(input.getAttribute("aria-invalid")).toBe("true");
    expect(screen.getByTestId("input-error-msg")).toHaveTextContent("Invalid format");
  });

  it("triggers onChange handler when value changes", () => {
    const handleChange = vi.fn();
    render(<Input label="Symbol" onChange={handleChange} />);
    const input = screen.getByLabelText("Symbol");
    fireEvent.change(input, { target: { value: "EURUSD" } });
    expect(handleChange).toHaveBeenCalled();
  });

  it("handles loading spinner state", () => {
    render(<Input label="Loading Field" loading />);
    expect(screen.getByTestId("input-spinner")).toBeInTheDocument();
    expect(screen.getByLabelText("Loading Field")).toBeDisabled();
  });
});
