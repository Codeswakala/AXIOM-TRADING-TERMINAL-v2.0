import { fireEvent, render, screen, within } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import {
  addSymbolToWatchlist,
  DEFAULT_MARKET_WORKSPACE_PREFERENCE,
  MarketWatchlistPanel,
  PROFESSIONAL_MARKET_WORKSPACE_KEY,
  removeSymbolFromWatchlist,
  toMarketWorkspacePreferenceWrite,
  validateMarketWorkspacePreference,
  WATCHLIST_FORBIDDEN_FIELDS,
  type MarketWorkspacePreference,
} from "./marketWatchlists";

async function readRawSource(pathSuffix: string): Promise<string> {
  const modules = import.meta.glob("../**/*.{ts,tsx}", {
    query: "?raw",
    import: "default",
  });
  const parts = pathSuffix.split("/");
  const fileName = parts[parts.length - 1] ?? pathSuffix;
  const entry = Object.entries(modules).find(
    ([path]) => path.endsWith(pathSuffix) || path.endsWith(fileName),
  );
  if (!entry) throw new Error(`Raw source not found: ${pathSuffix}`);
  return (entry[1] as () => Promise<string>)();
}

describe("UI-003-P02 market watchlists", () => {
  it("test_ui003_watchlists_use_operator_workspace_preferences_no_new_table", async () => {
    const payload = toMarketWorkspacePreferenceWrite(DEFAULT_MARKET_WORKSPACE_PREFERENCE);
    expect(payload.workspace_key).toBe(PROFESSIONAL_MARKET_WORKSPACE_KEY);
    expect(payload.layout_config?.watchlists).toBeDefined();
    expect(payload.metadata?.ui_workstream).toBe("UI-003-P02");

    const sourceText = await readRawSource("market/marketWatchlists.tsx");
    expect(sourceText).toContain("fetchWorkspacePreferences");
    expect(sourceText).toContain("createWorkspacePreference");
    expect(sourceText).toContain("updateWorkspacePreference");
    expect(sourceText).not.toContain("CREATE TABLE");
    expect(sourceText).not.toContain("alembic");
    expect(sourceText).not.toContain("/api/v1/market-watchlists");
  });

  it("test_ui003_watchlists_store_symbol_ids_only_no_positions_orders_or_accounts", () => {
    const watchlist = addSymbolToWatchlist(
      DEFAULT_MARKET_WORKSPACE_PREFERENCE.watchlists[0],
      "btcusd",
      "H1",
    );
    const reduced = removeSymbolFromWatchlist(watchlist, "EURUSD");
    const payload = toMarketWorkspacePreferenceWrite({
      ...DEFAULT_MARKET_WORKSPACE_PREFERENCE,
      active_symbol: "BTCUSD",
      active_timeframe: "H1",
      watchlists: [reduced],
    });
    const text = JSON.stringify(payload).toLowerCase();
    expect(text).toContain("btcusd");
    expect(text).toContain("h1");
    for (const forbidden of WATCHLIST_FORBIDDEN_FIELDS) {
      expect(text).not.toContain(`\"${forbidden}\"`);
    }
  });

  it("test_ui003_watchlists_reject_execution_broker_account_payload_fields", () => {
    const unsafe = {
      ...DEFAULT_MARKET_WORKSPACE_PREFERENCE,
      watchlists: [
        {
          ...DEFAULT_MARKET_WORKSPACE_PREFERENCE.watchlists[0],
          broker: "blocked",
          account_id: "blocked",
          quantity: 1,
          order_ticket: "blocked",
        },
      ],
    } as unknown as MarketWorkspacePreference;
    expect(() => validateMarketWorkspacePreference(unsafe)).toThrow(/FORBIDDEN_WATCHLIST_FIELD/);
  });

  it("test_ui003_watchlists_are_keyboard_operable_and_accessible", () => {
    const onAddSymbol = vi.fn();
    const onRemoveSymbol = vi.fn();
    const onSelectSymbol = vi.fn();
    render(
      <MarketWatchlistPanel
        watchlist={DEFAULT_MARKET_WORKSPACE_PREFERENCE.watchlists[0]}
        availableSymbols={["EURUSD", "BTCUSD"]}
        availableTimeframes={["M1", "H1"]}
        selectedSymbol="EURUSD"
        selectedTimeframe="M1"
        onAddSymbol={onAddSymbol}
        onRemoveSymbol={onRemoveSymbol}
        onSelectSymbol={onSelectSymbol}
      />,
    );

    const panel = screen.getByLabelText("Professional market watchlist");
    expect(panel).toHaveTextContent(/symbol and timeframe ids only/i);
    expect(screen.getByLabelText("Watchlist symbol")).toBeInTheDocument();
    expect(screen.getByLabelText("Watchlist timeframe")).toBeInTheDocument();

    const addButton = screen.getByRole("button", { name: "Add symbol to watchlist" });
    addButton.focus();
    expect(addButton).toHaveFocus();
    fireEvent.click(addButton);
    expect(onAddSymbol).toHaveBeenCalledWith("EURUSD", "M1");

    const list = screen.getByLabelText("Primary market watchlist symbols");
    fireEvent.click(within(list).getByRole("button", { name: "Focus EURUSD" }));
    expect(onSelectSymbol).toHaveBeenCalledWith("EURUSD");
    fireEvent.click(within(list).getByRole("button", { name: "Remove EURUSD" }));
    expect(onRemoveSymbol).toHaveBeenCalledWith("EURUSD");
  });

  it("test_ui003_watchlist_persistence_preserves_alembic_head", async () => {
    const sourceText = await readRawSource("market/marketWatchlists.tsx");
    expect(sourceText).not.toContain("revision");
    expect(sourceText).not.toContain("op.create_table");
    expect(sourceText).not.toContain("/api/v1/market-watchlists");
    expect(sourceText).toContain(PROFESSIONAL_MARKET_WORKSPACE_KEY);
  });
});
