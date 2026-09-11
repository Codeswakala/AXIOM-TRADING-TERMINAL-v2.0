import { describe, it, expect } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { SkipLink } from "./SkipLink";

describe("UI-010-P01 SkipLink Component (T-1, AC-1)", () => {
  it("renders with href='#main-content' and accessible aria-label", () => {
    render(<SkipLink />);

    const link = screen.getByRole("link", { name: "Skip to main content" });
    expect(link).toBeInTheDocument();
    expect(link).toHaveAttribute("href", "#main-content");
    expect(link).toHaveAttribute("data-ui010-component", "skip-link");
    expect(link.className).toContain("ix-skip-link");
  });

  it("focuses target element when clicked", () => {
    render(
      <div>
        <SkipLink targetId="main-content" />
        <main id="main-content" tabIndex={-1}>
          <h1>Primary Workspace</h1>
        </main>
      </div>,
    );

    const link = screen.getByRole("link", { name: "Skip to main content" });
    const mainEl = screen.getByRole("main");

    fireEvent.click(link);
    expect(document.activeElement).toBe(mainEl);
  });

  it("supports custom targetId and custom child label", () => {
    render(
      <div>
        <SkipLink targetId="custom-content">Bypass to Custom Workspace</SkipLink>
        <section id="custom-content" aria-label="Custom Content Region" tabIndex={-1}>
          <h1>Custom Content</h1>
        </section>
      </div>,
    );

    const link = screen.getByRole("link", { name: "Skip to main content" });
    expect(link).toHaveAttribute("href", "#custom-content");
    expect(link).toHaveTextContent("Bypass to Custom Workspace");

    const customSection = screen.getByRole("region", { name: "Custom Content Region" });
    fireEvent.click(link);
    expect(document.activeElement).toBe(customSection);
  });
});
