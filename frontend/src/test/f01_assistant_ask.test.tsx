/**
 * BO-F-01 — Assistant Ask Surface (2026-08-21)
 *
 * Pins the ask path end-to-end at the unit level:
 *  1. askAssistant posts to POST /api/v1/collaboration/assistant-respond
 *     with Bearer auth + {prompt, grounding_source_ids}; 401 -> typed
 *     ApiError; GET functions untouched.
 *  2. AssistantAskComposer: accessible input (label/placeholder/keyboard),
 *     submit disabled on empty prompt, grounding picker (checkbox, <=10 cap,
 *     remove chips), grounded vs refusal rendering (summary/sources/
 *     disclaimer/audit-correlation), honest submitting/error/401 states,
 *     chip pre-fill.
 *  3. Boundary invariants: no actuation vocabulary anywhere in the ask
 *     surface; the deterministic-local disclosure remains.
 */

import { describe, expect, it, vi } from "vitest";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import {
  askAssistant,
  useAskAssistant,
  type AssistantResearchResponse,
} from "../api/assistantClient";
import {
  AssistantAskComposer,
  ContextualAssistantPanel,
  GROUNDING_FAMILIES,
  MAX_GROUNDING_SOURCE_IDS,
} from "../workstation/ai/ContextualAssistantPanel";
import { WorkspaceContextProvider } from "../workstation/ai/WorkspaceContext";
import * as client from "../api/client";

// ---- Mock api/client (grounding-candidate families) ------------------------
vi.mock("../api/client", async () => {
  const actual = await vi.importActual<typeof client>("../api/client");
  return {
    ...actual,
    fetchCorrelationReports: vi.fn().mockResolvedValue([]),
    fetchRegimeReports: vi.fn().mockResolvedValue([]),
    fetchScenarioReports: vi.fn().mockResolvedValue([]),
    fetchPortfolioRiskReports: vi.fn().mockResolvedValue([]),
    fetchSignalValidationReports: vi.fn().mockResolvedValue([]),
    fetchChartResearchAnnotations: vi.fn().mockResolvedValue([]),
    fetchJournalEntries: vi.fn().mockResolvedValue([]),
    fetchTradePlans: vi.fn().mockResolvedValue([]),
  };
});

vi.mock("../auth/tokenStorage", () => ({
  getAccessToken: () => "test-token",
}));

const GROUNDED_RESPONSE: AssistantResearchResponse = {
  assistant_response_id: "resp-grounded-1",
  created_at: "2026-08-21T10:00:00Z",
  operator_id: "admin",
  request_id: "req-1",
  request_text_hash: "hash-1",
  assistant_policy_version: "w5-u01.non_actuating.v1",
  provider_name: "local_rule_based",
  provider_version: "w5-u02.persisted_response.v1",
  model_or_engine_version: "rule_based_grounded_assistant.v1",
  source_artifact_ids: ["art-101"],
  grounding_summary: "Correlation BTCUSDT/ETHUSDT r=0.7321 n=17520",
  response_text: "Grounded research summary over the selected correlation report.",
  refused: false,
  refusal_reason: null,
  limitations: ["research_assistance_only"],
  disclaimer: "AI-generated research assistance only. Not financial advice, not an instruction, may be wrong. Operator judgment required. AXIOM does not act.",
  research_status: "research_only",
  audit_correlation_id: "corr-ask-1",
  provenance: { external_llm_used: false },
};

const REFUSED_RESPONSE: AssistantResearchResponse = {
  ...GROUNDED_RESPONSE,
  assistant_response_id: "resp-refused-1",
  refused: true,
  refusal_reason: "ORDER_INSTRUCTION_REFUSED",
  response_text: "Refused: ORDER_INSTRUCTION_REFUSED. AI-generated research assistance only.",
  grounding_summary: "",
  source_artifact_ids: [],
  research_status: "refused",
};

