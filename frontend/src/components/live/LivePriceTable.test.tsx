import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { LivePriceTable } from "./LivePriceTable";
import type { SymbolQuote } from "../../live/types";

const sample: Record<string, SymbolQuote> = {
  EURUSD: {
    symbol: "EURUSD",
    marketClass: "forex",
    timeframe: "M1",
    open: "1.10000",
    high: "1.10100",
    low: "1.09900",
    close: "1.10050",
    volume: "100",
    openTime: "2024-01-01T00:00:00Z",
    source: "live:simulated",
    updatedAt: "2024-01-01T00:00:01Z",
    flash: "up",
  },
  BTCUSD: {
    symbol: "BTCUSD",
    marketClass: "crypto",
    timeframe: "M1",
    open: "42000",
    high: "42100",
    low: "41900",
    close: "42050",
    volume: "12",
    openTime: "2024-01-01T00:00:00Z",
    source: "live:simulated",
    updatedAt: "2024-01-01T00:00:01Z",
    flash: null,
  },
};

describe("LivePriceTable", () => {
  it("renders multiple symbol rows", () => {
    render(<LivePriceTable quotes={sample} expectedSymbols={["EURUSD", "BTCUSD"]} />);
    expect(screen.getByText("EURUSD")).toBeInTheDocument();
    expect(screen.getByText("BTCUSD")).toBeInTheDocument();
    expect(screen.getByText("Live Prices")).toBeInTheDocument();
  });

  it("shows waiting state for missing expected symbols", () => {
    render(<LivePriceTable quotes={{}} expectedSymbols={["EURUSD"]} />);
    expect(screen.getByText("Waiting for tick…")).toBeInTheDocument();
  });
});
