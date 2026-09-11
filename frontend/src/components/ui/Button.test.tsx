import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { Button } from "./Button";

describe("UI-009-P02 Button Component (T-1, AC-1)", () => {
  it("renders with default props and text content", () => {
    render(<Button>Submit Order Analysis</Button>);
    const btn = screen.getByRole("button", { name: /Submit Order Analysis/i });
    expect(btn).toBeInTheDocument();
    expect(btn.getAttribute("data-variant")).toBe("primary");
    expect(btn.getAttribute("data-size")).toBe("md");
    expect(btn.getAttribute("type")).toBe("button");
  });

  it("handles variants and sizes correctly", () => {
    const { rerender } = render(<Button variant="secondary" size="sm">Secondary SM</Button>);
    let btn = screen.getByRole("button");
    expect(btn.getAttribute("data-variant")).toBe("secondary");
    expect(btn.getAttribute("data-size")).toBe("sm");

    rerender(<Button variant="destructive" size="lg">Destructive LG</Button>);
    btn = screen.getByRole("button");
    expect(btn.getAttribute("data-variant")).toBe("destructive");
    expect(btn.getAttribute("data-size")).toBe("lg");

    rerender(<Button variant="ghost">Ghost</Button>);
    btn = screen.getByRole("button");
    expect(btn.getAttribute("data-variant")).toBe("ghost");
  });

  it("handles loading state and sets aria-busy (AC-1)", () => {
    render(<Button loading>Processing</Button>);
    const btn = screen.getByRole("button");
    expect(btn).toBeDisabled();
    expect(btn.getAttribute("aria-busy")).toBe("true");
    expect(screen.getByTestId("button-spinner")).toBeInTheDocument();
  });

  it("triggers onClick when not disabled", () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click Me</Button>);
    fireEvent.click(screen.getByRole("button"));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it("does not trigger onClick when disabled", () => {
    const handleClick = vi.fn();
    render(<Button disabled onClick={handleClick}>Disabled</Button>);
    const btn = screen.getByRole("button");
    expect(btn).toBeDisabled();
    fireEvent.click(btn);
    expect(handleClick).not.toHaveBeenCalled();
  });
});
