/**
 * ContextualAssistantPanel — Embedded Assistant in Context Panel (UI-008-P03)
 *
 * Provides workspace-embedded AI research assistance and contextual prompt suggestions
 * across /intelligence, /investigation, and /charts.
 *
 * BO-F-01 (2026-08-21): the panel now hosts the REAL ask surface —
 * `AssistantAskComposer` — wiring the B-06 backend seam (the grounded
 * assistant-respond endpoint; see `api/assistantClient.ts`):
 *   - accessible question input + submit (label, keyboard, focus)
 *   - operator-selected grounding artifacts (checkbox picker, <=10 ids;
 *     empty selection submits honestly -> backend GROUNDING_REQUIRED)
 *   - grounded-response and classed-refusal rendering with disclaimer +
 *     audit correlation id
 *   - honest loading / error / 401 states (no fabricated responses)
 *   - suggestion chips remain as clickable pre-fill shortcuts (not the
 *     only surface)
 *
 * Non-Actuating / Read-Only Invariant (unchanged and re-pinned by F-01 tests):
 * - Strictly zero order/trade execution controls.
 * - Deterministic local assistant; no external LLM; RESEARCH-ONLY.
 */

import { useEffect, useMemo, useState, type FormEvent } from "react";
import { useWorkspaceContext } from "./WorkspaceContext";
import {
  type AssistantResearchResponse,
  useAskAssistant,
  useAssistantResponses,
} from "../../api/assistantClient";
import {
  fetchChartResearchAnnotations,
  fetchCorrelationReports,
  fetchJournalEntries,
  fetchPortfolioRiskReports,
  fetchRegimeReports,
  fetchScenarioReports,
  fetchSignalValidationReports,
  fetchTradePlans,
} from "../../api/client";
import "./ContextualAssistantPanel.css";

export const CONTEXTUAL_ASSISTANT_DISCLAIMER =
  "AI-generated research assistance only. Not financial advice, not an instruction, may be wrong. Operator judgment required. AXIOM does not act.";

export const MAX_GROUNDING_SOURCE_IDS = 10;

export interface ContextualAssistantPanelProps {
  liveResponses?: AssistantResearchResponse[];
  loading?: boolean;
  error?: string | null;
  isUnauthorized?: boolean;
  autoFetch?: boolean;
  onSelectPrompt?: (prompt: string) => void;
  defaultCollapsed?: boolean;
}

export function generatePromptSuggestions(
  workspaceId: string,
  symbol: string | null,
  timeframe: string | null,
  artifactId: string | null,
): string[] {
  const symbolLabel = symbol ?? "active symbol";
  const tfLabel = timeframe ?? "active timeframe";

  const suggestions: string[] = [];

  const ws = workspaceId.toLowerCase();
  if (ws.includes("intel") || ws.includes("report")) {
    suggestions.push(`Explain regime boundaries for ${symbolLabel}`);
    suggestions.push(`View correlation matrix assumptions (${tfLabel})`);
    suggestions.push("Check calibration quality & ECE bounds");
  } else if (ws.includes("investig") || ws.includes("signal")) {
    suggestions.push(`Trace signal lineage for ${symbolLabel}`);
    suggestions.push("Explain guardrail status & freshness");
    suggestions.push("Check scenario comparison parameters");
  } else if (ws.includes("chart") || ws.includes("market")) {
    suggestions.push(`Summarize structure for ${symbolLabel} (${tfLabel})`);
    suggestions.push(`View historical volatility analogues for ${symbolLabel}`);
    suggestions.push("Check market session & spread context");
  } else {
    suggestions.push(`Inspect research context for ${symbolLabel}`);
    suggestions.push(`View recent advisory signals (${tfLabel})`);
    suggestions.push("Review model uncertainty disclosures");
  }

  if (artifactId) {
    suggestions.push(`Explain provenance of artifact ${artifactId}`);
  }

  suggestions.push("View recent refusal audit events");
  return suggestions;
}

/* =========================================================================
   BO-F-01 — grounding-source candidates
   The B-06 grounding families with a client-side GET surface. Dataset
   snapshots are intentionally absent (no client-side GET exists; ids can
   only come from the other eight families here — honest, per the B-06
   contract where unresolved ids are excluded).
   ========================================================================= */

