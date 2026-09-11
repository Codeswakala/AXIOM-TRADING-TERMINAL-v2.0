/**
 * BO-F-04 — Alerts Center Completion (domain filtering + timestamp/lineage)
 *
 * Pins:
 *  1. The five-domain mapping is data-origin-derived from PERSISTED fields
 *     (signal_id / model_artifact_id / subject_type / market_class) with the
 *     documented neutral "research" bucket — never invented.
 *  2. The domain filter controls the list client-side; ALL is the default;
 *     each domain shows only its alerts; a domain with no alerts renders an
 *     honest empty notice.
 *  3. Every alert card visibly renders the absolute-UTC timestamp and the
 *     lineage source (or an honest "none").
 *  4. The read-state-only ack discipline is preserved: Acknowledge only for
 *     unacknowledged alerts, disabled while acknowledging, no banned
 *     remediation vocabulary in any control.
 */

import { describe, expect, it } from "vitest";
import { fireEvent, render, screen } from "@testing-library/react";
import {
  ALERT_DOMAINS,
  alertDomain,
  formatAlertTimestamp,
  MonitoringAlertsPanel,
} from "../components/alerts/MonitoringAlertsPanel";
import type { MonitoringAlert } from "../api/client";

function makeAlert(overrides: Partial<MonitoringAlert> = {}): MonitoringAlert {
  return {
    alert_id: "alert-1",
    created_at: "2026-07-16T10:00:00Z",
    alert_type: "DRIFT_DETECTED",
    severity: "warning",
    subject_type: "model_artifact",
    subject_id: "model-1",
    market_class: null,
    symbol: null,
    timeframe: null,
    model_artifact_id: "model-1",
    signal_id: null,
    summary: "Drift monitoring evidence requires operator review.",
    evidence: { drift_detected: true },
    lineage: { source: "w2_u10_drift_monitoring_record" },
    acknowledged: false,
    acknowledged_at: null,
    acknowledged_by: null,
    audit_correlation_id: "corr-1",
    ...overrides,
  };
}

const MARKET_ALERT = makeAlert({
  alert_id: "a-market",
  alert_type: "LIVE_DATA_STALE",
  subject_type: "market_series",
  subject_id: "forex:EURUSD:M1",
  market_class: "forex",
  symbol: "EURUSD",
  timeframe: "M1",
  model_artifact_id: null,
  lineage: { source: "w1_live_market_observability" },
});

const SIGNAL_ALERT = makeAlert({
  alert_id: "a-signal",
  alert_type: "SIGNAL_WITHHELD",
  subject_type: "advisory_signal",
  subject_id: "sig-1",
  model_artifact_id: null,
  signal_id: "sig-1",
  lineage: { source: "w1_observability" },
});

const RISK_ALERT = makeAlert({ alert_id: "a-risk" });

const SYSTEM_ALERT = makeAlert({
  alert_id: "a-system",
  alert_type: "INFERENCE_HEALTH_DEGRADED",
  subject_type: "system_component",
  subject_id: "live-inference-engine",
  model_artifact_id: null,
  lineage: { source: "w1_observability" },
});

const RESEARCH_ALERT = makeAlert({
  alert_id: "a-research",
  alert_type: "UNKNOWN_SUBJECT_ALERT",
  subject_type: "something_unmapped",
  subject_id: "x-1",
  model_artifact_id: null,
  lineage: {},
});

describe("BO-F-04.1 — data-origin-derived domain mapping", () => {
  it("maps each persisted-subject family to its domain", () => {
    expect(alertDomain(MARKET_ALERT)).toBe("market");
    expect(alertDomain(SIGNAL_ALERT)).toBe("signal");
    expect(alertDomain(RISK_ALERT)).toBe("risk");
    expect(alertDomain(SYSTEM_ALERT)).toBe("system");
  });

  it("derives the domain from the field, not the label: signal_id wins over subject_type", () => {
    const mixed = makeAlert({
      subject_type: "model_artifact",
      model_artifact_id: "m-1",
      signal_id: "s-9",
    });
    expect(alertDomain(mixed)).toBe("signal");
  });

  it("market_class alone attributes an alert to the market domain", () => {
    const byMarketClass = makeAlert({
      subject_type: "something_custom",
      market_class: "crypto",
      model_artifact_id: null,
    });
    expect(alertDomain(byMarketClass)).toBe("market");
  });

  it("unknown/null-fielded subjects fall to the documented neutral research bucket — never invented", () => {
    expect(alertDomain(RESEARCH_ALERT)).toBe("research");
    const allNull = makeAlert({
      subject_type: "whatever",
      model_artifact_id: null,
      market_class: null,
    });
    expect(alertDomain(allNull)).toBe("research");
    expect(ALERT_DOMAINS).toEqual(["market", "signal", "risk", "research", "system"]);
  });
});

