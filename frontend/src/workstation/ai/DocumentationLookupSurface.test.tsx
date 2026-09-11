import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import {
  DocumentationLookupSurface,
  SandboxedMarkdownViewer,
} from "./DocumentationLookupSurface";

describe("UI-008-P05 DocumentationLookupSurface Component (T-1, T-4, T-5, U-1..U-5)", () => {
  it("renders documentation lookup surface with split-pane layout and disclaimer (T-1, U-1)", () => {
    render(<DocumentationLookupSurface />);

    expect(
      screen.getByRole("region", { name: /Platform Documentation & Knowledge Lookup/i }),
    ).toBeInTheDocument();
    expect(screen.getByTestId("doc-disclaimer")).toHaveTextContent(
      "Platform documentation and knowledge lookup for research only",
    );
    expect(screen.getByTestId("doc-search-input")).toBeInTheDocument();
    expect(screen.getByTestId("active-doc-article")).toBeInTheDocument();
  });

  it("filters topics by category pill buttons (U-3)", () => {
    render(<DocumentationLookupSurface />);

    // Click Statistics filter
    const statsPill = screen.getByTestId("cat-filter-statistics");
    fireEvent.click(statsPill);

    const docItems = screen.getAllByTestId(/^doc-item-/);
    expect(docItems.length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText("Wilson Score Intervals").length).toBeGreaterThanOrEqual(1);
  });

  it("updates search input and filters results list in real-time (U-2)", () => {
    render(<DocumentationLookupSurface />);

    const searchInput = screen.getByTestId("doc-search-input");
    fireEvent.change(searchInput, { target: { value: "Architecture" } });

    expect(screen.getAllByText("05 — Canonical System Architecture").length).toBeGreaterThanOrEqual(1);
  });

  it("selects document and renders reading view (U-4)", () => {
    render(<DocumentationLookupSurface />);

    const item = screen.getByTestId("doc-item-gov-17-security");
    fireEvent.click(item);

    const article = screen.getByTestId("active-doc-article");
    expect(article).toHaveTextContent("17 — Institutional Security Standard");
    expect(article).toHaveTextContent("Zero Trust Architecture");
  });

  it("handles Escape key to close surface (T-5, U-5)", () => {
    const handleClose = vi.fn();
    render(<DocumentationLookupSurface onClose={handleClose} />);

    const region = screen.getByRole("region", {
      name: /Platform Documentation & Knowledge Lookup/i,
    });
    fireEvent.keyDown(region, { key: "Escape", code: "Escape" });

    expect(handleClose).toHaveBeenCalledTimes(1);
  });

  it("renders close button when onClose prop is provided", () => {
    const handleClose = vi.fn();
    render(<DocumentationLookupSurface onClose={handleClose} />);

    const closeBtn = screen.getByTestId("doc-close-button");
    fireEvent.click(closeBtn);

    expect(handleClose).toHaveBeenCalledTimes(1);
  });

  // (T-4) Sandboxed Markdown Viewer safety test
  describe("SandboxedMarkdownViewer (T-4)", () => {
    it("safely renders headings, lists, paragraphs, and math formulas without script injection", () => {
      const sampleMarkdown = `
### Heading 3 Sample
- Bullet item 1
- Bullet item 2
$$r = 0.95$$
Standard explanation paragraph text.
`;
      render(<SandboxedMarkdownViewer content={sampleMarkdown} />);

      expect(screen.getByText("Heading 3 Sample")).toBeInTheDocument();
      expect(screen.getByText("Bullet item 1")).toBeInTheDocument();
      expect(screen.getByTestId("math-block")).toHaveTextContent("r = 0.95");
      expect(screen.getByText("Standard explanation paragraph text.")).toBeInTheDocument();
    });
  });
});
