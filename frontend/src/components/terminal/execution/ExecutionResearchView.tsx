/**
 * ExecutionResearchView — SURF-P01 (Build Order SURF-P01, authorized 2026-08-16).
 *
 * This module is the re-home of `frontend/src/pages/ExecutionResearchPage.tsx`
 * into the terminal primary stage as the full-height EXECUTION RESEARCH view
 * mounted at `/?view=execution`; the legacy route `/execution-research`
 * redirects here.
 *
 * SURF-P01 surfaces capability that was built but not reachable:
 * - S2: the six detail GETs (run, fill, ledger entry, risk report, experiment,
 *   analytics report) now have read-only client functions and are retrieved
 *   on demand when the operator opens a detail record.
 * - S3: the previous silent fills truncation (first five runs only) is removed
 *   at the bundle level, and this view loads fills for every returned run.
 * - R4: six independent read seams, each with its own loading/error state and
 *   genuine loaded counts — one failing seam never blanks the surface
 *   (the item-4 M5 pattern).
 *
 * T-1 applies with full force (Build Order §3): every artifact group carries
 * the SIMULATED · NON-ACTUATING label; no actuation affordance exists, real or
 * implied. The five POST endpoints are EXPLICITLY OUT OF SCOPE — no client
 * function and no create affordance exist anywhere in this module.
 */
import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import {
  fetchExecutionExperimentsList,
  fetchExecutionExperimentDetail,
  fetchExecutionRiskReportsList,
  fetchExecutionRiskReportDetail,
  fetchSimulatedAnalyticsReportsList,
  fetchSimulatedAnalyticsReportDetail,
  fetchSimulatedExecutionRunDetail,
  fetchSimulatedFillDetail,
  fetchSimulatedLedgerEntriesList,
  fetchSimulatedLedgerEntryDetail,
  fetchSimulatedRunFills,
  fetchSimulatedRunsList,
  type ExecutionResearchBundle,
  type ExecutionResearchExperiment,
  type ExecutionRiskResearchReport,
  type SimulatedExecutionAnalyticsReport,
  type SimulatedExecutionRun,
  type SimulatedExecutionRunDetail,
  type SimulatedFillEvent,
  type SimulatedPaperLedgerEntry,
} from "../../../api/client";

export const EXECUTION_RESEARCH_DISCLAIMER =
  "SIMULATED execution research only. Display-only evidence, not financial advice. AXIOM does not act. Governance Gate CLOSED.";

/** R4: per-source state row — the item-4 M5 pattern. */
export type ExecutionSourceStatusRow = {
  family: string;
  state: "loading" | "error" | "ready";
  detail: string | null;
  rowCount: number;
};

export type ExecutionDetailSelection = {
  family: "run" | "fill" | "ledger" | "risk" | "experiment" | "analytics";
  id: string;
};

export type ExecutionDetailRecord =
  | { family: "run"; data: SimulatedExecutionRunDetail }
  | { family: "fill"; data: SimulatedFillEvent }
  | { family: "ledger"; data: SimulatedPaperLedgerEntry }
  | { family: "risk"; data: ExecutionRiskResearchReport }
  | { family: "experiment"; data: ExecutionResearchExperiment }
  | { family: "analytics"; data: SimulatedExecutionAnalyticsReport };

export type ExecutionDetailState =
  | { selection: ExecutionDetailSelection; loading: true; error: null; record: null }
  | { selection: ExecutionDetailSelection; loading: false; error: string; record: null }
  | { selection: ExecutionDetailSelection; loading: false; error: null; record: ExecutionDetailRecord };

const FAMILY_LABELS: Record<ExecutionDetailSelection["family"], string> = {
  run: "simulated run",
  fill: "simulated fill",
  ledger: "simulated ledger entry",
  risk: "risk report",
  experiment: "replay experiment",
  analytics: "analytics report",
};

