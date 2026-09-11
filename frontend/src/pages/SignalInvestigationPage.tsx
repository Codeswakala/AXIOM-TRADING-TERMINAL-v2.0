import { useEffect, useMemo, useState } from "react";
import {
  fetchAdvisorySignals,
  fetchInstitutionalIntelligenceBundle,
  type AdvisorySignal,
  type InstitutionalIntelligenceBundle,
  type InstitutionalReport,
} from "../api/client";
import { ContextualAssistantPanel } from "../workstation/ai/ContextualAssistantPanel";
import { Panel, PanelHeader, EmptyState, ErrorBanner, Skeleton } from "../components/ui";

const INVESTIGATION_DISCLAIMER =
  "Signal investigation is research review only — not financial advice, not a trade instruction, not a signal mutation, and not an action surface. Operator judgment required. AXIOM does not act.";

type WorkspaceProps = {
  signals: AdvisorySignal[];
  intelligence: InstitutionalIntelligenceBundle;
  selectedSignalId?: string | null;
  loading?: boolean;
  error?: string | null;
  onSelectSignal?: (signalId: string) => void;
  onRefresh?: () => void;
};

const EMPTY_INTELLIGENCE: InstitutionalIntelligenceBundle = {
  relation: [],
  context: [],
  hypothetical: [],
  risk: [],
  validation: [],
};

const REPORT_GROUPS: Array<[keyof InstitutionalIntelligenceBundle, string]> = [
  ["relation", "Cross-market relation reports"],
  ["context", "Market context reports"],
  ["hypothetical", "Hypothetical research reports"],
  ["risk", "Market-series risk reports"],
  ["validation", "Advisory quality reports"],
];

export type InvestigationPlanningDataSource = {
  surface: string;
  existingRoute: string;
  existingStore: string;
  existingReadSeam: string;
  p01Posture: string;
};

export const UI005_INVESTIGATION_PLANNING_SOURCES: InvestigationPlanningDataSource[] = [
  {
    surface: "Signal Investigation",
    existingRoute: "/investigate",
    existingStore: "W3 advisory signal records and linked report ids",
    existingReadSeam: "fetchAdvisorySignals + fetchInstitutionalIntelligenceBundle",
    p01Posture: "Read-only rationale, guardrails, lineage, and related reports",
  },
  {
    surface: "Scenario Comparison",
    existingRoute: "/compare-scenarios",
    existingStore: "W4 stored hypothetical scenario reports",
    existingReadSeam: "fetchScenarioReports / fetchScenarioReport",
    p01Posture: "Existing hypothetical comparisons with assumptions and limitations",
  },
  {
    surface: "Trade Planning",
    existingRoute: "/trade-plans",
    existingStore: "W5 trade plan research notes",
    existingReadSeam: "existing trade plan read path",
    p01Posture: "Research-note planning context only; mutation scope unchanged",
  },
  {
    surface: "Execution Research",
    existingRoute: "/execution-research",
    existingStore: "W6 SIMULATED execution research artifacts",
    existingReadSeam: "fetchExecutionResearchBundle",
    p01Posture: "SIMULATED display-only evidence with assumptions and limitations",
  },
  {
    surface: "Research Journal",
    existingRoute: "/journal",
    existingStore: "W5 manual research journal entries",
    existingReadSeam: "fetchJournalEntries",
    p01Posture: "Research documentation links and reflections",
  },
  {
    surface: "Portfolio Research",
    existingRoute: "/portfolio-research",
    existingStore: "W7 hypothetical portfolio research dashboard/report preview",
    existingReadSeam: "fetchPortfolioResearchDashboard + fetchAdvancedResearchReport",
    p01Posture: "Hypothetical review context; no real portfolio state",
  },
];

function InvestigationPlanningFrame() {
  return (
    <Panel
      className="span-12 investigation-planning-frame"
      aria-label="Investigation and planning workspace frame"
      header={
        <PanelHeader
          title="Investigation & Planning Workspace"
          subtitle="A workflow frame over existing investigation, comparison, planning, journal, simulated research, and portfolio-research surfaces. This frame maps sources first and adds no new route, no persisted view state, and no browser-authored analytical result."
          headingLevel={2}
          actions={
            <div className="research-guardrail-card" role="note" aria-label="Investigation planning guardrail">
              <strong>Gate CLOSED</strong>
              <span>Research-only · Existing routes · SIMULATED evidence only</span>
            </div>
          }
        />
      }
    >
      <div className="investigation-source-grid" aria-label="UI-005 governed data-source inventory">
        {UI005_INVESTIGATION_PLANNING_SOURCES.map((item) => (
          <article className="investigation-source-card" key={item.surface}>
            <span className="ix-metadata">{item.surface}</span>
            <strong className="mono">{item.existingRoute}</strong>
            <dl className="kv compact">
              <dt>Existing store</dt>
              <dd>{item.existingStore}</dd>
              <dt>Read seam</dt>
              <dd className="mono">{item.existingReadSeam}</dd>
              <dt>P01 posture</dt>
              <dd>{item.p01Posture}</dd>
            </dl>
          </article>
        ))}
      </div>
    </Panel>
  );
}

