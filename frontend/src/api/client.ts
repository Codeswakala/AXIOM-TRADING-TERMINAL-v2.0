/**
 * Frontend API client with optional Bearer auth.
 */

import { getAccessToken } from "../auth/tokenStorage";
import type { LiveMarketStats } from "../live/types";

export type ServiceCheck = {
  name: string;
  status: "up" | "down" | "degraded" | "stub";
  detail?: string | null;
  latency_ms?: number | null;
};

export type HealthResponse = {
  status: "ok" | "error";
  service: string;
  version: string;
  environment: string;
  timestamp: string;
  message: string;
  latency_ms?: number | null;
};

export type ReadinessResponse = {
  status: "ready" | "not_ready";
  service: string;
  version: string;
  environment: string;
  timestamp: string;
  checks: ServiceCheck[];
};

export type AuditEvent = {
  id: string;
  category: string;
  action: string;
  actor: string;
  message: string;
  resource_type: string | null;
  resource_id: string | null;
  details: Record<string, unknown> | null;
  created_at: string;
};

export type SystemInfoResponse = {
  name: string;
  version: string;
  environment: string;
  wave: string;
  unit: string;
  architecture_version: string;
  description: string;
  timestamp: string;
};

export type PlatformMetricsResponse = {
  service: string;
  version: string;
  environment: string;
  observability: {
    process: { pid: number; uptime_seconds: number };
    http: {
      requests_total: number;
      errors_total: number;
      latency_avg_ms: number;
      latency_max_ms: number;
    };
    governance: { gate_refusals_total: number };
  };
  database: { status: string; latency_ms: number | null; backend: string; pool: Record<string, unknown> };
  live_market: {
    running: boolean;
    connected: boolean;
    messages_received: number;
    persist_count: number;
    persist_errors: number;
    lag_ms: number | null;
    subscribers: number;
  };
};

export type DatabaseStatsResponse = {
  backend: string;
  database_url_scheme: string;
  pool: Record<string, unknown>;
  candle_count: number;
  audit_count: number;
};

export type RouteInventoryResponse = {
  service: string;
  version: string;
  routes: Array<Record<string, unknown>>;
  actuation_surface_present: boolean;
  governance_gate_capability_present: boolean;
};

export type RbacPermissionsResponse = {
  policy: string;
  roles: Record<string, string[]>;
  forbidden_capabilities_present: boolean;
};

export type ApiCatalogueResponse = {
  service: string;
  catalogue_version: string;
  api_version: string;
  routes: Array<Record<string, unknown>>;
  route_count: number;
  actuation_surface_present: boolean;
  governance_gate_capability_present: boolean;
  abuse_guard: { status: string; reason: string };
  persistence: { catalogue_table_persisted: boolean; alembic_head_expected: string };
};

export type PluginContractsResponse = {
  service: string;
  contract_version: string;
  contracts: Array<Record<string, unknown>>;
  capability_allowlist: string[];
  dynamic_code_execution_enabled: boolean;
  third_party_plugin_execution_enabled: boolean;
  plugin_execution_audit_table_present: boolean;
  governance_gate_capability_present: boolean;
};

export type PlatformOperationsEvidence = {
  health: HealthResponse;
  readiness: ReadinessResponse;
  metrics: PlatformMetricsResponse;
  persistenceStats: DatabaseStatsResponse;
  systemInfo: SystemInfoResponse;
  routeInventory: RouteInventoryResponse;
  rbac: RbacPermissionsResponse;
  apiCatalogue: ApiCatalogueResponse;
  pluginContracts: PluginContractsResponse;
};

export type Operator = {
  id: string;
  username: string;
  role: string;
  is_active: boolean;
  display_name: string | null;
  last_login_at: string | null;
  created_at: string;
};

export type TokenBundle = {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
};

export type LoginResponse = {
  tokens: TokenBundle;
  operator: Operator;
};

export type AdvisorySignalState = "emitted" | "withheld" | "warning" | "expired" | "superseded";

export type AnalyticsUncertainty = {
  method: string;
  lower: number;
  upper: number;
  confidence_level: number;
  sample_count: number;
};

export type AdvisoryAnalyticsMetric = {
  key: string;
  label: string;
  value: number;
  unit: string;
  sample_count: number;
  uncertainty: AnalyticsUncertainty;
  interpretation: string;
};

export type ConfidenceBand = {
  label: string;
  lower: number;
  upper: number;
  sample_count: number;
  average_calibrated_confidence: number | null;
  calibration_status: string;
  uncertainty: AnalyticsUncertainty;
  unreliable: boolean;
  economic_context: string;
};

export type AdvisoryAnalyticsResponse = {
  generated_from: string;
  disclaimer: string;
  metrics: AdvisoryAnalyticsMetric[];
  confidence_bands: ConfidenceBand[];
  notes: string[];
};

export type MonitoringAlert = {
  alert_id: string;
  created_at: string;
  alert_type: string;
  severity: string;
  subject_type: string;
  subject_id: string;
  market_class: string | null;
  symbol: string | null;
  timeframe: string | null;
  model_artifact_id: string | null;
  signal_id: string | null;
  summary: string;
  evidence: Record<string, unknown>;
  lineage: Record<string, unknown>;
  acknowledged: boolean;
  acknowledged_at: string | null;
  acknowledged_by: string | null;
  audit_correlation_id: string;
};

export type InstitutionalReport = {
  id: string;
  artifact_type?: string;
  method_version?: string;
  sample_count?: number;
  research_status?: string;
  report_hash?: string;
  limitations?: string[];
  uncertainty?: Record<string, unknown>;
  economic_usefulness?: Record<string, unknown>;
  economic_meaning?: Record<string, unknown>;
  metrics?: Record<string, unknown>;
  results?: Record<string, unknown>;
  input_lineage?: Record<string, unknown>;
  created_at?: string;
  [key: string]: unknown;
};

export type InstitutionalIntelligenceBundle = {
  relation: InstitutionalReport[];
  context: InstitutionalReport[];
  hypothetical: InstitutionalReport[];
  risk: InstitutionalReport[];
  validation: InstitutionalReport[];
};

export type SimulatedExecutionRun = {
  run_id: string;
  created_at: string;
  operator_id: string;
  simulation_mode: string;
  simulation_policy_version: string;
  input_artifact_ids: string[];
  replay_scope: Record<string, unknown>;
  fill_model_name: string;
  fill_model_version: string;
  assumptions: Record<string, unknown>;
  limitations: string[];
  research_status: string;
  simulation_disclaimer: string;
  audit_correlation_id: string;
};

export type SimulatedFillEvent = {
  simulated_fill_id: string;
  run_id: string;
  created_at: string;
  simulation_mode: string;
  market_class: string;
  symbol: string;
  timeframe: string;
  as_of_time: string;
  simulated_research_direction: string;
  simulated_units: number;
  requested_reference_price: number;
  simulated_fill_price: number;
  simulated_slippage_bps: number;
  source_candle_ids: string[];
  fill_model_name: string;
  fill_model_version: string;
  research_status: string;
  simulation_disclaimer: string;
  audit_correlation_id: string;
};

