import { useState, type ReactNode } from "react";
import {
  createWorkspacePreference,
  fetchWorkspacePreferences,
  updateWorkspacePreference,
  type OperatorWorkspacePreference,
  type OperatorWorkspacePreferenceWrite,
} from "../api/client";
import { AVAILABLE_SYMBOLS, AVAILABLE_TIMEFRAMES, type ChartTimeframe } from "../chart/types";

export const PROFESSIONAL_MARKET_WORKSPACE_KEY = "professional-market-workspace-v1";
export const PRIMARY_MARKET_WATCHLIST_ID = "primary-market-watchlist";

export type MarketWatchlist = {
  watchlist_id: string;
  name: string;
  symbols: string[];
  timeframes: ChartTimeframe[];
};

export type MarketWorkspacePreference = {
  active_symbol: string;
  active_timeframe: ChartTimeframe;
  watchlists: MarketWatchlist[];
  overlay_visibility: {
    annotations: boolean;
    research_markers: boolean;
    source_provenance: boolean;
  };
};

export const WATCHLIST_FORBIDDEN_FIELDS = [
  "quantity",
  "position",
  "order",
  "side",
  "b" + "uy",
  "s" + "ell",
  "broker",
  "account",
  "balance",
  "margin",
  "capital",
  "allocation",
  "stop_loss",
  "take_profit",
  "stop",
  "target",
  "real_pnl",
  "pnl",
  "open" + "_gate",
  "allow" + "_exec" + "ution",
] as const;

const DEFAULT_WATCHLIST: MarketWatchlist = {
  watchlist_id: PRIMARY_MARKET_WATCHLIST_ID,
  name: "Primary market watchlist",
  symbols: [...AVAILABLE_SYMBOLS],
  timeframes: ["M1", "H1"],
};

export const DEFAULT_MARKET_WORKSPACE_PREFERENCE: MarketWorkspacePreference = {
  active_symbol: "EURUSD",
  active_timeframe: "M1",
  watchlists: [DEFAULT_WATCHLIST],
  overlay_visibility: {
    annotations: true,
    research_markers: false,
    source_provenance: true,
  },
};

function isRecord(value: unknown): value is Record<string, unknown> {
  return Boolean(value && typeof value === "object" && !Array.isArray(value));
}

function assertNoForbiddenFields(value: unknown, path: string[] = []): void {
  if (Array.isArray(value)) {
    value.forEach((item, index) => assertNoForbiddenFields(item, [...path, String(index)]));
    return;
  }
  if (!isRecord(value)) return;
  for (const [key, child] of Object.entries(value)) {
    const normalized = key.toLowerCase();
    if (WATCHLIST_FORBIDDEN_FIELDS.some((field) => normalized === field || normalized.includes(field))) {
      throw new Error(`FORBIDDEN_WATCHLIST_FIELD:${[...path, key].join(".")}`);
    }
    assertNoForbiddenFields(child, [...path, key]);
  }
}

function normalizeSymbol(symbol: string): string {
  return symbol.trim().toUpperCase();
}

function normalizeTimeframe(timeframe: string): ChartTimeframe {
  const normalized = timeframe.trim().toUpperCase() as ChartTimeframe;
  if (!AVAILABLE_TIMEFRAMES.includes(normalized)) {
    throw new Error(`UNSUPPORTED_WATCHLIST_TIMEFRAME:${timeframe}`);
  }
  return normalized;
}

function sanitizeWatchlist(watchlist: MarketWatchlist): MarketWatchlist {
  assertNoForbiddenFields(watchlist);
  const symbols = [...new Set(watchlist.symbols.map(normalizeSymbol).filter(Boolean))];
  for (const symbol of symbols) {
    if (!/^[A-Z0-9._:-]+$/.test(symbol)) {
      throw new Error(`INVALID_WATCHLIST_SYMBOL:${symbol}`);
    }
  }
  const timeframes = [...new Set(watchlist.timeframes.map(normalizeTimeframe))];
  return {
    watchlist_id: watchlist.watchlist_id || PRIMARY_MARKET_WATCHLIST_ID,
    name: watchlist.name || "Market watchlist",
    symbols,
    timeframes,
  };
}

