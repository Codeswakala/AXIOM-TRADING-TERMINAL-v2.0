import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { SortableHeader } from "./SortableHeader";

describe("UI-009-P04 SortableHeader Component (T-3, AC-3, U-3)", () => {
  it("renders unsorted header with correct aria-sort and neutral icon indicator", () => {
    const handleSort = vi.fn();
    render(
      <SortableHeader
        columnKey="symbol"
        header="Asset Symbol"
        sorted={false}
        onSort={handleSort}
      />,
    );

    const btn = screen.getByRole("button", { name: /Asset Symbol/i });
    expect(btn).toBeInTheDocument();
    expect(btn).toHaveAttribute("data-sorted", "false");
    expect(btn).toHaveAttribute("data-direction", "none");
    expect(screen.getByTestId("sort-indicator")).toHaveTextContent("↕");

    fireEvent.click(btn);
    expect(handleSort).toHaveBeenCalledTimes(1);
    expect(handleSort).toHaveBeenCalledWith("symbol", "asc");
  });

  it("renders ascending sorted header and toggles to descending on click", () => {
    const handleSort = vi.fn();
    render(
      <SortableHeader
        columnKey="price"
        header="Market Price"
        sorted={true}
        sortDirection="asc"
        onSort={handleSort}
      />,
    );

    const btn = screen.getByRole("button", { name: /Market Price/i });
    expect(btn).toHaveAttribute("data-sorted", "true");
    expect(btn).toHaveAttribute("data-direction", "asc");
    expect(screen.getByTestId("sort-indicator")).toHaveTextContent("↑");

    fireEvent.click(btn);
    expect(handleSort).toHaveBeenCalledTimes(1);
    expect(handleSort).toHaveBeenCalledWith("price", "desc");
  });

  it("renders descending sorted header and toggles to ascending on click", () => {
    const handleSort = vi.fn();
    render(
      <SortableHeader
        columnKey="price"
        header="Market Price"
        sorted={true}
        sortDirection="desc"
        onSort={handleSort}
      />,
    );

    const btn = screen.getByRole("button", { name: /Market Price/i });
    expect(btn).toHaveAttribute("data-direction", "desc");
    expect(screen.getByTestId("sort-indicator")).toHaveTextContent("↓");

    fireEvent.click(btn);
    expect(handleSort).toHaveBeenCalledWith("price", "asc");
  });

  it("supports keyboard toggling via Enter and Space keys", () => {
    const handleSort = vi.fn();
    render(
      <SortableHeader
        columnKey="timestamp"
        header="Event Time"
        sorted={false}
        onSort={handleSort}
      />,
    );

    const btn = screen.getByRole("button", { name: /Event Time/i });

    // Enter key
    fireEvent.keyDown(btn, { key: "Enter" });
    expect(handleSort).toHaveBeenCalledWith("timestamp", "asc");

    // Space key
    fireEvent.keyDown(btn, { key: " " });
    expect(handleSort).toHaveBeenCalledWith("timestamp", "asc");
  });
});
