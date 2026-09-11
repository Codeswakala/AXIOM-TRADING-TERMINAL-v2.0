/**
 * DATA-P02 fail-first frontend tests — timeframe aggregation honesty (M4/M5/M8),
 * single-source-of-truth timeframe mapping (S2), and session context (M7).
 *
 * Every test here MUST fail against the pre-DATA-P02 tree and pass after the
 * aggregation contract ships:
 *  - the timeframe vocabulary module does not exist yet,
 *  - the notice renders from `timeframe !== "1m"` (hardcoded) instead of the
 *    typed series discriminant,
 *  - the chart performs a client-side M1 fallback for higher timeframes,
 *  - no session-context module exists.
 */
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { TerminalProvider } from "../components/terminal/TerminalContext";
import { TerminalChartStage } from "../components/terminal/TerminalChartStage";
import * as client from "../api/client";
import {
  TIMEFRAME_OPTIONS,
  timeframeCodeOf,
  timeframeMinutesOf,
} from "../api/timeframes";
import {
  SESSIONS,
  sessionsAtTime,
  sessionLabelOfTime,
  overlapPeriodLabel,
  sessionLabelOfBar,
} from "../terminal/sessions";

vi.mock("../api/client", async () => {
  const actual = await vi.importActual<typeof client>("../api/client");
  return {
    ...actual,
    fetchCandles: vi.fn(),
    fetchChartResearchAnnotations: vi.fn().mockResolvedValue([]),
    createChartResearchAnnotation: vi.fn(),
    seedChartHistory: vi.fn(),
  };
});

vi.mock("../components/chart/PriceChart", () => ({
  PriceChart: ({ bars }: { bars: unknown[] }) => (
    <div data-testid="mock-price-chart" data-bars-count={bars.length} />
  ),
}));

const nativeEnvelope = (bars: client.ApiCandle[]) => ({
  kind: "native" as const,
  timeframe: "M1",
  bars,
});

const aggregatedEnvelope = (timeframe: string, bars: client.ApiCandle[]) => ({
  kind: "aggregated" as const,
  timeframe,
  sourceTimeframe: "M1",
  excludedPartialBuckets: 0,
  bars,
});

const unavailableEnvelope = (timeframe: string, detail: string) => ({
  kind: "unavailable" as const,
  timeframe,
  detail,
  bars: [] as client.ApiCandle[],
});

const candle = (minute: number, source = "seed:synthetic"): client.ApiCandle => ({
  id: `c${minute}`,
  market_class: "forex",
  symbol: "EURUSD",
  timeframe: "M1",
  open_time: new Date(Date.UTC(2026, 7, 17, 10, minute)).toISOString(),
  open: "1.10000",
  high: "1.10500",
  low: "1.09900",
  close: "1.10100",
  volume: "100",
  source,
  created_at: new Date(Date.UTC(2026, 7, 17, 10, minute)).toISOString(),
});

const renderStage = () =>
  render(
    <TerminalProvider initialSymbol="EUR/USD" enableLiveMarket={false}>
      <TerminalChartStage />
    </TerminalProvider>,
  );

beforeEach(() => {
  vi.clearAllMocks();
  mockSeries({ M1: nativeEnvelope([candle(0), candle(1)]) });
});

/** Mount always fetches M1 once; clicking a timeframe fetches its code.
 *  M3 asserts the CALL PATTERN — exactly one request per timeframe switch,
 *  and never an M1 re-fetch after a higher-timeframe response. */
function mockSeries(map: Record<string, client.CandleSeriesResult>) {
  vi.mocked(client.fetchCandles).mockImplementation(async (params) => {
    const tf = (params as { timeframe?: string }).timeframe ?? "M1";
    return map[tf] ?? map.M1;
  });
}

describe("DATA-P02 S2 — single source of truth for the timeframe vocabulary", () => {
  it("test_data_p02_frontend_timeframe_table_matches_backend_golden", () => {
    expect(TIMEFRAME_OPTIONS).toEqual([
      { label: "1m", code: "M1", minutes: 1 },
      { label: "5m", code: "M5", minutes: 5 },
      { label: "15m", code: "M15", minutes: 15 },
      { label: "1h", code: "H1", minutes: 60 },
      { label: "4h", code: "H4", minutes: 240 },
      { label: "1d", code: "D1", minutes: 1440 },
    ]);
    expect(timeframeCodeOf("1m")).toBe("M1");
    expect(timeframeCodeOf("1h")).toBe("H1");
    expect(timeframeCodeOf("1d")).toBe("D1");
    expect(timeframeMinutesOf("H4")).toBe(240);
  });
});

