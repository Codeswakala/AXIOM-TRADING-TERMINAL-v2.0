/**
 * SignalInvestigationRecords (UI-CONV-P03 item 6)
 *
 * Relocated from pages/SignalInvestigationPage.tsx (deleted this cycle):
 *   - INVESTIGATION_DISCLAIMER, EMPTY_INTELLIGENCE, REPORT_GROUPS
 *   - InvestigationPlanningDataSource + UI005_INVESTIGATION_PLANNING_SOURCES
 *   - InvestigationPlanningFrame (workflow frame over existing surfaces)
 *   - reportTitle / reportSummary / safeSummaryValue / formatDate helpers
 *
 * SignalInvestigationFrame is the re-homed home of the page's workspace chrome
 * (h1 heading, read-only paragraph, disclaimer, planning frame) — rendered
 * inside the terminal's expanded signal card so the investigation surface
 * lives exactly once (BUILD_DIRECTIVE_UI-CONV-P03_ITEM6 §2: extend, do not
 * duplicate). Sections 2-7 (persisted signals, detail, rationale, guardrails,
 * lineage, explainability) already exist in the dock card and are NOT
 * rebuilt here. The "Investigation reads persisted evidence only." paragraph
 * from the page's detail header is carried into the frame so the wording
 * survives verbatim.
 */

import type { InstitutionalIntelligenceBundle, InstitutionalReport } from "../../../api/client";
import { Panel, PanelHeader } from "../../ui";

export const INVESTIGATION_DISCLAIMER =
  "Signal investigation is research review only — not financial advice, not a trade instruction, not a signal mutation, and not an action surface. Operator judgment required. AXIOM does not act.";

export const EMPTY_INTELLIGENCE: InstitutionalIntelligenceBundle = {
  relation: [],
  context: [],
  hypothetical: [],
  risk: [],
  validation: [],
};

export const REPORT_GROUPS: Array<[keyof InstitutionalIntelligenceBundle, string]> = [
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
    existingRoute: "/?view=execution",
    existingStore: "W6 SIMULATED execution research artifacts",
    existingReadSeam: "fetchSimulatedRunsList / fetchSimulatedRunFills / detail seams for ledger, risk, experiments, analytics",
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

export function formatDate(value: string | null): string {
  if (!value) return "—";
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return value;
  return parsed.toISOString();
}

export function reportTitle(report: InstitutionalReport): string {
  const type = typeof report.artifact_type === "string" ? report.artifact_type : "research_report";
  return `${type.replace(/_/g, " ")} · ${report.id}`;
}

export function reportSummary(report: InstitutionalReport): string {
  const status = typeof report.research_status === "string" ? report.research_status : "research_only";
  const samples = typeof report.sample_count === "number" ? `n=${report.sample_count}` : "n=—";
  return `${status} · ${samples}`;
}

export function safeSummaryValue(value: unknown): string {
  if (typeof value === "string") return value;
  if (typeof value === "number" || typeof value === "boolean") return String(value);
  if (value == null) return "—";
  return "present";
}

export function InvestigationPlanningFrame() {
  return (
    <Panel
      className="span-12 investigation-planning-frame"
      aria-label="Investigation and planning workspace frame"
      data-testid="investigation-planning-frame"
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
      <div
        className="investigation-source-grid"
        aria-label="UI-005 governed data-source inventory"
        data-testid="investigation-sources-inventory"
      >
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

/**
 * SignalInvestigationFrame — the re-homed workspace chrome (group 1).
 * Rendered inside the expanded signal card (the single investigation home)
 * and importable directly by the regression suites.
 */
export function SignalInvestigationFrame() {
  return (
    <div className="signal-investigation-frame" data-testid="signal-investigation-frame">
      <h1>Signal Investigation Workspace</h1>
      <p className="muted">
        Read-only investigation of persisted advisory signal rationale, guardrails, lineage,
        and linked intelligence reports. Presentation-only: no client-side inference, no
        guardrail override, no signal mutation, and no browser-side analytics rerun.
      </p>
      <p className="muted">
        Investigation reads persisted evidence only. It does not change this signal, rerun the
        model, alter guardrails, or create an instruction.
      </p>
      <section className="advisory-disclaimer" aria-label="Signal investigation disclaimer">
        <strong>Research investigation only.</strong> {INVESTIGATION_DISCLAIMER}
      </section>
      <InvestigationPlanningFrame />
    </div>
  );
}
