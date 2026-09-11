// N-2: AssistantAuditSubSection.tsx
// Source: /home/user/axiom/frontend/src/workstation/governance/AssistantAuditSubSection.tsx
// UI-008-P02: Connected to live read-only refusal audit events API seam.
// Non-actuating / read-only: Zero order or execution controls.

import { ASSISTANT_REFUSAL_REASON_CODES } from "../../test/ui008_refusal_taxonomy.fixture";
import { ASSISTANT_DISCLOSURE_REGISTER } from "../../test/ui008_disclosure_register.fixture";
import {
  type AssistantAuditEvent,
  useAssistantAudit,
} from "../../api/assistantClient";

/**
 * Pinned identifiers of record (BO §3.4, §3.5, §3.7; R5-6; R-7 REQUIRED; TD-078 banner).
 */
export const AI_DISCLAIMER_TEXT =
  "AI-generated research assistance only. Not financial advice, not an instruction, may be wrong. Operator judgment required. AXIOM does not act.";

export const SELF_DESCRIPTION_BANNER_TEXT =
  "deterministic local assistant; no external LLM; external LLM requires a future gated Build Order";

export interface AssistantAuditSubSectionProps {
  /** If provided, overrides internal hook state for testing */
  liveAuditEvents?: AssistantAuditEvent[];
  loading?: boolean;
  error?: string | null;
  isUnauthorized?: boolean;
  /** Whether to automatically fetch live data (default: false for P01 test backward-compat) */
  autoFetch?: boolean;
}

/**
 * AssistantAuditSubSection — UI-008-P02 (additive; mounts within the UI-007-P03 audit surface).
 *
 * Disposition:
 * - Renders the AI experience frame, title, self-description banner (TD-078), disclaimer (R5-6).
 * - Renders the carried-open register at full severity (BO §3.9; 18 items per D-2.6(i)).
 * - Renders the six-code refusal taxonomy (BO §3.2).
 * - P02 Live Seam: Displays loading skeleton, error banner, 401 auth notice, empty state, or live refusal audit records.
 * - Read-only by architecture; no POST/PUT/PATCH/DELETE; no new endpoint.
 */
