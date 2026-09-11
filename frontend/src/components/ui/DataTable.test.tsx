import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { DataTable, type ColumnDef } from "./DataTable";

interface MockTelemetryRow {
  id: string;
  symbol: string;
  price: number;
  changePct: number;
  status: string;
}

const mockColumns: ColumnDef<MockTelemetryRow>[] = [
  { key: "symbol", header: "Symbol", sortable: true, align: "left" },
  { key: "price", header: "Price", sortable: true, align: "numeric" },
  { key: "changePct", header: "Change %", align: "numeric", render: (val) => `${val > 0 ? "+" : ""}${val}%` },
  { key: "status", header: "Status", align: "center" },
];

const mockRows: MockTelemetryRow[] = [
  { id: "1", symbol: "EURUSD", price: 1.0854, changePct: 0.15, status: "Active" },
  { id: "2", symbol: "GBPUSD", price: 1.2642, changePct: -0.22, status: "Active" },
  { id: "3", symbol: "USDJPY", price: 154.20, changePct: 0.05, status: "Idle" },
];

describe("UI-009-P04 DataTable Component (T-1, AC-1)", () => {
  it("renders columns, headers, and rows correctly", () => {
    render(<DataTable columns={mockColumns} rows={mockRows} ariaLabel="Market Telemetry Table" />);

    expect(screen.getByRole("table", { name: "Market Telemetry Table" })).toBeInTheDocument();
    expect(screen.getByText("EURUSD")).toBeInTheDocument();
    expect(screen.getByText("GBPUSD")).toBeInTheDocument();
    expect(screen.getByText("USDJPY")).toBeInTheDocument();
    expect(screen.getByText("+0.15%")).toBeInTheDocument();
    expect(screen.getByText("-0.22%")).toBeInTheDocument();
  });

  it("renders empty state with role='status' when rows array is empty", () => {
    render(
      <DataTable
        columns={mockColumns}
        rows={[]}
        emptyText="No historical telemetry records found"
        emptyIcon={<span data-testid="empty-icon">📭</span>}
      />,
    );

    const emptyState = screen.getByTestId("table-empty-state");
    expect(emptyState).toHaveAttribute("role", "status");
    expect(emptyState).toHaveTextContent("No historical telemetry records found");
    expect(screen.getByTestId("empty-icon")).toBeInTheDocument();
  });

  it("renders skeleton placeholder rows with aria-busy='true' when loading", () => {
    render(
      <DataTable
        columns={mockColumns}
        rows={mockRows}
        loading={true}
        skeletonRowCount={3}
      />,
    );

    const table = screen.getByRole("table");
    expect(table).toHaveAttribute("aria-busy", "true");
    const skeletonRows = screen.getAllByTestId("table-skeleton-row");
    expect(skeletonRows).toHaveLength(3);
    // Rows should not be rendered while loading
    expect(screen.queryByText("EURUSD")).not.toBeInTheDocument();
  });

  it("handles row click events when onRowClick is provided", () => {
    const handleRowClick = vi.fn();
    render(<DataTable columns={mockColumns} rows={mockRows} onRowClick={handleRowClick} />);

    const row1 = screen.getByTestId("table-row-1");
    fireEvent.click(row1);

    expect(handleRowClick).toHaveBeenCalledTimes(1);
    expect(handleRowClick).toHaveBeenCalledWith(mockRows[0]);
  });

  it("integrates pagination component when pagination prop is supplied", () => {
    const handlePageChange = vi.fn();
    render(
      <DataTable
        columns={mockColumns}
        rows={mockRows}
        pagination={{
          page: 2,
          pageSize: 3,
          totalRows: 10,
          onPageChange: handlePageChange,
        }}
      />,
    );

    expect(screen.getByRole("navigation", { name: "Pagination Navigation" })).toBeInTheDocument();
    expect(screen.getByText(/Page/)).toBeInTheDocument();
  });
});