export type SimulatedPaperLedgerEntry = {
  ledger_entry_id: string;
  created_at: string;
  simulation_mode: string;
  run_id: string;
  simulated_fill_id: string;
  operator_id: string;
  ledger_event_type: string;
  simulated_research_direction: string;
  simulated_units: number;
  simulated_entry_value: number;
  simulated_exit_value: number;
  simulated_return_estimate: number;
  uncertainty: Record<string, unknown>;
  limitations: string[];
  research_status: string;
  simulation_disclaimer: string;
  audit_correlation_id: string;
};

export type ExecutionRiskResearchReport = {
  report_id: string;
  created_at: string;
  simulation_mode: string;
  input_artifact_ids: string[];
  simulated_request_summary: Record<string, unknown>;
  risk_metrics: Record<string, unknown>;
  uncertainty: Record<string, unknown>;
  limitations: string[];
  economic_usefulness: Record<string, unknown>;
  research_status: string;
  simulation_disclaimer: string;
  audit_correlation_id: string;
};

export type ExecutionResearchExperiment = {
  experiment_id: string;
  created_at: string;
  simulation_mode: string;
  operator_id: string;
  experiment_title: string;
  pre_registration_plan: Record<string, unknown>;
  plan_hash: string;
  as_of_time: string;
  as_of_window: Record<string, unknown>;
  replay_input_lineage: Record<string, unknown>;
  included_scope_summary: Record<string, unknown>;
  uncertainty: Record<string, unknown>;
  limitations: string[];
  research_status: string;
  simulation_disclaimer: string;
  audit_correlation_id: string;
};

export type SimulatedExecutionAnalyticsReport = {
  report_id: string;
  created_at: string;
  simulation_mode: string;
  analytics_type: string;
  included_scope: Record<string, unknown>;
  sample_count: number;
  metrics: Record<string, unknown>;
  uncertainty: Record<string, unknown>;
  limitations: string[];
  economic_usefulness: Record<string, unknown>;
  report_hash: string;
  source_artifact_ids: string[];
  research_status: string;
  simulation_disclaimer: string;
  audit_correlation_id: string;
};

export type ExecutionResearchBundle = {
  runs: SimulatedExecutionRun[];
  fills: SimulatedFillEvent[];
  ledger: SimulatedPaperLedgerEntry[];
  riskReports: ExecutionRiskResearchReport[];
  experiments: ExecutionResearchExperiment[];
  analyticsReports: SimulatedExecutionAnalyticsReport[];
};

/** SURF-P01: detail shape of `GET /simulated-runs/{run_id}` (run + its fills). */
export type SimulatedExecutionRunDetail = {
  run: SimulatedExecutionRun;
  fills: SimulatedFillEvent[];
};

export type OperatorWorkspacePreference = {
  preference_id: string;
  created_at: string;
  updated_at: string;
  operator_id: string;
  workspace_key: string;
  layout_config: Record<string, unknown>;
  visible_modules: string[];
  theme_config: Record<string, unknown>;
  research_status: string;
  metadata: Record<string, unknown>;
  audit_correlation_id: string;
};

export type OperatorWorkspacePreferenceWrite = {
  workspace_key?: string;
  layout_config?: Record<string, unknown>;
  visible_modules?: string[];
  theme_config?: Record<string, unknown>;
  metadata?: Record<string, unknown>;
};

export type ResearchCollection = {
  collection_id: string;
  created_at: string;
  updated_at: string;
  operator_id: string;
  name: string;
  description: string | null;
  research_status: string;
  audit_correlation_id: string;
};

export type ResearchCollectionMember = {
  member_id: string;
  created_at: string;
  operator_id: string;
  collection_id: string;
  artifact_type: string;
  artifact_id: string;
  audit_correlation_id: string;
};

export type ResearchTag = {
  tag_id: string;
  created_at: string;
  operator_id: string;
  artifact_type: string;
  artifact_id: string;
  tag: string;
  audit_correlation_id: string;
};

export type ResearchManagementBundle = {
  collections: ResearchCollection[];
  members: ResearchCollectionMember[];
  tags: ResearchTag[];
  supported_artifact_types: string[];
  posture: string;
};

export type ResearchCollectionWrite = {
  name: string;
  description?: string | null;
};

export type ResearchArtifactReferenceWrite = {
  artifact_type: string;
  artifact_id: string;
};

export type ResearchTagWrite = ResearchArtifactReferenceWrite & {
  tag: string;
};

export type PortfolioResearchMetric = {
  key: string;
  label: string;
  value: number;
  sample_count: number;
  source_artifact_ids: string[];
  uncertainty: Record<string, unknown>;
  limitations: string[];
  economic_usefulness: Record<string, unknown>;
};

export type PortfolioResearchDashboard = {
  operator_id: string;
  generated_at: string;
  research_status: string;
  disclaimer: string;
  aggregate_cards: PortfolioResearchMetric[];
  included_scope: Record<string, unknown>;
  limitations: string[];
  economic_usefulness: Record<string, unknown>;
  source_artifact_ids: string[];
};

export type AdvancedResearchReport = {
  report_id: string;
  method_version: string;
  operator_id: string;
  research_status: string;
  disclaimer: string;
  included_scope: Record<string, unknown>;
  sections: Array<Record<string, unknown>>;
  source_artifact_ids: string[];
  limitations: string[];
  economic_usefulness: Record<string, unknown>;
  report_hash: string;
  export_preview_markdown: string;
  persisted: boolean;
};

export type ManualJournalEntry = {
  journal_id: string;
  created_at: string;
  updated_at?: string;
  operator_id: string;
  title: string;
  reflection_text: string;
  linked_plan_id: string | null;
  linked_signal_ids: string[];
  linked_report_ids: string[];
  emotion_tags: string[];
  process_tags: string[];
  lesson_notes: string | null;
  research_disclaimer: string;
  research_status: string;
  audit_correlation_id: string;
};

export type ManualJournalEntryWrite = {
  title: string;
  reflection_text: string;
  linked_plan_id?: string | null;
  linked_signal_ids?: string[];
  linked_report_ids?: string[];
  emotion_tags?: string[];
  process_tags?: string[];
  lesson_notes?: string | null;
};

export type TradePlanNote = {
  plan_id: string;
  created_at: string;
  updated_at: string;
  operator_id: string;
  title: string;
  market_context: string;
  hypothesis: string;
  linked_signal_ids: string[];
  linked_report_ids: string[];
  scenario_notes: string | null;
  risk_notes: string | null;
  invalidating_conditions_text: string | null;
  decision_status: "draft" | "archived" | "reviewed" | string;
  research_disclaimer: string;
  research_status: string;
  audit_correlation_id: string;
};

export type TradePlanNoteWrite = {
  title: string;
  market_context: string;
  hypothesis: string;
  linked_signal_ids?: string[];
  linked_report_ids?: string[];
  scenario_notes?: string | null;
  risk_notes?: string | null;
  invalidating_conditions_text?: string | null;
  decision_status?: "draft" | "archived" | "reviewed";
};

