/**
 * BO-F-02 — Signal Presentation: Two Families (Structural + Predictive)
 *
 * Pins:
 *  1. Two-family framing: explicit family tabs, both families visible as
 *     distinct surfaces, predictive labeled "PREDICTIVE (ML)".
 *  2. Structural derivation: `deriveStructuralEvents` faithfully transcribes
 *     non-null indicator-series markers into events (type/direction/time/
 *     symbol/timeframe); unknown lines are never invented; FVG edges pair by
 *     timestamp; all-null series yields zero events (no fabrication).
 *  3. Structural framing: "descriptive — not a prediction"; honest empty and
 *     unavailable states.
 *  4. Predictive family: deferred-empty state states the deferral honestly;
 *     existing filters/behavior preserved (default family is predictive).
 *  5. No-actuation: neither surface carries order/execution vocabulary.
 */

import { describe, expect, it, vi } from "vitest";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import {
  deriveStructuralEvents,
  MAX_STRUCTURAL_EVENTS,
  STRUCTURAL_SIGNAL_INDICATORS,
  StructuralSignalStream,
} from "../components/terminal/StructuralSignalStream";
import { TerminalSignalStream } from "../components/terminal/TerminalSignalStream";
import { TerminalProvider } from "../components/terminal/TerminalContext";
import type { IndicatorSeriesEnvelope } from "../api/client";
import * as client from "../api/client";

vi.mock("../api/client", async () => {
  const actual = await vi.importActual<typeof client>("../api/client");
  return {
    ...actual,
    fetchAdvisorySignals: vi.fn().mockResolvedValue([]),
    fetchSignalValidationReports: vi.fn().mockResolvedValue([]),
    fetchInstitutionalIntelligenceBundle: vi.fn().mockResolvedValue(null),
    fetchIndicatorSeries: vi.fn(),
  };
});

vi.mock("../../hooks/useLiveMarket", () => ({
  useLiveMarket: () => ({
    quotes: {},
    stats: { running: false },
    start: vi.fn(),
    stop: vi.fn(),
    error: null,
  }),
}));

function envelope(
  seriesKind: IndicatorSeriesEnvelope["seriesKind"] = "native",
  indicators: IndicatorSeriesEnvelope["indicators"] = {},
): IndicatorSeriesEnvelope {
  return {
    symbol: "EURUSD",
    timeframe: "H1",
    seriesKind,
    sourceTimeframe: null,
    excludedPartialBuckets: null,
    detail: null,
    indicators,
  };
}

const point = (time: string, value: string | null) => ({ time, value });

