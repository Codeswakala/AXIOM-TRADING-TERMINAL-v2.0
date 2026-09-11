import { describe, it, expect } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { Accordion } from "./Accordion";

describe("UI-009-P02 Accordion Component (T-8, AC-8)", () => {
  const items = [
    { id: "sec-1", title: "Section 1", content: "Content of section 1", defaultExpanded: true },
    { id: "sec-2", title: "Section 2", content: "Content of section 2" },
  ];

  it("renders default expanded section and toggles expansion on click", () => {
    render(<Accordion items={items} />);

    expect(screen.getByTestId("accordion-panel-sec-1")).toHaveTextContent("Content of section 1");
    expect(screen.queryByTestId("accordion-panel-sec-2")).not.toBeInTheDocument();

    const trigger2 = screen.getByTestId("accordion-trigger-sec-2");
    fireEvent.click(trigger2);

    expect(screen.getByTestId("accordion-panel-sec-2")).toHaveTextContent("Content of section 2");
    expect(screen.queryByTestId("accordion-panel-sec-1")).not.toBeInTheDocument(); // single mode
  });

  it("supports multiple expanded sections when allowMultiple=true", () => {
    render(<Accordion items={items} allowMultiple />);

    const trigger2 = screen.getByTestId("accordion-trigger-sec-2");
    fireEvent.click(trigger2);

    expect(screen.getByTestId("accordion-panel-sec-1")).toBeInTheDocument();
    expect(screen.getByTestId("accordion-panel-sec-2")).toBeInTheDocument();
  });
});
