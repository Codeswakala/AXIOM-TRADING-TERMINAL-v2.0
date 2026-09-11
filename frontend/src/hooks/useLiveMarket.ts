/**
 * Authenticated live market WebSocket consumer with reconnection.
 *
 * Only active when `enabled` is true (caller must gate on auth).
 */

import { useCallback, useEffect, useRef, useState } from "react";
import { getAccessToken } from "../auth/tokenStorage";
import {
  fetchLiveMarketStats,
  fetchWsTicket,
  getLiveMarketWebSocketUrlWithTicket,
  startLiveMarket,
  stopLiveMarket,
} from "../api/client";
import {
  isLiveCandle,
  type LiveConnectionState,
  type LiveMarketMessage,
  type LiveMarketStats,
  type SymbolQuote,
} from "../live/types";

const MAX_BACKOFF_MS = 15000;
const BASE_BACKOFF_MS = 1000;

export type UseLiveMarketResult = {
  connectionState: LiveConnectionState;
  quotes: Record<string, SymbolQuote>;
  messageCount: number;
  lastMessageAt: string | null;
  messagesPerMinute: number;
  lagHintMs: number | null;
  error: string | null;
  feedStats: LiveMarketStats | null;
  reconnectCount: number;
  startFeed: () => Promise<void>;
  stopFeed: () => Promise<void>;
  refreshStats: () => Promise<void>;
  reconnectNow: () => void;
};

function parseMessage(raw: string): LiveMarketMessage | null {
  try {
    return JSON.parse(raw) as LiveMarketMessage;
  } catch {
    return null;
  }
}

