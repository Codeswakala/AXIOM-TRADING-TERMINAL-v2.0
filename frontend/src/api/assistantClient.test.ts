import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import {
  fetchAssistantResponses,
  fetchAssistantResponse,
  fetchAssistantAuditEvents,
  ApiError,
} from "./assistantClient";
import * as tokenStorage from "../auth/tokenStorage";

describe("UI-008-P02 Assistant Client API", () => {
  const originalFetch = globalThis.fetch;

  beforeEach(() => {
    vi.spyOn(tokenStorage, "getAccessToken").mockReturnValue("test-jwt-token-xyz");
  });

  afterEach(() => {
    globalThis.fetch = originalFetch;
    vi.restoreAllMocks();
  });

  it("fetchAssistantResponses sends Bearer token and parses response array", async () => {
    const mockResponses = [
      {
        assistant_response_id: "resp-1",
        created_at: "2026-08-10T10:00:00Z",
        operator_id: "op-1",
        request_id: "req-1",
        request_text_hash: "hash123",
        assistant_policy_version: "v1.0",
        provider_name: "RuleBasedGroundedAssistant",
        provider_version: "1.0",
        model_or_engine_version: "grounded_v1",
        source_artifact_ids: ["art-1"],
        grounding_summary: "Grounding verified against regime report",
        response_text: "Market is in low volatility regime.",
        refused: false,
        refusal_reason: null,
        limitations: ["Historical data only"],
        disclaimer: "RESEARCH-ONLY",
        research_status: "VERIFIED",
        audit_correlation_id: "corr-1",
        provenance: {},
      },
    ];

    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => mockResponses,
    });

    const data = await fetchAssistantResponses({ limit: 10 });
    expect(data).toHaveLength(1);
    expect(data[0].assistant_response_id).toBe("resp-1");
    expect(data[0].refused).toBe(false);

    expect(globalThis.fetch).toHaveBeenCalledWith(
      "/api/v1/collaboration/assistant-responses?limit=10",
      expect.objectContaining({
        method: "GET",
        headers: expect.any(Headers),
      }),
    );
  });

  it("fetchAssistantResponse queries single response by ID", async () => {
    const mockResponse = {
      assistant_response_id: "resp-42",
      created_at: "2026-08-10T10:00:00Z",
      operator_id: "op-1",
      request_id: "req-42",
      request_text_hash: "hash42",
      assistant_policy_version: "v1.0",
      provider_name: "RuleBasedGroundedAssistant",
      provider_version: "1.0",
      model_or_engine_version: "grounded_v1",
      source_artifact_ids: [],
      grounding_summary: "Refusal triggered",
      response_text: "Query was refused due to out-of-scope request.",
      refused: true,
      refusal_reason: "UNGROUNDED_QUERY_REFUSED",
      limitations: [],
      disclaimer: "RESEARCH-ONLY",
      research_status: "REFUSED",
      audit_correlation_id: "corr-42",
      provenance: {},
    };

    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => mockResponse,
    });

    const data = await fetchAssistantResponse("resp-42");
    expect(data.assistant_response_id).toBe("resp-42");
    expect(data.refused).toBe(true);
    expect(data.refusal_reason).toBe("UNGROUNDED_QUERY_REFUSED");
  });

  it("fetchAssistantAuditEvents queries audit events with SECURITY category", async () => {
    const mockAuditEvents = [
      {
        id: "evt-1",
        category: "SECURITY",
        action: "assistant.refused",
        actor: "op-1",
        message: "Refusal: UNGROUNDED_QUERY_REFUSED",
        resource_type: "assistant_response",
        resource_id: "resp-1",
        details: { reason: "UNGROUNDED_QUERY_REFUSED" },
        created_at: "2026-08-10T10:00:00Z",
      },
    ];

    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => mockAuditEvents,
    });

    const data = await fetchAssistantAuditEvents({ limit: 25 });
    expect(data).toHaveLength(1);
    expect(data[0].action).toBe("assistant.refused");
    expect(globalThis.fetch).toHaveBeenCalledWith(
      "/api/v1/persistence/audit-events?category=SECURITY&limit=25",
      expect.anything(),
    );
  });

  it("throws ApiError with isUnauthorized=true on 401 response", async () => {
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 401,
      json: async () => ({ detail: "Not authenticated" }),
    });

    await expect(fetchAssistantResponses()).rejects.toThrow(ApiError);
    try {
      await fetchAssistantResponses();
    } catch (err) {
      expect(err instanceof ApiError).toBe(true);
      if (err instanceof ApiError) {
        expect(err.status).toBe(401);
        expect(err.isUnauthorized).toBe(true);
        expect(err.message).toBe("Not authenticated");
      }
    }
  });

  it("throws ApiError with detail on 500 error", async () => {
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 500,
      json: async () => ({ detail: "Internal database error" }),
    });

    await expect(fetchAssistantResponses()).rejects.toThrow("Internal database error");
  });
});