export function AssistantAuditSubSection({
  liveAuditEvents,
  loading: propLoading,
  error: propError,
  isUnauthorized: propUnauthorized,
  autoFetch = false,
}: AssistantAuditSubSectionProps = {}) {
  const hookState = useAssistantAudit({ autoFetch, category: "SECURITY" });

  const loading = propLoading !== undefined ? propLoading : hookState.loading;
  const error = propError !== undefined ? propError : hookState.error;
  const isUnauthorized =
    propUnauthorized !== undefined ? propUnauthorized : hookState.isUnauthorized;
  const auditEvents =
    liveAuditEvents !== undefined ? liveAuditEvents : hookState.auditEvents;

  const isSkeletonEmpty =
    !loading && !error && !isUnauthorized && auditEvents.length === 0;

  return (
    <section
      className="ix-assistant-audit-sub-section"
      data-ui008-component="assistant-audit-sub-section"
      role="region"
      data-ui008-p01-skeleton-empty={isSkeletonEmpty ? "true" : undefined}
      aria-label="Assistant Audit Sub-Section (P01 skeleton; mounts within UI-007 audit surface)"
    >
      <header className="ix-assistant-audit-sub-section__header">
        <h3 className="ix-assistant-audit-sub-section__title">
          Assistant Audit Sub-Section
        </h3>
        <p
          className="ix-assistant-audit-sub-section__banner"
          data-ui008-banner="td-078-self-description"
          data-testid="td-078-self-description"
        >
          {SELF_DESCRIPTION_BANNER_TEXT}
        </p>
        <p
          className="ix-assistant-audit-sub-section__disclaimer"
          data-ui008-disclaimer="r5-6"
          data-testid="r5-6"
        >
          {AI_DISCLAIMER_TEXT}
        </p>
      </header>

      <div
        className="ix-assistant-audit-sub-section__body"
        data-ui008-p01-skeleton-empty={isSkeletonEmpty ? "true" : undefined}
      >
        {/* Loading State */}
        {loading && (
          <div
            className="ix-assistant-audit-sub-section__loading"
            data-testid="audit-loading-skeleton"
            data-ui008-state="loading"
            role="status"
            aria-live="polite"
          >
            <div className="ix-skeleton ix-skeleton--line" />
            <div className="ix-skeleton ix-skeleton--line" />
            <p className="ix-audit-loading-text">Loading refusal audit records...</p>
          </div>
        )}

        {/* 401 Unauthorized State */}
        {!loading && isUnauthorized && (
          <div
            className="ix-assistant-audit-sub-section__auth-required"
            data-testid="audit-auth-required"
            data-ui008-state="unauthorized"
            role="alert"
          >
            <span className="ix-auth-icon" aria-hidden="true">{"\u{1F512}"}</span>
            <p className="ix-auth-message">
              Authentication required. Valid operator session required to access audit records.
            </p>
          </div>
        )}

        {/* Error State */}
        {!loading && !isUnauthorized && error && (
          <div
            className="ix-assistant-audit-sub-section__error"
            data-testid="audit-error-banner"
            data-ui008-state="error"
            role="alert"
          >
            <span className="ix-error-icon" aria-hidden="true">{"\u{26A0}"}</span>
            <p className="ix-error-message">{error}</p>
          </div>
        )}

        {/* Live Audit Events List */}
        {!loading && !isUnauthorized && !error && auditEvents.length > 0 && (
          <div
            className="ix-assistant-audit-sub-section__events"
            data-testid="assistant-audit-list"
            data-ui008-state="ready"
          >
            <h4 className="ix-assistant-audit-heading">Recorded Refusal Audit Events</h4>
            <ul className="ix-assistant-audit-list" role="list">
              {auditEvents.map((evt) => (
                <li
                  key={evt.id}
                  className="ix-assistant-audit-item"
                  data-ui008-audit-row={evt.id}
                  data-testid={`audit-row-${evt.id}`}
                >
                  <div className="ix-audit-row-header">
                    <span className="ix-audit-id">{evt.id}</span>
                    <span className="ix-audit-timestamp">{evt.created_at}</span>
                    <span className="ix-audit-action-badge">{evt.action}</span>
                  </div>
                  <p className="ix-audit-message">{evt.message}</p>
                  <div className="ix-audit-meta">
                    <span className="ix-audit-actor">Actor: {evt.actor}</span>
                    {evt.resource_type && (
                      <span className="ix-audit-resource">
                        Resource: {evt.resource_type} ({evt.resource_id ?? "none"})
                      </span>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Empty State / P01 Skeleton fallback */}
        {isSkeletonEmpty && (
          <p
            className="ix-assistant-audit-sub-section__empty"
            data-ui008-empty-state="p01-skeleton"
            data-testid="p01-skeleton"
          >
            <span data-ui008-icon="empty" aria-hidden="true">{"\u{1F4CB}"}</span>
            {" "}Assistant audit sub-section skeleton. Audit-event integration (read-only) deferred to P02+.
          </p>
        )}
      </div>

      <footer className="ix-assistant-audit-sub-section__footer">
        <h4 className="ix-assistant-audit-sub-section__disclosure-title">
          Carried-Open Register (BO §3.9; verbatim)
        </h4>
        <ul
          className="ix-assistant-audit-disclosure"
          data-ui008-component="disclosure-register"
          role="list"
          aria-label="Carried-Open Register (verbatim, full severity)"
        >
          {ASSISTANT_DISCLOSURE_REGISTER.map((entry) => (
            <li
              key={entry.id}
              className={`ix-assistant-audit-disclosure__row ix-severity-${entry.severityClass}`}
              data-ui008-disclosure-row={entry.id}
            >
              <span className="ix-assistant-audit-disclosure__icon" data-ui008-icon aria-hidden="true">
                {entry.icon}
              </span>
              <span className="ix-assistant-audit-disclosure__id">{entry.id}</span>
              <span className="ix-assistant-audit-disclosure__severity" data-ui008-severity>
                {entry.severityLabel}
              </span>
              <span className="ix-assistant-audit-disclosure__text" data-ui008-disclosure-text>
                {entry.text}
              </span>
              <span className="ix-assistant-audit-disclosure__source-pin" data-ui008-source-pin>
                (source: {entry.sourcePin})
              </span>
            </li>
          ))}
        </ul>

        <h4 className="ix-assistant-audit-sub-section__refusal-title">
          Refusal Taxonomy (BO §3.2; six codes; test 27)
        </h4>
        <ul
          className="ix-assistant-audit-refusal"
          data-ui008-component="refusal-surface"
          role="list"
          aria-label="Refusal Taxonomy (six codes, BO §3.2)"
        >
          {ASSISTANT_REFUSAL_REASON_CODES.map((code) => (
            <li key={code} data-ui008-refusal-code={code} data-testid={code}>
              <span className="ix-assistant-audit-refusal__code">{code}</span>
            </li>
          ))}
        </ul>
      </footer>
    </section>
  );
}
