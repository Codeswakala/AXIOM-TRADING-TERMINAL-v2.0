/**
 * SURF-P02 — provider / dock / rail surfacing suite (Build Order S2, S3, S5,
 * S6, M2, R2, R3). Named tests prove the unread count is genuine (derived
 * from acknowledged === false), absence renders as absence when the count is
 * unknown, acknowledge is confirmed by the API before the state renders (no
 * optimistic update), failures surface explicitly, the detail GET is
 * retrievable on selection, the client default limit is raised, and the rail
 * launcher navigates to the ALERTS dock with a genuine badge.
 */
import { act, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter, Route, Routes, useLocation } from "react-router-dom";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { AlertsProvider } from "./AlertsProvider";
import { TerminalAlertsDock } from "../terminal/TerminalAlertsDock";
import { UnifiedModuleRail } from "../../workstation/navigation/UnifiedModuleRail";
import * as client from "../../api/client";
import type { MonitoringAlert } from "../../api/client";

vi.mock("../../api/client", async () => {
  const actual = await vi.importActual<typeof client>("../../api/client");
  return {
    ...actual,
    fetchMonitoringAlerts: vi.fn(),
    acknowledgeMonitoringAlert: vi.fn(),
    fetchMonitoringAlertDetail: vi.fn(),
  };
});

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

function renderInProvider(ui: React.ReactElement) {
  return render(
    <MemoryRouter>
      <AlertsProvider>{ui}</AlertsProvider>
    </MemoryRouter>,
  );
}

beforeEach(() => {
  vi.clearAllMocks();
});

