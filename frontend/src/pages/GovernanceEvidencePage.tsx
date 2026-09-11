import { useEffect, useMemo, useState } from "react";
import {
  fetchAuditEvents,
  fetchInstitutionalIntelligenceBundle,
  fetchPlatformOperationsEvidence,
  type AuditEvent,
  type InstitutionalIntelligenceBundle,
  type PlatformOperationsEvidence,
} from "../api/client";
import { AssistantAuditSubSection } from "../workstation/governance/AssistantAuditSubSection";
import { EmptyState, ErrorBanner, Skeleton } from "../components/ui";

export type GovernanceSource = {
  surface: string;
  existingSource: string;
  readSeam: string;
  p01Posture: string;
};

export type GovernanceStatusItem = {
  label: string;
  value: string;
  detail: string;
};

export const UI007_GOVERNANCE_SOURCES: GovernanceSource[] = [
  {
    surface: "Governance status",
    existingSource: "Constitutional records, UI shell posture, route inventory, API catalogue, plugin contracts",
    readSeam: "UI shell constants + GET /api/v1/institutional-platform/route-inventory + GET /api/v1/institutional-platform/api-catalogue + GET /api/v1/institutional-platform/plugin-contracts",
    p01Posture: "Read-only governance posture display is now rendered in P02; deeper records remain later phases.",
  },
  {
    surface: "Audit events",
    existingSource: "audit_events",
    readSeam: "GET /api/v1/persistence/audit-events",
    p01Posture: "P03 renders existing rows and refusal reason-codes as stored text.",
  },
  {
    surface: "Production status",
    existingSource: "Doc 11 and ITRGA governance records",
    readSeam: "Canonical governance records; no production-status API action",
    p01Posture: "Read-only posture: Production NOT CERTIFIED and Doc 11 HELD.",
  },
  {
    surface: "Platform health",
    existingSource: "Health service",
    readSeam: "GET /api/v1/health",
    p01Posture: "Inventory only; liveness display remains a later authorized phase.",
  },
  {
    surface: "Runtime readiness",
    existingSource: "Readiness service",
    readSeam: "GET /api/v1/ready",
    p01Posture: "Inventory only; runtime readiness is never production status.",
  },
  {
    surface: "Observability metrics",
    existingSource: "Observability service",
    readSeam: "GET /api/v1/metrics",
    p01Posture: "Inventory only; backend-sanitized values remain read-only.",
  },
  {
    surface: "Persistence stats",
    existingSource: "Persistence service",
    readSeam: "GET /api/v1/persistence/stats",
    p01Posture: "Inventory only; counts and stats remain read-only.",
  },
  {
    surface: "System version",
    existingSource: "System service and settings",
    readSeam: "GET /api/v1/system/info",
    p01Posture: "Inventory only; version display remains read-only.",
  },
  {
    surface: "RBAC vocabulary",
    existingSource: "Institutional platform permissions",
    readSeam: "GET /api/v1/institutional-platform/rbac/permissions",
    p01Posture: "Inventory only; permission vocabulary remains read-only.",
  },
  {
    surface: "Operator scope",
    existingSource: "Current operator institutional scope records",
    readSeam: "GET /api/v1/institutional-platform/operator-scope-records",
    p01Posture: "Inventory only; current-operator scope remains read-only.",
  },
  {
    surface: "Evidence records",
    existingSource: "Build Orders, delivery reports, ITRGA reviews, and evidence packs",
    readSeam: "Canonical repository governance records and first-party evidence manifests",
    p01Posture: "Inventory only; evidence viewer remains a later authorized phase.",
  },
  {
    surface: "Validation summaries",
    existingSource: "Existing research, intelligence, validation, and artifact read seams",
    readSeam: "Existing UI-004/UI-006 artifact/report read APIs",
    p01Posture: "Inventory only; stored verdicts, samples, scope, and limitations remain verbatim.",
  },
];

export const UI007_GUARDRAILS: GovernanceStatusItem[] = [
  {
    label: "Gate posture",
    value: "Gate CLOSED",
    detail: "Read-only constitutional fact. No UI affordance changes this state.",
  },
  {
    label: "Production posture",
    value: "Production NOT CERTIFIED",
    detail: "Doc 11 remains HELD. Runtime readiness is separate from production status.",
  },
  {
    label: "PostCSS high residual",
    value: "TD-UI-POSTCSS-HIGH CLOSED",
    detail: "Remediated by dedicated dependency Build Order; no longer a Doc 11 high-severity blocker.",
  },
  {
    label: "Workspace posture",
    value: "Read-only governance display",
    detail: "P03 adds audit row display only. AXIOM does not act.",
  },
] as const;