function formatDate(value: string | null): string {
  if (!value) return "—";
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return value;
  return parsed.toISOString();
}

function formatConfidence(value: number | null): string {
  if (value == null) return "Unavailable";
  return `${(value * 100).toFixed(1)}% calibrated confidence`;
}

function reportTitle(report: InstitutionalReport): string {
  const type = typeof report.artifact_type === "string" ? report.artifact_type : "research_report";
  return `${type.replace(/_/g, " ")} · ${report.id}`;
}

function reportSummary(report: InstitutionalReport): string {
  const status = typeof report.research_status === "string" ? report.research_status : "research_only";
  const samples = typeof report.sample_count === "number" ? `n=${report.sample_count}` : "n=—";
  return `${status} · ${samples}`;
}

function safeSummaryValue(value: unknown): string {
  if (typeof value === "string") return value;
  if (typeof value === "number" || typeof value === "boolean") return String(value);
  if (value == null) return "—";
  return "present";
}

export function SignalInvestigationWorkspace({
  signals,
  intelligence,
  selectedSignalId = null,
  loading = false,
  error = null,
  onSelectSignal,
  onRefresh,
}: WorkspaceProps) {
  const selected = useMemo(
    () => signals.find((signal) => signal.signal_id === selectedSignalId) ?? signals[0] ?? null,
    [signals, selectedSignalId],
  );

  return (
    <>
      <div className="page-header">
        <div>
          <h1>Signal Investigation Workspace</h1>
          <p className="muted">
            Read-only investigation of persisted advisory signal rationale, guardrails, lineage,
            and linked intelligence reports. Presentation-only: no client-side inference, no
            guardrail override, no signal mutation, and no browser-side analytics rerun.
          </p>
        </div>
        <button type="button" className="btn primary" onClick={onRefresh}>
          Refresh Investigation
        </button>
      </div>

      <section className="advisory-disclaimer" aria-label="Signal investigation disclaimer">
        <strong>Research investigation only.</strong> {INVESTIGATION_DISCLAIMER}
      </section>

      {error ? <ErrorBanner title="Signal Investigation Error" message={error} /> : null}
      {loading ? <Skeleton variant="rect" height="80px" aria-label="Loading signal investigation context" /> : null}

      <InvestigationPlanningFrame />

      <div className="signal-investigation-grid">
        <section className="panel signal-list-panel" aria-label="Investigation signal selector">
          <h2>Persisted signals</h2>
          {signals.length === 0 && !loading ? (
            <EmptyState
              title="No Persisted Signals"
              description="No persisted advisory signals returned by the read-only API."
              variant="compact"
            />
          ) : null}
          <div className="signal-card-list">
            {signals.map((signal) => (
              <button
                key={signal.signal_id}
                type="button"
                className={`signal-card signal-${signal.signal_state}${
                  selected?.signal_id === signal.signal_id ? " active" : ""
                }`}
                onClick={() => onSelectSignal?.(signal.signal_id)}
              >
                <span className={`signal-state-badge signal-${signal.signal_state}`}>
                  {signal.signal_state}
                </span>
                <span className="signal-card-title">
                  {signal.symbol} · {signal.timeframe} · {signal.signal_direction}
                </span>
                <span className="signal-card-meta">{formatDate(signal.as_of_time)}</span>
                <span className="signal-card-meta">{signal.state_reason}</span>
              </button>
            ))}
          </div>
        </section>

        <section className="panel signal-investigation-detail" aria-label="Signal investigation detail">
          <h2>Investigation Detail</h2>
          {selected ? (
            <InvestigationDetail signal={selected} intelligence={intelligence} />
          ) : (
            <p className="muted">Select a signal to investigate.</p>
          )}
        </section>
      </div>
    </>
  );
}

