/**
 * Chart State — presentation only (05_SYSTEM_ARCHITECTURE §30).
 * Holds symbol/timeframe/chartType/viewport; does not fetch or compute analytics.
 */

import { useCallback, useState } from "react";
import {
  AVAILABLE_SYMBOLS,
  AVAILABLE_TIMEFRAMES,
  DEFAULT_CHART_STATE,
  type ChartState,
  type ChartTimeframe,
  type ChartType,
} from "./types";

export function useChartState(initial: Partial<ChartState> = {}) {
  const [state, setState] = useState<ChartState>({ ...DEFAULT_CHART_STATE, ...initial });

  const setSymbol = useCallback((symbol: string) => {
    setState((s) => ({ ...s, symbol: symbol.toUpperCase() }));
  }, []);

  const setTimeframe = useCallback((timeframe: ChartTimeframe) => {
    setState((s) => ({ ...s, timeframe }));
  }, []);

  const setChartType = useCallback((chartType: ChartType) => {
    setState((s) => ({ ...s, chartType }));
  }, []);

  const setViewport = useCallback((from: number | null, to: number | null) => {
    setState((s) => ({ ...s, viewportFrom: from, viewportTo: to }));
  }, []);

  return {
    state,
    setSymbol,
    setTimeframe,
    setChartType,
    setViewport,
    availableSymbols: [...AVAILABLE_SYMBOLS],
    availableTimeframes: AVAILABLE_TIMEFRAMES,
  };
}
