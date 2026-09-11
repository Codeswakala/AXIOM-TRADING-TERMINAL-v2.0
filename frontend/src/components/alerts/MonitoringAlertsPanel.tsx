/**
 * MonitoringAlertsPanel — extended in place for SURF-P02 (R8: extended, not
 * relocated). This component was the orphan UI-005/W3-U08 alerts panel; it
 * remains the single alerts surface and is now mounted in the terminal right
 * dock (ALERTS tab) via TerminalAlertsDock.
 *
 * SURF-P02 extensions: data-testid hooks (S7), the read-state-only
 * Acknowledge control (M1), the operator-selectable detail record (S5), the
 * list-cap disclosure (S6), and explicit ack-failure surfacing (M2).
 * Preserved verbatim: the severity mapping (S4) and the R1 disclaimer
 * sentence (exported as ALERTS_DISCLAIMER below), which remains the honesty
 * surface of this domain.
 *
 * BO-F-04 (2026-08-21): the alerts-center completion —
 *   F-04.1 a five-domain filter (market / signal / risk / research / system)
 *         with DATA-ORIGIN-DERIVED assignment (never a client-invented
 *         category; unknown/mixed subjects fall to the documented neutral
 *         "research" bucket);
 *   F-04.2 every alert card visibly surfaces its absolute-UTC `created_at`
 *         and its provenance (subject type/id + lineage source where
 *         present); the detail record keeps the full field set;
 *   F-04.3 the read-state-only acknowledge discipline is untouched
 *         (provider-owned M2: state renders only after the API confirms);
 *   F-04.4 honest empty/error states preserved.
 */
import { useMemo, useState } from "react";
import type { MonitoringAlert } from "../../api/client";
import "./MonitoringAlertsPanel.css";

export const ALERTS_DISCLAIMER =
  "Read-only alerts inform the operator; they do not retrain, remediate, or act.";

export const ALERTS_LIST_CAP = 200;

/** BO-F-04.1 — the five alert domains (data-origin-derived). */
export type AlertDomain = "market" | "signal" | "risk" | "research" | "system";

export const ALERT_DOMAIN_FILTERS = [
  "ALL",
  "MARKET",
  "SIGNAL",
  "RISK",
  "RESEARCH",
  "SYSTEM",
] as const;

export type AlertDomainFilter = (typeof ALERT_DOMAIN_FILTERS)[number];

export const ALERT_DOMAINS: readonly AlertDomain[] = [
  "market",
  "signal",
  "risk",
  "research",
  "system",
];

/**
 * BO-F-04.1 — the domain mapping (documented, data-origin-derived).
 *
 * Priority order over the alert's PERSISTED fields — never client-invented:
 *   1. signal  — `signal_id` set, or subject `advisory_signal`
 *                (SIGNAL_WITHHELD emission).
 *   2. risk    — `model_artifact_id` set, or subject `model_artifact`
 *                (DRIFT_DETECTED emission — model-risk conditions).
 *   3. market  — subject `market_series`, or any `market_class`
 *                (LIVE_DATA_STALE emission).
 *   4. system  — subject `system_component` (INFERENCE_HEALTH_DEGRADED).
 *   5. research — the documented NEUTRAL bucket: any alert whose persisted
 *                subject fields do not attribute it to the four concrete
 *                operational domains. Nothing is invented — a null-fielded
 *                or unknown alert lands here honestly.
 */
export function alertDomain(alert: MonitoringAlert): AlertDomain {
  if (alert.signal_id !== null || alert.subject_type === "advisory_signal") {
    return "signal";
  }
  if (alert.model_artifact_id !== null || alert.subject_type === "model_artifact") {
    return "risk";
  }
  if (alert.subject_type === "market_series" || alert.market_class !== null) {
    return "market";
  }
  if (alert.subject_type === "system_component") {
    return "system";
  }
  return "research";
}

/** BO-F-04.2 — absolute-UTC timestamp (never a relative age that hides it). */
export function formatAlertTimestamp(createdAt: string): string {
  const parsed = new Date(createdAt);
  if (Number.isNaN(parsed.getTime())) return createdAt; // honest raw fallback
  return `${parsed.toISOString().slice(0, 16).replace("T", " ")} UTC`;
}

export function severityClass(severity: string): string {
  if (severity === "critical") return "danger";
  if (severity === "warning") return "degraded";
  return "stub";
}