type WorkspaceProps = {
  bundle: ExecutionResearchBundle;
  loading?: boolean;
  error?: string | null;
  onRefresh?: () => void;
  sourceStatus?: ExecutionSourceStatusRow[];
  detail?: ExecutionDetailState | null;
  onSelectDetail?: (selection: ExecutionDetailSelection) => void;
  onCloseDetail?: () => void;
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

/** M2: the per-group SIMULATED · NON-ACTUATING label. */
function SimulatedGroupBadge({ family }: { family: string }) {
  return (
    <span className="badge stub" data-testid={`execution-sim-badge-${family}`}>
      SIMULATED · NON-ACTUATING
    </span>
  );
}

export function ExecutionResearchWorkspace({
  bundle,
  loading = false,
  error = null,
  onRefresh,
  sourceStatus = [],
  detail = null,
  onSelectDetail,
  onCloseDetail,
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
      <div className="page-header" data-testid="execution-research-header">
        <div>
          <h1>Execution Research Workspace</h1>
          <p className="muted">
            Display-only workspace for server-persisted SIMULATED execution research artifacts.
            Metrics are read from audited backend records; the browser performs no authoritative
            analytics rerun.
          </p>
        </div>
        <div className="execution-header-actions">
          <span className="ix-metadata mono">SIMULATED · NON-ACTUATING</span>
          <button
            type="button"
            className="btn primary"
            onClick={onRefresh}
            data-testid="execution-research-refresh"
          >
            Refresh Research
          </button>
        </div>
      </div>

      <section
        className="advisory-disclaimer"
        aria-label="Execution research disclaimer"
        data-testid="execution-research-disclaimer"
      >
        <strong>SIMULATED.</strong> {EXECUTION_RESEARCH_DISCLAIMER}
      </section>

      <section
        className="panel span-12 investigation-context-panel"
        aria-label="Execution research investigation context"
        data-testid="execution-investigation-context"
      >
        <h2>Investigation Context</h2>
        <p className="muted">
          Execution Research contributes SIMULATED evidence to investigation and planning. It reads
          existing W6 artifacts through the execution-research read seams (simulated runs, fills,
          ledger, risk reports, experiments, analytics), preserves assumptions, uncertainty,
          limitations, source ids, hashes, and policy details, and links only to existing
          registered workspaces. Gate CLOSED.
        </p>
        <div
          className="investigation-evidence-link-list"
          aria-label="Read-only execution research context navigation"
        >
          <Link className="btn" to="/?dock=signals">
            Open signal investigation workspace
          </Link>
          <Link className="btn" to="/trade-plans">
            Open trade planning workspace
          </Link>
          <Link className="btn" to="/journal">
            Open research journal workspace
          </Link>
          <Link className="btn" to="/?panel=scenarios">
            Open scenario comparison workspace
          </Link>
          <Link className="btn" to="/?panel=portfolio">
            Open portfolio research workspace
          </Link>
        </div>
      </section>

      {error ? (
        <p className="error-text" data-testid="execution-research-error">
          {error}
        </p>
      ) : null}
      {loading ? (
        <p className="muted" data-testid="execution-research-loading">
          Loading SIMULATED execution research artifacts…
        </p>
      ) : null}

      {sourceStatus.length > 0 ? (
        <section
          className="panel span-12"
          aria-label="Execution research source status"
          data-testid="execution-source-status"
        >
          <h2>Source Status</h2>
          <p className="muted">
            Independent per-source state for the six execution-research read seams (R4): one
            failing seam never blanks the surface. Row counts are genuine loaded counts — nothing
            is fabricated.
          </p>
          <div className="artifact-source-grid">
            {sourceStatus.map((row) => (
              <article
                className="artifact-source-card"
                key={row.family}
                data-testid={`exec-source-status-${row.state}`}
              >
                <span className="ix-metadata">{row.family}</span>
                {row.state === "loading" ? <p className="muted">Loading…</p> : null}
                {row.state === "error" ? (
                  <p className="error-text">{row.detail ?? "Failed to load source"}</p>
                ) : null}
                {row.state === "ready" ? <small>{row.rowCount} rows loaded</small> : null}
              </article>
            ))}
          </div>
        </section>
      ) : null}

      {detail ? (
        <section
          className="panel span-12"
          aria-label="Execution research detail record"
          data-testid="execution-detail-panel"
        >
          <div className="artifact-explorer-frame-head">
            <div>
              <h2>Detail record — {FAMILY_LABELS[detail.selection.family]}</h2>
              <p className="muted mono">{detail.selection.id}</p>
            </div>
            <button
              type="button"
              className="btn"
              onClick={onCloseDetail}
              data-testid="execution-detail-close"
            >
              Close detail
            </button>
          </div>
          {detail.loading ? (
            <p className="muted" data-testid="execution-detail-loading">
              Loading detail record…
            </p>
          ) : null}
          {detail.error ? (
            <p className="error-text" data-testid="execution-detail-error">
              {detail.error}
            </p>
          ) : null}
          {detail.record ? (
            <div data-testid="execution-detail-record">
              <DetailRecordBody record={detail.record} />
            </div>
          ) : null}
        </section>
      ) : null}

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
        <section className="panel" aria-label="Simulated execution runs" data-testid="execution-group-runs">
          <div className="group-head">
            <h2>Simulated Runs</h2>
            <SimulatedGroupBadge family="runs" />
          </div>
          {bundle.runs.length === 0 ? <p className="muted">No simulated runs returned.</p> : null}
          {bundle.runs.map((run) => (
            <RunCard key={run.run_id} run={run} onSelectDetail={onSelectDetail} />
          ))}
        </section>

        <section className="panel" aria-label="Simulated fill events" data-testid="execution-group-fills">
          <div className="group-head">
            <h2>Simulated Fills</h2>
            <SimulatedGroupBadge family="fills" />
          </div>
          {bundle.fills.length === 0 ? <p className="muted">No simulated fills returned.</p> : null}
          {bundle.fills.map((fill) => (
            <FillCard key={fill.simulated_fill_id} fill={fill} onSelectDetail={onSelectDetail} />
          ))}
        </section>

        <section className="panel" aria-label="Simulated paper ledger" data-testid="execution-group-ledger">
          <div className="group-head">
            <h2>Paper Research Ledger</h2>
            <SimulatedGroupBadge family="ledger" />
          </div>
          {bundle.ledger.length === 0 ? (
            <p className="muted">No simulated ledger rows returned.</p>
          ) : null}
          {bundle.ledger.map((entry) => (
            <LedgerCard key={entry.ledger_entry_id} entry={entry} onSelectDetail={onSelectDetail} />
          ))}
        </section>

        <section className="panel" aria-label="Execution risk reports" data-testid="execution-group-risk">
          <div className="group-head">
            <h2>Risk Research Reports</h2>
            <SimulatedGroupBadge family="risk" />
          </div>
          {bundle.riskReports.length === 0 ? <p className="muted">No risk reports returned.</p> : null}
          {bundle.riskReports.map((report) => (
            <RiskReportCard key={report.report_id} report={report} onSelectDetail={onSelectDetail} />
          ))}
        </section>

        <section className="panel" aria-label="Execution experiments" data-testid="execution-group-experiments">
          <div className="group-head">
            <h2>Replay Experiments</h2>
            <SimulatedGroupBadge family="experiments" />
          </div>
          {bundle.experiments.length === 0 ? (
            <p className="muted">No replay experiments returned.</p>
          ) : null}
          {bundle.experiments.map((experiment) => (
            <ExperimentCard
              key={experiment.experiment_id}
              experiment={experiment}
              onSelectDetail={onSelectDetail}
            />
          ))}
        </section>

        <section className="panel" aria-label="Simulated analytics reports" data-testid="execution-group-analytics">
          <div className="group-head">
            <h2>Analytics &amp; Comparison</h2>
            <SimulatedGroupBadge family="analytics" />
          </div>
          {bundle.analyticsReports.length === 0 ? (
            <p className="muted">No analytics reports returned.</p>
          ) : null}
          {bundle.analyticsReports.map((report) => (
            <AnalyticsCard key={report.report_id} report={report} onSelectDetail={onSelectDetail} />
          ))}
        </section>
      </div>
    </>
  );
}

function SimBadge({ value }: { value: string }) {
  return <span className="badge up">{value}</span>;
}

function DetailButton({
  family,
  id,
  onSelectDetail,
}: {
  family: ExecutionDetailSelection["family"];
  id: string;
  onSelectDetail?: (selection: ExecutionDetailSelection) => void;
}) {
  if (!onSelectDetail) return null;
  return (
    <button
      type="button"
      className="btn"
      data-testid={`execution-detail-open-${family}-${id}`}
      onClick={() => onSelectDetail({ family, id })}
    >
      View detail
    </button>
  );
}

function RunCard({
  run,
  onSelectDetail,
}: {
  run: SimulatedExecutionRun;
  onSelectDetail?: (selection: ExecutionDetailSelection) => void;
}) {
  return (
    <article className="execution-research-card" aria-label={`Simulated run ${run.run_id}`} data-testid={`execution-run-card-${run.run_id}`}>
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
      <DetailButton family="run" id={run.run_id} onSelectDetail={onSelectDetail} />
    </article>
  );
}

function FillCard({
  fill,
  onSelectDetail,
}: {
  fill: SimulatedFillEvent;
  onSelectDetail?: (selection: ExecutionDetailSelection) => void;
}) {
  return (
    <article className="execution-research-card" aria-label={`Simulated fill ${fill.simulated_fill_id}`} data-testid={`execution-fill-card-${fill.simulated_fill_id}`}>
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
      <DetailButton family="fill" id={fill.simulated_fill_id} onSelectDetail={onSelectDetail} />
    </article>
  );
}

function LedgerCard({
  entry,
  onSelectDetail,
}: {
  entry: SimulatedPaperLedgerEntry;
  onSelectDetail?: (selection: ExecutionDetailSelection) => void;
}) {
  return (
    <article className="execution-research-card" aria-label={`Simulated ledger ${entry.ledger_entry_id}`} data-testid={`execution-ledger-card-${entry.ledger_entry_id}`}>
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
      <DetailButton family="ledger" id={entry.ledger_entry_id} onSelectDetail={onSelectDetail} />
    </article>
  );
}

function RiskReportCard({
  report,
  onSelectDetail,
}: {
  report: ExecutionRiskResearchReport;
  onSelectDetail?: (selection: ExecutionDetailSelection) => void;
}) {
  return (
    <article className="execution-research-card" aria-label={`Execution risk report ${report.report_id}`} data-testid={`execution-risk-card-${report.report_id}`}>
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
      <DetailButton family="risk" id={report.report_id} onSelectDetail={onSelectDetail} />
    </article>
  );
}

function ExperimentCard({
  experiment,
  onSelectDetail,
}: {
  experiment: ExecutionResearchExperiment;
  onSelectDetail?: (selection: ExecutionDetailSelection) => void;
}) {
  return (
    <article className="execution-research-card" aria-label={`Execution experiment ${experiment.experiment_id}`} data-testid={`execution-experiment-card-${experiment.experiment_id}`}>
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
      <DetailButton family="experiment" id={experiment.experiment_id} onSelectDetail={onSelectDetail} />
    </article>
  );
}

function AnalyticsCard({
  report,
  onSelectDetail,
}: {
  report: SimulatedExecutionAnalyticsReport;
  onSelectDetail?: (selection: ExecutionDetailSelection) => void;
}) {
  return (
    <article className="execution-research-card analytics-highlight" aria-label={`Simulated analytics ${report.report_id}`} data-testid={`execution-analytics-card-${report.report_id}`}>
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
      <DetailButton family="analytics" id={report.report_id} onSelectDetail={onSelectDetail} />
    </article>
  );
}

function DetailRecordBody({ record }: { record: ExecutionDetailRecord }) {
  switch (record.family) {
    case "run":
      return (
        <>
          <RunCard run={record.data.run} />
          <h4>Fills ({record.data.fills.length})</h4>
          {record.data.fills.length === 0 ? <p className="muted">No fills for this run.</p> : null}
          {record.data.fills.map((fill) => (
            <FillCard key={fill.simulated_fill_id} fill={fill} />
          ))}
        </>
      );
    case "fill":
      return <FillCard fill={record.data} />;
    case "ledger":
      return <LedgerCard entry={record.data} />;
    case "risk":
      return <RiskReportCard report={record.data} />;
    case "experiment":
      return <ExperimentCard experiment={record.data} />;
    case "analytics":
      return <AnalyticsCard report={record.data} />;
  }
}

/**
 * ExecutionResearchView — data orchestration for the EXECUTION RESEARCH
 * stage view (SURF-P01).
 *
 * Six independent read seams with per-source state (R4 / item-4 M5 pattern):
 * runs + fills, ledger, risk reports, experiments, analytics reports. Each
 * detail record is retrieved on demand through one of the six surfaced
 * detail GETs (S2). No POST client function is referenced anywhere.
 */
export function ExecutionResearchView() {
  const [runs, setRuns] = useState<SimulatedExecutionRun[]>([]);
  const [runsLoading, setRunsLoading] = useState(false);
  const [runsError, setRunsError] = useState<string | null>(null);

  const [fills, setFills] = useState<SimulatedFillEvent[]>([]);
  const [fillsLoading, setFillsLoading] = useState(false);
  const [fillsError, setFillsError] = useState<string | null>(null);

  const [ledger, setLedger] = useState<SimulatedPaperLedgerEntry[]>([]);
  const [ledgerLoading, setLedgerLoading] = useState(false);
  const [ledgerError, setLedgerError] = useState<string | null>(null);

  const [riskReports, setRiskReports] = useState<ExecutionRiskResearchReport[]>([]);
  const [riskLoading, setRiskLoading] = useState(false);
  const [riskError, setRiskError] = useState<string | null>(null);

  const [experiments, setExperiments] = useState<ExecutionResearchExperiment[]>([]);
  const [experimentsLoading, setExperimentsLoading] = useState(false);
  const [experimentsError, setExperimentsError] = useState<string | null>(null);

  const [analyticsReports, setAnalyticsReports] = useState<SimulatedExecutionAnalyticsReport[]>([]);
  const [analyticsLoading, setAnalyticsLoading] = useState(false);
  const [analyticsError, setAnalyticsError] = useState<string | null>(null);

  const [detail, setDetail] = useState<ExecutionDetailState | null>(null);

  async function loadRunsAndFills() {
    setRunsLoading(true);
    setRunsError(null);
    try {
      const runRows = await fetchSimulatedRunsList(25);
      setRuns(runRows);
      setFillsLoading(true);
      setFillsError(null);
      try {
        // S3: fills for EVERY returned run — no truncation anywhere.
        const groups = await Promise.all(
          runRows.map((run) => fetchSimulatedRunFills(run.run_id, 50)),
        );
        setFills(groups.flat());
      } catch (err) {
        setFillsError(err instanceof Error ? err.message : "Failed to load simulated fills");
      } finally {
        setFillsLoading(false);
      }
    } catch (err) {
      setRunsError(err instanceof Error ? err.message : "Failed to load simulated runs");
      setFillsError("Simulated runs unavailable — fills not loaded");
    } finally {
      setRunsLoading(false);
    }
  }

  async function loadLedger() {
    setLedgerLoading(true);
    setLedgerError(null);
    try {
      setLedger(await fetchSimulatedLedgerEntriesList(25));
    } catch (err) {
      setLedgerError(err instanceof Error ? err.message : "Failed to load simulated ledger rows");
    } finally {
      setLedgerLoading(false);
    }
  }

  async function loadRiskReports() {
    setRiskLoading(true);
    setRiskError(null);
    try {
      setRiskReports(await fetchExecutionRiskReportsList(25));
    } catch (err) {
      setRiskError(err instanceof Error ? err.message : "Failed to load risk reports");
    } finally {
      setRiskLoading(false);
    }
  }

  async function loadExperiments() {
    setExperimentsLoading(true);
    setExperimentsError(null);
    try {
      setExperiments(await fetchExecutionExperimentsList(25));
    } catch (err) {
      setExperimentsError(err instanceof Error ? err.message : "Failed to load replay experiments");
    } finally {
      setExperimentsLoading(false);
    }
  }

  async function loadAnalyticsReports() {
    setAnalyticsLoading(true);
    setAnalyticsError(null);
    try {
      setAnalyticsReports(await fetchSimulatedAnalyticsReportsList(25));
    } catch (err) {
      setAnalyticsError(err instanceof Error ? err.message : "Failed to load analytics reports");
    } finally {
      setAnalyticsLoading(false);
    }
  }

  function loadAll() {
    void loadRunsAndFills();
    void loadLedger();
    void loadRiskReports();
    void loadExperiments();
    void loadAnalyticsReports();
  }

  // Load on first mount; refresh is operator-initiated (item-4 M5 pattern).
  const [hasLoaded, setHasLoaded] = useState(false);
  useEffect(() => {
    if (!hasLoaded) {
      setHasLoaded(true);
      loadAll();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps -- load-on-mount only
  }, [hasLoaded]);

  async function selectDetail(selection: ExecutionDetailSelection) {
    setDetail({ selection, loading: true, error: null, record: null });
    try {
      switch (selection.family) {
        case "run": {
          const data = await fetchSimulatedExecutionRunDetail(selection.id);
          setDetail({ selection, loading: false, error: null, record: { family: "run", data } });
          return;
        }
        case "fill": {
          const data = await fetchSimulatedFillDetail(selection.id);
          setDetail({ selection, loading: false, error: null, record: { family: "fill", data } });
          return;
        }
        case "ledger": {
          const data = await fetchSimulatedLedgerEntryDetail(selection.id);
          setDetail({ selection, loading: false, error: null, record: { family: "ledger", data } });
          return;
        }
        case "risk": {
          const data = await fetchExecutionRiskReportDetail(selection.id);
          setDetail({ selection, loading: false, error: null, record: { family: "risk", data } });
          return;
        }
        case "experiment": {
          const data = await fetchExecutionExperimentDetail(selection.id);
          setDetail({
            selection,
            loading: false,
            error: null,
            record: { family: "experiment", data },
          });
          return;
        }
        case "analytics": {
          const data = await fetchSimulatedAnalyticsReportDetail(selection.id);
          setDetail({
            selection,
            loading: false,
            error: null,
            record: { family: "analytics", data },
          });
          return;
        }
      }
    } catch (err) {
      setDetail({
        selection,
        loading: false,
        error: err instanceof Error ? err.message : "Failed to load detail record",
        record: null,
      });
    }
  }

  const bundle = useMemo<ExecutionResearchBundle>(
    () => ({
      runs,
      fills,
      ledger,
      riskReports,
      experiments,
      analyticsReports,
    }),
    [runs, fills, ledger, riskReports, experiments, analyticsReports],
  );

  const sourceStatus: ExecutionSourceStatusRow[] = [
    {
      family: "Simulated runs",
      state: runsLoading ? "loading" : runsError ? "error" : "ready",
      detail: runsError,
      rowCount: runs.length,
    },
    {
      family: "Simulated fills",
      state: fillsLoading ? "loading" : fillsError ? "error" : "ready",
      detail: fillsError,
      rowCount: fills.length,
    },
    {
      family: "Paper ledger",
      state: ledgerLoading ? "loading" : ledgerError ? "error" : "ready",
      detail: ledgerError,
      rowCount: ledger.length,
    },
    {
      family: "Risk reports",
      state: riskLoading ? "loading" : riskError ? "error" : "ready",
      detail: riskError,
      rowCount: riskReports.length,
    },
    {
      family: "Replay experiments",
      state: experimentsLoading ? "loading" : experimentsError ? "error" : "ready",
      detail: experimentsError,
      rowCount: experiments.length,
    },
    {
      family: "Analytics reports",
      state: analyticsLoading ? "loading" : analyticsError ? "error" : "ready",
      detail: analyticsError,
      rowCount: analyticsReports.length,
    },
  ];

  return (
    <ExecutionResearchWorkspace
      bundle={bundle}
      sourceStatus={sourceStatus}
      detail={detail}
      onSelectDetail={(selection) => void selectDetail(selection)}
      onCloseDetail={() => setDetail(null)}
      onRefresh={() => loadAll()}
    />
  );
}

/**
 * Legacy export-name continuity: `ExecutionResearchPage` remains importable
 * under its original name and now resolves to the Execution Research stage
 * view.
 */
export { ExecutionResearchView as ExecutionResearchPage };
