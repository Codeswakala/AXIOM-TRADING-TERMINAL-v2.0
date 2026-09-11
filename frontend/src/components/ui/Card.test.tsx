import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { Card } from "./Card";

describe("UI-009-P02 Card Component (T-5, AC-5)", () => {
  it("renders header, body, and footer slots", () => {
    render(
      <Card
        header={<h3>Card Title</h3>}
        footer={<small>Card Footer</small>}
      >
        <p>Card Body Content</p>
      </Card>,
    );

    expect(screen.getByTestId("card-header")).toHaveTextContent("Card Title");
    expect(screen.getByTestId("card-body")).toHaveTextContent("Card Body Content");
    expect(screen.getByTestId("card-footer")).toHaveTextContent("Card Footer");
  });

  it("handles interactive variant and click events", () => {
    const handleClick = vi.fn();
    render(<Card variant="interactive" onClick={handleClick}>Interactive Card</Card>);
    const card = screen.getByText("Interactive Card").closest(".ix-card");
    expect(card).toHaveAttribute("role", "button");

    fireEvent.click(card!);
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
