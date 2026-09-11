import { useEffect, useState } from "react";
import { TerminalGovernanceBadge } from "./TerminalGovernanceBadge";
import "./TerminalMultiPane.css";

export type WebSocketFeedStatus = "live" | "connecting" | "disconnected" | "degraded" | "empty" | "idle";

export interface TickerMarketData {
  symbol?: string | null;
  price?: number | string | null;
  change24h?: number | string | null;
  change24hPercent?: number | string | null;
  high24h?: number | string | null;
  low24h?: number | string | null;
  volume24h?: string | number | null;
  range?: number | string | null;
  spread?: number | string | null;
  timestamp?: string | null;
  posture?: "live:simulated" | "seed:synthetic" | "disconnected" | "unavailable";
}

export interface TerminalTopTickerProps {
  symbol?: string | null;
  marketData?: TickerMarketData | null;
  wsStatus?: WebSocketFeedStatus;
  showGovernanceBadge?: boolean;
  className?: string;
  initialClockUtc?: string;
}

/**
 * TerminalTopTicker
 *
 * Persistent global ticker header: symbol, price, 24h change, high/low,
 * session clock, WebSocket connection status, and governance badge.
 *
 * Adheres strictly to:
 * - T-1: Zero actuation controls
 * - T-6: Data honesty (unavailable states explicitly labelled, never fabricated)
 * - Doc 16 Brand Standards & Optical Monospace Precision
 * - SAL-2 (Internal) presentation surface
 */
export function TerminalTopTicker({
  symbol = "EUR/USD",
  marketData = null,
  wsStatus = "disconnected",
  showGovernanceBadge = true,
  className = "",
  initialClockUtc,
}: TerminalTopTickerProps) {
  const [clockUtc, setClockUtc] = useState<string>(() => {
    if (initialClockUtc) return initialClockUtc;
    const now = new Date();
    return now.toTimeString().slice(0, 8) + " UTC";
  });

  useEffect(() => {
    const timer = window.setInterval(() => {
      const now = new Date();
      const hours = String(now.getUTCHours()).padStart(2, "0");
      const minutes = String(now.getUTCMinutes()).padStart(2, "0");
      const seconds = String(now.getUTCSeconds()).padStart(2, "0");
      setClockUtc(`${hours}:${minutes}:${seconds} UTC`);
    }, 1000);
    return () => window.clearInterval(timer);
  }, []);

  const activeSymbol = symbol || "NO SYMBOL";
  const hasPrice = marketData != null && marketData.price != null && marketData.price !== "";
  const priceValue = hasPrice ? Number(marketData?.price) : null;
  const isPriceValidNumber = priceValue !== null && !isNaN(priceValue);

  // Format price honestly
  let formattedPrice: string;
  let priceStateClass = "normal";

  if (wsStatus === "connecting" && !hasPrice) {
    formattedPrice = "Loading…";
    priceStateClass = "loading";
  } else if (wsStatus === "disconnected" && !hasPrice) {
    formattedPrice = "Disconnected";
    priceStateClass = "disconnected";
  } else if (wsStatus === "empty" && !hasPrice) {
    formattedPrice = "Empty Feed";
    priceStateClass = "empty";
  } else if (!hasPrice) {
    formattedPrice = "--";
    priceStateClass = "unavailable";
  } else if (isPriceValidNumber && priceValue !== null) {
    const isCrypto = activeSymbol.includes("BTC") || activeSymbol.includes("ETH");
    formattedPrice = isCrypto
      ? priceValue.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })
      : priceValue.toFixed(5);
  } else {
    formattedPrice = String(marketData?.price);
  }

  // Format 24h change honestly
  const hasChange =
    marketData != null &&
    (marketData.change24hPercent != null || marketData.change24h != null);
  const changePercent = hasChange ? Number(marketData?.change24hPercent ?? 0) : null;
  const isChangePositive = changePercent !== null && changePercent > 0;
  const isChangeNegative = changePercent !== null && changePercent < 0;

  const changeClass = !hasChange
    ? "neutral"
    : isChangePositive
      ? "positive"
      : isChangeNegative
        ? "negative"
        : "neutral";

  const formattedChange = !hasChange
    ? "--"
    : `${isChangePositive ? "+" : ""}${changePercent?.toFixed(2)}%`;

  // Format high/low honestly
  const hasHighLow =
    marketData != null && marketData.high24h != null && marketData.low24h != null;
  const formattedHighLow = hasHighLow
    ? `H: ${Number(marketData?.high24h).toFixed(5)} L: ${Number(marketData?.low24h).toFixed(5)}`
    : "H: -- L: --";

  // Posture
  const posture = marketData?.posture ?? "live:simulated";

  return (
    <div
      className={`terminal-top-ticker ${className}`}
      data-testid="terminal-top-ticker"
      role="region"
      aria-label="Terminal Live Ticker"
    >
      {/* Left Group: Brand, Symbol, Price, Change */}
      <div className="ticker-left-group">
        <div className="ticker-brand-badge" data-testid="ticker-brand-badge">
          <span className="ticker-brand-mark" aria-hidden="true">
            AX
          </span>
          <span>AXIOM TERMINAL</span>
        </div>

        <div className="ticker-symbol-badge" data-testid="ticker-symbol-badge">
          {activeSymbol}
        </div>

        <div
          className={`ticker-price-metric ${priceStateClass}`}
          data-testid="ticker-price-metric"
        >
          {formattedPrice}
        </div>

        <div
          className={`ticker-change-metric ${changeClass}`}
          data-testid="ticker-change-metric"
        >
          {formattedChange}
        </div>
      </div>

      {/* Center Group: Telemetry (Spread, Volume, High/Low) */}
      <div className="ticker-center-group">
        <div className="ticker-telemetry-item" data-testid="ticker-spread">
          <span className="ticker-telemetry-label">SPREAD:</span>
          <span className="ticker-telemetry-value">
            {marketData?.spread != null ? `${marketData.spread} pts` : "--"}
          </span>
        </div>

        <div className="ticker-telemetry-item" data-testid="ticker-volume">
          <span className="ticker-telemetry-label">VOL:</span>
          <span className="ticker-telemetry-value">
            {marketData?.volume24h != null ? String(marketData.volume24h) : "--"}
          </span>
        </div>

        <div className="ticker-telemetry-item" data-testid="ticker-high-low">
          <span className="ticker-telemetry-value">{formattedHighLow}</span>
        </div>
      </div>

      {/* Right Group: WebSocket Status, Clock, Posture & Governance Badge */}
      <div className="ticker-right-group">
        <div
          className={`ticker-ws-badge ${wsStatus}`}
          data-testid="ticker-ws-badge"
          aria-label={`WebSocket status: ${wsStatus}`}
        >
          <span className="ticker-ws-dot" aria-hidden="true" />
          <span>
            {wsStatus === "live"
              ? "WS: LIVE [●]"
              : wsStatus === "connecting"
                ? "WS: CONNECTING [○]"
                : wsStatus === "disconnected"
                  ? "WS: DISCONNECTED [○]"
                  : wsStatus === "degraded"
                    ? "WS: DEGRADED [○]"
                    : "WS: IDLE [○]"}
          </span>
        </div>

        <div className="ticker-posture-badge" data-testid="ticker-posture-badge">
          {posture}
        </div>

        <div className="ticker-clock-badge" data-testid="ticker-clock-badge">
          {clockUtc}
        </div>

        {showGovernanceBadge ? (
          <TerminalGovernanceBadge compact={false} />
        ) : null}
      </div>
    </div>
  );
}
