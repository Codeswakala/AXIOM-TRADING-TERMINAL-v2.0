import { useEffect, useMemo, useState } from "react";
import {
  createTradePlan,
  fetchTradePlans,
  updateTradePlan,
  type TradePlanNote,
  type TradePlanNoteWrite,
} from "../api/client";
import { EmptyState, ErrorBanner, Skeleton } from "../components/ui";

const EMPTY_FORM: TradePlanNoteWrite = {
  title: "Research plan note",
  market_context: "Market context linked to governed research artifacts.",
  hypothesis: "Research hypothesis for operator review only.",
  linked_signal_ids: [],
  linked_report_ids: [],
  scenario_notes: "Hypothetical scenario notes only.",
  risk_notes: "Research risk notes only; not an instruction.",
  invalidating_conditions_text: "Archive if evidence changes or becomes stale.",
  decision_status: "draft",
};

const TRADE_PLAN_ALLOWED_WRITE_FIELDS = new Set([
  "title",
  "market_context",
  "hypothesis",
  "linked_signal_ids",
  "linked_report_ids",
  "scenario_notes",
  "risk_notes",
  "invalidating_conditions_text",
  "decision_status",
]);

export function assertTradePlanResearchPayload(payload: Record<string, unknown>): TradePlanNoteWrite {
  const unknownFields = Object.keys(payload).filter((key) => !TRADE_PLAN_ALLOWED_WRITE_FIELDS.has(key));
  if (unknownFields.length > 0) {
    throw new Error(`RESEARCH_NOTE_FIELD_NOT_ALLOWED:${unknownFields.join(",")}`);
  }
  return payload as TradePlanNoteWrite;
}

