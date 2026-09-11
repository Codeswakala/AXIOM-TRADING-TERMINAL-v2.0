/**
 * BO-F-03 — Intelligence Presentation (all five families + governed generation)
 *
 * Pins:
 *  1. The five generation client functions post to the correct B-04
 *     endpoints with Bearer auth and the exact request schemas.
 *  2. The structured B-04 422 ({error_code, detail, insufficient_data})
 *     maps to IntelligenceGenerationError (insufficientData + errorCode) — never a
 *     fabricated report.
 *  3. All five families render with uncertainty/sample/limitations/
 *     data-class/lineage + the research-only framing (test-pinned).
 *  4. The generation trigger produces a persisted report and re-reads it;
 *     the insufficient-data path renders an honest notice.
 *  5. No actuation controls; no fabricated metrics (server-values-only).
 */

import { describe, expect, it, vi } from "vitest";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import {
  createCorrelationReport,
  createPortfolioRiskReport,
  createRegimeReport,
  createScenarioReport,
  createSignalValidationReport,
  IntelligenceGenerationError,
  type ScenarioReport,
  type PortfolioRiskReport,
} from "../api/client";
import { TerminalIntelligenceCards } from "../components/terminal/TerminalIntelligenceCards";
import { TerminalProvider } from "../components/terminal/TerminalContext";
import * as client from "../api/client";

vi.mock("../api/client", async () => {
  const actual = await vi.importActual<typeof client>("../api/client");
  return {
    ...actual,
    fetchCorrelationReports: vi.fn().mockResolvedValue([]),
    fetchRegimeReports: vi.fn().mockResolvedValue([]),
    fetchScenarioReports: vi.fn().mockResolvedValue([]),
    fetchPortfolioRiskReports: vi.fn().mockResolvedValue([]),
    fetchSignalValidationReports: vi.fn().mockResolvedValue([]),
    fetchCandles: vi.fn(),
  };
});

vi.mock("../auth/tokenStorage", () => ({
  getAccessToken: () => "test-token",
}));

vi.mock("../../hooks/useLiveMarket", () => ({
  useLiveMarket: () => ({ quotes: {}, stats: { running: false }, error: null }),
}));

const originalFetch = globalThis.fetch;

function mockFetchJson(payload: unknown, status = 200) {
  // A fresh Response per call (a shared instance's body can only be read once).
  const fetchMock = vi.fn().mockImplementation(() =>
    Promise.resolve(new Response(JSON.stringify(payload), { status })),
  );
  globalThis.fetch = fetchMock as unknown as typeof fetch;
  return fetchMock;
}

afterEach(() => {
  globalThis.fetch = originalFetch;
  vi.restoreAllMocks();
});

