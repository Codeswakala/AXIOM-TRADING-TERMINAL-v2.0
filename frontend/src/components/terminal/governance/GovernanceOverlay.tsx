/**
 * GovernanceOverlay (UI-CONV-P03 item 5)
 *
 * Re-homed home of GovernanceEvidencePage: a shell-owned governance overlay
 * in the overlay layer (the item-3 settings pattern), reachable from
 *   - the left module rail (its Govern launcher navigates to /governance),
 *   - the legacy route /governance (redirect, never 404 — R2),
 *   - the deep link /?open=governance.
 *
 * Home reasoning (BUILD_DIRECTIVE_UI-CONV-P03_ITEM5 §4):
 *   - NOT the right dock (320 px) or a bottom-dock tab: 1,072-line
 *     constitutional surface with four major capability groups; governance
 *     is not a research artifact.
 *   - NOT a stage view: the directive's OBS-CONV3-4 warning requires the
 *     stage rendering branch to be BUILT and PROVEN before any ?view= claim.
 *     Item 4 owns that build; item 5 must not front-load it. The overlay
 *     pattern is already proven by item 3 and makes no stage claim.
 *
 * Constitutional notes:
 *   - M2: reasonCodeFor (named export) is preserved verbatim in
 *     ./governanceRecords with its "—" absence marker.
 *   - M3: the four constitutional declarations (Production certification
 *     boundary, Read-Only Governance Boundary, Inert Display Rules,
 *     Standing Residuals) render as always-visible sections — no tooltip,
 *     accordion-default-closed, or secondary tab.
 *   - M5: nine state variables across three INDEPENDENT fetches; each
 *     section degrades independently — a failed audit fetch never blanks
 *     the certification boundary.
 *   - R3: runtime values never render plausible-looking fallbacks; absence
 *     renders as absence.
 */

import { useEffect, useMemo, useState } from "react";
import {
  fetchApiCatalogue,
  fetchAuditEvents,
  fetchInstitutionalIntelligenceBundle,
  fetchOperatorScopeRecord,
  fetchOperatorScopeRecords,
  fetchPlatformOperationsEvidence,
  fetchPluginContracts,
  fetchRbacPermissions,
  fetchRouteInventory,
  type ApiCatalogueResponse,
  type AuditEvent,
  type InstitutionalIntelligenceBundle,
  type OperatorScopeListResult,
  type OperatorScopeRecordResult,
  type PlatformOperationsEvidence,
  type PluginContractsResponse,
  type RbacPermissionsResponse,
  type RouteInventoryResponse,
} from "../../../api/client";
import { PlatformRecordsSection } from "./PlatformRecordsSection";
import { AssistantAuditSubSection } from "../../../workstation/governance/AssistantAuditSubSection";
import { EmptyState, ErrorBanner, Skeleton } from "../../ui";
import { useOverlayController } from "../../../workstation/overlays/OverlayProvider";
import {
  reasonCodeFor,
  type GovernanceStatusItem,
  UI007_CERTIFICATION_STATUS,
  UI007_EVIDENCE_MANIFEST,
  UI007_GOVERNANCE_SOURCES,
  UI007_GOVERNANCE_STATUS,
  UI007_GUARDRAILS,
  UI007_READINESS_POSTURE_RECORDS,
  UI007_STANDING_RESIDUALS,
} from "./governanceRecords";
import "./GovernanceOverlay.css";

function detailText(details: Record<string, unknown> | null): string {
  if (!details || Object.keys(details).length === 0) return "{}";
  return JSON.stringify(details, null, 2);
}

function StatusGrid({ items }: { items: GovernanceStatusItem[] }) {
  return (
    <div className="artifact-explorer-summary-grid">
      {items.map((item) => (
        <article className="research-overview-card" key={`${item.label}-${item.value}`}>
          <span className="badge stub">{item.label}</span>
          <strong>{item.value}</strong>
          <small>{item.detail}</small>
        </article>
      ))}
    </div>
  );
}

