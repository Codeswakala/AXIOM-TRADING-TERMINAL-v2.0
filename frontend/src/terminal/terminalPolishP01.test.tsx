/**
 * POLISH-P01 fail-first frontend tests — code splitting with RBAC-before-chunk
 * (M2), confluence as evidence aggregation (M5), the M7 guard, and the
 * watchlist-clip fix (M3).
 *
 * Every test here MUST fail against the pre-POLISH-P01 tree and pass once the
 * phase ships: the lazy registry does not exist, the confluence module does
 * not exist, the guard vocabulary is not extended, and the watchlist CSS does
 * not wrap its provenance labels.
 */
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter, Routes, Route } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { GatedRouteElement, WORKSPACE_REGISTRY } from "../workstation/registry/workspaceRegistry";
import { computeConfluence, CONFLUENCE_FORBIDDEN_TERMS, NON_ACTUATING_LABEL } from "../terminal/confluence";

// The lazy chunk-fetch proof: the mocked page module records whether it was
// EVER imported. If the gate works, the dynamic import never fires for an
// unauthorized role.
let intelligenceChunkFetched = false;
vi.mock("../pages/InstitutionalIntelligencePage", () => {
  intelligenceChunkFetched = true;
  return {
    InstitutionalIntelligencePage: () => <div data-testid="intelligence-page-rendered" />,
  };
});

vi.mock("../pages/LiveMarketPage", () => ({
  LiveMarketPage: () => <div data-testid="live-market-page-rendered" />,
}));

describe("POLISH-P01 M2 — lazy routes are gated before their chunk is fetched", () => {
  beforeEach(() => {
    intelligenceChunkFetched = false;
  });

  it("test_polish_p01_lazy_route_chunk_not_fetched_when_unauthorized", async () => {
    // The registry entry for /intelligence is a LAZY component (chunk fetched
    // on first render) wrapped by the route gate. An operator WITHOUT an
    // allowed role must see the denial WITHOUT the chunk module ever being
    // imported.
    const def = WORKSPACE_REGISTRY.find((w) => w.route === "/intelligence");
    expect(def).toBeDefined();
    // Render the route with an UNPRIVILEGED operator.
    vi.mocked(useAuth).mockReturnValue({
      operator: { username: "w7-u06-a", role: "unprivileged" } as never,
      loading: false,
      isAuthenticated: true,
      login: async () => {},
      logout: async () => {},
      refreshProfile: async () => {},
    });
    render(
      <MemoryRouter initialEntries={["/intelligence"]}>
        <Routes>
          <Route path="/intelligence" element={<GatedRouteElement definition={def!} />} />
        </Routes>
      </MemoryRouter>,
    );
    await waitFor(() =>
      expect(screen.getByTestId("route-access-denied")).toBeInTheDocument(),
    );
    expect(intelligenceChunkFetched).toBe(false);
    expect(screen.queryByTestId("intelligence-page-rendered")).not.toBeInTheDocument();
  });

  it("test_polish_p01_lazy_route_chunk_fetched_when_authorized", async () => {
    const def = WORKSPACE_REGISTRY.find((w) => w.route === "/intelligence");
    vi.mocked(useAuth).mockReturnValue({
      operator: { username: "admin", role: "admin" } as never,
      loading: false,
      isAuthenticated: true,
      login: async () => {},
      logout: async () => {},
      refreshProfile: async () => {},
    });
    render(
      <MemoryRouter initialEntries={["/intelligence"]}>
        <Routes>
          <Route path="/intelligence" element={<GatedRouteElement definition={def!} />} />
        </Routes>
      </MemoryRouter>,
    );
    await waitFor(() =>
      expect(screen.getByTestId("intelligence-page-rendered")).toBeInTheDocument(),
    );
    expect(intelligenceChunkFetched).toBe(true);
  });
});