export const UI007_GOVERNANCE_STATUS: GovernanceStatusItem[] = [
  {
    label: "Governance Gate",
    value: "Gate CLOSED",
    detail: "Constitutional state rendered as display-only text. There is no UI affordance that changes this state.",
  },
  {
    label: "Workspace route",
    value: "/governance",
    detail: "Single protected Governance & Evidence route under the UI-001/UI-002 shell contract.",
  },
  {
    label: "Governance boundary",
    value: "G-1…G-7 read-only",
    detail: "Governance, audit, production, validation, readiness, and evidence facts are displayed without mutation.",
  },
];

export const UI007_CERTIFICATION_STATUS: GovernanceStatusItem[] = [
  {
    label: "Production status",
    value: "Production NOT CERTIFIED",
    detail: "Current canonical posture under Doc 11. UI-007 displays the fact only.",
  },
  {
    label: "Doc 11 track",
    value: "HELD",
    detail: "Production Readiness Certification remains a separate ITRGA governance track.",
  },
  {
    label: "Doc 11 outcome vocabulary",
    value: "CERTIFIED · CERTIFIED WITH CONDITIONS · DEFERRED · NOT CERTIFIED",
    detail: "Outcome vocabulary is shown for transparency; the current status remains NOT CERTIFIED.",
  },
  {
    label: "PostCSS high residual",
    value: "TD-UI-POSTCSS-HIGH CLOSED / REMEDIATED",
    detail: "The high-severity PostCSS blocker is recorded as remediated by ITRGA; it is no longer an open production-readiness blocker.",
  },
];

export const UI007_STANDING_RESIDUALS: GovernanceStatusItem[] = [
  {
    label: "TD-UI-REACTROUTER-MODERATE",
    value: "OPEN · MODERATE · NON-BLOCKING",
    detail: "React Router moderate advisories remain disclosed below the high audit gate.",
  },
  {
    label: "TD-W7-U07-RATE-GUARD",
    value: "DEFERRED",
    detail: "Existing readiness residual remains tracked for a future dedicated hardening decision.",
  },
  {
    label: "TD-W6-CI-AUDIT",
    value: "TRACKED",
    detail: "Network audit environment flake class remains tracked and must be disclosed if it recurs.",
  },
  {
    label: "UI-002-P04b",
    value: "INDEPENDENT",
    detail: "Independent non-blocking item carried outside the UI-007-P03 surface.",
  },
  {
    label: "TD-UI005-COMPLETION-TIMEOUT",
    value: "OPEN · LOW · CONTENTION-FRAGILE",
    detail: "The UI-005 completion harness has a fixed timeout that can expire under CI contention; it is not a P05 behaviour verdict.",
  },
  {
    label: "TD-AXIOM-GIT-PROVENANCE",
    value: "OPEN · HIGH · PRE-CERTIFICATION BLOCKER",
    detail: "Single-commit repository provenance requires a dedicated baseline/tagging Build Order before Doc 11 certification.",
  },
];

export function reasonCodeFor(event: AuditEvent): string {
  const details = event.details ?? {};
  const direct = details.reason_code;
  if (typeof direct === "string" && direct.trim()) return direct;
  const refusal = Object.values(details).find(
    (value) => typeof value === "string" && /^[A-Z0-9_]+_REFUSED$/.test(value),
  );
  return typeof refusal === "string" ? refusal : "—";
}

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
    <section className="panel span-12" aria-label="Read-only audit explorer">
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

        <article className="artifact-detail-card" aria-label="Read-only audit event detail">
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
              <section aria-label="Audit event detail payload">
                <h4>Details payload</h4>
                <pre className="mono">{detailText(selectedEvent.details)}</pre>
              </section>
              <section aria-label="Refusal reason-code viewer">
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


type EvidenceManifestRecord = {
  id: string;
  recordType: string;
  status: string;
  methodVersion: string;
  observedCount: string;
  scope: string;
  uncertainty: string;
  limitations: string[];
  sourceIds: string[];
  lineage: string;
  auditReference: string;
  reportHash: string;
  recordedAt: string;
};

/**
 * First-party evidence index. Each value is copied from an existing AXIOM
 * governance/evidence record; this component never discovers files at runtime.
 */