function InvestigationDetail({
  signal,
  intelligence,
}: {
  signal: AdvisorySignal;
  intelligence: InstitutionalIntelligenceBundle;
}) {
  return (
    <article className="signal-investigation-card">
      <header className="signal-detail-head">
        <div>
          <span className={`signal-state-badge signal-${signal.signal_state}`}>
            {signal.signal_state}
          </span>
          <h3>
            {signal.symbol} · {signal.timeframe} · {signal.signal_direction}
          </h3>
          <p className="muted">
            Investigation reads persisted evidence only. It does not change this signal, rerun the
            model, alter guardrails, or create an instruction.
          </p>
        </div>
        <div className="confidence-box" aria-label="Calibrated confidence">
          <span>Calibrated confidence</span>
          <strong>{formatConfidence(signal.calibrated_confidence)}</strong>
          <small>{signal.calibration_status}</small>
        </div>
      </header>

      <section className="signal-section">
        <h4>Rationale</h4>
        <p>{signal.rationale}</p>
      </section>

      <div className="signal-detail-grid">
        <section className="signal-section">
          <h4>Guardrail states</h4>
          <dl className="kv compact">
            <dt>State reason</dt>
            <dd>{signal.state_reason}</dd>
            <dt>Operating domain</dt>
            <dd>{signal.operating_domain_status}</dd>
            <dt>Calibration</dt>
            <dd>{signal.calibration_status}</dd>
            <dt>Economic verdict</dt>
            <dd>{signal.economic_verdict}</dd>
            <dt>Freshness</dt>
            <dd>{signal.freshness_status ?? "—"}</dd>
            <dt>Expiry</dt>
            <dd>{formatDate(signal.expires_at)}</dd>
          </dl>
        </section>

        <section className="signal-section">
          <h4>Lineage</h4>
          <dl className="kv compact">
            <dt>Signal id</dt>
            <dd className="mono">{signal.signal_id}</dd>
            <dt>Model</dt>
            <dd className="mono">{signal.model_artifact_id}</dd>
            <dt>Model version</dt>
            <dd className="mono">{signal.model_version}</dd>
            <dt>Experiment</dt>
            <dd className="mono">{signal.experiment_id}</dd>
            <dt>Feature set</dt>
            <dd className="mono">{signal.feature_set_version}</dd>
            <dt>Input hash</dt>
            <dd className="mono">{signal.inference_input_hash}</dd>
          </dl>
        </section>
      </div>

      <section className="signal-section">
        <h4>Linked validation and report ids</h4>
        <div className="linked-report-id-grid">
          <span>Statistical: <code>{signal.statistical_report_id ?? "—"}</code></span>
          <span>Calibration: <code>{signal.calibration_report_id ?? "—"}</code></span>
          <span>Economic: <code>{signal.economic_report_id ?? "—"}</code></span>
          <span>Generalization: <code>{signal.generalization_report_id ?? "—"}</code></span>
        </div>
      </section>

      <section className="signal-section" aria-label="Related investigation evidence links">
        <h4>Related evidence links</h4>
        <p className="muted">
          Navigation only. Links open existing research workspaces that disclose stored reports,
          signal context, and chart context without changing this investigation.
        </p>
        <div className="investigation-evidence-link-list">
          <a className="btn" href="/intelligence">Open intelligence report viewer</a>
          <a className="btn" href="/signals">Open advisory signal record</a>
          <a className="btn" href="/charts">Open chart context</a>
        </div>
      </section>

      <section className="signal-section" aria-label="Safe explainability summary">
        <h4>Safe explainability summary</h4>
        <dl className="kv compact">
          <dt>Confidence source</dt>
          <dd>{safeSummaryValue(signal.explainability_summary.confidence_source)}</dd>
          <dt>Freshness status</dt>
          <dd>{signal.freshness_status ?? "—"}</dd>
          <dt>Eligibility reasons</dt>
          <dd>{signal.eligibility_reasons.length ? signal.eligibility_reasons.join(", ") : "—"}</dd>
        </dl>
      </section>

      <section className="signal-section" aria-label="Linked intelligence reports">
        <h4>Linked intelligence reports</h4>
        <div className="investigation-report-grid">
          {REPORT_GROUPS.map(([key, label]) => (
            <div key={key} className="investigation-report-group">
              <strong>{label}</strong>
              {intelligence[key].length === 0 ? <span className="muted">No reports returned.</span> : null}
              {intelligence[key].slice(0, 2).map((report) => (
                <article key={`${key}-${report.id}`} className="investigation-report-card">
                  <span>{reportTitle(report)}</span>
                  <small>{reportSummary(report)}</small>
                </article>
              ))}
            </div>
          ))}
        </div>
      </section>
    </article>
  );
}

export function SignalInvestigationPage() {
  const [signals, setSignals] = useState<AdvisorySignal[]>([]);
  const [intelligence, setIntelligence] = useState<InstitutionalIntelligenceBundle>(EMPTY_INTELLIGENCE);
  const [selectedSignalId, setSelectedSignalId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      const [signalRows, intelligenceRows] = await Promise.all([
        fetchAdvisorySignals({ limit: 100 }),
        fetchInstitutionalIntelligenceBundle(5),
      ]);
      setSignals(signalRows);
      setIntelligence(intelligenceRows);
      setSelectedSignalId((current) =>
        current && signalRows.some((signal) => signal.signal_id === current)
          ? current
          : signalRows[0]?.signal_id ?? null,
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load signal investigation context");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void load();
  }, []);

  return (
    <>
      <SignalInvestigationWorkspace
        signals={signals}
        intelligence={intelligence}
        selectedSignalId={selectedSignalId}
        loading={loading}
        error={error}
        onSelectSignal={setSelectedSignalId}
        onRefresh={() => void load()}
      />
      <section data-ui008-mount="contextual-assistant-panel" aria-label="Contextual Assistant mount point">
        <ContextualAssistantPanel />
      </section>
    </>
  );
}
