import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import {
  ALERTS_DISCLAIMER,
  ALERTS_LIST_CAP,
  MonitoringAlertsPanel,
  severityClass,
} from "./MonitoringAlertsPanel";
import type { MonitoringAlert } from "../../api/client";

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

describe("MonitoringAlertsPanel", () => {
  it("renders alerts as read-only information", () => {
    render(<MonitoringAlertsPanel alerts={[makeAlert()]} />);
    expect(screen.getByText("Monitoring Alerts")).toBeInTheDocument();
    expect(screen.getByText("DRIFT_DETECTED")).toBeInTheDocument();
    expect(screen.getByText(/do not retrain, remediate, or act/i)).toBeInTheDocument();
    expect(screen.getByText("warning")).toBeInTheDocument();
    const buttonText = screen.queryAllByRole("button").map((item) => item.textContent ?? "").join(" ");
    const forbidden = ["b" + "uy", "s" + "ell", "or" + "der", "exec" + "ute", "remed" + "iate"];
    for (const word of forbidden) {
      expect(buttonText.toLowerCase()).not.toContain(word);
    }
  });

  it("test_surf_p02_r1_disclaimer_rendered_verbatim", () => {
    render(<MonitoringAlertsPanel alerts={[makeAlert()]} />);
    expect(screen.getByText(ALERTS_DISCLAIMER)).toBeInTheDocument();
  });

  it("test_surf_p02_m1_acknowledge_label_is_read_state_only", () => {
    render(<MonitoringAlertsPanel alerts={[makeAlert()]} onAcknowledge={() => undefined} />);
    // M1: the exact label — and never Resolve/Dismiss/Clear/Fix/Action/Handle.
    expect(screen.getByText("Acknowledge")).toBeInTheDocument();
    const allText = document.body.textContent ?? "";
    for (const banned of ["Resolve", "Dismiss", "Clear alert", "Fix", "Action", "Handle"]) {
      expect(allText).not.toContain(banned);
    }
  });

  it("test_surf_p02_m3_acknowledged_alerts_remain_visible_by_default", () => {
    render(
      <MonitoringAlertsPanel
        alerts={[makeAlert({ acknowledged: true, acknowledged_at: "2026-07-16T11:00:00Z" })]}
        onAcknowledge={() => undefined}
      />,
    );
    // The acknowledged alert stays in the list with its read state shown…
    expect(screen.getByText("DRIFT_DETECTED")).toBeInTheDocument();
    expect(screen.getByText(/Ack: yes/)).toBeInTheDocument();
    // …and no Acknowledge control renders for it (already read).
    expect(screen.queryByText("Acknowledge")).not.toBeInTheDocument();
  });

  it("test_surf_p02_s4_severity_mapping_handles_all_three_literal_values", () => {
    expect(severityClass("critical")).toBe("danger");
    expect(severityClass("warning")).toBe("degraded");
    expect(severityClass("info")).toBe("stub");
    render(
      <MonitoringAlertsPanel
        alerts={[
          makeAlert({ alert_id: "a-crit", severity: "critical" }),
          makeAlert({ alert_id: "a-warn", severity: "warning" }),
          makeAlert({ alert_id: "a-info", severity: "info" }),
        ]}
      />,
    );
    expect(screen.getByTestId("alert-severity-a-crit")).toHaveClass("danger");
    expect(screen.getByTestId("alert-severity-a-warn")).toHaveClass("degraded");
    expect(screen.getByTestId("alert-severity-a-info")).toHaveClass("stub");
  });

  it("test_surf_p02_s6_list_cap_is_disclosed_when_reached", () => {
    const many = Array.from({ length: ALERTS_LIST_CAP }, (_, i) =>
      makeAlert({ alert_id: `alert-${i}` }),
    );
    render(<MonitoringAlertsPanel alerts={many} />);
    expect(screen.getByTestId("alerts-list-cap-note")).toHaveTextContent(
      `Showing the most recent ${ALERTS_LIST_CAP} alerts (list cap).`,
    );
  });

  it("test_surf_p02_s5_detail_record_renders_stored_fields", () => {
    const alert = makeAlert({
      acknowledged: true,
      acknowledged_at: "2026-07-16T11:00:00Z",
      acknowledged_by: "lead_operator",
      evidence: { drift_detected: true, ks_statistic: 0.31 },
      lineage: { source: "w2_u10_drift_monitoring_record" },
    });
    render(
      <MonitoringAlertsPanel alerts={[alert]} detailAlert={alert} onCloseDetail={() => undefined} />,
    );
    const detail = screen.getByTestId("alerts-detail-record");
    expect(detail).toHaveTextContent("alert-1");
    expect(detail).toHaveTextContent("Acknowledged");
    expect(detail).toHaveTextContent("yes at 2026-07-16T11:00:00Z by lead_operator");
    expect(detail).toHaveTextContent("ks_statistic");
    expect(detail).toHaveTextContent("w2_u10_drift_monitoring_record");
    expect(screen.getByTestId("alert-detail-close")).toBeInTheDocument();
  });

  it("test_surf_p02_m2_ack_error_is_surfaced_explicitly", () => {
    render(
      <MonitoringAlertsPanel alerts={[makeAlert()]} ackError="Failed to acknowledge alert" />,
    );
    expect(screen.getByTestId("alerts-ack-error")).toHaveTextContent(
      "Failed to acknowledge alert",
    );
  });

  it("test_surf_p02_s7_testids_cover_every_major_region", () => {
    render(
      <MonitoringAlertsPanel
        alerts={[makeAlert()]}
        onRefresh={() => undefined}
        onAcknowledge={() => undefined}
        onSelectDetail={() => undefined}
      />,
    );
    expect(screen.getByTestId("monitoring-alerts-panel")).toBeInTheDocument();
    expect(screen.getByTestId("alerts-refresh-btn")).toBeInTheDocument();
    expect(screen.getByTestId("alerts-list")).toBeInTheDocument();
    expect(screen.getByTestId("alert-item-alert-1")).toBeInTheDocument();
    expect(screen.getByTestId("alert-ack-alert-1")).toBeInTheDocument();
    expect(screen.getByTestId("alert-detail-open-alert-1")).toBeInTheDocument();
    expect(screen.getByTestId("alert-severity-alert-1")).toBeInTheDocument();
  });
});
