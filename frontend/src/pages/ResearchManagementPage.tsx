import { useEffect, useMemo, useState } from "react";
import {
  addResearchCollectionMember,
  createResearchCollection,
  createResearchTag,
  fetchAdvancedResearchReport,
  fetchAdvisorySignals,
  fetchChartResearchAnnotations,
  fetchExecutionResearchBundle,
  fetchInstitutionalIntelligenceBundle,
  fetchJournalEntries,
  fetchPortfolioResearchDashboard,
  fetchResearchManagementBundle,
  fetchScenarioReports,
  fetchTradePlans,
  removeResearchCollectionMember,
  type AdvancedResearchReport,
  type AdvisorySignal,
  type ChartResearchAnnotation,
  type ExecutionResearchBundle,
  type InstitutionalIntelligenceBundle,
  type InstitutionalReport,
  type ManualJournalEntry,
  type PortfolioResearchDashboard,
  type ResearchArtifactReferenceWrite,
  type ResearchCollection,
  type ResearchCollectionMember,
  type ResearchCollectionWrite,
  type ResearchTag,
  type ResearchTagWrite,
  type ScenarioReport,
  type TradePlanNote,
} from "../api/client";

export type ArtifactExplorerSource = {
  family: string;
  existingStore: string;
  existingReadSeam: string;
  p01Posture: string;
};

export const UI006_ARTIFACT_EXPLORER_SOURCES: ArtifactExplorerSource[] = [
  {
    family: "Advisory signals",
    existingStore: "W3 advisory signal records",
    existingReadSeam: "fetchAdvisorySignals / fetchAdvisorySignal",
    p01Posture: "Signal state, rationale, calibrated confidence, guardrails, and lineage as stored",
  },
  {
    family: "Intelligence reports",
    existingStore: "W4/W7 institutional report stores",
    existingReadSeam: "fetchInstitutionalIntelligenceBundle",
    p01Posture: "Correlation, regime, validation, economic, and report metadata as stored",
  },
  {
    family: "Scenario reports",
    existingStore: "W4 stored hypothetical scenario reports",
    existingReadSeam: "fetchScenarioReports / fetchScenarioReport",
    p01Posture: "Scenario assumptions, uncertainty, limitations, source ids, and hashes as stored",
  },
  {
    family: "Portfolio research",
    existingStore: "W7 hypothetical portfolio research dashboard/report preview",
    existingReadSeam: "fetchPortfolioResearchDashboard / fetchAdvancedResearchReport",
    p01Posture: "Included scope, source ids, limitations, and economic-usefulness values as stored",
  },
  {
    family: "Chart annotations",
    existingStore: "W5 chart research annotations",
    existingReadSeam: "fetchChartResearchAnnotations",
    p01Posture: "Chart context, source ids, uncertainty, and research status as stored",
  },
  {
    family: "Trade plans",
    existingStore: "W5 trade plan research notes",
    existingReadSeam: "fetchTradePlans",
    p01Posture: "Research-note metadata and linked artifact ids as stored",
  },
  {
    family: "Research journal",
    existingStore: "W5 manual research journal reflections",
    existingReadSeam: "fetchJournalEntries",
    p01Posture: "Reflection metadata, tags, and linked artifact ids as stored",
  },
  {
    family: "Execution research",
    existingStore: "W6 SIMULATED execution research artifacts",
    existingReadSeam: "fetchExecutionResearchBundle",
    p01Posture: "SIMULATED runs, fills, ledger, risk, experiments, and analytics metadata as stored",
  },
  {
    family: "Collections",
    existingStore: "W7 research_collections",
    existingReadSeam: "fetchResearchManagementBundle / fetchResearchCollections",
    p01Posture: "Collection metadata in existing W7 store; create-only organization row mutation authorized in P04",
  },
  {
    family: "Collection memberships",
    existingStore: "W7 research_collection_members",
    existingReadSeam: "fetchResearchManagementBundle",
    p01Posture: "Artifact type/id references in existing W7 store; add/remove reference-only mutation authorized in P04",
  },
  {
    family: "Tags",
    existingStore: "W7 research_tags",
    existingReadSeam: "fetchResearchManagementBundle / fetchResearchTags",
    p01Posture: "Tag labels and artifact type/id references in existing W7 store; create-only mutation authorized in P05",
  },
];

type CatalogEntry = {
  id: string;
  family: string;
  artifactType: string;
  label: string;
  status: string;
  methodVersion?: string;
  sampleCount?: number | string;
  storedVerdict?: string;
  storedConfidence?: string;
  uncertainty?: string;
  limitations: string[];
  sourceIds: string[];
  reportHash?: string;
  lineage: string[];
  organizationContext: string[];
  detailRows: Array<[string, string]>;
};

type ResearchManagementProps = {
  collections: ResearchCollection[];
  members: ResearchCollectionMember[];
  tags: ResearchTag[];
  artifacts: ScenarioReport[];
  signals?: AdvisorySignal[];
  intelligenceReports?: InstitutionalReport[];
  tradePlans?: TradePlanNote[];
  journalEntries?: ManualJournalEntry[];
  executionBundle?: ExecutionResearchBundle;
  portfolioDashboard?: PortfolioResearchDashboard | null;
  advancedReport?: AdvancedResearchReport | null;
  chartAnnotations?: ChartResearchAnnotation[];
  loading?: boolean;
  error?: string | null;
  onRefresh?: () => void;
  onCreateCollection?: (payload: ResearchCollectionWrite) => Promise<void> | void;
  onAddMember?: (collectionId: string, payload: ResearchArtifactReferenceWrite) => Promise<void> | void;
  onRemoveMember?: (collectionId: string, memberId: string) => Promise<void> | void;
  onCreateTag?: (payload: ResearchTagWrite) => Promise<void> | void;
};

const EMPTY_EXECUTION_BUNDLE: ExecutionResearchBundle = {
  runs: [],
  fills: [],
  ledger: [],
  riskReports: [],
  experiments: [],
  analyticsReports: [],
};

function textOrDash(value: string | null | undefined): string {
  return value && value.trim() ? value : "—";
}

