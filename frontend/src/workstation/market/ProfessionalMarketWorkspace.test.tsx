import { render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import {
  ChartAccessibleSummary,
  ProfessionalMarketOverview,
} from "../../components/chart/ChartWorkspaceSurface";
import { InstitutionalWorkspaceShell } from "../components/InstitutionalWorkspaceShell";

const authState = vi.hoisted(() => ({
  value: {
    operator: { username: "operator", role: "admin" },
    loading: false,
    isAuthenticated: true,
    logout: vi.fn(),
    login: vi.fn(),
    refreshProfile: vi.fn(),
  },
}));

vi.mock("../../context/AuthContext", () => ({
  useAuth: () => authState.value,
}));

vi.mock("../persistence/shellPreferences", () => ({
  loadShellLayoutPreference: vi.fn().mockResolvedValue(null),
  persistShellLayoutPreference: vi.fn().mockResolvedValue({}),
}));

function renderMarketOverview() {
  render(
    <ProfessionalMarketOverview
      symbol="EURUSD"
      timeframe="M1"
      chartType="candlestick"
      barCount={120}
      connectionState="connected"
      feedRunning={true}
      lastLiveAt="2026-07-22T10:00:00Z"
      sourceSummary="seed:synthetic=100 · live:simulated=20"
    />,
  );
}

async function readRawSource(pathSuffix: string): Promise<string> {
  const modules = import.meta.glob("../../**/*.{ts,tsx}", {
    query: "?raw",
    import: "default",
  });
  const parts = pathSuffix.split("/");
  const fileName = parts[parts.length - 1] ?? pathSuffix;
  const entry = Object.entries(modules).find(
    ([path]) => path.endsWith(pathSuffix) || path.endsWith(fileName),
  );
  if (!entry) throw new Error(`Raw source not found: ${pathSuffix}`);
  return (entry[1] as () => Promise<string>)();
}

describe("UI-003-P01 Professional Market Workspace frame", () => {
  it("test_ui003_market_workspace_mounts_inside_single_ui001_shell", () => {
    render(
      <MemoryRouter initialEntries={["/charts"]}>
        <Routes>
          <Route element={<InstitutionalWorkspaceShell />}>
            <Route
              path="/charts"
              element={
                <ProfessionalMarketOverview
                  symbol="EURUSD"
                  timeframe="M1"
                  chartType="candlestick"
                  barCount={25}
                  connectionState="connected"
                  feedRunning={false}
                  lastLiveAt={null}
                  sourceSummary="seed:synthetic=25"
                />
              }
            />
          </Route>
        </Routes>
      </MemoryRouter>,
    );

    expect(screen.getAllByTestId("institutional-workspace-shell")).toHaveLength(1);
    expect(screen.getAllByLabelText("Global command bar")).toHaveLength(1);
    expect(screen.getAllByLabelText("Institutional workflow navigation")).toHaveLength(1);
    expect(screen.getByLabelText("Primary workspace")).toHaveAttribute(
      "data-active-telemetry-id",
      "workspace.monitor.chart_workspace",
    );
    expect(screen.getByLabelText("Professional market workspace overview")).toBeInTheDocument();
  });

  it("test_ui003_market_workspace_uses_existing_chart_and_market_sources_only", async () => {
    const chartPage = await readRawSource("components/chart/ChartWorkspaceSurface.tsx");
    const chartData = await readRawSource("hooks/useChartData.ts");
    const combined = `${chartPage}\n${chartData}`;

    expect(combined).toContain("useChartData");
    expect(combined).toContain("fetchCandles");
    expect(combined).toContain("fetchChartResearchAnnotations");
    expect(combined).toContain("PriceChart");
    expect(combined).toContain("useLiveMarket");
    for (const forbidden of [
      "inferSignal",
      "runInference",
      "authoritativeRecompute",
      "emitSignal",
      "/api/v1/search",
      "/api/v1/orders",
      "new WebSocket(\"wss://",
    ]) {
      expect(combined).not.toContain(forbidden);
    }
  });

  it("test_ui003_market_workspace_labels_synthetic_and_simulated_data_non_authoritative", () => {
    renderMarketOverview();

    const overview = screen.getByLabelText("Professional market workspace overview");
    expect(overview).toHaveTextContent("seed:synthetic");
    expect(overview).toHaveTextContent("live:simulated");
    expect(overview).toHaveTextContent(/non-authoritative/i);
    expect(overview).toHaveTextContent(/chart context only/i);
    expect(overview).not.toHaveTextContent(/real market data/i);
  });

  it("test_ui003_market_workspace_contains_no_execution_or_actuation_controls", async () => {
    renderMarketOverview();
    const buttonText = screen
      .queryAllByRole("button")
      .map((button) => button.textContent?.toLowerCase() ?? "")
      .join(" ");
    for (const marker of ["b" + "uy", "s" + "ell", "place order", "connect broker", "open gate"]) {
      expect(buttonText).not.toContain(marker);
    }

    const sourceText = (await readRawSource("components/chart/ChartWorkspaceSurface.tsx")).toLowerCase();
    for (const marker of [
      "b" + "uy",
      "s" + "ell",
      "place_order",
      "exec" + "ute",
      "go-live",
      "connect-broker",
      "account_id",
      "order_ticket",
      "open_gate",
      "allow_exec" + "ution",
    ]) {
      expect(sourceText).not.toContain(marker);
    }
  });

  it("test_ui003_market_workspace_has_accessible_chart_summary_and_controls", () => {
    render(
      <>
        <ProfessionalMarketOverview
          symbol="BTCUSD"
          timeframe="H1"
          chartType="line"
          barCount={80}
          connectionState="connected"
          feedRunning={true}
          lastLiveAt="2026-07-22T10:00:00Z"
          sourceSummary="seed:synthetic=80"
        />
        <ChartAccessibleSummary
          symbol="BTCUSD"
          timeframe="H1"
          chartType="line"
          barCount={80}
          sourceSummary="seed:synthetic=80"
        />
      </>,
    );

    expect(screen.getByLabelText("Professional market workspace overview")).toBeInTheDocument();
    expect(screen.getByLabelText("Market workspace data-source inventory")).toBeInTheDocument();
    expect(screen.getByLabelText("Accessible chart summary")).toHaveTextContent(
      "BTCUSD H1 line chart",
    );
    expect(screen.getByLabelText("Accessible chart summary")).toHaveTextContent("80 bars");
  });
});
