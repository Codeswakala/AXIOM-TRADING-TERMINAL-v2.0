import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import {
  ContextualAssistantPanel,
  generatePromptSuggestions,
} from "./ContextualAssistantPanel";
import { WorkspaceContextProvider } from "./WorkspaceContext";
import type { AssistantResearchResponse } from "../../api/assistantClient";

describe("UI-008-P03 ContextualAssistantPanel Component (T-1, T-4, T-5)", () => {
  const mockResponses: AssistantResearchResponse[] = [
    {
      assistant_response_id: "ctx-resp-1",
      created_at: "2026-08-10T12:00:00Z",
      operator_id: "op_test",
      request_id: "req-ctx-1",
      request_text_hash: "hash_ctx_1",
      assistant_policy_version: "v1.0",
      provider_name: "RuleBasedGroundedAssistant",
      provider_version: "1.0",
      model_or_engine_version: "v1",
      source_artifact_ids: ["artifact-101"],
      grounding_summary: "Contextual advice for EURUSD",
      response_text: "EURUSD volatility is currently bounded within historical 1H standard deviations.",
      refused: false,
      refusal_reason: null,
      limitations: ["Derived from 1H series"],
      disclaimer: "RESEARCH-ONLY · NOT FINANCIAL ADVICE",
      research_status: "VERIFIED",
      audit_correlation_id: "corr-ctx-1",
      provenance: {},
    },
  ];

  // (T-1) Component rendering
  it("renders contextual assistant panel with disclaimer and active chips", () => {
    render(
      <WorkspaceContextProvider
        initialState={{
          activeWorkspaceId: "intelligence",
          activeSymbol: "EURUSD",
          activeTimeframe: "1H",
          selectedArtifactId: "rep-404",
          marketRegime: "STABLE",
        }}
      >
        <ContextualAssistantPanel liveResponses={mockResponses} />
      </WorkspaceContextProvider>,
    );

    expect(
      screen.getByRole("region", { name: /Contextual Assistant Panel/i }),
    ).toBeInTheDocument();
    expect(screen.getByTestId("contextual-disclaimer")).toHaveTextContent(
      "AI-generated research assistance only",
    );

    // Active context chips (U-2)
    expect(screen.getByTestId("chip-workspace")).toHaveTextContent("intelligence");
    expect(screen.getByTestId("chip-symbol")).toHaveTextContent("EURUSD");
    expect(screen.getByTestId("chip-timeframe")).toHaveTextContent("1H");
    expect(screen.getByTestId("chip-regime")).toHaveTextContent("STABLE");
    expect(screen.getByTestId("chip-artifact")).toHaveTextContent("rep-404");
  });

  // (U-1) Collapsible panel behavior
  it("toggles collapse and expand state when collapse button is clicked", () => {
    render(
      <WorkspaceContextProvider>
        <ContextualAssistantPanel liveResponses={mockResponses} defaultCollapsed={false} />
      </WorkspaceContextProvider>,
    );

    const toggleBtn = screen.getByTestId("assistant-collapse-toggle");
    expect(toggleBtn).toHaveTextContent("Collapse");
    expect(screen.getByTestId("active-context-chips")).toBeInTheDocument();

    // Click collapse
    fireEvent.click(toggleBtn);
    expect(toggleBtn).toHaveTextContent("Expand");
    expect(screen.queryByTestId("active-context-chips")).not.toBeInTheDocument();

    // Click expand
    fireEvent.click(toggleBtn);
    expect(toggleBtn).toHaveTextContent("Collapse");
    expect(screen.getByTestId("active-context-chips")).toBeInTheDocument();
  });

  // (T-4) Contextual prompt suggestion generation and click interaction
  it("generates contextual prompt suggestions and notifies on click (T-4, U-3)", () => {
    const handleSelectPrompt = vi.fn();

    render(
      <WorkspaceContextProvider
        initialState={{
          activeWorkspaceId: "intelligence",
          activeSymbol: "GBPUSD",
          activeTimeframe: "4H",
        }}
      >
        <ContextualAssistantPanel
          liveResponses={mockResponses}
          onSelectPrompt={handleSelectPrompt}
        />
      </WorkspaceContextProvider>,
    );

    const chips = screen.getAllByTestId("prompt-suggestion-chip");
    expect(chips.length).toBeGreaterThan(0);
    expect(chips[0].textContent).toContain("GBPUSD");

    // Click first suggestion chip
    fireEvent.click(chips[0]);
    expect(handleSelectPrompt).toHaveBeenCalledTimes(1);
    expect(screen.getByTestId("selected-prompt-feedback")).toBeInTheDocument();
  });

  // (T-5) State transitions: Loading state
  it("renders loading skeleton during data fetch", () => {
    render(
      <WorkspaceContextProvider>
        <ContextualAssistantPanel loading={true} />
      </WorkspaceContextProvider>,
    );

    expect(screen.getByTestId("contextual-loading-skeleton")).toBeInTheDocument();
    expect(screen.getByText(/Loading contextual assistant insights/i)).toBeInTheDocument();
  });

  // (T-5) State transitions: Error state
  it("renders error state banner when error is passed", () => {
    render(
      <WorkspaceContextProvider>
        <ContextualAssistantPanel error="Failed to fetch contextual responses" />
      </WorkspaceContextProvider>,
    );

    const errorBanner = screen.getByTestId("contextual-error-banner");
    expect(errorBanner).toBeInTheDocument();
    expect(errorBanner.textContent).toContain("Failed to fetch contextual responses");
  });

  // (T-5) State transitions: 401 Unauthorized state
  it("renders 401 unauthorized notice when session is unauthenticated", () => {
    render(
      <WorkspaceContextProvider>
        <ContextualAssistantPanel isUnauthorized={true} />
      </WorkspaceContextProvider>,
    );

    expect(screen.getByTestId("contextual-auth-required")).toBeInTheDocument();
    expect(screen.getByText(/Authentication required/i)).toBeInTheDocument();
  });

  // (T-5) State transitions: Empty state
  it("renders empty state message when no responses exist", () => {
    render(
      <WorkspaceContextProvider>
        <ContextualAssistantPanel liveResponses={[]} />
      </WorkspaceContextProvider>,
    );

    expect(screen.getByTestId("contextual-empty-state")).toBeInTheDocument();
  });

  // generatePromptSuggestions helper unit tests
  describe("generatePromptSuggestions", () => {
    it("generates intelligence-specific suggestions", () => {
      const suggestions = generatePromptSuggestions("intelligence", "BTCUSD", "1D", null);
      expect(suggestions.some((s) => s.includes("regime boundaries"))).toBe(true);
      expect(suggestions.some((s) => s.includes("correlation matrix"))).toBe(true);
    });

    it("generates investigation-specific suggestions", () => {
      const suggestions = generatePromptSuggestions("investigation", "ETHUSD", "1H", "sig-1");
      expect(suggestions.some((s) => s.includes("Trace signal lineage"))).toBe(true);
      expect(suggestions.some((s) => s.includes("provenance of artifact sig-1"))).toBe(true);
    });

    it("generates chart-specific suggestions", () => {
      const suggestions = generatePromptSuggestions("charts", "XAUUSD", "15m", null);
      expect(suggestions.some((s) => s.includes("Summarize structure for XAUUSD"))).toBe(true);
    });
  });
});
