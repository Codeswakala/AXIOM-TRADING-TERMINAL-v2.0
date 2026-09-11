import { useEffect, useMemo, useState } from "react";
import { useTerminal } from "./TerminalContext";
import { fetchCandles, type ApiCandle } from "../../api/client";
import "./TerminalMultiPane.css";

export type AssetCategory = "ALL" | "FX" | "CRYPTO";

export interface TerminalWatchlistDockProps {
  onSymbolSelect?: (symbol: string) => void;
  className?: string;
}

/** DATA-P01: per-symbol sparkline state. One code path per statistic — the
 * sparkline is rendered from the same seeded candle series the chart stage
 * consumes (fetchCandles); nothing is synthesised at render time. */
type SparklineState =
  | { status: "loading" }
  | { status: "error" }
  | { status: "ready"; candles: ApiCandle[] };

/** M2: provenance label derived directly from the candles' source field. */
function candleProvenance(candles: ApiCandle[]): string | null {
  if (candles.length === 0) return null;
  const hasSeed = candles.some((c) => c.source === "seed:synthetic");
  const hasLive = candles.some((c) => c.source === "live:simulated");
  if (hasSeed && hasLive) return "SEED:SYNTHETIC + LIVE:SIMULATED";
  if (hasSeed) return "SEED:SYNTHETIC";
  if (hasLive) return "LIVE:SIMULATED";
  return null;
}

/** M2/M3: price provenance from the quote's source field. "LIVE" never
 * renders alone — the simulated qualifier is always present. */
function quoteProvenance(source: string | null | undefined): string | null {
  if (!source) return null;
  const s = source.toLowerCase();
  if (s.includes("simulated")) return "LIVE:SIMULATED";
  if (s.includes("synthetic") || s.includes("seed")) return "SEED:SYNTHETIC";
  return null;
}

function SparklineSvg({ closes }: { closes: number[] }) {
  if (closes.length < 2) return null;
  const width = 64;
  const height = 16;
  const min = Math.min(...closes);
  const max = Math.max(...closes);
  const span = max - min || 1;
  const points = closes
    .map((value, index) => {
      const x = (index / (closes.length - 1)) * width;
      const y = height - 2 - ((value - min) / span) * (height - 4);
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    })
    .join(" ");
  return (
    <svg
      width={width}
      height={height}
      viewBox={`0 0 ${width} ${height}`}
      aria-hidden="true"
      className="watchlist-sparkline-svg"
    >
      <polyline points={points} fill="none" stroke="currentColor" strokeWidth="1.2" />
    </svg>
  );
}

/**
 * TerminalWatchlistDock
 *
 * Multi-asset watchlist docked in the terminal left slot (P02).
 * Displays live simulated prices, percentage change, and intraperiod range across Forex and Crypto.
 * DATA-P01: adds per-symbol sparklines rendered from the seeded candle series,
 * with provenance labels on both the price and the sparkline (M2/M3).
 *
 * Adheres strictly to:
 * - T-1: Zero execution or order placement affordances
 * - T-6: Data honesty (unavailable states explicitly labelled with dashes, never fabricated)
 * - C-1: Zero synthetic market depth rendering
 * - Doc 16 Brand Standards & Pure Token Consumption
 * - SAL-2 (Internal) presentation surface
 */
