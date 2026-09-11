import { describe, expect, it, vi, beforeEach, afterEach } from "vitest";
import { isLiveCandle } from "../live/types";

/**
 * WebSocket message handling logic unit tests.
 * Full hook mounting is covered via component tests; here we verify message parsing
 * and quote update semantics used by the hook.
 */

type QuoteMap = Record<
  string,
  {
    symbol: string;
    close: string;
    flash: "up" | "down" | null;
  }
>;

function applyCandle(
  quotes: QuoteMap,
  prevClose: Record<string, number>,
  msg: {
    type: string;
    symbol: string;
    close: string;
    market_class: string;
    timeframe: string;
    open: string;
    high: string;
    low: string;
    volume: string | null;
    open_time: string;
    source: string | null;
  },
): QuoteMap {
  if (!isLiveCandle(msg as never)) return quotes;
  const closeNum = Number(msg.close);
  const prev = prevClose[msg.symbol];
  let flash: "up" | "down" | null = null;
  if (prev != null && !Number.isNaN(closeNum)) {
    if (closeNum > prev) flash = "up";
    else if (closeNum < prev) flash = "down";
  }
  if (!Number.isNaN(closeNum)) prevClose[msg.symbol] = closeNum;
  return {
    ...quotes,
    [msg.symbol]: { symbol: msg.symbol, close: msg.close, flash },
  };
}

describe("live quote update semantics", () => {
  it("marks flash up/down based on previous close", () => {
    const prev: Record<string, number> = {};
    let quotes: QuoteMap = {};
    const base = {
      type: "live_candle",
      market_class: "forex",
      timeframe: "M1",
      open: "1.1",
      high: "1.2",
      low: "1.0",
      volume: "1",
      open_time: "t",
      source: "live:simulated",
    };
    quotes = applyCandle(quotes, prev, { ...base, symbol: "EURUSD", close: "1.10" });
    expect(quotes.EURUSD.flash).toBeNull();
    quotes = applyCandle(quotes, prev, { ...base, symbol: "EURUSD", close: "1.11" });
    expect(quotes.EURUSD.flash).toBe("up");
    quotes = applyCandle(quotes, prev, { ...base, symbol: "EURUSD", close: "1.09" });
    expect(quotes.EURUSD.flash).toBe("down");
  });

  it("tracks multiple symbols independently", () => {
    const prev: Record<string, number> = {};
    let quotes: QuoteMap = {};
    const mk = (symbol: string, close: string) =>
      applyCandle(quotes, prev, {
        type: "live_candle",
        symbol,
        close,
        market_class: "x",
        timeframe: "M1",
        open: close,
        high: close,
        low: close,
        volume: null,
        open_time: "t",
        source: "live:simulated",
      });
    quotes = mk("EURUSD", "1.1");
    quotes = mk("BTCUSD", "42000");
    expect(Object.keys(quotes).sort()).toEqual(["BTCUSD", "EURUSD"]);
  });
});

describe("WebSocket URL construction", () => {
  const original = window.location;

  beforeEach(() => {
    // jsdom location
    Object.defineProperty(window, "location", {
      value: { ...original, protocol: "http:", host: "localhost:8000" },
      writable: true,
    });
  });

  afterEach(() => {
    Object.defineProperty(window, "location", { value: original });
    vi.unstubAllEnvs?.();
  });

  it("embeds short-lived ticket query param (not access JWT)", async () => {
    const { getLiveMarketWebSocketUrlWithTicket } = await import("../api/client");
    const url = getLiveMarketWebSocketUrlWithTicket("short-lived-ticket-value");
    expect(url).toContain("/ws/market");
    expect(url).toContain("ticket=short-lived-ticket-value");
    expect(url).not.toContain("token=");
    expect(url.startsWith("ws://")).toBe(true);
  });
});
