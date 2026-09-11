// N-1: AssistantCommandSurface.tsx
// Source: /home/user/axiom/frontend/src/workstation/ai/AssistantCommandSurface.tsx
// UI-008-P03: Extended with live response data & contextual prompt suggestions.
// Non-actuating / read-only: Zero order or execution controls.

import { useState, useMemo } from "react";
import { ASSISTANT_DISABLED_REASON, ASSISTANT_REFUSAL_REASON_CODES } from "../../test/ui008_refusal_taxonomy.fixture";
import { ASSISTANT_DISCLOSURE_REGISTER } from "../../test/ui008_disclosure_register.fixture";
import {
  type AssistantResearchResponse,
  useAssistantResponses,
} from "../../api/assistantClient";
import { useWorkspaceContext } from "./WorkspaceContext";
import { generatePromptSuggestions } from "./ContextualAssistantPanel";

/**
 * Pinned identifiers of record (BO §3.4, §3.5, §3.6, §3.7; R5-6; R-7 REQUIRED; TD-078 banner).
 * These strings are byte-equal wherever they render; never re-typed at the call site.
 */
export const AI_DISCLAIMER_TEXT =
  "AI-generated research assistance only. Not financial advice, not an instruction, may be wrong. Operator judgment required. AXIOM does not act.";

export const SELF_DESCRIPTION_BANNER_TEXT =
  "deterministic local assistant; no external LLM; external LLM requires a future gated Build Order";

export interface AssistantCommandSurfaceProps {
  /** If provided, overrides internal hook state for testing */
  liveResponses?: AssistantResearchResponse[];
  loading?: boolean;
  error?: string | null;
  isUnauthorized?: boolean;
  /** Whether to automatically fetch live data (default: false for P01 test backward-compat) */
  autoFetch?: boolean;
  onSelectPrompt?: (prompt: string) => void;
  showSuggestions?: boolean;
}

/**
 * AssistantCommandSurface — UI-008-P03 (additive; mounts within the UI-002 command palette surface).
 *
 * Disposition:
 * - Renders the AI experience frame, title, self-description banner (TD-078), disclaimer (R5-6), and a
 *   disclosure mount point that surfaces the carried-open register (BO §3.9).
 * - Surfaces the six-code refusal taxonomy as a read-only fixture list (BO §3.2).
 * - P02 Live Seam: Displays loading skeleton, error banner, 401 auth notice, empty state, or response list.
 * - P03 Extension: Contextual prompt suggestions based on active workspace state.
 * - Read-only by architecture; no POST/PUT/PATCH/DELETE; no new endpoint; no new route.
 */
