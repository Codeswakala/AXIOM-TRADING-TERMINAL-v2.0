import { useEffect, useState } from "react";
import {
  fetchAdvancedResearchReport,
  fetchPortfolioResearchDashboard,
  type AdvancedResearchReport,
  type PortfolioResearchDashboard,
  type PortfolioResearchMetric,
} from "../api/client";

type PortfolioResearchProps = {
  dashboard: PortfolioResearchDashboard | null;
  report: AdvancedResearchReport | null;
  loading?: boolean;
  error?: string | null;
  onRefresh?: () => void;
};

function jsonText(value: unknown): string {
  return JSON.stringify(value, null, 2);
}

function MetricCard({ metric }: { metric: PortfolioResearchMetric }) {
  return (
    <article className="portfolio-research-card">
      <span className="badge stub">hypothetical research</span>
      <h3>{metric.label}</h3>
      <strong>{metric.value}</strong>
      <small>Sample count: {metric.sample_count}</small>
      <small>Uncertainty: {String(metric.uncertainty.method ?? "declared")}</small>
      <small>Economic usefulness: {String(metric.economic_usefulness.verdict ?? "not_assessed")}</small>
      <small className="mono">Source artifacts: {metric.source_artifact_ids.join(", ") || "not supplied"}</small>
    </article>
  );
}

export function PortfolioResearchWorkspace({
  dashboard,
  report,
  loading = false,
  error = null,
  onRefresh,
}: PortfolioResearchProps) {
  return (
    <>
      <div className="page-header">
        <div>
          <h1>Portfolio Research</h1>
          <p className="muted">
            Research aggregation over existing governed advisory and simulated artifacts. Figures are
            hypothetical descriptors with uncertainty and limitations.
          </p>
        </div>
        <button type="button" className="btn primary" onClick={onRefresh}>
          Refresh research view
        </button>
      </div>

      <section className="advisory-disclaimer" aria-label="Portfolio research disclaimer">
        <strong>Hypothetical research only.</strong> This dashboard summarizes governed research
        artifacts. AXIOM does not act and this view is not a live venue record.
      </section>

      <section className="panel span-12 investigation-context-panel" aria-label="Portfolio investigation context">
        <h2>Investigation Context</h2>
        <p className="muted">
          Portfolio research contributes hypothetical review context to investigation and planning.
          It shows existing governed research artifacts, source ids, limitations, and included scope;
          it is not a live venue control and not a transaction surface.
        </p>
        <div className="investigation-evidence-link-list" aria-label="Read-only portfolio context navigation">
          <a className="btn" href="/investigate">Open signal investigation workspace</a>
          <a className="btn" href="/compare-scenarios">Open scenario comparison workspace</a>
        </div>
      </section>

      {error ? <p className="error-text">{error}</p> : null}
      {loading ? <p className="muted">Loading portfolio research dashboard…</p> : null}

      <div className="portfolio-research-grid">
        <section className="panel span-12" aria-label="Hypothetical aggregate figures">
          <h2>Hypothetical Aggregate Figures</h2>
          <div className="portfolio-research-card-grid">
            {(dashboard?.aggregate_cards ?? []).map((metric) => (
              <MetricCard metric={metric} key={metric.key} />
            ))}
          </div>
        </section>

        <section className="panel" aria-label="Report builder and export preview">
          <h2>Report Builder / Export Preview</h2>
          {report ? (
            <article className="portfolio-report-preview">
              <dl className="kv compact">
                <dt>Status</dt>
                <dd>{report.research_status}</dd>
                <dt>Report hash</dt>
                <dd className="mono">{report.report_hash}</dd>
                <dt>Persisted</dt>
                <dd>{String(report.persisted)}</dd>
                <dt>Economic usefulness</dt>
                <dd>{String(report.economic_usefulness.verdict ?? "not_assessed")}</dd>
                <dt>Source artifacts</dt>
                <dd className="mono">{report.source_artifact_ids.join(", ") || "not supplied"}</dd>
              </dl>
              <pre className="signal-json">{report.export_preview_markdown}</pre>
            </article>
          ) : (
            <p className="muted">No report preview loaded.</p>
          )}
        </section>

        <section className="panel" aria-label="Uncertainty and limitations">
          <h2>Uncertainty & Limitations</h2>
          <ul className="scenario-limitations">
            {(dashboard?.limitations ?? []).map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
          <h2>Included Scope</h2>
          <pre className="signal-json">{jsonText(dashboard?.included_scope ?? {})}</pre>
        </section>
      </div>
    </>
  );
}

export function PortfolioResearchPage() {
  const [dashboard, setDashboard] = useState<PortfolioResearchDashboard | null>(null);
  const [report, setReport] = useState<AdvancedResearchReport | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      const [dashboardResponse, reportResponse] = await Promise.all([
        fetchPortfolioResearchDashboard(),
        fetchAdvancedResearchReport(),
      ]);
      setDashboard(dashboardResponse);
      setReport(reportResponse);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load portfolio research view");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void load();
  }, []);

  return (
    <PortfolioResearchWorkspace
      dashboard={dashboard}
      report={report}
      loading={loading}
      error={error}
      onRefresh={() => void load()}
    />
  );
}
