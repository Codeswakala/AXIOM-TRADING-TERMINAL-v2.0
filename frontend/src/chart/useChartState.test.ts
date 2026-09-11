import { describe, expect, it } from "vitest";
import { DEFAULT_CHART_STATE } from "./types";

describe("ChartState defaults", () => {
  it("defaults to EURUSD M1 candlestick presentation state", () => {
    expect(DEFAULT_CHART_STATE.symbol).toBe("EURUSD");
    expect(DEFAULT_CHART_STATE.timeframe).toBe("M1");
    expect(DEFAULT_CHART_STATE.chartType).toBe("candlestick");
    expect(DEFAULT_CHART_STATE.viewportFrom).toBeNull();
  });
});
