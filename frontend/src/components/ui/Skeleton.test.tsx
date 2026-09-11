import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { Skeleton } from "./Skeleton";

describe("UI-009-P05 Skeleton Component (T-3, AC-3)", () => {
  it("renders text skeleton with aria-busy and loading role", () => {
    render(<Skeleton variant="text" />);

    const skeleton = screen.getByRole("status");
    expect(skeleton).toBeInTheDocument();
    expect(skeleton).toHaveAttribute("aria-busy", "true");
    expect(skeleton).toHaveAttribute("aria-label", "Loading");
    expect(skeleton.className).toContain("ix-skeleton--text");
  });

  it("handles rectangular and circular variants", () => {
    const { rerender } = render(<Skeleton variant="rect" width="100%" height="80px" />);
    let skeleton = screen.getByRole("status");
    expect(skeleton.className).toContain("ix-skeleton--rect");
    expect(skeleton.style.width).toBe("100%");
    expect(skeleton.style.height).toBe("80px");

    rerender(<Skeleton variant="circle" width="48px" height="48px" />);
    skeleton = screen.getByRole("status");
    expect(skeleton.className).toContain("ix-skeleton--circle");
  });

  it("renders multiple skeleton items when count > 1", () => {
    render(<Skeleton variant="text" count={4} />);

    const group = screen.getByRole("status");
    expect(group.className).toContain("ix-skeleton-group");
    const items = screen.getAllByTestId("skeleton-item");
    expect(items).toHaveLength(4);
  });

  it("returns null when count is 0 or negative", () => {
    const { container } = render(<Skeleton count={0} />);
    expect(container.firstChild).toBeNull();
  });
});
