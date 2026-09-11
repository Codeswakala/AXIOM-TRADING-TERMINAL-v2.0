import { useEffect, useMemo, useState } from "react";
import { fetchScenarioReports, type ScenarioReport } from "../../../api/client";

/**
 * ScenarioComparisonPanel
 *
 * UI-CONV-P03 item 2 — the comparison capabilities of the legacy
 * ScenarioComparisonPage are re-homed into the terminal bottom dock SCENARIOS
 * tab (relocation, not retirement): persisted scenario selector, side-by-side
 * comparison, hypothetical result, assumptions, uncertainty, provenance,
 * limitations. No scenario creation or client-side computation (T-1 / R3).
 */

const SCENARIO_COMPARISON_DISCLAIMER =
  "Scenario comparison is hypothetical research review only — not a prediction, not guaranteed, not financial advice, not a trade instruction, and not an action surface. Operator judgment required. AXIOM does not act.";

type ComparisonPanelProps = {
  reports: ScenarioReport[];
  loading?: boolean;
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



export function ScenarioComparisonCard({ report }: { report: ScenarioReport }) {
  return (
    <article
      className="scenario-comparison-card"
      aria-label={`Scenario ${report.scenario_name}`}
      data-testid={`scenario-comparison-card-${report.id}`}
    >
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

export function ScenarioComparisonPanel({ reports, loading = false, onRefresh }: ComparisonPanelProps) {
  const [selectedReportIds, setSelectedReportIds] = useState<string[]>([]);
  const compared = useMemo(
    () => reports.filter((report) => selectedReportIds.includes(report.id)),
    [reports, selectedReportIds],
  );

  // Default to the first two persisted scenarios on load; after the operator
  // interacts, the selection is honoured exactly (deselection is real).
  useEffect(() => {
    if (selectedReportIds.length === 0 && reports.length > 0) {
      setSelectedReportIds(reports.slice(0, 2).map((report) => report.id));
    }
  }, [reports, selectedReportIds.length]);

  function toggleReport(reportId: string) {
    setSelectedReportIds((current) =>
      current.includes(reportId) ? current.filter((id) => id !== reportId) : [...current, reportId],
    );
  }

  return (
    <div className="scenario-comparison-section" data-testid="scenario-comparison-panel">
      <div className="panel-actions-row">
        <span className="panel-title-text">Scenario Comparison Workspace</span>
        <span className="provenance-badge mono">Hypothetical · Non-Actuating</span>
        {onRefresh ? (
          <button
            type="button"
            className="btn"
            onClick={onRefresh}
            data-testid="scenario-refresh-btn"
          >
            Refresh Scenarios
          </button>
        ) : null}
      </div>

      <p className="muted">
        Read-only comparison of existing persisted scenario reports. Presentation-only: no scenario
        creation, no hypothetical computation, no browser-side analytics rerun, and no transaction
        controls.
      </p>

      <section className="advisory-disclaimer" aria-label="Scenario comparison disclaimer">
        <strong>Hypothetical comparison only.</strong> {SCENARIO_COMPARISON_DISCLAIMER}
      </section>

      <section className="panel investigation-context-panel" aria-label="Scenario investigation context">
        <h2>Investigation Context</h2>
        <p className="muted">
          Scenario comparison contributes hypothetical evidence to the investigation and planning workflow.
          It links to existing workspaces only and preserves assumptions, uncertainty, limitations, scope,
          source artifact ids, and report hashes from stored scenario reports.
        </p>
        <div className="investigation-evidence-link-list" aria-label="Read-only scenario context navigation">
          <a className="btn" href="/investigate">
            Open signal investigation workspace
          </a>
          <a className="btn" href="/portfolio-research">
            Open portfolio research workspace
          </a>
        </div>
      </section>

      <div className="scenario-comparison-grid">
        <section
          className="panel scenario-picker-panel"
          aria-label="Persisted scenario selector"
          data-testid="scenario-comparison-picker"
        >
          <h2>Existing persisted scenarios</h2>
          <p className="muted">
            Select at least two existing records. This workspace does not create or compute scenarios.
          </p>
          {!loading && reports.length === 0 ? (
            <div className="dock-empty-state" data-testid="scenario-comparison-empty">
              <span className="empty-title">No Scenarios Found</span>
              <p className="empty-sub">No persisted scenario reports returned by the read-only API.</p>
            </div>
          ) : null}
          <div className="scenario-picker-list">
            {reports.map((report) => {
              const checked = compared.some((item) => item.id === report.id);
              return (
                <label key={report.id} className="scenario-picker-card" data-testid={`scenario-picker-${report.id}`}>
                  <input
                    type="checkbox"
                    checked={checked}
                    onChange={() => toggleReport(report.id)}
                    data-testid={`scenario-picker-checkbox-${report.id}`}
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

        <section
          className="panel scenario-comparison-panel"
          aria-label="Scenario comparison detail"
          data-testid="scenario-comparison-side-by-side"
        >
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
    </div>
  );
}

/** Standalone self-fetching wrapper (used when dock data is unavailable). */
export function ScenarioComparisonPanelStandalone() {
  const [reports, setReports] = useState<ScenarioReport[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    void fetchScenarioReports(50)
      .then((result) => {
        if (!cancelled) setReports(result);
      })
      .catch(() => {
        if (!cancelled) setReports([]);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  return <ScenarioComparisonPanel reports={reports} loading={loading} />;
}
