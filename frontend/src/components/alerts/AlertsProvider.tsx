/**
 * AlertsProvider — SURF-P02 (Build Order SURF-P02, authorized 2026-08-17).
 *
 * Single source of truth for the operator's monitoring alerts, mounted at the
 * shell level so the left-rail badge and the terminal's ALERTS dock share one
 * fetch and one state. The unread count is derived from the API list
 * (`acknowledged === false`) — a genuine count, never a placeholder (S2/R2).
 *
 * If the count cannot be determined (loading or failure), `unreadCount` is
 * `null` and consumers render absence — never 0, never a fabricated number.
 *
 * Acknowledge is read-state only (M1): the state updates only after the API
 * confirms (M2 — no optimistic update), and acknowledged alerts remain in the
 * list (M3). The alerts surface reads; the R1 disclaimer sentence states its
 * constitutional boundary and is rendered verbatim by the panel.
 */
import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import {
  acknowledgeMonitoringAlert,
  fetchMonitoringAlerts,
  type MonitoringAlert,
} from "../../api/client";

export type AlertsContextValue = {
  alerts: MonitoringAlert[];
  /** Genuine count of unacknowledged alerts, or null when unknown. */
  unreadCount: number | null;
  loading: boolean;
  error: string | null;
  ackError: string | null;
  acknowledgingId: string | null;
  refresh: () => void;
  acknowledge: (alertId: string) => Promise<boolean>;
};

const AlertsContext = createContext<AlertsContextValue | undefined>(undefined);

export function AlertsProvider({ children }: { children: ReactNode }) {
  const [alerts, setAlerts] = useState<MonitoringAlert[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [ackError, setAckError] = useState<string | null>(null);
  const [acknowledgingId, setAcknowledgingId] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      setAlerts(await fetchMonitoringAlerts(200));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load monitoring alerts");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  const acknowledge = useCallback(
    async (alertId: string): Promise<boolean> => {
      setAcknowledgingId(alertId);
      setAckError(null);
      try {
        // M2: render the acknowledged state only after the API confirms.
        const updated = await acknowledgeMonitoringAlert(alertId);
        setAlerts((current) =>
          current.map((alert) => (alert.alert_id === alertId ? updated : alert)),
        );
        return true;
      } catch (err) {
        setAckError(err instanceof Error ? err.message : "Failed to acknowledge alert");
        return false;
      } finally {
        setAcknowledgingId(null);
      }
    },
    [],
  );

  const unreadCount = useMemo<number | null>(() => {
    if (loading || error) return null;
    return alerts.filter((alert) => !alert.acknowledged).length;
  }, [alerts, loading, error]);

  const value = useMemo<AlertsContextValue>(
    () => ({
      alerts,
      unreadCount,
      loading,
      error,
      ackError,
      acknowledgingId,
      refresh: () => void load(),
      acknowledge,
    }),
    [alerts, unreadCount, loading, error, ackError, acknowledgingId, load, acknowledge],
  );

  return <AlertsContext.Provider value={value}>{children}</AlertsContext.Provider>;
}

export function useMonitoringAlerts(): AlertsContextValue {
  const context = useContext(AlertsContext);
  if (!context) {
    throw new Error("useMonitoringAlerts must be used within an AlertsProvider");
  }
  return context;
}
