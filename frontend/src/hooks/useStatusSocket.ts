import { useEffect, useState } from "react";
import { fetchWsTicket, getWebSocketUrl } from "../api/client";

export type SocketState = "connecting" | "open" | "closed" | "error" | "unsupported";

/**
 * Authenticated WebSocket readiness hook for the scoped status channel.
 * Uses the same short-lived ticket mechanism as live market streams.
 */
export function useStatusSocket(enabled = true): {
  state: SocketState;
  lastMessage: string | null;
} {
  const [state, setState] = useState<SocketState>("connecting");
  const [lastMessage, setLastMessage] = useState<string | null>(null);

  useEffect(() => {
    if (!enabled || typeof WebSocket === "undefined") {
      setState("unsupported");
      return;
    }

    let cancelled = false;
    let socket: WebSocket | null = null;

    void (async () => {
      setState("connecting");
      let ticket: string;
      try {
        const issued = await fetchWsTicket();
        ticket = issued.ticket;
      } catch {
        if (!cancelled) setState("error");
        return;
      }

      if (cancelled) return;
      try {
        const base = getWebSocketUrl("/ws/status");
        const sep = base.includes("?") ? "&" : "?";
        socket = new WebSocket(`${base}${sep}ticket=${encodeURIComponent(ticket)}`);
      } catch {
        setState("error");
        return;
      }

      socket.onopen = () => setState("open");
      socket.onerror = () => setState("error");
      socket.onclose = () => setState("closed");
      socket.onmessage = (event) => {
        setLastMessage(typeof event.data === "string" ? event.data : "[binary]");
      };
    })();

    return () => {
      cancelled = true;
      socket?.close();
    };
  }, [enabled]);

  return { state, lastMessage };
}
