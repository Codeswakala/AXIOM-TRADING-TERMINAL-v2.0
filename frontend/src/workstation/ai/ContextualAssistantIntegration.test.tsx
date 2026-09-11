import { describe, it, expect } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { WorkspaceContextProvider, useWorkspaceContext } from "./WorkspaceContext";
import { ContextualAssistantPanel } from "./ContextualAssistantPanel";

function ContextSwitchHarness() {
  const { setContextState } = useWorkspaceContext();

  return (
    <div>
      <div className="test-switcher">
        <button
          type="button"
          data-testid="btn-switch-intel"
          onClick={() =>
            setContextState({
              activeWorkspaceId: "intelligence",
              activeSymbol: "EURUSD",
              activeTimeframe: "1H",
              selectedArtifactId: "rep-intel-101",
              marketRegime: "EXPANSION",
            })
          }
        >
          Switch to Intelligence
        </button>

        <button
          type="button"
          data-testid="btn-switch-investig"
          onClick={() =>
            setContextState({
              activeWorkspaceId: "investigation",
              activeSymbol: "BTCUSD",
              activeTimeframe: "4H",
              selectedArtifactId: "sig-crypto-202",
              marketRegime: "HIGH_VOLATILITY",
            })
          }
        >
          Switch to Investigation
        </button>

        <button
          type="button"
          data-testid="btn-switch-charts"
          onClick={() =>
            setContextState({
              activeWorkspaceId: "charts",
              activeSymbol: "XAUUSD",
              activeTimeframe: "1D",
              selectedArtifactId: null,
              marketRegime: "CONSOLIDATION",
            })
          }
        >
          Switch to Charts
        </button>
      </div>

      <ContextualAssistantPanel liveResponses={[]} />
    </div>
  );
}

describe("UI-008-P03 Contextual Assistant Workspace Integration & Switching (T-3)", () => {
  it("dynamically adapts context chips and prompt suggestions when workspace switches (T-3)", () => {
    render(
      <WorkspaceContextProvider>
        <ContextSwitchHarness />
      </WorkspaceContextProvider>,
    );

    // Initial state
    expect(screen.getByTestId("chip-symbol")).toHaveTextContent("EURUSD");

    // 1. Switch to Intelligence
    fireEvent.click(screen.getByTestId("btn-switch-intel"));
    expect(screen.getByTestId("chip-workspace")).toHaveTextContent("intelligence");
    expect(screen.getByTestId("chip-symbol")).toHaveTextContent("EURUSD");
    expect(screen.getByTestId("chip-timeframe")).toHaveTextContent("1H");
    expect(screen.getByTestId("chip-artifact")).toHaveTextContent("rep-intel-101");
    expect(screen.getByTestId("chip-regime")).toHaveTextContent("EXPANSION");

    const intelChips = screen.getAllByTestId("prompt-suggestion-chip");
    expect(intelChips.some((c) => c.textContent?.includes("regime boundaries"))).toBe(true);

    // 2. Switch to Investigation
    fireEvent.click(screen.getByTestId("btn-switch-investig"));
    expect(screen.getByTestId("chip-workspace")).toHaveTextContent("investigation");
    expect(screen.getByTestId("chip-symbol")).toHaveTextContent("BTCUSD");
    expect(screen.getByTestId("chip-timeframe")).toHaveTextContent("4H");
    expect(screen.getByTestId("chip-artifact")).toHaveTextContent("sig-crypto-202");
    expect(screen.getByTestId("chip-regime")).toHaveTextContent("HIGH_VOLATILITY");

    const investigChips = screen.getAllByTestId("prompt-suggestion-chip");
    expect(investigChips.some((c) => c.textContent?.includes("Trace signal lineage"))).toBe(true);

    // 3. Switch to Charts
    fireEvent.click(screen.getByTestId("btn-switch-charts"));
    expect(screen.getByTestId("chip-workspace")).toHaveTextContent("charts");
    expect(screen.getByTestId("chip-symbol")).toHaveTextContent("XAUUSD");
    expect(screen.getByTestId("chip-timeframe")).toHaveTextContent("1D");
    expect(screen.queryByTestId("chip-artifact")).not.toBeInTheDocument();

    const chartChips = screen.getAllByTestId("prompt-suggestion-chip");
    expect(chartChips.some((c) => c.textContent?.includes("Summarize structure for XAUUSD"))).toBe(true);
  });
});
