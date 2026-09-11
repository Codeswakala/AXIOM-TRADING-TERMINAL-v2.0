/**
 * PlatformRecordsSection — SURF-P03 (Build Order SURF-P03, authorized
 * 2026-08-17).
 *
 * Renders the RECORD payloads of the institutional platform governance
 * endpoints — the content the overlay's posture summary never showed:
 * route-inventory routes, RBAC per-role permission lists, the API catalogue
 * routes + abuse guard + persistence, plugin contracts + capability
 * allowlist — plus the operator scope records (list and detail), which had
 * no client function at all.
 *
 * Discipline:
 * - M2: pure inspection. No control here can modify roles, register routes,
 *   alter scope, or enable plugins.
 * - M3: a 403 on the scope endpoints renders an explicit access notice that
 *   is visually distinct from an empty result and from a transport error.
 * - R2: five independent fetches with per-source state and genuine counts —
 *   one failing source never blanks the others.
 * - M4: values that also appear in the overlay's posture summary come from
 *   the same institutional endpoints (immutable configuration); this section
 *   renders records "as returned by" its own fetch and never silently
 *   reconciles with the summary.
 */
import type {
  ApiCatalogueResponse,
  OperatorScopeListResult,
  OperatorScopeRecordResult,
  PluginContractsResponse,
  RbacPermissionsResponse,
  RouteInventoryResponse,
} from "../../../api/client";

export type PlatformSourceStatusRow = {
  family: string;
  state: "loading" | "error" | "ready" | "denied";
  detail: string | null;
  rowCount: number;
};

type Props = {
  routeInventory: RouteInventoryResponse | null;
  routeInventoryLoading: boolean;
  routeInventoryError: string | null;
  rbac: RbacPermissionsResponse | null;
  rbacLoading: boolean;
  rbacError: string | null;
  apiCatalogue: ApiCatalogueResponse | null;
  apiCatalogueLoading: boolean;
  apiCatalogueError: string | null;
  pluginContracts: PluginContractsResponse | null;
  pluginContractsLoading: boolean;
  pluginContractsError: string | null;
  scopeResult: OperatorScopeListResult | null;
  scopeLoading: boolean;
  scopeRecordResult: OperatorScopeRecordResult | null;
  scopeDetailLoading: boolean;
  onRefreshScope?: () => void;
  onSelectScopeDetail?: (operatorId: string) => void;
};

const SCOPE_ACCESS_DENIED_TEXT =
  "Access to institutional scope records is denied for your role. This is an access restriction, not an empty result.";

function directValue(value: unknown): string {
  if (typeof value === "string" && value.trim()) return value;
  if (typeof value === "number" || typeof value === "boolean") return String(value);
  if (value === null || value === undefined) return "—";
  return JSON.stringify(value);
}

function routeLabel(route: Record<string, unknown>): string {
  const path = directValue(route.path);
  const methods = Array.isArray(route.methods) ? route.methods.join(", ") : directValue(route.methods);
  return `${methods} ${path}`;
}