describe("BO-F-01.1 — askAssistant client", () => {
  const originalFetch = globalThis.fetch;

  afterEach(() => {
    globalThis.fetch = originalFetch;
    vi.restoreAllMocks();
  });

  it("posts to the B-06 endpoint with Bearer auth and the B-06 body contract", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify(GROUNDED_RESPONSE), { status: 201 }),
    );
    globalThis.fetch = fetchMock as unknown as typeof fetch;

    const result = await askAssistant("summarize the correlation", ["art-101"]);

    expect(fetchMock).toHaveBeenCalledTimes(1);
    const [url, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(url).toBe("/api/v1/collaboration/assistant-respond");
    expect(init.method).toBe("POST");
    const headers = init.headers as Headers;
    expect(headers.get("Authorization")).toBe("Bearer test-token");
    expect(headers.get("Content-Type")).toBe("application/json");
    expect(JSON.parse(init.body as string)).toEqual({
      prompt: "summarize the correlation",
      grounding_source_ids: ["art-101"],
    });
    expect(result.assistant_response_id).toBe("resp-grounded-1");
  });

  it("maps 401 to a typed ApiError (isUnauthorized) without fabricating a response", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ detail: "Not authenticated" }), { status: 401 }),
    );
    globalThis.fetch = fetchMock as unknown as typeof fetch;

    await expect(askAssistant("hi", [])).rejects.toMatchObject({
      isUnauthorized: true,
      status: 401,
    });
  });

  it("maps a structured backend 422 to a readable error", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ detail: "prompt must not be blank" }), { status: 422 }),
    );
    globalThis.fetch = fetchMock as unknown as typeof fetch;

    await expect(askAssistant("hi", [])).rejects.toMatchObject({
      isUnauthorized: false,
      status: 422,
    });
  });
});