function AuditExplorerPanel({
  auditEvents,
  loading = false,
  error = null,
  onRefresh,
}: {
  auditEvents: AuditEvent[];
  loading?: boolean;
  error?: string | null;
  onRefresh?: () => void;
}) {
  const [query, setQuery] = useState("");
  const [sortOrder, setSortOrder] = useState<"newest" | "oldest">("newest");
  const [selectedId, setSelectedId] = useState(auditEvents[0]?.id ?? "");

  useEffect(() => {
    if (!selectedId && auditEvents[0]) {
      setSelectedId(auditEvents[0].id);
    } else if (selectedId && !auditEvents.some((event) => event.id === selectedId)) {
      setSelectedId(auditEvents[0]?.id ?? "");
    }
  }, [auditEvents, selectedId]);

  const filteredEvents = useMemo(() => {
    const normalized = query.trim().toLowerCase();
    const scoped = normalized
      ? auditEvents.filter((event) =>
          [
            event.id,
            event.category,
            event.action,
            event.actor,
            event.message,
            event.resource_type ?? "",
            event.resource_id ?? "",
            reasonCodeFor(event),
          ]
            .join(" ")
            .toLowerCase()
            .includes(normalized),
        )
      : auditEvents;
    return [...scoped].sort((left, right) => {
      const leftTime = Date.parse(left.created_at);
      const rightTime = Date.parse(right.created_at);
      return sortOrder === "newest" ? rightTime - leftTime : leftTime - rightTime;
    });
  }, [auditEvents, query, sortOrder]);

  const selectedEvent =
    filteredEvents.find((event) => event.id === selectedId) ?? filteredEvents[0] ?? null;

  return (
    <section className="panel span-12" aria-label="Read-only audit explorer" data-testid="governance-audit-explorer">
      <div className="artifact-explorer-frame-head">
        <div>
          <h2>Audit Explorer</h2>
          <p className="muted">
            Existing audit rows are displayed as returned by the audit_events read seam. Filters and
            ordering are browser presentation state only.
          </p>
        </div>
        <button type="button" className="btn" onClick={onRefresh} disabled={!onRefresh || loading}>
          Refresh audit rows
        </button>
      </div>

      <div className="artifact-filter-panel" aria-label="In-memory audit filters">
        <label className="field-inline">
          <span>Category, action, reason, or resource</span>
          <input value={query} onChange={(event) => setQuery(event.target.value)} />
        </label>
        <label className="field-inline">
          <span>Order</span>
          <select value={sortOrder} onChange={(event) => setSortOrder(event.target.value as "newest" | "oldest")}>
            <option value="newest">Newest first</option>
            <option value="oldest">Oldest first</option>
          </select>
        </label>
        <p className="muted" role="note">
          In-memory only: showing {filteredEvents.length} of {auditEvents.length} audit rows. A
          filtered view is not a full-scope governance claim.
        </p>
      </div>

      {error ? <ErrorBanner title="Audit Error" message={error} /> : null}
      {loading ? <Skeleton variant="rect" height="120px" aria-label="Loading audit rows" /> : null}

      <div className="artifact-catalog-layout">
        <div className="artifact-catalog-list" aria-label="Read-only audit event list">
          {filteredEvents.length === 0 && !loading ? (
            <EmptyState
              title="No Audit Rows"
              description="No audit rows match the current filter."
              variant="compact"
            />
          ) : null}
          {filteredEvents.map((event) => (
            <button
              key={event.id}
              type="button"
              className={`artifact-catalog-card${selectedEvent?.id === event.id ? " active" : ""}`}
              onClick={() => setSelectedId(event.id)}
            >
              <span className="badge stub">{event.category}</span>
              <strong>{event.action}</strong>
              <small>{event.actor}</small>
              <small className="mono">{reasonCodeFor(event)}</small>
              <small className="mono">{event.id}</small>
            </button>
          ))}
        </div>

        <article className="artifact-detail-card" aria-label="Read-only audit event detail" data-testid="governance-audit-event-detail">
          {selectedEvent ? (
            <>
              <header>
                <span className="badge stub">{selectedEvent.category}</span>
                <h3>{selectedEvent.action}</h3>
                <p className="muted">Audit fields and reason-codes are shown as stored text.</p>
              </header>
              <dl className="kv compact">
                <dt>Audit id</dt>
                <dd className="mono">{selectedEvent.id}</dd>
                <dt>Actor</dt>
                <dd>{selectedEvent.actor}</dd>
                <dt>Message</dt>
                <dd>{selectedEvent.message}</dd>
                <dt>Resource type</dt>
                <dd>{selectedEvent.resource_type ?? "—"}</dd>
                <dt>Resource id</dt>
                <dd className="mono">{selectedEvent.resource_id ?? "—"}</dd>
                <dt>Reason code</dt>
                <dd className="mono">{reasonCodeFor(selectedEvent)}</dd>
                <dt>Created at</dt>
                <dd className="mono">{selectedEvent.created_at}</dd>
              </dl>
              <section aria-label="Audit event detail payload" data-testid="governance-audit-details-payload">
                <h4>Details payload</h4>
                <pre className="mono">{detailText(selectedEvent.details)}</pre>
              </section>
              <section aria-label="Refusal reason-code viewer" data-testid="governance-refusal-reason-viewer">
                <h4>Refusal reason-code viewer</h4>
                <p className="muted">
                  SCREAMING_SNAKE refusal reason-codes remain stored refusal text. This viewer does
                  not reinterpret them as an authorization path.
                </p>
                <strong className="mono">{reasonCodeFor(selectedEvent)}</strong>
              </section>
            </>
          ) : (
            <p className="muted">Select an audit row.</p>
          )}
        </article>
      </div>
    </section>
  );
}



function storedText(value: unknown): string {
  if (value === undefined || value === null) return "—";
  if (typeof value === "string") return value;
  if (typeof value === "number" || typeof value === "boolean") return String(value);
  return JSON.stringify(value);
}

function storedList(value: unknown): string {
  return Array.isArray(value) ? value.map((item) => storedText(item)).join(", ") : storedText(value);
}

