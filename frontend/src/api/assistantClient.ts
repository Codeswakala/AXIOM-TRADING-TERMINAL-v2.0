/**
 * AXIOM Assistant Client — Typed API Client & React Hooks (UI-008-P02)
 *
 * Provides authenticated, read-only access to:
 * - GET /api/v1/collaboration/assistant-responses
 * - GET /api/v1/collaboration/assistant-responses/{response_id}
 * - GET /api/v1/persistence/audit-events (filtered for assistant/refusal records)
 *
 * Non-Actuating / Read-Only Invariant:
 * - Strictly zero mutation endpoints (no POST, PUT, PATCH, DELETE).
 * - Bearer JWT authentication required.
 * - Handles 401 Unauthorized gracefully.
 */

import { useState, useEffect, useCallback } from "react";
import { getAccessToken } from "../auth/tokenStorage";

export const API_BASE = "";

export interface AssistantResearchResponse {
  assistant_response_id: string;
  created_at: string;
  operator_id: string;
  request_id: string;
  request_text_hash: string;
  assistant_policy_version: string;
  provider_name: string;
  provider_version: string;
  model_or_engine_version: string;
  source_artifact_ids: string[];
  grounding_summary: string;
  response_text: string;
  refused: boolean;
  refusal_reason: string | null;
  limitations: string[];
  disclaimer: string;
  research_status: string;
  audit_correlation_id: string;
  provenance: Record<string, unknown>;
}

export interface AssistantAuditEvent {
  id: string;
  category: string;
  action: string;
  actor: string;
  message: string;
  resource_type: string | null;
  resource_id: string | null;
  details: Record<string, unknown> | null;
  created_at: string;
}

export class ApiError extends Error {
  status: number;
  isUnauthorized: boolean;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.isUnauthorized = status === 401;
  }
}