const COLLECTION_WRITE_FIELDS = new Set(["name", "description"]);
const MEMBER_REFERENCE_FIELDS = new Set(["artifact_type", "artifact_id"]);
const TAG_WRITE_FIELDS = new Set(["artifact_type", "artifact_id", "tag"]);
const TAGGABLE_ARTIFACT_TYPES = new Set([
  "advisory_signal",
  "correlation_report",
  "regime_report",
  "scenario_report",
  "portfolio_risk_report",
  "signal_validation_report",
  "simulated_execution_run",
  "simulated_fill_event",
  "simulated_paper_ledger_entry",
  "execution_risk_research_report",
  "execution_research_experiment",
  "simulated_execution_analytics_report",
  "trade_plan_note",
  "manual_trade_journal_entry",
]);

export function assertCollectionOrganizationPayload(
  payload: Record<string, unknown>,
): ResearchCollectionWrite {
  const unknown = Object.keys(payload).filter((key) => !COLLECTION_WRITE_FIELDS.has(key));
  if (unknown.length > 0) {
    throw new Error(`COLLECTION_ORGANIZATION_FIELD_NOT_ALLOWED:${unknown.join(",")}`);
  }
  return payload as ResearchCollectionWrite;
}

export function assertMemberReferencePayload(
  payload: Record<string, unknown>,
): ResearchArtifactReferenceWrite {
  const unknown = Object.keys(payload).filter((key) => !MEMBER_REFERENCE_FIELDS.has(key));
  if (unknown.length > 0) {
    throw new Error(`MEMBER_REFERENCE_FIELD_NOT_ALLOWED:${unknown.join(",")}`);
  }
  return payload as ResearchArtifactReferenceWrite;
}


export function assertTagOrganizationPayload(payload: Record<string, unknown>): ResearchTagWrite {
  const unknown = Object.keys(payload).filter((key) => !TAG_WRITE_FIELDS.has(key));
  if (unknown.length > 0) {
    throw new Error(`TAG_ORGANIZATION_FIELD_NOT_ALLOWED:${unknown.join(",")}`);
  }
  return payload as ResearchTagWrite;
}

function asText(value: unknown): string {
  if (typeof value === "string" && value.trim()) return value;
  if (typeof value === "number" && Number.isFinite(value)) return String(value);
  if (typeof value === "boolean") return String(value);
  if (Array.isArray(value)) return `${value.length} items`;
  if (value && typeof value === "object") return "present";
  return "—";
}

function asPercent(value: number | null | undefined): string {
  return typeof value === "number" && Number.isFinite(value) ? `${(value * 100).toFixed(1)}%` : "—";
}

function objectValue(value: Record<string, unknown> | undefined, key: string): string {
  return value ? asText(value[key]) : "—";
}

function uncertaintyText(value: Record<string, unknown> | undefined): string {
  if (!value) return "—";
  const method = asText(value.method);
  const sample = asText(value.sample_count);
  const lower = asText(value.lower);
  const upper = asText(value.upper);
  return `${method} · n=${sample} · ${lower} to ${upper}`;
}

function compactList(values: Array<string | null | undefined>): string[] {
  return values.filter((value): value is string => Boolean(value && value.trim()));
}

function allReports(bundle: InstitutionalIntelligenceBundle | null): InstitutionalReport[] {
  if (!bundle) return [];
  return [
    ...bundle.relation,
    ...bundle.context,
    ...bundle.hypothetical,
    ...bundle.risk,
    ...bundle.validation,
  ];
}

function orgContextFor(entry: { id: string; artifactType: string }, members: ResearchCollectionMember[], tags: ResearchTag[]): string[] {
  const collectionRefs = members
    .filter((member) => member.artifact_id === entry.id || member.artifact_type === entry.artifactType)
    .map((member) => `collection:${member.collection_id}`);
  const tagRefs = tags
    .filter((tag) => tag.artifact_id === entry.id || tag.artifact_type === entry.artifactType)
    .map((tag) => `tag:${tag.tag}`);
  return [...collectionRefs, ...tagRefs];
}