function EvidenceViewerPanel() {
  return (
    <section className="panel span-12" aria-label="Read-only evidence viewer" data-testid="governance-evidence-viewer">
      <div className="artifact-explorer-frame-head">
        <div>
          <h2>Evidence Viewer</h2>
          <p className="muted">
            First-party evidence index with source-preserving fields. This is an index of recorded
            evidence, not a file browser, upload surface, or generated narrative.
          </p>
        </div>
        <div className="research-guardrail-card" role="note" aria-label="Evidence viewer posture">
          <strong>Recorded fields only</strong>
          <span>Read-only · First-party index · No source alteration</span>
        </div>
      </div>

      <div className="artifact-source-grid" aria-label="Evidence record manifest">
        {UI007_EVIDENCE_MANIFEST.map((record) => (
          <article className="artifact-source-card" key={record.id} data-verbatim="true">
            <span className="ix-metadata">{record.recordType}</span>
            <h3 className="mono">{record.id}</h3>
            <dl className="kv compact">
              <dt>Status / verdict as stored</dt>
              <dd>{record.status}</dd>
              <dt>Method / version as stored</dt>
              <dd className="mono">{record.methodVersion}</dd>
              <dt>Observed sample / test count</dt>
              <dd className="mono">{record.observedCount}</dd>
              <dt>Scope as stored</dt>
              <dd>{record.scope}</dd>
              <dt>Uncertainty / observation</dt>
              <dd>{record.uncertainty}</dd>
              <dt>Limitations</dt>
              <dd>{record.limitations.join(" · ")}</dd>
              <dt>Source ids</dt>
              <dd className="mono">{record.sourceIds.join(" · ")}</dd>
              <dt>Lineage</dt>
              <dd>{record.lineage}</dd>
              <dt>Audit reference</dt>
              <dd className="mono">{record.auditReference}</dd>
              <dt>Report hash</dt>
              <dd className="mono">{record.reportHash}</dd>
              <dt>Recorded at</dt>
              <dd className="mono">{record.recordedAt}</dd>
            </dl>
          </article>
        ))}
      </div>
    </section>
  );
}

function ValidationSummaryPanel({
  bundle,
  loading = false,
  error = null,
}: {
  bundle: InstitutionalIntelligenceBundle | null;
  loading?: boolean;
  error?: string | null;
}) {
  const records = bundle?.validation ?? [];

  return (
    <section className="panel span-12" aria-label="Read-only validation summary panels" data-testid="governance-validation-panels">
      <div className="artifact-explorer-frame-head">
        <div>
          <h2>Validation Summary Panels</h2>
          <p className="muted">
            Every validation record returned by the established intelligence read seam is shown with
            its stored scope, count, uncertainty, limitations, lineage, and status fields visible.
          </p>
        </div>
        <div className="research-guardrail-card" role="note" aria-label="Validation summary posture">
          <strong>{records.length} returned record{records.length === 1 ? "" : "s"}</strong>
          <span>Read-only · Scope visible · Source-preserving</span>
        </div>
      </div>

      {error ? <ErrorBanner title="Validation Error" message={error} /> : null}
      {loading ? <Skeleton variant="rect" height="120px" aria-label="Loading existing validation records" /> : null}
      {!loading && records.length === 0 ? (
        <EmptyState
          title="No Validation Records"
          description="No validation records were returned by the existing read seam."
          variant="compact"
        />
      ) : null}

      <div className="artifact-source-grid" aria-label="Validation records returned by existing read seam">
        {records.map((record) => (
          <article className="artifact-source-card" key={storedText(record.id)} data-verbatim="true">
            <span className="ix-metadata">{storedText(record.artifact_type)}</span>
            <h3 className="mono">{storedText(record.id)}</h3>
            <dl className="kv compact">
              <dt>Status / verdict as stored</dt>
              <dd>{storedText(record.research_status)}</dd>
              <dt>Method / version as stored</dt>
              <dd className="mono">{storedText(record.method_version)}</dd>
              <dt>Sample count</dt>
              <dd className="mono">{storedText(record.sample_count)}</dd>
              <dt>Scope</dt>
              <dd className="mono">{storedText(record.validation_scope ?? record.market_scope)}</dd>
              <dt>Uncertainty</dt>
              <dd className="mono">{storedText(record.uncertainty)}</dd>
              <dt>Limitations</dt>
              <dd>{storedList(record.limitations)}</dd>
              <dt>Source ids</dt>
              <dd className="mono">{storedList(record.source_signal_ids ?? record.source_artifact_ids)}</dd>
              <dt>Lineage</dt>
              <dd className="mono">{storedText(record.input_lineage)}</dd>
              <dt>Audit reference</dt>
              <dd className="mono">{storedText(record.audit_correlation_id)}</dd>
              <dt>Report hash</dt>
              <dd className="mono">{storedText(record.report_hash)}</dd>
              <dt>Recorded at</dt>
              <dd className="mono">{storedText(record.created_at)}</dd>
            </dl>
          </article>
        ))}
      </div>
    </section>
  );
}



function directValue(value: unknown): string {
  if (value === undefined || value === null) return "—";
  if (typeof value === "string" || typeof value === "number" || typeof value === "boolean") {
    return String(value);
  }
  return JSON.stringify(value);
}

