import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { Pagination } from "./Pagination";

describe("UI-009-P04 Pagination Component (T-4, AC-4)", () => {
  it("renders page info, range text, and buttons", () => {
    const handlePageChange = vi.fn();
    render(
      <Pagination
        page={2}
        pageSize={25}
        totalRows={120}
        onPageChange={handlePageChange}
      />,
    );

    expect(screen.getByRole("navigation", { name: "Pagination Navigation" })).toBeInTheDocument();
    expect(screen.getByTestId("pagination-info")).toHaveTextContent("Showing 26–50 of 120");
    expect(screen.getByTestId("pagination-info")).toHaveTextContent("Page 2 of 5");
  });

  it("disables first and previous buttons on page 1 (boundary protection)", () => {
    const handlePageChange = vi.fn();
    render(
      <Pagination
        page={1}
        pageSize={10}
        totalRows={50}
        onPageChange={handlePageChange}
      />,
    );

    expect(screen.getByTestId("pagination-first")).toBeDisabled();
    expect(screen.getByTestId("pagination-prev")).toBeDisabled();
    expect(screen.getByTestId("pagination-next")).not.toBeDisabled();
    expect(screen.getByTestId("pagination-last")).not.toBeDisabled();
  });

  it("disables next and last buttons on last page (boundary protection)", () => {
    const handlePageChange = vi.fn();
    render(
      <Pagination
        page={5}
        pageSize={10}
        totalRows={50}
        onPageChange={handlePageChange}
      />,
    );

    expect(screen.getByTestId("pagination-first")).not.toBeDisabled();
    expect(screen.getByTestId("pagination-prev")).not.toBeDisabled();
    expect(screen.getByTestId("pagination-next")).toBeDisabled();
    expect(screen.getByTestId("pagination-last")).toBeDisabled();
  });

  it("triggers onPageChange with correct page numbers", () => {
    const handlePageChange = vi.fn();
    render(
      <Pagination
        page={2}
        pageSize={10}
        totalRows={50}
        onPageChange={handlePageChange}
      />,
    );

    // Next
    fireEvent.click(screen.getByTestId("pagination-next"));
    expect(handlePageChange).toHaveBeenCalledWith(3);

    // Prev
    fireEvent.click(screen.getByTestId("pagination-prev"));
    expect(handlePageChange).toHaveBeenCalledWith(1);

    // Last
    fireEvent.click(screen.getByTestId("pagination-last"));
    expect(handlePageChange).toHaveBeenCalledWith(5);

    // First
    fireEvent.click(screen.getByTestId("pagination-first"));
    expect(handlePageChange).toHaveBeenCalledWith(1);
  });

  it("triggers onPageSizeChange when page size dropdown changes", () => {
    const handlePageChange = vi.fn();
    const handlePageSizeChange = vi.fn();
    render(
      <Pagination
        page={1}
        pageSize={10}
        totalRows={100}
        onPageChange={handlePageChange}
        onPageSizeChange={handlePageSizeChange}
        pageSizeOptions={[10, 25, 50]}
      />,
    );

    const select = screen.getByTestId("pagination-page-size-select");
    fireEvent.change(select, { target: { value: "25" } });

    expect(handlePageSizeChange).toHaveBeenCalledWith(25);
  });
});