function buildCatalogEntries({
  collections,
  members,
  tags,
  artifacts,
  signals = [],
  intelligenceReports = [],
  tradePlans = [],
  journalEntries = [],
  executionBundle = EMPTY_EXECUTION_BUNDLE,
  portfolioDashboard = null,
  advancedReport = null,
  chartAnnotations = [],
}: Required<Pick<ResearchManagementProps, "collections" | "members" | "tags" | "artifacts">> &
  Pick<
    ResearchManagementProps,
    | "signals"
    | "intelligenceReports"
    | "tradePlans"
    | "journalEntries"
    | "executionBundle"
    | "portfolioDashboard"
    | "advancedReport"
    | "chartAnnotations"
  >): CatalogEntry[] {
  const entries: CatalogEntry[] = [];

  for (const signal of signals) {
    entries.push({
      id: signal.signal_id,
      family: "Advisory signals",
      artifactType: "advisory_signal",
      label: `${signal.symbol} · ${signal.timeframe} · ${signal.signal_direction}`,
      status: signal.signal_state,
      methodVersion: signal.model_version,
      storedVerdict: signal.economic_verdict,
      storedConfidence: asPercent(signal.calibrated_confidence),
      uncertainty: signal.calibration_status,
      limitations: signal.eligibility_reasons,
      sourceIds: compactList([
        signal.statistical_report_id,
        signal.calibration_report_id,
        signal.economic_report_id,
        signal.generalization_report_id,
      ]),
      reportHash: signal.inference_input_hash,
      lineage: compactList([signal.model_artifact_id, signal.experiment_id, signal.feature_set_version]),
      organizationContext: orgContextFor({ id: signal.signal_id, artifactType: "advisory_signal" }, members, tags),
      detailRows: [
        ["State reason", signal.state_reason],
        ["Operating domain", signal.operating_domain_status],
        ["Freshness", textOrDash(signal.freshness_status)],
      ],
    });
  }

  for (const report of intelligenceReports) {
    const artifactType = asText(report.artifact_type || "institutional_report");
    entries.push({
      id: report.id,
      family: "Intelligence reports",
      artifactType,
      label: `${artifactType} · ${report.id}`,
      status: asText(report.research_status || "research_only"),
      methodVersion: asText(report.method_version),
      sampleCount: typeof report.sample_count === "number" ? report.sample_count : undefined,
      storedVerdict: objectValue(report.economic_usefulness, "verdict"),
      uncertainty: uncertaintyText(report.uncertainty),
      limitations: report.limitations ?? [],
      sourceIds: Array.isArray(report.source_artifact_ids) ? report.source_artifact_ids : [],
      reportHash: asText(report.report_hash),
      lineage: compactList([objectValue(report.input_lineage, "source")]),
      organizationContext: orgContextFor({ id: report.id, artifactType }, members, tags),
      detailRows: [
        ["Result fields", asText(report.results)],
        ["Input lineage", asText(report.input_lineage)],
      ],
    });
  }

  for (const scenario of artifacts) {
    entries.push({
      id: scenario.id,
      family: "Scenario reports",
      artifactType: scenario.artifact_type,
      label: scenario.scenario_name,
      status: scenario.research_status,
      methodVersion: scenario.method_version,
      sampleCount: scenario.sample_count,
      storedVerdict: objectValue(scenario.economic_usefulness, "verdict"),
      uncertainty: uncertaintyText(scenario.uncertainty),
      limitations: scenario.limitations,
      sourceIds: scenario.source_artifact_ids,
      reportHash: scenario.report_hash,
      lineage: compactList([objectValue(scenario.input_lineage, "input_policy"), objectValue(scenario.market_scope, "symbol")]),
      organizationContext: orgContextFor({ id: scenario.id, artifactType: scenario.artifact_type }, members, tags),
      detailRows: [
        ["Hypothetical result", asText(scenario.scenario_result.hypothetical_return ?? scenario.hypothetical_return)],
        ["Assumptions", asText(scenario.assumptions)],
        ["Scope", asText(scenario.market_scope)],
      ],
    });
  }

  if (portfolioDashboard) {
    entries.push({
      id: `portfolio-dashboard-${portfolioDashboard.operator_id}`,
      family: "Portfolio research",
      artifactType: "portfolio_research_dashboard",
      label: "Portfolio research dashboard",
      status: portfolioDashboard.research_status,
      sampleCount: portfolioDashboard.aggregate_cards.length,
      storedVerdict: objectValue(portfolioDashboard.economic_usefulness, "verdict"),
      uncertainty: portfolioDashboard.aggregate_cards.map((metric) => asText(metric.uncertainty.method)).join(", ") || "—",
      limitations: portfolioDashboard.limitations,
      sourceIds: portfolioDashboard.source_artifact_ids,
      lineage: compactList([objectValue(portfolioDashboard.included_scope, "policy")]),
      organizationContext: orgContextFor(
        { id: `portfolio-dashboard-${portfolioDashboard.operator_id}`, artifactType: "portfolio_research_dashboard" },
        members,
        tags,
      ),
      detailRows: [
        ["Included scope", asText(portfolioDashboard.included_scope)],
        ["Generated at", portfolioDashboard.generated_at],
      ],
    });
  }

  if (advancedReport) {
    entries.push({
      id: advancedReport.report_id,
      family: "Portfolio research",
      artifactType: "advanced_research_report",
      label: "Advanced research report preview",
      status: advancedReport.research_status,
      methodVersion: advancedReport.method_version,
      storedVerdict: objectValue(advancedReport.economic_usefulness, "verdict"),
      limitations: advancedReport.limitations,
      sourceIds: advancedReport.source_artifact_ids,
      reportHash: advancedReport.report_hash,
      lineage: compactList([asText(advancedReport.included_scope)]),
      organizationContext: orgContextFor({ id: advancedReport.report_id, artifactType: "advanced_research_report" }, members, tags),
      detailRows: [
        ["Persisted", String(advancedReport.persisted)],
        ["Sections", String(advancedReport.sections.length)],
      ],
    });
  }

  for (const annotation of chartAnnotations) {
    entries.push({
      id: annotation.id,
      family: "Chart annotations",
      artifactType: annotation.artifact_type,
      label: annotation.artifact_type,
      status: annotation.research_status,
      uncertainty: uncertaintyText(annotation.uncertainty),
      limitations: [],
      sourceIds: annotation.source_artifact_ids,
      lineage: compactList([objectValue(annotation.chart_context, "symbol"), objectValue(annotation.chart_context, "timeframe")]),
      organizationContext: orgContextFor({ id: annotation.id, artifactType: annotation.artifact_type }, members, tags),
      detailRows: [
        ["Chart context", asText(annotation.chart_context)],
        ["Provenance", asText(annotation.provenance)],
      ],
    });
  }

  for (const plan of tradePlans) {
    entries.push({
      id: plan.plan_id,
      family: "Trade plans",
      artifactType: "trade_plan_note",
      label: plan.title,
      status: plan.research_status,
      storedVerdict: plan.decision_status,
      limitations: compactList([plan.invalidating_conditions_text]),
      sourceIds: [...plan.linked_signal_ids, ...plan.linked_report_ids],
      lineage: compactList([plan.audit_correlation_id]),
      organizationContext: orgContextFor({ id: plan.plan_id, artifactType: "trade_plan_note" }, members, tags),
      detailRows: [
        ["Market context", plan.market_context],
        ["Hypothesis", plan.hypothesis],
      ],
    });
  }

  for (const journal of journalEntries) {
    entries.push({
      id: journal.journal_id,
      family: "Research journal",
      artifactType: "manual_research_journal",
      label: journal.title,
      status: journal.research_status,
      limitations: compactList([journal.lesson_notes]),
      sourceIds: compactList([journal.linked_plan_id, ...journal.linked_signal_ids, ...journal.linked_report_ids]),
      lineage: compactList([journal.audit_correlation_id]),
      organizationContext: orgContextFor({ id: journal.journal_id, artifactType: "manual_research_journal" }, members, tags),
      detailRows: [
        ["Reflection", journal.reflection_text],
        ["Process tags", journal.process_tags.join(", ") || "—"],
      ],
    });
  }

  for (const run of executionBundle.runs) {
    entries.push({
      id: run.run_id,
      family: "Execution research",
      artifactType: "simulated_execution_run",
      label: run.run_id,
      status: run.research_status,
      methodVersion: run.simulation_policy_version,
      storedVerdict: run.simulation_mode,
      limitations: run.limitations,
      sourceIds: run.input_artifact_ids,
      lineage: compactList([run.fill_model_name, run.fill_model_version]),
      organizationContext: orgContextFor({ id: run.run_id, artifactType: "simulated_execution_run" }, members, tags),
      detailRows: [
        ["Replay scope", asText(run.replay_scope)],
        ["Assumptions", asText(run.assumptions)],
      ],
    });
  }

  for (const risk of executionBundle.riskReports) {
    entries.push({
      id: risk.report_id,
      family: "Execution research",
      artifactType: "execution_risk_research_report",
      label: risk.report_id,
      status: risk.research_status,
      storedVerdict: objectValue(risk.economic_usefulness, "verdict"),
      uncertainty: uncertaintyText(risk.uncertainty),
      limitations: risk.limitations,
      sourceIds: risk.input_artifact_ids,
      lineage: compactList([risk.audit_correlation_id]),
      organizationContext: orgContextFor({ id: risk.report_id, artifactType: "execution_risk_research_report" }, members, tags),
      detailRows: [
        ["Request evidence", asText(risk.simulated_request_summary)],
        ["Risk metrics", asText(risk.risk_metrics)],
      ],
    });
  }

  for (const analytics of executionBundle.analyticsReports) {
    entries.push({
      id: analytics.report_id,
      family: "Execution research",
      artifactType: "simulated_execution_analytics_report",
      label: analytics.analytics_type,
      status: analytics.research_status,
      sampleCount: analytics.sample_count,
      storedVerdict: objectValue(analytics.economic_usefulness, "verdict"),
      uncertainty: uncertaintyText(analytics.uncertainty),
      limitations: analytics.limitations,
      sourceIds: analytics.source_artifact_ids,
      reportHash: analytics.report_hash,
      lineage: compactList([asText(analytics.included_scope)]),
      organizationContext: orgContextFor({ id: analytics.report_id, artifactType: "simulated_execution_analytics_report" }, members, tags),
      detailRows: [
        ["Metrics", asText(analytics.metrics)],
        ["Simulation mode", analytics.simulation_mode],
      ],
    });
  }

  for (const collection of collections) {
    entries.push({
      id: collection.collection_id,
      family: "Collections",
      artifactType: "research_collection",
      label: collection.name,
      status: collection.research_status,
      limitations: [],
      sourceIds: [],
      lineage: compactList([collection.audit_correlation_id]),
      organizationContext: [],
      detailRows: [["Description", textOrDash(collection.description)]],
    });
  }

  for (const member of members) {
    entries.push({
      id: member.member_id,
      family: "Collection memberships",
      artifactType: "research_collection_member",
      label: `${member.artifact_type} · ${member.artifact_id}`,
      status: "reference_only",
      limitations: [],
      sourceIds: [member.artifact_id],
      lineage: compactList([member.collection_id, member.audit_correlation_id]),
      organizationContext: [`collection:${member.collection_id}`],
      detailRows: [["Referenced artifact type", member.artifact_type]],
    });
  }

  for (const tag of tags) {
    entries.push({
      id: tag.tag_id,
      family: "Tags",
      artifactType: "research_tag",
      label: tag.tag,
      status: "reference_only",
      limitations: [],
      sourceIds: [tag.artifact_id],
      lineage: compactList([tag.audit_correlation_id]),
      organizationContext: [`tag:${tag.tag}`],
      detailRows: [["Referenced artifact type", tag.artifact_type]],
    });
  }

  return entries;
}

