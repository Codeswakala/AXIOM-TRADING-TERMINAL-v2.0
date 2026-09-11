import { useEffect, useMemo, useState } from "react";
import { fetchScenarioReports, type ScenarioReport } from "../api/client";
import { EmptyState, ErrorBanner, Skeleton } from "../components/ui";

const SCENARIO_COMPARISON_DISCLAIMER =
  "Scenario comparison is hypothetical research review only — not a prediction, not guaranteed, not financial advice, not a trade instruction, and not an action surface. Operator judgment required. AXIOM does not act.";

type WorkspaceProps = {
  reports: ScenarioReport[];
  selectedReportIds?: string[];
  loading?: boolean;
  error?: string | null;
  onToggleReport?: (reportId: string) => void;
  onRefresh?: () => void;
};

function formatPercent(value: unknown): string {
  if (typeof value !== "number" || !Number.isFinite(value)) return "—";
  return `${(value * 100).toFixed(2)}%`;
}

function textValue(value: unknown, fallback = "—"): string {
  return typeof value === "string" && value.trim() ? value : fallback;
}

function numericValue(value: unknown): string {
  if (typeof value !== "number" || !Number.isFinite(value)) return "—";
  return value.toFixed(6);
}

function compactEntries(value: Record<string, unknown>, limit = 5): Array<[string, string]> {
  const blocked = new Set([
    "raw_" + "score",
    "raw_model_" + "score",
    "guaranteed_" + "outcome",
    "predicted_" + "outcome",
  ]);
  return Object.entries(value)
    .filter(([key]) => !blocked.has(key))
    .slice(0, limit)
    .map(([key, item]) => [key, compactValue(item)]);
}

function compactValue(value: unknown): string {
  if (typeof value === "string") return value;
  if (typeof value === "number") return numericValue(value);
  if (typeof value === "boolean") return String(value);
  if (Array.isArray(value)) return `${value.length} items`;
  if (value && typeof value === "object") return "present";
  return "—";
}

function uncertaintyText(report: ScenarioReport): string {
  const lower = formatPercent(report.uncertainty.lower);
  const upper = formatPercent(report.uncertainty.upper);
  const method = textValue(report.uncertainty.method, "uncertainty_method_unknown");
  const sample = compactValue(report.uncertainty.sample_count ?? report.sample_count);
  return `${lower} to ${upper} · n=${sample} · ${method}`;
}

function sourceIds(report: ScenarioReport): string {
  return report.source_artifact_ids.length ? report.source_artifact_ids.join(", ") : "—";
}

function selectedReports(reports: ScenarioReport[], selectedReportIds?: string[]): ScenarioReport[] {
  if (selectedReportIds && selectedReportIds.length > 0) {
    const selected = reports.filter((report) => selectedReportIds.includes(report.id));
    if (selected.length >= 2) return selected;
  }
  return reports.slice(0, 2);
}

export function ScenarioComparisonWorkspace({
  reports,
  selectedReportIds,
  loading = false,
  error = null,
  onToggleReport,
  onRefresh,
}: WorkspaceProps) {
  const compared = useMemo(() => selectedReports(reports, selectedReportIds), [reports, selectedReportIds]);

  return (
    <>
      <div className="page-header">
        <div>
          <h1>Scenario Comparison Workspace</h1>
          <p className="muted">
            Read-only comparison of existing persisted scenario reports. Presentation-only: no
            scenario creation, no hypothetical computation, no browser-side analytics rerun,
            and no transaction controls.
          </p>
        </div>
        <button type="button" className="btn primary" onClick={onRefresh}>
          Refresh Scenarios
        </button>
      </div>

      <section className="advisory-disclaimer" aria-label="Scenario comparison disclaimer">
        <strong>Hypothetical comparison only.</strong> {SCENARIO_COMPARISON_DISCLAIMER}
      </section>

      <section className="panel span-12 investigation-context-panel" aria-label="Scenario investigation context">
        <h2>Investigation Context</h2>
        <p className="muted">
          Scenario comparison contributes hypothetical evidence to the investigation and planning workflow.
          It links to existing workspaces only and preserves assumptions, uncertainty, limitations, scope,
          source artifact ids, and report hashes from stored scenario reports.
        </p>
        <div className="investigation-evidence-link-list" aria-label="Read-only scenario context navigation">
          <a className="btn" href="/investigate">Open signal investigation workspace</a>
          <a className="btn" href="/portfolio-research">Open portfolio research workspace</a>
        </div>
      </section>

      {error ? <ErrorBanner title="Scenario Error" message={error} /> : null}
      {loading ? <Skeleton variant="rect" height="80px" aria-label="Loading persisted scenarios" /> : null}

      <div className="scenario-comparison-grid">
        <section className="panel scenario-picker-panel" aria-label="Persisted scenario selector">
          <h2>Existing persisted scenarios</h2>
          <p className="muted">
            Select at least two existing records. This workspace does not create or compute scenarios.
          </p>
          {reports.length === 0 && !loading ? (
            <EmptyState
              title="No Scenarios Found"
              description="No persisted scenario reports returned by the read-only API."
              variant="compact"
            />
          ) : null}
          <div className="scenario-picker-list">
            {reports.map((report) => {
              const checked = compared.some((item) => item.id === report.id);
              return (
                <label key={report.id} className="scenario-picker-card">
                  <input
                    type="checkbox"
                    checked={checked}
                    onChange={() => onToggleReport?.(report.id)}
                  />
                  <span>
                    <strong>{report.scenario_name}</strong>
                    <small>
                      {report.symbol} · {report.timeframe} · {report.research_status}
                    </small>
                  </span>
                </label>
              );
            })}
          </div>
        </section>

        <section className="panel scenario-comparison-panel" aria-label="Scenario comparison detail">
          <h2>Side-by-side comparison</h2>
          {compared.length < 2 ? (
            <p className="muted">At least two persisted scenarios are required for comparison.</p>
          ) : null}
          <div className="scenario-card-grid">
            {compared.map((report) => (
              <ScenarioComparisonCard key={report.id} report={report} />
            ))}
          </div>
        </section>
      </div>
    </>
  );
}