describe("BO-F-01.3/.4 — AssistantAskComposer rendering", () => {
  const originalFetch = globalThis.fetch;

  afterEach(() => {
    globalThis.fetch = originalFetch;
    vi.restoreAllMocks();
  });

  function renderComposer() {
    return render(<AssistantAskComposer />);
  }

  it("renders an accessible labelled input, submit, and grounding toggle", () => {
    renderComposer();
    const input = screen.getByTestId("ask-question-input");
    expect(input).toBeInTheDocument();
    expect(screen.getByLabelText(/Ask the grounded assistant/i)).toBe(input);
    expect(input.getAttribute("placeholder")).toContain("research artifacts");
    expect(screen.getByTestId("ask-submit-btn")).toBeDisabled();
    expect(screen.getByTestId("grounding-toggle-btn")).toHaveTextContent("0/10");
  });

  it("disables submit on an empty prompt and never sends (honest empty)", async () => {
    const fetchMock = vi.fn();
    globalThis.fetch = fetchMock as unknown as typeof fetch;
    renderComposer();

    const form = screen.getByTestId("ask-form");
    fireEvent.submit(form);
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("submits the trimmed prompt + selected grounding ids (form submit; the Enter-key path is a browser behavior exercised in the Level-I capture — jsdom does not implement implicit form submission)", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify(GROUNDED_RESPONSE), { status: 201 }),
    );
    globalThis.fetch = fetchMock as unknown as typeof fetch;
    renderComposer();

    fireEvent.change(screen.getByTestId("ask-question-input"), {
      target: { value: "  summarize the correlation  " },
    });
    // The input lives inside the form that owns the submit button — the
    // browser performs implicit submission on Enter; jsdom does not, so the
    // unit test drives the form submit directly.
    const input = screen.getByTestId("ask-question-input") as HTMLInputElement;
    expect(input.type).toBe("text");
    expect(input.closest("form")).toBe(screen.getByTestId("ask-form"));
    fireEvent.submit(screen.getByTestId("ask-form"));
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1));
    const [, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(JSON.parse(init.body as string).prompt).toBe("summarize the correlation");
  });

  it("renders a grounded response with summary, sources, disclaimer, and audit correlation", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify(GROUNDED_RESPONSE), { status: 201 }),
    );
    globalThis.fetch = fetchMock as unknown as typeof fetch;
    renderComposer();

    fireEvent.change(screen.getByTestId("ask-question-input"), {
      target: { value: "summarize the correlation" },
    });
    fireEvent.click(screen.getByTestId("ask-submit-btn"));

    await waitFor(() =>
      expect(screen.getByTestId("ask-result-grounded")).toBeInTheDocument(),
    );
    expect(screen.getByTestId("ask-grounding-summary")).toHaveTextContent("r=0.7321");
    expect(screen.getByTestId("ask-source-ids")).toHaveTextContent("art-101");
    expect(screen.getByTestId("ask-response-text")).toHaveTextContent("Grounded research summary");
    expect(screen.getByTestId("ask-result-disclaimer")).toHaveTextContent(
      "AI-generated research assistance only",
    );
    expect(screen.getByTestId("ask-audit-correlation")).toHaveTextContent("corr-ask-1");
  });

  it("renders a classed refusal distinctly (never as an error)", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify(REFUSED_RESPONSE), { status: 201 }),
    );
    globalThis.fetch = fetchMock as unknown as typeof fetch;
    renderComposer();

    fireEvent.change(screen.getByTestId("ask-question-input"), {
      target: { value: "place an order" },
    });
    fireEvent.click(screen.getByTestId("ask-submit-btn"));

    await waitFor(() =>
      expect(screen.getByTestId("ask-result-refused")).toBeInTheDocument(),
    );
    expect(screen.getByTestId("ask-refusal-class")).toHaveTextContent(
      "Refused: ORDER_INSTRUCTION_REFUSED",
    );
    expect(screen.queryByTestId("ask-error-banner")).not.toBeInTheDocument();
  });

  it("handles 401 honestly with the auth-required notice", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ detail: "Not authenticated" }), { status: 401 }),
    );
    globalThis.fetch = fetchMock as unknown as typeof fetch;
    renderComposer();

    fireEvent.change(screen.getByTestId("ask-question-input"), {
      target: { value: "hi" },
    });
    fireEvent.click(screen.getByTestId("ask-submit-btn"));

    await waitFor(() =>
      expect(screen.getByTestId("ask-auth-required")).toBeInTheDocument(),
    );
    expect(screen.queryByTestId("ask-result-grounded")).not.toBeInTheDocument();
  });

  it("handles backend error honestly with the error banner", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ detail: "Assistant response not persisted" }), {
        status: 500,
      }),
    );
    globalThis.fetch = fetchMock as unknown as typeof fetch;
    renderComposer();

    fireEvent.change(screen.getByTestId("ask-question-input"), {
      target: { value: "hi" },
    });
    fireEvent.click(screen.getByTestId("ask-submit-btn"));

    await waitFor(() =>
      expect(screen.getByTestId("ask-error-banner")).toBeInTheDocument(),
    );
    expect(screen.queryByTestId("ask-result-grounded")).not.toBeInTheDocument();
  });

  it("grounding selector: lists candidates, selects/removes, and caps at 10", async () => {
    const candidates = Array.from({ length: 12 }, (_, i) => ({
      id: `art-${i}`,
      family: "correlation-report",
      label: `Correlation pair ${i}`,
    }));
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify(GROUNDED_RESPONSE), { status: 201 }),
    );
    globalThis.fetch = fetchMock as unknown as typeof fetch;
    vi.mocked(client.fetchCorrelationReports).mockResolvedValueOnce(
      candidates as unknown as Awaited<ReturnType<typeof client.fetchCorrelationReports>>,
    );
    renderComposer();

    fireEvent.click(screen.getByTestId("grounding-toggle-btn"));
    await waitFor(() =>
      expect(screen.getByTestId("grounding-picker")).toBeInTheDocument(),
    );

    // Select 10 (cap reached)
    for (let i = 0; i < MAX_GROUNDING_SOURCE_IDS; i++) {
      fireEvent.click(screen.getByTestId(`grounding-checkbox-art-${i}`));
    }
    expect(screen.getByTestId("grounding-toggle-btn")).toHaveTextContent("10/10");
    // The 11th checkbox is disabled at the cap.
    expect(screen.getByTestId("grounding-checkbox-art-10")).toBeDisabled();
    expect(screen.getByTestId("grounding-checkbox-art-11")).toBeDisabled();

    // Remove one -> the cap opens.
    fireEvent.click(screen.getByTestId("grounding-selected-art-0"));
    expect(screen.getByTestId("grounding-toggle-btn")).toHaveTextContent("9/10");

    // Submit carries the remaining ids.
    fireEvent.change(screen.getByTestId("ask-question-input"), {
      target: { value: "summarize" },
    });
    fireEvent.click(screen.getByTestId("ask-submit-btn"));
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1));
    const [, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    const body = JSON.parse(init.body as string);
    expect(body.grounding_source_ids).toHaveLength(9);
    expect(body.grounding_source_ids).not.toContain("art-0");
  });

  it("empty grounding selection still submits (honest GROUNDING_REQUIRED path)", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(
        JSON.stringify({
          ...GROUNDED_RESPONSE,
          refused: true,
          refusal_reason: "GROUNDING_REQUIRED",
          source_artifact_ids: [],
          grounding_summary: "",
        }),
        { status: 201 },
      ),
    );
    globalThis.fetch = fetchMock as unknown as typeof fetch;
    renderComposer();

    fireEvent.change(screen.getByTestId("ask-question-input"), {
      target: { value: "market outlook" },
    });
    fireEvent.click(screen.getByTestId("ask-submit-btn"));

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1));
    const [, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(JSON.parse(init.body as string).grounding_source_ids).toEqual([]);
    await waitFor(() =>
      expect(screen.getByTestId("ask-refusal-class")).toHaveTextContent(
        "Refused: GROUNDING_REQUIRED",
      ),
    );
  });

  it("no actuation vocabulary anywhere in the ask surface", () => {
    renderComposer();
    const surface = screen.getByTestId("assistant-ask-composer");
    const text = surface.textContent ?? "";
    for (const forbidden of [
      "place order",
      "buy",
      "sell",
      "broker",
      "execution",
      "account",
    ]) {
      expect(text.toLowerCase()).not.toContain(forbidden);
    }
  });
});