export function useLiveMarket(enabled: boolean): UseLiveMarketResult {
  const [connectionState, setConnectionState] = useState<LiveConnectionState>("idle");
  const [quotes, setQuotes] = useState<Record<string, SymbolQuote>>({});
  const [messageCount, setMessageCount] = useState(0);
  const [lastMessageAt, setLastMessageAt] = useState<string | null>(null);
  const [messagesPerMinute, setMessagesPerMinute] = useState(0);
  const [lagHintMs, setLagHintMs] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [feedStats, setFeedStats] = useState<LiveMarketStats | null>(null);
  const [reconnectCount, setReconnectCount] = useState(0);
  const [reconnectTick, setReconnectTick] = useState(0);

  const wsRef = useRef<WebSocket | null>(null);
  const intentionalClose = useRef(false);
  const attemptRef = useRef(0);
  const timestampsRef = useRef<number[]>([]);
  const prevCloseRef = useRef<Record<string, number>>({});

  const refreshStats = useCallback(async () => {
    if (!enabled) return;
    try {
      const stats = await fetchLiveMarketStats();
      setFeedStats(stats);
      if (stats.lag_ms != null) setLagHintMs(stats.lag_ms);
      // Seed quotes from server snapshot when available
      if (stats.latest_by_symbol) {
        setQuotes((prev) => {
          const next = { ...prev };
          for (const [symbol, candle] of Object.entries(stats.latest_by_symbol)) {
            next[symbol] = {
              symbol: candle.symbol,
              marketClass: candle.market_class,
              timeframe: candle.timeframe,
              open: candle.open,
              high: candle.high,
              low: candle.low,
              close: candle.close,
              volume: candle.volume,
              openTime: candle.open_time,
              source: candle.source,
              updatedAt: candle.received_at ?? new Date().toISOString(),
              flash: null,
            };
          }
          return next;
        });
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load live stats");
    }
  }, [enabled]);

  const startFeed = useCallback(async () => {
    await startLiveMarket();
    await refreshStats();
  }, [refreshStats]);

  const stopFeed = useCallback(async () => {
    await stopLiveMarket();
    await refreshStats();
  }, [refreshStats]);

  const reconnectNow = useCallback(() => {
    setReconnectTick((n) => n + 1);
  }, []);

  // Rate window (messages / last 60s)
  useEffect(() => {
    if (!enabled) return;
    const id = window.setInterval(() => {
      const cutoff = Date.now() - 60_000;
      timestampsRef.current = timestampsRef.current.filter((t) => t >= cutoff);
      setMessagesPerMinute(timestampsRef.current.length);
    }, 2000);
    return () => window.clearInterval(id);
  }, [enabled]);

  // Stats poll while authenticated
  useEffect(() => {
    if (!enabled) return;
    void refreshStats();
    const id = window.setInterval(() => void refreshStats(), 5000);
    return () => window.clearInterval(id);
  }, [enabled, refreshStats]);

  // WebSocket lifecycle
  useEffect(() => {
    if (!enabled) {
      intentionalClose.current = true;
      wsRef.current?.close();
      wsRef.current = null;
      setConnectionState("idle");
      return;
    }

    let cancelled = false;
    let reconnectTimer: number | undefined;

    const connect = () => {
      void (async () => {
        if (!getAccessToken()) {
          setConnectionState("error");
          setError("No access token — sign in required");
          return;
        }
        if (cancelled) return;

        intentionalClose.current = false;
        setConnectionState(attemptRef.current === 0 ? "connecting" : "reconnecting");
        setError(null);

        let ticket: string;
        try {
          const issued = await fetchWsTicket();
          ticket = issued.ticket;
        } catch (err) {
          if (cancelled) return;
          setConnectionState("error");
          setError(err instanceof Error ? err.message : "Failed to issue WS ticket");
          return;
        }
        if (cancelled) return;

        let socket: WebSocket;
        try {
          // Short-lived ticket in query — not the long-lived access JWT (W0-U08)
          socket = new WebSocket(getLiveMarketWebSocketUrlWithTicket(ticket));
        } catch {
          setConnectionState("error");
          setError("Failed to open WebSocket");
          return;
        }
        wsRef.current = socket;

        socket.onopen = () => {
          if (cancelled) return;
          attemptRef.current = 0;
          setConnectionState("connected");
          setError(null);
        };

        socket.onmessage = (event) => {
          if (cancelled) return;
          const msg = parseMessage(String(event.data));
          if (!msg) return;

          if (isLiveCandle(msg)) {
            const now = Date.now();
            timestampsRef.current.push(now);
            setMessageCount((c) => c + 1);
            setLastMessageAt(new Date(now).toISOString());

            const closeNum = Number(msg.close);
            const prev = prevCloseRef.current[msg.symbol];
            let flash: "up" | "down" | null = null;
            if (prev != null && !Number.isNaN(closeNum)) {
              if (closeNum > prev) flash = "up";
              else if (closeNum < prev) flash = "down";
            }
            if (!Number.isNaN(closeNum)) prevCloseRef.current[msg.symbol] = closeNum;

            if (msg.received_at) {
              const lag = now - Date.parse(msg.received_at);
              if (!Number.isNaN(lag)) setLagHintMs(Math.max(0, lag));
            }

            setQuotes((prevQuotes) => ({
              ...prevQuotes,
              [msg.symbol]: {
                symbol: msg.symbol,
                marketClass: msg.market_class,
                timeframe: msg.timeframe,
                open: msg.open,
                high: msg.high,
                low: msg.low,
                close: msg.close,
                volume: msg.volume,
                openTime: msg.open_time,
                source: msg.source,
                updatedAt: msg.received_at ?? new Date(now).toISOString(),
                flash,
              },
            }));
          }
        };

        socket.onerror = () => {
          if (cancelled) return;
          setError("WebSocket error");
        };

        socket.onclose = () => {
          if (cancelled || intentionalClose.current) {
            setConnectionState("disconnected");
            return;
          }
          setConnectionState("reconnecting");
          attemptRef.current += 1;
          setReconnectCount((c) => c + 1);
          const delay = Math.min(
            MAX_BACKOFF_MS,
            BASE_BACKOFF_MS * 2 ** Math.min(attemptRef.current, 4),
          );
          reconnectTimer = window.setTimeout(connect, delay);
        };
      })();
    };

    connect();

    return () => {
      cancelled = true;
      intentionalClose.current = true;
      if (reconnectTimer) window.clearTimeout(reconnectTimer);
      wsRef.current?.close();
      wsRef.current = null;
    };
  }, [enabled, reconnectTick]);

  return {
    connectionState,
    quotes,
    messageCount,
    lastMessageAt,
    messagesPerMinute,
    lagHintMs,
    error,
    feedStats,
    reconnectCount,
    startFeed,
    stopFeed,
    refreshStats,
    reconnectNow,
  };
}