describe("BO-F-04.1 — the domain filter control", () => {
  const ALL_FIVE = [MARKET_ALERT, SIGNAL_ALERT, RISK_ALERT, SYSTEM_ALERT, RESEARCH_ALERT];

  function renderPanel(alerts = ALL_FIVE) {
    return render(<MonitoringAlertsPanel alerts={alerts} />);
  }

  it("renders ALL + five domain tabs with ALL selected by default", () => {
    renderPanel();
    for (const domain of ["all", "market", "signal", "risk", "research", "system"]) {
      expect(screen.getByTestId(`alerts-domain-${domain}`)).toBeInTheDocument();
    }
    expect(screen.getByTestId("alerts-domain-all")).toHaveAttribute("aria-selected", "true");
    expect(screen.getByTestId("alerts-domain-count")).toHaveTextContent("5/5");
  });

  it("filters client-side per domain with an accurate count", () => {
    renderPanel();
    fireEvent.click(screen.getByTestId("alerts-domain-market"));
    expect(screen.getByTestId("alert-item-a-market")).toBeInTheDocument();
    expect(screen.queryByTestId("alert-item-a-signal")).not.toBeInTheDocument();
    expect(screen.queryByTestId("alert-item-a-risk")).not.toBeInTheDocument();
    expect(screen.getByTestId("alerts-domain-count")).toHaveTextContent("1/5");

    fireEvent.click(screen.getByTestId("alerts-domain-risk"));
    expect(screen.getByTestId("alert-item-a-risk")).toBeInTheDocument();
    expect(screen.queryByTestId("alert-item-a-market")).not.toBeInTheDocument();
  });

  it("renders an honest empty notice for a domain with no alerts", () => {
    renderPanel([MARKET_ALERT]);
    fireEvent.click(screen.getByTestId("alerts-domain-system"));
    expect(screen.getByTestId("alerts-domain-empty")).toHaveTextContent(
      "No alerts in the system domain.",
    );
    // The underlying list is non-empty, so the global empty state stays hidden.
    expect(screen.queryByTestId("alerts-empty")).not.toBeInTheDocument();
  });

  it("every alert card carries its derived domain chip", () => {
    renderPanel();
    expect(screen.getByTestId("alert-domain-a-market")).toHaveAttribute("data-domain", "market");
    expect(screen.getByTestId("alert-domain-a-signal")).toHaveAttribute("data-domain", "signal");
    expect(screen.getByTestId("alert-domain-a-research")).toHaveAttribute("data-domain", "research");
  });
});

describe("BO-F-04.2 — timestamp + lineage surfacing", () => {
  it("formats the created_at as absolute UTC (never a relative age)", () => {
    expect(formatAlertTimestamp("2026-07-16T10:00:00Z")).toBe("2026-07-16 10:00 UTC");
    // Invalid input falls back to the raw string (honest, not fabricated).
    expect(formatAlertTimestamp("not-a-date")).toBe("not-a-date");
  });

  it("renders the absolute timestamp and lineage source on every card", () => {
    render(
      <MonitoringAlertsPanel
        alerts={[MARKET_ALERT, RESEARCH_ALERT]}
      />,
    );
    expect(screen.getByTestId("alert-created-a-market")).toHaveTextContent(
      "Created: 2026-07-16 10:00 UTC",
    );
    expect(screen.getByTestId("alert-lineage-a-market")).toHaveTextContent(
      "Lineage: w1_live_market_observability",
    );
    // No lineage source -> honest "none", never invented.
    expect(screen.getByTestId("alert-lineage-a-research")).toHaveTextContent("Lineage: none");
  });

  it("the detail record surfaces the derived domain alongside the full field set", () => {
    render(<MonitoringAlertsPanel alerts={[RISK_ALERT]} detailAlert={RISK_ALERT} />);
    expect(screen.getByTestId("alerts-detail-domain")).toHaveTextContent("risk");
    expect(screen.getByTestId("alerts-detail-record")).toHaveTextContent("2026-07-16T10:00:00Z");
  });
});

describe("BO-F-04.3 — read-state-only ack discipline preserved", () => {
  it("Acknowledge renders only for unacknowledged alerts and disables while acknowledging", () => {
    render(
      <MonitoringAlertsPanel
        alerts={[
          makeAlert({ alert_id: "unacked", acknowledged: false }),
          makeAlert({ alert_id: "acked", acknowledged: true }),
        ]}
        onAcknowledge={() => undefined}
        acknowledgingId="unacked"
      />,
    );
    expect(screen.getByTestId("alert-ack-unacked")).toBeDisabled();
    expect(screen.getByTestId("alert-ack-unacked")).toHaveTextContent("Acknowledging…");
    expect(screen.queryByTestId("alert-ack-acked")).not.toBeInTheDocument();
  });

  it("no remediation/actuation vocabulary anywhere in the panel controls", () => {
    render(
      <MonitoringAlertsPanel
        alerts={[MARKET_ALERT, SIGNAL_ALERT, RISK_ALERT, SYSTEM_ALERT, RESEARCH_ALERT]}
        onRefresh={() => undefined}
        onAcknowledge={() => undefined}
        onSelectDetail={() => undefined}
      />,
    );
    const controls = screen
      .getAllByRole("button")
      .map((button) => button.textContent ?? "")
      .join(" ")
      .toLowerCase();
    for (const banned of [
      "buy",
      "sell",
      "order",
      "execute",
      "remediate",
      "resolve",
      "dismiss",
      "clear alert",
    ]) {
      expect(controls).not.toContain(banned);
    }
  });
});