describe("BO-F-02.2 — deriveStructuralEvents (pure transcription)", () => {
  it("transcribes non-null markers into typed events with direction and time", () => {
    const env = envelope("native", {
      BOS55: {
        shape: "multi",
        kind: "computed",
        lines: {
          bos_up: [point("2026-08-20T12:00:00Z", null), point("2026-08-20T13:00:00Z", "1.1052")],
          bos_down: [point("2026-08-20T12:00:00Z", null), point("2026-08-20T14:00:00Z", "1.0981")],
        },
      },
      CHOCH55: {
        shape: "multi",
        kind: "computed",
        lines: {
          choch_up: [point("2026-08-20T15:00:00Z", "1.1110")],
          choch_down: [point("2026-08-20T15:00:00Z", null)],
        },
      },
    });
    const events = deriveStructuralEvents(env);
    expect(events).toHaveLength(3);
    const bosUp = events.find((event) => event.id === "BOS55:bos_up:2026-08-20T13:00:00Z");
    expect(bosUp).toMatchObject({
      type: "BOS",
      direction: "up",
      label: "Break of structure upward",
      level: 1.1052,
      symbol: "EURUSD",
      timeframe: "H1",
    });
    const chochUp = events.find((event) => event.type === "CHoCH" && event.direction === "up");
    expect(chochUp?.level).toBe(1.111);
  });

  it("pairs FVG top/bottom edges at a shared timestamp into one zone event", () => {
    const env = envelope("native", {
      FVG3: {
        shape: "multi",
        kind: "computed",
        lines: {
          fvg_top: [point("2026-08-20T13:00:00Z", "1.1100")],
          fvg_bottom: [point("2026-08-20T13:00:00Z", "1.1060")],
        },
      },
    });
    const events = deriveStructuralEvents(env);
    expect(events).toHaveLength(1);
    expect(events[0]).toMatchObject({
      id: "FVG3:zone:2026-08-20T13:00:00Z",
      type: "FVG",
      direction: "zone",
      label: "Fair value gap zone",
    });
  });

  it("emits single-edge FVG markers when only one edge exists at a timestamp", () => {
    const env = envelope("native", {
      FVG3: {
        shape: "multi",
        kind: "computed",
        lines: {
          fvg_top: [point("2026-08-20T13:00:00Z", "1.1100")],
          fvg_bottom: [point("2026-08-20T13:00:00Z", null)],
        },
      },
    });
    const events = deriveStructuralEvents(env);
    expect(events).toHaveLength(1);
    expect(events[0]).toMatchObject({ label: "Fair value gap top edge", direction: "zone" });
  });

  it("never fabricates: all-null series and unavailable envelopes yield zero events", () => {
    const allNull = envelope("native", {
      BOS55: {
        shape: "multi",
        kind: "computed",
        lines: {
          bos_up: [point("2026-08-20T13:00:00Z", null)],
          bos_down: [point("2026-08-20T13:00:00Z", null)],
        },
      },
      SWINGS55: {
        shape: "multi",
        kind: "computed",
        lines: {
          swing_high: [point("2026-08-20T13:00:00Z", null)],
          swing_low: [point("2026-08-20T13:00:00Z", null)],
        },
      },
    });
    expect(deriveStructuralEvents(allNull)).toHaveLength(0);
    expect(deriveStructuralEvents(envelope("unavailable"))).toHaveLength(0);
  });

  it("never invents meanings for unknown line names (skipped, not mislabeled)", () => {
    const env = envelope("native", {
      BOS55: {
        shape: "multi",
        kind: "computed",
        lines: { some_future_line: [point("2026-08-20T13:00:00Z", "1.1")] },
      },
    });
    expect(deriveStructuralEvents(env)).toHaveLength(0);
  });

  it("sorts newest-first and caps at the bounded event limit", () => {
    const highLines: Record<string, Array<{ time: string; value: string | null }>> = {};
    for (let i = 0; i < MAX_STRUCTURAL_EVENTS + 10; i++) {
      const hour = String(i).padStart(2, "0");
      highLines["swing_high"] = [
        ...(highLines["swing_high"] ?? []),
        point(`2026-08-20T${hour}:00:00Z`, "1.0"),
      ];
    }
    const capped = deriveStructuralEvents(
      envelope("native", {
        SWINGS55: { shape: "multi", kind: "computed", lines: highLines },
      }),
    );
    expect(capped).toHaveLength(MAX_STRUCTURAL_EVENTS);
    expect(capped[0].time > capped[capped.length - 1].time).toBe(true);
  });

  it("covers the full SMC/ICT structural set in the indicator request list", () => {
    expect(STRUCTURAL_SIGNAL_INDICATORS).toEqual([
      "BOS55",
      "CHOCH55",
      "FVG3",
      "STRUCT55",
      "SWINGS55",
    ]);
  });
});

describe("BO-F-02.1/.3 — two-family framing in TerminalSignalStream", () => {
  function renderStream() {
    return render(
      <TerminalProvider initialSymbol="EUR/USD" enableLiveMarket={false}>
        <TerminalSignalStream />
      </TerminalProvider>,
    );
  }

  it("renders the two family tabs with the predictive family labeled and default", () => {
    renderStream();
    expect(screen.getByTestId("signal-family-structural")).toBeInTheDocument();
    expect(screen.getByTestId("signal-family-predictive")).toBeInTheDocument();
    expect(screen.getByTestId("signal-family-predictive")).toHaveAttribute("aria-selected", "true");
    expect(screen.getByTestId("signal-family-structural")).toHaveAttribute("aria-selected", "false");
    expect(screen.getByTestId("predictive-family-label")).toHaveTextContent("PREDICTIVE (ML)");
    // Existing predictive surface preserved at default: state filters present.
    expect(screen.getByTestId("signal-filter-all")).toBeInTheDocument();
  });

  it("switches to the structural family surface on tab click", async () => {
    vi.mocked(client.fetchIndicatorSeries).mockResolvedValue(
      envelope("native", {
        BOS55: {
          shape: "multi",
          kind: "computed",
          lines: { bos_up: [point("2026-08-20T13:00:00Z", "1.1")], bos_down: [] },
        },
      }),
    );
    renderStream();
    fireEvent.click(screen.getByTestId("signal-family-structural"));
    await waitFor(() =>
      expect(screen.getByTestId("structural-signal-stream")).toBeInTheDocument(),
    );
    expect(screen.getByTestId("signal-family-structural")).toHaveAttribute("aria-selected", "true");
    expect(screen.getByTestId("structural-descriptive-framing")).toHaveTextContent(
      "DETERMINISTIC · DESCRIPTIVE — NOT A PREDICTION",
    );
    // The predictive filter bar is not mounted while structural is active.
    expect(screen.queryByTestId("signal-filter-all")).not.toBeInTheDocument();
  });

  it("predictive deferred-empty state states the deferral honestly", async () => {
    renderStream();
    await waitFor(() =>
      expect(screen.getByTestId("signal-deferred-empty-state")).toBeInTheDocument(),
    );
    expect(screen.getByTestId("signal-deferred-empty-state")).toHaveTextContent(
      "predictive track is deferred",
    );
    expect(screen.getByTestId("signal-deferred-empty-state")).toHaveTextContent(
      "Structural family",
    );
  });
});