describe("DATA-P02 M4/M5 — the notice renders from the typed discriminant", () => {
  it("test_data_p02_native_series_renders_no_resampled_notice", async () => {
    renderStage();
    await waitFor(() =>
      expect(screen.getByTestId("timeframe-native-notice")).toHaveTextContent("Native M1 Stream"),
    );
    expect(screen.queryByTestId("timeframe-resampled-notice")).not.toBeInTheDocument();
    expect(screen.queryByTestId("timeframe-unavailable-state")).not.toBeInTheDocument();
  });

  it("test_data_p02_aggregated_series_renders_accurate_notice_from_discriminant", async () => {
    mockSeries({
      M1: nativeEnvelope([candle(0), candle(1)]),
      H1: aggregatedEnvelope("H1", [candle(0), candle(1), candle(2)]),
    });
    renderStage();
    fireEvent.click(screen.getByTestId("chart-tf-1h"));
    await waitFor(() =>
      expect(screen.getByTestId("timeframe-resampled-notice")).toBeInTheDocument(),
    );
    const notice = screen.getByTestId("timeframe-resampled-notice");
    expect(notice).toHaveTextContent("M1");
    expect(notice).toHaveTextContent("wall-clock aligned");
    expect(notice).toHaveTextContent("60");
    expect(screen.queryByTestId("timeframe-native-notice")).not.toBeInTheDocument();
    // The mock's bars are 1-minute bars; the envelope says aggregated — the
    // notice must follow the DISCRIMINANT, not the bar timestamps or count.
    expect(client.fetchCandles).toHaveBeenLastCalledWith({
      symbol: "EURUSD",
      timeframe: "H1",
      limit: 100,
      order: "asc",
    });
    expect(client.fetchCandles).toHaveBeenCalledTimes(2); // mount M1 + switch H1
  });

  it("test_data_p02_unavailable_series_renders_absence_not_improvisation", async () => {
    mockSeries({
      M1: nativeEnvelope([candle(0), candle(1)]),
      H1: unavailableEnvelope("H1", "insufficient M1 coverage to form a complete H1 bucket"),
    });
    renderStage();
    fireEvent.click(screen.getByTestId("chart-tf-1h"));
    await waitFor(() =>
      expect(screen.getByTestId("timeframe-unavailable-state")).toBeInTheDocument(),
    );
    expect(screen.queryByTestId("timeframe-resampled-notice")).not.toBeInTheDocument();
    expect(screen.queryByTestId("timeframe-native-notice")).not.toBeInTheDocument();
    expect(screen.queryByTestId("mock-price-chart")).not.toBeInTheDocument();
    // M3: one request for the switch and NO M1 re-fetch after it — the
    // client-side fallback is gone.
    expect(client.fetchCandles).toHaveBeenCalledTimes(2);
    expect(client.fetchCandles).toHaveBeenLastCalledWith({
      symbol: "EURUSD",
      timeframe: "H1",
      limit: 100,
      order: "asc",
    });
    const detail = screen.getByTestId("timeframe-unavailable-state");
    expect(detail).toHaveTextContent("insufficient M1 coverage");
  });

  it("test_data_p02_no_m1_fallback_when_higher_timeframe_has_no_native_records", async () => {
    // The old code refetched M1 whenever a higher timeframe returned nothing
    // (3 calls: mount, H4, fallback M1). With the discriminant an unavailable
    // response must not trigger a second request — unaggregated M1 bars are
    // never passed off as H4 again.
    mockSeries({
      M1: nativeEnvelope([candle(0), candle(1)]),
      H4: unavailableEnvelope("H4", "no coverage"),
    });
    renderStage();
    fireEvent.click(screen.getByTestId("chart-tf-4h"));
    await waitFor(() =>
      expect(screen.getByTestId("timeframe-unavailable-state")).toBeInTheDocument(),
    );
    expect(client.fetchCandles).toHaveBeenCalledTimes(2);
    expect(client.fetchCandles).toHaveBeenLastCalledWith({
      symbol: "EURUSD",
      timeframe: "H4",
      limit: 100,
      order: "asc",
    });
  });
});

describe("POST-CLOSURE HOTFIX — timeframe switch must reset when the last bar time regresses", () => {
  it("test_postclosure_time_regression_forces_full_series_reset", () => {
    const source = readFileSync(
      join(process.cwd(), "src/components/chart/PriceChart.tsx"),
      "utf8",
    );
    // Anchor: the regression condition that forces a full reset when the new
    // series' last bar is OLDER than the previous series' last bar (the M6
    // partial-bucket exclusion makes this the NORMAL case on 1m -> 1h/1d).
    const anchorText = "lastTime < lastTimeRef.current";
    expect(source).toContain(anchorText);
    const residue = source.replace(anchorText, "");
    // Non-vacuity: without the anchor, the remaining guard is count-based
    // only — the exact shape that crashed the stage on a plain timeframe
    // switch with no live bar merged.
    expect(residue).toContain("bars.length < lastLenRef.current");
    expect(residue).toContain("bars.length > lastLenRef.current + 5");
  });
});

