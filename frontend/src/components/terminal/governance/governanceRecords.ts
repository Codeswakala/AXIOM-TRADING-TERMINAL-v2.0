/**
 * governanceRecords — UI-CONV-P03 item 5 relocation
 *
 * Declared governance state relocated from pages/GovernanceEvidencePage.tsx:
 * the UI007_* constant tables, their record types, and reasonCodeFor.
 * These constants are DECLARED governance state (gate posture, certification
 * status, standing residuals, evidence manifest, readiness posture records),
 * not fabricated statistics — per BUILD_DIRECTIVE_UI-CONV-P03_ITEM5 §2.2 they
 * are the correct kind of hardcoding and are NOT to be made dynamic.
 * reasonCodeFor is constitutional logic: the "—" fallback is an honest
 * absence marker and is preserved verbatim (M2).
 */

import type { AuditEvent } from "../../../api/client";

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
