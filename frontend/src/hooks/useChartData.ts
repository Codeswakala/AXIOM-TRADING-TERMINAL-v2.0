/**
 * Chart data hook — fetches historical candles and applies live WS updates.
 * Analytical computation is forbidden here; only mapping + series merge.
 */

import { useCallback, useEffect, useRef, useState } from "react";
import { fetchCandles } from "../api/client";
import { useLiveMarket } from "./useLiveMarket";
import {
  apiCandleToBar,
  mergeLiveBar,
  type CandleBar,
  type ChartLoadState,
  type ChartState,
} from "../chart/types";
import { parseCandleTime } from "../chart/types";

export type UseChartDataResult = {
  bars: CandleBar[];
  loadState: ChartLoadState;
  error: string | null;
  connectionState: ReturnType<typeof useLiveMarket>["connectionState"];
  feedRunning: boolean;
  lastLiveAt: string | null;
  reload: () => Promise<void>;
  startFeed: () => Promise<void>;
  stopFeed: () => Promise<void>;
};

export function useChartData(chartState: ChartState, enabled: boolean): UseChartDataResult {
  const [bars, setBars] = useState<CandleBar[]>([]);
  const [loadState, setLoadState] = useState<ChartLoadState>("idle");
  const [error, setError] = useState<string | null>(null);
  const live = useLiveMarket(enabled);
  const symbolRef = useRef(chartState.symbol);
  const timeframeRef = useRef(chartState.timeframe);

  symbolRef.current = chartState.symbol;
  timeframeRef.current = chartState.timeframe;

  const reload = useCallback(async () => {
    if (!enabled) return;
    setLoadState("loading");
    setError(null);
    try {
      const series = await fetchCandles({
        symbol: chartState.symbol,
        timeframe: chartState.timeframe,
        limit: 500,
        order: "asc",
      });
      if (series.kind === "unavailable") {
        // DATA-P02 M4: absence is honest — empty series, never improvised.
        setBars([]);
        setError(series.detail);
        setLoadState("empty");
        return;
      }
      const next = series.bars
        .map(apiCandleToBar)
        .filter((b) => b.time > 0 && Number.isFinite(b.open));
      setBars(next);
      setLoadState(next.length === 0 ? "empty" : "ready");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load candles");
      setLoadState("error");
    }
  }, [chartState.symbol, chartState.timeframe, enabled]);

  useEffect(() => {
    void reload();
  }, [reload]);

  // Apply live quote for matching symbol/timeframe
  useEffect(() => {
    if (!enabled) return;
    const q = live.quotes[chartState.symbol];
    if (!q) return;
    if (q.timeframe.toUpperCase() !== chartState.timeframe.toUpperCase()) return;

    const bar: CandleBar = {
      time: parseCandleTime(q.openTime),
      open: Number(q.open),
      high: Number(q.high),
      low: Number(q.low),
      close: Number(q.close),
      volume: q.volume != null ? Number(q.volume) : null,
    };
    if (bar.time <= 0 || !Number.isFinite(bar.close)) return;

    setBars((prev) => {
      const merged = mergeLiveBar(prev, bar);
      return merged;
    });
    setLoadState((s) => (s === "empty" || s === "idle" ? "ready" : s));
  }, [enabled, live.quotes, chartState.symbol, chartState.timeframe]);

  return {
    bars,
    loadState,
    error,
    connectionState: live.connectionState,
    feedRunning: live.feedStats?.running ?? false,
    lastLiveAt: live.lastMessageAt,
    reload,
    startFeed: live.startFeed,
    stopFeed: live.stopFeed,
  };
}