export function ArtifactExplorerFrame() {
  return (
    <section className="panel span-12 artifact-explorer-frame" aria-label="Unified artifact explorer frame">
      <div className="artifact-explorer-frame-head">
        <div>
          <h2>Unified Research Artifact Explorer</h2>
          <p className="muted">
            Centralized discovery over existing governed research artifacts and existing W7 research
            organization records. Completion posture: catalog, metadata, lineage, relationships, and
            filters are presentation-only; collection, membership, and tag controls are organization-only over existing stores.
          </p>
        </div>
        <div className="research-guardrail-card" role="note" aria-label="Artifact explorer guardrail">
          <strong>Gate CLOSED</strong>
          <span>Research-only · Existing /research-management route · Organization-only mutation</span>
        </div>
      </div>

      <div className="artifact-explorer-summary-grid" aria-label="Artifact explorer completion guardrails">
        <article className="research-overview-card">
          <span className="badge stub">Route posture</span>
          <strong className="mono">/research-management</strong>
          <small>Existing UI-001/UI-002 registered workspace; no new route or duplicate navigation.</small>
        </article>
        <article className="research-overview-card">
          <span className="badge stub">Organization controls</span>
          <strong>Organization-only</strong>
          <small>Collections, memberships, and tags use existing W7 stores; source artifact truth remains unchanged.</small>
        </article>
        <article className="research-overview-card">
          <span className="badge stub">Artifact truth</span>
          <strong>Verbatim</strong>
          <small>Stored statuses, verdicts, confidence, uncertainty, limitations, ids, and hashes are not altered.</small>
        </article>
      </div>
    </section>
  );
}

function ArtifactSourceInventory() {
  return (
    <section className="panel span-12 artifact-source-inventory" aria-label="UI-006 governed data-source inventory">
      <h2>Governed Data-Source Inventory</h2>
      <p className="muted">
        Every artifact family is mapped to an existing governed store and an existing read seam.
        Catalog detail below discloses stored metadata without changing organization records.
      </p>
      <div className="artifact-source-grid">
        {UI006_ARTIFACT_EXPLORER_SOURCES.map((item) => (
          <article className="artifact-source-card" key={item.family}>
            <span className="ix-metadata">{item.family}</span>
            <dl className="kv compact">
              <dt>Existing store</dt>
              <dd>{item.existingStore}</dd>
              <dt>Read seam</dt>
              <dd className="mono">{item.existingReadSeam}</dd>
              <dt>Current posture</dt>
              <dd>{item.p01Posture}</dd>
            </dl>
          </article>
        ))}
      </div>
    </section>
  );
}

