import { useEffect, useMemo, useState } from "react";
import {
  fetchAdvisoryAnalytics,
  fetchAdvisorySignals,
  fetchInstitutionalIntelligenceBundle,
  fetchJournalEntries,
  fetchResearchManagementBundle,
  type AdvisoryAnalyticsMetric,
  type AdvisoryAnalyticsResponse,
  type AdvisorySignal,
  type ConfidenceBand,
  type InstitutionalIntelligenceBundle,
  type InstitutionalReport,
  type ManualJournalEntry,
  type ResearchManagementBundle,
} from "../api/client";
import { AssistantReviewSubPanel } from "./institutional/AssistantReviewSubPanel";
import { ContextualAssistantPanel } from "../workstation/ai/ContextualAssistantPanel";
import { Panel, PanelHeader, Collapsible, EmptyState, ErrorBanner, Skeleton } from "../components/ui";

type DashboardProps = {
  bundle: InstitutionalIntelligenceBundle | null;
  signals?: AdvisorySignal[];
  analytics?: AdvisoryAnalyticsResponse | null;
  researchManagement?: ResearchManagementBundle | null;
  journalEntries?: ManualJournalEntry[];
  loading?: boolean;
  error?: string | null;
  onRefresh?: () => void;
};

type SectionSpec = {
  key: keyof InstitutionalIntelligenceBundle;
  title: string;
  description: string;
};

export type ResearchDataSourceInventoryItem = {
  surface: string;
  existingOrigin: string;
  existingReadSource: string;
  route: string;
  phase: string;
  posture: string;
};

export const UI004_RESEARCH_DATA_SOURCES: ResearchDataSourceInventoryItem[] = [
  {
    surface: "Institutional Intelligence",
    existingOrigin: "W4 governed intelligence report families",
    existingReadSource: "fetchInstitutionalIntelligenceBundle",
    route: "/intelligence",
    phase: "P01 frame and inventory",
    posture: "Stored report fields displayed as-is",
  },
  {
    surface: "Advisory Signals",
    existingOrigin: "W3 advisory signal records",
    existingReadSource: "fetchAdvisorySignals",
    route: "/signals",
    phase: "P02 integration boundary",
    posture: "Read-only signal context; calibrated confidence only",
  },
  {
    surface: "Performance Analytics",
    existingOrigin: "Existing advisory analytics response",
    existingReadSource: "fetchAdvisoryAnalytics",
    route: "/analytics",
    phase: "P02b analytics boundary",
    posture: "Stored metrics with uncertainty and sample counts",
  },
  {
    surface: "Validation",
    existingOrigin: "W4 signal validation reports",
    existingReadSource: "fetchInstitutionalIntelligenceBundle.validation",
    route: "/intelligence",
    phase: "P04 integrity panels boundary",
    posture: "Validation status rendered verbatim",
  },
  {
    surface: "Economic Usefulness",
    existingOrigin: "Stored economic verdict/usefulness fields on reports/signals",
    existingReadSource: "existing report economic_usefulness / economic_verdict fields",
    route: "/intelligence",
    phase: "P04 integrity panels boundary",
    posture: "Verdicts displayed verbatim", 
  },
  {
    surface: "Research Artifacts",
    existingOrigin: "W7 research collections and tags",
    existingReadSource: "fetchResearchManagementBundle",
    route: "/?view=research",
    phase: "P05 artifact context boundary",
    posture: "Context links only; collections/tags read-only in UI-004",
  },
  {
    surface: "Report Viewers",
    existingOrigin: "Existing W4/W7 report payloads and hashes",
    existingReadSource: "existing intelligence and portfolio report read APIs",
    route: "/intelligence",
    phase: "P03 viewer boundary",
    posture: "Progressive disclosure of stored fields",
  },
];

const SECTIONS: SectionSpec[] = [
  {
    key: "relation",
    title: "Cross-Market Relation Reports",
    description: "Statistical relationship research with intervals and lineage.",
  },
  {
    key: "context",
    title: "Market Context Reports",
    description: "Explainable market-context labels with confidence and evidence.",
  },
  {
    key: "hypothetical",
    title: "Hypothetical Research Studies",
    description: "Counterfactual research with assumptions, limitations, and uncertainty.",
  },
  {
    key: "risk",
    title: "Market-Series Risk Reports",
    description: "Hypothetical risk metrics with sample counts; not a real account view.",
  },
  {
    key: "validation",
    title: "Advisory Quality Review",
    description: "Historical signal-record validation with honest outcome-data status.",
  },
];

function pct(value: unknown): string {
  if (typeof value !== "number") return "—";
  return `${(value * 100).toFixed(2)}%`;
}

function text(value: unknown): string {
  if (value == null) return "—";
  if (typeof value === "string") return value;
  if (typeof value === "number" || typeof value === "boolean") return String(value);
  return JSON.stringify(sanitizeForDisplay(value));
}

function sanitizeForDisplay(value: unknown): unknown {
  const blockedKey = `raw_${"score"}`;
  if (Array.isArray(value)) return value.map((item) => sanitizeForDisplay(item));
  if (value && typeof value === "object") {
    return Object.fromEntries(
      Object.entries(value as Record<string, unknown>)
        .filter(([key]) => key !== blockedKey)
        .map(([key, nested]) => [key, sanitizeForDisplay(nested)]),
    );
  }
  return value;
}

type DisplayInterval = {
  lower: unknown;
  upper: unknown;
  sampleCount: unknown;
  method: unknown;
};

function asRecord(value: unknown): Record<string, unknown> | null {
  return value && typeof value === "object" && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : null;
}

function boundedInterval(value: unknown): Record<string, unknown> | null {
  const record = asRecord(value);
  if (!record) return null;
  return typeof record.lower === "number" && typeof record.upper === "number" ? record : null;
}