export interface GroundingCandidate {
  id: string;
  family: string;
  label: string;
}

/** A grounding-family row is an arbitrary persisted-artifact record; the
    per-family accessors own the field semantics. */
export type GroundingFamilyRow = Record<string, unknown>;

export interface GroundingFamily {
  family: string;
  heading: string;
  load: () => Promise<GroundingFamilyRow[]>;
  idOf: (row: GroundingFamilyRow) => string;
  describe: (row: GroundingFamilyRow) => string;
}

const text = (value: unknown): string => (typeof value === "string" ? value : "");

export const GROUNDING_FAMILIES: GroundingFamily[] = [
  {
    family: "correlation-report",
    heading: "Correlation reports",
    load: async () =>
      (await fetchCorrelationReports(20)).map(
        (row) => row as unknown as GroundingFamilyRow,
      ),
    idOf: (row) => text(row.id),
    describe: (row) =>
      `Correlation ${text(row.left_symbol)}/${text(row.right_symbol)} ${text(row.timeframe)}`,
  },
  {
    family: "regime-report",
    heading: "Regime reports",
    load: async () =>
      (await fetchRegimeReports(20)).map((row) => row as unknown as GroundingFamilyRow),
    idOf: (row) => text(row.id),
    describe: (row) =>
      `Regime ${text(row.symbol)} ${text(row.timeframe)} (${text(row.regime_label)})`,
  },
  {
    family: "scenario-report",
    heading: "Scenario reports",
    load: async () =>
      (await fetchScenarioReports(20)).map(
        (row) => row as unknown as GroundingFamilyRow,
      ),
    idOf: (row) => text(row.id),
    describe: (row) => `Scenario ${text(row.symbol)} ${text(row.timeframe)}`,
  },
  {
    family: "portfolio-risk-report",
    heading: "Portfolio-risk reports",
    load: async () =>
      (await fetchPortfolioRiskReports(20)).map(
        (row) => row as unknown as GroundingFamilyRow,
      ),
    idOf: (row) => text(row.id),
    describe: (row) => `Portfolio-risk ${text(row.symbol)} ${text(row.timeframe)}`,
  },
  {
    family: "signal-validation-report",
    heading: "Signal-validation reports",
    load: async () =>
      (await fetchSignalValidationReports(20)).map(
        (row) => row as unknown as GroundingFamilyRow,
      ),
    idOf: (row) => text(row.id),
    describe: (row) => `Signal validation (n=${String(row.sample_count ?? "")})`,
  },
  {
    family: "chart-annotation",
    heading: "Chart annotations",
    load: async () =>
      (await fetchChartResearchAnnotations({ limit: 20 })).map(
        (row) => row as unknown as GroundingFamilyRow,
      ),
    idOf: (row) => text(row.id),
    describe: (row) => `Chart annotation (${text(row.artifact_type)})`,
  },
  {
    family: "journal-entry",
    heading: "Journal entries",
    load: async () =>
      (await fetchJournalEntries(20)).map(
        (row) => row as unknown as GroundingFamilyRow,
      ),
    idOf: (row) => text(row.journal_id),
    describe: (row) => `Journal: ${text(row.title)}`,
  },
  {
    family: "trade-plan",
    heading: "Trade-plan notes",
    load: async () =>
      (await fetchTradePlans(20)).map((row) => row as unknown as GroundingFamilyRow),
    idOf: (row) => text(row.plan_id),
    describe: (row) => `Trade plan: ${text(row.title)}`,
  },
];

export interface AssistantAskComposerProps {
  /** Suggestion chips pre-fill the input through this one-shot prompt. */
  prefillPrompt?: string | null;
  /** Called when the prefill has been consumed (clears the draft owner). */
  onPrefillConsumed?: () => void;
}

/**
 * AssistantAskComposer — the BO-F-01 ask surface.
 *
 * Question input + submit + grounding selector + grounded/refusal rendering.
 * Never fabricates: loading skeleton while asking, error banner on failure,
 * auth notice on 401, and a classed refusal is rendered as the backend's own
 * honest answer (not as an error).
 */