function PlatformOperationsPanel({
  evidence,
  loading = false,
  error = null,
}: {
  evidence: PlatformOperationsEvidence | null;
  loading?: boolean;
  error?: string | null;
}) {
  return (
    <section className="panel span-12" aria-label="Platform health readiness version and API posture" data-testid="governance-platform-posture">
      <div className="artifact-explorer-frame-head">
        <div>
          <h2>Platform Health, Readiness &amp; API Posture</h2>
          <p className="muted">
            Existing operational read responses are displayed as returned. Runtime evidence describes
            process state only; it does not constitute a production certification decision.
          </p>
        </div>
        <div className="research-guardrail-card" role="note" aria-label="Runtime certification separation">
          <strong>Runtime evidence only</strong>
          <span>Production NOT CERTIFIED · Doc 11 HELD</span>
        </div>
      </div>

      <section className="advisory-disclaimer" aria-label="Runtime readiness is not production certification">
        <strong>Runtime readiness is not production certification.</strong> A liveness or readiness
        response reports current process/dependency evidence. Production remains NOT CERTIFIED under
        the separate Doc 11 ITRGA track.
      </section>

      {error ? <ErrorBanner title="Operations Error" message={error} /> : null}
      {loading ? <Skeleton variant="rect" height="120px" aria-label="Loading existing operational read responses" /> : null}
      {!loading && !evidence ? (
        <EmptyState
          title="Operational Evidence Unavailable"
          description="Operational read responses are not currently available from the existing services."
          variant="compact"
        />
      ) : null}

      {evidence ? (
        <div className="artifact-source-grid" aria-label="Read-only operational evidence panels">
          <article className="artifact-source-card" data-verbatim="true">
            <span className="ix-metadata">GET /health · as returned</span>
            <h3>Runtime liveness</h3>
            <dl className="kv compact">
              <dt>Status</dt>
              <dd>{directValue(evidence.health.status)}</dd>
              <dt>Service</dt>
              <dd>{directValue(evidence.health.service)}</dd>
              <dt>Version</dt>
              <dd className="mono">{directValue(evidence.health.version)}</dd>
              <dt>Environment</dt>
              <dd>{directValue(evidence.health.environment)}</dd>
              <dt>Latency ms</dt>
              <dd className="mono">{directValue(evidence.health.latency_ms)}</dd>
              <dt>Timestamp</dt>
              <dd className="mono">{directValue(evidence.health.timestamp)}</dd>
            </dl>
          </article>

          <article className="artifact-source-card" data-verbatim="true">
            <span className="ix-metadata">GET /ready · as returned</span>
            <h3>Runtime readiness</h3>
            <dl className="kv compact">
              <dt>Status</dt>
              <dd>{directValue(evidence.readiness.status)}</dd>
              <dt>Service</dt>
              <dd>{directValue(evidence.readiness.service)}</dd>
              <dt>Version</dt>
              <dd className="mono">{directValue(evidence.readiness.version)}</dd>
              <dt>Timestamp</dt>
              <dd className="mono">{directValue(evidence.readiness.timestamp)}</dd>
            </dl>
            <h4>Checks as returned</h4>
            <dl className="kv compact">
              {evidence.readiness.checks.map((check) => (
                <div key={check.name}>
                  <dt>{check.name}</dt>
                  <dd className="mono">
                    {check.status} · {directValue(check.latency_ms)} ms · {directValue(check.detail)}
                  </dd>
                </div>
              ))}
            </dl>
          </article>

          <article className="artifact-source-card" aria-label="Production certification remains separate" data-verbatim="true">
            <span className="ix-metadata">Doc 11 · canonical governance record</span>
            <h3>Production certification boundary</h3>
            <dl className="kv compact">
              <dt>Production status</dt>
              <dd>Production NOT CERTIFIED</dd>
              <dt>Doc 11 track</dt>
              <dd>HELD</dd>
              <dt>Runtime interpretation</dt>
              <dd>Readiness response is not a certification outcome.</dd>
            </dl>
          </article>

          <article className="artifact-source-card" data-verbatim="true">
            <span className="ix-metadata">GET /api/v1/metrics · safe direct fields</span>
            <h3>Observability metrics</h3>
            <dl className="kv compact">
              <dt>Uptime seconds</dt>
              <dd className="mono">{directValue(evidence.metrics.observability.process.uptime_seconds)}</dd>
              <dt>HTTP requests</dt>
              <dd className="mono">{directValue(evidence.metrics.observability.http.requests_total)}</dd>
              <dt>HTTP errors</dt>
              <dd className="mono">{directValue(evidence.metrics.observability.http.errors_total)}</dd>
              <dt>Average latency ms</dt>
              <dd className="mono">{directValue(evidence.metrics.observability.http.latency_avg_ms)}</dd>
              <dt>Maximum latency ms</dt>
              <dd className="mono">{directValue(evidence.metrics.observability.http.latency_max_ms)}</dd>
              <dt>Database status</dt>
              <dd>{directValue(evidence.metrics.database.status)}</dd>
              <dt>Database latency ms</dt>
              <dd className="mono">{directValue(evidence.metrics.database.latency_ms)}</dd>
              <dt>Secret marker count</dt>
              <dd className="mono">0</dd>
            </dl>
          </article>

          <article className="artifact-source-card" data-verbatim="true">
            <span className="ix-metadata">GET /api/v1/persistence/stats · as returned</span>
            <h3>Persistence statistics</h3>
            <dl className="kv compact">
              <dt>Backend</dt>
              <dd>{directValue(evidence.persistenceStats.backend)}</dd>
              <dt>URL scheme</dt>
              <dd className="mono">{directValue(evidence.persistenceStats.database_url_scheme)}</dd>
              <dt>Candle count</dt>
              <dd className="mono">{directValue(evidence.persistenceStats.candle_count)}</dd>
              <dt>Audit count</dt>
              <dd className="mono">{directValue(evidence.persistenceStats.audit_count)}</dd>
              <dt>Pool</dt>
              <dd className="mono">{directValue(evidence.persistenceStats.pool)}</dd>
            </dl>
          </article>

          <article className="artifact-source-card" data-verbatim="true">
            <span className="ix-metadata">GET /api/v1/system/info · as returned</span>
            <h3>Version &amp; system identity</h3>
            <dl className="kv compact">
              <dt>Name</dt>
              <dd>{directValue(evidence.systemInfo.name)}</dd>
              <dt>Platform version</dt>
              <dd className="mono">{directValue(evidence.systemInfo.version)}</dd>
              <dt>Wave / unit</dt>
              <dd>{directValue(evidence.systemInfo.wave)} · {directValue(evidence.systemInfo.unit)}</dd>
              <dt>Architecture version</dt>
              <dd className="mono">{directValue(evidence.systemInfo.architecture_version)}</dd>
              <dt>Timestamp</dt>
              <dd className="mono">{directValue(evidence.systemInfo.timestamp)}</dd>
              <dt>API catalogue Alembic head</dt>
              <dd className="mono">{directValue(evidence.apiCatalogue.persistence.alembic_head_expected)}</dd>
            </dl>
          </article>

          <article className="artifact-source-card" data-verbatim="true">
            <span className="ix-metadata">Existing institutional read APIs · as returned</span>
            <h3>Route, RBAC, API &amp; plugin posture</h3>
            <dl className="kv compact">
              <dt>Route inventory version</dt>
              <dd className="mono">{directValue(evidence.routeInventory.version)}</dd>
              <dt>Route actuation surface present</dt>
              <dd>{directValue(evidence.routeInventory.actuation_surface_present)}</dd>
              <dt>Route Gate capability present</dt>
              <dd>{directValue(evidence.routeInventory.governance_gate_capability_present)}</dd>
              <dt>RBAC policy</dt>
              <dd>{directValue(evidence.rbac.policy)}</dd>
              <dt>RBAC vocabulary</dt>
              <dd className="mono">{directValue(evidence.rbac.roles)}</dd>
              <dt>API catalogue version / route count</dt>
              <dd className="mono">
                {directValue(evidence.apiCatalogue.catalogue_version)} · {directValue(evidence.apiCatalogue.route_count)}
              </dd>
              <dt>Abuse guard</dt>
              <dd>{directValue(evidence.apiCatalogue.abuse_guard.status)} · {directValue(evidence.apiCatalogue.abuse_guard.reason)}</dd>
              <dt>Dynamic plugin code enabled</dt>
              <dd>{directValue(evidence.pluginContracts.dynamic_code_execution_enabled)}</dd>
              <dt>Third-party plugin enabled</dt>
              <dd>{directValue(evidence.pluginContracts.third_party_plugin_execution_enabled)}</dd>
            </dl>
          </article>

          <article className="artifact-source-card" aria-label="Readiness posture records and residual honesty">
            <span className="ix-metadata">Existing W7-U07 constants and canonical registers</span>
            <h3>Readiness posture records &amp; residual honesty</h3>
            <dl className="kv compact">
              {UI007_READINESS_POSTURE_RECORDS.map((postureRecord) => (
                <div key={postureRecord.item}>
                  <dt>{postureRecord.item}</dt>
                  <dd>
                    <span className="mono">{postureRecord.status}</span> · {postureRecord.technicalDebtId ?? "no technical debt id"} · {postureRecord.rationale}
                  </dd>
                </div>
              ))}
              {UI007_STANDING_RESIDUALS.map((residual) => (
                <div key={residual.label}>
                  <dt>{residual.label}</dt>
                  <dd>{residual.value} · {residual.detail}</dd>
                </div>
              ))}
            </dl>
          </article>
        </div>
      ) : null}
    </section>
  );
}