export type PortfolioRiskReport = {
  id: string;
  created_at: string;
  artifact_type: string;
  method_version: string;
  market_class: string;
  symbol: string;
  timeframe: string;
  as_of_start: string;
  as_of_end: string;
  sample_count: number;
  max_drawdown: number;
  realized_volatility: number;
  stress_loss: number;
  metrics: Record<string, any>;
  uncertainty: Record<string, any>;
  assumptions: Record<string, any>;
  economic_usefulness: Record<string, any>;
  config: Record<string, any>;
  input_lineage: Record<string, any>;
  source_artifact_ids: string[];
  market_scope: Record<string, any>;
  results: Record<string, any>;
  limitations: string[];
  report_hash: string;
  research_status: string;
  created_by: string;
  audit_correlation_id: string;
  notes: string | null;
};

export type ScenarioReport = {
  id: string;
  created_at: string;
  artifact_type: string;
  method_version: string;
  market_class: string;
  symbol: string;
  timeframe: string;
  as_of_start: string;
  as_of_end: string;
  sample_count: number;
  scenario_name: string;
  hypothetical_return: number;
  scenario_result: Record<string, unknown>;
  assumptions: Record<string, unknown>;
  inputs: Record<string, unknown>;
  uncertainty: Record<string, unknown>;
  economic_usefulness: Record<string, unknown>;
  config: Record<string, unknown>;
  input_lineage: Record<string, unknown>;
  source_artifact_ids: string[];
  market_scope: Record<string, unknown>;
  results: Record<string, unknown>;
  limitations: string[];
  report_hash: string;
  research_status: string;
  created_by: string;
  audit_correlation_id: string;
  notes: string | null;
};

export type ChartResearchAnnotation = {
  id: string;
  created_at: string;
  operator_id: string;
  artifact_type: "chart_research_annotation" | "chart_research_drawing" | string;
  chart_context: Record<string, unknown>;
  content: Record<string, unknown>;
  source_artifact_ids: string[];
  provenance: Record<string, unknown>;
  uncertainty: Record<string, unknown>;
  disclaimer: string;
  research_status: string;
  audit_correlation_id: string;
};

export type ChartResearchAnnotationCreate = {
  artifact_type?: "chart_research_annotation" | "chart_research_drawing";
  chart_context: Record<string, unknown>;
  content: Record<string, unknown>;
  source_artifact_ids: string[];
  provenance?: Record<string, unknown>;
  uncertainty?: Record<string, unknown>;
  research_status?: "research_only";
};

export type AdvisorySignal = {
  signal_id: string;
  created_at: string;
  as_of_time: string;
  market_class: string;
  provider: string;
  symbol: string;
  timeframe: string;
  model_artifact_id: string;
  model_version: string;
  feature_set_version: string;
  experiment_id: string;
  statistical_report_id: string | null;
  calibration_report_id: string | null;
  economic_report_id: string | null;
  generalization_report_id: string | null;
  inference_input_hash: string;
  raw_score: number | null;
  calibrated_confidence: number | null;
  input_staleness_seconds: number | null;
  signal_validity_seconds: number | null;
  expires_at: string | null;
  freshness_status: string | null;
  signal_direction: string;
  signal_state: AdvisorySignalState;
  state_reason: string;
  eligibility_reasons: string[];
  operating_domain_status: string;
  calibration_status: string;
  economic_verdict: string;
  risk_notes: string | null;
  rationale: string;
  explainability_summary: Record<string, unknown>;
  state_transition_history: string[];
  audit_correlation_id: string;
};

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "";

async function request<T>(
  path: string,
  init: RequestInit = {},
  auth = false,
): Promise<T> {
  const headers = new Headers(init.headers);
  headers.set("Accept", "application/json");
  if (init.body && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }
  if (auth) {
    const token = getAccessToken();
    if (token) headers.set("Authorization", `Bearer ${token}`);
  }
  const response = await fetch(`${API_BASE}${path}`, { ...init, headers });
  if (!response.ok) {
    let detail = `Request failed (${response.status}) for ${path}`;
    try {
      const err = (await response.json()) as { detail?: string };
      if (err.detail) detail = String(err.detail);
    } catch {
      /* ignore */
    }
    // SURF-P03: attach the HTTP status to the error so callers can
    // distinguish an access denial (403) from a transport failure. The error
    // message is unchanged — existing callers are unaffected.
    const error = new Error(detail) as Error & { status?: number };
    error.status = response.status;
    throw error;
  }
  if (response.status === 204) {
    return undefined as T;
  }
  return (await response.json()) as T;
}

export type V2ModeResponse = {
  mode: string;
  valid_modes: string[];
  deferred_modes: string[];
};

/** FE-U02 (PC-FEU02-1 C3): authed read of the platform's locked mode
 *  configuration — powers the chrome mode-badge verification mark. */
export function fetchV2Mode(): Promise<V2ModeResponse> {
  return request<V2ModeResponse>("/api/v1/v2/mode", {}, true);
}

export function fetchHealth(): Promise<HealthResponse> {
  return request<HealthResponse>("/health");
}

export function fetchReadiness(): Promise<ReadinessResponse> {
  return request<ReadinessResponse>("/ready");
}

export function fetchAuditEvents(params: { category?: string; limit?: number } = {}): Promise<AuditEvent[]> {
  const query = new URLSearchParams();
  if (params.category) query.set("category", params.category);
  query.set("limit", String(params.limit ?? 50));
  return request<AuditEvent[]>(`/api/v1/persistence/audit-events?${query.toString()}`, {}, true);
}

export function fetchSystemInfo(): Promise<SystemInfoResponse> {
  return request<SystemInfoResponse>("/api/v1/system/info", {}, true);
}

export function fetchPlatformMetrics(): Promise<PlatformMetricsResponse> {
  return request<PlatformMetricsResponse>("/api/v1/metrics", {}, true);
}

export function fetchDatabaseStats(): Promise<DatabaseStatsResponse> {
  return request<DatabaseStatsResponse>("/api/v1/persistence/stats", {}, true);
}

export function fetchRouteInventory(): Promise<RouteInventoryResponse> {
  return request<RouteInventoryResponse>(
    "/api/v1/institutional-platform/route-inventory",
    {},
    true,
  );
}

export function fetchRbacPermissions(): Promise<RbacPermissionsResponse> {
  return request<RbacPermissionsResponse>(
    "/api/v1/institutional-platform/rbac/permissions",
    {},
    true,
  );
}

export function fetchApiCatalogue(): Promise<ApiCatalogueResponse> {
  return request<ApiCatalogueResponse>(
    "/api/v1/institutional-platform/api-catalogue",
    {},
    true,
  );
}

export function fetchPluginContracts(): Promise<PluginContractsResponse> {
  return request<PluginContractsResponse>(
    "/api/v1/institutional-platform/plugin-contracts",
    {},
    true,
  );
}

/** SURF-P03: per-operator institutional scope record (derived, read-only). */
export type OperatorScopeRecord = {
  operator_id: string;
  username: string;
  role: string;
  record_type: string;
  research_status: string;
};