export function TerminalWatchlistDock({
  onSymbolSelect,
  className = "",
}: TerminalWatchlistDockProps) {
  const { selectedSymbol, setSelectedSymbol, liveMarket, supportedSymbols } = useTerminal();
  const [searchQuery, setSearchQuery] = useState("");
  const [categoryFilter, setCategoryFilter] = useState<AssetCategory>("ALL");
  const [sparklines, setSparklines] = useState<Record<string, SparklineState>>({});

  // DATA-P01 S4/R1: fetch the seeded candle series per symbol for sparklines.
  // Each symbol degrades independently — one failing fetch removes only that
  // symbol's sparkline, never its price row or the watchlist.
  useEffect(() => {
    let cancelled = false;
    for (const sym of supportedSymbols) {
      const symKey = sym.replace("/", "");
      setSparklines((current) => ({ ...current, [symKey]: { status: "loading" } }));
      fetchCandles({ symbol: symKey, timeframe: "M1", limit: 30, order: "asc" })
        .then((series) => {
          if (cancelled) return;
          if (series.kind === "native") {
            setSparklines((current) => ({
              ...current,
              [symKey]: { status: "ready", candles: series.bars },
            }));
          } else {
            // DATA-P02 M4: a non-native response for M1 means the series is
            // unavailable — degrade this symbol's sparkline honestly.
            setSparklines((current) => ({ ...current, [symKey]: { status: "error" } }));
          }
        })
        .catch(() => {
          if (cancelled) return;
          setSparklines((current) => ({ ...current, [symKey]: { status: "error" } }));
        });
    }
    return () => {
      cancelled = true;
    };
  }, [supportedSymbols]);

  const handleSelect = (symbol: string) => {
    setSelectedSymbol(symbol);
    if (onSymbolSelect) onSymbolSelect(symbol);
  };

  const filteredSymbols = useMemo(() => {
    return supportedSymbols.filter((sym) => {
      const matchesSearch = sym.toLowerCase().includes(searchQuery.toLowerCase().trim());
      const isCrypto = sym.includes("BTC") || sym.includes("ETH") || sym.includes("SOL");
      const matchesCategory =
        categoryFilter === "ALL" ||
        (categoryFilter === "FX" && !isCrypto) ||
        (categoryFilter === "CRYPTO" && isCrypto);
      return matchesSearch && matchesCategory;
    });
  }, [supportedSymbols, searchQuery, categoryFilter]);

  return (
    <div
      className={`terminal-watchlist-dock ${className}`}
      data-testid="terminal-watchlist-dock"
      role="region"
      aria-label="Market Watchlist"
    >
      {/* Watchlist Header & Search */}
      <div className="watchlist-header">
        <div className="watchlist-title-row">
          <span className="watchlist-title">WATCHLIST</span>
          <span className="watchlist-count-badge" data-testid="watchlist-count">
            {filteredSymbols.length} PAIRS
          </span>
        </div>

        {/* Search Input */}
        <div className="watchlist-search-box">
          <input
            type="text"
            className="watchlist-search-input"
            placeholder="Search symbols..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            aria-label="Search instruments"
            data-testid="watchlist-search-input"
          />
          {searchQuery ? (
            <button
              type="button"
              className="watchlist-clear-search"
              onClick={() => setSearchQuery("")}
              aria-label="Clear search"
            >
              ×
            </button>
          ) : null}
        </div>

        {/* Category Filter Tabs */}
        <div className="watchlist-filter-tabs" role="tablist" aria-label="Asset Class Filter">
          {(["ALL", "FX", "CRYPTO"] as const).map((cat) => (
            <button
              key={cat}
              type="button"
              role="tab"
              aria-selected={categoryFilter === cat}
              className={`watchlist-tab-btn ${categoryFilter === cat ? "active" : ""}`}
              onClick={() => setCategoryFilter(cat)}
              data-testid={`watchlist-tab-${cat.toLowerCase()}`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Watchlist Instrument Rows */}
      <div className="watchlist-rows-container" role="list" aria-label="Instrument Quotes">
        {filteredSymbols.length === 0 ? (
          <div className="watchlist-empty-state" data-testid="watchlist-no-results">
            <span className="empty-text">No matching instruments found</span>
          </div>
        ) : (
          filteredSymbols.map((sym) => {
            const isSelected = sym === selectedSymbol;
            const symKey = sym.replace("/", "");
            const quote = liveMarket.quotes[sym] ?? liveMarket.quotes[symKey] ?? null;
            const isCrypto = sym.includes("BTC") || sym.includes("ETH") || sym.includes("SOL");

            const hasQuote = quote != null && quote.close != null && quote.close !== "";
            const closeNum = hasQuote ? Number(quote?.close) : null;
            const openNum = hasQuote && quote?.open != null ? Number(quote?.open) : null;
            const highNum = hasQuote && quote?.high != null ? Number(quote?.high) : null;
            const lowNum = hasQuote && quote?.low != null ? Number(quote?.low) : null;
            // OBS-DATA1-2 (2026-08-18): display precision routes from the
            // instrument's quote convention, not a crypto boolean. JPY pairs
            // quote at three decimals; a five-decimal JPY display padded the
            // corrected tick convention with zeros at the render layer.
            const isJpy = sym.includes("JPY");

            // Format price honestly
            let formattedPrice = "--";
            if (closeNum !== null && !isNaN(closeNum)) {
              formattedPrice = isCrypto
                ? closeNum.toLocaleString("en-US", {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                  })
                : isJpy
                  ? closeNum.toFixed(3)
                  : closeNum.toFixed(5);
            }

            // Format change percentage honestly
            const hasChange =
              closeNum !== null && openNum !== null && !isNaN(closeNum) && !isNaN(openNum);
            const changePercent =
              hasChange && openNum !== 0 ? ((closeNum! - openNum!) / openNum!) * 100 : null;
            const isPos = changePercent !== null && changePercent > 0;
            const isNeg = changePercent !== null && changePercent < 0;

            const changeClass = !hasChange
              ? "neutral"
              : isPos
                ? "positive"
                : isNeg
                  ? "negative"
                  : "neutral";

            const formattedChange = !hasChange
              ? "--"
              : `${isPos ? "+" : ""}${changePercent?.toFixed(2)}%`;

            // Intraperiod range (H - L), labelled Range, never spread
            const hasRange =
              highNum !== null && lowNum !== null && !isNaN(highNum) && !isNaN(lowNum);
            const rangeValue = hasRange ? highNum! - lowNum! : null;
            const formattedRange =
              rangeValue !== null
                ? isCrypto
                  ? rangeValue.toFixed(2)
                  : isJpy
                    ? rangeValue.toFixed(3)
                    : rangeValue.toFixed(5)
                : "--";

            return (
              <div
                key={sym}
                role="listitem"
                className={`watchlist-item-row ${isSelected ? "selected" : ""}`}
                onClick={() => handleSelect(sym)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" || e.key === " ") {
                    e.preventDefault();
                    handleSelect(sym);
                  }
                }}
                tabIndex={0}
                aria-label={`${sym} quote. Last price: ${formattedPrice}, Change: ${formattedChange}`}
                data-testid={`watchlist-row-${sym.toLowerCase().replace("/", "-")}`}
              >
                {/* Left: Symbol & Market Tag */}
                <div className="item-symbol-block">
                  <div className="item-symbol-name">
                    <span className={`item-active-dot ${isSelected ? "active" : ""}`} />
                    <span className="symbol-label">{sym}</span>
                  </div>
                  <span className={`item-market-class ${isCrypto ? "crypto" : "fx"}`}>
                    {isCrypto ? "CRYPTO" : "FX"}
                  </span>
                </div>

                {/* Center/Right: Price, Change %, and Range */}
                <div className="item-metrics-block">
                  <div className="item-price-row">
                    <span className="item-price-val mono" data-testid={`price-${symKey.toLowerCase()}`}>
                      {formattedPrice}
                    </span>
                    {quoteProvenance(quote?.source) ? (
                      <span
                        className="watchlist-provenance-chip mono"
                        data-testid={`watchlist-provenance-${symKey.toLowerCase()}`}
                      >
                        {quoteProvenance(quote?.source)}
                      </span>
                    ) : null}
                  </div>
                  <div className="item-sub-metrics">
                    <span
                      className={`item-change-val ${changeClass} mono`}
                      data-testid={`change-${symKey.toLowerCase()}`}
                    >
                      {formattedChange}
                    </span>
                    <span
                      className="item-range-val mono"
                      title="Intraperiod Range (High - Low)"
                      data-testid={`range-${symKey.toLowerCase()}`}
                    >
                      R: {formattedRange}
                    </span>
                  </div>
                  {sparklines[symKey]?.status === "ready" &&
                  (sparklines[symKey] as { status: "ready"; candles: ApiCandle[] }).candles.length >= 2 ? (
                    <div className="watchlist-sparkline-block" data-testid={`watchlist-sparkline-${symKey.toLowerCase()}`}>
                      <SparklineSvg
                        closes={(sparklines[symKey] as { status: "ready"; candles: ApiCandle[] }).candles
                          .map((c) => Number(c.close))
                          .filter((n) => Number.isFinite(n))}
                      />
                      {candleProvenance(
                        (sparklines[symKey] as { status: "ready"; candles: ApiCandle[] }).candles,
                      ) ? (
                        <span
                          className="watchlist-provenance-tag mono"
                          data-testid={`watchlist-sparkline-source-${symKey.toLowerCase()}`}
                        >
                          {candleProvenance(
                            (sparklines[symKey] as { status: "ready"; candles: ApiCandle[] }).candles,
                          )}
                        </span>
                      ) : null}
                    </div>
                  ) : null}
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