export function GovernanceEvidenceWorkspace({
  auditEvents = [],
  auditLoading = false,
  auditError = null,
  onRefreshAuditEvents,
  validationBundle = null,
  validationLoading = false,
  validationError = null,
  platformOperations = null,
  platformOperationsLoading = false,
  platformOperationsError = null,
  routeInventory = null,
  routeInventoryLoading = false,
  routeInventoryError = null,
  rbac = null,
  rbacLoading = false,
  rbacError = null,
  apiCatalogue = null,
  apiCatalogueLoading = false,
  apiCatalogueError = null,
  pluginContracts = null,
  pluginContractsLoading = false,
  pluginContractsError = null,
  scopeResult = null,
  scopeLoading = false,
  scopeRecordResult = null,
  scopeDetailLoading = false,
  onRefreshScope,
  onSelectScopeDetail,
}: {
  auditEvents?: AuditEvent[];
  auditLoading?: boolean;
  auditError?: string | null;
  onRefreshAuditEvents?: () => void;
  validationBundle?: InstitutionalIntelligenceBundle | null;
  validationLoading?: boolean;
  validationError?: string | null;
  platformOperations?: PlatformOperationsEvidence | null;
  platformOperationsLoading?: boolean;
  platformOperationsError?: string | null;
  routeInventory?: RouteInventoryResponse | null;
  routeInventoryLoading?: boolean;
  routeInventoryError?: string | null;
  rbac?: RbacPermissionsResponse | null;
  rbacLoading?: boolean;
  rbacError?: string | null;
  apiCatalogue?: ApiCatalogueResponse | null;
  apiCatalogueLoading?: boolean;
  apiCatalogueError?: string | null;
  pluginContracts?: PluginContractsResponse | null;
  pluginContractsLoading?: boolean;
  pluginContractsError?: string | null;
  scopeResult?: OperatorScopeListResult | null;
  scopeLoading?: boolean;
  scopeRecordResult?: OperatorScopeRecordResult | null;
  scopeDetailLoading?: boolean;
  onRefreshScope?: () => void;
  onSelectScopeDetail?: (operatorId: string) => void;
}) {
  return (
    <>
      <div className="page-header">
        <div>
          <h1>Governance & Evidence</h1>
          <p className="muted">
            Read-only workspace for constitutional posture, production status, audit rows,
            evidence records, validation summaries, health, readiness, and version information.
          </p>
        </div>
        <span className="badge stub" aria-label="UI-007 phase marker">
          UI-007-P05 · Operations evidence
        </span>
      </div>

      <section className="advisory-disclaimer" aria-label="Governance workspace disclaimer">
        <strong>Governance visibility only.</strong> This workspace displays existing governance and
        evidence posture. It does not change governance state, production state, audit records, or
        validation outcomes.
      </section>

      <section className="panel span-12" aria-label="Governance workspace frame" data-testid="governance-frame">
        <div className="artifact-explorer-frame-head">
          <div>
            <h2>Governance Workspace Frame</h2>
            <p className="muted">
              Single protected route on the institutional shell. P05 adds operational evidence
              while preserving the prior read-only governance, audit, evidence, and validation surfaces.
            </p>
          </div>
          <div className="research-guardrail-card" role="note" aria-label="Governance inert status">
            <strong>Gate CLOSED</strong>
            <span>Production NOT CERTIFIED · Doc 11 HELD · AXIOM does not act</span>
          </div>
        </div>
      </section>

      <section className="panel span-12" aria-label="Governance status read-only panel">
        <h2>Governance Status</h2>
        <p className="muted">
          Current governance posture is displayed from canonical records and shell posture. The status
          is informational and cannot be changed from this workspace.
        </p>
        <StatusGrid items={UI007_GOVERNANCE_STATUS} />
      </section>

      <section className="panel span-12" aria-label="Certification status read-only panel" data-testid="governance-certification-status">
        <h2>Certification Status</h2>
        <p className="muted">
          Production Readiness Certification remains an out-of-band Doc 11 governance track. This
          panel displays the current status and outcome vocabulary without any action affordance.
        </p>
        <StatusGrid items={UI007_CERTIFICATION_STATUS} />
      </section>

      <section className="panel span-12" aria-label="Residual status read-only panel" data-testid="governance-standing-residuals">
        <h2>Standing Residuals</h2>
        <p className="muted">
          Residuals are displayed as tracked governance facts. No residual is modified by this surface.
        </p>
        <StatusGrid items={UI007_STANDING_RESIDUALS} />
      </section>

      <AuditExplorerPanel
        auditEvents={auditEvents}
        loading={auditLoading}
        error={auditError}
        onRefresh={onRefreshAuditEvents}
      />

      <EvidenceViewerPanel />

      <ValidationSummaryPanel
        bundle={validationBundle}
        loading={validationLoading}
        error={validationError}
      />

      <PlatformOperationsPanel
        evidence={platformOperations}
        loading={platformOperationsLoading}
        error={platformOperationsError}
      />

      <PlatformRecordsSection
        routeInventory={routeInventory}
        routeInventoryLoading={routeInventoryLoading}
        routeInventoryError={routeInventoryError}
        rbac={rbac}
        rbacLoading={rbacLoading}
        rbacError={rbacError}
        apiCatalogue={apiCatalogue}
        apiCatalogueLoading={apiCatalogueLoading}
        apiCatalogueError={apiCatalogueError}
        pluginContracts={pluginContracts}
        pluginContractsLoading={pluginContractsLoading}
        pluginContractsError={pluginContractsError}
        scopeResult={scopeResult}
        scopeLoading={scopeLoading}
        scopeRecordResult={scopeRecordResult}
        scopeDetailLoading={scopeDetailLoading}
        onRefreshScope={onRefreshScope}
        onSelectScopeDetail={onSelectScopeDetail}
      />

      <section className="panel span-12" aria-label="Read-only governance guardrails" data-testid="governance-readonly-boundary">
        <h2>Read-Only Governance Boundary</h2>
        <p className="muted">
          G-1 through G-7 are rendered as operator-visible constraints. All entries are informational.
        </p>
        <StatusGrid items={UI007_GUARDRAILS} />
      </section>

      <section className="panel span-12" aria-label="UI-007 governed data-source inventory" data-testid="governance-sources-inventory">
        <h2>Governance Data-Source Inventory</h2>
        <p className="muted">
          Every Doc 12 §9 surface is mapped to an existing read seam or canonical governance record.
          This phase adds no backend endpoint, table, migration, or dependency.
        </p>
        <div className="artifact-source-grid">
          {UI007_GOVERNANCE_SOURCES.map((item) => (
            <article className="artifact-source-card" key={item.surface}>
              <span className="ix-metadata">{item.surface}</span>
              <dl className="kv compact">
                <dt>Existing source</dt>
                <dd>{item.existingSource}</dd>
                <dt>Read seam</dt>
                <dd className="mono">{item.readSeam}</dd>
                <dt>P01/P02/P03 posture</dt>
                <dd>{item.p01Posture}</dd>
              </dl>
            </article>
          ))}
        </div>
      </section>

      <section className="panel span-12" aria-label="Forbidden governance affordance notice" data-testid="governance-inert-display-rules">
        <h2>Inert Display Rules</h2>
        <div className="artifact-organization-grid">
          <article className="research-artifact-card">
            <h3>Gate state</h3>
            <p className="muted">Shown as CLOSED. The UI presents no switch, form, or action path.</p>
          </article>
          <article className="research-artifact-card">
            <h3>Production state</h3>
            <p className="muted">Shown as NOT CERTIFIED / HELD. The UI presents no approval path.</p>
          </article>
          <article className="research-artifact-card">
            <h3>Audit state</h3>
            <p className="muted">Audit rows remain stored records. This surface adds no record-changing path.</p>
          </article>
        </div>
      </section>

      <section data-ui008-mount="audit-sub-section" aria-label="Assistant Audit Sub-Section mount point">
        <AssistantAuditSubSection />
      </section>
    </>
  );
}

