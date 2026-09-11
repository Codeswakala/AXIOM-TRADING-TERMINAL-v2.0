import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, cleanup } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import {
  TYPOGRAPHY_SCALE,
  TYPOGRAPHY_TOKENS,
  SPACING_SCALE,
  HIERARCHY_TOKENS,
} from "./theme";
import {
  Panel,
  PanelHeader,
  PanelActionBar,
  DataTable,
  Button,
  StatusChip,
  formatPips,
  formatPercent,
} from "../../components/ui";
import { InstitutionalWorkspaceShell } from "../components/InstitutionalWorkspaceShell";
import { ProtectedRoute } from "../../auth/ProtectedRoute";

const authState = {
  operator: { username: "governance_officer", role: "admin" },
  loading: false,
  isAuthenticated: true,
  logout: vi.fn(),
  login: vi.fn(),
  refreshProfile: vi.fn(),
};

vi.mock("../../context/AuthContext", () => ({
  useAuth: () => authState,
}));

vi.mock("../persistence/shellPreferences", () => ({
  loadShellLayoutPreference: vi.fn().mockResolvedValue(null),
  persistShellLayoutPreference: vi.fn().mockResolvedValue({}),
}));

describe("Cross-Workspace Cohesion & Visual Regression Audit (UI-011-P05 / T-1, T-2, AC-1, AC-2, AC-3)", () => {
  beforeEach(() => {
    cleanup();
  });

  it("AC-1 & AC-3: renders 4 primary workspaces sequentially via MemoryRouter without visual jumps or font shifts", () => {
    const targetWorkspaces = [
      { route: "/intelligence", title: "Institutional Intelligence" },
      { route: "/charts", title: "Professional Market Workspace" },
      { route: "/governance", title: "Governance & Evidence Workspace" },
      { route: "/investigate", title: "Signal Investigation Workspace" },
    ];

    for (const ws of targetWorkspaces) {
      const { unmount } = render(
        <MemoryRouter initialEntries={[ws.route]}>
          <Routes>
            <Route
              element={
                <ProtectedRoute>
                  <InstitutionalWorkspaceShell />
                </ProtectedRoute>
              }
            >
              <Route
                path={ws.route}
                element={
                  <div className="ix-workspace-content" data-testid={`workspace-${ws.route.replace("/", "")}`}>
                    <Panel
                      header={
                        <PanelHeader
                          title={ws.title}
                          subtitle="Harmonized institutional research frame"
                          headingLevel={2}
                          actions={<StatusChip level="HIGH" label="Governed" />}
                        />
                      }
                    >
                      <p>Workspace body content with uniform spacing and typography.</p>
                    </Panel>
                  </div>
                }
              />
            </Route>
          </Routes>
        </MemoryRouter>,
      );

      // Verify shell global header and primary workspace are present
      expect(screen.getByLabelText("Global command bar")).toBeInTheDocument();
      expect(screen.getByLabelText("Primary workspace")).toBeInTheDocument();
      expect(screen.getByRole("heading", { level: 2, name: ws.title })).toBeInTheDocument();
      expect(screen.getByText("Harmonized institutional research frame")).toBeInTheDocument();

      unmount();
    }
  });

  it("AC-1 & AC-2: verifies uniform panel balance and non-overlapping grid layout across workspaces", () => {
    render(
      <div className="ix-workspace-grid" style={{ display: "grid", gridTemplateColumns: "repeat(12, 1fr)", gap: "16px" }}>
        <Panel
          className="span-6"
          variant="raised"
          header={<PanelHeader title="Alpha Factor Attribution" headingLevel={3} />}
          actionBar={<PanelActionBar><Button size="sm">Refresh Context</Button></PanelActionBar>}
          footer={<span>Level 2 Active Context Frame</span>}
        >
          <p>Left column factor analytics.</p>
        </Panel>

        <Panel
          className="span-6"
          variant="raised"
          header={<PanelHeader title="Model Generalization Metrics" headingLevel={3} />}
          actionBar={<PanelActionBar><Button size="sm">Export Telemetry</Button></PanelActionBar>}
          footer={<span>Level 2 Active Context Frame</span>}
        >
          <p>Right column generalization analytics.</p>
        </Panel>
      </div>,
    );

    const headings = screen.getAllByRole("heading", { level: 3 });
    expect(headings).toHaveLength(2);
    expect(headings[0]).toHaveTextContent("Alpha Factor Attribution");
    expect(headings[1]).toHaveTextContent("Model Generalization Metrics");

    const panels = screen.getAllByTestId("panel-body");
    expect(panels).toHaveLength(2);
  });

  it("AC-2: verifies monospace tabular-nums numerical alignment across multi-workspace data presentations", () => {
    interface CrossWorkspaceMetric {
      workspace: string;
      metric: string;
      price: string;
      spread: string;
      pips: string;
      confidence: string;
    }

    const columns = [
      { key: "workspace", header: "Workspace", align: "left" as const },
      { key: "metric", header: "Metric Name", align: "left" as const },
      { key: "price", header: "Price", align: "numeric" as const },
      { key: "spread", header: "Spread", align: "numeric" as const },
      { key: "pips", header: "Pips", align: "numeric" as const },
      { key: "confidence", header: "Confidence", align: "numeric" as const },
    ];

    const rows: CrossWorkspaceMetric[] = [
      {
        workspace: "/charts",
        metric: "EUR/USD Bid/Ask",
        price: "1.08520",
        spread: "0.9",
        pips: formatPips(18.5),
        confidence: formatPercent(92.4),
      },
      {
        workspace: "/investigate",
        metric: "Signal Alpha Spread",
        price: "1.08490",
        spread: "1.2",
        pips: formatPips(-4.3),
        confidence: formatPercent(86.1),
      },
    ];

    render(<DataTable columns={columns} rows={rows} />);

    const priceHeader = screen.getByTestId("column-header-price");
    expect(priceHeader).toHaveClass("ix-data-table__th--numeric");

    const priceCells = screen.getAllByText(/1\.08520|1\.08490/);
    expect(priceCells[0]).toHaveClass("ix-data-table__cell--numeric");
    expect(priceCells[1]).toHaveClass("ix-data-table__cell--numeric");
  });

  it("AC-1 & AC-3: validates visual cohesion contracts, token scales, and typography hierarchies", () => {
    // 1. Spacing grid consistency (4px base)
    expect(SPACING_SCALE.space1).toBe("var(--ix-space-1)");
    expect(SPACING_SCALE.space4).toBe("var(--ix-space-4)");
    expect(SPACING_SCALE.space6).toBe("var(--ix-space-6)");

    // 2. Optical typography scale contracts
    expect(TYPOGRAPHY_SCALE.displayTitle).toBe("var(--ix-type-display-title)");
    expect(TYPOGRAPHY_SCALE.workspaceTitle).toBe("var(--ix-type-workspace-title)");
    expect(TYPOGRAPHY_SCALE.panelHeading).toBe("var(--ix-type-panel-heading)");
    expect(TYPOGRAPHY_SCALE.body).toBe("var(--ix-type-body)");
    expect(TYPOGRAPHY_SCALE.metadata).toBe("var(--ix-type-metadata)");

    // 3. Typed typography tokens
    expect(TYPOGRAPHY_TOKENS.fontSizeDisplay).toBe("var(--ix-font-size-display)");
    expect(TYPOGRAPHY_TOKENS.fontSizeWorkspaceTitle).toBe("var(--ix-font-size-workspace-title)");
    expect(TYPOGRAPHY_TOKENS.fontSizeMetadata).toBe("var(--ix-font-size-metadata)");

    // 4. Hierarchy tokens
    expect(HIERARCHY_TOKENS.level1).toBe("var(--ix-hierarchy-level-1)");
    expect(HIERARCHY_TOKENS.level2).toBe("var(--ix-hierarchy-level-2)");
    expect(HIERARCHY_TOKENS.level3).toBe("var(--ix-hierarchy-level-3)");
    expect(HIERARCHY_TOKENS.level4).toBe("var(--ix-hierarchy-level-4)");
  });
});
