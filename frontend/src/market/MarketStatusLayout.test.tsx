import { render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import {
  MarketStatusCards,
  MarketWorkspaceStateNotice,
} from "../components/chart/ChartWorkspaceSurface";
import { InstitutionalWorkspaceShell } from "../workstation/components/InstitutionalWorkspaceShell";

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

vi.mock("../context/AuthContext", () => ({
  useAuth: () => authState.value,
}));

vi.mock("../workstation/persistence/shellPreferences", () => ({
  loadShellLayoutPreference: vi.fn().mockResolvedValue(null),
  persistShellLayoutPreference: vi.fn().mockResolvedValue({}),
}));

async function readRaw(pathSuffix: string): Promise<string> {
  const modules = import.meta.glob("../**/*.{ts,tsx,css}", {
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

describe("UI-003-P04 market status and responsive layout", () => {
  it("test_ui003_market_overview_uses_existing_simulated_status_sources_only", async () => {
    render(
      <MarketStatusCards
        symbol="EURUSD"
        timeframe="M1"
        barCount={524}
        connectionState="connected"
        feedRunning
        lastLiveAt="2026-07-23T05:12:06.518Z"
        sourceSummary="seed:synthetic=500 · live:simulated=24"
      />,
    );

    const cards = screen.getByLabelText("Market status overview cards");
    expect(cards).toHaveTextContent("live:simulated");
    expect(cards).toHaveTextContent(/governed simulated stream/i);
    expect(cards).toHaveTextContent("seed:synthetic=500");

    const chartSource = await readRaw("components/chart/ChartWorkspaceSurface.tsx");
    expect(chartSource).toContain("useChartData");
    expect(chartSource).toContain("MarketStatusCards");
    expect(chartSource).not.toContain("new MarketDataProvider");
    expect(chartSource).not.toContain("brokerFeed");
  });

  it("test_ui003_market_status_never_claims_real_feed_or_broker_connection", async () => {
    render(
      <MarketStatusCards
        symbol="BTCUSD"
        timeframe="H1"
        barCount={80}
        connectionState="connected"
        feedRunning
        lastLiveAt="2026-07-23T05:12:06.518Z"
        sourceSummary="live:simulated=80"
      />,
    );
    const text = screen.getByLabelText("Market status overview cards").textContent?.toLowerCase() ?? "";
    expect(text).toContain("live:simulated");
    expect(text).not.toContain("real feed");
    expect(text).not.toContain("broker connection");

    const chartSource = (await readRaw("components/chart/ChartWorkspaceSurface.tsx")).toLowerCase();
    expect(chartSource).toContain("live:simulated");
    expect(chartSource).not.toContain("real feed");
    expect(chartSource).not.toContain("broker connection");
  });

  it("test_ui003_responsive_layout_preserves_single_shell_no_duplicate_nav", async () => {
    render(
      <MemoryRouter initialEntries={["/charts"]}>
        <Routes>
          <Route element={<InstitutionalWorkspaceShell />}>
            <Route
              path="/charts"
              element={
                <MarketStatusCards
                  symbol="EURUSD"
                  timeframe="M1"
                  barCount={12}
                  connectionState="idle"
                  feedRunning={false}
                  lastLiveAt={null}
                  sourceSummary={null}
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
    expect(screen.getByLabelText("Market status overview cards")).toBeInTheDocument();

    expect(screen.getByLabelText("Market status overview cards").querySelector(".market-status-card-grid")).not.toBeNull();
    expect(screen.getAllByRole("article").length).toBeGreaterThanOrEqual(5);
  });

  it("test_ui003_empty_loading_error_states_are_accessible_and_research_framed", () => {
    render(
      <>
        <MarketWorkspaceStateNotice state="loading" message="Loading existing historical candles…" />
        <MarketWorkspaceStateNotice state="empty" message="No governed candles available." />
        <MarketWorkspaceStateNotice state="error" message="Failed to load market context." />
      </>,
    );

    expect(screen.getByLabelText("Market workspace loading state")).toHaveAttribute("role", "status");
    expect(screen.getByLabelText("Market workspace empty state")).toHaveAttribute("role", "status");
    expect(screen.getByLabelText("Market workspace error state")).toHaveAttribute("role", "alert");
    expect(screen.getAllByText(/Research-only presentation/i)).toHaveLength(3);
    expect(screen.getAllByText(/No inference, no action, no order path/i)).toHaveLength(3);
  });
});
