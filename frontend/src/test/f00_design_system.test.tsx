/**
 * BO-F-00 — Design-System Foundation, Six-Theme System & Animated Wave Login
 * Unit + integration evidence (executed by `npm test`).
 *
 * Covers the BO §8 acceptance criteria:
 *  1. Six themes defined as token overrides; token presence test-pinned
 *     (registry ↔ tokens.css hex pinning).
 *  2. Theme switcher works (OverlayProvider cycle + setTheme) and the
 *     per-operator persistence round-trip normalizes the six-theme
 *     vocabulary (the live re-login restore is evidenced by the Level-I
 *     playwright capture probe, not by jsdom).
 *  3. All themes meet WCAG AA; High-Contrast meets AAA — contrast asserted
 *     from the same registry hexes the CSS must implement.
 *  4. Wave login reduced-motion freeze pinned at the CSS level; scene has no
 *     market-data strings pinned at the component level.
 *  5. Favicon link + asset existence; landing <h1> present; router-flag
 *     decision (Option A) pinned at the source level.
 */

import { describe, expect, it, vi } from "vitest";
import { fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import * as fs from "fs";
import {
  DEFAULT_THEME_ID,
  THEME_IDS,
  THEME_META,
  computeContrastRatio,
  nextThemeId,
  normalizeThemeId,
  rgbToHex,
  themeClassName,
} from "../workstation/design/theme";
import {
  toShellPreferenceWrite,
  shellPreferenceFromRecord,
  type ShellLayoutPreference,
} from "../workstation/persistence/shellPreferences";
import { defaultLayoutForWorkspace } from "../workstation/panels/layoutManager";
import type { OperatorWorkspacePreference } from "../api/client";
import { OverlayProvider, useOverlayController } from "../workstation/overlays/OverlayProvider";
import { AuthProvider } from "../context/AuthContext";
import { LoginPage } from "../pages/LoginPage";
import { TradingTerminalWorkspace } from "../components/terminal/TradingTerminalWorkspace";
import * as client from "../api/client";

// Mock API Client (hoisted to module top-level — vitest requires top-level vi.mock).
vi.mock("../api/client", async () => {
  const actual = await vi.importActual<typeof client>("../api/client");
  return {
    ...actual,
    fetchAdvisorySignals: vi.fn().mockResolvedValue([]),
    fetchSignalValidationReports: vi.fn().mockResolvedValue([]),
    fetchCorrelationReports: vi.fn().mockResolvedValue([]),
    fetchRegimeReports: vi.fn().mockResolvedValue([]),
    fetchCandles: vi
      .fn()
      .mockResolvedValue({ kind: "unavailable", timeframe: "M1", detail: "test", bars: [] }),
    fetchChartResearchAnnotations: vi.fn().mockResolvedValue([]),
    createChartResearchAnnotation: vi.fn(),
    seedChartHistory: vi.fn().mockResolvedValue({ status: "ok", seeded: { EURUSD: 80 } }),
    fetchTradePlans: vi.fn().mockResolvedValue([]),
    fetchJournalEntries: vi.fn().mockResolvedValue([]),
    fetchPortfolioRiskReports: vi.fn().mockResolvedValue([]),
    fetchScenarioReports: vi.fn().mockResolvedValue([]),
    fetchMonitoringAlerts: vi.fn().mockResolvedValue([]),
    fetchInstitutionalIntelligenceBundle: vi.fn().mockResolvedValue(null),
  };
});

// Mock PriceChart in tests to avoid JSDOM Canvas2D null measureText.
vi.mock("../components/chart/PriceChart", () => ({
  PriceChart: ({ bars }: { bars: unknown[] }) => (
    <div data-testid="mock-price-chart">Mock Canvas ({bars?.length ?? 0} bars)</div>
  ),
}));

const FRONTEND_ROOT = process.cwd();

function readWorkspaceFile(relativePath: string): string {
  return fs.readFileSync(`${FRONTEND_ROOT}/${relativePath}`, "utf8");
}

const tokensCss = () => readWorkspaceFile("src/workstation/design/tokens.css");
const loginCss = () => readWorkspaceFile("src/pages/LoginPage.css");
const indexHtml = () => readWorkspaceFile("index.html");
const mainTsx = () => readWorkspaceFile("src/main.tsx");

describe("BO-F-00.1 — six-theme registry (theme.ts)", () => {
  it("defines exactly the six approved themes with the approved default", () => {
    expect(THEME_IDS).toEqual([
      "midnight",
      "light",
      "slate",
      "teal",
      "amber",
      "high-contrast",
    ]);
    expect(DEFAULT_THEME_ID).toBe("midnight");
    for (const id of THEME_IDS) {
      expect(THEME_META[id].id).toBe(id);
      expect(THEME_META[id].className).toBe(`theme-${id}`);
      expect(THEME_META[id].label.length).toBeGreaterThan(0);
      expect(THEME_META[id].description.length).toBeGreaterThan(0);
    }
  });

  it("normalizes legacy and unknown theme values to the six-theme vocabulary", () => {
    // Pre-F-00 records persisted "dark"/"light".
    expect(normalizeThemeId("dark")).toBe("midnight");
    expect(normalizeThemeId("light")).toBe("light");
    expect(normalizeThemeId("slate")).toBe("slate");
    expect(normalizeThemeId("teal")).toBe("teal");
    expect(normalizeThemeId("amber")).toBe("amber");
    expect(normalizeThemeId("high-contrast")).toBe("high-contrast");
    expect(normalizeThemeId("bogus")).toBe("midnight");
    expect(normalizeThemeId(undefined)).toBe("midnight");
    expect(normalizeThemeId(42)).toBe("midnight");
  });

  it("cycles through all six themes in the fixed order and returns to the start", () => {
    let current = DEFAULT_THEME_ID;
    const visited: string[] = [];
    for (let i = 0; i < THEME_IDS.length; i++) {
      visited.push(current);
      current = nextThemeId(current);
    }
    expect(visited).toEqual([...THEME_IDS]);
    expect(current).toBe(DEFAULT_THEME_ID);
    expect(themeClassName("slate")).toBe("theme-slate");
  });
});

describe("BO-F-00.1 — token presence pinned per theme (tokens.css ↔ registry)", () => {
  it("each theme override block exists and implements the registry hexes", () => {
    const css = tokensCss();
    for (const id of THEME_IDS) {
      const meta = THEME_META[id];
      if (id === "midnight") {
        // Midnight is the :root default — no override block; the root token
        // values must equal the registry values.
        const rootBlock = css.slice(css.indexOf(":root {"), css.indexOf("}"));
        expect(rootBlock).toContain(rgbToHex(meta.bgRoot).toLowerCase());
        expect(rootBlock).toContain(rgbToHex(meta.bgSurface).toLowerCase());
        expect(rootBlock).toContain(rgbToHex(meta.textPrimary).toLowerCase());
        continue;
      }
      const selector = `.ix-shell.theme-${id}`;
      expect(css).toContain(selector);
      const blockStart = css.indexOf(selector);
      const blockEnd = css.indexOf("}", css.indexOf("--ix-color-accent", blockStart) + 1);
      const block = css.slice(blockStart, blockEnd);
      for (const hex of [
        rgbToHex(meta.bgRoot),
        rgbToHex(meta.bgSurface),
        rgbToHex(meta.textPrimary),
        rgbToHex(meta.textSecondary),
        rgbToHex(meta.textMuted),
      ]) {
        expect(block, `${selector} must contain ${hex}`).toContain(hex.toLowerCase());
      }
      if (meta.accent) {
        expect(block, `${selector} must set the accent override`).toContain(
          rgbToHex(meta.accent).toLowerCase(),
        );
      }
      if (meta.focus) {
        expect(block, `${selector} must set the focus override`).toContain(
          rgbToHex(meta.focus).toLowerCase(),
        );
      }
    }
  });

  it("the six-theme set is fixed and enumerated — no dynamic theme injection", () => {
    // The registry is a closed Record keyed by the enumerated ids; nothing
    // in the theme system accepts arbitrary styling.
    expect(Object.keys(THEME_META)).toHaveLength(6);
    expect(Object.keys(THEME_META).sort()).toEqual([...THEME_IDS].sort());
  });
});

describe("BO-F-00.1 — WCAG contrast per theme (AA; High-Contrast AAA)", () => {
  const AA_TEXT = 4.5;
  const AAA_TEXT = 7.0;
  const AA_UI = 3.0;
  const defaultAccentHex = "#3b82f6";
  const defaultFocusHex = "#8cc2ff";

  it.each([...THEME_IDS])("%s: text pairs meet WCAG AA on their surfaces", (id) => {
    const meta = THEME_META[id];
    expect(
      computeContrastRatio(rgbToHex(meta.textPrimary), rgbToHex(meta.bgRoot)),
    ).toBeGreaterThanOrEqual(id === "high-contrast" ? AAA_TEXT : AA_TEXT);
    expect(
      computeContrastRatio(rgbToHex(meta.textSecondary), rgbToHex(meta.bgSurface)),
    ).toBeGreaterThanOrEqual(id === "high-contrast" ? AAA_TEXT : AA_TEXT);
    expect(
      computeContrastRatio(rgbToHex(meta.textMuted), rgbToHex(meta.bgSurface)),
    ).toBeGreaterThanOrEqual(AA_TEXT);
    const accent = meta.accent ? rgbToHex(meta.accent) : defaultAccentHex;
    const focus = meta.focus ? rgbToHex(meta.focus) : defaultFocusHex;
    expect(computeContrastRatio(accent, rgbToHex(meta.bgRoot))).toBeGreaterThanOrEqual(AA_UI);
    expect(computeContrastRatio(focus, rgbToHex(meta.bgRoot))).toBeGreaterThanOrEqual(AA_UI);
  });

  it("high-contrast meets AAA for every text tier on black", () => {
    const meta = THEME_META["high-contrast"];
    expect(
      computeContrastRatio(rgbToHex(meta.textPrimary), rgbToHex(meta.bgRoot)),
    ).toBeGreaterThanOrEqual(AAA_TEXT);
    expect(
      computeContrastRatio(rgbToHex(meta.textSecondary), rgbToHex(meta.bgRoot)),
    ).toBeGreaterThanOrEqual(AAA_TEXT);
    expect(
      computeContrastRatio(rgbToHex(meta.textMuted), rgbToHex(meta.bgRoot)),
    ).toBeGreaterThanOrEqual(AAA_TEXT);
    expect(
      computeContrastRatio(rgbToHex(meta.focus ?? [255, 255, 0]), rgbToHex(meta.bgRoot)),
    ).toBeGreaterThanOrEqual(AAA_TEXT);
  });
});

describe("BO-F-00.1 — per-operator theme persistence round-trip (workspace-preferences path)", () => {
  const baseState: ShellLayoutPreference = {
    activeWorkspaceId: "monitor.operations",
    lastRoute: "/",
    navigationCollapsed: false,
    panelLayout: defaultLayoutForWorkspace("monitor.operations"),
    themeMode: "midnight",
    updatedAt: "2026-08-21T00:00:00Z",
  };

  function recordFrom(state: ShellLayoutPreference): OperatorWorkspacePreference {
    const write = toShellPreferenceWrite(state);
    return {
      preference_id: "pref-1",
      operator_id: "op-1",
      workspace_key: write.workspace_key ?? "",
      layout_config: write.layout_config ?? {},
      visible_modules: write.visible_modules ?? [],
      theme_config: write.theme_config ?? {},
      metadata: write.metadata ?? {},
      research_status: "research_only",
      audit_correlation_id: "corr-1",
      created_at: "2026-08-21T00:00:00Z",
      updated_at: state.updatedAt,
    };
  }

  it.each([...THEME_IDS])("round-trips themeMode=%s through the write/read boundary", (id) => {
    const restored = shellPreferenceFromRecord(recordFrom({ ...baseState, themeMode: id }));
    expect(restored?.themeMode).toBe(id);
  });

  it("normalizes legacy 'dark' records to midnight (pre-F-00 compatibility)", () => {
    const legacy = recordFrom(baseState);
    legacy.theme_config = { mode: "dark", density: "institutional" };
    expect(shellPreferenceFromRecord(legacy)?.themeMode).toBe("midnight");
  });
});

describe("BO-F-00.1 — OverlayProvider theme switcher", () => {
  function ThemeHarness() {
    const overlay = useOverlayController();
    return (
      <div>
        <span data-testid="current-theme">{overlay.themeMode}</span>
        <button type="button" onClick={overlay.toggleTheme} data-testid="cycle-theme">
          cycle
        </button>
        <button type="button" onClick={() => overlay.setTheme("slate")} data-testid="set-slate">
          slate
        </button>
        <button
          type="button"
          onClick={() => overlay.setTheme("high-contrast")}
          data-testid="set-hc"
        >
          hc
        </button>
      </div>
    );
  }

  function renderHarness() {
    render(
      <OverlayProvider>
        <ThemeHarness />
      </OverlayProvider>,
    );
  }

  it("starts on midnight (the approved default)", () => {
    renderHarness();
    expect(screen.getByTestId("current-theme").textContent).toBe("midnight");
  });

  it("cycles through the full six-theme order and wraps", () => {
    renderHarness();
    const cycle = screen.getByTestId("cycle-theme");
    const seen: string[] = [];
    for (let i = 0; i < 6; i++) {
      seen.push(screen.getByTestId("current-theme").textContent ?? "");
      fireEvent.click(cycle);
    }
    expect(seen).toEqual([...THEME_IDS]);
    expect(screen.getByTestId("current-theme").textContent).toBe("midnight");
  });

  it("setTheme applies a specific theme", () => {
    renderHarness();
    fireEvent.click(screen.getByTestId("set-slate"));
    expect(screen.getByTestId("current-theme").textContent).toBe("slate");
    fireEvent.click(screen.getByTestId("set-hc"));
    expect(screen.getByTestId("current-theme").textContent).toBe("high-contrast");
  });
});

describe("BO-F-00.2 — login scene (REF-002 edition)", () => {
  // SUPERSEDED BY CITATION (FE-U01 corrective cycle 3, Operator instruction
  // 2026-09-10: REPLACE the old UI with the REF-002 template build). The
  // BO-F-00.2 "wave" composition (two 8-candle rows, 12 particles) is
  // RETIRED with the old surface; the surviving law is the SUBSTANCE:
  // an aria-hidden, value-free decorative scene with candle silhouettes.
  it("composes the REF-002 scene (aria-hidden, candle chart present)", () => {
    render(
      <MemoryRouter>
        <AuthProvider>
          <LoginPage />
        </AuthProvider>
      </MemoryRouter>,
    );
    const scene = screen.getByTestId("login-decorative-scene");
    expect(scene.getAttribute("aria-hidden")).toBe("true");
    const candles = scene.querySelectorAll(".deco-candle");
    expect(candles.length).toBeGreaterThanOrEqual(8);
    expect(screen.getByTestId("login-glow-pulse")).toBeInTheDocument();
  });

  it("the decorative scene carries zero market-data strings or values", () => {
    render(
      <MemoryRouter>
        <AuthProvider>
          <LoginPage />
        </AuthProvider>
      </MemoryRouter>,
    );
    const scene = screen.getByTestId("login-decorative-scene");
    // Decorative only: the scene subtree must contain no text at all, and
    // therefore no prices, symbols, axes, or timestamps.
    expect(scene.textContent?.trim()).toBe("");
    expect(scene.querySelectorAll("[data-price]")).toHaveLength(0);
    expect(scene.querySelectorAll("[data-timestamp]")).toHaveLength(0);
    // Governance framing remains on the login surface — SUPERSEDED BY
    // CITATION (BO-FE-U01 §2.1/§2.2, adopted 2026-09-10): hardcoded
    // pre-auth claims are excluded (AAE-006); the door now renders the
    // truthful pattern-(b) posture label instead.
    expect(screen.getByTestId("login-posture-unverified").textContent).toContain(
      "POSTURE: VERIFIED AFTER SIGN-IN",
    );
  });

  it("reduced-motion: the CSS freezes every animated scene layer and never re-enables", () => {
    const css = loginCss();
    // SUPERSEDED BY CITATION (cycle 3): selector list re-keyed to the
    // REF-002 scene's animated layers; the LAW is unchanged — first
    // freeze block covers every animated layer, nothing re-enables.
    const firstReduce = css.indexOf("@media (prefers-reduced-motion: reduce)");
    expect(firstReduce).toBeGreaterThan(-1);
    const blockEnd = css.indexOf("}", css.indexOf("animation: none !important", firstReduce)) + 1;
    const reduceBlock = css.slice(firstReduce, blockEnd);
    for (const selector of [
      ".scene-bokeh",
      ".deco-candle",
      ".login-glow-pulse",
    ]) {
      expect(reduceBlock, `freeze block must cover ${selector}`).toContain(selector);
    }
    expect(reduceBlock).toContain("animation: none !important");
    expect(css.lastIndexOf("animation-duration")).toBeLessThan(firstReduce);
  });

  it("scene motion is transform/opacity-only (GPU-composited, no layout churn)", () => {
    const css = loginCss();
    // SUPERSEDED BY CITATION (cycle 3): keyframe names re-keyed to the
    // REF-002 motion system; the LAW is unchanged.
    for (const keyframes of ["bokeh-breathe", "candle-flicker", "glow-pulse"]) {
      expect(css).toContain(`@keyframes ${keyframes}`);
    }
    const start = css.indexOf("@keyframes bokeh-breathe");
    const end = css.indexOf("/* ---- hero foreground content ---- */");
    const block = css.slice(start, end);
    for (const forbidden of ["width:", "height:", "margin", "padding", "top:", "left:", "font"]) {
      expect(block, `scene motion must not animate ${forbidden.trim()}`).not.toContain(forbidden);
    }
  });
});

describe("BO-F-00.3 — hygiene items", () => {
  it("favicon: index.html links the shipped brand asset and the asset exists", () => {
    const html = indexHtml();
    expect(html).toContain('rel="icon"');
    expect(html).toContain('href="/branding/axiom-logo.png"');
    expect(fs.existsSync(`${FRONTEND_ROOT}/public/branding/axiom-logo.png`)).toBe(true);
  });

  it("router flags: Option A is pinned (v7_startTransition + v7_relativeSplatPath)", () => {
    const src = mainTsx();
    expect(src).toContain("v7_startTransition: true");
    expect(src).toContain("v7_relativeSplatPath: true");
  });

  it("landing surface carries an <h1> (OBS-CAPASSESS-H1 discharge)", async () => {
    render(
      <MemoryRouter initialEntries={["/"]}>
        <AuthProvider>
          <TradingTerminalWorkspace enableLiveMarket={false} />
        </AuthProvider>
      </MemoryRouter>,
    );
    const heading = await screen.findByTestId("operations-landing-h1");
    expect(heading.tagName).toBe("H1");
    expect(heading.textContent).toContain("AXIOM Institutional Trading Terminal");
  });
});