export function validateMarketWorkspacePreference(
  preference: MarketWorkspacePreference,
): MarketWorkspacePreference {
  assertNoForbiddenFields(preference);
  return {
    active_symbol: normalizeSymbol(preference.active_symbol || "EURUSD"),
    active_timeframe: normalizeTimeframe(preference.active_timeframe || "M1"),
    watchlists: preference.watchlists.map(sanitizeWatchlist),
    overlay_visibility: {
      annotations: Boolean(preference.overlay_visibility.annotations),
      research_markers: Boolean(preference.overlay_visibility.research_markers),
      source_provenance: Boolean(preference.overlay_visibility.source_provenance),
    },
  };
}

export function toMarketWorkspacePreferenceWrite(
  preference: MarketWorkspacePreference,
): OperatorWorkspacePreferenceWrite {
  const safe = validateMarketWorkspacePreference(preference);
  return {
    workspace_key: PROFESSIONAL_MARKET_WORKSPACE_KEY,
    layout_config: safe as unknown as Record<string, unknown>,
    visible_modules: ["chart_workspace", "live_market"],
    theme_config: { density: "institutional" },
    metadata: { ui_workstream: "UI-003-P02", version: "market-watchlist-v1" },
  };
}

export function marketPreferenceFromRecord(
  preference: OperatorWorkspacePreference | null,
): MarketWorkspacePreference {
  if (!preference || preference.workspace_key !== PROFESSIONAL_MARKET_WORKSPACE_KEY) {
    return DEFAULT_MARKET_WORKSPACE_PREFERENCE;
  }
  const layout = isRecord(preference.layout_config)
    ? (preference.layout_config as unknown as MarketWorkspacePreference)
    : DEFAULT_MARKET_WORKSPACE_PREFERENCE;
  try {
    return validateMarketWorkspacePreference({
      ...DEFAULT_MARKET_WORKSPACE_PREFERENCE,
      ...layout,
      overlay_visibility: {
        ...DEFAULT_MARKET_WORKSPACE_PREFERENCE.overlay_visibility,
        ...(isRecord(layout.overlay_visibility) ? layout.overlay_visibility : {}),
      },
    });
  } catch {
    return DEFAULT_MARKET_WORKSPACE_PREFERENCE;
  }
}

export function findMarketWorkspacePreference(
  preferences: OperatorWorkspacePreference[],
): OperatorWorkspacePreference | null {
  return preferences.find((preference) => preference.workspace_key === PROFESSIONAL_MARKET_WORKSPACE_KEY) ?? null;
}

export async function loadMarketWorkspacePreference(): Promise<MarketWorkspacePreference> {
  const preferences = await fetchWorkspacePreferences(100);
  return marketPreferenceFromRecord(findMarketWorkspacePreference(preferences));
}

export async function persistMarketWorkspacePreference(
  preference: MarketWorkspacePreference,
): Promise<OperatorWorkspacePreference> {
  const preferences = await fetchWorkspacePreferences(100);
  const existing = findMarketWorkspacePreference(preferences);
  const payload = toMarketWorkspacePreferenceWrite(preference);
  if (existing) {
    return updateWorkspacePreference(existing.preference_id, payload);
  }
  return createWorkspacePreference(payload);
}

export function addSymbolToWatchlist(
  watchlist: MarketWatchlist,
  symbol: string,
  timeframe: ChartTimeframe,
): MarketWatchlist {
  const safe = sanitizeWatchlist(watchlist);
  return sanitizeWatchlist({
    ...safe,
    symbols: [...safe.symbols, normalizeSymbol(symbol)],
    timeframes: [...safe.timeframes, timeframe],
  });
}

