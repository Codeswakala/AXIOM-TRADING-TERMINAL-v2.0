import { useEffect, useMemo, useState } from "react";
import {
  fetchExecutionResearchBundle,
  type ExecutionResearchBundle,
  type ExecutionResearchExperiment,
  type ExecutionRiskResearchReport,
  type SimulatedExecutionAnalyticsReport,
  type SimulatedExecutionRun,
  type SimulatedFillEvent,
  type SimulatedPaperLedgerEntry,
} from "../api/client";

export const EXECUTION_RESEARCH_DISCLAIMER =
  "SIMULATED execution research only. Display-only evidence, not financial advice. AXIOM does not act. Governance Gate CLOSED.";

const EMPTY_BUNDLE: ExecutionResearchBundle = {
  runs: [],
  fills: [],
  ledger: [],
  riskReports: [],
  experiments: [],
  analyticsReports: [],
};

type WorkspaceProps = {
  bundle: ExecutionResearchBundle;
  loading?: boolean;
  error?: string | null;
  onRefresh?: () => void;
};

function fmt(value: unknown): string {
  if (typeof value === "number") return Number.isInteger(value) ? String(value) : value.toFixed(6);
  if (typeof value === "string" && value.trim()) return value;
  if (typeof value === "boolean") return String(value);
  if (Array.isArray(value)) return `${value.length} items`;
  if (value && typeof value === "object") return "present";
  return "—";
}

function pct(value: number | undefined): string {
  return typeof value === "number" ? `${(value * 100).toFixed(2)}%` : "—";
}

function firstMetricValue(metrics: Record<string, unknown>, key: string): string {
  const metric = metrics[key];
  if (!metric || typeof metric !== "object") return "—";
  return fmt((metric as Record<string, unknown>).value);
}

function uncertaintySummary(value: Record<string, unknown>): string {
  const method = fmt(value.method);
  const sample = fmt(value.sample_count);
  const metrics = value.metrics;
  if (metrics && typeof metrics === "object") {
    return `${method} · n=${sample} · per-metric uncertainty present`;
  }
  return `${method} · n=${sample}`;
}

function compactRecordEntries(value: Record<string, unknown>, limit = 4): Array<[string, string]> {
  return Object.entries(value)
    .slice(0, limit)
    .map(([key, item]) => [key, fmt(item)]);
}

function joinedIds(value: string[] | undefined): string {
  return value && value.length ? value.join(", ") : "—";
}

function LimitationsList({ items }: { items: string[] }) {
  return items.length ? (
    <ul className="scenario-limitations">
      {items.map((item) => (
        <li key={item}>{item}</li>
      ))}
    </ul>
  ) : (
    <p className="muted">No limitations supplied by the stored artifact.</p>
  );
}

function CompactRecord({ value }: { value: Record<string, unknown> }) {
  const entries = compactRecordEntries(value);
  if (entries.length === 0) return <span>—</span>;
  return (
    <dl className="kv compact">
      {entries.map(([key, item]) => (
        <div key={key} className="kv-row">
          <dt>{key}</dt>
          <dd>{item}</dd>
        </div>
      ))}
    </dl>
  );
}

