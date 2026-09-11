/** TypeScript models for live market WebSocket messages (W0-U06). */

export type LiveConnectionState =
  | "idle"
  | "connecting"
  | "connected"
  | "reconnecting"
  | "disconnected"
  | "error";

export type LiveCandleMessage = {
  type: "live_candle";
  channel: "market";
  market_class: string;
  symbol: string;
  timeframe: string;
  open_time: string;
  open: string;
  high: string;
  low: string;
  close: string;
  volume: string | null;
  source: string | null;
  received_at?: string;
  persist_action?: string;
  candle_id?: string;
  persist_error?: string;
};

export type LiveSubscribedMessage = {
  type: "subscribed";
  channel: string;
  symbol?: string;
  timeframe?: string;
  running?: boolean;
  message?: string;
};

export type LivePongMessage = {
  type: "pong";
  stats?: {
    running?: boolean;
    subscribers?: number;
  };
};

export type LiveMarketMessage =
  | LiveCandleMessage
  | LiveSubscribedMessage
  | LivePongMessage
  | { type: string; [key: string]: unknown };

export type SymbolQuote = {
  symbol: string;
  marketClass: string;
  timeframe: string;
  open: string;
  high: string;
  low: string;
  close: string;
  volume: string | null;
  openTime: string;
  source: string | null;
  updatedAt: string;
  flash?: "up" | "down" | null;
};

export type LiveMarketStats = {
  running: boolean;
  auto_start: boolean;
  adapter: string | null;
  connected: boolean;
  market_class: string;
  symbol: string;
  symbols: string[];
  timeframe: string;
  messages_received: number;
  persist_count: number;
  persist_errors: number;
  lag_ms: number | null;
  last_message_at: string | null;
  last_persisted_at: string | null;
  started_at: string | null;
  subscribers: number;
  last_candle: LiveCandleMessage | null;
  latest_by_symbol: Record<string, LiveCandleMessage>;
  last_error: string | null;
  reconnect_count: number;
  adapter_details: Record<string, unknown>;
};

export function isLiveCandle(msg: LiveMarketMessage): msg is LiveCandleMessage {
  return msg.type === "live_candle" && typeof (msg as LiveCandleMessage).symbol === "string";
}