describe("DATA-P02 M8 — T-1 guard with non-vacuity anchors", () => {
  it("test_data_p02_honesty_anchor_present_and_hardcoded_notice_trigger_absent", () => {
    const source = readFileSync(
      join(process.cwd(), "src/components/terminal/TerminalChartStage.tsx"),
      "utf8",
    );
    // Anchor sentence: the aggregation disclosure text the guard protects.
    // Its removal must fail the build — M8 pins the honesty text itself.
    const anchor = "wall-clock aligned";
    expect(source).toContain(anchor);
    const residue = source.replace(anchor, "");

    // The pre-fix hardcoded triggers must be gone: the notice may no longer
    // render from a timeframe label comparison, and the annotation metadata
    // may no longer hardcode "resampled" for every non-1m timeframe.
    expect(residue).not.toContain('timeframe !== "1m"');
    expect(residue).not.toContain('"native" : "resampled"');
    // The client-side M1 fallback must be gone (M3).
    expect(residue).not.toContain("rawCandles.length === 0");
    // The series kind must be a discriminant, not inferred from bar counts.
    expect(residue).not.toContain("bars.length === 0 ? kind");
  });
});

describe("DATA-P02 M7 — session context (UTC boundaries and overlaps)", () => {
  it("test_data_p02_sessions_utc_boundaries", () => {
    const cases: Array<[string, string[]]> = [
      ["2026-08-18T06:59:00Z", ["tokyo"]],
      ["2026-08-18T07:00:00Z", ["tokyo", "london"]],
      ["2026-08-18T09:00:00Z", ["london"]],
      ["2026-08-18T11:59:00Z", ["london"]],
      ["2026-08-18T12:00:00Z", ["london", "newyork"]],
      ["2026-08-18T16:00:00Z", ["newyork"]],
      ["2026-08-18T20:59:00Z", ["newyork"]],
      ["2026-08-18T21:00:00Z", []],
      ["2026-08-18T23:59:00Z", []],
      ["2026-08-18T00:00:00Z", ["tokyo"]],
    ];
    for (const [iso, expected] of cases) {
      const active = sessionsAtTime(new Date(iso)).map((s) => s.id);
      expect(active).toEqual(expected);
    }
  });

  it("test_data_p02_sessions_closed_on_weekend", () => {
    // Saturday 10:00 UTC — FX sessions are closed; a weekend bar falls in no
    // session and must say so, not inherit Friday's label.
    expect(sessionsAtTime(new Date("2026-08-15T10:00:00Z"))).toEqual([]);
    expect(sessionLabelOfTime(new Date("2026-08-15T10:00:00Z"))).toContain("CLOSED");
  });

  it("test_data_p02_session_overlap_periods_labelled", () => {
    // 08:00 UTC: Tokyo + London overlap (07:00–09:00 UTC).
    const label = sessionLabelOfTime(new Date("2026-08-18T08:00:00Z"));
    expect(label).toContain("TOKYO");
    expect(label).toContain("LONDON");
    expect(label).toContain("overlap");
    expect(overlapPeriodLabel("tokyo", "london")).toContain("07:00");
    expect(overlapPeriodLabel("tokyo", "london")).toContain("09:00");
    expect(overlapPeriodLabel("london", "newyork")).toContain("12:00");
    expect(overlapPeriodLabel("london", "newyork")).toContain("16:00");
  });

  it("test_data_p02_bar_session_lookup", () => {
    // A bar stamped 13:00 UTC on a Wednesday falls in the London+New York
    // overlap; one at 03:00 UTC falls in Tokyo alone.
    const weds = new Date("2026-08-19T13:00:00Z");
    expect(sessionLabelOfBar(Math.floor(weds.getTime() / 1000))).toContain("LONDON");
    expect(sessionLabelOfBar(Math.floor(weds.getTime() / 1000))).toContain("NEW YORK");
    const tokyo = new Date("2026-08-19T03:00:00Z");
    expect(sessionLabelOfBar(Math.floor(tokyo.getTime() / 1000))).toBe("TOKYO");
    expect(SESSIONS.map((s) => s.id)).toEqual(["tokyo", "london", "newyork"]);
  });
});