export function ExecutionResearchWorkspace({
  bundle,
  loading = false,
  error = null,
  onRefresh,
}: WorkspaceProps) {
  const counts = useMemo(
    () => [
      ["Runs", bundle.runs.length],
      ["Fills", bundle.fills.length],
      ["Ledger", bundle.ledger.length],
      ["Risk reports", bundle.riskReports.length],
      ["Experiments", bundle.experiments.length],
      ["Analytics", bundle.analyticsReports.length],
    ],
    [bundle],
  );

  return (
    <>
      <div className="page-header">
        <div>
          <h1>Execution Research Workspace</h1>
          <p className="muted">
            Display-only workspace for server-persisted SIMULATED execution research artifacts.
            Metrics are read from audited backend records; the browser performs no authoritative
            analytics rerun.
          </p>
        </div>
        <button type="button" className="btn primary" onClick={onRefresh}>
          Refresh Research
        </button>
      </div>

      <section className="advisory-disclaimer" aria-label="Execution research disclaimer">
        <strong>SIMULATED.</strong> {EXECUTION_RESEARCH_DISCLAIMER}
      </section>

      <section
        className="panel span-12 investigation-context-panel"
        aria-label="Execution research investigation context"
      >
        <h2>Investigation Context</h2>
        <p className="muted">
          Execution Research contributes SIMULATED evidence to investigation and planning. It reads
          existing W6 artifacts through fetchExecutionResearchBundle, preserves assumptions,
          uncertainty, limitations, source ids, hashes, and policy details, and links only to
          existing registered workspaces. Gate CLOSED.
        </p>
        <div className="investigation-evidence-link-list" aria-label="Read-only execution research context navigation">
          <a className="btn" href="/investigate">Open signal investigation workspace</a>
          <a className="btn" href="/trade-plans">Open trade planning workspace</a>
          <a className="btn" href="/journal">Open research journal workspace</a>
          <a className="btn" href="/compare-scenarios">Open scenario comparison workspace</a>
          <a className="btn" href="/portfolio-research">Open portfolio research workspace</a>
        </div>
      </section>

      {error ? <p className="error-text">{error}</p> : null}
      {loading ? <p className="muted">Loading SIMULATED execution research artifacts…</p> : null}

      <section className="panel span-12" aria-label="Execution research artifact counts">
        <h2>Persisted SIMULATED artifacts</h2>
        <div className="metric-card-grid">
          {counts.map(([label, count]) => (
            <article key={label} className="metric-card">
              <h3>{label}</h3>
              <strong>{count}</strong>
              <p className="muted">Server-persisted SIMULATED research records.</p>
            </article>
          ))}
        </div>
      </section>

      <div className="execution-research-grid">
        <section className="panel" aria-label="Simulated execution runs">
          <h2>Simulated Runs</h2>
          {bundle.runs.length === 0 ? <p className="muted">No simulated runs returned.</p> : null}
          {bundle.runs.slice(0, 3).map((run) => (
            <RunCard key={run.run_id} run={run} />
          ))}
        </section>

        <section className="panel" aria-label="Simulated fill events">
          <h2>Simulated Fills</h2>
          {bundle.fills.length === 0 ? <p className="muted">No simulated fills returned.</p> : null}
          {bundle.fills.slice(0, 4).map((fill) => (
            <FillCard key={fill.simulated_fill_id} fill={fill} />
          ))}
        </section>

        <section className="panel" aria-label="Simulated paper ledger">
          <h2>Paper Research Ledger</h2>
          {bundle.ledger.length === 0 ? <p className="muted">No simulated ledger rows returned.</p> : null}
          {bundle.ledger.slice(0, 3).map((entry) => (
            <LedgerCard key={entry.ledger_entry_id} entry={entry} />
          ))}
        </section>

        <section className="panel" aria-label="Execution risk reports">
          <h2>Risk Research Reports</h2>
          {bundle.riskReports.length === 0 ? <p className="muted">No risk reports returned.</p> : null}
          {bundle.riskReports.slice(0, 3).map((report) => (
            <RiskReportCard key={report.report_id} report={report} />
          ))}
        </section>

        <section className="panel" aria-label="Execution experiments">
          <h2>Replay Experiments</h2>
          {bundle.experiments.length === 0 ? <p className="muted">No replay experiments returned.</p> : null}
          {bundle.experiments.slice(0, 3).map((experiment) => (
            <ExperimentCard key={experiment.experiment_id} experiment={experiment} />
          ))}
        </section>

        <section className="panel" aria-label="Simulated analytics reports">
          <h2>Analytics & Comparison</h2>
          {bundle.analyticsReports.length === 0 ? <p className="muted">No analytics reports returned.</p> : null}
          {bundle.analyticsReports.slice(0, 3).map((report) => (
            <AnalyticsCard key={report.report_id} report={report} />
          ))}
        </section>
      </div>
    </>
  );
}

function SimBadge({ value }: { value: string }) {
  return <span className="badge up">{value}</span>;
}

function RunCard({ run }: { run: SimulatedExecutionRun }) {
  return (
    <article className="execution-research-card" aria-label={`Simulated run ${run.run_id}`}>
      <SimBadge value={run.simulation_mode} />
      <h3>{run.run_id}</h3>
      <dl className="kv compact">
        <dt>Policy</dt>
        <dd>{run.simulation_policy_version}</dd>
        <dt>Fill model</dt>
        <dd>{run.fill_model_version}</dd>
        <dt>Status</dt>
        <dd>{run.research_status}</dd>
        <dt>Source artifacts</dt>
        <dd className="mono">{joinedIds(run.input_artifact_ids)}</dd>
      </dl>
      <section>
        <h4>Replay scope</h4>
        <CompactRecord value={run.replay_scope} />
      </section>
      <section>
        <h4>Assumptions</h4>
        <CompactRecord value={run.assumptions} />
      </section>
      <section>
        <h4>Limitations</h4>
        <LimitationsList items={run.limitations} />
      </section>
    </article>
  );
}

function FillCard({ fill }: { fill: SimulatedFillEvent }) {
  return (
    <article className="execution-research-card" aria-label={`Simulated fill ${fill.simulated_fill_id}`}>
      <SimBadge value={fill.simulation_mode} />
      <h3>{fill.symbol} · {fill.timeframe}</h3>
      <dl className="kv compact">
        <dt>Simulated units</dt>
        <dd>{fmt(fill.simulated_units)}</dd>
        <dt>Reference price</dt>
        <dd>{fmt(fill.requested_reference_price)}</dd>
        <dt>Model output price</dt>
        <dd>{fmt(fill.simulated_fill_price)}</dd>
        <dt>Slippage bps</dt>
        <dd>{fmt(fill.simulated_slippage_bps)}</dd>
        <dt>Source candles</dt>
        <dd className="mono">{joinedIds(fill.source_candle_ids)}</dd>
        <dt>Status</dt>
        <dd>{fill.research_status}</dd>
      </dl>
    </article>
  );
}