/** SURF-P03: typed result of a scope-records read. A 403 from the backend is
 * an access denial and must be rendered as such (M3), never as empty data or
 * as a transport error. */
export type OperatorScopeListResult =
  | { kind: "ok"; records: OperatorScopeRecord[] }
  | { kind: "denied"; detail: string }
  | { kind: "error"; detail: string };

export type OperatorScopeRecordResult =
  | { kind: "ok"; record: OperatorScopeRecord }
  | { kind: "denied"; detail: string }
  | { kind: "error"; detail: string };

/** SURF-P03 S2: list the current operator's institutional scope records.
 * The backend enforces institutional.operator_scope.read independently; the
 * UI renders whatever it returns, including the 403 (R3). */
export async function fetchOperatorScopeRecords(): Promise<OperatorScopeListResult> {
  try {
    const records = await request<OperatorScopeRecord[]>(
      "/api/v1/institutional-platform/operator-scope-records",
      {},
      true,
    );
    return { kind: "ok", records };
  } catch (err) {
    const status = (err as Error & { status?: number }).status;
    const detail = err instanceof Error ? err.message : "Failed to load scope records";
    return status === 403 ? { kind: "denied", detail } : { kind: "error", detail };
  }
}

/** SURF-P03 S2: read one scope record by operator id (own id only — the
 * backend denies cross-operator reads with 403). */
export async function fetchOperatorScopeRecord(
  operatorId: string,
): Promise<OperatorScopeRecordResult> {
  try {
    const record = await request<OperatorScopeRecord>(
      `/api/v1/institutional-platform/operator-scope-records/${encodeURIComponent(operatorId)}`,
      {},
      true,
    );
    return { kind: "ok", record };
  } catch (err) {
    const status = (err as Error & { status?: number }).status;
    const detail = err instanceof Error ? err.message : "Failed to load scope record";
    return status === 403 ? { kind: "denied", detail } : { kind: "error", detail };
  }
}

export async function fetchPlatformOperationsEvidence(): Promise<PlatformOperationsEvidence> {
  const [
    health,
    readiness,
    metrics,
    persistenceStats,
    systemInfo,
    routeInventory,
    rbac,
    apiCatalogue,
    pluginContracts,
  ] = await Promise.all([
    fetchHealth(),
    fetchReadiness(),
    fetchPlatformMetrics(),
    fetchDatabaseStats(),
    fetchSystemInfo(),
    fetchRouteInventory(),
    fetchRbacPermissions(),
    fetchApiCatalogue(),
    fetchPluginContracts(),
  ]);
  return {
    health,
    readiness,
    metrics,
    persistenceStats,
    systemInfo,
    routeInventory,
    rbac,
    apiCatalogue,
    pluginContracts,
  };
}

export function login(username: string, password: string): Promise<LoginResponse> {
  return request<LoginResponse>("/api/v1/auth/login", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
}

export function refreshTokens(refreshToken: string): Promise<TokenBundle> {
  return request<TokenBundle>("/api/v1/auth/refresh", {
    method: "POST",
    body: JSON.stringify({ refresh_token: refreshToken }),
  });
}

export function logoutRequest(): Promise<{ status: string }> {
  return request<{ status: string }>("/api/v1/auth/logout", { method: "POST" }, true);
}

export function fetchCurrentOperator(): Promise<Operator> {
  return request<Operator>("/api/v1/operator/me", {}, true);
}

export function fetchLiveMarketStats(): Promise<LiveMarketStats> {
  return request<LiveMarketStats>("/api/v1/market/live/stats", {}, true);
}

export function fetchAdvisorySignals(params: {
  signal_id?: string;
  model_artifact_id?: string;
  market_class?: string;
  symbol?: string;
  timeframe?: string;
  signal_state?: AdvisorySignalState;
  current_only?: boolean;
  limit?: number;
} = {}): Promise<AdvisorySignal[]> {
  const q = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined && value !== "") q.set(key, String(value));
  }
  return request<AdvisorySignal[]>(`/api/v1/signals/history?${q.toString()}`, {}, true);
}

export function fetchAdvisorySignal(signalId: string): Promise<AdvisorySignal> {
  return request<AdvisorySignal>(
    `/api/v1/signals/history/${encodeURIComponent(signalId)}`,
    {},
    true,
  );
}

export function fetchAdvisoryAnalytics(limit = 500): Promise<AdvisoryAnalyticsResponse> {
  return request<AdvisoryAnalyticsResponse>(
    `/api/v1/analytics/advisory-performance?limit=${encodeURIComponent(String(limit))}`,
    {},
    true,
  );
}

export function fetchScenarioReports(limit = 50): Promise<ScenarioReport[]> {
  return request<ScenarioReport[]>(
    `/api/v1/intelligence/scenario-reports?limit=${encodeURIComponent(String(limit))}`,
    {},
    true,
  );
}

export function fetchScenarioReport(reportId: string): Promise<ScenarioReport> {
  return request<ScenarioReport>(
    `/api/v1/intelligence/scenario-reports/${encodeURIComponent(reportId)}`,
    {},
    true,
  );
}

export function fetchPortfolioRiskReports(limit = 50): Promise<PortfolioRiskReport[]> {
  return request<PortfolioRiskReport[]>(
    `/api/v1/intelligence/portfolio-risk-reports?limit=${encodeURIComponent(String(limit))}`,
    {},
    true,
  );
}

export function fetchPortfolioRiskReport(reportId: string): Promise<PortfolioRiskReport> {
  return request<PortfolioRiskReport>(
    `/api/v1/intelligence/portfolio-risk-reports/${encodeURIComponent(reportId)}`,
    {},
    true,
  );
}

export type CorrelationReport = {
  id: string;
  created_at: string;
  artifact_type: string;
  method_version: string;
  left_market_class: string;
  left_symbol: string;
  right_market_class: string;
  right_symbol: string;
  timeframe: string;
  sample_count: number;
  correlation_value: number;
  uncertainty: {
    method?: string;
    lower?: number;
    upper?: number;
    confidence_level?: number;
    [key: string]: unknown;
  };

  significance: {
    p_value?: number;
    [key: string]: unknown;
  };
  report_hash: string;
  research_status: string;

  /** BO-F-03: B-04 read surface fields — the generation endpoints append the
      honest data-class label to `notes`; rendered verbatim, never computed. */
  notes?: string;
  limitations?: string[];

  /** BO-F-05: persisted lineage fields (backend read model — B-04
      generation appends them; rendered verbatim, never computed). */
  source_artifact_ids?: string[];
  audit_correlation_id?: string;
  created_by?: string;
};



export type RegimeReport = {
  id: string;
  created_at: string;
  artifact_type: string;
  method_version: string;
  market_class: string;
  symbol: string;
  timeframe: string;
  sample_count: number;
  regime_label: string;
  confidence: number;
  uncertainty: {
    method?: string;
    lower?: number;
    upper?: number;
    [key: string]: unknown;
  };

  evidence: Record<string, unknown>;
  report_hash: string;
  research_status: string;

  /** BO-F-03: B-04 read surface fields — the generation endpoints append the
      honest data-class label to `notes`; rendered verbatim, never computed. */
  notes?: string;
  limitations?: string[];

  /** BO-F-05: persisted lineage fields (backend read model — B-04
      generation appends them; rendered verbatim, never computed). */
  source_artifact_ids?: string[];
  audit_correlation_id?: string;
  created_by?: string;
};