function firstNestedInterval(value: unknown): Record<string, unknown> | null {
  const record = asRecord(value);
  if (!record) return null;
  for (const nested of Object.values(record)) {
    const nestedRecord = asRecord(nested);
    const direct = boundedInterval(nestedRecord);
    if (direct) return direct;
    const nestedUncertainty = boundedInterval(nestedRecord?.uncertainty);
    if (nestedUncertainty) return nestedUncertainty;
  }
  return null;
}

function displayInterval(report: InstitutionalReport): DisplayInterval | null {
  const top = asRecord(report.uncertainty);
  const direct = boundedInterval(top);
  if (direct) {
    return {
      lower: direct.lower,
      upper: direct.upper,
      sampleCount: direct.sample_count,
      method: direct.method,
    };
  }
  const nested = firstNestedInterval(top?.metrics) ?? firstNestedInterval(report.metrics);
  if (!nested) return null;
  return {
    lower: nested.lower,
    upper: nested.upper,
    sampleCount: top?.sample_count ?? nested.sample_count,
    method: top?.method ?? nested.method,
  };
}

function uncertaintyText(report: InstitutionalReport): string {
  const interval = displayInterval(report);
  if (!interval) return "Uncertainty missing";
  return `${pct(interval.lower)} to ${pct(interval.upper)} · n=${text(interval.sampleCount)} · ${text(
    interval.method,
  )}`;
}

function primaryLabel(report: InstitutionalReport): string {
  const candidates = [
    report["reg" + "ime_" + "label"],
    report["scen" + "ario_" + "name"],
    report.artifact_type,
    report.method_version,
  ];
  return text(candidates.find((item) => item != null));
}

function allReports(bundle: InstitutionalIntelligenceBundle | null): InstitutionalReport[] {
  return bundle ? Object.values(bundle).flat() : [];
}

function countReportRows(bundle: InstitutionalIntelligenceBundle | null): number {
  if (!bundle) return 0;
  let total = 0;
  for (const rows of Object.values(bundle)) {
    total += rows.length;
  }
  return total;
}

function hasEconomicContext(report: InstitutionalReport): boolean {
  return Boolean(report.economic_usefulness ?? report.economic_meaning ?? report["economic_verdict"]);
}

