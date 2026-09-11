// N-3: AssistantReviewSubPanel.tsx
// Source: /home/user/axiom/frontend/src/pages/institutional/AssistantReviewSubPanel.tsx
// BO-UI008-P01 §1.1 row 3; skeleton (no live data wiring); A-1/A-2/A-4/A-5/A-6/A-7/A-8 conformant
// Byte budget: ~100 lines; static/typed fixtures only; no fetch/call

const AI_DISCLAIMER_TEXT =
  "AI-generated research assistance only. Not financial advice, not an instruction, may be wrong. Operator judgment required. AXIOM does not act.";

const SELF_DESCRIPTION_BANNER_TEXT =
  "deterministic local assistant; no external LLM; external LLM requires a future gated Build Order";

/**
 * AssistantReviewSubPanel — P01 skeleton (additive; mounts within the UI-006 Institutional
 * Intelligence surface).
 *
 * Disposition:
 * - Renders the AI experience frame, title, self-description banner (TD-078), disclaimer (R5-6).
 * - Empty state: P01 honest-empty (F-16).
 * - Read-only by architecture; no POST/PUT/PATCH/DELETE; no new endpoint.
 * - No new workspace-registry entry (BO §3.6); this is a sub-panel within the existing surface.
 * - The component is mounted additively within the existing UI-006 surface
 *   (the M-3 additive diff to InstitutionalIntelligencePage.tsx).
 * - At P01 the sub-panel renders the frame + banner + disclaimer + empty state;
 *   the carried-open register and refusal taxonomy are rendered at this sub-panel
 *   for surface coverage (BO §3.9 + §3.2 conformance; the disclosure and refusal
 *   surfaces are also rendered at the command surface and audit sub-section for
 *   cross-surface coverage; all three are read-only).
 */
export function AssistantReviewSubPanel() {
  return (
    <section
      className="ix-assistant-review-sub-panel"
      data-ui008-component="assistant-review-sub-panel"
      role="region"
      aria-label="Assistant Review Sub-Panel (P01 skeleton; mounts within UI-006 surface)"
    >
      <header className="ix-assistant-review-sub-panel__header">
        <h3 className="ix-assistant-review-sub-panel__title">
          Assistant Review Sub-Panel (P01 skeleton)
        </h3>
        <p className="ix-assistant-review-sub-panel__banner" data-ui008-banner="td-078-self-description" data-testid="td-078-self-description">
          {SELF_DESCRIPTION_BANNER_TEXT}
        </p>
        <p className="ix-assistant-review-sub-panel__disclaimer" data-ui008-disclaimer="r5-6" data-testid="r5-6">
          {AI_DISCLAIMER_TEXT}
        </p>
      </header>

      <div className="ix-assistant-review-sub-panel__body" data-ui008-p01-skeleton-empty="true">
        <p className="ix-assistant-review-sub-panel__empty" data-ui008-empty-state="p01-skeleton" data-testid="p01-skeleton">
          <span data-ui008-icon="empty" aria-hidden="true">{"\u{1F50D}"}</span>
          {" "}Assistant review sub-panel skeleton. Institutional-intelligence integration deferred to P03+.
        </p>
      </div>
    </section>
  );
}
