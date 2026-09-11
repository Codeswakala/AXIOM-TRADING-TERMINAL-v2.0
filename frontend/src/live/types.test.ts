import { describe, expect, it } from "vitest";
import { isLiveCandle, type LiveMarketMessage } from "./types";

describe("live message models", () => {
  it("identifies live_candle messages", () => {
    const msg: LiveMarketMessage = {
      type: "live_candle",
      channel: "market",
      market_class: "forex",
      symbol: "EURUSD",
      timeframe: "M1",
      open_time: "2024-01-01T00:00:00Z",
      open: "1.1",
      high: "1.2",
      low: "1.0",
      close: "1.15",
      volume: "10",
      source: "live:simulated",
    };
    expect(isLiveCandle(msg)).toBe(true);
  });

  it("rejects non-candle messages", () => {
    expect(isLiveCandle({ type: "subscribed", channel: "market" })).toBe(false);
    expect(isLiveCandle({ type: "pong" })).toBe(false);
  });
});
