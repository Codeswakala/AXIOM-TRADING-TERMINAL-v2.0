import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import {
  TYPOGRAPHY_SCALE,
  TYPOGRAPHY_TOKENS,
  computeContrastRatio,
} from "./theme";
import {
  DataTable,
  formatPips,
  formatPercent,
  formatPearsonR,
  type ColumnDef,
} from "../../components/ui";

describe("Optical Typography & Monospace Financial Data Polish (UI-011-P04 / T-1, T-2, AC-1, AC-2, AC-3)", () => {
  it("AC-1: verifies typography scale tokens and optical hierarchy contracts in theme", () => {
    expect(TYPOGRAPHY_TOKENS.fontSizeDisplay).toBe("var(--ix-font-size-display)");
    expect(TYPOGRAPHY_TOKENS.fontSizeWorkspaceTitle).toBe("var(--ix-font-size-workspace-title)");
    expect(TYPOGRAPHY_TOKENS.fontSizeSectionHeading).toBe("var(--ix-font-size-section-heading)");
    expect(TYPOGRAPHY_TOKENS.fontSizePanelHeading).toBe("var(--ix-font-size-panel-heading)");
    expect(TYPOGRAPHY_TOKENS.fontSizeBody).toBe("var(--ix-font-size-body)");
    expect(TYPOGRAPHY_TOKENS.fontSizeMetadata).toBe("var(--ix-font-size-metadata)");
    expect(TYPOGRAPHY_TOKENS.fontMono).toBe("var(--ix-font-mono)");
    expect(TYPOGRAPHY_TOKENS.fontSans).toBe("var(--ix-font-sans)");

    expect(TYPOGRAPHY_SCALE.displayTitle).toBe("var(--ix-type-display-title)");
    expect(TYPOGRAPHY_SCALE.workspaceTitle).toBe("var(--ix-type-workspace-title)");
    expect(TYPOGRAPHY_SCALE.sectionHeading).toBe("var(--ix-type-section-heading)");
    expect(TYPOGRAPHY_SCALE.panelHeading).toBe("var(--ix-type-panel-heading)");
    expect(TYPOGRAPHY_SCALE.body).toBe("var(--ix-type-body)");
    expect(TYPOGRAPHY_SCALE.metadata).toBe("var(--ix-type-metadata)");
  });

  it("AC-2: verifies monospace tabular-nums alignment on financial data columns in DataTable", () => {
    interface FinancialDataRow {
      symbol: string;
      price: string;
      spread: string;
      pips: string;
      confidence: string;
    }

    const columns: ColumnDef<FinancialDataRow>[] = [
      { key: "symbol", header: "Instrument", align: "left" },
      { key: "price", header: "Price", align: "numeric" },
      { key: "spread", header: "Spread", align: "numeric" },
      { key: "pips", header: "Pips", align: "numeric" },
      { key: "confidence", header: "Confidence", align: "numeric" },
    ];

    const rows: FinancialDataRow[] = [
      {
        symbol: "EUR/USD",
        price: "1.08450",
        spread: "0.8",
        pips: formatPips(14.2),
        confidence: formatPercent(87.5),
      },
    ];

    render(<DataTable columns={columns} rows={rows} />);

    const priceHeader = screen.getByTestId("column-header-price");
    expect(priceHeader).toHaveClass("ix-data-table__th--numeric");

    const priceCell = screen.getByText("1.08450");
    expect(priceCell).toHaveClass("ix-data-table__cell--numeric");

    const spreadCell = screen.getByText("0.8");
    expect(spreadCell).toHaveClass("ix-data-table__cell--numeric");

    const pipsCell = screen.getByText("+14.2 pips");
    expect(pipsCell).toHaveClass("ix-data-table__cell--numeric");

    const confidenceCell = screen.getByText("87.5%");
    expect(confidenceCell).toHaveClass("ix-data-table__cell--numeric");
  });

  it("AC-2: formats financial statistical metrics deterministically for monospace presentation", () => {
    expect(formatPips(22.4)).toBe("+22.4 pips");
    expect(formatPips(-10.1)).toBe("-10.1 pips");
    expect(formatPercent(94.2)).toBe("94.2%");
    expect(formatPearsonR(0.88)).toBe("r=0.88");
  });

  it("AC-3: validates optical label/value contrast ratios across dark surface hierarchies", () => {
    const surfaceBg = "#111822"; // --ix-bg-surface
    const rootBg = "#0B0E14";    // --ix-bg-root
    const metadataText = "#94A3B8"; // --ix-text-muted (0.75rem label)
    const primaryValue = "#EEF4FC";  // --ix-text-primary (0.9rem value)

    const labelContrast = computeContrastRatio(metadataText, surfaceBg);
    const valueContrast = computeContrastRatio(primaryValue, surfaceBg);

    // Optical separation: label is muted but meets WCAG 2.1 AA (>4.5:1), value is high luminance (>12:1)
    expect(labelContrast).toBeGreaterThan(5.0);
    expect(valueContrast).toBeGreaterThan(12.0);
    expect(valueContrast).toBeGreaterThan(labelContrast);

    // Root background verification
    const rootLabelContrast = computeContrastRatio(metadataText, rootBg);
    const rootValueContrast = computeContrastRatio(primaryValue, rootBg);
    expect(rootLabelContrast).toBeGreaterThan(6.0);
    expect(rootValueContrast).toBeGreaterThan(14.0);
  });
});