function ArtifactCatalog({ entries }: { entries: CatalogEntry[] }) {
  const [selectedEntryId, setSelectedEntryId] = useState<string>(entries[0]?.id ?? "");
  const [familyFilter, setFamilyFilter] = useState("all");
  const [statusFilter, setStatusFilter] = useState("all");
  const [relationshipFilter, setRelationshipFilter] = useState("all");

  const familyOptions = useMemo(() => Array.from(new Set(entries.map((entry) => entry.family))).sort(), [entries]);
  const statusOptions = useMemo(() => Array.from(new Set(entries.map((entry) => entry.status))).sort(), [entries]);
  const relationshipOptions = useMemo(
    () => Array.from(new Set(entries.flatMap((entry) => entry.organizationContext))).sort(),
    [entries],
  );

  const filteredEntries = useMemo(
    () =>
      entries.filter((entry) => {
        const familyMatch = familyFilter === "all" || entry.family === familyFilter;
        const statusMatch = statusFilter === "all" || entry.status === statusFilter;
        const relationshipMatch =
          relationshipFilter === "all" || entry.organizationContext.includes(relationshipFilter);
        return familyMatch && statusMatch && relationshipMatch;
      }),
    [entries, familyFilter, relationshipFilter, statusFilter],
  );

  const selectedEntry = useMemo(
    () =>
      filteredEntries.find((entry) => entry.id === selectedEntryId) ?? filteredEntries[0] ?? null,
    [filteredEntries, selectedEntryId],
  );

  useEffect(() => {
    if (!selectedEntryId && filteredEntries[0]) {
      setSelectedEntryId(filteredEntries[0].id);
    } else if (selectedEntryId && !filteredEntries.some((entry) => entry.id === selectedEntryId)) {
      setSelectedEntryId(filteredEntries[0]?.id ?? "");
    }
  }, [filteredEntries, selectedEntryId]);

  return (
    <section className="panel span-12 artifact-catalog-panel" aria-label="Unified artifact catalog lineage relationships and filters">
      <h2>Unified Artifact Catalog</h2>
      <p className="muted">
        Read-only catalog rows disclose stored metadata, lineage, and explicit relationship references.
        Filters are temporary presentation state and do not change artifacts or organization records.
      </p>

      <div className="artifact-filter-panel" aria-label="In-memory artifact filters">
        <label className="field-inline">
          <span>Family</span>
          <select value={familyFilter} onChange={(event) => setFamilyFilter(event.target.value)}>
            <option value="all">All families</option>
            {familyOptions.map((family) => (
              <option key={family} value={family}>{family}</option>
            ))}
          </select>
        </label>
        <label className="field-inline">
          <span>Status</span>
          <select value={statusFilter} onChange={(event) => setStatusFilter(event.target.value)}>
            <option value="all">All statuses</option>
            {statusOptions.map((status) => (
              <option key={status} value={status}>{status}</option>
            ))}
          </select>
        </label>
        <label className="field-inline">
          <span>Stored relationship</span>
          <select
            value={relationshipFilter}
            onChange={(event) => setRelationshipFilter(event.target.value)}
          >
            <option value="all">All stored references</option>
            {relationshipOptions.map((relationship) => (
              <option key={relationship} value={relationship}>{relationship}</option>
            ))}
          </select>
        </label>
        <p className="muted" role="note">
          In-memory only: the filtered view is a presentation subset and never a full-scope analytical claim.
        </p>
      </div>

      <section className="artifact-filter-summary" aria-label="Filtered view scope notice">
        <span className="badge stub">No cherry-picking</span>
        <p className="muted">
          Showing {filteredEntries.length} of {entries.length} catalog rows. Metadata detail preserves stored
          scope, sample count, uncertainty, limitations, source ids, lineage, and hashes for the selected row.
        </p>
      </section>

      <div className="artifact-catalog-layout">
        <div className="artifact-catalog-list" aria-label="Read-only unified artifact catalog">
          {filteredEntries.length === 0 ? <p className="muted">No artifact metadata matches these filters.</p> : null}
          {filteredEntries.map((entry) => (
            <button
              key={`${entry.family}-${entry.id}`}
              type="button"
              className={`artifact-catalog-card${selectedEntry?.id === entry.id ? " active" : ""}`}
              onClick={() => setSelectedEntryId(entry.id)}
            >
              <span className="badge stub">{entry.family}</span>
              <strong>{entry.label}</strong>
              <small>{entry.artifactType} · {entry.status}</small>
              <small className="mono">{entry.id}</small>
            </button>
          ))}
        </div>

        <article className="artifact-detail-card" aria-label="Read-only artifact metadata detail">
          {selectedEntry ? <ArtifactMetadataDetail entry={selectedEntry} /> : <p className="muted">Select an artifact.</p>}
        </article>
      </div>
    </section>
  );
}

