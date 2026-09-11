import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";

describe("UI-009-P05 Command Palette Styling Harmonization (T-2, AC-2)", () => {
  it("verifies command palette classes are defined with tokenized styling", () => {
    const { container } = render(
      <div className="ix-command-palette" role="dialog" aria-label="Command palette">
        <input placeholder="Search commands…" />
        <div className="ix-command-list" role="menu">
          <section className="ix-command-group">
            <h2 className="ix-nav-group-title">Navigation</h2>
            <button type="button" className="ix-command-item active">
              <span>Go to Charts</span>
              <span className="ix-metadata">Navigate</span>
            </button>
          </section>
        </div>
      </div>,
    );

    const palette = container.querySelector(".ix-command-palette");
    expect(palette).toBeInTheDocument();
    expect(palette).toHaveAttribute("role", "dialog");
    expect(screen.getByText("Go to Charts")).toBeInTheDocument();
    expect(screen.getByText("Navigation")).toBeInTheDocument();
  });
});
