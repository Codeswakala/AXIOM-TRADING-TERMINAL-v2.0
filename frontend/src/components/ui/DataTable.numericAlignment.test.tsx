import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { DataTable, type ColumnDef } from "./DataTable";

interface MockMetricRow {
  metricName: string;
  sampleCount: number;
  rValue: number;
  ciLower: number;
  ciUpper: number;
  status: string;
}

const metricColumns: ColumnDef<MockMetricRow>[] = [
  { key: "metricName", header: "Metric Name", align: "left" },
  { key: "sampleCount", header: "Sample Count (n)", align: "numeric" },
  { key: "rValue", header: "Pearson R", align: "numeric" },
  { key: "ciLower", header: "CI Lower", align: "numeric" },
  { key: "ciUpper", header: "CI Upper", align: "numeric" },
  { key: "status", header: "Status", align: "center" },
];

const metricRows: MockMetricRow[] = [
  { metricName: "Hurst Exponent", sampleCount: 120, rValue: 0.68, ciLower: 0.55, ciUpper: 0.78, status: "Verified" },
  { metricName: "Volatility Spread", sampleCount: 450, rValue: -0.42, ciLower: -0.58, ciUpper: -0.25, status: "Verified" },
];

describe("UI-009-P04 DataTable Monospace & Numeric Alignment (T-2, AC-2, U-8)", () => {
  it("applies numeric alignment and monospace tabular classes to numeric columns", () => {
    render(<DataTable columns={metricColumns} rows={metricRows} />);

    // Header cells alignment check
    const numericHeaders = ["column-header-sampleCount", "column-header-rValue", "column-header-ciLower", "column-header-ciUpper"];
    for (const testId of numericHeaders) {
      const th = screen.getByTestId(testId);
      expect(th.className).toContain("ix-data-table__th--numeric");
    }

    const leftTh = screen.getByTestId("column-header-metricName");
    expect(leftTh.className).toContain("ix-data-table__th--left");

    const centerTh = screen.getByTestId("column-header-status");
    expect(centerTh.className).toContain("ix-data-table__th--center");
  });

  it("applies numeric alignment classes to body cells of numeric columns", () => {
    const { container } = render(<DataTable columns={metricColumns} rows={metricRows} />);

    const numericCells = container.querySelectorAll(".ix-data-table__cell--numeric");
    // 2 rows * 4 numeric columns = 8 numeric cells
    expect(numericCells.length).toBe(8);

    const leftCells = container.querySelectorAll(".ix-data-table__cell--left");
    // 2 rows * 1 left column = 2 left cells
    expect(leftCells.length).toBe(2);

    const centerCells = container.querySelectorAll(".ix-data-table__cell--center");
    // 2 rows * 1 center column = 2 center cells
    expect(centerCells.length).toBe(2);
  });
});