describe("SURF-P02 — alerts surfacing (provider, dock, rail)", () => {
  it("test_surf_p02_s2_unread_count_is_genuine_from_acknowledged_false", async () => {
    vi.mocked(client.fetchMonitoringAlerts).mockResolvedValue([
      makeAlert({ alert_id: "a1" }),
      makeAlert({ alert_id: "a2" }),
      makeAlert({ alert_id: "a3", acknowledged: true }),
    ]);

    renderInProvider(<TerminalAlertsDock />);

    await waitFor(() => {
      expect(screen.getByTestId("monitoring-alerts-panel")).toBeInTheDocument();
    });
    // 2 unacknowledged of 3 — the count is derived, never assumed.
    expect(screen.getByTestId("alert-ack-a1")).toBeInTheDocument();
    expect(screen.getByTestId("alert-ack-a2")).toBeInTheDocument();
    expect(screen.queryByTestId("alert-ack-a3")).not.toBeInTheDocument();
    // Acknowledged alert remains visible (M3).
    expect(screen.getByTestId("alert-item-a3")).toHaveTextContent("Ack: yes");
  });

  it("test_surf_p02_s2_r3_badge_renders_genuine_count_and_absence_when_unknown", async () => {
    vi.mocked(client.fetchMonitoringAlerts).mockResolvedValue([
      makeAlert({ alert_id: "a1" }),
      makeAlert({ alert_id: "a2", acknowledged: true }),
    ]);

    renderInProvider(<UnifiedModuleRail />);

    await waitFor(() => {
      expect(screen.getByTestId("rail-alerts-badge")).toHaveTextContent("1");
    });
    expect(screen.getByTestId("rail-btn-alerts")).toHaveAttribute(
      "aria-label",
      "System Alerts (1 Unread)",
    );
  });

  it("test_surf_p02_r3_load_failure_renders_absence_in_badge_and_error_in_panel", async () => {
    vi.mocked(client.fetchMonitoringAlerts).mockRejectedValue(new Error("alerts seam down"));

    renderInProvider(
      <>
        <UnifiedModuleRail />
        <TerminalAlertsDock />
      </>,
    );

    await waitFor(() => {
      expect(screen.getByTestId("alerts-load-error")).toHaveTextContent("alerts seam down");
    });
    // R2/R3: the count cannot be determined — the badge renders as absence,
    // never a fabricated 0 or a placeholder.
    expect(screen.queryByTestId("rail-alerts-badge")).not.toBeInTheDocument();
    expect(screen.getByTestId("rail-btn-alerts")).toHaveAttribute("aria-label", "System Alerts");
  });

  it("test_surf_p02_m2_acknowledge_confirmed_before_state_renders", async () => {
    let resolveAck!: (value: MonitoringAlert) => void;
    vi.mocked(client.fetchMonitoringAlerts).mockResolvedValue([makeAlert()]);
    vi.mocked(client.acknowledgeMonitoringAlert).mockImplementation(
      () =>
        new Promise<MonitoringAlert>((resolve) => {
          resolveAck = resolve;
        }),
    );

    renderInProvider(<TerminalAlertsDock />);

    await waitFor(() => {
      expect(screen.getByTestId("alert-ack-alert-1")).toBeInTheDocument();
    });
    fireEvent.click(screen.getByTestId("alert-ack-alert-1"));

    // M2: pending — the item still reads unacknowledged and the control shows
    // progress; nothing renders optimistically.
    expect(screen.getByText("Acknowledging…")).toBeInTheDocument();
    expect(screen.getByTestId("alert-item-alert-1")).toHaveTextContent("Ack: no");

    await act(async () => {
      resolveAck(makeAlert({ acknowledged: true, acknowledged_at: "2026-07-16T11:00:00Z" }));
    });

    await waitFor(() => {
      expect(screen.getByTestId("alert-item-alert-1")).toHaveTextContent("Ack: yes");
    });
    // The acknowledged alert remains visible (M3) and its control is gone.
    expect(screen.getByTestId("alert-item-alert-1")).toBeInTheDocument();
    expect(screen.queryByTestId("alert-ack-alert-1")).not.toBeInTheDocument();
  });

  it("test_surf_p02_m2_ack_failure_leaves_alert_unacknowledged_and_surfaces_error", async () => {
    vi.mocked(client.fetchMonitoringAlerts).mockResolvedValue([makeAlert()]);
    vi.mocked(client.acknowledgeMonitoringAlert).mockRejectedValue(
      new Error("Failed to acknowledge alert"),
    );

    renderInProvider(<TerminalAlertsDock />);

    await waitFor(() => {
      expect(screen.getByTestId("alert-ack-alert-1")).toBeInTheDocument();
    });
    fireEvent.click(screen.getByTestId("alert-ack-alert-1"));

    await waitFor(() => {
      expect(screen.getByTestId("alerts-ack-error")).toHaveTextContent(
        "Failed to acknowledge alert",
      );
    });
    // The alert stays unacknowledged and its control remains available.
    expect(screen.getByTestId("alert-item-alert-1")).toHaveTextContent("Ack: no");
    expect(screen.getByTestId("alert-ack-alert-1")).toBeInTheDocument();
  });

  it("test_surf_p02_s5_detail_get_retrieves_record_on_selection", async () => {
    vi.mocked(client.fetchMonitoringAlerts).mockResolvedValue([makeAlert()]);
    vi.mocked(client.fetchMonitoringAlertDetail).mockResolvedValue(
      makeAlert({ acknowledged: true, acknowledged_by: "lead_operator" }),
    );

    renderInProvider(<TerminalAlertsDock />);

    await waitFor(() => {
      expect(screen.getByTestId("alert-detail-open-alert-1")).toBeInTheDocument();
    });
    fireEvent.click(screen.getByTestId("alert-detail-open-alert-1"));

    expect(client.fetchMonitoringAlertDetail).toHaveBeenCalledWith("alert-1");
    await waitFor(() => {
      expect(screen.getByTestId("alerts-detail-record")).toBeInTheDocument();
    });
    expect(screen.getByTestId("alerts-detail-record")).toHaveTextContent("lead_operator");
  });

  it("test_surf_p02_s6_client_default_limit_raised_from_5", () => {
    // The silent default-5 truncation is gone; the default equals the API
    // maximum (200) with the cap disclosed in the panel.
    const clientPath = join(process.cwd(), "src/api/client.ts");
    if (!existsSync(clientPath)) {
      throw new Error(`client.ts not found at ${clientPath}`);
    }
    const source = readFileSync(clientPath, "utf8");
    expect(source).toContain("fetchMonitoringAlerts(limit = 200)");
  });

  it("test_surf_p02_s1_rail_launcher_navigates_to_the_alerts_dock", async () => {
    vi.mocked(client.fetchMonitoringAlerts).mockResolvedValue([makeAlert()]);

    function LocationProbe() {
      const location = useLocation();
      return (
        <div data-testid="location-probe">
          {location.pathname}
          {location.search}
        </div>
      );
    }

    render(
      <MemoryRouter initialEntries={["/research"]}>
        <AlertsProvider>
          <UnifiedModuleRail />
          <Routes>
            <Route path="*" element={<LocationProbe />} />
          </Routes>
        </AlertsProvider>
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByTestId("rail-alerts-badge")).toHaveTextContent("1");
    });
    fireEvent.click(screen.getByTestId("rail-btn-alerts"));

    await waitFor(() => {
      expect(screen.getByTestId("location-probe")).toHaveTextContent("/?dock=alerts");
    });
  });
});