export function AssistantAskComposer({
  prefillPrompt,
  onPrefillConsumed,
}: AssistantAskComposerProps = {}) {
  const { ask, submitting, error, isUnauthorized, response } = useAskAssistant();
  const [promptDraft, setPromptDraft] = useState<string>("");
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [pickerOpen, setPickerOpen] = useState<boolean>(false);
  const [candidates, setCandidates] = useState<GroundingCandidate[]>([]);
  const [pickerLoading, setPickerLoading] = useState<boolean>(true);
  const [pickerNote, setPickerNote] = useState<string | null>(null);

  // Load grounding candidates across the eight families (tolerant: a
  // failing family yields an empty slice, never a broken surface).
  useEffect(() => {
    let cancelled = false;
    async function loadCandidates() {
      setPickerLoading(true);
      const settled = await Promise.allSettled(
        GROUNDING_FAMILIES.map((family) => family.load()),
      );
      if (cancelled) return;
      const collected: GroundingCandidate[] = [];
      let failures = 0;
      settled.forEach((result, index) => {
        if (result.status === "fulfilled" && Array.isArray(result.value)) {
          const family = GROUNDING_FAMILIES[index];
          for (const row of result.value) {
            collected.push({
              id: family.idOf(row),
              family: family.family,
              label: family.describe(row),
            });
          }
        } else {
          failures += 1;
        }
      });
      setCandidates(collected);
      setPickerNote(
        collected.length === 0
          ? "No persisted artifacts available to ground an answer yet. Submit without a selection for the honest GROUNDING_REQUIRED refusal."
          : failures > 0
            ? "Some artifact families could not be loaded; the listed artifacts are the complete available set."
            : null,
      );
      setPickerLoading(false);
    }
    void loadCandidates();
    return () => {
      cancelled = true;
    };
  }, []);

  // Suggestion-chip pre-fill (one-shot).
  useEffect(() => {
    if (prefillPrompt !== undefined && prefillPrompt !== null && prefillPrompt !== "") {
      setPromptDraft(prefillPrompt);
      onPrefillConsumed?.();
    }
  }, [prefillPrompt, onPrefillConsumed]);

  const trimmedPrompt = promptDraft.trim();
  const atSelectionCap = selectedIds.length >= MAX_GROUNDING_SOURCE_IDS;

  function toggleCandidate(candidateId: string) {
    setSelectedIds((current) => {
      if (current.includes(candidateId)) {
        return current.filter((id) => id !== candidateId);
      }
      if (current.length >= MAX_GROUNDING_SOURCE_IDS) {
        return current;
      }
      return [...current, candidateId];
    });
  }

  function removeSelected(candidateId: string) {
    setSelectedIds((current) => current.filter((id) => id !== candidateId));
  }

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    if (!trimmedPrompt || submitting) {
      return; // honest: an empty ask is not sent
    }
    await ask(trimmedPrompt, selectedIds);
  }

  return (
    <section
      className="ix-ask-composer"
      data-f01-component="assistant-ask-composer"
      data-testid="assistant-ask-composer"
      aria-label="Assistant ask"
    >
      <form className="ix-ask-form" onSubmit={handleSubmit} data-testid="ask-form">
        <label className="ix-ask-label" htmlFor="assistant-question-input">
          Ask the grounded assistant
        </label>
        <div className="ix-ask-input-row">
          <input
            id="assistant-question-input"
            className="ix-ask-input"
            type="text"
            value={promptDraft}
            onChange={(event) => setPromptDraft(event.target.value)}
            placeholder="Ask about your selected research artifacts…"
            maxLength={1000}
            disabled={submitting}
            data-testid="ask-question-input"
          />
          <button
            type="submit"
            className="ix-ask-submit-btn"
            disabled={!trimmedPrompt || submitting}
            data-testid="ask-submit-btn"
          >
            {submitting ? "Asking…" : "Ask"}
          </button>
        </div>
      </form>

      <div className="ix-grounding-section" data-testid="grounding-selector">
        <button
          type="button"
          className="ix-grounding-toggle"
          onClick={() => setPickerOpen((current) => !current)}
          aria-expanded={pickerOpen}
          data-testid="grounding-toggle-btn"
        >
          Grounding artifacts ({selectedIds.length}/{MAX_GROUNDING_SOURCE_IDS})
          {pickerOpen ? " ▾" : " ▸"}
        </button>

        {pickerOpen && (
          <div className="ix-grounding-picker" data-testid="grounding-picker">
            <p className="ix-grounding-hint">
              Select persisted artifacts the answer must be grounded in. No selection is
              honest too — the backend returns its GROUNDING_REQUIRED refusal.
            </p>
            {pickerLoading && (
              <p className="ix-grounding-muted" data-testid="grounding-loading">
                Loading available artifacts…
              </p>
            )}
            {!pickerLoading && pickerNote && (
              <p className="ix-grounding-muted" data-testid="grounding-note">
                {pickerNote}
              </p>
            )}
            {!pickerLoading && candidates.length > 0 && (
              <ul className="ix-grounding-list" role="group" aria-label="Grounding artifacts">
                {candidates.map((candidate) => {
                  const checked = selectedIds.includes(candidate.id);
                  const disabled = !checked && atSelectionCap;
                  return (
                    <li key={candidate.id} className="ix-grounding-item">
                      <label
                        className={`ix-grounding-label${disabled ? " ix-grounding-label--disabled" : ""}`}
                      >
                        <input
                          type="checkbox"
                          checked={checked}
                          disabled={disabled}
                          onChange={() => toggleCandidate(candidate.id)}
                          data-testid={`grounding-checkbox-${candidate.id}`}
                        />
                        <span className="ix-grounding-family mono">{candidate.family}</span>
                        <span className="ix-grounding-desc">{candidate.label}</span>
                        <span className="ix-grounding-id mono">{candidate.id}</span>
                      </label>
                    </li>
                  );
                })}
              </ul>
            )}
          </div>
        )}

        {selectedIds.length > 0 && (
          <div className="ix-grounding-selected" data-testid="grounding-selected-chips">
            {selectedIds.map((id) => (
              <button
                key={id}
                type="button"
                className="ix-grounding-chip mono"
                onClick={() => removeSelected(id)}
                aria-label={`Remove grounding artifact ${id}`}
                data-testid={`grounding-selected-${id}`}
              >
                {id} ✕
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Ask lifecycle states — honest, never fabricated */}
      {submitting && (
        <div
          className="ix-ask-submitting"
          data-testid="ask-submitting-state"
          role="status"
          aria-live="polite"
        >
          <div className="ix-skeleton ix-skeleton--line" />
          <div className="ix-skeleton ix-skeleton--line" />
          <p className="ix-ask-state-text">Asking the grounded assistant…</p>
        </div>
      )}

      {!submitting && isUnauthorized && (
        <div
          className="ix-ask-auth-required"
          data-testid="ask-auth-required"
          role="alert"
        >
          <span aria-hidden="true">{"\u{1F512}"}</span>
          <p>
            Authentication required. A valid operator session is needed to ask the assistant.
          </p>
        </div>
      )}

      {!submitting && !isUnauthorized && error && (
        <div className="ix-ask-error" data-testid="ask-error-banner" role="alert">
          <span aria-hidden="true">{"\u{26A0}"}</span>
          <p>{error}</p>
        </div>
      )}

      {!submitting && !isUnauthorized && !error && response && (
        <div
          className={`ix-ask-result ${response.refused ? "ix-ask-result--refused" : "ix-ask-result--grounded"}`}
          data-testid={response.refused ? "ask-result-refused" : "ask-result-grounded"}
          role="status"
          aria-live="polite"
        >
          <div className="ix-ask-result-header">
            {response.refused ? (
              <span className="ix-badge ix-badge--refused" data-testid="ask-refusal-class">
                Refused: {response.refusal_reason ?? "REFUSED"}
              </span>
            ) : (
              <span className="ix-badge ix-badge--ok" data-testid="ask-grounded-badge">
                Grounded research response
              </span>
            )}
          </div>
          {!response.refused && response.grounding_summary && (
            <p className="ix-ask-summary" data-testid="ask-grounding-summary">
              {response.grounding_summary}
            </p>
          )}
          {response.source_artifact_ids.length > 0 && (
            <div className="ix-ask-sources" data-testid="ask-source-ids">
              <span className="ix-ask-sources-label">Sources: </span>
              {response.source_artifact_ids.map((sourceId) => (
                <span key={sourceId} className="ix-ask-source-id mono">
                  {sourceId}
                </span>
              ))}
            </div>
          )}
          <p className="ix-ask-response-text" data-testid="ask-response-text">
            {response.response_text}
          </p>
          <p className="ix-ask-disclaimer" data-testid="ask-result-disclaimer">
            {response.disclaimer || CONTEXTUAL_ASSISTANT_DISCLAIMER}
          </p>
          <p className="ix-ask-correlation muted mono" data-testid="ask-audit-correlation">
            audit-correlation: {response.audit_correlation_id}
          </p>
        </div>
      )}
    </section>
  );
}

export function ContextualAssistantPanel({
  liveResponses,
  loading: propLoading,
  error: propError,
  isUnauthorized: propUnauthorized,
  autoFetch = false,
  onSelectPrompt,
  defaultCollapsed = false,
}: ContextualAssistantPanelProps) {
  const [isCollapsed, setIsCollapsed] = useState(defaultCollapsed);
  const [selectedPrompt, setSelectedPrompt] = useState<string | null>(null);
  const [prefillPrompt, setPrefillPrompt] = useState<string | null>(null);

  const {
    activeWorkspaceId,
    activeSymbol,
    activeTimeframe,
    selectedArtifactId,
    marketRegime,
  } = useWorkspaceContext();

  const hookState = useAssistantResponses({ autoFetch, limit: 10 });

  const loading = propLoading !== undefined ? propLoading : hookState.loading;
  const error = propError !== undefined ? propError : hookState.error;
  const isUnauthorized =
    propUnauthorized !== undefined ? propUnauthorized : hookState.isUnauthorized;
  const responses = liveResponses !== undefined ? liveResponses : hookState.responses;

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
    // BO-F-01.2: the chips are now clickable shortcuts that pre-fill the ask
    // input (the real ask surface), while the existing onSelectPrompt contract
    // is preserved for hosts that consume it.
    setPrefillPrompt(prompt);
    if (onSelectPrompt) {
      onSelectPrompt(prompt);
    }
  }

  return (
    <section
      className={`ix-contextual-assistant-panel ${isCollapsed ? "ix-panel--collapsed" : ""}`}
      data-ui008-component="contextual-assistant-panel"
      role="region"
      aria-label="Contextual Assistant Panel"
    >
      <header className="ix-contextual-assistant-panel__header">
        <div className="ix-panel-header-left">
          <span className="ix-assistant-icon" aria-hidden="true">{"\u{1F916}"}</span>
          <h3 className="ix-contextual-assistant-title">Contextual Assistant</h3>
        </div>
        <button
          type="button"
          className="ix-collapse-toggle-btn"
          aria-expanded={!isCollapsed}
          aria-label={isCollapsed ? "Expand contextual assistant" : "Collapse contextual assistant"}
          onClick={() => setIsCollapsed((prev) => !prev)}
          data-testid="assistant-collapse-toggle"
        >
          {isCollapsed ? "Expand" : "Collapse"}
        </button>
      </header>

      {!isCollapsed && (
        <div className="ix-contextual-assistant-panel__body">
          <p
            className="ix-contextual-disclaimer"
            data-ui008-disclaimer="contextual-r5-6"
            data-testid="contextual-disclaimer"
          >
            {CONTEXTUAL_ASSISTANT_DISCLAIMER}
          </p>

          {/* Active Context Chips (U-2) */}
          <div
            className="ix-context-chips-row"
            data-testid="active-context-chips"
            aria-label="Active workspace context"
          >
            <span className="ix-context-chip" data-testid="chip-workspace">
              Workspace: <strong>{activeWorkspaceId}</strong>
            </span>
            {activeSymbol && (
              <span className="ix-context-chip" data-testid="chip-symbol">
                Symbol: <strong>{activeSymbol}</strong>
              </span>
            )}
            {activeTimeframe && (
              <span className="ix-context-chip" data-testid="chip-timeframe">
                TF: <strong>{activeTimeframe}</strong>
              </span>
            )}
            {marketRegime && (
              <span className="ix-context-chip" data-testid="chip-regime">
                Regime: <strong>{marketRegime}</strong>
              </span>
            )}
            {selectedArtifactId && (
              <span className="ix-context-chip" data-testid="chip-artifact">
                Artifact: <strong>{selectedArtifactId}</strong>
              </span>
            )}
          </div>

          {/* BO-F-01: the real ask surface (input + grounding + render) */}
          <AssistantAskComposer
            prefillPrompt={prefillPrompt}
            onPrefillConsumed={() => setPrefillPrompt(null)}
          />

          {/* Contextual Prompt Suggestions (U-3) — now pre-fill shortcuts */}
          <div className="ix-prompt-suggestions-section" aria-label="Suggested research prompts">
            <h4 className="ix-suggestions-heading">Suggested Inquiries</h4>
            <div className="ix-prompt-chips-grid" role="group" aria-label="Prompt suggestion chips">
              {promptSuggestions.map((prompt) => (
                <button
                  key={prompt}
                  type="button"
                  className={`ix-prompt-chip ${selectedPrompt === prompt ? "ix-prompt-chip--selected" : ""}`}
                  onClick={() => handlePromptClick(prompt)}
                  data-testid="prompt-suggestion-chip"
                >
                  <span className="ix-chip-prefix">{"\u{203A}"}</span> {prompt}
                </button>
              ))}
            </div>
            {selectedPrompt && (
              <div className="ix-selected-prompt-feedback" data-testid="selected-prompt-feedback">
                <span className="ix-metadata">Active query context: </span>
                <span className="mono">{selectedPrompt}</span>
              </div>
            )}
          </div>

          {/* Loading State */}
          {loading && (
            <div
              className="ix-contextual-loading"
              data-testid="contextual-loading-skeleton"
              data-ui008-state="loading"
              role="status"
              aria-live="polite"
            >
              <div className="ix-skeleton ix-skeleton--line" />
              <div className="ix-skeleton ix-skeleton--line" />
              <p className="ix-loading-text">Loading contextual assistant insights...</p>
            </div>
          )}

          {/* 401 Unauthorized State */}
          {!loading && isUnauthorized && (
            <div
              className="ix-contextual-auth-required"
              data-testid="contextual-auth-required"
              data-ui008-state="unauthorized"
              role="alert"
            >
              <span className="ix-auth-icon" aria-hidden="true">{"\u{1F512}"}</span>
              <p className="ix-auth-text">
                Authentication required. Valid operator session required for assistant guidance.
              </p>
            </div>
          )}

          {/* Error State */}
          {!loading && !isUnauthorized && error && (
            <div
              className="ix-contextual-error"
              data-testid="contextual-error-banner"
              data-ui008-state="error"
              role="alert"
            >
              <span className="ix-error-icon" aria-hidden="true">{"\u{26A0}"}</span>
              <p className="ix-error-text">{error}</p>
            </div>
          )}

          {/* Live Contextual Responses */}
          {!loading && !isUnauthorized && !error && responses.length > 0 && (
            <div className="ix-contextual-responses" data-testid="contextual-responses-list">
              <h4 className="ix-responses-heading">Recent Contextual Responses</h4>
              <ul className="ix-contextual-response-list" role="list">
                {responses.map((resp) => (
                  <li
                    key={resp.assistant_response_id}
                    className={`ix-contextual-response-item ${resp.refused ? "ix-item--refused" : ""}`}
                    data-testid={`contextual-response-${resp.assistant_response_id}`}
                  >
                    <div className="ix-item-header">
                      <span className="ix-item-id mono">{resp.assistant_response_id}</span>
                      {resp.refused ? (
                        <span className="ix-badge ix-badge--refused">
                          REFUSED: {resp.refusal_reason ?? "REFUSED"}
                        </span>
                      ) : (
                        <span className="ix-badge ix-badge--ok">{resp.research_status}</span>
                      )}
                    </div>
                    <p className="ix-item-summary">{resp.grounding_summary}</p>
                    <p className="ix-item-text">{resp.response_text}</p>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Empty State */}
          {!loading && !isUnauthorized && !error && responses.length === 0 && (
            <div
              className="ix-contextual-empty"
              data-testid="contextual-empty-state"
              data-ui008-state="empty"
            >
              <p className="muted">
                No recent assistant responses recorded for this context. Ask a question above or select an inquiry to explore research context.
              </p>
            </div>
          )}
        </div>
      )}
    </section>
  );
}
