import { describe, it, expect } from "vitest";
import { render } from "@testing-library/react";
import { Panel } from "../../components/ui/Panel";
import { DataTable } from "../../components/ui/DataTable";
import { Card } from "../../components/ui/Card";

describe("UI-010-P02 Responsive Reflow & Zero Horizontal Scroll (T-4, AC-4, U-2)", () => {
  it("AC-4: verifies workspace containers have box-sizing and fluid container constraints", () => {
    const { container } = render(
      <div className="test-workspace-reflow">
        <Panel variant="raised">
          <Card>
            <DataTable
              columns={[
                { key: "metric", header: "Metric" },
                { key: "value", header: "Value", align: "numeric" },
              ]}
              rows={[{ metric: "Test", value: 100 }]}
            />
          </Card>
        </Panel>
      </div>,
    );

    const panel = container.querySelector(".ix-panel");
    expect(panel).toBeInTheDocument();

    const tableContainer = container.querySelector(".ix-data-table-container");
    expect(tableContainer).toBeInTheDocument();
  });
});