function LedgerCard({ entry }: { entry: SimulatedPaperLedgerEntry }) {
  return (
    <article className="execution-research-card" aria-label={`Simulated ledger ${entry.ledger_entry_id}`}>
      <SimBadge value={entry.simulation_mode} />
      <h3>{entry.ledger_event_type}</h3>
      <dl className="kv compact">
        <dt>Run id</dt>
        <dd className="mono">{entry.run_id}</dd>
        <dt>Fill id</dt>
        <dd className="mono">{entry.simulated_fill_id}</dd>
        <dt>Return estimate</dt>
        <dd>{pct(entry.simulated_return_estimate)}</dd>
        <dt>Uncertainty</dt>
        <dd>{uncertaintySummary(entry.uncertainty)}</dd>
        <dt>Status</dt>
        <dd>{entry.research_status}</dd>
      </dl>
      <section>
        <h4>Limitations</h4>
        <LimitationsList items={entry.limitations} />
      </section>
    </article>
  );
}

function RiskReportCard({ report }: { report: ExecutionRiskResearchReport }) {
  return (
    <article className="execution-research-card" aria-label={`Execution risk report ${report.report_id}`}>
      <SimBadge value={report.simulation_mode} />
      <h3>{report.report_id}</h3>
      <dl className="kv compact">
        <dt>Source artifacts</dt>
        <dd className="mono">{joinedIds(report.input_artifact_ids)}</dd>
        <dt>Fill count</dt>
        <dd>{firstMetricValue(report.risk_metrics, "simulated_fill_count")}</dd>
        <dt>Uncertainty</dt>
        <dd>{uncertaintySummary(report.uncertainty)}</dd>
        <dt>Economic usefulness</dt>
        <dd>{fmt(report.economic_usefulness.verdict)}</dd>
        <dt>Status</dt>
        <dd>{report.research_status}</dd>
      </dl>
      <section>
        <h4>Request evidence</h4>
        <CompactRecord value={report.simulated_request_summary} />
      </section>
      <section>
        <h4>Limitations</h4>
        <LimitationsList items={report.limitations} />
      </section>
    </article>
  );
}

function ExperimentCard({ experiment }: { experiment: ExecutionResearchExperiment }) {
  return (
    <article className="execution-research-card" aria-label={`Execution experiment ${experiment.experiment_id}`}>
      <SimBadge value={experiment.simulation_mode} />
      <h3>{experiment.experiment_title}</h3>
      <dl className="kv compact">
        <dt>Plan hash</dt>
        <dd className="mono">{experiment.plan_hash.slice(0, 12)}…</dd>
        <dt>Uncertainty</dt>
        <dd>{uncertaintySummary(experiment.uncertainty)}</dd>
        <dt>Status</dt>
        <dd>{experiment.research_status}</dd>
      </dl>
      <section>
        <h4>Pre-registration plan</h4>
        <CompactRecord value={experiment.pre_registration_plan} />
      </section>
      <section>
        <h4>As-of window</h4>
        <CompactRecord value={experiment.as_of_window} />
      </section>
      <section>
        <h4>Replay lineage</h4>
        <CompactRecord value={experiment.replay_input_lineage} />
      </section>
      <section>
        <h4>Included scope</h4>
        <CompactRecord value={experiment.included_scope_summary} />
      </section>
      <section>
        <h4>Limitations</h4>
        <LimitationsList items={experiment.limitations} />
      </section>
    </article>
  );
}

function AnalyticsCard({ report }: { report: SimulatedExecutionAnalyticsReport }) {
  return (
    <article className="execution-research-card analytics-highlight" aria-label={`Simulated analytics ${report.report_id}`}>
      <SimBadge value={report.simulation_mode} />
      <h3>{report.analytics_type}</h3>
      <dl className="kv compact">
        <dt>Sample count</dt>
        <dd>{report.sample_count}</dd>
        <dt>Uncertainty</dt>
        <dd>{uncertaintySummary(report.uncertainty)}</dd>
        <dt>Economic usefulness</dt>
        <dd>{fmt(report.economic_usefulness.verdict)}</dd>
        <dt>Hash</dt>
        <dd className="mono">{report.report_hash.slice(0, 12)}…</dd>
        <dt>Source artifacts</dt>
        <dd className="mono">{joinedIds(report.source_artifact_ids)}</dd>
      </dl>
      <section>
        <h4>Included scope</h4>
        <CompactRecord value={report.included_scope} />
      </section>
      <section>
        <h4>Metrics</h4>
        <CompactRecord value={report.metrics} />
      </section>
      <section>
        <h4>Limitations</h4>
        <LimitationsList items={report.limitations} />
      </section>
    </article>
  );
}

export function ExecutionResearchPage() {
  const [bundle, setBundle] = useState<ExecutionResearchBundle>(EMPTY_BUNDLE);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      setBundle(await fetchExecutionResearchBundle(25));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load execution research artifacts");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void load();
  }, []);

  return (
    <ExecutionResearchWorkspace
      bundle={bundle}
      loading={loading}
      error={error}
      onRefresh={() => void load()}
    />
  );
}
