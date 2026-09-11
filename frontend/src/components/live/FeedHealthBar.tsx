import type { LiveConnectionState, LiveMarketStats } from "../../live/types";
import { StatusPill } from "../StatusPill";

type Props = {
  connectionState: LiveConnectionState;
  lastMessageAt: string | null;
  messagesPerMinute: number;
  messageCount: number;
  lagHintMs: number | null;
  reconnectCount: number;
  feedStats: LiveMarketStats | null;
  error: string | null;
  onStart: () => void;
  onStop: () => void;
  onReconnect: () => void;
  busy?: boolean;
};

function pillState(state: LiveConnectionState): "ok" | "error" | "loading" {
  if (state === "connected") return "ok";
  if (state === "connecting" || state === "reconnecting") return "loading";
  return "error";
}

export function FeedHealthBar({
  connectionState,
  lastMessageAt,
  messagesPerMinute,
  messageCount,
  lagHintMs,
  reconnectCount,
  feedStats,
  error,
  onStart,
  onStop,
  onReconnect,
  busy,
}: Props) {
  return (
    <section className="panel span-12 feed-health">
      <div className="feed-health-row">
        <div>
          <h2>Live Feed Health</h2>
          <div className="feed-health-pills">
            <StatusPill state={pillState(connectionState)} label={connectionState} />
            <span className={`badge ${feedStats?.running ? "up" : "degraded"}`}>
              adapter {feedStats?.running ? "running" : "stopped"}
            </span>
            {feedStats?.adapter ? (
              <span className="badge stub mono">{feedStats.adapter}</span>
            ) : null}
          </div>
        </div>
        <div className="feed-actions">
          <button type="button" className="btn primary" disabled={busy} onClick={onStart}>
            Start feed
          </button>
          <button type="button" className="btn" disabled={busy} onClick={onStop}>
            Stop feed
          </button>
          <button type="button" className="btn" disabled={busy} onClick={onReconnect}>
            Reconnect WS
          </button>
        </div>
      </div>

      <dl className="kv feed-kv">
        <dt>Last update</dt>
        <dd className="mono">{lastMessageAt ?? "—"}</dd>
        <dt>Messages (session)</dt>
        <dd className="mono">{messageCount}</dd>
        <dt>Rate (approx)</dt>
        <dd className="mono">{messagesPerMinute}/min</dd>
        <dt>Lag hint</dt>
        <dd className="mono">{lagHintMs != null ? `${Math.round(lagHintMs)} ms` : "—"}</dd>
        <dt>Server lag</dt>
        <dd className="mono">
          {feedStats?.lag_ms != null ? `${Math.round(feedStats.lag_ms)} ms` : "—"}
        </dd>
        <dt>WS reconnects</dt>
        <dd className="mono">{reconnectCount}</dd>
        <dt>Symbols</dt>
        <dd className="mono">{(feedStats?.symbols ?? []).join(", ") || "—"}</dd>
        <dt>Persisted</dt>
        <dd className="mono">{feedStats?.persist_count ?? "—"}</dd>
      </dl>
      {error ? <p className="error-text">{error}</p> : null}
    </section>
  );
}