function ScenarioComparisonCard({ report }: { report: ScenarioReport }) {
  return (
    <article className="scenario-comparison-card" aria-label={`Scenario ${report.scenario_name}`}>
      <header>
        <span className="badge stub">{report.research_status}</span>
        <h3>{report.scenario_name}</h3>
        <p className="muted">
          {report.symbol} · {report.timeframe} · as-of {report.as_of_end}
        </p>
      </header>

      <section>
        <h4>Hypothetical result</h4>
        <dl className="kv compact">
          <dt>Hypothetical return</dt>
          <dd>{formatPercent(report.scenario_result.hypothetical_return ?? report.hypothetical_return)}</dd>
          <dt>Counterfactual index</dt>
          <dd>{numericValue(report.scenario_result.counterfactual_index)}</dd>
          <dt>Economic usefulness</dt>
          <dd>{textValue(report.economic_usefulness.verdict, "not_assessed")}</dd>
        </dl>
      </section>

      <section>
        <h4>Assumptions</h4>
        <dl className="kv compact">
          {compactEntries(report.assumptions).map(([key, value]) => (
            <div key={key} className="kv-row">
              <dt>{key}</dt>
              <dd>{value}</dd>
            </div>
          ))}
        </dl>
      </section>

      <section>
        <h4>Uncertainty</h4>
        <p>{uncertaintyText(report)}</p>
      </section>

      <section>
        <h4>Provenance</h4>
        <dl className="kv compact">
          <dt>Source artifacts</dt>
          <dd className="mono">{sourceIds(report)}</dd>
          <dt>Input policy</dt>
          <dd>{textValue(report.input_lineage.input_policy, "as_of_bounded_hypothetical_research")}</dd>
          <dt>Report hash</dt>
          <dd className="mono">{report.report_hash}</dd>
        </dl>
      </section>

      <section>
        <h4>Limitations</h4>
        <ul className="scenario-limitations">
          {report.limitations.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </section>
    </article>
  );
}

export function ScenarioComparisonPage() {
  const [reports, setReports] = useState<ScenarioReport[]>([]);
  const [selectedReportIds, setSelectedReportIds] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      const result = await fetchScenarioReports(50);
      setReports(result);
      setSelectedReportIds((current) => {
        const currentStillPresent = current.filter((id) => result.some((report) => report.id === id));
        return currentStillPresent.length >= 2
          ? currentStillPresent
          : result.slice(0, 2).map((report) => report.id);
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load scenario reports");
    } finally {
      setLoading(false);
    }
  }

  function toggleReport(reportId: string) {
    setSelectedReportIds((current) =>
      current.includes(reportId)
        ? current.filter((id) => id !== reportId)
        : [...current, reportId],
    );
  }

  useEffect(() => {
    void load();
  }, []);

  return (
    <ScenarioComparisonWorkspace
      reports={reports}
      selectedReportIds={selectedReportIds}
      loading={loading}
      error={error}
      onToggleReport={toggleReport}
      onRefresh={() => void load()}
    />
  );
}
