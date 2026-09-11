import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { TerminalProvider } from "../components/terminal/TerminalContext";
import { TerminalWatchlistDock } from "../components/terminal/TerminalWatchlistDock";
import { TerminalMarketTelemetry } from "../components/terminal/TerminalMarketTelemetry";
import { TradingTerminalWorkspace } from "../components/terminal/TradingTerminalWorkspace";
import type { UseLiveMarketResult } from "../hooks/useLiveMarket";

// Create flexible mock factory for useLiveMarket
const createMockLiveMarket = (overrides: Partial<UseLiveMarketResult> = {}): UseLiveMarketResult => ({
  connectionState: "connected",
  quotes: {
    EURUSD: {
      symbol: "EURUSD",
      marketClass: "forex",
      timeframe: "1m",
      open: "1.08410",
      high: "1.08490",
      low: "1.08390",
      close: "1.08450",
      volume: "14200000",
      openTime: "2026-08-12T15:00:00Z",
      source: "synthetic",
      updatedAt: "2026-08-12T15:00:10Z",
      flash: null,
    },
    GBPUSD: {
      symbol: "GBPUSD",
      marketClass: "forex",
      timeframe: "1m",
      open: "1.29050",
      high: "1.29150",
      low: "1.29000",
      close: "1.29120",
      volume: "8500000",
      openTime: "2026-08-12T15:00:00Z",
      source: "synthetic",
      updatedAt: "2026-08-12T15:00:10Z",
      flash: null,
    },
    BTCUSD: {
      symbol: "BTCUSD",
      marketClass: "crypto",
      timeframe: "1m",
      open: "64100.00",
      high: "64350.00",
      low: "64050.00",
      close: "64250.00",
      volume: "1250000",
      openTime: "2026-08-12T15:00:00Z",
      source: "synthetic",
      updatedAt: "2026-08-12T15:00:10Z",
      flash: null,
    },
    "USD/CAD": {
      symbol: "USDCAD",
      marketClass: "forex",
      timeframe: "1m",
      open: "1.36500",
      high: "1.36600",
      low: "1.36450",
      close: "1.36550",
      volume: null, // Null volume test case (B-P02-1 / T-6)
      openTime: "2026-08-12T15:00:00Z",
      source: "synthetic",
      updatedAt: "2026-08-12T15:00:10Z",
      flash: null,
    },
    // OBS-DATA1-2: JPY quote at the 3-decimal tick convention.
    USDJPY: {
      symbol: "USDJPY",
      marketClass: "forex",
      timeframe: "1m",
      open: "150.000",
      high: "150.015",
      low: "149.990",
      close: "150.010",
      volume: "9000000",
      openTime: "2026-08-12T15:00:00Z",
      source: "live:simulated",
      updatedAt: "2026-08-12T15:00:10Z",
      flash: null,
    },
  },
  messageCount: 1248,
  lastMessageAt: "2026-08-12T15:00:10Z",
  messagesPerMinute: 24,
  lagHintMs: 12,
  error: null,
  feedStats: {
    running: true,
    auto_start: true,
    adapter: "synthetic",
    connected: true,
    market_class: "forex",
    symbol: "EURUSD",
    symbols: ["EURUSD", "GBPUSD", "USDJPY", "BTCUSD", "ETHUSD"],
    timeframe: "1m",
    messages_received: 1248,
    persist_count: 1248,
    persist_errors: 0,
    lag_ms: 12,
    last_message_at: "2026-08-12T15:00:10Z",
    last_persisted_at: "2026-08-12T15:00:10Z",
    started_at: "2026-08-12T14:00:00Z",
    subscribers: 1,
    last_candle: null,
    latest_by_symbol: {},
    last_error: null,
    reconnect_count: 0,
    adapter_details: {},
  },
  reconnectCount: 0,
  startFeed: vi.fn().mockResolvedValue(undefined),
  stopFeed: vi.fn().mockResolvedValue(undefined),
  refreshStats: vi.fn().mockResolvedValue(undefined),
  reconnectNow: vi.fn(),
  ...overrides,
});

let currentMockLiveMarket = createMockLiveMarket();

vi.mock("../hooks/useLiveMarket", () => ({
  useLiveMarket: () => currentMockLiveMarket,
}));

// DATA-P01: the dock now fetches candle series per symbol for sparklines.
// Existing tests assert prices/change/selection, so resolve empty series.
vi.mock("../api/client", async (importOriginal) => {
  const actual = await importOriginal<typeof import("../api/client")>();
  return {
    ...actual,
    fetchCandles: vi.fn().mockResolvedValue({ kind: "native", timeframe: "M1", bars: [] }),
  };
});