export type SignalValidationReport = {
  id: string;
  created_at: string;
  artifact_type: string;
  method_version: string;
  sample_count: number;
  metrics: {
    brier_score?: number;
    expected_calibration_error?: number;
    ece?: number;
    max_calibration_error?: number;
    [key: string]: unknown;
  };

  uncertainty: {
    method?: string;
    lower?: number;
    upper?: number;
    confidence_level?: number;
    [key: string]: unknown;
  };
  limitations: unknown[];
  report_hash: string;
  research_status: string;

  /** BO-F-03: B-04 read surface fields — the generation endpoints append the
      honest data-class label to `notes`; rendered verbatim, never computed. */
  notes?: string;

  /** BO-F-05: persisted lineage fields (backend read model). */
  source_signal_ids?: string[];
  audit_correlation_id?: string;
  created_by?: string;
};



export function fetchCorrelationReports(limit = 50): Promise<CorrelationReport[]> {
  return request<CorrelationReport[]>(
    `/api/v1/intelligence/correlation-reports?limit=${encodeURIComponent(String(limit))}`,
    {},
    true,
  );
}

export function fetchRegimeReports(limit = 50): Promise<RegimeReport[]> {
  return request<RegimeReport[]>(
    `/api/v1/intelligence/regime-reports?limit=${encodeURIComponent(String(limit))}`,
    {},
    true,
  );
}

export function fetchSignalValidationReports(limit = 50): Promise<SignalValidationReport[]> {
  return request<SignalValidationReport[]>(
    `/api/v1/intelligence/signal-validation-reports?limit=${encodeURIComponent(String(limit))}`,
    {},
    true,
  );
}

export function fetchMonitoringAlerts(limit = 200): Promise<MonitoringAlert[]> {
  // SURF-P02 S6: the previous default of 5 was a silent truncation of an
  // endpoint that accepts up to 200 (OBS-CONV2-1 family). The default now
  // equals the API maximum, and the alerts surface discloses the list cap
  // whenever the response reaches it.
  return request<MonitoringAlert[]>(
    `/api/v1/alerts?limit=${encodeURIComponent(String(limit))}`,
    {},
    true,
  );
}

/** SURF-P02 S3: acknowledge an alert's read-state (operator-authenticated).
 * The backend mutates read-state fields only and writes one audit entry. */
export function acknowledgeMonitoringAlert(alertId: string): Promise<MonitoringAlert> {
  return request<MonitoringAlert>(
    `/api/v1/alerts/${encodeURIComponent(alertId)}/ack`,
    { method: "POST" },
    true,
  );
}

/** SURF-P02 S5: retrieve one alert record (previously unreachable). */
export function fetchMonitoringAlertDetail(alertId: string): Promise<MonitoringAlert> {
  return request<MonitoringAlert>(
    `/api/v1/alerts/${encodeURIComponent(alertId)}`,
    {},
    true,
  );
}

export async function fetchInstitutionalIntelligenceBundle(
  limit = 10,
): Promise<InstitutionalIntelligenceBundle> {
  const q = `limit=${encodeURIComponent(String(limit))}`;
  const [relation, context, hypothetical, risk, validation] = await Promise.all([
    request<InstitutionalReport[]>(`/api/v1/intelligence/correlation-reports?${q}`, {}, true),
    request<InstitutionalReport[]>(`/api/v1/intelligence/regime-reports?${q}`, {}, true),
    request<InstitutionalReport[]>(`/api/v1/intelligence/scenario-reports?${q}`, {}, true),
    request<InstitutionalReport[]>(`/api/v1/intelligence/portfolio-risk-reports?${q}`, {}, true),
    request<InstitutionalReport[]>(`/api/v1/intelligence/signal-validation-reports?${q}`, {}, true),
  ]);
  return { relation, context, hypothetical, risk, validation };
}

export async function fetchExecutionResearchBundle(limit = 25): Promise<ExecutionResearchBundle> {
  const q = `limit=${encodeURIComponent(String(limit))}`;
  const runs = await request<SimulatedExecutionRun[]>(
    `/api/v1/execution-research/simulated-runs?${q}`,
    {},
    true,
  );
  // SURF-P01 S3: fills are fetched for EVERY returned run. The previous
  // first-5 truncation was a quiet inaccuracy (OBS-CONV2-1 family) — an
  // operator could not see that fills beyond five runs were missing.
  const fillGroups = await Promise.all(
    runs.map((run) =>
      request<SimulatedFillEvent[]>(
        `/api/v1/execution-research/simulated-runs/${encodeURIComponent(run.run_id)}/fills?limit=50`,
        {},
        true,
      ),
    ),
  );
  const [ledger, riskReports, experiments, analyticsReports] = await Promise.all([
    request<SimulatedPaperLedgerEntry[]>(
      `/api/v1/execution-research/simulated-ledger-entries?${q}`,
      {},
      true,
    ),
    request<ExecutionRiskResearchReport[]>(
      `/api/v1/execution-research/execution-risk-reports?${q}`,
      {},
      true,
    ),
    request<ExecutionResearchExperiment[]>(
      `/api/v1/execution-research/execution-experiments?${q}`,
      {},
      true,
    ),
    request<SimulatedExecutionAnalyticsReport[]>(
      `/api/v1/execution-research/simulated-analytics-reports?${q}`,
      {},
      true,
    ),
  ]);
  return {
    runs,
    fills: fillGroups.flat(),
    ledger,
    riskReports,
    experiments,
    analyticsReports,
  };
}

/* =========================================================================
   SURF-P01 — execution-research read seams (12 read-only functions).
   The backend has 17 execution-research endpoints (12 GET + 5 POST). The
   five POSTs are EXPLICITLY OUT OF SCOPE for SURF-P01 (Build Order §4) — no
   client function exists for them and none is added here. The six detail
   GETs were previously unreachable from the UI; these functions surface
   them. All functions are read-only and carry no actuation of any kind.
   ========================================================================= */

export function fetchSimulatedRunsList(limit = 25): Promise<SimulatedExecutionRun[]> {
  return request<SimulatedExecutionRun[]>(
    `/api/v1/execution-research/simulated-runs?limit=${encodeURIComponent(String(limit))}`,
    {},
    true,
  );
}

export function fetchSimulatedRunFills(runId: string, limit = 50): Promise<SimulatedFillEvent[]> {
  return request<SimulatedFillEvent[]>(
    `/api/v1/execution-research/simulated-runs/${encodeURIComponent(runId)}/fills?limit=${encodeURIComponent(String(limit))}`,
    {},
    true,
  );
}