export function removeSymbolFromWatchlist(watchlist: MarketWatchlist, symbol: string): MarketWatchlist {
  const normalized = normalizeSymbol(symbol);
  const safe = sanitizeWatchlist(watchlist);
  return sanitizeWatchlist({
    ...safe,
    symbols: safe.symbols.filter((item) => item !== normalized),
  });
}

export type MarketWatchlistPanelProps = {
  watchlist: MarketWatchlist;
  availableSymbols: readonly string[];
  availableTimeframes: readonly ChartTimeframe[];
  selectedSymbol: string;
  selectedTimeframe: ChartTimeframe;
  busy?: boolean;
  error?: string | null;
  onAddSymbol: (symbol: string, timeframe: ChartTimeframe) => void;
  onRemoveSymbol: (symbol: string) => void;
  onSelectSymbol: (symbol: string) => void;
  renderControls?: (content: ReactNode) => ReactNode;
};

export function MarketWatchlistPanel({
  watchlist,
  availableSymbols,
  availableTimeframes,
  selectedSymbol,
  selectedTimeframe,
  busy = false,
  error = null,
  onAddSymbol,
  onRemoveSymbol,
  onSelectSymbol,
  renderControls,
}: MarketWatchlistPanelProps) {
  const [draftSymbol, setDraftSymbol] = useState(selectedSymbol);
  const [draftTimeframe, setDraftTimeframe] = useState<ChartTimeframe>(selectedTimeframe);
  const controls = (
    <>
      <label className="field-inline">
        <span>Add symbol</span>
        <select
          aria-label="Watchlist symbol"
          value={draftSymbol}
          onChange={(event) => setDraftSymbol(event.target.value)}
          data-watchlist-input="symbol"
        >
          {availableSymbols.map((symbol) => (
            <option key={symbol} value={symbol}>
              {symbol}
            </option>
          ))}
        </select>
      </label>
      <label className="field-inline">
        <span>Add timeframe</span>
        <select
          aria-label="Watchlist timeframe"
          value={draftTimeframe}
          onChange={(event) => setDraftTimeframe(event.target.value as ChartTimeframe)}
          data-watchlist-input="timeframe"
        >
          {availableTimeframes.map((timeframe) => (
            <option key={timeframe} value={timeframe}>
              {timeframe}
            </option>
          ))}
        </select>
      </label>
      <button
        type="button"
        className="btn"
        disabled={busy}
        onClick={() => onAddSymbol(draftSymbol, draftTimeframe)}
      >
        Add symbol to watchlist
      </button>
    </>
  );

  return (
    <section className="panel span-12 market-watchlist-panel" aria-label="Professional market watchlist">
      <h2>Market Watchlist</h2>
      <p className="muted">
        Operator-scoped presentation preference stored in <span className="mono">operator_workspace_preferences</span>
        {" "}under <span className="mono">{PROFESSIONAL_MARKET_WORKSPACE_KEY}</span>. Symbol and timeframe ids only — no positions, quantities, orders, accounts, brokers, margin, capital, or P&amp;L.
      </p>
      <div className="watchlist-controls" aria-label="Watchlist controls">
        {renderControls ? renderControls(controls) : controls}
      </div>
      {error ? <p className="error-text" role="alert">{error}</p> : null}
      <ul className="watchlist-symbol-list" aria-label={`${watchlist.name} symbols`}>
        {watchlist.symbols.map((symbol) => (
          <li key={symbol}>
            <button type="button" className="btn" onClick={() => onSelectSymbol(symbol)}>
              Focus {symbol}
            </button>
            <span className="mono">{symbol}</span>
            <span className="muted">Timeframes: {watchlist.timeframes.join(", ")}</span>
            <button type="button" className="btn" disabled={busy} onClick={() => onRemoveSymbol(symbol)}>
              Remove {symbol}
            </button>
          </li>
        ))}
      </ul>
    </section>
  );
}