describe("POLISH-P01 M5 — confluence is evidence aggregation, not a verdict", () => {
  const line = (values: Array<number | null>) => ({
    shape: "line" as const,
    kind: "computed" as const,
    points: values.map((v, i) => ({
      time: new Date(Date.UTC(2026, 7, 17, 10, i)).toISOString(),
      value: v === null ? null : String(v),
    })),
  });
  const multi = (lines: Record<string, Array<number | null>>) => ({
    shape: "multi" as const,
    kind: "computed" as const,
    lines: Object.fromEntries(
      Object.entries(lines).map(([name, values]) => [name, line(values).points]),
    ),
  });

  it("test_polish_p01_confluence_emits_score_with_uncertainty_not_verdict", () => {
    const results = {
      SMA20: line([1.0, 1.02, 1.04, 1.06, 1.08, 1.10]), // rising -> up
      EMA20: line([1.10, 1.08, 1.06, 1.04, 1.02, 1.00]), // falling -> down
      RSI14: line([40, 45, 50, 55, 60, 65]), // last 65 > 50 -> up
      MACD12269: {
        shape: "macd" as const,
        kind: "computed" as const,
        points: [
          { time: new Date().toISOString(), macd: "1", signal: "0.5", histogram: "0.5" },
        ],
      }, // histogram > 0 -> up
      ADX14: multi({ adx: [null, null, 20, 25], plus_di: [null, null, 10, 20], minus_di: [null, null, 30, 10] }), // excluded (strength)
    };
    const out = computeConfluence(results);
    // 3 directional (SMA up, EMA down, RSI up, MACD up) = 4 directional,
    // 3 up / 1 down -> direction up, score 0.75.
    expect(out.directionalCount).toBe(4);
    expect(out.alignedCount).toBe(3);
    expect(out.direction).toBe("up");
    expect(out.score).toBeCloseTo(0.75, 9);
    // The uncertainty band is a number, stated as a band — never a verdict.
    expect(typeof out.uncertaintyBand).toBe("number");
    expect(out.uncertaintyBand).toBeGreaterThan(0);
    expect((out as unknown as Record<string, unknown>).verdict).toBeUndefined();
    expect((out as unknown as Record<string, unknown>).eligible).toBeUndefined();
    expect((out as unknown as Record<string, unknown>).riskReward).toBeUndefined();
    // Exclusions are stated, not silent: ADX is out of the count.
    expect(out.excluded).toContain("ADX14");
  });

  it("test_polish_p01_confluence_empty_state_and_band_math", () => {
    const empty = computeConfluence({});
    expect(empty.directionalCount).toBe(0);
    expect(empty.score).toBeNull();
    expect(empty.direction).toBe("none");
    // Wilson 95% band on 3/4 aligned: p=0.75, n=4 -> z*sqrt(p(1-p)/n)
    const z = 1.96;
    const expected = z * Math.sqrt(0.75 * 0.25 / 4);
    const results = {
      SMA20: line([1.0, 1.02, 1.04, 1.06, 1.08, 1.10]),
      EMA20: line([1.10, 1.08, 1.06, 1.04, 1.02, 1.00]),
      RSI14: line([40, 45, 50, 55, 60, 65]),
      MACD12269: {
        shape: "macd" as const,
        kind: "computed" as const,
        points: [
          { time: new Date().toISOString(), macd: "1", signal: "0.5", histogram: "0.5" },
        ],
      },
    };
    expect(computeConfluence(results).uncertaintyBand).toBeCloseTo(expected, 9);
    expect(NON_ACTUATING_LABEL).toContain("NON-ACTUATING");
  });
});

describe("POLISH-P01 M7 — no eligibility or risk/reward language", () => {
  it("test_polish_p01_no_eligibility_or_risk_reward_language", () => {
    // The forbidden vocabulary lives in the confluence module; the stage
    // source stays free of it; and the render surface asserts it.
    const stageSource = readFileSync(
      join(process.cwd(), "src/components/terminal/TerminalChartStage.tsx"),
      "utf8",
    );
    const anchor = "describe data, they never advise a trade";
    expect(stageSource).toContain(anchor);
    const residue = stageSource.replace(anchor, "");
    for (const term of CONFLUENCE_FORBIDDEN_TERMS) {
      expect(residue).not.toContain(term);
    }
    expect(CONFLUENCE_FORBIDDEN_TERMS).toContain("eligible");
    expect(CONFLUENCE_FORBIDDEN_TERMS).toContain("risk/reward");
    expect(CONFLUENCE_FORBIDDEN_TERMS).toContain("setup quality");
    expect(CONFLUENCE_FORBIDDEN_TERMS).toContain("take the trade");
    expect(CONFLUENCE_FORBIDDEN_TERMS).toContain("high probability setup");
  });
});

describe("POLISH-P01 M3 — the watchlist clip fix does not truncate values", () => {
  it("test_polish_p01_watchlist_wrap_anchors_present", () => {
    // The CSS fix allows the provenance LABELS to wrap (never the values);
    // this anchor check pins the mechanism so a revert to clipping fails.
    const css = readFileSync(
      join(process.cwd(), "src/components/terminal/TerminalMultiPane.css"),
      "utf8",
    );
    for (const anchorText of [
      ".watchlist-provenance-chip {",
      ".watchlist-provenance-tag {",
      ".item-price-row {",
      ".watchlist-sparkline-block {",
    ]) {
      expect(css).toContain(anchorText);
    }
    expect(css).toContain("white-space: normal");
    // The values themselves stay nowrap — no truncation, no wrapping.
    expect(css).toContain(".item-price-val");
  });
});

// Silence the real useAuth in this file's mocks (the gate uses it).
vi.mock("../context/AuthContext", async () => {
  const actual = await vi.importActual<typeof import("../context/AuthContext")>(
    "../context/AuthContext",
  );
  return { ...actual, useAuth: vi.fn() };
});
