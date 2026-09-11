/**
 * Workspace Context Provider & Hook (UI-008-P03)
 *
 * Supplies active workspace state (symbol, timeframe, selected artifact ID, market regime)
 * to contextual assistant panels and command surfaces across /intelligence, /investigation,
 * and /charts.
 *
 * Read-Only & Isolated:
 * - Only carries non-sensitive presentation identifiers.
 * - No order, sizing, trading account, or broker credential data.
 */

import { createContext, useContext, useState, useMemo, useCallback, type ReactNode } from "react";

export interface WorkspaceState {
  activeWorkspaceId: string;
  activeSymbol: string | null;
  activeTimeframe: string | null;
  selectedArtifactId: string | null;
  marketRegime: string | null;
}

export interface WorkspaceContextValue extends WorkspaceState {
  setActiveWorkspaceId: (workspaceId: string) => void;
  setActiveSymbol: (symbol: string | null) => void;
  setActiveTimeframe: (timeframe: string | null) => void;
  setSelectedArtifactId: (artifactId: string | null) => void;
  setMarketRegime: (regime: string | null) => void;
  setContextState: (updates: Partial<WorkspaceState>) => void;
  resetContext: () => void;
}

const DEFAULT_STATE: WorkspaceState = {
  activeWorkspaceId: "default",
  activeSymbol: "EURUSD",
  activeTimeframe: "1H",
  selectedArtifactId: null,
  marketRegime: "LOW_VOLATILITY_RANGING",
};

const WorkspaceContext = createContext<WorkspaceContextValue | null>(null);

export interface WorkspaceContextProviderProps {
  children: ReactNode;
  initialState?: Partial<WorkspaceState>;
}

export function WorkspaceContextProvider({
  children,
  initialState,
}: WorkspaceContextProviderProps) {
  const [state, setState] = useState<WorkspaceState>(() => ({
    ...DEFAULT_STATE,
    ...initialState,
  }));

  const setActiveWorkspaceId = useCallback((activeWorkspaceId: string) => {
    setState((prev) => ({ ...prev, activeWorkspaceId }));
  }, []);

  const setActiveSymbol = useCallback((activeSymbol: string | null) => {
    setState((prev) => ({ ...prev, activeSymbol }));
  }, []);

  const setActiveTimeframe = useCallback((activeTimeframe: string | null) => {
    setState((prev) => ({ ...prev, activeTimeframe }));
  }, []);

  const setSelectedArtifactId = useCallback((selectedArtifactId: string | null) => {
    setState((prev) => ({ ...prev, selectedArtifactId }));
  }, []);

  const setMarketRegime = useCallback((marketRegime: string | null) => {
    setState((prev) => ({ ...prev, marketRegime }));
  }, []);

  const setContextState = useCallback((updates: Partial<WorkspaceState>) => {
    setState((prev) => ({ ...prev, ...updates }));
  }, []);

  const resetContext = useCallback(() => {
    setState(DEFAULT_STATE);
  }, []);

  const value = useMemo<WorkspaceContextValue>(
    () => ({
      ...state,
      setActiveWorkspaceId,
      setActiveSymbol,
      setActiveTimeframe,
      setSelectedArtifactId,
      setMarketRegime,
      setContextState,
      resetContext,
    }),
    [
      state,
      setActiveWorkspaceId,
      setActiveSymbol,
      setActiveTimeframe,
      setSelectedArtifactId,
      setMarketRegime,
      setContextState,
      resetContext,
    ],
  );

  return <WorkspaceContext.Provider value={value}>{children}</WorkspaceContext.Provider>;
}

export function useWorkspaceContext(): WorkspaceContextValue {
  const ctx = useContext(WorkspaceContext);
  if (!ctx) {
    // Graceful fallback for components mounted outside provider (e.g. standalone unit tests)
    return {
      ...DEFAULT_STATE,
      setActiveWorkspaceId: () => {},
      setActiveSymbol: () => {},
      setActiveTimeframe: () => {},
      setSelectedArtifactId: () => {},
      setMarketRegime: () => {},
      setContextState: () => {},
      resetContext: () => {},
    };
  }
  return ctx;
}
