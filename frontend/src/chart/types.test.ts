import { describe, expect, it } from "vitest";
import { apiCandleToBar, mergeLiveBar, parseCandleTime, type CandleBar } from "./types";

describe("chart types helpers", () => {
  it("parses ISO times to unix seconds", () => {
    const t = parseCandleTime("2024-01-01T00:00:00Z");
    expect(t).toBe(1704067200);
  });

  it("maps API candles to bars", () => {
    const bar = apiCandleToBar({
      open_time: "2024-01-01T00:00:00Z",
      open: "1.1",
      high: "1.2",
      low: "1.0",
      close: "1.15",
      volume: "10",
    });
    expect(bar.time).toBe(1704067200);
    expect(bar.close).toBe(1.15);
  });

  it("updates forming candle and appends new bars", () => {
    const series: CandleBar[] = [
      { time: 100, open: 1, high: 2, low: 0.5, close: 1.5 },
    ];
    const updated = mergeLiveBar(series, {
      time: 100,
      open: 1,
      high: 2.2,
      low: 0.5,
      close: 1.8,
    });
    expect(updated).toHaveLength(1);
    expect(updated[0].close).toBe(1.8);
    expect(updated[0].high).toBe(2.2);

    const appended = mergeLiveBar(updated, {
      time: 160,
      open: 1.8,
      high: 1.9,
      low: 1.7,
      close: 1.85,
    });
    expect(appended).toHaveLength(2);
    expect(appended[1].time).toBe(160);
  });

  it("ignores out-of-order older live bars", () => {
    const series: CandleBar[] = [
      { time: 200, open: 1, high: 2, low: 1, close: 1.5 },
    ];
    const next = mergeLiveBar(series, {
      time: 100,
      open: 1,
      high: 1,
      low: 1,
      close: 1,
    });
    expect(next).toHaveLength(1);
    expect(next[0].time).toBe(200);
  });
});