function ResearchWorkspaceFrame({ bundle }: { bundle: InstitutionalIntelligenceBundle | null }) {
  const reportRows = allReports(bundle);
  const validationRows = bundle?.validation.length ?? 0;
  const economicRows = reportRows.filter(hasEconomicContext).length;
  const overview = [
    {
      label: "Intelligence reports",
      value: String(reportRows.length),
      source: "fetchInstitutionalIntelligenceBundle",
      note: "Existing governed report families",
    },
    {
      label: "Advisory signal source",
      value: "registered",
      source: "fetchAdvisorySignals",
      note: "Read-only signal integration boundary",
    },
    {
      label: "Analytics source",
      value: "registered",
      source: "fetchAdvisoryAnalytics",
      note: "Existing metrics with uncertainty",
    },
    {
      label: "Validation rows",
      value: String(validationRows),
      source: "bundle.validation",
      note: "Stored validation fields only",
    },
    {
      label: "Economic context rows",
      value: String(economicRows),
      source: "economic_usefulness / economic_verdict",
      note: "Verbatim verdict posture",
    },
    {
      label: "Artifact source",
      value: "registered",
      source: "fetchResearchManagementBundle",
      note: "Collections and tags read-only in UI-004",
    },
  ];

  return (
    <section className="panel span-12 research-workspace-frame" aria-label="Research and intelligence workspace frame">
      <div className="research-workspace-frame-head">
        <div>
          <h2>Research & Intelligence Workspace</h2>
          <p className="muted">
            Continuous research workflow over existing governed artifacts. The browser presents stored
            values only, preserves validation and economic verdict text, and does not create signals,
            invoke external AI, or expose an execution pathway.
          </p>
        </div>
        <div className="research-guardrail-card" role="note" aria-label="Stored-value guardrail">
          <strong>Stored-value guardrail</strong>
          <span>Gate CLOSED · Research-only · Existing read sources only</span>
        </div>
      </div>

      <div className="research-overview-card-grid" aria-label="Research workspace overview cards">
        {overview.map((item) => (
          <article className="research-overview-card" key={item.label}>
            <span className="ix-metadata">{item.label}</span>
            <strong className="mono">{item.value}</strong>
            <small>{item.note}</small>
            <small className="mono">{item.source}</small>
          </article>
        ))}
      </div>

      <div className="research-data-source-inventory" aria-label="UI-004 governed data-source inventory">
        <h3>Governed Data-Source Inventory</h3>
        <p className="muted">
          Every UI-004 surface below maps to an existing governed store or read API. Later phases may
          deepen presentation, but P01 establishes source ownership first.
        </p>
        <div className="research-data-source-grid">
          {UI004_RESEARCH_DATA_SOURCES.map((item) => (
            <article className="research-data-source-card" key={item.surface}>
              <strong>{item.surface} source</strong>
              <dl className="kv compact">
                <dt>Origin</dt>
                <dd>{item.existingOrigin}</dd>
                <dt>Read source</dt>
                <dd className="mono">{item.existingReadSource}</dd>
                <dt>Route</dt>
                <dd className="mono">{item.route}</dd>
                <dt>Phase</dt>
                <dd>{item.phase}</dd>
                <dt>Posture</dt>
                <dd>{item.posture}</dd>
              </dl>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

function signalStateLabel(signal: AdvisorySignal): string {
  const labels: Record<AdvisorySignal["signal_state"], string> = {
    emitted: "Advisory",
    warning: "Warning",
    withheld: "Withheld",
    expired: "Expired",
    superseded: "Superseded",
  };
  return labels[signal.signal_state];
}

function signalStateHelp(signal: AdvisorySignal): string {
  switch (signal.signal_state) {
    case "emitted":
      return "Clean advisory record; research-only and operator-decided.";
    case "warning":
      return "Guardrail warning; review calibration, freshness, and limitations.";
    case "withheld":
      return "Withheld record; not presented as current advisory context.";
    case "expired":
      return "Expired record; retained for research history only.";
    case "superseded":
      return "Superseded record; retained for lineage and audit context.";
  }
}

function calibratedConfidenceText(value: number | null): string {
  if (value == null) return "Not calibrated";
  return `${(value * 100).toFixed(1)}% calibrated`;
}

function dateText(value: string | null): string {
  if (!value) return "—";
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return value;
  return parsed.toISOString();
}

function lineageRows(signal: AdvisorySignal): Array<[string, string | null]> {
  return [
    ["Signal id", signal.signal_id],
    ["Model artifact", signal.model_artifact_id],
    ["Model version", signal.model_version],
    ["Experiment", signal.experiment_id],
    ["Feature set", signal.feature_set_version],
    ["Statistical report", signal.statistical_report_id],
    ["Calibration report", signal.calibration_report_id],
    ["Economic report", signal.economic_report_id],
    ["Generalization report", signal.generalization_report_id],
  ];
}

export function ResearchAdvisorySignalPanel({
  signals,
  loading = false,
  error = null,
}: {
  signals: AdvisorySignal[];
  loading?: boolean;
  error?: string | null;
}) {
  const selected = signals[0] ?? null;
  return (
    <section className="panel span-12 research-signal-panel" aria-label="Read-only advisory signal research surface">
      <div className="research-signal-panel-head">
        <div>
          <h2>Advisory Signal Research Context</h2>
          <p className="muted">
            Existing advisory records from <span className="mono">fetchAdvisorySignals</span> are shown
            as read-only research context with stored guardrails, calibrated confidence, freshness,
            economic verdict, rationale, and lineage. They are not financial advice, not a trade
            instruction, and the operator decides independently.
          </p>
        </div>
        <div className="research-guardrail-card" role="note" aria-label="Advisory signal posture">
          <strong>Advisory posture</strong>
          <span>Read-only · Calibrated confidence · Non-actionable</span>
        </div>
      </div>

      {error ? <ErrorBanner title="Advisory Signals Error" message={error} /> : null}
      {loading ? <Skeleton variant="rect" height="120px" aria-label="Loading existing advisory records" /> : null}
      {signals.length === 0 && !loading ? (
        <EmptyState
          title="No Advisory Signals"
          description="No existing advisory signals returned by the read API."
          variant="compact"
        />
      ) : null}

      <div className="research-signal-layout">
        <div className="research-signal-card-grid" aria-label="Read-only advisory signal cards">
          {signals.map((signal) => (
            <article className={`research-signal-card signal-${signal.signal_state}`} key={signal.signal_id} data-readonly="true">
              <span className={`signal-state-badge signal-${signal.signal_state}`}>{signalStateLabel(signal)}</span>
              <strong>{signal.symbol} · {signal.timeframe}</strong>
              <small>{signalStateHelp(signal)}</small>
              <dl className="kv compact">
                <dt>State reason</dt>
                <dd>{signal.state_reason}</dd>
                <dt>Freshness</dt>
                <dd>{signal.freshness_status ?? "—"}</dd>
                <dt>Calibrated confidence</dt>
                <dd>{calibratedConfidenceText(signal.calibrated_confidence)}</dd>
                <dt>Economic verdict</dt>
                <dd>{signal.economic_verdict}</dd>
              </dl>
            </article>
          ))}
        </div>

        {selected ? (
          <article className="research-signal-detail-card" aria-label="Selected advisory signal stored detail">
            <div className="signal-detail-head">
              <div>
                <span className={`signal-state-badge signal-${selected.signal_state}`}>{signalStateLabel(selected)}</span>
                <h3>{selected.symbol} · {selected.timeframe}</h3>
                <p className="muted">{selected.rationale}</p>
              </div>
              <div className="confidence-box" aria-label="Stored calibrated confidence">
                <span>Calibrated Confidence</span>
                <strong>{calibratedConfidenceText(selected.calibrated_confidence)}</strong>
                <small>{selected.calibration_status}</small>
              </div>
            </div>

            <div className="signal-detail-grid">
              <section className="signal-section">
                <h4>Stored guardrails</h4>
                <dl className="kv compact">
                  <dt>State reason</dt>
                  <dd>{selected.state_reason}</dd>
                  <dt>Operating domain</dt>
                  <dd>{selected.operating_domain_status}</dd>
                  <dt>Calibration</dt>
                  <dd>{selected.calibration_status}</dd>
                  <dt>Economic verdict</dt>
                  <dd>{selected.economic_verdict}</dd>
                  <dt>Freshness</dt>
                  <dd>{selected.freshness_status ?? "—"}</dd>
                  <dt>Expires</dt>
                  <dd>{dateText(selected.expires_at)}</dd>
                </dl>
              </section>

              <section className="signal-section">
                <h4>Lineage and context links</h4>
                <dl className="kv compact">
                  {lineageRows(selected).map(([label, value]) => (
                    <div className="kv-row" key={label}>
                      <dt>{label}</dt>
                      <dd className="mono">{value ?? "—"}</dd>
                    </div>
                  ))}
                </dl>
                <div className="research-context-link-list" aria-label="Read-only signal context navigation">
                  <a className="btn" href="/signals">Open advisory signal workspace</a>
                  <a className="btn" href="/investigate">Open investigation workspace</a>
                </div>
              </section>
            </div>
          </article>
        ) : null}
      </div>
    </section>
  );
}

function metricHasUncertainty(metric: AdvisoryAnalyticsMetric): boolean {
  return Boolean(
    metric.uncertainty &&
      typeof metric.uncertainty.lower === "number" &&
      typeof metric.uncertainty.upper === "number" &&
      typeof metric.uncertainty.sample_count === "number",
  );
}

function analyticsPercent(value: number | null): string {
  if (value == null) return "Unavailable";
  return `${(value * 100).toFixed(1)}%`;
}

function analyticsIntervalText(item: AdvisoryAnalyticsMetric | ConfidenceBand): string {
  return `${analyticsPercent(item.uncertainty.lower)} to ${analyticsPercent(item.uncertainty.upper)}`;
}

function analyticsRecord(analytics: AdvisoryAnalyticsResponse | null): Record<string, unknown> {
  return analytics ? (analytics as unknown as Record<string, unknown>) : {};
}

function stringArrayField(source: Record<string, unknown>, key: string): string[] {
  const value = source[key];
  return Array.isArray(value) ? value.filter((item): item is string => typeof item === "string") : [];
}

function displayJsonField(source: Record<string, unknown>, key: string, fallback: string): string {
  const value = source[key];
  if (value == null) return fallback;
  if (typeof value === "string") return value;
  return JSON.stringify(value, null, 2);
}

export function ResearchPerformanceAnalyticsPanel({
  analytics,
  loading = false,
  error = null,
}: {
  analytics: AdvisoryAnalyticsResponse | null;
  loading?: boolean;
  error?: string | null;
}) {
  const metrics = analytics?.metrics ?? [];
  const bands = analytics?.confidence_bands ?? [];
  const record = analyticsRecord(analytics);
  const limitations = stringArrayField(record, "limitations");
  const sourceArtifactIds = stringArrayField(record, "source_artifact_ids");

  return (
    <section className="panel span-12 research-analytics-panel" aria-label="Read-only performance analytics research surface">
      <div className="research-signal-panel-head">
        <div>
          <h2>Performance Analytics Research Context</h2>
          <p className="muted">
            Existing analytics from <span className="mono">fetchAdvisoryAnalytics</span> are displayed
            read-only with stored uncertainty, sample counts, confidence bands, source notes, and
            limitations. This panel does not infer, rescore, or produce a browser-side performance
            metric from displayed signal rows.
          </p>
        </div>
        <div className="research-guardrail-card" role="note" aria-label="Analytics no cherry picking posture">
          <strong>No selective performance claim</strong>
          <span>Sample counts · uncertainty · limitations visible</span>
        </div>
      </div>

      {error ? <ErrorBanner title="Advisory Analytics Error" message={error} /> : null}
      {loading ? <Skeleton variant="rect" height="120px" aria-label="Loading existing advisory analytics" /> : null}
      {analytics?.disclaimer ? <p className="advisory-disclaimer">{analytics.disclaimer}</p> : null}

      <div className="research-analytics-grid">
        <section className="research-analytics-section" aria-label="Stored analytics metrics with uncertainty">
          <h3>Stored Metrics</h3>
          <div className="research-analytics-card-grid">
            {metrics.map((metric) => (
              <article className={`research-analytics-card${metricHasUncertainty(metric) ? "" : " metric-warning"}`} key={metric.key}>
                <span className="ix-metadata">{metric.label}</span>
                {metricHasUncertainty(metric) ? (
                  <>
                    <strong className="mono">{analyticsPercent(metric.value)}</strong>
                    <dl className="kv compact">
                      <dt>Interval</dt>
                      <dd>{analyticsIntervalText(metric)}</dd>
                      <dt>Sample count</dt>
                      <dd className="mono">{metric.sample_count}</dd>
                      <dt>Method</dt>
                      <dd>{metric.uncertainty.method}</dd>
                    </dl>
                    <small>{metric.interpretation}</small>
                  </>
                ) : (
                  <>
                    <strong>Metric withheld: uncertainty missing</strong>
                    <small>Point-estimate-only analytics are not displayed.</small>
                  </>
                )}
              </article>
            ))}
          </div>
        </section>

        <section className="research-analytics-section" aria-label="Stored calibrated confidence bands">
          <h3>Calibrated Confidence Bands</h3>
          <div className="research-analytics-card-grid">
            {bands.map((band) => (
              <article className={`research-analytics-card${band.unreliable ? " metric-warning" : ""}`} key={band.label}>
                <span className="ix-metadata">{band.label}</span>
                <strong className="mono">{analyticsPercent(band.average_calibrated_confidence)}</strong>
                <dl className="kv compact">
                  <dt>Band</dt>
                  <dd>{analyticsPercent(band.lower)} to {analyticsPercent(band.upper)}</dd>
                  <dt>Uncertainty</dt>
                  <dd>{analyticsIntervalText(band)}</dd>
                  <dt>Sample count</dt>
                  <dd className="mono">{band.sample_count}</dd>
                  <dt>Calibration</dt>
                  <dd>{band.calibration_status}</dd>
                  <dt>Economic context</dt>
                  <dd>{band.economic_context}</dd>
                </dl>
                {band.unreliable ? <small className="warning-text">Unreliable calibration warning preserved.</small> : null}
              </article>
            ))}
          </div>
        </section>

        <section className="research-analytics-section span-all" aria-label="Analytics scope notes limitations and sources">
          <h3>Scope, Notes, Limitations, and Sources</h3>
          <dl className="kv compact">
            <dt>Generated from</dt>
            <dd>{analytics?.generated_from ?? "existing advisory analytics response"}</dd>
            <dt>Included scope</dt>
            <dd className="mono">{displayJsonField(record, "included_scope", "Current analytics response scope; no browser-side row filtering applied")}</dd>
            <dt>Source artifacts</dt>
            <dd className="mono">{sourceArtifactIds.length > 0 ? sourceArtifactIds.join(", ") : "Not supplied by current read response"}</dd>
          </dl>
          <div className="research-analytics-notes">
            <div>
              <strong>Notes</strong>
              <ul>
                {(analytics?.notes ?? []).map((note) => <li key={note}>{note}</li>)}
              </ul>
            </div>
            <div>
              <strong>Limitations</strong>
              {limitations.length > 0 ? (
                <ul>{limitations.map((item) => <li key={item}>{item}</li>)}</ul>
              ) : (
                <p className="muted">No limitations array supplied by current read response; metric uncertainty and source notes remain visible.</p>
              )}
            </div>
          </div>
          <div className="research-context-link-list" aria-label="Read-only analytics context navigation">
            <a className="btn" href="/analytics">Open performance analytics workspace</a>
            <a className="btn" href="/signals">Open advisory signal workspace</a>
          </div>
        </section>
      </div>
    </section>
  );
}

type ReportFamilyView = {
  key: keyof InstitutionalIntelligenceBundle;
  title: string;
  description: string;
  reports: InstitutionalReport[];
};

function reportFamilies(bundle: InstitutionalIntelligenceBundle | null): ReportFamilyView[] {
  return SECTIONS.map((section) => ({
    ...section,
    reports: bundle?.[section.key] ?? [],
  }));
}

function reportDisplayId(report: InstitutionalReport): string {
  return report.id ?? report.report_id ?? report.report_hash ?? "stored-report";
}

function reportMethodVersion(report: InstitutionalReport): string {
  return text(report.method_version ?? report["model_version"] ?? report["validation_version"]);
}

function reportSourceIds(report: InstitutionalReport): string[] {
  const direct = report.source_artifact_ids;
  if (Array.isArray(direct)) return direct.map(String);
  const lineage = asRecord(report.input_lineage);
  const lineageSourceIds = lineage?.source_artifact_ids;
  if (Array.isArray(lineageSourceIds)) return lineageSourceIds.map(String);
  return [];
}

function storedFieldJson(value: unknown): string {
  return JSON.stringify(sanitizeForDisplay(value ?? {}), null, 2);
}

export function IntelligenceReportViewer({
  bundle,
}: {
  bundle: InstitutionalIntelligenceBundle | null;
}) {
  const families = reportFamilies(bundle);
  const firstFamilyWithReport = families.find((family) => family.reports.length > 0) ?? families[0];
  const [activeFamilyKey, setActiveFamilyKey] = useState<keyof InstitutionalIntelligenceBundle>(firstFamilyWithReport.key);
  const activeFamily = families.find((family) => family.key === activeFamilyKey) ?? firstFamilyWithReport;
  const [selectedReportId, setSelectedReportId] = useState<string | null>(null);
  const selectedReport =
    activeFamily.reports.find((report) => reportDisplayId(report) === selectedReportId) ??
    activeFamily.reports[0] ??
    null;

  useEffect(() => {
    if (!selectedReport || activeFamily.reports.some((report) => reportDisplayId(report) === selectedReportId)) return;
    setSelectedReportId(reportDisplayId(selectedReport));
  }, [activeFamily.reports, selectedReport, selectedReportId]);

  return (
    <section className="panel span-12 intelligence-report-viewer" aria-label="First-party intelligence report viewer">
      <div className="research-signal-panel-head">
        <div>
          <h2>Intelligence Report Viewer</h2>
          <p className="muted">
            First-party viewer for existing W4/W7 report payloads. Drilldowns reveal stored fields,
            report hashes, methods, uncertainty, source lineage, and limitations without changing
            verdicts or creating generated explanations.
          </p>
        </div>
        <div className="research-guardrail-card" role="note" aria-label="Report viewer integrity posture">
          <strong>Disclosure only</strong>
          <span>Stored fields · lineage · limitations</span>
        </div>
      </div>

      <nav className="report-family-nav" aria-label="Report family navigation">
        {families.map((family) => (
          <button
            key={family.key}
            type="button"
            className={`btn ${activeFamily.key === family.key ? "primary" : ""}`}
            aria-pressed={activeFamily.key === family.key}
            onClick={() => {
              setActiveFamilyKey(family.key);
              setSelectedReportId(family.reports[0] ? reportDisplayId(family.reports[0]) : null);
            }}
          >
            Family: {family.title}
            <span className="sr-only"> — {family.description}</span>
          </button>
        ))}
      </nav>

      <div className="report-viewer-layout">
        <section className="report-artifact-list" aria-label="Stored report artifact list">
          <h3>{activeFamily.title} artifacts</h3>
          {activeFamily.reports.length === 0 ? (
            <EmptyState
              title="No Stored Reports"
              description="No stored reports returned for this family."
              variant="compact"
            />
          ) : null}
          {activeFamily.reports.map((report) => {
            const reportId = reportDisplayId(report);
            return (
              <button
                type="button"
                key={reportId}
                className={`report-artifact-card${selectedReport && reportDisplayId(selectedReport) === reportId ? " active" : ""}`}
                onClick={() => setSelectedReportId(reportId)}
              >
                <span className="badge stub">{text(report.research_status ?? "research_only")}</span>
                <strong>{primaryLabel(report)}</strong>
                <small className="mono">{reportId}</small>
                <small>Method: {reportMethodVersion(report)}</small>
              </button>
            );
          })}
        </section>

        <section className="report-detail-viewer" aria-label="Stored report detail viewer">
          {selectedReport ? (
            <article className="report-detail-card">
              <div className="report-detail-head">
                <div>
                  <span className="badge stub">{text(selectedReport.research_status ?? "research_only")}</span>
                  <h3>{primaryLabel(selectedReport)}</h3>
                  <p className="muted">Stored report detail from the selected governed artifact.</p>
                </div>
                <dl className="kv compact report-integrity-kv">
                  <dt>Report id</dt>
                  <dd className="mono">{reportDisplayId(selectedReport)}</dd>
                  <dt>Report hash</dt>
                  <dd className="mono">{text(selectedReport.report_hash)}</dd>
                  <dt>Method/version</dt>
                  <dd className="mono">{reportMethodVersion(selectedReport)}</dd>
                  <dt>Sample count</dt>
                  <dd className="mono">{text(selectedReport.sample_count)}</dd>
                </dl>
              </div>

              <div className="report-drilldown-stack" aria-label="Progressive report drilldowns">
                <details open>
                  <summary>Stored artifact fields</summary>
                  <dl className="kv compact">
                    <dt>Artifact type</dt>
                    <dd>{text(selectedReport.artifact_type)}</dd>
                    <dt>Economic context</dt>
                    <dd>{text(selectedReport.economic_usefulness ?? selectedReport.economic_meaning)}</dd>
                    <dt>Uncertainty</dt>
                    <dd>{uncertaintyText(selectedReport)}</dd>
                  </dl>
                </details>
                <details>
                  <summary>Source lineage and report integrity</summary>
                  <dl className="kv compact">
                    <dt>Source artifacts</dt>
                    <dd className="mono">{reportSourceIds(selectedReport).join(", ") || "No source artifact ids supplied"}</dd>
                    <dt>Input lineage</dt>
                    <dd><pre className="signal-json">{storedFieldJson(selectedReport.input_lineage)}</pre></dd>
                  </dl>
                </details>
                <details>
                  <summary>Limitations and stored payload</summary>
                  <div className="report-limitations-block">
                    <strong>Limitations</strong>
                    {Array.isArray(selectedReport.limitations) && selectedReport.limitations.length > 0 ? (
                      <ul>{selectedReport.limitations.map((item) => <li key={item}>{item}</li>)}</ul>
                    ) : (
                      <p className="muted">No limitations array supplied by this stored report.</p>
                    )}
                    <strong>Stored results</strong>
                    <pre className="signal-json">{storedFieldJson(selectedReport.results ?? selectedReport.metrics)}</pre>
                  </div>
                </details>
              </div>
            </article>
          ) : (
            <p className="muted" role="status">Select a stored report artifact.</p>
          )}
        </section>
      </div>
    </section>
  );
}

function verdictText(value: unknown): string {
  const record = asRecord(value);
  if (typeof record?.verdict === "string") return record.verdict;
  if (typeof record?.status === "string") return record.status;
  return text(value);
}

function firstValidationReport(bundle: InstitutionalIntelligenceBundle | null): InstitutionalReport | null {
  return bundle?.validation[0] ?? allReports(bundle)[0] ?? null;
}

function outcomeStatusText(report: InstitutionalReport | null): string {
  const status = asRecord(report?.["outcome_data_status"]);
  return verdictText(status ?? report?.research_status ?? null);
}

function scopeText(report: InstitutionalReport | null, analytics: AdvisoryAnalyticsResponse | null): string {
  const analyticsScope = analyticsRecord(analytics).included_scope;
  if (analyticsScope) return storedFieldJson(analyticsScope);
  const reportScope = report?.market_scope ?? report?.["included_scope"];
  if (reportScope) return storedFieldJson(reportScope);
  return "Stored scope not supplied by this read response";
}

export function ValidationEconomicIntegrityPanel({
  bundle,
  signals = [],
  analytics = null,
}: {
  bundle: InstitutionalIntelligenceBundle | null;
  signals?: AdvisorySignal[];
  analytics?: AdvisoryAnalyticsResponse | null;
}) {
  const report = firstValidationReport(bundle);
  const signal = signals[0] ?? null;
  const limitations = Array.isArray(report?.limitations) ? report.limitations : [];
  const sourceIds = report ? reportSourceIds(report) : [];
  const validationRows = [
    ["Report research status", text(report?.research_status)],
    ["Outcome status", outcomeStatusText(report)],
    ["Signal state reason", text(signal?.state_reason)],
    ["Calibration status", text(signal?.calibration_status)],
    ["Operating domain", text(signal?.operating_domain_status)],
    ["Freshness status", text(signal?.freshness_status)],
  ];
  const economicRows = [
    ["Signal economic verdict", text(signal?.economic_verdict)],
    ["Report economic usefulness", verdictText(report?.economic_usefulness)],
    ["Report economic meaning", verdictText(report?.economic_meaning)],
    ["Research status", text(report?.research_status)],
  ];

  return (
    <section className="panel span-12 validation-economic-integrity-panel" aria-label="Validation and economic-usefulness integrity panels">
      <div className="research-signal-panel-head">
        <div>
          <h2>Validation & Economic-Usefulness Integrity</h2>
          <p className="muted">
            Stored validation statuses and economic verdicts are displayed as supplied by existing
            reports and advisory records. The panel shows sample counts, source scope, and limitations
            next to those values so warning and not-assessed states remain visible.
          </p>
        </div>
        <div className="research-guardrail-card" role="note" aria-label="Verbatim verdict guardrail">
          <strong>Verbatim verdicts</strong>
          <span>Stored status · sample count · limitations</span>
        </div>
      </div>

      <div className="validation-economic-grid">
        <section className="validation-economic-card" aria-label="Stored validation statuses">
          <h3>Stored Validation Statuses</h3>
          <dl className="kv compact">
            {validationRows.map(([label, value]) => (
              <div className="kv-row" key={label}>
                <dt>{label}</dt>
                <dd className="mono">{value}</dd>
              </div>
            ))}
          </dl>
        </section>

        <section className="validation-economic-card" aria-label="Stored economic-usefulness verdicts">
          <h3>Stored Economic-Usefulness Verdicts</h3>
          <dl className="kv compact">
            {economicRows.map(([label, value]) => (
              <div className="kv-row" key={label}>
                <dt>{label}</dt>
                <dd className="mono">{value}</dd>
              </div>
            ))}
          </dl>
        </section>

        <section className="validation-economic-card span-all" aria-label="Validation scope sample counts and limitations">
          <h3>Scope, Sample Counts, and Limitations</h3>
          <dl className="kv compact">
            <dt>Sample count</dt>
            <dd className="mono">{text(report?.sample_count ?? analytics?.metrics?.[0]?.sample_count)}</dd>
            <dt>Uncertainty</dt>
            <dd>{report ? uncertaintyText(report) : "No validation report selected"}</dd>
            <dt>Source artifacts</dt>
            <dd className="mono">{sourceIds.length > 0 ? sourceIds.join(", ") : "No source artifact ids supplied"}</dd>
            <dt>Stored scope</dt>
            <dd><pre className="signal-json">{scopeText(report, analytics)}</pre></dd>
          </dl>
          <strong>Limitations</strong>
          {limitations.length > 0 ? (
            <ul className="scenario-limitations">{limitations.map((item) => <li key={item}>{item}</li>)}</ul>
          ) : (
            <p className="muted">No limitations array supplied by this stored report.</p>
          )}
        </section>
      </div>

      <p className="advisory-disclaimer" role="note">
        <strong>Research-only interpretation boundary.</strong> Validation and economic-usefulness
        values are not trading instructions, not financial advice, and not execution criteria. AXIOM
        displays the stored research record; the operator decides independently.
      </p>
    </section>
  );
}

function artifactIdsFromReports(bundle: InstitutionalIntelligenceBundle | null): string[] {
  const ids = new Set<string>();
  for (const report of allReports(bundle)) {
    ids.add(reportDisplayId(report));
    for (const sourceId of reportSourceIds(report)) ids.add(sourceId);
  }
  return [...ids].filter(Boolean).sort();
}

function analyticsSourceIds(analytics: AdvisoryAnalyticsResponse | null): string[] {
  return stringArrayField(analyticsRecord(analytics), "source_artifact_ids");
}

export function ResearchArtifactContextPanel({
  bundle,
  signals = [],
  analytics = null,
  researchManagement = null,
  journalEntries = [],
}: {
  bundle: InstitutionalIntelligenceBundle | null;
  signals?: AdvisorySignal[];
  analytics?: AdvisoryAnalyticsResponse | null;
  researchManagement?: ResearchManagementBundle | null;
  journalEntries?: ManualJournalEntry[];
}) {
  const reportIds = artifactIdsFromReports(bundle);
  const signalIds = signals.map((signal) => signal.signal_id);
  const analyticsIds = analyticsSourceIds(analytics);
  const collections = researchManagement?.collections ?? [];
  const members = researchManagement?.members ?? [];
  const tags = researchManagement?.tags ?? [];

  return (
    <section className="panel span-12 research-artifact-context-panel" aria-label="Read-only research artifact context">
      <div className="research-signal-panel-head">
        <div>
          <h2>Research Artifact Context</h2>
          <p className="muted">
            Existing collections, tags, journal references, report ids, signal ids, and source artifact
            ids are shown as read-only research context. Source artifacts stay in their governed stores;
            this phase does not persist saved views.
          </p>
        </div>
        <div className="research-guardrail-card" role="note" aria-label="Artifact context posture">
          <strong>Read-only context</strong>
          <span>Existing ids · tags · collections</span>
        </div>
      </div>

      <div className="research-artifact-grid">
        <section className="research-artifact-card" aria-label="Existing research collections">
          <h3>Collections</h3>
          {collections.length === 0 ? <p className="muted">No collections returned by the read API.</p> : null}
          {collections.map((collection) => (
            <article className="research-artifact-item" key={collection.collection_id}>
              <strong>{collection.name}</strong>
              <small className="mono">{collection.collection_id}</small>
              <small>{collection.description ?? "No description"}</small>
              <span className="badge stub">{collection.research_status}</span>
            </article>
          ))}
        </section>

        <section className="research-artifact-card" aria-label="Existing collection member references">
          <h3>Member References</h3>
          {members.length === 0 ? <p className="muted">No member references returned by the read API.</p> : null}
          {members.map((member) => (
            <article className="research-artifact-item" key={member.member_id}>
              <strong>{member.artifact_type}</strong>
              <small className="mono">{member.artifact_id}</small>
              <small className="mono">collection {member.collection_id}</small>
            </article>
          ))}
        </section>

        <section className="research-artifact-card" aria-label="Existing research tags">
          <h3>Tags</h3>
          {tags.length === 0 ? <p className="muted">No tags returned by the read API.</p> : null}
          {tags.map((tag) => (
            <article className="research-artifact-item" key={tag.tag_id}>
              <strong>{tag.tag}</strong>
              <small>{tag.artifact_type}</small>
              <small className="mono">{tag.artifact_id}</small>
            </article>
          ))}
        </section>

        <section className="research-artifact-card" aria-label="Journal references">
          <h3>Journal References</h3>
          {journalEntries.length === 0 ? <p className="muted">No journal references returned by the read API.</p> : null}
          {journalEntries.map((entry) => (
            <article className="research-artifact-item" key={entry.journal_id}>
              <strong>{entry.title}</strong>
              <small className="mono">{entry.journal_id}</small>
              <small>Signals: {entry.linked_signal_ids.join(", ") || "none"}</small>
              <small>Reports: {entry.linked_report_ids.join(", ") || "none"}</small>
            </article>
          ))}
        </section>

        <section className="research-artifact-card span-all" aria-label="Existing artifact id inventory">
          <h3>Artifact Id Inventory</h3>
          <dl className="kv compact">
            <dt>Report/source ids</dt>
            <dd className="mono">{reportIds.join(", ") || "No report ids returned"}</dd>
            <dt>Signal ids</dt>
            <dd className="mono">{signalIds.join(", ") || "No signal ids returned"}</dd>
            <dt>Analytics source ids</dt>
            <dd className="mono">{analyticsIds.join(", ") || "No analytics source ids supplied by current response"}</dd>
          </dl>
        </section>

        <section className="research-artifact-card span-all" aria-label="Saved view persistence absence">
          <h3>Saved View Preferences</h3>
          <p className="muted">
            Saved view persistence is not implemented in UI-004-P05. No preference row is written,
            no report body is copied, and no persistence proof is claimed for this phase.
          </p>
        </section>
      </div>
    </section>
  );
}

export function InstitutionalIntelligenceWorkspace({
  bundle,
  signals = [],
  analytics = null,
  researchManagement = null,
  journalEntries = [],
  loading = false,
  error = null,
  onRefresh,
}: DashboardProps) {
  const totalReports = useMemo(() => countReportRows(bundle), [bundle]);

  return (
    <>
      <div className="page-header">
        <div>
          <h1>Institutional Intelligence</h1>
          <p className="muted">
            Presentation-only research dashboard. AXIOM reads persisted intelligence reports and displays
            uncertainty, sample count, assumptions, limitations, and lineage without recomputing metrics in
            the browser.
          </p>
        </div>
        <button type="button" className="btn primary" onClick={onRefresh}>
          Refresh Research
        </button>
      </div>

      <section className="advisory-disclaimer" aria-label="Institutional intelligence disclaimer">
        <strong>Research context only.</strong> These reports are not financial advice, not a guarantee,
        not a prediction, and not an instruction. The operator decides independently; AXIOM does not act.
      </section>

      {error ? <ErrorBanner title="Institutional Intelligence Error" message={error} /> : null}
      {loading ? <Skeleton variant="rect" height="80px" aria-label="Loading institutional intelligence reports" /> : null}

      <ResearchWorkspaceFrame bundle={bundle} />
      <ResearchAdvisorySignalPanel signals={signals} loading={loading} error={error} />
      <ResearchPerformanceAnalyticsPanel analytics={analytics} loading={loading} error={error} />
      <IntelligenceReportViewer bundle={bundle} />
      <ValidationEconomicIntegrityPanel bundle={bundle} signals={signals} analytics={analytics} />
      <ResearchArtifactContextPanel
        bundle={bundle}
        signals={signals}
        analytics={analytics}
        researchManagement={researchManagement}
        journalEntries={journalEntries}
      />

      <Panel
        className="span-12"
        aria-label="Institutional intelligence summary"
        header={
          <PanelHeader
            title="Read-only Report Summary"
            subtitle={`Reports loaded: ${totalReports}. Each card is sourced from an authenticated read-only API and preserves persisted uncertainty and sample-count fields.`}
            headingLevel={2}
          />
        }
      >
        <p className="muted">
          Reports loaded: <span className="mono">{totalReports}</span>. Each card is sourced from an
          authenticated read-only API and preserves persisted uncertainty and sample-count fields.
        </p>
      </Panel>

      <div className="intelligence-section-grid">
        {SECTIONS.map((section) => (
          <ReportSection
            key={section.key}
            title={section.title}
            description={section.description}
            reports={bundle?.[section.key] ?? []}
          />
        ))}
      </div>

      <section data-ui008-mount="review-sub-panel" aria-label="Assistant Review Sub-Panel mount point">
        <AssistantReviewSubPanel />
      </section>

      <section data-ui008-mount="contextual-assistant-panel" aria-label="Contextual Assistant mount point">
        <ContextualAssistantPanel />
      </section>
    </>
  );
}

function ReportSection({
  title,
  description,
  reports,
}: {
  title: string;
  description: string;
  reports: InstitutionalReport[];
}) {
  return (
    <Panel
      className="intelligence-section"
      aria-label={title}
      header={
        <PanelHeader
          title={title}
          subtitle={description}
          headingLevel={2}
        />
      }
    >
      {reports.length === 0 ? <p className="muted">No reports returned.</p> : null}
      <div className="intelligence-card-list">
        {reports.map((report) => (
          <ReportCard key={report.id} report={report} />
        ))}
      </div>
    </Panel>
  );
}

function ReportCard({ report }: { report: InstitutionalReport }) {
  const limitations = Array.isArray(report.limitations) ? report.limitations : [];
  return (
    <article className="intelligence-card">
      <div className="intelligence-card-head">
        <h3>{primaryLabel(report)}</h3>
        <span className="badge stub">{text(report.research_status ?? "research_only")}</span>
      </div>
      <dl className="kv compact">
        <dt>Sample count</dt>
        <dd>{text(report.sample_count)}</dd>
        <dt>Uncertainty</dt>
        <dd>{uncertaintyText(report)}</dd>
        <dt>Economic context</dt>
        <dd>{text(report.economic_usefulness ?? report.economic_meaning)}</dd>
        <dt>Lineage</dt>
        <dd className="mono">{text(report.report_hash)}</dd>
      </dl>
      <Collapsible title="Evidence and limitations" defaultExpanded={false}>
        <pre className="signal-json">{JSON.stringify(sanitizeForDisplay({ limitations, results: report.results }), null, 2)}</pre>
      </Collapsible>
    </article>
  );
}

export function InstitutionalIntelligencePage() {
  const [bundle, setBundle] = useState<InstitutionalIntelligenceBundle | null>(null);
  const [signals, setSignals] = useState<AdvisorySignal[]>([]);
  const [analytics, setAnalytics] = useState<AdvisoryAnalyticsResponse | null>(null);
  const [researchManagement, setResearchManagement] = useState<ResearchManagementBundle | null>(null);
  const [journalEntries, setJournalEntries] = useState<ManualJournalEntry[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      const [nextBundle, nextSignals, nextAnalytics, nextResearchManagement, nextJournalEntries] = await Promise.all([
        fetchInstitutionalIntelligenceBundle(10),
        fetchAdvisorySignals({ limit: 25 }),
        fetchAdvisoryAnalytics(),
        fetchResearchManagementBundle(50),
        fetchJournalEntries(25),
      ]);
      setBundle(nextBundle);
      setSignals(nextSignals);
      setAnalytics(nextAnalytics);
      setResearchManagement(nextResearchManagement);
      setJournalEntries(nextJournalEntries);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load institutional research records");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void load();
  }, []);

  return (
    <InstitutionalIntelligenceWorkspace
      bundle={bundle}
      signals={signals}
      analytics={analytics}
      researchManagement={researchManagement}
      journalEntries={journalEntries}
      loading={loading}
      error={error}
      onRefresh={() => void load()}
    />
  );
}