export function fetchSimulatedLedgerEntriesList(limit = 25): Promise<SimulatedPaperLedgerEntry[]> {
  return request<SimulatedPaperLedgerEntry[]>(
    `/api/v1/execution-research/simulated-ledger-entries?limit=${encodeURIComponent(String(limit))}`,
    {},
    true,
  );
}

export function fetchExecutionRiskReportsList(limit = 25): Promise<ExecutionRiskResearchReport[]> {
  return request<ExecutionRiskResearchReport[]>(
    `/api/v1/execution-research/execution-risk-reports?limit=${encodeURIComponent(String(limit))}`,
    {},
    true,
  );
}

export function fetchExecutionExperimentsList(limit = 25): Promise<ExecutionResearchExperiment[]> {
  return request<ExecutionResearchExperiment[]>(
    `/api/v1/execution-research/execution-experiments?limit=${encodeURIComponent(String(limit))}`,
    {},
    true,
  );
}

export function fetchSimulatedAnalyticsReportsList(
  limit = 25,
): Promise<SimulatedExecutionAnalyticsReport[]> {
  return request<SimulatedExecutionAnalyticsReport[]>(
    `/api/v1/execution-research/simulated-analytics-reports?limit=${encodeURIComponent(String(limit))}`,
    {},
    true,
  );
}

export function fetchSimulatedExecutionRunDetail(runId: string): Promise<SimulatedExecutionRunDetail> {
  return request<SimulatedExecutionRunDetail>(
    `/api/v1/execution-research/simulated-runs/${encodeURIComponent(runId)}`,
    {},
    true,
  );
}

export function fetchSimulatedFillDetail(fillId: string): Promise<SimulatedFillEvent> {
  return request<SimulatedFillEvent>(
    `/api/v1/execution-research/simulated-fills/${encodeURIComponent(fillId)}`,
    {},
    true,
  );
}

export function fetchSimulatedLedgerEntryDetail(
  ledgerEntryId: string,
): Promise<SimulatedPaperLedgerEntry> {
  return request<SimulatedPaperLedgerEntry>(
    `/api/v1/execution-research/simulated-ledger-entries/${encodeURIComponent(ledgerEntryId)}`,
    {},
    true,
  );
}

export function fetchExecutionRiskReportDetail(
  reportId: string,
): Promise<ExecutionRiskResearchReport> {
  return request<ExecutionRiskResearchReport>(
    `/api/v1/execution-research/execution-risk-reports/${encodeURIComponent(reportId)}`,
    {},
    true,
  );
}

export function fetchExecutionExperimentDetail(
  experimentId: string,
): Promise<ExecutionResearchExperiment> {
  return request<ExecutionResearchExperiment>(
    `/api/v1/execution-research/execution-experiments/${encodeURIComponent(experimentId)}`,
    {},
    true,
  );
}

export function fetchSimulatedAnalyticsReportDetail(
  reportId: string,
): Promise<SimulatedExecutionAnalyticsReport> {
  return request<SimulatedExecutionAnalyticsReport>(
    `/api/v1/execution-research/simulated-analytics-reports/${encodeURIComponent(reportId)}`,
    {},
    true,
  );
}

export function fetchWorkspacePreferences(limit = 50): Promise<OperatorWorkspacePreference[]> {
  return request<OperatorWorkspacePreference[]>(
    `/api/v1/institutional-platform/workspace-preferences?limit=${encodeURIComponent(String(limit))}`,
    {},
    true,
  );
}

export function createWorkspacePreference(
  payload: OperatorWorkspacePreferenceWrite,
): Promise<OperatorWorkspacePreference> {
  return request<OperatorWorkspacePreference>(
    "/api/v1/institutional-platform/workspace-preferences",
    { method: "POST", body: JSON.stringify(payload) },
    true,
  );
}

export function updateWorkspacePreference(
  preferenceId: string,
  payload: OperatorWorkspacePreferenceWrite,
): Promise<OperatorWorkspacePreference> {
  return request<OperatorWorkspacePreference>(
    `/api/v1/institutional-platform/workspace-preferences/${encodeURIComponent(preferenceId)}`,
    { method: "PUT", body: JSON.stringify(payload) },
    true,
  );
}

export function fetchResearchManagementBundle(limit = 50): Promise<ResearchManagementBundle> {
  return request<ResearchManagementBundle>(
    `/api/v1/institutional-platform/research-management?limit=${encodeURIComponent(String(limit))}`,
    {},
    true,
  );
}

export function fetchResearchCollections(limit = 50): Promise<ResearchCollection[]> {
  return request<ResearchCollection[]>(
    `/api/v1/institutional-platform/research-collections?limit=${encodeURIComponent(String(limit))}`,
    {},
    true,
  );
}

export function createResearchCollection(
  payload: ResearchCollectionWrite,
): Promise<ResearchCollection> {
  return request<ResearchCollection>(
    "/api/v1/institutional-platform/research-collections",
    { method: "POST", body: JSON.stringify(payload) },
    true,
  );
}

export function addResearchCollectionMember(
  collectionId: string,
  payload: ResearchArtifactReferenceWrite,
): Promise<ResearchCollectionMember> {
  return request<ResearchCollectionMember>(
    `/api/v1/institutional-platform/research-collections/${encodeURIComponent(collectionId)}/members`,
    { method: "POST", body: JSON.stringify(payload) },
    true,
  );
}

export function removeResearchCollectionMember(
  collectionId: string,
  memberId: string,
): Promise<{ status: string; member_id: string }> {
  return request<{ status: string; member_id: string }>(
    `/api/v1/institutional-platform/research-collections/${encodeURIComponent(collectionId)}/members/${encodeURIComponent(memberId)}`,
    { method: "DELETE" },
    true,
  );
}

export function fetchResearchTags(limit = 100): Promise<ResearchTag[]> {
  return request<ResearchTag[]>(
    `/api/v1/institutional-platform/research-tags?limit=${encodeURIComponent(String(limit))}`,
    {},
    true,
  );
}

export function createResearchTag(payload: ResearchTagWrite): Promise<ResearchTag> {
  return request<ResearchTag>(
    "/api/v1/institutional-platform/research-tags",
    { method: "POST", body: JSON.stringify(payload) },
    true,
  );
}

export function fetchPortfolioResearchDashboard(): Promise<PortfolioResearchDashboard> {
  return request<PortfolioResearchDashboard>(
    "/api/v1/institutional-platform/portfolio-research/dashboard",
    {},
    true,
  );
}

export function fetchAdvancedResearchReport(): Promise<AdvancedResearchReport> {
  return request<AdvancedResearchReport>(
    "/api/v1/institutional-platform/portfolio-research/report",
    {},
    true,
  );
}

export function fetchJournalEntries(limit = 50): Promise<ManualJournalEntry[]> {
  return request<ManualJournalEntry[]>(
    `/api/v1/collaboration/journal-entries?limit=${encodeURIComponent(String(limit))}`,
    {},
    true,
  );
}

export function createJournalEntry(payload: ManualJournalEntryWrite): Promise<ManualJournalEntry> {
  return request<ManualJournalEntry>(
    "/api/v1/collaboration/journal-entries",
    { method: "POST", body: JSON.stringify(payload) },
    true,
  );
}