describe("UI-NEW-P02 Market Watchlist & Market Telemetry Surface", () => {
  // Test 1 (Mandatory named test #1)
  // DATA-P01 OBS-DATA1-2: JPY pairs display at the 3-decimal tick
  // convention — the corrected generator's scale must survive at the render
  // layer, not be padded back to five decimals.
  it("test_data_p01_obs1_2_jpy_price_displays_three_decimal_ticks", () => {
    currentMockLiveMarket = createMockLiveMarket();

    render(
      <TerminalProvider initialSymbol="EUR/USD">
        <TerminalWatchlistDock />
      </TerminalProvider>,
    );

    expect(screen.getByTestId("price-usdjpy")).toHaveTextContent("150.010");
    expect(screen.getByTestId("price-usdjpy").textContent).not.toMatch(/\.\d{4}/);
    // Non-JPY forex keeps the 5-decimal convention.
    expect(screen.getByTestId("price-eurusd")).toHaveTextContent("1.08450");
  });

  it("test_uinew_p02_watchlist_dock_renders_multi_asset_symbols_and_selection", () => {
    currentMockLiveMarket = createMockLiveMarket();

    render(
      <TerminalProvider initialSymbol="EUR/USD">
        <TerminalWatchlistDock />
      </TerminalProvider>,
    );

    // Verify watchlist container & header
    expect(screen.getByTestId("terminal-watchlist-dock")).toBeInTheDocument();
    expect(screen.getByText("WATCHLIST")).toBeInTheDocument();

    // Verify Forex instruments render
    expect(screen.getByTestId("watchlist-row-eur-usd")).toBeInTheDocument();
    expect(screen.getByTestId("watchlist-row-gbp-usd")).toBeInTheDocument();
    expect(screen.getByTestId("price-eurusd")).toHaveTextContent("1.08450");
    expect(screen.getByTestId("change-eurusd")).toHaveTextContent("+0.04%");

    // Verify Crypto instruments render
    expect(screen.getByTestId("watchlist-row-btc-usd")).toBeInTheDocument();
    expect(screen.getByTestId("price-btcusd")).toHaveTextContent("64,250.00");

    // Verify search filtering
    const searchInput = screen.getByTestId("watchlist-search-input");
    fireEvent.change(searchInput, { target: { value: "BTC" } });
    expect(screen.getByTestId("watchlist-row-btc-usd")).toBeInTheDocument();
    expect(screen.queryByTestId("watchlist-row-eur-usd")).not.toBeInTheDocument();

    // Verify clear search
    fireEvent.change(searchInput, { target: { value: "" } });
    expect(screen.getByTestId("watchlist-row-eur-usd")).toBeInTheDocument();

    // Verify category filter tabs
    const cryptoTab = screen.getByTestId("watchlist-tab-crypto");
    fireEvent.click(cryptoTab);
    expect(screen.getByTestId("watchlist-row-btc-usd")).toBeInTheDocument();
    expect(screen.queryByTestId("watchlist-row-eur-usd")).not.toBeInTheDocument();
  });

  // Test 2 (Mandatory named test #2)
  it("test_uinew_p02_active_symbol_selection_propagates_to_terminal_state", () => {
    currentMockLiveMarket = createMockLiveMarket();

    render(<TradingTerminalWorkspace initialSymbol="EUR/USD" initialRightView="TELEMETRY" />);

    // Initial state: EUR/USD active
    expect(screen.getByTestId("ticker-symbol-badge")).toHaveTextContent("EUR/USD");
    expect(screen.getByTestId("telemetry-instrument-section")).toHaveTextContent("EUR/USD");

    // Click GBP/USD row in watchlist
    const gbpRow = screen.getByTestId("watchlist-row-gbp-usd");
    fireEvent.click(gbpRow);

    // Verify active selection propagated to Top Ticker and Telemetry panel
    expect(screen.getByTestId("ticker-symbol-badge")).toHaveTextContent("GBP/USD");
    expect(screen.getByTestId("telemetry-instrument-section")).toHaveTextContent("GBP/USD");
    expect(screen.getByTestId("telemetry-price")).toHaveTextContent("1.29120");
  });

  // Test 3 (Mandatory named test #3 — B-P02-1 Spine: Backend Supported Fields Only)
  it("test_uinew_p02_telemetry_renders_only_backend_supported_fields", () => {
    currentMockLiveMarket = createMockLiveMarket();

    render(
      <TerminalProvider initialSymbol="EUR/USD">
        <TerminalMarketTelemetry />
      </TerminalProvider>,
    );

    // 1. Verify genuine OHLC candle fields from /ws/market
    expect(screen.getByTestId("telemetry-price")).toHaveTextContent("1.08450");
    expect(screen.getByTestId("telemetry-open")).toHaveTextContent("1.08410");
    expect(screen.getByTestId("telemetry-high")).toHaveTextContent("1.08490");
    expect(screen.getByTestId("telemetry-low")).toHaveTextContent("1.08390");

    // 2. Verify intraperiod range strictly labelled as Range (H - L), NOT spread
    expect(screen.getByTestId("telemetry-range")).toHaveTextContent("0.00100 pts (10.0 pips)");

    // 3. Verify session volume from candle.volume
    expect(screen.getByTestId("telemetry-volume")).toHaveTextContent("14.20M");

    // 4. Verify feed protocol statistics from LiveMarketStatsResponse
    expect(screen.getByTestId("telemetry-ws-channel")).toHaveTextContent("/ws/market");
    expect(screen.getByTestId("telemetry-ws-status")).toHaveTextContent("CONNECTED");
    expect(screen.getByTestId("telemetry-tick-rate")).toHaveTextContent("24 msgs/min");
    expect(screen.getByTestId("telemetry-tick-count")).toHaveTextContent("1,248");
    expect(screen.getByTestId("telemetry-feed-lag")).toHaveTextContent("12 ms");
    expect(screen.getByTestId("telemetry-posture-badge")).toHaveTextContent("live:simulated");

    // 5. Verify explicit Gate-closed disclosure on spread & depth
    expect(screen.getByTestId("telemetry-disclosure-card")).toHaveTextContent(
      "SPREAD & DEPTH: UNAVAILABLE",
    );
  });

  // Test 4 (Mandatory named test #4 — C-1 Permanence / Zero Depth Ladder)
  it("test_uinew_p02_no_bid_ask_or_depth_rendering_anywhere_in_terminal", () => {
    currentMockLiveMarket = createMockLiveMarket();

    render(<TradingTerminalWorkspace initialSymbol="EUR/USD" />);

    const terminalText = screen.getByTestId("trading-terminal-workspace").textContent?.toLowerCase() ?? "";

    // Strictly assert zero order book / depth ladder terms
    expect(terminalText).not.toContain("depth ladder");
    expect(terminalText).not.toContain("order book");
    expect(terminalText).not.toContain("orderbook");
    expect(terminalText).not.toContain("bid size");
    expect(terminalText).not.toContain("ask size");
  });

  // Test 5 (Mandatory named test #5 — T-6 Data Honesty: Null volume, Stale & Disconnected feeds)
  it("test_uinew_p02_unavailable_and_stale_feed_states_render_explicitly_without_fabrication", () => {
    // Case A: Null volume handling (e.g. USD/CAD has volume: null)
    currentMockLiveMarket = createMockLiveMarket();

    const { rerender } = render(
      <TerminalProvider initialSymbol="USD/CAD">
        <TerminalMarketTelemetry />
      </TerminalProvider>,
    );

    expect(screen.getByTestId("telemetry-volume")).toHaveTextContent("Unavailable");

    // Case B: Disconnected feed (connectionState = "disconnected", quotes = {})
    currentMockLiveMarket = createMockLiveMarket({
      connectionState: "disconnected",
      quotes: {},
      messageCount: 0,
      messagesPerMinute: 0,
      lagHintMs: null,
      feedStats: null,
    });

    rerender(
      <TerminalProvider initialSymbol="EUR/USD">
        <TerminalMarketTelemetry />
      </TerminalProvider>,
    );

    expect(screen.getByTestId("telemetry-price")).toHaveTextContent("--");
    expect(screen.getByTestId("telemetry-open")).toHaveTextContent("--");
    expect(screen.getByTestId("telemetry-high")).toHaveTextContent("--");
    expect(screen.getByTestId("telemetry-low")).toHaveTextContent("--");
    expect(screen.getByTestId("telemetry-range")).toHaveTextContent("--");
    expect(screen.getByTestId("telemetry-volume")).toHaveTextContent("Unavailable");
    expect(screen.getByTestId("telemetry-ws-status")).toHaveTextContent("DISCONNECTED");
  });

  // Test 6 (Mandatory named test #6 — T-1 Zero Actuation)
  it("test_uinew_p02_contains_no_execution_or_order_or_broker_or_account_control", () => {
    currentMockLiveMarket = createMockLiveMarket();

    render(<TradingTerminalWorkspace initialSymbol="EUR/USD" />);

    const buttons = screen.queryAllByRole("button");
    const inputs = screen.queryAllByRole("textbox");

    const interactiveText = [
      ...buttons.map((b) => b.textContent?.toLowerCase() ?? ""),
      ...inputs.map((i) => i.getAttribute("placeholder")?.toLowerCase() ?? ""),
    ].join(" ");

    const forbiddenActuation = [
      "buy",
      "sell",
      "place_order",
      "submit_order",
      "order_ticket",
      "execute",
      "connect-broker",
      "account_id",
      "position",
      "balance",
      "margin",
      "open_gate",
      "allow_execution",
    ];

    for (const term of forbiddenActuation) {
      expect(interactiveText).not.toContain(term);
    }
  });
});
