import { describe, it, expect } from "vitest";
import { render, screen, within } from "@testing-library/react";
import { AssistantCommandSurface } from "./AssistantCommandSurface";
import type { AssistantResearchResponse } from "../../api/assistantClient";

describe("UI-008-P02 AssistantCommandSurface Live Data Integration", () => {
  const mockResponses: AssistantResearchResponse[] = [
    {
      assistant_response_id: "resp-201",
      created_at: "2026-08-10T11:00:00Z",
      operator_id: "operator_1",
      request_id: "req-201",
      request_text_hash: "hash_abc",
      assistant_policy_version: "rule_based.v1",
      provider_name: "RuleBasedGroundedAssistant",
      provider_version: "1.0.0",
      model_or_engine_version: "grounded_rules_v1",
      source_artifact_ids: ["artifact-regime-01"],
      grounding_summary: "Grounding verified against active regime classification report",
      response_text: "The current market environment reflects low volatility regime with stable spread.",
      refused: false,
      refusal_reason: null,
      limitations: ["Derived from 1H OHLCV series", "No execution capability"],
      disclaimer: "RESEARCH-ONLY · NOT FINANCIAL ADVICE",
      research_status: "VERIFIED",
      audit_correlation_id: "audit-corr-201",
      provenance: { source: "historical_replay" },
    },
    {
      assistant_response_id: "resp-202",
      created_at: "2026-08-10T11:05:00Z",
      operator_id: "operator_1",
      request_id: "req-202",
      request_text_hash: "hash_xyz",
      assistant_policy_version: "rule_based.v1",
      provider_name: "RuleBasedGroundedAssistant",
      provider_version: "1.0.0",
      model_or_engine_version: "grounded_rules_v1",
      source_artifact_ids: [],
      grounding_summary: "Query violated grounding constraint",
      response_text: "Refusal: Cannot generate speculative trade recommendations.",
      refused: true,
      refusal_reason: "SPECULATIVE_PROJECTION_REFUSED",
      limitations: ["Refusal event"],
      disclaimer: "RESEARCH-ONLY · NOT FINANCIAL ADVICE",
      research_status: "REFUSED",
      audit_correlation_id: "audit-corr-202",
      provenance: { source: "guardrail" },
    },
  ];

  // (T-1) Live responses rendering
  it("renders live assistant research responses when data is provided", () => {
    render(<AssistantCommandSurface liveResponses={mockResponses} />);

    const responseList = screen.getByTestId("assistant-response-list");
    expect(responseList).toBeInTheDocument();

    const row1 = screen.getByTestId("response-resp-201");
    expect(row1).toBeInTheDocument();
    expect(within(row1).getByText(/low volatility regime/i)).toBeInTheDocument();
    expect(within(row1).getByText("VERIFIED")).toBeInTheDocument();

    const row2 = screen.getByTestId("response-resp-202");
    expect(row2).toBeInTheDocument();
    expect(within(row2).getByTestId("refusal-badge")).toHaveTextContent("REFUSED: SPECULATIVE_PROJECTION_REFUSED");
  });

  // (T-3) Skeleton loading state
  it("renders skeleton loading state during data fetch", () => {
    render(<AssistantCommandSurface loading={true} />);

    const skeleton = screen.getByTestId("assistant-loading-skeleton");
    expect(skeleton).toBeInTheDocument();
    expect(skeleton.getAttribute("data-ui008-state")).toBe("loading");
    expect(screen.getByText(/Loading verified assistant responses/i)).toBeInTheDocument();
  });

  // (T-4) Error state banner
  it("renders error banner with recovery message when error occurs (N-3)", () => {
    render(<AssistantCommandSurface error="Network connection failed: 503 Service Unavailable" />);

    const errorBanner = screen.getByTestId("assistant-error-banner");
    expect(errorBanner).toBeInTheDocument();
    expect(errorBanner.getAttribute("data-ui008-state")).toBe("error");
    expect(errorBanner.textContent).toContain("Network connection failed");
  });

  // (T-5) Empty state rendering
  it("renders empty state when response array is empty (N-2)", () => {
    render(<AssistantCommandSurface liveResponses={[]} />);

    const empty = screen.getByTestId("p01-skeleton");
    expect(empty).toBeInTheDocument();
  });

  // (T-6) 401 Unauthorized handling state (N-4)
  it("renders 401 unauthorized notice when session is invalid", () => {
    render(<AssistantCommandSurface isUnauthorized={true} />);

    const authBanner = screen.getByTestId("assistant-auth-required");
    expect(authBanner).toBeInTheDocument();
    expect(authBanner.getAttribute("data-ui008-state")).toBe("unauthorized");
    expect(authBanner.textContent).toContain("Authentication required");
  });

  // (N-1) Malformed/null error recovery
  it("handles empty/malformed responses safely without crashing", () => {
    render(<AssistantCommandSurface liveResponses={[]} error={null} loading={false} />);
    expect(screen.getByRole("region", { name: /Assistant Command Surface/i })).toBeInTheDocument();
  });
});