function CollectionMembershipOrganizationPanel({
  collections,
  catalogEntries,
  members,
  onCreateCollection,
  onAddMember,
  onRemoveMember,
}: {
  collections: ResearchCollection[];
  catalogEntries: CatalogEntry[];
  members: ResearchCollectionMember[];
  onCreateCollection?: (payload: ResearchCollectionWrite) => Promise<void> | void;
  onAddMember?: (collectionId: string, payload: ResearchArtifactReferenceWrite) => Promise<void> | void;
  onRemoveMember?: (collectionId: string, memberId: string) => Promise<void> | void;
}) {
  const [collectionName, setCollectionName] = useState("Artifact review set");
  const [collectionDescription, setCollectionDescription] = useState(
    "Reference-only grouping of governed research artifacts.",
  );
  const [selectedCollectionId, setSelectedCollectionId] = useState(collections[0]?.collection_id ?? "");
  const [selectedArtifactKey, setSelectedArtifactKey] = useState(
    catalogEntries[0] ? `${catalogEntries[0].artifactType}::${catalogEntries[0].id}` : "",
  );

  useEffect(() => {
    if (!selectedCollectionId && collections[0]) {
      setSelectedCollectionId(collections[0].collection_id);
    }
  }, [collections, selectedCollectionId]);

  useEffect(() => {
    if (!selectedArtifactKey && catalogEntries[0]) {
      setSelectedArtifactKey(`${catalogEntries[0].artifactType}::${catalogEntries[0].id}`);
    }
  }, [catalogEntries, selectedArtifactKey]);

  const selectedCollection =
    collections.find((collection) => collection.collection_id === selectedCollectionId) ??
    collections[0] ??
    null;
  const selectedArtifact =
    catalogEntries.find((entry) => `${entry.artifactType}::${entry.id}` === selectedArtifactKey) ??
    catalogEntries[0] ??
    null;
  const selectedCollectionMembers = selectedCollection
    ? members.filter((member) => member.collection_id === selectedCollection.collection_id)
    : [];
  const canMutate = Boolean(onCreateCollection || onAddMember || onRemoveMember);

  if (!canMutate) {
    return null;
  }

  function collectionPayload(): ResearchCollectionWrite {
    return assertCollectionOrganizationPayload({
      name: collectionName,
      description: collectionDescription,
    });
  }

  function memberPayload(): ResearchArtifactReferenceWrite {
    return assertMemberReferencePayload({
      artifact_type: selectedArtifact?.artifactType ?? "",
      artifact_id: selectedArtifact?.id ?? "",
    });
  }

  return (
    <section className="panel span-12 artifact-organization-mutation" aria-label="Collection membership organization controls">
      <h2>Collection Organization Controls</h2>
      <p className="muted">
        Organization-only mutation over existing W7 research-management stores. Collection rows store
        names and descriptions; membership rows store artifact type/id references only. Source artifact
        metadata remains unchanged.
      </p>
      <div className="artifact-mutation-grid">
        <article className="research-artifact-card" aria-label="Create research collection organization record">
          <h3>Create collection</h3>
          <label className="field">
            <span>Collection name</span>
            <input value={collectionName} onChange={(event) => setCollectionName(event.target.value)} />
          </label>
          <label className="field">
            <span>Description</span>
            <textarea
              value={collectionDescription}
              onChange={(event) => setCollectionDescription(event.target.value)}
            />
          </label>
          <button
            type="button"
            className="btn primary"
            onClick={() => void onCreateCollection?.(collectionPayload())}
          >
            Save collection record
          </button>
        </article>

        <article className="research-artifact-card" aria-label="Add artifact reference to collection">
          <h3>Add artifact reference</h3>
          <label className="field">
            <span>Target collection</span>
            <select
              value={selectedCollection?.collection_id ?? ""}
              onChange={(event) => setSelectedCollectionId(event.target.value)}
            >
              {collections.map((collection) => (
                <option key={collection.collection_id} value={collection.collection_id}>
                  {collection.name}
                </option>
              ))}
            </select>
          </label>
          <label className="field">
            <span>Artifact reference</span>
            <select
              value={selectedArtifact ? `${selectedArtifact.artifactType}::${selectedArtifact.id}` : ""}
              onChange={(event) => setSelectedArtifactKey(event.target.value)}
            >
              {catalogEntries.map((entry) => (
                <option key={`${entry.artifactType}-${entry.id}`} value={`${entry.artifactType}::${entry.id}`}>
                  {entry.artifactType} · {entry.label}
                </option>
              ))}
            </select>
          </label>
          <dl className="kv compact">
            <dt>Artifact type</dt>
            <dd>{selectedArtifact?.artifactType ?? "—"}</dd>
            <dt>Artifact id</dt>
            <dd className="mono">{selectedArtifact?.id ?? "—"}</dd>
          </dl>
          <button
            type="button"
            className="btn"
            disabled={!selectedCollection || !selectedArtifact}
            onClick={() => {
              if (selectedCollection && selectedArtifact) {
                void onAddMember?.(selectedCollection.collection_id, memberPayload());
              }
            }}
          >
            Add reference
          </button>
        </article>

        <article className="research-artifact-card" aria-label="Collection member reference removal">
          <h3>Existing member references</h3>
          <p className="muted">Removal detaches the reference row only; it does not alter the source artifact.</p>
          {selectedCollectionMembers.length === 0 ? <p className="muted">No references in selected collection.</p> : null}
          {selectedCollectionMembers.map((member) => (
            <div className="research-artifact-item" key={member.member_id}>
              <strong>{member.artifact_type}</strong>
              <small className="mono">{member.artifact_id}</small>
              <button
                type="button"
                className="btn"
                onClick={() => void onRemoveMember?.(member.collection_id, member.member_id)}
              >
                Remove reference
              </button>
            </div>
          ))}
        </article>
      </div>
    </section>
  );
}