export function PlatformRecordsSection({
  routeInventory,
  routeInventoryLoading,
  routeInventoryError,
  rbac,
  rbacLoading,
  rbacError,
  apiCatalogue,
  apiCatalogueLoading,
  apiCatalogueError,
  pluginContracts,
  pluginContractsLoading,
  pluginContractsError,
  scopeResult,
  scopeLoading,
  scopeRecordResult,
  scopeDetailLoading,
  onRefreshScope,
  onSelectScopeDetail,
}: Props) {
  const sourceStatus: PlatformSourceStatusRow[] = [
    {
      family: "Route inventory",
      state: routeInventoryLoading
        ? "loading"
        : routeInventoryError
          ? "error"
          : routeInventory
            ? "ready"
            : "loading",
      detail: routeInventoryError,
      rowCount: routeInventory?.routes.length ?? 0,
    },
    {
      family: "RBAC permissions",
      state: rbacLoading ? "loading" : rbacError ? "error" : rbac ? "ready" : "loading",
      detail: rbacError,
      rowCount: rbac ? Object.keys(rbac.roles).length : 0,
    },
    {
      family: "API catalogue",
      state: apiCatalogueLoading
        ? "loading"
        : apiCatalogueError
          ? "error"
          : apiCatalogue
            ? "ready"
            : "loading",
      detail: apiCatalogueError,
      rowCount: apiCatalogue?.routes.length ?? 0,
    },
    {
      family: "Plugin contracts",
      state: pluginContractsLoading
        ? "loading"
        : pluginContractsError
          ? "error"
          : pluginContracts
            ? "ready"
            : "loading",
      detail: pluginContractsError,
      rowCount: pluginContracts?.contracts.length ?? 0,
    },
    {
      family: "Operator scope records",
      state: scopeLoading
        ? "loading"
        : scopeResult?.kind === "denied"
          ? "denied"
          : scopeResult?.kind === "error"
            ? "error"
            : scopeResult?.kind === "ok"
              ? "ready"
              : "loading",
      detail: scopeResult && scopeResult.kind !== "ok" ? scopeResult.detail : null,
      rowCount: scopeResult?.kind === "ok" ? scopeResult.records.length : 0,
    },
  ];

  return (
    <section
      className="panel span-12"
      aria-label="Institutional platform records"
      data-testid="platform-records-section"
    >
      <div className="artifact-explorer-frame-head">
        <div>
          <h2>Platform Records</h2>
          <p className="muted">
            Record payloads of the institutional platform endpoints, rendered as returned:
            route inventory entries, per-role RBAC permission lists, API catalogue routes with
            abuse guard and persistence posture, plugin contracts with the capability allowlist,
            and operator scope records.
          </p>
        </div>
        <div className="research-guardrail-card" role="note" aria-label="Platform records inspection posture">
          <strong>Inspection view</strong>
          <span>No control here can modify roles, register routes, alter scope, or enable plugins</span>
        </div>
      </div>

      <section
        className="advisory-disclaimer"
        aria-label="Platform records read-only notice"
      >
        <strong>Read-only governance inspection.</strong> Every value below is an existing record
        read from the institutional platform. Values that also appear in the posture summary above
        come from the same endpoints and must agree; nothing here is reconciled silently.
      </section>

      <section className="panel span-12" aria-label="Platform record source status" data-testid="platform-source-status">
        <h3>Source Status</h3>
        <div className="artifact-source-grid">
          {sourceStatus.map((row) => (
            <article
              className="artifact-source-card"
              key={row.family}
              data-testid={
                row.state === "denied"
                  ? "platform-source-status-denied"
                  : `platform-source-status-${row.state}`
              }
            >
              <span className="ix-metadata">{row.family}</span>
              {row.state === "loading" ? <p className="muted">Loading…</p> : null}
              {row.state === "error" ? <p className="error-text">{row.detail}</p> : null}
              {row.state === "denied" ? (
                <p className="error-text">{SCOPE_ACCESS_DENIED_TEXT}</p>
              ) : null}
              {row.state === "ready" ? <small>{row.rowCount} records loaded</small> : null}
            </article>
          ))}
        </div>
      </section>

      <div className="execution-research-grid">
        <section className="panel" aria-label="Route inventory records" data-testid="platform-route-inventory">
          <h3>Route Inventory Records</h3>
          {routeInventoryError ? (
            <p className="error-text" data-testid="platform-route-inventory-error">
              {routeInventoryError}
            </p>
          ) : null}
          {!routeInventoryLoading && !routeInventoryError && routeInventory ? (
            routeInventory.routes.length === 0 ? (
              <p className="muted" data-testid="platform-route-inventory-empty">
                No route inventory records returned.
              </p>
            ) : (
              <ul className="alert-list">
                {routeInventory.routes.map((route, index) => (
                  <li
                    key={`${routeLabel(route)}-${index}`}
                    className="alert-list-item"
                    data-testid={`platform-route-entry-${index}`}
                  >
                    <div>
                      <div className="check-name mono">{routeLabel(route)}</div>
                      <div className="check-meta left">{directValue(route.permission)}</div>
                      <div className="alert-evidence mono">{directValue(route.description)}</div>
                    </div>
                  </li>
                ))}
              </ul>
            )
          ) : null}
        </section>

        <section className="panel" aria-label="RBAC role permission records" data-testid="platform-rbac-records">
          <h3>RBAC Role Permission Records</h3>
          {rbacError ? (
            <p className="error-text" data-testid="platform-rbac-error">
              {rbacError}
            </p>
          ) : null}
          {!rbacLoading && !rbacError && rbac ? (
            <>
              <dl className="kv compact">
                <div className="kv-row">
                  <dt>Policy</dt>
                  <dd>{directValue(rbac.policy)}</dd>
                </div>
                <div className="kv-row">
                  <dt>Forbidden capabilities present</dt>
                  <dd>{directValue(rbac.forbidden_capabilities_present)}</dd>
                </div>
              </dl>
              {Object.keys(rbac.roles).length === 0 ? (
                <p className="muted" data-testid="platform-rbac-empty">
                  No role permission records returned.
                </p>
              ) : (
                <ul className="alert-list">
                  {Object.entries(rbac.roles).map(([role, permissions]) => (
                    <li key={role} className="alert-list-item" data-testid={`platform-role-${role}`}>
                      <div>
                        <div className="check-name">{role}</div>
                        <div className="check-meta left mono">
                          {permissions.length} permissions · {permissions.join(", ")}
                        </div>
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </>
          ) : null}
        </section>

        <section className="panel" aria-label="API catalogue records" data-testid="platform-api-catalogue">
          <h3>API Catalogue Records</h3>
          {apiCatalogueError ? (
            <p className="error-text" data-testid="platform-api-catalogue-error">
              {apiCatalogueError}
            </p>
          ) : null}
          {!apiCatalogueLoading && !apiCatalogueError && apiCatalogue ? (
            <>
              <dl className="kv compact">
                <div className="kv-row">
                  <dt>Catalogue version</dt>
                  <dd className="mono">{directValue(apiCatalogue.catalogue_version)}</dd>
                </div>
                <div className="kv-row">
                  <dt>Abuse guard</dt>
                  <dd>
                    {directValue(apiCatalogue.abuse_guard.status)} · {directValue(apiCatalogue.abuse_guard.reason)}
                  </dd>
                </div>
                <div className="kv-row">
                  <dt>Persistence</dt>
                  <dd>
                    table persisted: {directValue(apiCatalogue.persistence.catalogue_table_persisted)} · alembic head expected:{" "}
                    <span className="mono">{directValue(apiCatalogue.persistence.alembic_head_expected)}</span>
                  </dd>
                </div>
              </dl>
              {apiCatalogue.routes.length === 0 ? (
                <p className="muted" data-testid="platform-api-catalogue-empty">
                  No API catalogue records returned.
                </p>
              ) : (
                <ul className="alert-list">
                  {apiCatalogue.routes.map((route, index) => (
                    <li
                      key={`${routeLabel(route)}-${index}`}
                      className="alert-list-item"
                      data-testid={`platform-catalogue-entry-${index}`}
                    >
                      <div>
                        <div className="check-name mono">{routeLabel(route)}</div>
                        <div className="check-meta left">{directValue(route.description)}</div>
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </>
          ) : null}
        </section>

        <section className="panel" aria-label="Plugin contract records" data-testid="platform-plugin-contracts">
          <h3>Plugin Contract Records</h3>
          {pluginContractsError ? (
            <p className="error-text" data-testid="platform-plugin-contracts-error">
              {pluginContractsError}
            </p>
          ) : null}
          {!pluginContractsLoading && !pluginContractsError && pluginContracts ? (
            <>
              <dl className="kv compact">
                <div className="kv-row">
                  <dt>Contract version</dt>
                  <dd className="mono">{directValue(pluginContracts.contract_version)}</dd>
                </div>
                <div className="kv-row">
                  <dt>Capability allowlist</dt>
                  <dd className="mono">
                    {pluginContracts.capability_allowlist.length
                      ? pluginContracts.capability_allowlist.join(", ")
                      : "—"}
                  </dd>
                </div>
              </dl>
              {pluginContracts.contracts.length === 0 ? (
                <p className="muted" data-testid="platform-plugin-contracts-empty">
                  No plugin contract records returned.
                </p>
              ) : (
                <ul className="alert-list">
                  {pluginContracts.contracts.map((contract, index) => (
                    <li
                      key={`${directValue(contract.name)}-${index}`}
                      className="alert-list-item"
                      data-testid={`platform-contract-entry-${index}`}
                    >
                      <div>
                        <div className="check-name">{directValue(contract.name)}</div>
                        <div className="check-meta left mono">{directValue(contract.version)}</div>
                        <div className="alert-evidence mono">
                          capabilities: {directValue(contract.capabilities)}
                        </div>
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </>
          ) : null}
        </section>

        <section className="panel" aria-label="Operator scope records" data-testid="platform-scope-records">
          <div className="group-head">
            <h3>Operator Scope Records</h3>
            <button
              type="button"
              className="btn"
              onClick={onRefreshScope}
              data-testid="platform-scope-refresh"
            >
              Refresh scope
            </button>
          </div>
          {scopeLoading ? (
            <p className="muted" data-testid="platform-scope-loading">
              Loading scope records…
            </p>
          ) : null}
          {!scopeLoading && scopeResult?.kind === "denied" ? (
            <p className="error-text" data-testid="platform-scope-access-denied">
              <strong>Access denied.</strong> {SCOPE_ACCESS_DENIED_TEXT}{" "}
              <span className="mono">{scopeResult.detail}</span>
            </p>
          ) : null}
          {!scopeLoading && scopeResult?.kind === "error" ? (
            <p className="error-text" data-testid="platform-scope-error">
              {scopeResult.detail}
            </p>
          ) : null}
          {!scopeLoading && scopeResult?.kind === "ok" && scopeResult.records.length === 0 ? (
            <p className="muted" data-testid="platform-scope-empty">
              No scope records returned for this operator.
            </p>
          ) : null}
          {!scopeLoading && scopeResult?.kind === "ok" && scopeResult.records.length > 0 ? (
            <ul className="alert-list" data-testid="platform-scope-list">
              {scopeResult.records.map((record) => (
                <li key={record.operator_id} className="alert-list-item" data-testid={`platform-scope-record-${record.operator_id}`}>
                  <div>
                    <div className="check-name">
                      {record.username} · {record.role}
                    </div>
                    <div className="check-meta left mono">
                      {record.record_type} · {record.research_status}
                    </div>
                    <div className="alert-evidence mono">operator {record.operator_id}</div>
                    {onSelectScopeDetail ? (
                      <div className="alert-item-actions">
                        <button
                          type="button"
                          className="btn"
                          onClick={() => onSelectScopeDetail(record.operator_id)}
                          data-testid={`platform-scope-detail-open-${record.operator_id}`}
                        >
                          View detail
                        </button>
                      </div>
                    ) : null}
                  </div>
                </li>
              ))}
            </ul>
          ) : null}
          {scopeRecordResult ? (
            <div data-testid="platform-scope-detail">
              {scopeDetailLoading ? (
                <p className="muted" data-testid="platform-scope-detail-loading">
                  Loading scope record…
                </p>
              ) : null}
              {scopeRecordResult.kind === "denied" ? (
                <p className="error-text" data-testid="platform-scope-detail-denied">
                  <strong>Access denied.</strong> {SCOPE_ACCESS_DENIED_TEXT}{" "}
                  <span className="mono">{scopeRecordResult.detail}</span>
                </p>
              ) : null}
              {scopeRecordResult.kind === "error" ? (
                <p className="error-text" data-testid="platform-scope-detail-error">
                  {scopeRecordResult.detail}
                </p>
              ) : null}
              {scopeRecordResult.kind === "ok" ? (
                <dl className="kv compact" data-testid="platform-scope-detail-record">
                  <div className="kv-row">
                    <dt>Operator id</dt>
                    <dd className="mono">{scopeRecordResult.record.operator_id}</dd>
                  </div>
                  <div className="kv-row">
                    <dt>Username</dt>
                    <dd>{scopeRecordResult.record.username}</dd>
                  </div>
                  <div className="kv-row">
                    <dt>Role</dt>
                    <dd>{scopeRecordResult.record.role}</dd>
                  </div>
                  <div className="kv-row">
                    <dt>Record type</dt>
                    <dd>{scopeRecordResult.record.record_type}</dd>
                  </div>
                  <div className="kv-row">
                    <dt>Research status</dt>
                    <dd>{scopeRecordResult.record.research_status}</dd>
                  </div>
                </dl>
              ) : null}
            </div>
          ) : null}
        </section>
      </div>
    </section>
  );
}
