import { describe, it, expect } from "vitest";
import { renderHook, act } from "@testing-library/react";
import { WorkspaceContextProvider, useWorkspaceContext } from "./WorkspaceContext";
import type { ReactNode } from "react";

describe("UI-008-P03 WorkspaceContext & Hook (T-2, T-6, T-7)", () => {
  const wrapper = ({ children }: { children: ReactNode }) => (
    <WorkspaceContextProvider
      initialState={{
        activeWorkspaceId: "intelligence",
        activeSymbol: "EURUSD",
        activeTimeframe: "1H",
        selectedArtifactId: "rep-01",
        marketRegime: "LOW_VOLATILITY",
      }}
    >
      {children}
    </WorkspaceContextProvider>
  );

  it("provides initial workspace state to consumer hooks", () => {
    const { result } = renderHook(() => useWorkspaceContext(), { wrapper });

    expect(result.current.activeWorkspaceId).toBe("intelligence");
    expect(result.current.activeSymbol).toBe("EURUSD");
    expect(result.current.activeTimeframe).toBe("1H");
    expect(result.current.selectedArtifactId).toBe("rep-01");
    expect(result.current.marketRegime).toBe("LOW_VOLATILITY");
  });

  it("updates symbol context correctly (T-6)", () => {
    const { result } = renderHook(() => useWorkspaceContext(), { wrapper });

    act(() => {
      result.current.setActiveSymbol("BTCUSD");
    });

    expect(result.current.activeSymbol).toBe("BTCUSD");
  });

  it("updates timeframe context correctly (T-7)", () => {
    const { result } = renderHook(() => useWorkspaceContext(), { wrapper });

    act(() => {
      result.current.setActiveTimeframe("4H");
    });

    expect(result.current.activeTimeframe).toBe("4H");
  });

  it("updates selected artifact and market regime", () => {
    const { result } = renderHook(() => useWorkspaceContext(), { wrapper });

    act(() => {
      result.current.setSelectedArtifactId("artifact-regime-99");
      result.current.setMarketRegime("TRENDING_EXPANSION");
    });

    expect(result.current.selectedArtifactId).toBe("artifact-regime-99");
    expect(result.current.marketRegime).toBe("TRENDING_EXPANSION");
  });

  it("setContextState performs partial state updates", () => {
    const { result } = renderHook(() => useWorkspaceContext(), { wrapper });

    act(() => {
      result.current.setContextState({
        activeWorkspaceId: "investigation",
        activeSymbol: "XAUUSD",
      });
    });

    expect(result.current.activeWorkspaceId).toBe("investigation");
    expect(result.current.activeSymbol).toBe("XAUUSD");
    expect(result.current.activeTimeframe).toBe("1H"); // preserved
  });

  it("resets context to default values", () => {
    const { result } = renderHook(() => useWorkspaceContext(), { wrapper });

    act(() => {
      result.current.setActiveSymbol("ETHUSD");
      result.current.resetContext();
    });

    expect(result.current.activeSymbol).toBe("EURUSD");
    expect(result.current.activeWorkspaceId).toBe("default");
  });

  it("gracefully falls back when mounted outside WorkspaceContextProvider", () => {
    const { result } = renderHook(() => useWorkspaceContext());
    expect(result.current.activeSymbol).toBe("EURUSD");
    expect(typeof result.current.setActiveSymbol).toBe("function");
  });
});
