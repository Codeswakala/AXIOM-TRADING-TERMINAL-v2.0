/**
 * TerminalAlertsDock — SURF-P02 integration mount for the ALERTS right-dock
 * tab. Consumes AlertsProvider (shared list + unread state), owns the
 * operator-selected detail fetch (S5), and renders the extended
 * MonitoringAlertsPanel — the single alerts surface.
 *
 * Acknowledge passes through to the provider: read-state only, confirmed by
 * the API before the state renders (M2), acknowledged alerts stay visible
 * (M3). This surface reads; the R1 disclaimer sentence rendered by the panel
 * states its constitutional boundary.
 */
import { useState } from "react";
import { fetchMonitoringAlertDetail, type MonitoringAlert } from "../../api/client";
import { useMonitoringAlerts } from "../alerts/AlertsProvider";
import { MonitoringAlertsPanel } from "../alerts/MonitoringAlertsPanel";

export function TerminalAlertsDock() {
  const {
    alerts,
    loading,
    error,
    ackError,
    acknowledgingId,
    refresh,
    acknowledge,
  } = useMonitoringAlerts();

  const [detailAlert, setDetailAlert] = useState<MonitoringAlert | null>(null);
  const [detailLoading, setDetailLoading] = useState(false);
  const [detailError, setDetailError] = useState<string | null>(null);

  async function selectDetail(alertId: string) {
    setDetailLoading(true);
    setDetailError(null);
    setDetailAlert(null);
    try {
      setDetailAlert(await fetchMonitoringAlertDetail(alertId));
    } catch (err) {
      setDetailError(err instanceof Error ? err.message : "Failed to load alert record");
    } finally {
      setDetailLoading(false);
    }
  }

  return (
    <div className="terminal-alerts-dock" data-testid="terminal-alerts-dock">
      <MonitoringAlertsPanel
        alerts={alerts}
        loading={loading}
        error={error}
        ackError={ackError}
        acknowledgingId={acknowledgingId}
        onRefresh={refresh}
        onAcknowledge={(alertId) => void acknowledge(alertId)}
        detailAlert={detailAlert}
        detailLoading={detailLoading}
        detailError={detailError}
        onSelectDetail={(alertId) => void selectDetail(alertId)}
        onCloseDetail={() => setDetailAlert(null)}
      />
    </div>
  );
}