/**
 * Self-fetching overlay container. Nine state variables across three
 * INDEPENDENT fetches (M5): audit, validation, platform-operations. Each
 * section degrades independently; failures surface explicit per-section
 * error text and never blank the constitutional declarations.
 */
export function GovernanceOverlay() {
  const overlay = useOverlayController();
  const [auditEvents, setAuditEvents] = useState<AuditEvent[]>([]);
  const [auditLoading, setAuditLoading] = useState(false);
  const [auditError, setAuditError] = useState<string | null>(null);
  const [validationBundle, setValidationBundle] = useState<InstitutionalIntelligenceBundle | null>(null);
  const [validationLoading, setValidationLoading] = useState(false);
  const [validationError, setValidationError] = useState<string | null>(null);
  const [platformOperations, setPlatformOperations] = useState<PlatformOperationsEvidence | null>(null);
  const [platformOperationsLoading, setPlatformOperationsLoading] = useState(false);
  const [platformOperationsError, setPlatformOperationsError] = useState<string | null>(null);
  // SURF-P03: five independent platform-record fetches (R2 per-source
  // pattern) — the four record collections plus operator scope records.
  const [routeInventory, setRouteInventory] = useState<RouteInventoryResponse | null>(null);
  const [routeInventoryLoading, setRouteInventoryLoading] = useState(false);
  const [routeInventoryError, setRouteInventoryError] = useState<string | null>(null);
  const [rbac, setRbac] = useState<RbacPermissionsResponse | null>(null);
  const [rbacLoading, setRbacLoading] = useState(false);
  const [rbacError, setRbacError] = useState<string | null>(null);
  const [apiCatalogue, setApiCatalogue] = useState<ApiCatalogueResponse | null>(null);
  const [apiCatalogueLoading, setApiCatalogueLoading] = useState(false);
  const [apiCatalogueError, setApiCatalogueError] = useState<string | null>(null);
  const [pluginContracts, setPluginContracts] = useState<PluginContractsResponse | null>(null);
  const [pluginContractsLoading, setPluginContractsLoading] = useState(false);
  const [pluginContractsError, setPluginContractsError] = useState<string | null>(null);
  const [scopeResult, setScopeResult] = useState<OperatorScopeListResult | null>(null);
  const [scopeLoading, setScopeLoading] = useState(false);
  const [scopeRecordResult, setScopeRecordResult] = useState<OperatorScopeRecordResult | null>(null);
  const [scopeDetailLoading, setScopeDetailLoading] = useState(false);

  async function loadAuditEvents() {
    setAuditLoading(true);
    setAuditError(null);
    try {
      setAuditEvents(await fetchAuditEvents({ limit: 50 }));
    } catch (err) {
      setAuditError(err instanceof Error ? err.message : "Failed to load audit rows");
    } finally {
      setAuditLoading(false);
    }
  }

  async function loadValidationRecords() {
    setValidationLoading(true);
    setValidationError(null);
    try {
      setValidationBundle(await fetchInstitutionalIntelligenceBundle(50));
    } catch (err) {
      setValidationError(err instanceof Error ? err.message : "Failed to load validation records");
    } finally {
      setValidationLoading(false);
    }
  }

  async function loadPlatformOperations() {
    setPlatformOperationsLoading(true);
    setPlatformOperationsError(null);
    try {
      setPlatformOperations(await fetchPlatformOperationsEvidence());
    } catch (err) {
      setPlatformOperationsError(
        err instanceof Error ? err.message : "Failed to load operational read responses",
      );
    } finally {
      setPlatformOperationsLoading(false);
    }
  }

  async function loadRouteInventoryRecords() {
    setRouteInventoryLoading(true);
    setRouteInventoryError(null);
    try {
      setRouteInventory(await fetchRouteInventory());
    } catch (err) {
      setRouteInventoryError(
        err instanceof Error ? err.message : "Failed to load route inventory records",
      );
    } finally {
      setRouteInventoryLoading(false);
    }
  }

  async function loadRbacRecords() {
    setRbacLoading(true);
    setRbacError(null);
    try {
      setRbac(await fetchRbacPermissions());
    } catch (err) {
      setRbacError(err instanceof Error ? err.message : "Failed to load RBAC records");
    } finally {
      setRbacLoading(false);
    }
  }

  async function loadApiCatalogueRecords() {
    setApiCatalogueLoading(true);
    setApiCatalogueError(null);
    try {
      setApiCatalogue(await fetchApiCatalogue());
    } catch (err) {
      setApiCatalogueError(
        err instanceof Error ? err.message : "Failed to load API catalogue records",
      );
    } finally {
      setApiCatalogueLoading(false);
    }
  }

  async function loadPluginContractRecords() {
    setPluginContractsLoading(true);
    setPluginContractsError(null);
    try {
      setPluginContracts(await fetchPluginContracts());
    } catch (err) {
      setPluginContractsError(
        err instanceof Error ? err.message : "Failed to load plugin contract records",
      );
    } finally {
      setPluginContractsLoading(false);
    }
  }

  async function loadScopeRecords() {
    setScopeLoading(true);
    setScopeResult(null);
    setScopeRecordResult(null);
    try {
      setScopeResult(await fetchOperatorScopeRecords());
    } catch (err) {
      setScopeResult({
        kind: "error",
        detail: err instanceof Error ? err.message : "Failed to load scope records",
      });
    } finally {
      setScopeLoading(false);
    }
  }

  async function selectScopeDetail(operatorId: string) {
    setScopeDetailLoading(true);
    setScopeRecordResult(null);
    setScopeRecordResult(await fetchOperatorScopeRecord(operatorId));
    setScopeDetailLoading(false);
  }

  // Load on first open; per-section refresh is operator-initiated.
  const [hasLoaded, setHasLoaded] = useState(false);
  useEffect(() => {
    if (overlay.governanceOpen && !hasLoaded) {
      setHasLoaded(true);
      void loadAuditEvents();
      void loadValidationRecords();
      void loadPlatformOperations();
      void loadRouteInventoryRecords();
      void loadRbacRecords();
      void loadApiCatalogueRecords();
      void loadPluginContractRecords();
      void loadScopeRecords();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps -- load-on-first-open only
  }, [overlay.governanceOpen, hasLoaded]);

  if (!overlay.governanceOpen) return null;

  return (
    <div className="ix-governance-backdrop" data-testid="governance-overlay-backdrop">
      <div
        className="ix-governance-overlay"
        role="dialog"
        aria-modal="true"
        aria-label="Governance and evidence"
        data-testid="governance-overlay"
      >
        <div className="ix-governance-header">
          <span className="ix-metadata mono">GOVERNANCE &amp; EVIDENCE</span>
          <button
            type="button"
            className="ix-shell-button"
            onClick={overlay.closeGovernance}
            aria-label="Close governance and evidence"
            data-testid="governance-overlay-close-btn"
          >
            Close
          </button>
        </div>
        <div className="ix-governance-body" data-testid="governance-overlay-body">
          <GovernanceEvidenceWorkspace
            auditEvents={auditEvents}
            auditLoading={auditLoading}
            auditError={auditError}
            onRefreshAuditEvents={() => void loadAuditEvents()}
            validationBundle={validationBundle}
            validationLoading={validationLoading}
            validationError={validationError}
            platformOperations={platformOperations}
            platformOperationsLoading={platformOperationsLoading}
            platformOperationsError={platformOperationsError}
            routeInventory={routeInventory}
            routeInventoryLoading={routeInventoryLoading}
            routeInventoryError={routeInventoryError}
            rbac={rbac}
            rbacLoading={rbacLoading}
            rbacError={rbacError}
            apiCatalogue={apiCatalogue}
            apiCatalogueLoading={apiCatalogueLoading}
            apiCatalogueError={apiCatalogueError}
            pluginContracts={pluginContracts}
            pluginContractsLoading={pluginContractsLoading}
            pluginContractsError={pluginContractsError}
            scopeResult={scopeResult}
            scopeLoading={scopeLoading}
            scopeRecordResult={scopeRecordResult}
            scopeDetailLoading={scopeDetailLoading}
            onRefreshScope={() => void loadScopeRecords()}
            onSelectScopeDetail={(operatorId) => void selectScopeDetail(operatorId)}
          />
        </div>
      </div>
    </div>
  );
}
