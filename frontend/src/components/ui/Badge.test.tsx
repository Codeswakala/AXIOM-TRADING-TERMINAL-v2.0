import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { Badge } from "./Badge";

describe("UI-009-P02 Badge Component (T-4, AC-4)", () => {
  it("renders text label and variant classes (never color alone)", () => {
    render(<Badge label="GATE CLOSED" variant="critical" />);
    const badge = screen.getByText("GATE CLOSED").closest(".ix-badge");
    expect(badge).toBeInTheDocument();
    expect(badge?.getAttribute("data-variant")).toBe("critical");
    expect(badge?.getAttribute("data-ui009-component")).toBe("badge");
  });

  it("renders icon when supplied", () => {
    render(<Badge label="Verified" variant="success" icon={<span data-testid="test-icon">✓</span>} />);
    expect(screen.getByTestId("test-icon")).toBeInTheDocument();
    expect(screen.getByText("Verified")).toBeInTheDocument();
  });
});
