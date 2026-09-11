import { useEffect, useState } from "react";
import {
  fetchAdvancedResearchReport,
  fetchPortfolioResearchDashboard,
  type AdvancedResearchReport,
  type PortfolioResearchDashboard,
  type PortfolioResearchMetric,
} from "../../../api/client";

/**
 * PortfolioResearchPanel
 *
 * UI-CONV-P03 item 1 — the capabilities of the legacy PortfolioResearchPage are
 * re-homed into the terminal bottom dock as the PORTFOLIO tab (relocation, not
 * retirement: every capability group carries over).
 *
 * - Investigation Context + read-only context navigation links
 * - Hypothetical Aggregate Figures (uncertainty + limitations per metric)
 * - Report Builder / Export Preview
 * - Uncertainty & Limitations + Included Scope
 *
 * R3: no fabricated values — absent data renders explicit empty/unavailable
 * states. T-1/T-6: research-only framing, no actuation.
 */

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
    <article className="portfolio-research-card" data-testid={`portfolio-metric-${metric.key}`}>
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
    <div className="dock-panel portfolio-research-panel" data-testid="portfolio-research-panel">
      <div className="panel-actions-row">
        <span className="panel-title-text">Portfolio Research</span>
        <span className="provenance-badge mono">Research-Only · Non-Actuating</span>
        <button
          type="button"
          className="btn"
          onClick={onRefresh}
          data-testid="portfolio-refresh-btn"
        >
          Refresh research view
        </button>
      </div>

      <section className="advisory-disclaimer" aria-label="Portfolio research disclaimer">
        <strong>Hypothetical research only.</strong> This dashboard summarizes governed research
        artifacts. AXIOM does not act and this view is not a live venue record.
      </section>

      <section className="panel investigation-context-panel" aria-label="Portfolio investigation context">
        <h2>Investigation Context</h2>
        <p className="muted">
          Portfolio research contributes hypothetical review context to investigation and planning.
          It shows existing governed research artifacts, source ids, limitations, and included scope;
          it is not a live venue control and not a transaction surface.
        </p>
        <div className="investigation-evidence-link-list" aria-label="Read-only portfolio context navigation">
          <a className="btn" href="/investigate">
            Open signal investigation workspace
          </a>
          <a className="btn" href="/compare-scenarios">
            Open scenario comparison workspace
          </a>
        </div>
      </section>

      {error ? (
        <p className="error-text" data-testid="portfolio-error">
          {error}
        </p>
      ) : null}
      {loading && !dashboard ? (
        <div className="dock-loading-state" data-testid="portfolio-loading">
          <span>Loading portfolio research dashboard…</span>
        </div>
      ) : null}

      {!loading && !dashboard && !error ? (
        <div className="dock-empty-state" data-testid="portfolio-empty">
          <span className="empty-title">No Portfolio Research Dashboard</span>
          <p className="empty-sub">
            The read-only research API returned no dashboard. Figures are evaluated server-side and
            never fabricated client-side.
          </p>
        </div>
      ) : null}

      <div className="portfolio-research-grid">
        <section className="panel" aria-label="Hypothetical aggregate figures" data-testid="portfolio-aggregate-cards">
          <h2>Hypothetical Aggregate Figures</h2>
          {dashboard && dashboard.aggregate_cards.length === 0 ? (
            <p className="muted">No aggregate figures returned.</p>
          ) : null}
          <div className="portfolio-research-card-grid">
            {(dashboard?.aggregate_cards ?? []).map((metric) => (
              <MetricCard metric={metric} key={metric.key} />
            ))}
          </div>
        </section>

        <section className="panel" aria-label="Report builder and export preview" data-testid="portfolio-report-preview">
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

        <section className="panel" aria-label="Uncertainty and limitations" data-testid="portfolio-uncertainty-limitations">
          <h2>Uncertainty & Limitations</h2>
          {dashboard && dashboard.limitations.length === 0 ? (
            <p className="muted">No limitations declared.</p>
          ) : null}
          <ul className="scenario-limitations">
            {(dashboard?.limitations ?? []).map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
          <h2>Included Scope</h2>
          <pre className="signal-json" data-testid="portfolio-included-scope">
            {jsonText(dashboard?.included_scope ?? {})}
          </pre>
        </section>
      </div>
    </div>
  );
}

/** Self-fetching dock-tab panel (consumes the same two endpoints as the legacy page). */
export function PortfolioResearchPanel() {
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