type Props = {
  alerts: MonitoringAlert[];
  loading?: boolean;
  error?: string | null;
  ackError?: string | null;
  acknowledgingId?: string | null;
  onRefresh?: () => void;
  onAcknowledge?: (alertId: string) => void;
  detailAlert?: MonitoringAlert | null;
  detailLoading?: boolean;
  detailError?: string | null;
  onSelectDetail?: (alertId: string) => void;
  onCloseDetail?: () => void;
};

export function MonitoringAlertsPanel({
  alerts,
  loading = false,
  error = null,
  ackError = null,
  acknowledgingId = null,
  onRefresh,
  onAcknowledge,
  detailAlert = null,
  detailLoading = false,
  detailError = null,
  onSelectDetail,
  onCloseDetail,
}: Props) {
  const capped = alerts.length >= ALERTS_LIST_CAP;
  const [domainFilter, setDomainFilter] = useState<AlertDomainFilter>("ALL");

  const filteredAlerts = useMemo(() => {
    if (domainFilter === "ALL") return alerts;
    const wanted = domainFilter.toLowerCase() as AlertDomain;
    return alerts.filter((alert) => alertDomain(alert) === wanted);
  }, [alerts, domainFilter]);

  const showDomainEmpty =
    !loading && !error && alerts.length > 0 && filteredAlerts.length === 0;

  return (
    <section className="panel span-12" aria-label="Operator monitoring alerts" data-testid="monitoring-alerts-panel">
      <h2>Monitoring Alerts</h2>
      <p className="muted">{ALERTS_DISCLAIMER}</p>

      {onRefresh ? (
        <button
          type="button"
          className="btn"
          onClick={onRefresh}
          data-testid="alerts-refresh-btn"
        >
          Refresh alerts
        </button>
      ) : null}

      {/* BO-F-04.1 — the five-domain filter (data-origin-derived) */}
      <div className="alerts-domain-filter" role="tablist" aria-label="Alert domain filter">
        {ALERT_DOMAIN_FILTERS.map((domain) => (
          <button
            key={domain}
            type="button"
            role="tab"
            aria-selected={domainFilter === domain}
            className={`alerts-domain-tab mono ${domainFilter === domain ? "active" : ""}`}
            onClick={() => setDomainFilter(domain)}
            data-testid={`alerts-domain-${domain.toLowerCase()}`}
          >
            {domain}
          </button>
        ))}
        <span className="alerts-domain-count mono" data-testid="alerts-domain-count">
          {filteredAlerts.length}/{alerts.length}
        </span>
      </div>

      {error ? (
        <p className="error-text" data-testid="alerts-load-error">
          {error}
        </p>
      ) : null}
      {loading ? (
        <p className="muted" data-testid="alerts-loading">
          Loading alerts…
        </p>
      ) : null}
      {ackError ? (
        <p className="error-text" data-testid="alerts-ack-error">
          {ackError}
        </p>
      ) : null}
      {!loading && !error && alerts.length === 0 ? (
        <p className="muted" data-testid="alerts-empty">
          No monitoring alerts returned.
        </p>
      ) : null}
      {showDomainEmpty ? (
        <p className="muted" data-testid="alerts-domain-empty">
          No alerts in the {domainFilter.toLowerCase()} domain.
        </p>
      ) : null}
      {!loading && !error && capped ? (
        <p className="muted" data-testid="alerts-list-cap-note">
          Showing the most recent {ALERTS_LIST_CAP} alerts (list cap).
        </p>
      ) : null}

      <ul className="alert-list" data-testid="alerts-list">
        {filteredAlerts.map((alert) => {
          const domain = alertDomain(alert);
          const lineageSource =
            alert.lineage && typeof alert.lineage.source === "string"
              ? alert.lineage.source
              : null;
          return (
            <li key={alert.alert_id} className="alert-list-item" data-testid={`alert-item-${alert.alert_id}`}>
              <div>
                <div className="check-name">{alert.alert_type}</div>
                <div className="check-meta left">{alert.summary}</div>
                <div className="alert-evidence mono">
                  Subject: {alert.subject_type}/{alert.subject_id} · Ack: {alert.acknowledged ? "yes" : "no"}
                </div>
                {/* BO-F-04.2 — absolute-UTC timestamp + lineage provenance */}
                <div className="alert-meta-line mono" data-testid={`alert-created-${alert.alert_id}`}>
                  Created: {formatAlertTimestamp(alert.created_at)}
                </div>
                <div className="alert-meta-line mono" data-testid={`alert-lineage-${alert.alert_id}`}>
                  Lineage: {lineageSource ?? "none"}
                </div>
                {/* BO-F-05.1 — the audit correlation completes the lineage pair */}
                <div className="alert-meta-line mono" data-testid={`alert-audit-${alert.alert_id}`}>
                  Audit: {alert.audit_correlation_id || "provenance not recorded"}
                </div>
                <div className="alert-item-actions">
                  {onSelectDetail ? (
                    <button
                      type="button"
                      className="btn"
                      onClick={() => onSelectDetail(alert.alert_id)}
                      data-testid={`alert-detail-open-${alert.alert_id}`}
                    >
                      View detail
                    </button>
                  ) : null}
                  {!alert.acknowledged && onAcknowledge ? (
                    <button
                      type="button"
                      className="btn primary"
                      disabled={acknowledgingId === alert.alert_id}
                      onClick={() => onAcknowledge(alert.alert_id)}
                      data-testid={`alert-ack-${alert.alert_id}`}
                    >
                      {acknowledgingId === alert.alert_id ? "Acknowledging…" : "Acknowledge"}
                    </button>
                  ) : null}
                </div>
              </div>
              <div className="alert-right-rail">
                <span
                  className={`alert-domain-chip mono ${domain}`}
                  data-testid={`alert-domain-${alert.alert_id}`}
                  data-domain={domain}
                >
                  {domain.toUpperCase()}
                </span>
                <span className={`badge ${severityClass(alert.severity)}`} data-testid={`alert-severity-${alert.alert_id}`}>
                  {alert.severity}
                </span>
              </div>
            </li>
          );
        })}
      </ul>

      {detailAlert || detailLoading || detailError ? (
        <section
          className="alert-detail"
          aria-label="Alert detail record"
          data-testid="alerts-detail-panel"
        >
          <div className="alert-detail-head">
            <h3>Alert detail</h3>
            {onCloseDetail ? (
              <button
                type="button"
                className="btn"
                onClick={onCloseDetail}
                data-testid="alert-detail-close"
              >
                Close detail
              </button>
            ) : null}
          </div>
          {detailLoading ? (
            <p className="muted" data-testid="alerts-detail-loading">
              Loading alert record…
            </p>
          ) : null}
          {detailError ? (
            <p className="error-text" data-testid="alerts-detail-error">
              {detailError}
            </p>
          ) : null}
          {detailAlert ? (
            <dl className="kv compact" data-testid="alerts-detail-record">
              <div className="kv-row">
                <dt>Alert id</dt>
                <dd className="mono">{detailAlert.alert_id}</dd>
              </div>
              <div className="kv-row">
                <dt>Type</dt>
                <dd>{detailAlert.alert_type}</dd>
              </div>
              <div className="kv-row">
                <dt>Severity</dt>
                <dd>{detailAlert.severity}</dd>
              </div>
              {/* BO-F-04.1 — the derived domain on the detail record too */}
              <div className="kv-row">
                <dt>Domain</dt>
                <dd className="mono" data-testid="alerts-detail-domain">
                  {alertDomain(detailAlert)}
                </dd>
              </div>
              <div className="kv-row">
                <dt>Created at</dt>
                <dd>{detailAlert.created_at}</dd>
              </div>
              <div className="kv-row">
                <dt>Summary</dt>
                <dd>{detailAlert.summary}</dd>
              </div>
              <div className="kv-row">
                <dt>Subject</dt>
                <dd className="mono">
                  {detailAlert.subject_type}/{detailAlert.subject_id}
                </dd>
              </div>
              <div className="kv-row">
                <dt>Acknowledged</dt>
                <dd>
                  {detailAlert.acknowledged ? "yes" : "no"}
                  {detailAlert.acknowledged_at ? ` at ${detailAlert.acknowledged_at}` : ""}
                  {detailAlert.acknowledged_by ? ` by ${detailAlert.acknowledged_by}` : ""}
                </dd>
              </div>
              <div className="kv-row">
                <dt>Evidence</dt>
                <dd className="mono">{JSON.stringify(detailAlert.evidence)}</dd>
              </div>
              <div className="kv-row">
                <dt>Lineage</dt>
                <dd className="mono">{JSON.stringify(detailAlert.lineage)}</dd>
              </div>
              {/* BO-F-05.1 — the audit correlation in the detail record */}
              <div className="kv-row">
                <dt>Audit correlation</dt>
                <dd className="mono" data-testid="alerts-detail-audit">
                  {detailAlert.audit_correlation_id || "provenance not recorded"}
                </dd>
              </div>
            </dl>
          ) : null}
        </section>
      ) : null}
    </section>
  );
}
