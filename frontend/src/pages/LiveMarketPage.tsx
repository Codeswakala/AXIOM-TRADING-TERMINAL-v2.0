import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useLiveMarket } from "../hooks/useLiveMarket";
import { FeedHealthBar } from "../components/live/FeedHealthBar";
import { LivePriceTable } from "../components/live/LivePriceTable";

export function LiveMarketPage() {
  const { isAuthenticated } = useAuth();
  const live = useLiveMarket(isAuthenticated);
  const [busy, setBusy] = useState(false);
  const [actionError, setActionError] = useState<string | null>(null);

  async function handleStart() {
    setBusy(true);
    setActionError(null);
    try {
      await live.startFeed();
    } catch (err) {
      setActionError(err instanceof Error ? err.message : "Start failed");
    } finally {
      setBusy(false);
    }
  }

  async function handleStop() {
    setBusy(true);
    setActionError(null);
    try {
      await live.stopFeed();
    } catch (err) {
      setActionError(err instanceof Error ? err.message : "Stop failed");
    } finally {
      setBusy(false);
    }
  }

  if (!isAuthenticated) {
    return (
      <div className="page-header">
        <div>
          <h1>Live Market</h1>
          <p className="error-text">Authentication required to view live market data.</p>
        </div>
      </div>
    );
  }

  const expected = live.feedStats?.symbols?.length
    ? live.feedStats.symbols
    : ["EURUSD", "BTCUSD"];

  return (
    <>
      <div className="page-header">
        <div>
          <h1>Live Market Dashboard</h1>
          <p className="muted">
            Institutional live watchlist driven by the authenticated WebSocket channel
            (<span className="mono"> /ws/market</span>. Simulated multi-symbol feed (foundation).
            No charts or execution in this unit.
          </p>
        </div>
      </div>

      <div className="panel-grid">
        <FeedHealthBar
          connectionState={live.connectionState}
          lastMessageAt={live.lastMessageAt}
          messagesPerMinute={live.messagesPerMinute}
          messageCount={live.messageCount}
          lagHintMs={live.lagHintMs}
          reconnectCount={live.reconnectCount}
          feedStats={live.feedStats}
          error={actionError ?? live.error}
          onStart={() => void handleStart()}
          onStop={() => void handleStop()}
          onReconnect={live.reconnectNow}
          busy={busy}
        />
        <LivePriceTable quotes={live.quotes} expectedSymbols={expected} />
      </div>
    </>
  );
}
