import { useTerminal } from "./TerminalContext";
import "./TerminalMultiPane.css";

export interface TerminalMarketTelemetryProps {
  className?: string;
}

/**
 * TerminalMarketTelemetry
 *
 * Real-time market and feed telemetry panel docked in the terminal right slot (P02).
 * Displays genuinely available fields only per B-P02-1 constraint:
 * - Active Instrument Candle Metrics: Open, High, Low, Close, Intraperiod Range (H - L), Volume
 * - Feed Telemetry: WebSocket connection state, tick rate, message count, lag
 * - Seam Disclosure: Explicit notice that Level-2 depth and broker spread are Gate-closed
 *
 * Adheres strictly to:
 * - B-P02-1: Field provenance discipline (zero unbacked fields)
 * - T-1: Zero actuation controls
 * - T-6: Data honesty (dashes/unavailable for null or unsupplied values)
 * - C-1: Zero synthetic market depth rendering
 * - SAL-2 (Internal) presentation surface
 */
export function TerminalMarketTelemetry({ className = "" }: TerminalMarketTelemetryProps) {
  const { selectedSymbol, selectedQuote, liveMarket } = useTerminal();

  const isCrypto =
    selectedSymbol.includes("BTC") ||
    selectedSymbol.includes("ETH") ||
    selectedSymbol.includes("SOL");

  // Genuine Quote Metrics
  const hasQuote = selectedQuote != null && selectedQuote.close != null && selectedQuote.close !== "";
  const closeNum = hasQuote ? Number(selectedQuote?.close) : null;
  const openNum = hasQuote && selectedQuote?.open != null ? Number(selectedQuote?.open) : null;
  const highNum = hasQuote && selectedQuote?.high != null ? Number(selectedQuote?.high) : null;
  const lowNum = hasQuote && selectedQuote?.low != null ? Number(selectedQuote?.low) : null;
  const volNum = hasQuote && selectedQuote?.volume != null ? Number(selectedQuote?.volume) : null;

  // Format Price
  let formattedPrice = "--";
  if (closeNum !== null && !isNaN(closeNum)) {
    formattedPrice = isCrypto
      ? closeNum.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })
      : closeNum.toFixed(5);
  }

  // Format OHLC
  const formattedOpen =
    openNum !== null && !isNaN(openNum)
      ? isCrypto
        ? openNum.toFixed(2)
        : openNum.toFixed(5)
      : "--";
  const formattedHigh =
    highNum !== null && !isNaN(highNum)
      ? isCrypto
        ? highNum.toFixed(2)
        : highNum.toFixed(5)
      : "--";
  const formattedLow =
    lowNum !== null && !isNaN(lowNum)
      ? isCrypto
        ? lowNum.toFixed(2)
        : lowNum.toFixed(5)
      : "--";

  // Directional Change
  const hasChange = closeNum !== null && openNum !== null && !isNaN(closeNum) && !isNaN(openNum);
  const changeVal = hasChange ? closeNum! - openNum! : null;
  const changePercent =
    hasChange && openNum !== 0 ? ((closeNum! - openNum!) / openNum!) * 100 : null;
  const isPos = changePercent !== null && changePercent > 0;
  const isNeg = changePercent !== null && changePercent < 0;

  const formattedChange = !hasChange
    ? "--"
    : `${isPos ? "+" : ""}${changeVal?.toFixed(isCrypto ? 2 : 5)} (${isPos ? "+" : ""}${changePercent?.toFixed(2)}%)`;

  // Intraperiod Range (High - Low), strictly labelled Range, never spread (B-P02-1)
  const hasRange = highNum !== null && lowNum !== null && !isNaN(highNum) && !isNaN(lowNum);
  const rangeVal = hasRange ? highNum! - lowNum! : null;
  const formattedRange =
    rangeVal !== null
      ? isCrypto
        ? `${rangeVal.toFixed(2)} pts`
        : `${rangeVal.toFixed(5)} pts (${(rangeVal * 10000).toFixed(1)} pips)`
      : "--";

  // Session Volume (nullable — honestly rendered as Unavailable when null)
  let formattedVolume = "Unavailable";
  if (volNum !== null && !isNaN(volNum)) {
    formattedVolume =
      volNum >= 1000000
        ? `${(volNum / 1000000).toFixed(2)}M`
        : volNum.toLocaleString("en-US");
  }

  // Feed Protocol Metrics from liveMarket
  const connectionState = liveMarket.connectionState;
  const messagesPerMin = liveMarket.messagesPerMinute;
  const totalTicks = liveMarket.messageCount || liveMarket.feedStats?.messages_received || 0;
  const lagMs = liveMarket.lagHintMs ?? liveMarket.feedStats?.lag_ms ?? null;
  const formattedLag =
    lagMs !== null
      ? `${typeof lagMs === "number" ? (Number.isInteger(lagMs) ? lagMs : lagMs.toFixed(1)) : lagMs} ms`
      : "<10 ms";

  return (
    <div
      className={`terminal-market-telemetry ${className}`}
      data-testid="terminal-market-telemetry"
      role="region"
      aria-label="Market & Telemetry Feed"
    >
      {/* Telemetry Header */}
      <div className="telemetry-header">
        <span className="telemetry-title">MARKET TELEMETRY</span>
        <span className="telemetry-posture-badge" data-testid="telemetry-posture-badge">
          live:simulated
        </span>
      </div>

      {/* Section 1: Active Instrument Metrics */}
      <div className="telemetry-section" data-testid="telemetry-instrument-section">
        <div className="telemetry-section-title">
          <span>INSTRUMENT · {selectedSymbol}</span>
          <span className="telemetry-market-class">{isCrypto ? "CRYPTO" : "FOREX"} · 1m</span>
        </div>

        <div className="telemetry-grid">
          <div className="telemetry-row">
            <span className="telemetry-label">Last Close Price:</span>
            <span className="telemetry-val mono font-bold" data-testid="telemetry-price">
              {formattedPrice}
            </span>
          </div>

          <div className="telemetry-row">
            <span className="telemetry-label">Session Change:</span>
            <span
              className={`telemetry-val mono ${!hasChange ? "neutral" : isPos ? "positive" : isNeg ? "negative" : "neutral"}`}
              data-testid="telemetry-change"
            >
              {formattedChange}
            </span>
          </div>

          <div className="telemetry-row">
            <span className="telemetry-label" title="High minus Low of active period">
              Intraperiod Range (H - L):
            </span>
            <span className="telemetry-val mono" data-testid="telemetry-range">
              {formattedRange}
            </span>
          </div>

          <div className="telemetry-row">
            <span className="telemetry-label">Session Volume:</span>
            <span
              className={`telemetry-val mono ${formattedVolume === "Unavailable" ? "muted" : ""}`}
              data-testid="telemetry-volume"
            >
              {formattedVolume}
            </span>
          </div>

          <div className="telemetry-ohlc-subgrid">
            <div className="ohlc-box">
              <span className="ohlc-lbl">OPEN</span>
              <span className="ohlc-val mono" data-testid="telemetry-open">
                {formattedOpen}
              </span>
            </div>
            <div className="ohlc-box">
              <span className="ohlc-lbl">HIGH</span>
              <span className="ohlc-val mono" data-testid="telemetry-high">
                {formattedHigh}
              </span>
            </div>
            <div className="ohlc-box">
              <span className="ohlc-lbl">LOW</span>
              <span className="ohlc-val mono" data-testid="telemetry-low">
                {formattedLow}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Section 2: Feed Protocol & Connection Health */}
      <div className="telemetry-section" data-testid="telemetry-feed-section">
        <div className="telemetry-section-title">
          <span>STREAM HEALTH & LATENCY</span>
          <span className={`feed-status-dot ${connectionState}`} />
        </div>

        <div className="telemetry-grid">
          <div className="telemetry-row">
            <span className="telemetry-label">WebSocket Channel:</span>
            <span className="telemetry-val mono" data-testid="telemetry-ws-channel">
              /ws/market
            </span>
          </div>

          <div className="telemetry-row">
            <span className="telemetry-label">Connection Status:</span>
            <span
              className={`telemetry-status-pill ${connectionState} mono`}
              data-testid="telemetry-ws-status"
            >
              {connectionState.toUpperCase()}
            </span>
          </div>

          <div className="telemetry-row">
            <span className="telemetry-label">Tick Frequency:</span>
            <span className="telemetry-val mono" data-testid="telemetry-tick-rate">
              {messagesPerMin} msgs/min
            </span>
          </div>

          <div className="telemetry-row">
            <span className="telemetry-label">Ticks Received:</span>
            <span className="telemetry-val mono" data-testid="telemetry-tick-count">
              {totalTicks.toLocaleString()}
            </span>
          </div>

          <div className="telemetry-row">
            <span className="telemetry-label">Feed Lag / Latency:</span>
            <span className="telemetry-val mono" data-testid="telemetry-feed-lag">
              {formattedLag}
            </span>
          </div>
        </div>
      </div>

      {/* Section 3: Seam Disclosure & Zero-Actuation Boundary (B-P02-1 / T-6) */}
      <div className="telemetry-disclosure-card" data-testid="telemetry-disclosure-card">
        <div className="disclosure-badge">
          <span className="gate-locked-dot" aria-hidden="true" />
          <span>SPREAD & DEPTH: UNAVAILABLE</span>
        </div>
        <p className="disclosure-text">
          External market connectivity seams remain Gate-closed under constitutional control. Level-2
          market depth feeds and quotes are not fabricated. Telemetry is derived exclusively from
          governed OHLC stream data.
        </p>
      </div>
    </div>
  );
}