describe("BO-F-01 — panel integration (chips pre-fill the ask input)", () => {
  const originalFetch = globalThis.fetch;

  afterEach(() => {
    globalThis.fetch = originalFetch;
    vi.restoreAllMocks();
  });

  it("suggestion chips now pre-fill the composer input and keep the existing contract", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify(GROUNDED_RESPONSE), { status: 201 }),
    );
    globalThis.fetch = fetchMock as unknown as typeof fetch;
    const onSelectPrompt = vi.fn();

    render(
      <WorkspaceContextProvider
        initialState={{ activeWorkspaceId: "intelligence", activeSymbol: "GBPUSD" }}
      >
        <ContextualAssistantPanel
          liveResponses={[]}
          onSelectPrompt={onSelectPrompt}
        />
      </WorkspaceContextProvider>,
    );

    const chip = screen.getAllByTestId("prompt-suggestion-chip")[0];
    const chipText = chip.textContent ?? "";
    fireEvent.click(chip);

    expect(onSelectPrompt).toHaveBeenCalledTimes(1);
    expect(screen.getByTestId("selected-prompt-feedback")).toBeInTheDocument();
    await waitFor(() => {
      expect((screen.getByTestId("ask-question-input") as HTMLInputElement).value).toContain(
        chipText.replace(/^\u203A\s*/, "").split(" ")[0],
      );
    });
  });

  it("panel preserves the mandatory disclaimer and RESEARCH-ONLY framing", () => {
    render(
      <WorkspaceContextProvider>
        <ContextualAssistantPanel liveResponses={[]} />
      </WorkspaceContextProvider>,
    );
    expect(screen.getByTestId("contextual-disclaimer")).toHaveTextContent(
      "AI-generated research assistance only",
    );
    expect(screen.getByTestId("contextual-disclaimer")).toHaveTextContent(
      "AXIOM does not act",
    );
  });
});

describe("BO-F-01.1 — useAskAssistant hook", () => {
  const originalFetch = globalThis.fetch;

  afterEach(() => {
    globalThis.fetch = originalFetch;
    vi.restoreAllMocks();
  });

  function HookHarness() {
    const { ask, submitting, response, isUnauthorized } = useAskAssistant();
    return (
      <div>
        <button
          type="button"
          data-testid="hook-ask"
          onClick={() => void ask("hello", [])}
        >
          ask
        </button>
        <span data-testid="hook-submitting">{String(submitting)}</span>
        <span data-testid="hook-unauthorized">{String(isUnauthorized)}</span>
        <span data-testid="hook-response">{response?.assistant_response_id ?? "none"}</span>
      </div>
    );
  }

  it("ask resolves the persisted response; 401 flags isUnauthorized", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(new Response(JSON.stringify(GROUNDED_RESPONSE), { status: 201 }))
      .mockResolvedValueOnce(
        new Response(JSON.stringify({ detail: "Not authenticated" }), { status: 401 }),
      );
    globalThis.fetch = fetchMock as unknown as typeof fetch;
    render(<HookHarness />);

    fireEvent.click(screen.getByTestId("hook-ask"));
    await waitFor(() =>
      expect(screen.getByTestId("hook-response")).toHaveTextContent("resp-grounded-1"),
    );

    fireEvent.click(screen.getByTestId("hook-ask"));
    await waitFor(() =>
      expect(screen.getByTestId("hook-unauthorized")).toHaveTextContent("true"),
    );
    expect(screen.getByTestId("hook-response")).toHaveTextContent("none");
  });
});

describe("BO-F-01 — grounding family registry", () => {
  it("defines exactly the eight B-06 families with a client-side GET surface", () => {
    expect(GROUNDING_FAMILIES.map((family) => family.family)).toEqual([
      "correlation-report",
      "regime-report",
      "scenario-report",
      "portfolio-risk-report",
      "signal-validation-report",
      "chart-annotation",
      "journal-entry",
      "trade-plan",
    ]);
    for (const family of GROUNDING_FAMILIES) {
      expect(typeof family.load).toBe("function");
      expect(typeof family.idOf).toBe("function");
      expect(typeof family.describe).toBe("function");
    }
  });
});
