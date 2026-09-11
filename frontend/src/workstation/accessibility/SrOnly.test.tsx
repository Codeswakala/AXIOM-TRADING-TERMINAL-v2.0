import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { SrOnly } from "./SrOnly";

describe("SrOnly Utility Component (UI-010-P05 / T-2, AC-2)", () => {
  it("renders screen-reader text with ix-sr-only class", () => {
    render(<SrOnly>Screen reader accessible instruction</SrOnly>);

    const element = screen.getByText("Screen reader accessible instruction");
    expect(element).toBeInTheDocument();
    expect(element).toHaveClass("ix-sr-only");
    expect(element).toHaveAttribute("data-ui010-component", "sr-only");
  });

  it("supports rendering as different HTML elements", () => {
    const { container } = render(<SrOnly as="p">Paragraph SR text</SrOnly>);
    const paragraph = container.querySelector("p.ix-sr-only");
    expect(paragraph).toBeInTheDocument();
    expect(paragraph).toHaveTextContent("Paragraph SR text");
  });
});