function splitIds(value: string): string[] {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function joinIds(value: string[] | undefined): string {
  return (value ?? []).join(", ");
}

function statusLabel(value: string): string {
  return value.replace(/_/g, " ");
}

function textOrDash(value: string | null | undefined): string {
  return value && value.trim() ? value : "—";
}

type WorkspaceProps = {
  plans: TradePlanNote[];
  loading?: boolean;
  error?: string | null;
  onCreatePlan?: (payload: TradePlanNoteWrite) => Promise<void> | void;
  onUpdatePlan?: (planId: string, payload: TradePlanNoteWrite) => Promise<void> | void;
  onRefresh?: () => void;
};

export function TradePlanningWorkspace({
  plans,
  loading = false,
  error = null,
  onCreatePlan,
  onUpdatePlan,
  onRefresh,
}: WorkspaceProps) {
  const [form, setForm] = useState<TradePlanNoteWrite>(EMPTY_FORM);
  const [linkedSignalText, setLinkedSignalText] = useState("");
  const [linkedReportText, setLinkedReportText] = useState("");
  const [selectedPlanId, setSelectedPlanId] = useState<string | null>(null);
  const selectedPlan = useMemo(
    () => plans.find((plan) => plan.plan_id === selectedPlanId) ?? plans[0] ?? null,
    [plans, selectedPlanId],
  );

  function payloadFromForm(): TradePlanNoteWrite {
    return assertTradePlanResearchPayload({
      ...form,
      linked_signal_ids: splitIds(linkedSignalText),
      linked_report_ids: splitIds(linkedReportText),
    });
  }

  function loadSelectedIntoForm(plan: TradePlanNote) {
    setSelectedPlanId(plan.plan_id);
    setForm({
      title: plan.title,
      market_context: plan.market_context,
      hypothesis: plan.hypothesis,
      linked_signal_ids: plan.linked_signal_ids,
      linked_report_ids: plan.linked_report_ids,
      scenario_notes: plan.scenario_notes,
      risk_notes: plan.risk_notes,
      invalidating_conditions_text: plan.invalidating_conditions_text,
      decision_status: plan.decision_status as TradePlanNoteWrite["decision_status"],
    });
    setLinkedSignalText(joinIds(plan.linked_signal_ids));
    setLinkedReportText(joinIds(plan.linked_report_ids));
  }

  return (
    <>
      <div className="page-header">
        <div>
          <h1>Trade Planning Workspace</h1>
          <p className="muted">
            Operator-authored research notes for reasoning about hypothetical plans. Presentation-only:
            governed artifact links, scenario notes, risk notes, and invalidating conditions. AXIOM
            remains passive; no venue action channel is provided.
          </p>
        </div>
        <button type="button" className="btn primary" onClick={onRefresh}>
          Refresh Plans
        </button>
      </div>

      <section className="advisory-disclaimer" aria-label="Trade planning disclaimer">
        <strong>Research plan note only.</strong> Hypothetical research, not financial advice,
        not a trade instruction. Operator judgment required. AXIOM does not act.
      </section>

      <section
        className="panel span-12 investigation-context-panel"
        aria-label="Trade planning investigation context"
      >
        <h2>Investigation Context</h2>
        <p className="muted">
          Trade planning continuity uses the existing W5 research-note store only. Fields remain
          title, market context, hypothesis, linked signal ids, linked report ids, scenario notes,
          risk notes, invalidating conditions, and review status. Artifact identifiers are shown as
          context pointers only; route links open existing registered research workspaces. Gate CLOSED.
        </p>
        <div className="investigation-evidence-link-list" aria-label="Read-only trade plan context navigation">
          <a className="btn" href="/investigate">Open signal investigation workspace</a>
          <a className="btn" href="/compare-scenarios">Open scenario comparison workspace</a>
          <a className="btn" href="/journal">Open research journal workspace</a>
          <a className="btn" href="/portfolio-research">Open portfolio research workspace</a>
        </div>
      </section>

      {error ? <ErrorBanner title="Trade Planning Error" message={error} /> : null}
      {loading ? <Skeleton variant="rect" height="80px" aria-label="Loading trade plan research notes" /> : null}

      <div className="trade-plan-grid">
        <section className="panel trade-plan-form-panel" aria-label="Create inert trade plan note">
          <h2>Research note editor</h2>
          <div className="trade-plan-form">
            <label className="field">
              <span>Title</span>
              <input
                value={form.title}
                onChange={(event) => setForm({ ...form, title: event.target.value })}
              />
            </label>
            <label className="field">
              <span>Market context</span>
              <textarea
                value={form.market_context}
                onChange={(event) => setForm({ ...form, market_context: event.target.value })}
              />
            </label>
            <label className="field">
              <span>Hypothesis</span>
              <textarea
                value={form.hypothesis}
                onChange={(event) => setForm({ ...form, hypothesis: event.target.value })}
              />
            </label>
            <label className="field">
              <span>Linked signal ids</span>
              <input
                value={linkedSignalText}
                onChange={(event) => setLinkedSignalText(event.target.value)}
                placeholder="signal-1, signal-2"
              />
            </label>
            <label className="field">
              <span>Linked report ids</span>
              <input
                value={linkedReportText}
                onChange={(event) => setLinkedReportText(event.target.value)}
                placeholder="report-1, scenario-1"
              />
            </label>
            <label className="field">
              <span>Scenario notes</span>
              <textarea
                value={form.scenario_notes ?? ""}
                onChange={(event) => setForm({ ...form, scenario_notes: event.target.value })}
              />
            </label>
            <label className="field">
              <span>Risk notes</span>
              <textarea
                value={form.risk_notes ?? ""}
                onChange={(event) => setForm({ ...form, risk_notes: event.target.value })}
              />
            </label>
            <label className="field">
              <span>Invalidating conditions</span>
              <textarea
                value={form.invalidating_conditions_text ?? ""}
                onChange={(event) =>
                  setForm({ ...form, invalidating_conditions_text: event.target.value })
                }
              />
            </label>
            <label className="field">
              <span>Decision status</span>
              <select
                value={form.decision_status}
                onChange={(event) =>
                  setForm({
                    ...form,
                    decision_status: event.target.value as TradePlanNoteWrite["decision_status"],
                  })
                }
              >
                <option value="draft">Draft</option>
                <option value="reviewed">Reviewed</option>
                <option value="archived">Archived</option>
              </select>
            </label>
          </div>
          <div className="trade-plan-actions">
            <button
              type="button"
              className="btn primary"
              onClick={() => void onCreatePlan?.(payloadFromForm())}
            >
              Save research note
            </button>
            {selectedPlan ? (
              <button
                type="button"
                className="btn"
                onClick={() => void onUpdatePlan?.(selectedPlan.plan_id, payloadFromForm())}
              >
                Update selected note
              </button>
            ) : null}
          </div>
        </section>

        <section className="panel trade-plan-list-panel" aria-label="Persisted trade plan notes">
          <h2>Persisted research notes</h2>
          {plans.length === 0 && !loading ? (
            <EmptyState
              title="No Research Notes"
              description="No trade plan research notes have been saved."
              variant="compact"
            />
          ) : null}
          <div className="trade-plan-list">
            {plans.map((plan) => (
              <button
                key={plan.plan_id}
                type="button"
                className={`trade-plan-card${selectedPlan?.plan_id === plan.plan_id ? " active" : ""}`}
                onClick={() => loadSelectedIntoForm(plan)}
              >
                <span className="badge stub">{statusLabel(plan.decision_status)}</span>
                <strong>{plan.title}</strong>
                <small>{plan.research_status}</small>
              </button>
            ))}
          </div>
        </section>

        <section className="panel trade-plan-detail-panel" aria-label="Trade plan research note detail">
          <h2>Research note detail</h2>
          {selectedPlan ? <TradePlanDetail plan={selectedPlan} /> : <p className="muted">Select a note.</p>}
        </section>
      </div>
    </>
  );
}

function TradePlanDetail({ plan }: { plan: TradePlanNote }) {
  return (
    <article className="trade-plan-detail-card">
      <header>
        <span className="badge stub">{statusLabel(plan.decision_status)}</span>
        <h3>{plan.title}</h3>
        <p className="muted">Existing W5 research note. Operator judgment required. AXIOM does not act.</p>
      </header>
      <section>
        <h4>Research status</h4>
        <p>{plan.research_status}</p>
      </section>
      <section>
        <h4>Market context</h4>
        <p>{plan.market_context}</p>
      </section>
      <section>
        <h4>Hypothesis</h4>
        <p>{plan.hypothesis}</p>
      </section>
      <section>
        <h4>Linked research artifacts</h4>
        <dl className="kv compact">
          <dt>Signals</dt>
          <dd className="mono">{plan.linked_signal_ids.join(", ") || "—"}</dd>
          <dt>Reports</dt>
          <dd className="mono">{plan.linked_report_ids.join(", ") || "—"}</dd>
        </dl>
      </section>
      <section>
        <h4>Scenario notes</h4>
        <p>{textOrDash(plan.scenario_notes)}</p>
      </section>
      <section>
        <h4>Risk notes</h4>
        <p>{textOrDash(plan.risk_notes)}</p>
      </section>
      <section>
        <h4>Invalidating conditions</h4>
        <p>{textOrDash(plan.invalidating_conditions_text)}</p>
      </section>
      <section aria-label="Trade plan artifact-id navigation">
        <h4>Investigation links</h4>
        <p className="muted">Links use registered workspace routes; identifiers remain displayed as artifact ids.</p>
        <div className="research-context-link-list">
          <a className="btn" href="/investigate">Review linked signals</a>
          <a className="btn" href="/compare-scenarios">Review scenario context</a>
          <a className="btn" href="/journal">Open reflections</a>
        </div>
      </section>
    </article>
  );
}

export function TradePlanningPage() {
  const [plans, setPlans] = useState<TradePlanNote[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      setPlans(await fetchTradePlans(50));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load trade plan research notes");
    } finally {
      setLoading(false);
    }
  }

  async function createPlan(payload: TradePlanNoteWrite) {
    setError(null);
    try {
      const created = await createTradePlan(payload);
      setPlans((current) => [created, ...current]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save research note");
    }
  }

  async function updatePlan(planId: string, payload: TradePlanNoteWrite) {
    setError(null);
    try {
      const updated = await updateTradePlan(planId, payload);
      setPlans((current) => current.map((plan) => (plan.plan_id === planId ? updated : plan)));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update research note");
    }
  }

  useEffect(() => {
    void load();
  }, []);

  return (
    <TradePlanningWorkspace
      plans={plans}
      loading={loading}
      error={error}
      onCreatePlan={(payload) => void createPlan(payload)}
      onUpdatePlan={(planId, payload) => void updatePlan(planId, payload)}
      onRefresh={() => void load()}
    />
  );
}
