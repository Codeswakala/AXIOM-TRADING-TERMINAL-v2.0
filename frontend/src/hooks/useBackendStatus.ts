import { useCallback, useEffect, useState } from "react";
import {
  fetchHealth,
  fetchReadiness,
  fetchSystemInfo,
  type HealthResponse,
  type ReadinessResponse,
  type SystemInfoResponse,
} from "../api/client";

export type BackendStatusState = {
  loading: boolean;
  error: string | null;
  health: HealthResponse | null;
  readiness: ReadinessResponse | null;
  system: SystemInfoResponse | null;
  refresh: () => void;
};

export function useBackendStatus(pollMs = 15000): BackendStatusState {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [readiness, setReadiness] = useState<ReadinessResponse | null>(null);
  const [system, setSystem] = useState<SystemInfoResponse | null>(null);
  const [tick, setTick] = useState(0);

  const refresh = useCallback(() => setTick((value) => value + 1), []);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      setLoading(true);
      setError(null);
      try {
        const [healthResult, readyResult, systemResult] = await Promise.all([
          fetchHealth(),
          fetchReadiness(),
          fetchSystemInfo(),
        ]);
        if (cancelled) return;
        setHealth(healthResult);
        setReadiness(readyResult);
        setSystem(systemResult);
      } catch (err) {
        if (cancelled) return;
        setError(err instanceof Error ? err.message : "Failed to reach backend");
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    void load();
    const id = window.setInterval(() => void load(), pollMs);
    return () => {
      cancelled = true;
      window.clearInterval(id);
    };
  }, [pollMs, tick]);

  return { loading, error, health, readiness, system, refresh };
}
