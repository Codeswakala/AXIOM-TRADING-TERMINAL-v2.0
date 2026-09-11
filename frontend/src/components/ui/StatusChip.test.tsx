import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { StatusChip } from "./StatusChip";

describe("UI-009-P02 StatusChip Component (T-6, AC-6)", () => {
  it("renders status level, geometric icon, and formatted percentage value", () => {
    render(<StatusChip level="HIGH" value={0.92} label="HIGH CONFIDENCE" />);
    const chip = screen.getByRole("status");
    expect(chip).toBeInTheDocument();
    expect(chip).toHaveTextContent("◆◆◆");
    expect(chip).toHaveTextContent("HIGH CONFIDENCE");
    expect(chip).toHaveTextContent("(92.0%)");
  });

  it("handles different levels correctly", () => {
    const { rerender } = render(<StatusChip level="MODERATE" value="MODERATE" />);
    expect(screen.getByRole("status")).toHaveTextContent("◆◆◇");

    rerender(<StatusChip level="LIMITED" />);
    expect(screen.getByRole("status")).toHaveTextContent("◆◇◇");

    rerender(<StatusChip level="UNCALIBRATED" />);
    expect(screen.getByRole("status")).toHaveTextContent("◇◇◇");
  });
});
