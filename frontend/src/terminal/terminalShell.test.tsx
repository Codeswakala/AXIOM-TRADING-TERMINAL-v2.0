import { render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { TerminalGovernanceBadge } from "../components/terminal/TerminalGovernanceBadge";
import {
  TerminalTopTicker,
  type TickerMarketData,
} from "../components/terminal/TerminalTopTicker";
import {
  TerminalMultiPaneLayout,
  TerminalSlotPlaceholder,
} from "../components/terminal/TerminalMultiPaneLayout";
import { TradingTerminalWorkspace } from "../components/terminal/TradingTerminalWorkspace";
import { DashboardPage } from "../pages/DashboardPage";
import { CURRENT_PROTECTED_ROUTES, WORKSPACE_REGISTRY } from "../workstation/registry/workspaceRegistry";
import { ProtectedRoute } from "../auth/ProtectedRoute";
import { InstitutionalWorkspaceShell } from "../workstation/components/InstitutionalWorkspaceShell";

// Mock Auth
const authState = vi.hoisted(() => {
  const logoutFn = vi.fn();
  return {
    logoutFn,
    value: {
      operator: { username: "lead_operator", role: "admin" },
      loading: false,
      isAuthenticated: true,
      logout: logoutFn,
      login: vi.fn(),
      refreshProfile: vi.fn(),
    },
  };
});

vi.mock("../context/AuthContext", () => ({
  useAuth: () => authState.value,
}));

vi.mock("../workstation/persistence/shellPreferences", () => ({
  loadShellLayoutPreference: vi.fn().mockResolvedValue(null),
  persistShellLayoutPreference: vi.fn().mockResolvedValue({}),
}));

beforeEach(() => {
  authState.logoutFn.mockReset();
  authState.value = {
    operator: { username: "lead_operator", role: "admin" },
    loading: false,
    isAuthenticated: true,
    logout: authState.logoutFn,
    login: vi.fn(),
    refreshProfile: vi.fn(),
  };
});

describe("UI-NEW-P01 Terminal Foundation & Multi-Pane Shell Architecture", () => {
  // Test 1 (Mandatory named test #1)
  it("test_uinew_p01_terminal_shell_mounts_multipane_layout_without_dom_collisions", () => {
    render(
      <TerminalMultiPaneLayout
        topTicker={<div data-testid="custom-ticker">Persistent Ticker</div>}
        leftSlot={<div data-testid="custom-left">Watchlist Slot</div>}
        centreSlot={<div data-testid="custom-centre">Chart Stage</div>}
        rightSlot={<div data-testid="custom-right">Telemetry Slot</div>}
        bottomSlot={<div data-testid="custom-bottom">Analytics Dock</div>}
      />,
    );

    // Verify main container
    const layout = screen.getByTestId("terminal-multipane-layout");
    expect(layout).toBeInTheDocument();

    // Verify all landmark regions
    expect(screen.getByRole("banner", { name: "Global Terminal Ticker Bar" })).toBeInTheDocument();
    expect(screen.getByRole("complementary", { name: "Market Watchlist Dock" })).toBeInTheDocument();
    expect(screen.getByRole("main", { name: "Primary Candlestick Chart Stage" })).toBeInTheDocument();
    expect(screen.getByRole("complementary", { name: "Signals & Telemetry Dock" })).toBeInTheDocument();
    expect(screen.getByRole("region", { name: "Terminal Analytics Dock" })).toBeInTheDocument();

    // Verify custom slot contents
    expect(screen.getByTestId("custom-ticker")).toHaveTextContent("Persistent Ticker");
    expect(screen.getByTestId("custom-left")).toHaveTextContent("Watchlist Slot");
    expect(screen.getByTestId("custom-centre")).toHaveTextContent("Chart Stage");
    expect(screen.getByTestId("custom-right")).toHaveTextContent("Telemetry Slot");
    expect(screen.getByTestId("custom-bottom")).toHaveTextContent("Analytics Dock");
  });

  it("test_uinew_p01_terminal_shell_renders_default_docked_placeholders", () => {
    render(
      <div>
        <TerminalMultiPaneLayout />
        <TerminalSlotPlaceholder
          title="Direct Placeholder Test"
          phase="P01"
          description="Verification of placeholder contract"
        />
      </div>,
    );

    expect(screen.getByTestId("placeholder-market-watchlist")).toBeInTheDocument();
    expect(screen.getByTestId("placeholder-primary-candlestick-chart-stage")).toBeInTheDocument();
    expect(screen.getByTestId("placeholder-signals-spread-telemetry")).toBeInTheDocument();
    expect(screen.getByTestId("placeholder-terminal-analytics-dock")).toBeInTheDocument();
    expect(screen.getByTestId("placeholder-direct-placeholder-test")).toBeInTheDocument();

    expect(screen.getByText("P02")).toBeInTheDocument();
    expect(screen.getByText("P03")).toBeInTheDocument();
    expect(screen.getByText("P02 / P04")).toBeInTheDocument();
    expect(screen.getByText("P05")).toBeInTheDocument();
  });

  // Test 2 (Mandatory named test #2)
  it("test_uinew_p01_global_ticker_renders_symbol_price_change_clock_and_ws_status", () => {
    const marketData: TickerMarketData = {
      symbol: "EUR/USD",
      price: 1.0845,
      change24hPercent: 0.35,
      high24h: 1.0892,
      low24h: 1.0811,
      volume24h: "14.2M",
      spread: 0.8,
      posture: "live:simulated",
    };

    render(
      <TerminalTopTicker
        symbol="EUR/USD"
        marketData={marketData}
        wsStatus="live"
        showGovernanceBadge={true}
        initialClockUtc="14:22:05 UTC"
      />,
    );

    expect(screen.getByTestId("ticker-brand-badge")).toHaveTextContent("AXIOM TERMINAL");
    expect(screen.getByTestId("ticker-symbol-badge")).toHaveTextContent("EUR/USD");
    expect(screen.getByTestId("ticker-price-metric")).toHaveTextContent("1.08450");
    expect(screen.getByTestId("ticker-change-metric")).toHaveTextContent("+0.35%");
    expect(screen.getByTestId("ticker-spread")).toHaveTextContent("0.8 pts");
    expect(screen.getByTestId("ticker-volume")).toHaveTextContent("14.2M");
    expect(screen.getByTestId("ticker-high-low")).toHaveTextContent("H: 1.08920 L: 1.08110");
    expect(screen.getByTestId("ticker-ws-badge")).toHaveTextContent("WS: LIVE [●]");
    expect(screen.getByTestId("ticker-posture-badge")).toHaveTextContent("live:simulated");
    expect(screen.getByTestId("ticker-clock-badge")).toHaveTextContent("14:22:05 UTC");
    expect(screen.getByTestId("terminal-governance-badge")).toBeInTheDocument();
  });

  // Test 3 (Mandatory named test #3 — T-1 Spine)
  it("test_uinew_p01_terminal_contains_no_execution_or_order_or_broker_or_account_control", () => {
    render(
      <MemoryRouter>
        <TradingTerminalWorkspace />
      </MemoryRouter>,
    );

    // Verify all interactive elements in the terminal workspace
    const buttons = screen.queryAllByRole("button");
    const links = screen.queryAllByRole("link");
    const inputs = screen.queryAllByRole("textbox");

    const allInteractiveText = [
      ...buttons.map((b) => b.textContent?.toLowerCase() ?? ""),
      ...links.map((l) => l.textContent?.toLowerCase() ?? ""),
      ...inputs.map((i) => i.getAttribute("placeholder")?.toLowerCase() ?? ""),
    ].join(" ");

    const forbiddenActuationTerms = [
      "buy",
      "sell",
      "place_order",
      "submit_order",
      "order_ticket",
      "execute",
      "go-live",
      "connect-broker",
      "broker",
      "account_id",
      "position",
      "balance",
      "margin",
      "capital",
      "real_pnl",
      "open_gate",
      "allow_execution",
    ];

    for (const term of forbiddenActuationTerms) {
      expect(allInteractiveText).not.toContain(term);
    }
  });

  // Test 4 (Mandatory named test #4 — T-6 Data Honesty Spine)
  it("test_uinew_p01_terminal_renders_no_fabricated_market_values_and_labels_unavailable_states", () => {
    // Case A: Disconnected feed
    const { rerender } = render(
      <TerminalTopTicker
        symbol="EUR/USD"
        marketData={null}
        wsStatus="disconnected"
      />,
    );

    const disconnectedPrice = screen.getByTestId("ticker-price-metric");
    expect(disconnectedPrice).toHaveTextContent("Disconnected");
    expect(disconnectedPrice.textContent).not.toMatch(/^\d+\.\d+$/); // Not a plausible fake number
    expect(screen.getByTestId("ticker-change-metric")).toHaveTextContent("--");
    expect(screen.getByTestId("ticker-spread")).toHaveTextContent("--");
    expect(screen.getByTestId("ticker-volume")).toHaveTextContent("--");
    expect(screen.getByTestId("ticker-high-low")).toHaveTextContent("H: -- L: --");
    expect(screen.getByTestId("ticker-ws-badge")).toHaveTextContent("WS: DISCONNECTED [○]");

    // Case B: Connecting feed
    rerender(
      <TerminalTopTicker
        symbol="EUR/USD"
        marketData={null}
        wsStatus="connecting"
      />,
    );
    const connectingPrice = screen.getByTestId("ticker-price-metric");
    expect(connectingPrice).toHaveTextContent("Loading…");
    expect(screen.getByTestId("ticker-ws-badge")).toHaveTextContent("WS: CONNECTING [○]");

    // Case C: Empty feed
    rerender(
      <TerminalTopTicker
        symbol="EUR/USD"
        marketData={null}
        wsStatus="empty"
      />,
    );
    const emptyPrice = screen.getByTestId("ticker-price-metric");
    expect(emptyPrice).toHaveTextContent("Empty Feed");

    // Case D: Idle feed with no quote
    rerender(
      <TerminalTopTicker
        symbol="EUR/USD"
        marketData={null}
        wsStatus="idle"
      />,
    );
    const idlePrice = screen.getByTestId("ticker-price-metric");
    expect(idlePrice).toHaveTextContent("--");
  });

  // Test 5 (Mandatory named test #5 — Route Preservation & Root Route Mount)
  it("test_uinew_p01_root_route_mounts_terminal_workstation_and_preserves_existing_routes", () => {
    // 1. Verify root route mounts DashboardPage with TradingTerminalWorkspace
    render(
      <MemoryRouter initialEntries={["/"]}>
        <Routes>
          <Route
            element={
              <ProtectedRoute>
                <InstitutionalWorkspaceShell />
              </ProtectedRoute>
            }
          >
            <Route path="/" element={<DashboardPage />} />
          </Route>
        </Routes>
      </MemoryRouter>,
    );

    expect(screen.getByTestId("trading-terminal-workspace")).toBeInTheDocument();
    expect(screen.getByTestId("terminal-multipane-layout")).toBeInTheDocument();
    expect(screen.getByTestId("terminal-top-ticker")).toBeInTheDocument();

    // 2. Verify all 16 registered routes remain fully preserved
    const expectedRoutes = [
      "/",
      "/live",
      "/charts",
      "/chart",
      "/signals",
      "/analytics",
      "/intelligence",
      "/investigate",
      "/compare-scenarios",
      "/trade-plans",
      "/execution-research",
      "/portfolio-research",
      "/journal",
      "/research-management",
      "/governance",
      "/workspace",
    ];

    expect(CURRENT_PROTECTED_ROUTES.sort()).toEqual(expectedRoutes.sort());
    expect(WORKSPACE_REGISTRY.length).toBe(16);
    expect(WORKSPACE_REGISTRY.every((w) => w.requiresAuth)).toBe(true);
    expect(WORKSPACE_REGISTRY.every((w) => w.noActuation)).toBe(true);
  });

  // Test 6 (Mandatory named test #6 — Governance Badge Inertness)
  it("test_uinew_p01_governance_badge_renders_gate_closed_research_only_inert", () => {
    render(<TerminalGovernanceBadge />);

    const badge = screen.getByTestId("terminal-governance-badge");
    expect(badge).toBeInTheDocument();
    expect(badge).toHaveAttribute("role", "status");
    expect(screen.getByTestId("terminal-gov-gate")).toHaveTextContent("GATE: CLOSED");
    expect(screen.getByTestId("terminal-gov-posture")).toHaveTextContent(
      "RESEARCH-ONLY · NON-ACTUATING",
    );

    // Verify it is not a clickable execution button
    expect(badge.tagName.toLowerCase()).not.toBe("button");
    expect(badge.tagName.toLowerCase()).not.toBe("a");
    expect(badge.getAttribute("onclick")).toBeNull();
  });
});