export function updateJournalEntry(
  journalId: string,
  payload: ManualJournalEntryWrite,
): Promise<ManualJournalEntry> {
  return request<ManualJournalEntry>(
    `/api/v1/collaboration/journal-entries/${encodeURIComponent(journalId)}`,
    { method: "PUT", body: JSON.stringify(payload) },
    true,
  );
}

export function fetchTradePlans(limit = 50): Promise<TradePlanNote[]> {
  return request<TradePlanNote[]>(
    `/api/v1/collaboration/trade-plans?limit=${encodeURIComponent(String(limit))}`,
    {},
    true,
  );
}

export function createTradePlan(payload: TradePlanNoteWrite): Promise<TradePlanNote> {
  return request<TradePlanNote>(
    "/api/v1/collaboration/trade-plans",
    { method: "POST", body: JSON.stringify(payload) },
    true,
  );
}

export function updateTradePlan(planId: string, payload: TradePlanNoteWrite): Promise<TradePlanNote> {
  return request<TradePlanNote>(
    `/api/v1/collaboration/trade-plans/${encodeURIComponent(planId)}`,
    { method: "PUT", body: JSON.stringify(payload) },
    true,
  );
}

export function fetchChartResearchAnnotations(params: {
  symbol?: string;
  timeframe?: string;
  limit?: number;
} = {}): Promise<ChartResearchAnnotation[]> {
  const q = new URLSearchParams();
  if (params.symbol) q.set("symbol", params.symbol);
  if (params.timeframe) q.set("timeframe", params.timeframe);
  q.set("limit", String(params.limit ?? 50));
  return request<ChartResearchAnnotation[]>(
    `/api/v1/collaboration/chart-annotations?${q.toString()}`,
    {},
    true,
  );
}

export function createChartResearchAnnotation(
  payload: ChartResearchAnnotationCreate,
): Promise<ChartResearchAnnotation> {
  return request<ChartResearchAnnotation>(
    "/api/v1/collaboration/chart-annotations",
    { method: "POST", body: JSON.stringify(payload) },
    true,
  );
}

/** CHART-P03 (S1): update a drawing's anchors — content-only change on the
 * same audited artifact; never a parallel persistence path. */
export function updateChartResearchAnnotation(params: {
  annotationId: string;
  content: Record<string, unknown>;
}): Promise<ChartResearchAnnotation> {
  return request<ChartResearchAnnotation>(
    `/api/v1/collaboration/chart-annotations/${params.annotationId}`,
    { method: "PATCH", body: JSON.stringify({ content: params.content }) },
    true,
  );
}

/** CHART-P03 (S1): remove a drawing — audited deletion of the same artifact. */
export function deleteChartResearchAnnotation(
  annotationId: string,
): Promise<ChartResearchAnnotation> {
  return request<ChartResearchAnnotation>(
    `/api/v1/collaboration/chart-annotations/${annotationId}`,
    { method: "DELETE" },
    true,
  );
}

export function startLiveMarket(): Promise<{ status: string; stats: LiveMarketStats }> {
  return request<{ status: string; stats: LiveMarketStats }>(
    "/api/v1/market/live/start",
    { method: "POST" },
    true,
  );
}

export function stopLiveMarket(): Promise<{ status: string; stats: LiveMarketStats }> {
  return request<{ status: string; stats: LiveMarketStats }>(
    "/api/v1/market/live/stop",
    { method: "POST" },
    true,
  );
}

export function seedChartHistory(): Promise<{
  status: string;
  seeded: Record<string, number>;
  timeframe: string;
}> {
  return request(
    "/api/v1/market/live/seed-history",
    { method: "POST" },
    true,
  );
}

export function getWebSocketUrl(path = "/ws/status"): string {
  const configured = import.meta.env.VITE_WS_BASE_URL;
  if (configured) {
    return `${configured}${path}`;
  }
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  return `${protocol}//${window.location.host}${path}`;
}

/** Short-lived one-time WS ticket (preferred — no access JWT in URL). */
export async function fetchWsTicket(): Promise<{ ticket: string; expires_in: number }> {
  return request<{ ticket: string; expires_in: number }>(
    "/api/v1/auth/ws-ticket",
    { method: "POST" },
    true,
  );
}

/** Live market WebSocket URL using short-lived ticket (W0-U08). */
export function getLiveMarketWebSocketUrlWithTicket(ticket: string): string {
  const base = getWebSocketUrl("/ws/market");
  const sep = base.includes("?") ? "&" : "?";
  return `${base}${sep}ticket=${encodeURIComponent(ticket)}`;
}

/** @deprecated Prefer ticket-based URL — access JWT in query is disabled by default. */
export function getLiveMarketWebSocketUrl(accessToken: string): string {
  const base = getWebSocketUrl("/ws/market");
  const sep = base.includes("?") ? "&" : "?";
  return `${base}${sep}token=${encodeURIComponent(accessToken)}`;
}

export type ApiCandle = {
  id: string;
  market_class: string;
  symbol: string;
  timeframe: string;
  open_time: string;
  open: string;
  high: string;
  low: string;
  close: string;
  volume: string | null;
  source: string | null;
  created_at: string;
  /** DATA-P02: populated only on aggregated bars (complete bucket accounting). */
  complete?: boolean | null;
  constituents?: number | null;
};

/**
 * DATA-P02 M4 — typed series result. The state is a discriminant carried on
 * the response; consumers must NEVER infer it from bar counts or message
 * strings.
 */
export type CandleSeriesResult =
  | { kind: "native"; timeframe: string; bars: ApiCandle[] }
  | {
      kind: "aggregated";
      timeframe: string;
      sourceTimeframe: string;
      excludedPartialBuckets: number;
      bars: ApiCandle[];
    }
  | { kind: "unavailable"; timeframe: string; detail: string; bars: ApiCandle[] };

/**
 * CHART-P01 M4 — per-indicator results, mirroring the backend's discriminated
 * union on `shape`. A typed discriminant, never inferred from values.
 */
export type LineIndicatorResult = {
  shape: "line";
  kind: "computed";
  points: Array<{ time: string; value: string | null }>;
};
/** CHART-P02: multi-line indicators (Ichimoku, ADX/DMI, levels, …) —
 * `lines` maps a line name to its point list (matches the backend's
 * MultiIndicatorRead). */
export type MultiIndicatorResult = {
  shape: "multi";
  kind: "computed";
  lines: Record<string, Array<{ time: string; value: string | null }>>;
};
export type BandIndicatorResult = {
  shape: "band";
  kind: "computed";
  points: Array<{ time: string; upper: string | null; middle: string | null; lower: string | null }>;
};
export type MacdIndicatorResult = {
  shape: "macd";
  kind: "computed";
  points: Array<{
    time: string;
    macd: string | null;
    signal: string | null;
    histogram: string | null;
  }>;
};
export type InsufficientIndicatorResult = {
  shape: "insufficient";
  required: number;
  available: number;
  detail?: string | null;
};
export type IndicatorResult =
  | LineIndicatorResult
  | MultiIndicatorResult
  | BandIndicatorResult
  | MacdIndicatorResult
  | InsufficientIndicatorResult;

