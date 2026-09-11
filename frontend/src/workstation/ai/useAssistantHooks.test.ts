import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import { renderHook, waitFor, act } from "@testing-library/react";
import { useAssistantResponses, useAssistantAudit } from "../../api/assistantClient";
import * as tokenStorage from "../../auth/tokenStorage";

describe("UI-008-P02 useAssistantResponses & useAssistantAudit React Hooks", () => {
  const originalFetch = globalThis.fetch;

  beforeEach(() => {
    vi.spyOn(tokenStorage, "getAccessToken").mockReturnValue("test-jwt-token-xyz");
  });

  afterEach(() => {
    globalThis.fetch = originalFetch;
    vi.restoreAllMocks();
  });

  describe("useAssistantResponses", () => {
    it("fetches responses on mount and updates state (T-7)", async () => {
      const mockData = [
        {
          assistant_response_id: "resp-101",
          created_at: "2026-08-10T10:30:00Z",
          operator_id: "admin",
          request_id: "req-101",
          request_text_hash: "hash101",
          assistant_policy_version: "v1.0",
          provider_name: "RuleBasedGroundedAssistant",
          provider_version: "1.0",
          model_or_engine_version: "v1",
          source_artifact_ids: [],
          grounding_summary: "Summary test",
          response_text: "Response test body",
          refused: false,
          refusal_reason: null,
          limitations: [],
          disclaimer: "RESEARCH-ONLY",
          research_status: "ACTIVE",
          audit_correlation_id: "corr-101",
          provenance: {},
        },
      ];

      globalThis.fetch = vi.fn().mockResolvedValue({
        ok: true,
        status: 200,
        json: async () => mockData,
      });

      const { result } = renderHook(() => useAssistantResponses({ autoFetch: true }));

      expect(result.current.loading).toBe(true);

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      expect(result.current.responses).toHaveLength(1);
      expect(result.current.responses[0].assistant_response_id).toBe("resp-101");
      expect(result.current.error).toBeNull();
      expect(result.current.isUnauthorized).toBe(false);
    });

    it("handles 401 error gracefully setting isUnauthorized flag", async () => {
      globalThis.fetch = vi.fn().mockResolvedValue({
        ok: false,
        status: 401,
        json: async () => ({ detail: "Unauthorized operator session" }),
      });

      const { result } = renderHook(() => useAssistantResponses({ autoFetch: true }));

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      expect(result.current.responses).toEqual([]);
      expect(result.current.isUnauthorized).toBe(true);
      expect(result.current.error).toContain("Unauthorized");
    });

    it("reload function re-executes fetch", async () => {
      const mockFetch = vi.fn().mockResolvedValue({
        ok: true,
        status: 200,
        json: async () => [],
      });
      globalThis.fetch = mockFetch;

      const { result } = renderHook(() => useAssistantResponses({ autoFetch: false }));
      expect(result.current.loading).toBe(false);

      await act(async () => {
        await result.current.reload();
      });

      expect(mockFetch).toHaveBeenCalledTimes(1);
    });
  });

  describe("useAssistantAudit", () => {
    it("fetches audit events on mount and updates state (T-8)", async () => {
      const mockAudit = [
        {
          id: "evt-99",
          category: "SECURITY",
          action: "assistant.refused",
          actor: "operator",
          message: "Refusal logged",
          resource_type: "assistant_response",
          resource_id: "resp-99",
          details: null,
          created_at: "2026-08-10T10:45:00Z",
        },
      ];

      globalThis.fetch = vi.fn().mockResolvedValue({
        ok: true,
        status: 200,
        json: async () => mockAudit,
      });

      const { result } = renderHook(() => useAssistantAudit({ autoFetch: true }));

      expect(result.current.loading).toBe(true);

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      expect(result.current.auditEvents).toHaveLength(1);
      expect(result.current.auditEvents[0].id).toBe("evt-99");
      expect(result.current.error).toBeNull();
      expect(result.current.isUnauthorized).toBe(false);
    });

    it("handles 401 error gracefully for audit hook", async () => {
      globalThis.fetch = vi.fn().mockResolvedValue({
        ok: false,
        status: 401,
        json: async () => ({ detail: "Unauthorized" }),
      });

      const { result } = renderHook(() => useAssistantAudit({ autoFetch: true }));

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      expect(result.current.auditEvents).toEqual([]);
      expect(result.current.isUnauthorized).toBe(true);
      expect(result.current.error).toContain("Unauthorized");
    });
  });
});
