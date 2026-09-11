import React, { createContext, useContext, useMemo, useState } from "react";
import { useLiveMarket, type UseLiveMarketResult } from "../../hooks/useLiveMarket";
import type { SymbolQuote } from "../../live/types";

export interface TerminalContextValue {
  selectedSymbol: string;
  setSelectedSymbol: (symbol: string) => void;
  liveMarket: UseLiveMarketResult;
  selectedQuote: SymbolQuote | null;
  supportedSymbols: readonly string[];
}

export const SUPPORTED_INSTRUMENTS = [
  // Forex Pairs
  "EUR/USD",
  "GBP/USD",
  "USD/JPY",
  "AUD/USD",
  "USD/CAD",
  "USD/CHF",
  "NZD/USD",
  "EUR/GBP",
  // Crypto Pairs
  "BTC/USD",
  "ETH/USD",
  "SOL/USD",
] as const;

const TerminalContext = createContext<TerminalContextValue | null>(null);

export interface TerminalProviderProps {
  children: React.ReactNode;
  initialSymbol?: string;
  enableLiveMarket?: boolean;
}

/**
 * TerminalProvider
 *
 * Provides shared active symbol selection and live market telemetry across
 * all docked terminal panes (Watchlist Dock, Chart Stage, Telemetry Panel, Ticker Header).
 */
export function TerminalProvider({
  children,
  initialSymbol = "EUR/USD",
  enableLiveMarket = true,
}: TerminalProviderProps) {
  const [selectedSymbol, setSelectedSymbol] = useState<string>(initialSymbol);
  const liveMarket = useLiveMarket(enableLiveMarket);

  const symbolKey = selectedSymbol.replace("/", "");
  const selectedQuote = liveMarket.quotes[selectedSymbol] ?? liveMarket.quotes[symbolKey] ?? null;

  const value = useMemo<TerminalContextValue>(
    () => ({
      selectedSymbol,
      setSelectedSymbol,
      liveMarket,
      selectedQuote,
      supportedSymbols: SUPPORTED_INSTRUMENTS,
    }),
    [selectedSymbol, liveMarket, selectedQuote],
  );

  return <TerminalContext.Provider value={value}>{children}</TerminalContext.Provider>;
}

export function useTerminal(): TerminalContextValue {
  const context = useContext(TerminalContext);
  if (!context) {
    throw new Error("useTerminal must be used within a TerminalProvider");
  }
  return context;
}