/**
 * CHART-P01 M6 — the envelope carries the DATA-P02 series kind the
 * computation ran over. seriesKind "unavailable" means no computation
 * occurred; `detail` states why.
 */
export type IndicatorSeriesEnvelope = {
  symbol: string;
  timeframe: string;
  seriesKind: "native" | "aggregated" | "unavailable";
  sourceTimeframe: string | null;
  excludedPartialBuckets: number | null;
  detail: string | null;
  indicators: Record<string, IndicatorResult>;
};

/**
 * CHART-P01 M1/M3 — indicator series computed SERVER-side over the same
 * window the series endpoint serves. The client only consumes.
 */
export function fetchIndicatorSeries(params: {
  symbol: string;
  timeframe: string;
  indicators: string[];
}): Promise<IndicatorSeriesEnvelope> {
  const q = new URLSearchParams();
  q.set("symbol", params.symbol);
  q.set("timeframe", params.timeframe);
  q.set("indicators", params.indicators.join(","));
  return request<IndicatorSeriesEnvelope>(
    `/api/v1/persistence/indicator-series?${q.toString()}`,
    {},
    true,
  );
}

/**
 * Candle series for charts (ascending chronological, last N bars).
 * DATA-P02 M2: served by the dedicated typed endpoint — aggregation happens
 * on the server (wall-clock-aligned OHLC buckets), never on the client.
 */
export function fetchCandles(params: {
  symbol: string;
  timeframe?: string;
  market_class?: string;
  limit?: number;
  order?: "asc" | "desc";
}): Promise<CandleSeriesResult> {
  const q = new URLSearchParams();
  q.set("symbol", params.symbol);
  if (params.timeframe) q.set("timeframe", params.timeframe);
  if (params.market_class) q.set("market_class", params.market_class);
  q.set("limit", String(params.limit ?? 500));
  q.set("order", params.order ?? "asc");
  return request<CandleSeriesResult>(
    `/api/v1/persistence/candle-series?${q.toString()}`,
    {},
    true,
  );
}

/* =========================================================================
   BO-F-03 — intelligence generation client (2026-08-21)
   -------------------------------------------------------------------------
   The B-04 generation seam: five governed POST endpoints that create
   RESEARCH ARTIFACTS ONLY (no actuation, no signal emission, no state
   mutation beyond the persisted report). These functions are the first
   frontend callers of that seam.

   Boundary invariants (BO-F-03 §7):
   - Bearer JWT on every generation call; 401 surfaces as a typed error.
   - The structured B-04 422 ({error_code, detail, insufficient_data}) is
     mapped to `IntelligenceGenerationError` — an honest insufficient-data signal,
     never a fabricated report.
   - Server-values-only: the caller renders the persisted report verbatim.
   ========================================================================= */

export interface IntelligenceSeriesRef {
  market_class: string;
  symbol: string;
  timeframe: string;
}

export interface CorrelationGenerationInput {
  left: IntelligenceSeriesRef;
  right: IntelligenceSeriesRef;
  as_of_start: string;
  as_of_end: string;
}

export interface RegimeGenerationInput {
  series: IntelligenceSeriesRef;
  as_of_start: string;
  as_of_end: string;
}

export interface ScenarioGenerationInput {
  series: IntelligenceSeriesRef;
  assumptions: {
    scenario_name: string;
    shock_return: number;
    horizon_bars: number;
    volatility_multiplier: number;
  };
  as_of_start: string;
  as_of_end: string;
}

export interface PortfolioRiskGenerationInput {
  series: IntelligenceSeriesRef;
  assumptions: {
    report_name: string;
    stress_multiplier: number;
    tail_quantile: number;
  };
  as_of_start: string;
  as_of_end: string;
}

export interface SignalValidationGenerationInput {
  scope_start: string;
  scope_end: string;
  market_class: string;
  symbol: string;
  timeframe: string;
  include_states: string[];
}

export class IntelligenceGenerationError extends Error {
  status: number;
  errorCode: string | null;
  insufficientData: boolean;

  constructor(message: string, status: number, errorCode: string | null, insufficientData: boolean) {
    super(message);
    this.name = "IntelligenceGenerationError";
    this.status = status;
    this.errorCode = errorCode;
    this.insufficientData = insufficientData;
  }
}

async function createIntelligenceReport<T>(
  path: string,
  body: unknown,
): Promise<T> {
  const headers = new Headers();
  headers.set("Accept", "application/json");
  headers.set("Content-Type", "application/json");
  const token = getAccessToken();
  if (token) headers.set("Authorization", `Bearer ${token}`);

  const response = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers,
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    let message = `Generation failed (${response.status}) for ${path}`;
    let errorCode: string | null = null;
    let insufficientData = false;
    try {
      const payload = (await response.json()) as {
        detail?: string | { error_code?: string; detail?: string; insufficient_data?: boolean };
      };
      if (payload.detail && typeof payload.detail === "object") {
        errorCode = payload.detail.error_code ?? null;
        insufficientData = payload.detail.insufficient_data === true;
        message = payload.detail.detail ?? message;
      } else if (typeof payload.detail === "string" && payload.detail) {
        message = payload.detail;
      }
    } catch {
      /* non-JSON error body: keep the status-based message */
    }
    throw new IntelligenceGenerationError(message, response.status, errorCode, insufficientData);
  }

  return (await response.json()) as T;
}

/** BO-F-03.1: generate a governed correlation intelligence report. */
export function createCorrelationReport(
  input: CorrelationGenerationInput,
): Promise<CorrelationReport> {
  return createIntelligenceReport<CorrelationReport>(
    "/api/v1/intelligence/correlation-reports",
    input,
  );
}

/** BO-F-03.1: generate a governed regime detection report. */
export function createRegimeReport(input: RegimeGenerationInput): Promise<RegimeReport> {
  return createIntelligenceReport<RegimeReport>(
    "/api/v1/intelligence/regime-reports",
    input,
  );
}

/** BO-F-03.1: generate a governed hypothetical scenario report. */
export function createScenarioReport(
  input: ScenarioGenerationInput,
): Promise<ScenarioReport> {
  return createIntelligenceReport<ScenarioReport>(
    "/api/v1/intelligence/scenario-reports",
    input,
  );
}

/** BO-F-03.1: generate a governed hypothetical portfolio-risk report. */
export function createPortfolioRiskReport(
  input: PortfolioRiskGenerationInput,
): Promise<PortfolioRiskReport> {
  return createIntelligenceReport<PortfolioRiskReport>(
    "/api/v1/intelligence/portfolio-risk-reports",
    input,
  );
}

/** BO-F-03.1: generate a governed signal-validation report. */
export function createSignalValidationReport(
  input: SignalValidationGenerationInput,
): Promise<SignalValidationReport> {
  return createIntelligenceReport<SignalValidationReport>(
    "/api/v1/intelligence/signal-validation-reports",
    input,
  );
}