export function AssistantCommandSurface({
  liveResponses,
  loading: propLoading,
  error: propError,
  isUnauthorized: propUnauthorized,
  autoFetch = false,
  onSelectPrompt,
  showSuggestions = false,
}: AssistantCommandSurfaceProps = {}) {
  const hookState = useAssistantResponses({ autoFetch });
  const [selectedPrompt, setSelectedPrompt] = useState<string | null>(null);

  const {
    activeWorkspaceId,
    activeSymbol,
    activeTimeframe,
    selectedArtifactId,
  } = useWorkspaceContext();

  const loading = propLoading !== undefined ? propLoading : hookState.loading;
  const error = propError !== undefined ? propError : hookState.error;
  const isUnauthorized =
    propUnauthorized !== undefined ? propUnauthorized : hookState.isUnauthorized;
  const responses = liveResponses !== undefined ? liveResponses : hookState.responses;

  const isSkeletonEmpty = !loading && !error && !isUnauthorized && responses.length === 0;

  const promptSuggestions = useMemo(
    () =>
      generatePromptSuggestions(
        activeWorkspaceId,
        activeSymbol,
        activeTimeframe,
        selectedArtifactId,
      ),
    [activeWorkspaceId, activeSymbol, activeTimeframe, selectedArtifactId],
  );

  function handlePromptClick(prompt: string) {
    setSelectedPrompt(prompt);
    if (onSelectPrompt) {
      onSelectPrompt(prompt);
    }
  }

  return (
    <section
      className="ix-assistant-command-surface"
      data-ui008-component="assistant-command-surface"
      role="region"
      data-ui008-p01-skeleton-empty={isSkeletonEmpty ? "true" : undefined}
      aria-label="Assistant Command Surface"
    >
      <header className="ix-assistant-command-surface__header">
        <h2 className="ix-assistant-command-surface__title">
          Institutional AI Experience — Assistant Command Surface
        </h2>
        <p
          className="ix-assistant-command-surface__banner"
          data-ui008-banner="td-078-self-description"
          data-testid="td-078-self-description"
        >
          {SELF_DESCRIPTION_BANNER_TEXT}
        </p>
        <p
          className="ix-assistant-command-surface__disclaimer"
          data-ui008-disclaimer="r5-6"
          data-testid="r5-6"
        >
          {AI_DISCLAIMER_TEXT}
        </p>
      </header>

      <div
        className="ix-assistant-command-surface__body"
        data-ui008-p01-skeleton-empty={isSkeletonEmpty ? "true" : undefined}
      >
        {/* Contextual Prompt Suggestions (P03) */}
        {showSuggestions && (
          <div className="ix-command-surface-suggestions" data-testid="command-surface-suggestions">
            <h3 className="ix-suggestions-title">Contextual Inquiries</h3>
            <div className="ix-suggestions-row" role="group" aria-label="Suggested inquiries">
              {promptSuggestions.slice(0, 4).map((prompt) => (
                <button
                  key={prompt}
                  type="button"
                  className={`ix-prompt-chip ${selectedPrompt === prompt ? "ix-prompt-chip--selected" : ""}`}
                  onClick={() => handlePromptClick(prompt)}
                  data-testid="command-prompt-chip"
                >
                  {prompt}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Loading State: Skeleton Placeholders */}
        {loading && (
          <div
            className="ix-assistant-command-surface__loading"
            data-testid="assistant-loading-skeleton"
            data-ui008-state="loading"
            role="status"
            aria-live="polite"
          >
            <div className="ix-skeleton ix-skeleton--title" />
            <div className="ix-skeleton ix-skeleton--line" />
            <div className="ix-skeleton ix-skeleton--line" />
            <p className="ix-assistant-loading-text">Loading verified assistant responses...</p>
          </div>
        )}

        {/* 401 Unauthorized State */}
        {!loading && isUnauthorized && (
          <div
            className="ix-assistant-command-surface__auth-required"
            data-testid="assistant-auth-required"
            data-ui008-state="unauthorized"
            role="alert"
          >
            <span className="ix-auth-icon" aria-hidden="true">{"\u{1F512}"}</span>
            <p className="ix-auth-message">
              Authentication required. Valid operator session required to access live assistant responses.
            </p>
          </div>
        )}

        {/* Error State */}
        {!loading && !isUnauthorized && error && (
          <div
            className="ix-assistant-command-surface__error"
            data-testid="assistant-error-banner"
            data-ui008-state="error"
            role="alert"
          >
            <span className="ix-error-icon" aria-hidden="true">{"\u{26A0}"}</span>
            <p className="ix-error-message">{error}</p>
          </div>
        )}

        {/* Live Responses List */}
        {!loading && !isUnauthorized && !error && responses.length > 0 && (
          <div
            className="ix-assistant-command-surface__responses"
            data-testid="assistant-response-list"
            data-ui008-state="ready"
          >
            <h3 className="ix-assistant-responses-heading">Recent Assistant Research Responses</h3>
            <ul className="ix-assistant-response-list" role="list">
              {responses.map((resp) => (
                <li
                  key={resp.assistant_response_id}
                  className={`ix-assistant-response-item ${resp.refused ? "ix-response--refused" : "ix-response--valid"}`}
                  data-ui008-response-row={resp.assistant_response_id}
                  data-testid={`response-${resp.assistant_response_id}`}
                >
                  <div className="ix-response-header">
                    <span className="ix-response-id">{resp.assistant_response_id}</span>
                    <span className="ix-response-timestamp">{resp.created_at}</span>
                    {resp.refused ? (
                      <span
                        className="ix-response-badge ix-response-badge--refused"
                        data-testid="refusal-badge"
                      >
                        REFUSED: {resp.refusal_reason ?? "UNKNOWN_REASON"}
                      </span>
                    ) : (
                      <span className="ix-response-badge ix-response-badge--ok">
                        {resp.research_status}
                      </span>
                    )}
                  </div>
                  <p className="ix-response-summary">{resp.grounding_summary}</p>
                  <p className="ix-response-text">{resp.response_text}</p>
                  {resp.limitations && resp.limitations.length > 0 && (
                    <div className="ix-response-limitations">
                      <span className="ix-limitations-label">Limitations: </span>
                      {resp.limitations.join("; ")}
                    </div>
                  )}
                  <div className="ix-response-provenance">
                    <small>Provider: {resp.provider_name} ({resp.model_or_engine_version})</small>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Empty State / P01 Skeleton fallback */}
        {isSkeletonEmpty && (
          <p
            className="ix-assistant-command-surface__empty"
            data-ui008-empty-state="p01-skeleton"
            data-testid="p01-skeleton"
          >
            <span data-ui008-icon="empty" aria-hidden="true">{"\u{1F4ED}"}</span>
            {" "}Assistant surface skeleton. Live wiring deferred to P02 (Navigator + guidance lane).
          </p>
        )}
      </div>

      <footer className="ix-assistant-command-surface__footer">
        <h3 className="ix-assistant-command-surface__disclosure-title">
          Carried-Open Register (BO §3.9; verbatim)
        </h3>
        <AssistantDisclosureRegister />

        <h3 className="ix-assistant-command-surface__refusal-title">
          Refusal Taxonomy (BO §3.2; six codes; test 27)
        </h3>
        <AssistantRefusalSurface />
      </footer>
    </section>
  );
}

/**
 * AssistantDisclosureRegister — renders the carried-open register (BO §3.9; D-2.6 conformance).
 */
function AssistantDisclosureRegister() {
  return (
    <ul
      className="ix-assistant-disclosure-register"
      data-ui008-component="disclosure-register"
      role="list"
      aria-label="Carried-Open Register (verbatim, full severity)"
    >
      {ASSISTANT_DISCLOSURE_REGISTER.map((entry) => (
        <li
          key={entry.id}
          className={`ix-assistant-disclosure-register__row ix-severity-${entry.severityClass}`}
          data-ui008-disclosure-row={entry.id}
        >
          <span className="ix-assistant-disclosure-register__icon" data-ui008-icon aria-hidden="true">
            {entry.icon}
          </span>
          <span className="ix-assistant-disclosure-register__id" data-testid="disclosure-id">
            {entry.id}
          </span>
          <span
            className="ix-assistant-disclosure-register__severity"
            data-ui008-severity
            data-testid="disclosure-severity"
          >
            {entry.severityLabel}
          </span>
          <span
            className="ix-assistant-disclosure-register__text"
            data-ui008-disclosure-text
            data-testid="disclosure-text"
          >
            {entry.text}
          </span>
          <span
            className="ix-assistant-disclosure-register__source-pin"
            data-ui008-source-pin
            data-testid="source-pin"
          >
            (source: {entry.sourcePin})
          </span>
        </li>
      ))}
    </ul>
  );
}

/**
 * AssistantRefusalSurface — renders the six-code refusal taxonomy (BO §3.2; test 27).
 */
function AssistantRefusalSurface() {
  return (
    <ul
      className="ix-assistant-refusal-surface"
      data-ui008-component="refusal-surface"
      role="list"
      aria-label="Refusal Taxonomy (six codes, BO §3.2)"
    >
      {ASSISTANT_REFUSAL_REASON_CODES.map((code) => (
        <li
          key={code}
          className="ix-assistant-refusal-surface__row"
          data-ui008-refusal-code={code}
          data-testid={code}
        >
          <span className="ix-assistant-refusal-surface__code">{code}</span>
          <span className="ix-assistant-refusal-surface__label">
            {code === ASSISTANT_DISABLED_REASON
              ? "(admin-state: operator/system has placed the assistant in a disabled state)"
              : "(request-refusal class)"}
          </span>
        </li>
      ))}
    </ul>
  );
}