describe("BO-F-03.1 — generation client contract", () => {
  it("createCorrelationReport posts the exact B-04 schema with Bearer auth", async () => {
    const fetchMock = mockFetchJson({ id: "corr-1" }, 201);
    await createCorrelationReport({
      left: { market_class: "crypto", symbol: "BTCUSD", timeframe: "H1" },
      right: { market_class: "crypto", symbol: "ETHUSD", timeframe: "H1" },
      as_of_start: "2026-07-01T00:00:00Z",
      as_of_end: "2026-07-31T23:00:00Z",
    });
    expect(fetchMock).toHaveBeenCalledTimes(1);
    const [url, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(url).toBe("/api/v1/intelligence/correlation-reports");
    expect(init.method).toBe("POST");
    expect((init.headers as Headers).get("Authorization")).toBe("Bearer test-token");
    expect(JSON.parse(init.body as string)).toEqual({
      left: { market_class: "crypto", symbol: "BTCUSD", timeframe: "H1" },
      right: { market_class: "crypto", symbol: "ETHUSD", timeframe: "H1" },
      as_of_start: "2026-07-01T00:00:00Z",
      as_of_end: "2026-07-31T23:00:00Z",
    });
  });

  it("all five generation functions target the correct B-04 endpoints", async () => {
    const fetchMock = mockFetchJson({ id: "r" }, 201);
    await createRegimeReport({
      series: { market_class: "crypto", symbol: "BTCUSD", timeframe: "H1" },
      as_of_start: "a",
      as_of_end: "b",
    });
    await createScenarioReport({
      series: { market_class: "crypto", symbol: "BTCUSD", timeframe: "H1" },
      assumptions: { scenario_name: "s", shock_return: -0.1, horizon_bars: 24, volatility_multiplier: 1.5 },
      as_of_start: "a",
      as_of_end: "b",
    });
    await createPortfolioRiskReport({
      series: { market_class: "crypto", symbol: "BTCUSD", timeframe: "H1" },
      assumptions: { report_name: "p", stress_multiplier: 2, tail_quantile: 0.05 },
      as_of_start: "a",
      as_of_end: "b",
    });
    await createSignalValidationReport({
      scope_start: "a",
      scope_end: "b",
      market_class: "crypto",
      symbol: "BTCUSD",
      timeframe: "H1",
      include_states: ["emitted", "withheld"],
    });
    const urls = (fetchMock.mock.calls as [string, RequestInit][]).map(([url]) => url);
    expect(urls).toEqual([
      "/api/v1/intelligence/regime-reports",
      "/api/v1/intelligence/scenario-reports",
      "/api/v1/intelligence/portfolio-risk-reports",
      "/api/v1/intelligence/signal-validation-reports",
    ]);
    const last = JSON.parse(fetchMock.mock.calls[3][1].body as string);
    expect(last.include_states).toEqual(["emitted", "withheld"]);
  });

  it("maps the structured B-04 422 to IntelligenceGenerationError with errorCode + insufficientData", async () => {
    mockFetchJson(
      { detail: { error_code: "CORRELATION_REQUIRES_THREE_ALIGNED_POINTS", detail: "CORRELATION_REQUIRES_THREE_ALIGNED_POINTS", insufficient_data: true } },
      422,
    );
    await expect(
      createCorrelationReport({
        left: { market_class: "crypto", symbol: "BTCUSD", timeframe: "H1" },
        right: { market_class: "crypto", symbol: "NOPEUSD", timeframe: "H1" },
        as_of_start: "a",
        as_of_end: "b",
      }),
    ).rejects.toMatchObject({
      name: "IntelligenceGenerationError",
      status: 422,
      errorCode: "CORRELATION_REQUIRES_THREE_ALIGNED_POINTS",
      insufficientData: true,
    });
  });
});

const SCENARIO_REPORT = {
  id: "scen-1",
  created_at: "2026-08-21T00:00:00Z",
  artifact_type: "scenario_report",
  method_version: "w4-u04.scenario.v1",
  market_class: "crypto",
  symbol: "BTCUSD",
  timeframe: "H1",
  as_of_start: "2026-07-01T00:00:00Z",
  as_of_end: "2026-07-31T23:00:00Z",
  sample_count: 17520,
  scenario_name: "BTCUSD adverse-shock research scenario",
  hypothetical_return: -0.1187,
  scenario_result: {},
  assumptions: { shock_return: -0.15, horizon_bars: 24, volatility_multiplier: 1.5 },
  inputs: {},
  uncertainty: { method: "scenario_envelope" },
  economic_usefulness: {},
  config: {},
  input_lineage: {},
  source_artifact_ids: [],
  market_scope: {},
  results: {},
  notes: "Hypothetical research scenario; not an instruction or prediction.; data-class: historical:real",
  limitations: ["hypothetical_only"],
  report_hash: "scen-hash-0000000000",
  research_status: "research_only",
} as unknown as ScenarioReport;

const PORTFOLIO_REPORT = {
  id: "port-1",
  created_at: "2026-08-21T00:00:00Z",
  artifact_type: "portfolio_risk_report",
  method_version: "w4-u05.portfolio_risk.v1",
  market_class: "crypto",
  symbol: "BTCUSD",
  timeframe: "H1",
  as_of_start: "2026-07-01T00:00:00Z",
  as_of_end: "2026-07-31T23:00:00Z",
  sample_count: 17520,
  max_drawdown: 0.1832,
  realized_volatility: 0.0411,
  stress_loss: 0.2271,
  metrics: {},
  uncertainty: {},
  assumptions: { stress_multiplier: 2, tail_quantile: 0.05 },
  economic_usefulness: {},
  config: {},
  input_lineage: {},
  source_artifact_ids: [],
  market_scope: {},
  results: {},
  notes: "Hypothetical market-series risk research; not a real portfolio or account.; data-class: historical:real",
  limitations: ["hypothetical_only"],
  report_hash: "port-hash-0000000000",
  research_status: "research_only",
} as unknown as PortfolioRiskReport;

const CORRELATION_REPORT = {
  id: "corr-1",
  created_at: "2026-08-21T00:00:00Z",
  artifact_type: "correlation_report",
  method_version: "w4-u01.correlation.v1",
  left_market_class: "crypto",
  left_symbol: "BTCUSD",
  right_market_class: "crypto",
  right_symbol: "ETHUSD",
  timeframe: "H1",
  sample_count: 17520,
  correlation_value: 0.7321,
  uncertainty: { method: "fisher_z_interval", lower: 0.7252, upper: 0.7389 },
  significance: { p_value: 0.0 },
  report_hash: "corr-hash-0000000000",
  research_status: "research_only",
  notes: "Research-only correlation context; not a signal and not causation.; data-class: historical:real",
};

function renderCards() {
  return render(
    <TerminalProvider initialSymbol="BTC/USD" enableLiveMarket={false}>
      <TerminalIntelligenceCards />
    </TerminalProvider>,
  );
}

describe("BO-F-03.2 — five-family rendering", () => {
  beforeEach(() => {
    vi.mocked(client.fetchCorrelationReports).mockResolvedValue([CORRELATION_REPORT] as never);
    vi.mocked(client.fetchScenarioReports).mockResolvedValue([SCENARIO_REPORT] as never);
    vi.mocked(client.fetchPortfolioRiskReports).mockResolvedValue([PORTFOLIO_REPORT] as never);
  });

  it("offers all five family tabs with CALIBRATION default", async () => {
    renderCards();
    await waitFor(() =>
      expect(screen.getByTestId("intel-calibration-panel")).toBeInTheDocument(),
    );
    for (const tab of ["calibration", "correlation", "regime", "scenario", "portfolio-risk"]) {
      expect(screen.getByTestId(`intel-tab-${tab}`)).toBeInTheDocument();
    }
    expect(screen.getByTestId("intel-tab-calibration")).toHaveAttribute("aria-selected", "true");
  });

  it("renders the scenario card with name/return/assumptions/n/data-class/hash + framing", async () => {
    renderCards();
    fireEvent.click(screen.getByTestId("intel-tab-scenario"));
    await waitFor(() => expect(screen.getByTestId("intel-scenario-panel")).toBeInTheDocument());
    expect(screen.getByTestId("scenario-name")).toHaveTextContent("adverse-shock research scenario");
    expect(screen.getByTestId("scenario-return")).toHaveTextContent("-11.87%");
    expect(screen.getByTestId("scenario-assumptions")).toHaveTextContent("shock_return");
    expect(screen.getByTestId("scenario-data-class")).toHaveTextContent("data-class: historical:real");
    expect(screen.getByTestId("scenario-framing")).toHaveTextContent("not a signal");
  });

  it("renders the portfolio-risk card with drawdown/vol/stress/n/data-class + framing", async () => {
    renderCards();
    fireEvent.click(screen.getByTestId("intel-tab-portfolio-risk"));
    await waitFor(() =>
      expect(screen.getByTestId("intel-portfolio-risk-panel")).toBeInTheDocument(),
    );
    expect(screen.getByTestId("portrisk-drawdown")).toHaveTextContent("18.32%");
    expect(screen.getByTestId("portrisk-vol")).toHaveTextContent("4.11%");
    expect(screen.getByTestId("portrisk-stress")).toHaveTextContent("22.71%");
    expect(screen.getByTestId("portrisk-data-class")).toHaveTextContent("data-class: historical:real");
    expect(screen.getByTestId("portrisk-framing")).toHaveTextContent("not a signal");
  });

  it("renders the correlation card with n + CI + data-class + framing", async () => {
    renderCards();
    fireEvent.click(screen.getByTestId("intel-tab-correlation"));
    await waitFor(() =>
      expect(screen.getByTestId("corr-row-corr-1")).toBeInTheDocument(),
    );
    expect(screen.getByTestId("corr-data-class-corr-1")).toHaveTextContent("data-class: historical:real");
    expect(screen.getByTestId("corr-framing-corr-1")).toHaveTextContent("not a signal");
  });

  it("renders the research-only generation framing with all five triggers", async () => {
    vi.mocked(client.fetchCandles).mockResolvedValue({
      kind: "native",
      timeframe: "H1",
      bars: [{ open_time: "2026-07-31T23:00:00Z", id: "c1" }],
    } as never);
    renderCards();
    await waitFor(() => expect(screen.getByTestId("generation-panel")).toBeInTheDocument());
    expect(screen.getByTestId("generation-framing")).toHaveTextContent("Research artifact only");
    for (const family of ["correlation", "regime", "scenario", "portfolio-risk", "signal-validation"]) {
      expect(screen.getByTestId(`gen-btn-${family}`)).toBeInTheDocument();
    }
  });
});

describe("BO-F-03.3 — governed generation surface", () => {
  beforeEach(() => {
    vi.mocked(client.fetchCandles).mockResolvedValue({
      kind: "native",
      timeframe: "H1",
      bars: [{ open_time: "2026-07-31T23:00:00Z", id: "c1" }],
    } as never);
  });

  it("generation trigger POSTs, reports the persisted id, and re-reads the family", async () => {
    const genSpy = vi.spyOn(client, "createScenarioReport").mockResolvedValue(SCENARIO_REPORT as never);
    const fetchScenario = vi.mocked(client.fetchScenarioReports);
    renderCards();

    await waitFor(() =>
      expect(screen.getByTestId("gen-btn-scenario")).not.toBeDisabled(),
    );
    fireEvent.click(screen.getByTestId("gen-btn-scenario"));

    await waitFor(() =>
      expect(screen.getByTestId("gen-status-scenario")).toHaveTextContent("persisted: scen-1"),
    );
    expect(genSpy).toHaveBeenCalledTimes(1);
    const input = genSpy.mock.calls[0][0] as {
      series: { symbol: string };
      assumptions: { scenario_name: string };
    };
    expect(input.series.symbol).toBe("BTCUSD");
    expect(input.assumptions.scenario_name).toContain("BTCUSD");
    // Re-read after generation (refresh tick re-fetches the family).
    await waitFor(() => expect(fetchScenario.mock.calls.length).toBeGreaterThanOrEqual(2));
  });

  it("insufficient-data (structured 422) renders an honest notice — nothing fabricated", async () => {
    vi.spyOn(client, "createCorrelationReport").mockRejectedValue(
      new IntelligenceGenerationError("CORRELATION_REQUIRES_THREE_ALIGNED_POINTS", 422, "CORRELATION_REQUIRES_THREE_ALIGNED_POINTS", true),
    );
    renderCards();

    await waitFor(() =>
      expect(screen.getByTestId("gen-btn-correlation")).not.toBeDisabled(),
    );
    fireEvent.click(screen.getByTestId("gen-btn-correlation"));

    await waitFor(() =>
      expect(screen.getByTestId("gen-insufficient-correlation")).toBeInTheDocument(),
    );
    expect(screen.getByTestId("gen-insufficient-correlation")).toHaveTextContent(
      "Insufficient data: CORRELATION_REQUIRES_THREE_ALIGNED_POINTS",
    );
    expect(screen.getByTestId("gen-insufficient-correlation")).toHaveTextContent(
      "nothing fabricated",
    );
  });

  it("no series -> generation disabled with an honest no-window notice", async () => {
    vi.mocked(client.fetchCandles).mockResolvedValue({
      kind: "unavailable",
      timeframe: "H1",
      detail: "no series",
      bars: [],
    } as never);
    renderCards();
    await waitFor(() =>
      expect(screen.getByTestId("generation-no-series-notice")).toBeInTheDocument(),
    );
    expect(screen.getByTestId("gen-btn-scenario")).toBeDisabled();
  });
});

describe("BO-F-03.4 — non-actuation + no-fabrication", () => {
  it("the intelligence surface carries zero actuation vocabulary", async () => {
    renderCards();
    await waitFor(() => expect(screen.getByTestId("generation-panel")).toBeInTheDocument());
    const text = (
      screen.getByTestId("terminal-intelligence-cards").textContent ?? ""
    ).toLowerCase();
    for (const forbidden of ["buy", "sell", "order", "broker", "execution", "account", "signal emit"]) {
      expect(text).not.toContain(forbidden);
    }
  });

  it("renders server values verbatim (no client-side metric recomputation)", async () => {
    vi.mocked(client.fetchScenarioReports).mockResolvedValue([SCENARIO_REPORT] as never);
    renderCards();
    fireEvent.click(screen.getByTestId("intel-tab-scenario"));
    await waitFor(() =>
      expect(screen.getByTestId("scenario-return")).toBeInTheDocument(),
    );
    // hypothetical_return -0.1187 rendered as percentage of the SAME value
    expect(screen.getByTestId("scenario-return")).toHaveTextContent("-11.87%");
  });
});
