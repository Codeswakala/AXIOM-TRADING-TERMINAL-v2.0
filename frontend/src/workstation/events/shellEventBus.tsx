import { createContext, useCallback, useContext, useMemo, useRef, type ReactNode } from "react";

export type ShellEvent = {
  type: string;
  source: string;
  timestamp: string;
  payload?: Record<string, unknown>;
};

type ShellEventBus = {
  publish: (event: Omit<ShellEvent, "timestamp">) => ShellEvent;
  recent: () => ShellEvent[];
};

const ShellEventBusContext = createContext<ShellEventBus | null>(null);

export function ShellEventBusProvider({ children }: { children: ReactNode }) {
  const eventsRef = useRef<ShellEvent[]>([]);

  const publish = useCallback((event: Omit<ShellEvent, "timestamp">): ShellEvent => {
    const item = { ...event, timestamp: new Date().toISOString() };
    eventsRef.current = [...eventsRef.current.slice(-24), item];
    return item;
  }, []);

  const recent = useCallback(() => eventsRef.current, []);

  const value = useMemo(() => ({ publish, recent }), [publish, recent]);
  return <ShellEventBusContext.Provider value={value}>{children}</ShellEventBusContext.Provider>;
}

export function useShellEventBus(): ShellEventBus {
  const value = useContext(ShellEventBusContext);
  if (!value) {
    return {
      publish: (event) => ({ ...event, timestamp: new Date().toISOString() }),
      recent: () => [],
    };
  }
  return value;
}