describe("BO-F-02.2/.4 — StructuralSignalStream surface", () => {
  function renderStructural() {
    return render(
      <TerminalProvider initialSymbol="BTC/USD" enableLiveMarket={false}>
        <StructuralSignalStream />
      </TerminalProvider>,
    );
  }

  it("renders derived events with type/direction/time/symbol/timeframe and descriptive labels", async () => {
    vi.mocked(client.fetchIndicatorSeries).mockResolvedValue(
      envelope("native", {
        BOS55: {
          shape: "multi",
          kind: "computed",
          lines: {
            bos_up: [point("2026-08-20T12:00:00Z", "64645")],
            bos_down: [],
          },
        },
      }),
    );
    renderStructural();
    await waitFor(() =>
      expect(screen.getByTestId("structural-count-badge")).toHaveTextContent("1 EVENTS"),
    );
    const event = screen.getByTestId("structural-event-BOS55:bos_up:2026-08-20T12:00:00Z");
    expect(event).toBeInTheDocument();
    expect(screen.getByTestId("structural-direction-BOS55:bos_up:2026-08-20T12:00:00Z")).toHaveTextContent("UP");
    expect(screen.getByTestId("structural-label-BOS55:bos_up:2026-08-20T12:00:00Z")).toHaveTextContent(
      "Break of structure upward",
    );
    expect(screen.getByTestId("structural-level-BOS55:bos_up:2026-08-20T12:00:00Z")).toHaveTextContent(
      "level 64645",
    );
  });

  it("honest empty state when the series yields no markers", async () => {
    vi.mocked(client.fetchIndicatorSeries).mockResolvedValue(
      envelope("native", {
        BOS55: { shape: "multi", kind: "computed", lines: { bos_up: [], bos_down: [] } },
      }),
    );
    renderStructural();
    await waitFor(() =>
      expect(screen.getByTestId("structural-empty-state")).toBeInTheDocument(),
    );
    expect(screen.getByTestId("structural-empty-state")).toHaveTextContent(
      "No structure events in the current window",
    );
  });

  it("honest unavailable state when the series kind is unavailable", async () => {
    vi.mocked(client.fetchIndicatorSeries).mockResolvedValue(envelope("unavailable"));
    renderStructural();
    await waitFor(() =>
      expect(screen.getByTestId("structural-empty-state")).toBeInTheDocument(),
    );
    expect(screen.getByTestId("structural-empty-state")).toHaveTextContent(
      "indicator series is unavailable",
    );
  });

  it("no-actuation: the structural surface carries zero order/execution vocabulary", async () => {
    vi.mocked(client.fetchIndicatorSeries).mockResolvedValue(
      envelope("native", {
        BOS55: {
          shape: "multi",
          kind: "computed",
          lines: { bos_up: [point("2026-08-20T12:00:00Z", "1.1")], bos_down: [] },
        },
      }),
    );
    renderStructural();
    await waitFor(() =>
      expect(screen.getByTestId("structural-event-BOS55:bos_up:2026-08-20T12:00:00Z")).toBeInTheDocument(),
    );
    const text = (screen.getByTestId("structural-signal-stream").textContent ?? "").toLowerCase();
    for (const forbidden of ["buy", "sell", "order", "broker", "execution", "account"]) {
      expect(text).not.toContain(forbidden);
    }
  });
});
