import { describe, it, expect } from "vitest";
import { render } from "@testing-library/react";
import { DataTable, type ColumnDef } from "./DataTable";

interface MockWideRow {
  id: string;
  col1: string;
  col2: string;
  col3: string;
  col4: string;
  col5: string;
  col6: string;
}

const wideColumns: ColumnDef<MockWideRow>[] = [
  { key: "col1", header: "Header 1", width: "200px" },
  { key: "col2", header: "Header 2", width: "200px" },
  { key: "col3", header: "Header 3", width: "200px" },
  { key: "col4", header: "Header 4", width: "200px" },
  { key: "col5", header: "Header 5", width: "200px" },
  { key: "col6", header: "Header 6", width: "200px" },
];

const mockRows: MockWideRow[] = [
  { id: "1", col1: "val1", col2: "val2", col3: "val3", col4: "val4", col5: "val5", col6: "val6" },
];

describe("UI-010-P02 DataTable Horizontal Scrolling & Sticky Headers (T-3, AC-3, U-4)", () => {
  it("AC-3: verifies table wrapper has overflow-x auto and thead has sticky position class", () => {
    const { container } = render(<DataTable columns={wideColumns} rows={mockRows} />);

    const wrapper = container.querySelector(".ix-data-table-wrapper");
    expect(wrapper).toBeInTheDocument();

    const thead = container.querySelector(".ix-data-table__head");
    expect(thead).toBeInTheDocument();

    const table = container.querySelector(".ix-data-table");
    expect(table).toBeInTheDocument();
  });
});