function ArtifactMetadataDetail({ entry }: { entry: CatalogEntry }) {
  return (
    <>
      <header>
        <span className="badge stub">{entry.family}</span>
        <h3>{entry.label}</h3>
        <p className="muted">Stored metadata is rendered verbatim from existing read responses.</p>
      </header>
      <dl className="kv compact">
        <dt>Artifact id</dt>
        <dd className="mono">{entry.id}</dd>
        <dt>Artifact type</dt>
        <dd>{entry.artifactType}</dd>
        <dt>Status</dt>
        <dd>{entry.status}</dd>
        <dt>Method/version</dt>
        <dd>{entry.methodVersion ?? "—"}</dd>
        <dt>Sample count</dt>
        <dd>{entry.sampleCount ?? "—"}</dd>
        <dt>Stored verdict</dt>
        <dd>{entry.storedVerdict ?? "—"}</dd>
        <dt>Stored confidence</dt>
        <dd>{entry.storedConfidence ?? "—"}</dd>
        <dt>Uncertainty</dt>
        <dd>{entry.uncertainty ?? "—"}</dd>
        <dt>Report hash</dt>
        <dd className="mono">{entry.reportHash ?? "—"}</dd>
      </dl>
      <section>
        <h4>Source ids</h4>
        <p className="mono">{entry.sourceIds.join(", ") || "—"}</p>
      </section>
      <section>
        <h4>Stored lineage</h4>
        <p className="mono">{entry.lineage.join(", ") || "—"}</p>
      </section>
      <section>
        <h4>Scope, samples, uncertainty, limitations</h4>
        <ul className="scenario-limitations">
          {(entry.limitations.length ? entry.limitations : ["not supplied"]).map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </section>
      <section>
        <h4>Stored relationships</h4>
        <p className="mono">{entry.organizationContext.join(", ") || "—"}</p>
      </section>
      <section>
        <h4>Stored detail fields</h4>
        <dl className="kv compact">
          {entry.detailRows.map(([key, value]) => (
            <div className="kv-row" key={key}>
              <dt>{key}</dt>
              <dd>{value}</dd>
            </div>
          ))}
        </dl>
      </section>
    </>
  );
}

function TagOrganizationPanel({
  catalogEntries,
  onCreateTag,
}: {
  catalogEntries: CatalogEntry[];
  onCreateTag?: (payload: ResearchTagWrite) => Promise<void> | void;
}) {
  const taggableEntries = useMemo(
    () => catalogEntries.filter((entry) => TAGGABLE_ARTIFACT_TYPES.has(entry.artifactType)),
    [catalogEntries],
  );
  const [tagText, setTagText] = useState("artifact-review");
  const [selectedArtifactKey, setSelectedArtifactKey] = useState(
    taggableEntries[0] ? `${taggableEntries[0].artifactType}::${taggableEntries[0].id}` : "",
  );

  useEffect(() => {
    if (!selectedArtifactKey && taggableEntries[0]) {
      setSelectedArtifactKey(`${taggableEntries[0].artifactType}::${taggableEntries[0].id}`);
    }
  }, [selectedArtifactKey, taggableEntries]);

  const selectedArtifact =
    taggableEntries.find((entry) => `${entry.artifactType}::${entry.id}` === selectedArtifactKey) ??
    taggableEntries[0] ??
    null;

  if (!onCreateTag) {
    return null;
  }

  function tagPayload(): ResearchTagWrite {
    return assertTagOrganizationPayload({
      artifact_type: selectedArtifact?.artifactType ?? "",
      artifact_id: selectedArtifact?.id ?? "",
      tag: tagText,
    });
  }

  return (
    <section className="panel span-12 artifact-organization-mutation" aria-label="Tag organization controls">
      <h2>Tag Organization Controls</h2>
      <p className="muted">
        Organization-only tag creation over the existing W7 research tag store. Tag rows store a label
        and an artifact type/id reference only. Tag deletion is not implemented in this phase.
      </p>
      <div className="artifact-mutation-grid">
        <article className="research-artifact-card" aria-label="Create artifact tag organization record">
          <h3>Create tag</h3>
          <label className="field">
            <span>Tag label</span>
            <input value={tagText} onChange={(event) => setTagText(event.target.value)} />
          </label>
          <label className="field">
            <span>Artifact reference</span>
            <select
              value={selectedArtifact ? `${selectedArtifact.artifactType}::${selectedArtifact.id}` : ""}
              onChange={(event) => setSelectedArtifactKey(event.target.value)}
            >
              {taggableEntries.map((entry) => (
                <option key={`${entry.artifactType}-${entry.id}`} value={`${entry.artifactType}::${entry.id}`}>
                  {entry.artifactType} · {entry.label}
                </option>
              ))}
            </select>
          </label>
          <dl className="kv compact">
            <dt>Artifact type</dt>
            <dd>{selectedArtifact?.artifactType ?? "—"}</dd>
            <dt>Artifact id</dt>
            <dd className="mono">{selectedArtifact?.id ?? "—"}</dd>
          </dl>
          <button
            type="button"
            className="btn primary"
            disabled={!selectedArtifact}
            onClick={() => {
              if (selectedArtifact) {
                void onCreateTag(tagPayload());
              }
            }}
          >
            Save tag record
          </button>
        </article>
      </div>
    </section>
  );
}


function OrganizationPreview({
  collections,
  members,
  tags,
}: {
  collections: ResearchCollection[];
  members: ResearchCollectionMember[];
  tags: ResearchTag[];
}) {
  return (
    <section className="panel span-12" aria-label="Read-only organization preview">
      <h2>Existing Research Organization Records</h2>
      <p className="muted">
        Read-only preview of existing W7 collections, membership references, and tags. Organization
        changes are limited to the audited controls above and persist only reference rows in existing W7 stores.
      </p>
      <div className="artifact-organization-grid">
        <article className="research-artifact-card" aria-label="Read-only collections preview">
          <h3>Collections</h3>
          {collections.length === 0 ? <p className="muted">No collections returned for this operator.</p> : null}
          {collections.slice(0, 3).map((collection) => (
            <div className="research-artifact-item" key={collection.collection_id}>
              <span className="badge stub">{collection.research_status}</span>
              <strong>{collection.name}</strong>
              <small>{textOrDash(collection.description)}</small>
              <small className="mono">{collection.collection_id}</small>
            </div>
          ))}
        </article>
        <article className="research-artifact-card" aria-label="Read-only membership preview">
          <h3>Membership references</h3>
          {members.length === 0 ? <p className="muted">No membership references returned.</p> : null}
          {members.slice(0, 3).map((member) => (
            <div className="research-artifact-item" key={member.member_id}>
              <strong>{member.artifact_type}</strong>
              <small className="mono">{member.artifact_id}</small>
              <small className="mono">collection {member.collection_id}</small>
            </div>
          ))}
        </article>
        <article className="research-artifact-card" aria-label="Read-only tags preview">
          <h3>Tags</h3>
          {tags.length === 0 ? <p className="muted">No tags returned.</p> : null}
          {tags.slice(0, 4).map((tag) => (
            <div className="research-artifact-item" key={tag.tag_id}>
              <strong>{tag.tag}</strong>
              <small>{tag.artifact_type}</small>
              <small className="mono">{tag.artifact_id}</small>
            </div>
          ))}
        </article>
      </div>
    </section>
  );
}

export function ResearchManagementWorkspace({
  collections,
  members,
  tags,
  artifacts,
  signals = [],
  intelligenceReports = [],
  tradePlans = [],
  journalEntries = [],
  executionBundle = EMPTY_EXECUTION_BUNDLE,
  portfolioDashboard = null,
  advancedReport = null,
  chartAnnotations = [],
  loading = false,
  error = null,
  onRefresh,
  onCreateCollection,
  onAddMember,
  onRemoveMember,
  onCreateTag,
}: ResearchManagementProps) {
  const catalogEntries = useMemo(
    () =>
      buildCatalogEntries({
        collections,
        members,
        tags,
        artifacts,
        signals,
        intelligenceReports,
        tradePlans,
        journalEntries,
        executionBundle,
        portfolioDashboard,
        advancedReport,
        chartAnnotations,
      }),
    [
      advancedReport,
      artifacts,
      chartAnnotations,
      collections,
      executionBundle,
      intelligenceReports,
      journalEntries,
      members,
      portfolioDashboard,
      signals,
      tags,
      tradePlans,
    ],
  );

  const counts = useMemo(
    () => [
      ["Catalog artifacts", catalogEntries.length],
      ["Collections", collections.length],
      ["Membership references", members.length],
      ["Tags", tags.length],
    ],
    [catalogEntries.length, collections.length, members.length, tags.length],
  );

  return (
    <>
      <div className="page-header">
        <div>
          <h1>Unified Research Artifact Explorer</h1>
          <p className="muted">
            Catalog, metadata detail, stored lineage, explicit relationships, temporary in-memory filters,
            and organization-only collection/membership/tag controls on the existing Research Management workspace.
          </p>
        </div>
        <button type="button" className="btn primary" onClick={onRefresh}>
          Refresh Explorer Sources
        </button>
      </div>

      <section className="advisory-disclaimer" aria-label="Unified artifact explorer disclaimer">
        <strong>Research-only artifact discovery.</strong> This completed UI-006 explorer reads existing artifact metadata,
        stored lineage, and explicit relationship references; organization controls write reference rows only.
        Filters are temporary in-memory presentation controls. AXIOM does not act.
      </section>

      {error ? <p className="error-text">{error}</p> : null}
      {loading ? <p className="muted">Loading unified artifact catalog sources…</p> : null}

      <ArtifactExplorerFrame />

      <section className="panel span-12" aria-label="Artifact explorer source counts">
        <h2>Current Source Counts</h2>
        <div className="artifact-explorer-summary-grid">
          {counts.map(([label, count]) => (
            <article className="research-overview-card" key={label}>
              <h3>{label}</h3>
              <strong>{count}</strong>
              <small>Presentation count from existing read responses.</small>
            </article>
          ))}
        </div>
      </section>

      <ArtifactSourceInventory />
      <ArtifactCatalog entries={catalogEntries} />
      <CollectionMembershipOrganizationPanel
        collections={collections}
        catalogEntries={catalogEntries}
        members={members}
        onCreateCollection={onCreateCollection}
        onAddMember={onAddMember}
        onRemoveMember={onRemoveMember}
      />
      <TagOrganizationPanel catalogEntries={catalogEntries} onCreateTag={onCreateTag} />
      <OrganizationPreview collections={collections} members={members} tags={tags} />
    </>
  );
}

export function ResearchManagementPage() {
  const [collections, setCollections] = useState<ResearchCollection[]>([]);
  const [members, setMembers] = useState<ResearchCollectionMember[]>([]);
  const [tags, setTags] = useState<ResearchTag[]>([]);
  const [artifacts, setArtifacts] = useState<ScenarioReport[]>([]);
  const [signals, setSignals] = useState<AdvisorySignal[]>([]);
  const [intelligenceReports, setIntelligenceReports] = useState<InstitutionalReport[]>([]);
  const [tradePlans, setTradePlans] = useState<TradePlanNote[]>([]);
  const [journalEntries, setJournalEntries] = useState<ManualJournalEntry[]>([]);
  const [executionBundle, setExecutionBundle] = useState<ExecutionResearchBundle>(EMPTY_EXECUTION_BUNDLE);
  const [portfolioDashboard, setPortfolioDashboard] = useState<PortfolioResearchDashboard | null>(null);
  const [advancedReport, setAdvancedReport] = useState<AdvancedResearchReport | null>(null);
  const [chartAnnotations, setChartAnnotations] = useState<ChartResearchAnnotation[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      const [
        bundle,
        scenarioReports,
        signalRows,
        intelligenceBundle,
        tradePlanRows,
        journalRows,
        executionRows,
        portfolioRows,
        advancedRows,
        annotationRows,
      ] = await Promise.all([
        fetchResearchManagementBundle(50),
        fetchScenarioReports(25),
        fetchAdvisorySignals({ limit: 25 }),
        fetchInstitutionalIntelligenceBundle(5),
        fetchTradePlans(25),
        fetchJournalEntries(25),
        fetchExecutionResearchBundle(25),
        fetchPortfolioResearchDashboard(),
        fetchAdvancedResearchReport(),
        fetchChartResearchAnnotations({ limit: 25 }),
      ]);
      setCollections(bundle.collections);
      setMembers(bundle.members);
      setTags(bundle.tags);
      setArtifacts(scenarioReports);
      setSignals(signalRows);
      setIntelligenceReports(allReports(intelligenceBundle));
      setTradePlans(tradePlanRows);
      setJournalEntries(journalRows);
      setExecutionBundle(executionRows);
      setPortfolioDashboard(portfolioRows);
      setAdvancedReport(advancedRows);
      setChartAnnotations(annotationRows);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load research artifact catalog sources");
    } finally {
      setLoading(false);
    }
  }

  async function createCollection(payload: ResearchCollectionWrite) {
    setError(null);
    try {
      const created = await createResearchCollection(payload);
      setCollections((current) => [created, ...current]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save collection record");
    }
  }

  async function addMember(collectionId: string, payload: ResearchArtifactReferenceWrite) {
    setError(null);
    try {
      const created = await addResearchCollectionMember(collectionId, payload);
      setMembers((current) => [created, ...current]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to add artifact reference");
    }
  }

  async function removeMember(collectionId: string, memberId: string) {
    setError(null);
    try {
      await removeResearchCollectionMember(collectionId, memberId);
      setMembers((current) => current.filter((member) => member.member_id !== memberId));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to remove artifact reference");
    }
  }

  async function createTag(payload: ResearchTagWrite) {
    setError(null);
    try {
      const created = await createResearchTag(payload);
      setTags((current) => [created, ...current]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save tag record");
    }
  }

  useEffect(() => {
    void load();
  }, []);

  return (
    <ResearchManagementWorkspace
      collections={collections}
      members={members}
      tags={tags}
      artifacts={artifacts}
      signals={signals}
      intelligenceReports={intelligenceReports}
      tradePlans={tradePlans}
      journalEntries={journalEntries}
      executionBundle={executionBundle}
      portfolioDashboard={portfolioDashboard}
      advancedReport={advancedReport}
      chartAnnotations={chartAnnotations}
      loading={loading}
      error={error}
      onCreateCollection={(payload) => void createCollection(payload)}
      onAddMember={(collectionId, payload) => void addMember(collectionId, payload)}
      onRemoveMember={(collectionId, memberId) => void removeMember(collectionId, memberId)}
      onCreateTag={(payload) => void createTag(payload)}
      onRefresh={() => void load()}
    />
  );
}