async function requestWithAuth<T>(path: string): Promise<T> {
  const headers = new Headers();
  headers.set("Accept", "application/json");

  const token = getAccessToken();
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${API_BASE}${path}`, {
    method: "GET",
    headers,
  });

  if (!response.ok) {
    let detail = `Request failed (${response.status}) for ${path}`;
    try {
      const err = (await response.json()) as { detail?: string };
      if (err.detail) {
        detail = String(err.detail);
      }
    } catch {
      /* ignore JSON parse failure on non-JSON error */
    }
    throw new ApiError(detail, response.status);
  }

  return (await response.json()) as T;
}

/**
 * Fetch list of persisted assistant research responses (read-only).
 */
export async function fetchAssistantResponses(
  params: { limit?: number } = {},
): Promise<AssistantResearchResponse[]> {
  const query = new URLSearchParams();
  query.set("limit", String(params.limit ?? 50));
  return requestWithAuth<AssistantResearchResponse[]>(
    `/api/v1/collaboration/assistant-responses?${query.toString()}`,
  );
}

/**
 * Fetch a single persisted assistant research response by ID.
 */
export async function fetchAssistantResponse(
  responseId: string,
): Promise<AssistantResearchResponse> {
  return requestWithAuth<AssistantResearchResponse>(
    `/api/v1/collaboration/assistant-responses/${encodeURIComponent(responseId)}`,
  );
}

/**
 * Fetch refusal and assistant-related audit events (read-only).
 */
export async function fetchAssistantAuditEvents(
  params: { limit?: number; category?: string } = {},
): Promise<AssistantAuditEvent[]> {
  const query = new URLSearchParams();
  query.set("category", params.category ?? "SECURITY");
  query.set("limit", String(params.limit ?? 50));
  return requestWithAuth<AssistantAuditEvent[]>(
    `/api/v1/persistence/audit-events?${query.toString()}`,
  );
}

export interface UseAssistantResponsesState {
  responses: AssistantResearchResponse[];
  loading: boolean;
  error: string | null;
  isUnauthorized: boolean;
  reload: () => Promise<void>;
}

/**
 * React hook for consuming persisted assistant responses.
 */
export function useAssistantResponses(
  options: { autoFetch?: boolean; limit?: number } = {},
): UseAssistantResponsesState {
  const { autoFetch = true, limit = 50 } = options;
  const [responses, setResponses] = useState<AssistantResearchResponse[]>([]);
  const [loading, setLoading] = useState<boolean>(autoFetch);
  const [error, setError] = useState<string | null>(null);
  const [isUnauthorized, setIsUnauthorized] = useState<boolean>(false);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    setIsUnauthorized(false);
    try {
      const data = await fetchAssistantResponses({ limit });
      setResponses(Array.isArray(data) ? data : []);
    } catch (err: unknown) {
      if (err instanceof ApiError && err.isUnauthorized) {
        setIsUnauthorized(true);
        setError("Unauthorized: Valid operator session required.");
      } else if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Failed to load assistant responses.");
      }
      setResponses([]);
    } finally {
      setLoading(false);
    }
  }, [limit]);

  useEffect(() => {
    if (autoFetch) {
      void load();
    }
  }, [autoFetch, load]);

  return { responses, loading, error, isUnauthorized, reload: load };
}

export interface UseAssistantAuditState {
  auditEvents: AssistantAuditEvent[];
  loading: boolean;
  error: string | null;
  isUnauthorized: boolean;
  reload: () => Promise<void>;
}

/**
 * React hook for consuming assistant & refusal audit events.
 */
export function useAssistantAudit(
  options: { autoFetch?: boolean; limit?: number; category?: string } = {},
): UseAssistantAuditState {
  const { autoFetch = true, limit = 50, category = "SECURITY" } = options;
  const [auditEvents, setAuditEvents] = useState<AssistantAuditEvent[]>([]);
  const [loading, setLoading] = useState<boolean>(autoFetch);
  const [error, setError] = useState<string | null>(null);
  const [isUnauthorized, setIsUnauthorized] = useState<boolean>(false);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    setIsUnauthorized(false);
    try {
      const data = await fetchAssistantAuditEvents({ limit, category });
      setAuditEvents(Array.isArray(data) ? data : []);
    } catch (err: unknown) {
      if (err instanceof ApiError && err.isUnauthorized) {
        setIsUnauthorized(true);
        setError("Unauthorized: Valid operator session required to view audit events.");
      } else if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Failed to load assistant audit events.");
      }
      setAuditEvents([]);
    } finally {
      setLoading(false);
    }
  }, [limit, category]);

  useEffect(() => {
    if (autoFetch) {
      void load();
    }
  }, [autoFetch, load]);

  return { auditEvents, loading, error, isUnauthorized, reload: load };
}

/* =========================================================================
   BO-F-01 — Assistant ask path (2026-08-21)
   -------------------------------------------------------------------------
   The B-06 backend seam is POST /api/v1/collaboration/assistant-respond:
   grounded, deterministic, local, non-actuating, refusal-classed. This adds
   the client-side ask (POST) alongside the existing read-only GET surface.

   Boundary invariants (BO-F-01 §7 / F-01.4):
   - Bearer JWT only; the prompt goes to the LOCAL backend — no third party.
   - 401 handled as a typed ApiError (no fabricated response).
   - The prompt is never logged client-side.
   ========================================================================= */

/**
 * Ask the grounded assistant (BO-B-06 contract). Returns the persisted
 * AssistantResearchResponse — either a grounded answer or a classed refusal
 * (e.g. GROUNDING_REQUIRED when no source ids are selected).
 */
export async function askAssistant(
  prompt: string,
  groundingSourceIds: string[],
): Promise<AssistantResearchResponse> {
  const headers = new Headers();
  headers.set("Accept", "application/json");
  headers.set("Content-Type", "application/json");

  const token = getAccessToken();
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(
    `${API_BASE}/api/v1/collaboration/assistant-respond`,
    {
      method: "POST",
      headers,
      body: JSON.stringify({
        prompt,
        grounding_source_ids: groundingSourceIds,
      }),
    },
  );

  if (!response.ok) {
    let detail = `Assistant ask failed (${response.status})`;
    try {
      const err = (await response.json()) as { detail?: unknown };
      if (typeof err.detail === "string" && err.detail) {
        detail = err.detail;
      } else if (err.detail && typeof err.detail === "object") {
        const structured = err.detail as { detail?: string };
        if (structured.detail) detail = structured.detail;
      }
    } catch {
      /* ignore JSON parse failure on non-JSON error */
    }
    throw new ApiError(detail, response.status);
  }

  return (await response.json()) as AssistantResearchResponse;
}

export interface UseAskAssistantState {
  ask: (prompt: string, groundingSourceIds: string[]) => Promise<boolean>;
  submitting: boolean;
  error: string | null;
  isUnauthorized: boolean;
  response: AssistantResearchResponse | null;
  reset: () => void;
}

/**
 * React hook wrapping the ask path. `ask` resolves true when a response or
 * refusal was persisted (a refusal IS a valid assistant response — it is
 * rendered distinctly, never treated as an error).
 */
export function useAskAssistant(): UseAskAssistantState {
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [isUnauthorized, setIsUnauthorized] = useState<boolean>(false);
  const [response, setResponse] = useState<AssistantResearchResponse | null>(null);

  const ask = useCallback(
    async (prompt: string, groundingSourceIds: string[]): Promise<boolean> => {
      setSubmitting(true);
      setError(null);
      setIsUnauthorized(false);
      try {
        const result = await askAssistant(prompt, groundingSourceIds);
        setResponse(result);
        return true;
      } catch (err: unknown) {
        setResponse(null);
        if (err instanceof ApiError && err.isUnauthorized) {
          setIsUnauthorized(true);
          setError("Unauthorized: Valid operator session required to ask the assistant.");
        } else if (err instanceof Error) {
          setError(err.message);
        } else {
          setError("Failed to reach the assistant.");
        }
        return false;
      } finally {
        setSubmitting(false);
      }
    },
    [],
  );

  const reset = useCallback(() => {
    setResponse(null);
    setError(null);
    setIsUnauthorized(false);
  }, []);

  return { ask, submitting, error, isUnauthorized, response, reset };
}