export const UI007_EVIDENCE_MANIFEST: EvidenceManifestRecord[] = [
  {
    id: "UI-007-P03",
    recordType: "ITRGA determination",
    status: "APPROVED WITH OBSERVATIONS",
    methodVersion: "UI-007-P03",
    observedCount: "5 named tests",
    scope: "Read-Only Audit Explorer & Refusal Reason-Code Viewer",
    uncertainty: "OBS-P03-1 regression and CI transcript required at P04",
    limitations: [
      "F-1 false-positive evidence grep halted the prior transcript",
      "OBS-P03-2 requires endpoint-declaration-focused grep hygiene",
    ],
    sourceIds: [
      "docs/build-orders/ITRGA_REVIEW_UI-007-P03.md",
      "docs/evidence/UI-007-P03_NAMED_VITEST.txt",
      "docs/evidence/UI-007-P03_OPERATOR_EVIDENCE_COMMANDS.md",
    ],
    lineage: "UI-007 design review → P01 → P02 → P03",
    auditReference: "PLUGIN_CONTRACT_IMPORT_REFUSED",
    reportHash: "Not recorded",
    recordedAt: "2026-07-27",
  },
  {
    id: "TD-UI-POSTCSS-HIGH",
    recordType: "ITRGA dependency remediation determination",
    status: "APPROVED — CLOSED",
    methodVersion: "vite ^8.1.4 · vitest ^4.1.10 · @vitejs/plugin-react ^6.0.3",
    observedCount: "414 backend tests · 56 frontend files / 251 tests",
    scope: "High-severity PostCSS dependency advisory remediation",
    uncertainty: "TD-UI-REACTROUTER-MODERATE remains a separately tracked moderate residual",
    limitations: [
      "F-1 records the accepted toolchain-major-upgrade scope correction",
      "Production Readiness Certification remains a separate Doc 11 track",
    ],
    sourceIds: [
      "docs/build-orders/ITRGA_REVIEW_TD-UI-POSTCSS-HIGH-REMEDIATION.md",
      "docs/evidence/TD-UI-POSTCSS-HIGH_FRONTEND_FULL_VITEST.txt",
      "docs/evidence/TD-UI-POSTCSS-HIGH_REMEDIATION_OPERATOR_EVIDENCE_COMMANDS.md",
    ],
    lineage: "TD-UI-POSTCSS-HIGH remediation Build Order → ITRGA determination",
    auditReference: "Not recorded",
    reportHash: "Not recorded",
    recordedAt: "2026-07-27",
  },
];

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
    <section className="panel span-12" aria-label="Read-only evidence viewer">
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
    <section className="panel span-12" aria-label="Read-only validation summary panels">
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


export type ReadinessPostureRecord = {
  item: string;
  status: string;
  technicalDebtId: string | null;
  rationale: string;
  source: string;
};

/** Existing W7-U07 readiness posture records, transcribed without reinterpretation. */
export const UI007_READINESS_POSTURE_RECORDS: ReadinessPostureRecord[] = [
  {
    item: "abuse_rate_guard",
    status: "formally_deferred",
    technicalDebtId: "TD-W7-U07-RATE-GUARD",
    rationale:
      "No rate-limit dependency or storage is introduced in W7-U07. Existing auth, RBAC, operator scoping, CI, and no-execution/Gate checks remain active. A future rate guard requires a dedicated dependency/storage spike.",
    source: "Existing W7-U07 readiness constant",
  },
  {
    item: "ADMIN_DEFAULT_CREDENTIAL_REJECTED_WITH_INSECURE_DEV_OFF",
    status: "True",
    technicalDebtId: null,
    rationale: "Existing W7-U07 production-framing rejection proof; no default value is disclosed in this workspace.",
    source: "docs/evidence/W7-U07_ADMIN_DEFAULT_REJECTION.txt",
  },
] as const;

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
    <section className="panel span-12" aria-label="Platform health readiness version and API posture">
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

      <section className="panel span-12" aria-label="Governance workspace frame">
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

      <section className="panel span-12" aria-label="Certification status read-only panel">
        <h2>Certification Status</h2>
        <p className="muted">
          Production Readiness Certification remains an out-of-band Doc 11 governance track. This
          panel displays the current status and outcome vocabulary without any action affordance.
        </p>
        <StatusGrid items={UI007_CERTIFICATION_STATUS} />
      </section>

      <section className="panel span-12" aria-label="Residual status read-only panel">
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

      <section className="panel span-12" aria-label="Read-only governance guardrails">
        <h2>Read-Only Governance Boundary</h2>
        <p className="muted">
          G-1 through G-7 are rendered as operator-visible constraints. All entries are informational.
        </p>
        <StatusGrid items={UI007_GUARDRAILS} />
      </section>

      <section className="panel span-12" aria-label="UI-007 governed data-source inventory">
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

      <section className="panel span-12" aria-label="Forbidden governance affordance notice">
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

export function GovernanceEvidencePage() {
  const [auditEvents, setAuditEvents] = useState<AuditEvent[]>([]);
  const [auditLoading, setAuditLoading] = useState(false);
  const [auditError, setAuditError] = useState<string | null>(null);
  const [validationBundle, setValidationBundle] = useState<InstitutionalIntelligenceBundle | null>(null);
  const [validationLoading, setValidationLoading] = useState(false);
  const [validationError, setValidationError] = useState<string | null>(null);
  const [platformOperations, setPlatformOperations] = useState<PlatformOperationsEvidence | null>(null);
  const [platformOperationsLoading, setPlatformOperationsLoading] = useState(false);
  const [platformOperationsError, setPlatformOperationsError] = useState<string | null>(null);

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

  useEffect(() => {
    void loadAuditEvents();
    void loadValidationRecords();
    void loadPlatformOperations();
  }, []);

  return (
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
    />
  );
}
