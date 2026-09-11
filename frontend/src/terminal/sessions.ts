/**
 * DATA-P02 M7 — session context (presentation and labelling over existing
 * data; no generator or walk changes).
 *
 * Session boundaries are pinned to FIXED UTC windows (DST-agnostic) and the
 * convention is disclosed in the delivery report:
 *   TOKYO     00:00–09:00 UTC
 *   LONDON    07:00–16:00 UTC
 *   NEW YORK  12:00–21:00 UTC
 * Overlaps: TOKYO∩LONDON 07:00–09:00 UTC, LONDON∩NEW YORK 12:00–16:00 UTC.
 * FX sessions are closed on weekends — a weekend bar falls in NO session and
 * says so, never inherits a weekday label.
 */

export type SessionId = "tokyo" | "london" | "newyork";

export interface SessionSpec {
  id: SessionId;
  label: string;
  startHour: number; // inclusive, UTC
  endHour: number; // exclusive, UTC
}

export const SESSIONS: readonly SessionSpec[] = [
  { id: "tokyo", label: "TOKYO", startHour: 0, endHour: 9 },
  { id: "london", label: "LONDON", startHour: 7, endHour: 16 },
  { id: "newyork", label: "NEW YORK", startHour: 12, endHour: 21 },
] as const;

const SESSION_BY_ID = new Map(SESSIONS.map((s) => [s.id, s]));

export function isWeekendUtc(date: Date): boolean {
  const day = date.getUTCDay();
  return day === 0 || day === 6;
}

/** Active sessions at a UTC moment. Empty on weekends (market closed). */
export function sessionsAtTime(date: Date): SessionSpec[] {
  if (isWeekendUtc(date)) return [];
  const hour = date.getUTCHours();
  return SESSIONS.filter((s) => hour >= s.startHour && hour < s.endHour);
}

export function overlapPeriodLabel(a: SessionId, b: SessionId): string {
  const sa = SESSION_BY_ID.get(a);
  const sb = SESSION_BY_ID.get(b);
  if (!sa || !sb) return "";
  const start = Math.max(sa.startHour, sb.startHour);
  const end = Math.min(sa.endHour, sb.endHour);
  const hhmm = (h: number) => `${String(h).padStart(2, "0")}:00`;
  return `${hhmm(start)}–${hhmm(end)} UTC`;
}

/** Human label for the session state of a UTC moment. */
export function sessionLabelOfTime(date: Date): string {
  const active = sessionsAtTime(date);
  if (active.length === 0) {
    return isWeekendUtc(date) ? "MARKET CLOSED (WEEKEND)" : "NO ACTIVE SESSION";
  }
  if (active.length === 1) return active[0].label;
  const overlap = overlapPeriodLabel(active[0].id, active[1].id);
  return `${active[0].label} + ${active[1].label} (overlap ${overlap})`;
}

/** Session state of a bar given its epoch-seconds UTC timestamp. */
export function sessionLabelOfBar(epochSeconds: number): string {
  return sessionLabelOfTime(new Date(epochSeconds * 1000));
}

/** UTC wall-clock label HH:MM for a Date. */
export function utcClockLabel(date: Date): string {
  const hh = String(date.getUTCHours()).padStart(2, "0");
  const mm = String(date.getUTCMinutes()).padStart(2, "0");
  return `${hh}:${mm}`;
}
