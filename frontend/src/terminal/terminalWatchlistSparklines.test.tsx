/**
 * DATA-P01 — watchlist sparkline & provenance surfacing suite (Build Order
 * S4, M2, M3, M5, R1). Named tests prove: sparklines render from the seeded
 * candle series (one code path — the same fetchCandles the chart uses);
 * provenance labels derive directly from the source fields; a synthetic
 * price never renders without the simulated qualifier; the `--` absence path
 * is preserved when quotes are absent; and one symbol's fetch failure
 * removes only that symbol's sparkline, never its row or the watchlist.
 */
import { render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { TerminalProvider } from "../components/terminal/TerminalContext";
import { TerminalWatchlistDock } from "../components/terminal/TerminalWatchlistDock";
import * as client from "../api/client";
import type { ApiCandle } from "../api/client";
import type { UseLiveMarketResult } from "../hooks/useLiveMarket";

function candleRow(symbol: string, close: number, index: number, source: string): ApiCandle {
  return {
    id: `c-${symbol}-${index}`,
    market_class: symbol.includes("BTC") ? "crypto" : "forex",
    symbol,
    timeframe: "M1",
    open_time: `2026-08-17T10:${String(index).padStart(2, "0")}:00Z`,
    open: String(close - 0.0001),
    high: String(close + 0.0002),
    low: String(close - 0.0003),
    close: String(close),
    volume: "100000",
    source,
    created_at: "2026-08-17T10:00:00Z",
  };
}

function seededSeries(symbol: string): ApiCandle[] {
  return Array.from({ length: 30 }, (_, i) =>
    candleRow(symbol, 1.1 + i * 0.0001, i, "seed:synthetic"),
  );
}

/** DATA-P02 M4: fetchCandles now returns the typed series envelope. */
function nativeOf(bars: ApiCandle[]) {
  return { kind: "native" as const, timeframe: "M1", bars };
}

function makeLiveMarket(overrides: Partial<UseLiveMarketResult> = {}): UseLiveMarketResult {
  return {
    connectionState: "connected",
    quotes: {
      EURUSD: {
        symbol: "EURUSD",
        marketClass: "forex",
        timeframe: "1m",
        open: "1.10000",
        high: "1.10100",
        low: "1.09900",
        close: "1.10050",
        volume: "14200000",
        openTime: "2026-08-17T10:00:00Z",
        source: "live:simulated",
        updatedAt: "2026-08-17T10:00:10Z",
        flash: null,
      },
    },
    messageCount: 0,
    lastMessageAt: null,
    messagesPerMinute: 0,
    lagHintMs: null,
    error: null,
    feedStats: null,
    reconnectCount: 0,
    startFeed: vi.fn().mockResolvedValue(undefined),
    stopFeed: vi.fn().mockResolvedValue(undefined),
    refreshStats: vi.fn().mockResolvedValue(undefined),
    reconnectNow: vi.fn(),
    ...overrides,
  };
}

let currentMockLiveMarket: UseLiveMarketResult = makeLiveMarket();

vi.mock("../hooks/useLiveMarket", () => ({
  useLiveMarket: () => currentMockLiveMarket,
}));

vi.mock("../api/client", async (importOriginal) => {
  const actual = await importOriginal<typeof client>();
  return {
    ...actual,
    fetchCandles: vi.fn(
      async (_params: {
        symbol: string;
        timeframe?: string;
        market_class?: string;
        limit?: number;
        order?: "asc" | "desc";
      }) => [] as ApiCandle[],
    ),
  };
});

function renderDock() {
  return render(
    <TerminalProvider initialSymbol="EUR/USD">
      <TerminalWatchlistDock />
    </TerminalProvider>,
  );
}

beforeEach(() => {
  vi.clearAllMocks();
  currentMockLiveMarket = makeLiveMarket();
});

describe("DATA-P01 — watchlist sparklines and synthetic provenance", () => {
  it("test_data_p01_s4_sparkline_renders_from_seeded_candle_series", async () => {
    vi.mocked(client.fetchCandles).mockResolvedValue(nativeOf(seededSeries("EURUSD")));

    renderDock();

    await waitFor(() => {
      expect(screen.getByTestId("watchlist-sparkline-eurusd")).toBeInTheDocument();
    });
    // One code path: the series was fetched with the same symbol the chart
    // uses — nothing synthesised at render time.
    const calls = (client.fetchCandles as unknown as { mock: { calls: unknown[][] } }).mock.calls;
    expect(calls.length).toBeGreaterThan(0);
    expect(calls[0][0]).toMatchObject({ symbol: "EURUSD", timeframe: "M1", limit: 30 });
  });

  it("test_data_p01_m2_sparkline_provenance_label_derives_from_candle_source", async () => {
    vi.mocked(client.fetchCandles).mockResolvedValue(nativeOf(seededSeries("EURUSD")));

    renderDock();

    await waitFor(() => {
      expect(screen.getByTestId("watchlist-sparkline-source-eurusd")).toHaveTextContent(
        "SEED:SYNTHETIC",
      );
    });
  });

  it("test_data_p01_m2_m3_price_provenance_chip_never_renders_live_alone", async () => {
    vi.mocked(client.fetchCandles).mockResolvedValue(nativeOf([]));

    renderDock();

    // The quote's source is "live:simulated" — the chip must render the
    // qualified form, never "LIVE" alone.
    await waitFor(() => {
      expect(screen.getByTestId("watchlist-provenance-eurusd")).toHaveTextContent(
        "LIVE:SIMULATED",
      );
    });
    expect(screen.getByTestId("watchlist-provenance-eurusd").textContent).not.toBe("LIVE");
  });

  it("test_data_p01_m5_absence_path_preserved_without_quotes", async () => {
    currentMockLiveMarket = makeLiveMarket({ quotes: {} });
    vi.mocked(client.fetchCandles).mockResolvedValue(nativeOf(seededSeries("EURUSD")));

    renderDock();

    // No quote: price and change render the honest absence markers — the
    // sparkline may still render from the seeded series, but the price is
    // never a fabricated fallback.
    await waitFor(() => {
      expect(screen.getByTestId("watchlist-sparkline-eurusd")).toBeInTheDocument();
    });
    expect(screen.getByTestId("price-eurusd")).toHaveTextContent("--");
    expect(screen.getByTestId("change-eurusd")).toHaveTextContent("--");
    expect(screen.getByTestId("range-eurusd")).toHaveTextContent("R: --");
  });

  it("test_data_p01_r1_symbol_seed_failure_removes_only_that_sparkline", async () => {
    vi.mocked(client.fetchCandles).mockImplementation((async (params) => {
      const symbol = (params as { symbol: string }).symbol;
      if (symbol === "GBPUSD") throw new Error("seed seam down");
      return nativeOf(seededSeries(symbol));
    }) as typeof client.fetchCandles);

    renderDock();

    await waitFor(() => {
      expect(screen.getByTestId("watchlist-sparkline-eurusd")).toBeInTheDocument();
    });
    // The failing symbol's sparkline is absent, but its row and price remain.
    expect(screen.queryByTestId("watchlist-sparkline-gbpusd")).not.toBeInTheDocument();
    expect(screen.getByTestId("watchlist-row-gbp-usd")).toBeInTheDocument();
    // The watchlist as a whole is not blanked.
    expect(screen.getByTestId("terminal-watchlist-dock")).toBeInTheDocument();
    expect(screen.getAllByRole("listitem").length).toBeGreaterThan(3);
  });
});
