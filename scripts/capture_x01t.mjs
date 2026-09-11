/**
 * BO-X-01-TERMINAL — Level-I verification capture (DA evidence tooling, untracked).
 *
 * The ten-hop governed operator workflow through the RUNNING terminal, in a
 * real browser against the real dev stack, over real data. Each hop asserts
 * DOM state and captures a screenshot; the log is the Level-I record.
 *
 * Log:   docs/evidence/x01t/x01t_capture_log.txt
 * Shots: docs/evidence/x01t/x01t_hopNN_*.png (+ corrected f06_dock.png)
 */

import { createRequire } from "module";
import { createHash } from "crypto";
import * as fs from "fs";

const require = createRequire("/home/user/axiom/frontend/package.json");
const { chromium } = require("playwright");

const BASE = "http://127.0.0.1:5173";
const OUT = "/home/user/axiom/docs/evidence/x01t";
fs.mkdirSync(OUT, { recursive: true });

const LINES = [];
const out = (line) => {
  console.log(line);
  LINES.push(line);
  fs.appendFileSync(`${OUT}/x01t_capture_log.txt`, line + "\n");
};
const sha = (buf) => createHash("sha256").update(buf).digest("hex");
// domClick: programmatic DOM activation (equivalent to keyboard activation)
// — the sticky global header can intercept pointer events on scrolled
// elements in the headless viewport; this helper is disclosed in the report.
const domClick = async (page, selector) => {
  const locator = page.locator(selector).first();
  await locator.waitFor({ state: "attached", timeout: 25000 });
  await locator.evaluate((el) => el.click());
};
const shot = async (page, name) => {
  const buf = await page.screenshot();
  fs.writeFileSync(`${OUT}/${name}`, buf);
  out(`  [shot] ${name} (sha256 ${sha(buf).slice(0, 16)}…)`);
};

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
page.setDefaultTimeout(30000);

out(`=== BO-X-01-TERMINAL CAPTURE (${new Date().toISOString()}) ===`);
out(`target: ${BASE} (vite dev, backend proxy 127.0.0.1:8000)`);
out(`stack: AXIOM v0.62.0 dev backend + chain-37 frontend (F-00 → F-06)`);

/* ---------------- HOP 1 — LOGIN (wave, reduced-motion, governance chips) -- */
out("HOP 1/10 — LOGIN");
await page.goto(`${BASE}/login`);
await page.waitForSelector('[data-testid="login-page-container"]');
const loginState = await page.evaluate(() => ({
  chips: document.querySelector('[data-testid="login-governance-chips"]')?.textContent,
  candles: document.querySelectorAll(".deco-candle.wave-candle").length,
  particles: document.querySelectorAll(".login-particle").length,
  glow: Boolean(document.querySelector('[data-testid="login-glow-pulse"]')),
  sceneText: document.querySelector('[data-testid="login-decorative-scene"]')?.textContent?.trim(),
}));
out(`  governance chips: ${JSON.stringify(loginState.chips)}`);
out(`  wave composition: candles=${loginState.candles} particles=${loginState.particles} glow=${loginState.glow} sceneText="${loginState.sceneText}"`);
const motion1 = await page.screenshot();
await page.waitForTimeout(700);
const motion2 = await page.screenshot();
out(`  motion frames differ: ${sha(motion1) !== sha(motion2)}`);
await page.emulateMedia({ reducedMotion: "reduce" });
await page.waitForTimeout(400);
const frozen1 = await page.screenshot();
await page.waitForTimeout(700);
const frozen2 = await page.screenshot();
out(`  reduced-motion frames identical: ${sha(frozen1) === sha(frozen2)}`);
await page.emulateMedia({ reducedMotion: null });
fs.writeFileSync(`${OUT}/x01t_hop01_frozen.png`, frozen1);
await shot(page, "x01t_hop01_login.png");
await page.getByTestId("login-username-input").fill("admin");
await page.getByTestId("login-password-input").fill("AxiomSecurePass2026!");
await page.getByTestId("login-submit-btn").click();
await page.waitForSelector('[data-testid="trading-terminal-workspace"]', { timeout: 20000 });
out("  auth succeeded — terminal mounted");

/* ---------------- HOP 2 — NAVIGATION LEGIBILITY + THEME PERSISTENCE -------- */
out("HOP 2/10 — NAVIGATION LEGIBILITY + THEME PERSISTENCE");
await page.waitForSelector('[data-testid="unified-module-rail"]');
const railState = await page.evaluate(() => {
  const buttons = [...document.querySelectorAll(".rail-button")];
  return {
    buttons: buttons.length,
    svgIcons: buttons.filter((b) => b.querySelector("svg.workspace-icon")).length,
    visibleLabels: [...document.querySelectorAll(".rail-label")].map((l) => l.textContent?.trim()),
    ariaLabeled: buttons.filter((b) => b.getAttribute("aria-label")).length,
  };
});
out(`  rail: buttons=${railState.buttons} svgIcons=${railState.svgIcons} ariaLabeled=${railState.ariaLabeled}`);
out(`  rail labels: ${JSON.stringify(railState.visibleLabels)}`);
const toggle = page.getByTestId("shell-theme-toggle-btn");
const themeBefore = await toggle.getAttribute("data-theme-id");
for (let i = 0; i < 6; i++) { await toggle.click(); await page.waitForTimeout(120); }
const themeAfter = await toggle.getAttribute("data-theme-id");
out(`  theme switch: ${themeBefore} -> ${themeAfter}`);
await page.reload();
await page.waitForSelector('[data-testid="trading-terminal-workspace"]', { timeout: 20000 });
await page.waitForTimeout(2000);
const themeAfterReload = await page.getByTestId("shell-theme-toggle-btn").getAttribute("data-theme-id");
out(`  theme persists across reload: ${themeAfterReload} (restored=${themeAfterReload === themeAfter})`);
await shot(page, "x01t_hop02_nav.png");
// cycle back to midnight
for (let i = 0; i < 6 && (await page.getByTestId("shell-theme-toggle-btn").getAttribute("data-theme-id")) !== "midnight"; i++) {
  await page.getByTestId("shell-theme-toggle-btn").click();
  await page.waitForTimeout(120);
}
// CORRECTED dock capture for OBS-F06-1 (navigation expanded)
await domClick(page, ".ix-nav-toggle");
await page.waitForTimeout(400);
await page.waitForSelector(".ix-nav-link", { timeout: 10000 });
const dockState = await page.evaluate(() => ({
  links: [...document.querySelectorAll(".ix-nav-link")].slice(0, 5).map((l) => ({
    icon: Boolean(l.querySelector("svg.workspace-icon")),
    label: l.querySelector(".ix-nav-copy span")?.textContent,
  })),
}));
out(`  dock (expanded): ${JSON.stringify(dockState)}`);
fs.writeFileSync(`${OUT}/f06_dock.png`, await page.screenshot());
out(`  [shot] f06_dock.png CORRECTED (dock expanded, sha256 ${sha(fs.readFileSync(`${OUT}/f06_dock.png`)).slice(0, 16)}…)`);
await domClick(page, ".ix-nav-toggle");
await page.waitForTimeout(300);

/* ---------------- HOP 3 — INSTRUMENT -> WATCHLIST -> CHART ------------------ */
out("HOP 3/10 — INSTRUMENT SELECTION -> WATCHLIST -> CHART");
await page.waitForSelector('[data-testid="watchlist-row-btc-usd"]', { timeout: 20000 });
await domClick(page, '[data-testid="watchlist-row-btc-usd"]');
await page.waitForFunction(
  () => document.querySelector('[data-testid="chart-symbol-badge"]')?.textContent?.includes("BTC/USD"),
  undefined,
  { timeout: 25000 },
);
const chartState = await page.evaluate(() => ({
  symbol: document.querySelector('[data-testid="chart-symbol-badge"]')?.textContent,
  stage: Boolean(document.querySelector('[data-testid="terminal-chart-stage"]')),
  posture: document.querySelector('[data-testid="ticker-posture-badge"]')?.textContent,
  overlayButtons: [...document.querySelectorAll('[data-testid^="overlay-"]')].slice(0, 4).map((b) => b.getAttribute("data-testid")),
}));
out(`  chart: ${JSON.stringify(chartState)}`);
await shot(page, "x01t_hop03_chart.png");

/* ---------------- HOP 4 — STRUCTURAL SIGNALS ------------------------------- */
out("HOP 4/10 — STRUCTURAL SIGNALS (real derived events)");
await domClick(page, '[data-testid="right-dock-tab-signals"]');
await page.waitForSelector('[data-testid="terminal-signal-stream"]', { timeout: 20000 });
await domClick(page, '[data-testid="signal-family-structural"]');
await page.waitForSelector('[data-testid="structural-signal-stream"]', { timeout: 20000 });
await page.waitForFunction(
  () => {
    const badge = document.querySelector('[data-testid="structural-count-badge"]');
    return badge && /[1-9]\d* EVENTS/.test(badge.textContent ?? "");
  },
  undefined,
  { timeout: 25000 },
);
const structuralState = await page.evaluate(() => ({
  count: document.querySelector('[data-testid="structural-count-badge"]')?.textContent,
  framing: document.querySelector('[data-testid="structural-descriptive-framing"]')?.textContent,
  provenance: document.querySelector('[data-testid="structural-provenance-line"]')?.textContent,
  firstEvent: document.querySelector('[data-testid^="structural-label-"]')?.textContent,
}));
out(`  structural: ${JSON.stringify(structuralState)}`);
await shot(page, "x01t_hop04_structural.png");

/* ---------------- HOP 5 — PREDICTIVE SIGNALS (deferred) -------------------- */
out("HOP 5/10 — PREDICTIVE SIGNALS (honest deferred-empty)");
await domClick(page, '[data-testid="signal-family-predictive"]');
await page.waitForSelector('[data-testid="signal-deferred-empty-state"]', { timeout: 20000 });
const predictiveState = await page.evaluate(() => ({
  label: document.querySelector('[data-testid="predictive-family-label"]')?.textContent,
  deferred: document.querySelector('[data-testid="signal-deferred-empty-state"]')?.textContent?.slice(0, 120),
}));
out(`  predictive: ${JSON.stringify(predictiveState)}`);
await shot(page, "x01t_hop05_predictive.png");

/* ---------------- HOP 6 — INTELLIGENCE (generate + read five families) ----- */
out("HOP 6/10 — INTELLIGENCE (five families, generate + read)");
await domClick(page, '[data-testid="right-dock-tab-intelligence"]');
await page.waitForSelector('[data-testid="terminal-intelligence-cards"]', { timeout: 20000 });
await page.waitForFunction(
  () => !document.querySelector('[data-testid="gen-btn-scenario"]')?.disabled,
  undefined,
  { timeout: 25000 },
);
const genSurface = await page.evaluate(() => ({
  framing: document.querySelector('[data-testid="generation-framing"]')?.textContent,
  window: document.querySelector('[data-testid="generation-window-note"]')?.textContent?.slice(0, 80),
}));
out(`  generation: ${JSON.stringify(genSurface)}`);
const families = ["scenario", "portfolio-risk", "correlation", "regime"];
for (const family of families) {
  await page.getByTestId(`gen-btn-${family}`).click();
  await page.waitForSelector(`[data-testid="gen-status-${family}"]`, { timeout: 25000 });
  const status = await page.getByTestId(`gen-status-${family}`).textContent();
  out(`  ${family}: ${status}`);
}
// honest insufficient-data on signal-validation
await page.getByTestId("gen-btn-signal-validation").click();
await page.waitForSelector('[data-testid="gen-insufficient-signal-validation"]', { timeout: 25000 });
out(`  signal-validation: ${await page.getByTestId("gen-insufficient-signal-validation").textContent()}`);
// read back one family card with data-class + lineage fields
await domClick(page, '[data-testid="intel-tab-scenario"]');
await page.waitForSelector('[data-testid="scenario-name"]', { timeout: 20000 });
const scenarioCard = await page.evaluate(() => ({
  name: document.querySelector('[data-testid="scenario-name"]')?.textContent,
  ret: document.querySelector('[data-testid="scenario-return"]')?.textContent,
  dataClass: document.querySelector('[data-testid="scenario-data-class"]')?.textContent,
  framing: document.querySelector('[data-testid="scenario-framing"]')?.textContent,
}));
out(`  scenario card: ${JSON.stringify(scenarioCard)}`);
await shot(page, "x01t_hop06_intelligence.png");

/* ---------------- HOP 7 — ALERTS ------------------------------------------- */
out("HOP 7/10 — ALERTS (domain filter + timestamp + lineage + ack)");
await domClick(page, '[data-testid="right-dock-tab-alerts"]');
await page.waitForSelector('[data-testid="monitoring-alerts-panel"]', { timeout: 20000 });
await page.waitForFunction(
  () => document.querySelectorAll('[data-testid^="alert-item-"]').length >= 3,
  undefined,
  { timeout: 25000 },
);
const alertsAll = await page.evaluate(() => ({
  count: document.querySelector('[data-testid="alerts-domain-count"]')?.textContent,
  domains: [...document.querySelectorAll('[data-testid^="alert-domain-"]')].map((el) => el.getAttribute("data-domain")),
  created: document.querySelector('[data-testid^="alert-created-"]')?.textContent,
  lineage: document.querySelector('[data-testid^="alert-lineage-"]')?.textContent,
  audit: document.querySelector('[data-testid^="alert-audit-"]')?.textContent,
}));
out(`  alerts all: ${JSON.stringify(alertsAll)}`);
await domClick(page, '[data-testid="alerts-domain-market"]');
await page.waitForFunction(
  () => document.querySelectorAll('[data-testid^="alert-item-"]').length === 1,
  undefined,
  { timeout: 25000 },
);
out(`  market filter: ${await page.getByTestId("alerts-domain-count").textContent()}`);
await domClick(page, '[data-testid="alerts-domain-all"]');
await page.waitForFunction(
  () => document.querySelectorAll('[data-testid^="alert-item-"]').length >= 3,
  undefined,
  { timeout: 25000 },
);
const ackBefore = await page.evaluate(() => document.querySelectorAll('[data-testid^="alert-ack-"]').length);
await page.locator('[data-testid^="alert-ack-"]').first().click();
await page.waitForFunction(
  (before) => document.querySelectorAll('[data-testid^="alert-ack-"]').length === before - 1,
  ackBefore,
  { timeout: 25000 },
);
out(`  ack: buttons ${ackBefore} -> ${ackBefore - 1} (read-state-only, API-confirmed)`);
await shot(page, "x01t_hop07_alerts.png");

/* ---------------- HOP 8 — LINEAGE / EVIDENCE ------------------------------- */
out("HOP 8/10 — LINEAGE / EVIDENCE (persisted-only)");
await domClick(page, '[data-testid="right-dock-tab-intelligence"]');
await page.waitForSelector('[data-testid="terminal-intelligence-cards"]', { timeout: 20000 });
await domClick(page, '[data-testid="intel-tab-correlation"]');
await page.waitForSelector('[data-testid^="lineage-toggle-"]', { timeout: 25000 });
await page.locator('[data-testid^="lineage-toggle-"]').first().click();
await page.waitForSelector('[data-testid="lineage-evidence-panel"]', { timeout: 25000 });
const lineageState = await page.evaluate(() => ({
  hash: document.querySelector('[data-testid="lineage-report-hash"]')?.textContent,
  audit: document.querySelector('[data-testid="lineage-audit-correlation"]')?.textContent,
  capNote: document.querySelector('[data-testid="lineage-source-cap-note"]')?.textContent?.slice(0, 80),
  fabricatedChainAbsent:
    !document.body.textContent.includes("Market Data Series") &&
    !document.body.textContent.includes("Grounded Model Registry"),
  panelControls: document.querySelectorAll('[data-testid="lineage-evidence-panel"] button, [data-testid="lineage-evidence-panel"] input').length,
}));
out(`  lineage: ${JSON.stringify(lineageState)}`);
await shot(page, "x01t_hop08_lineage.png");

/* ---------------- HOP 9 — ASSISTANT ---------------------------------------- */
out("HOP 9/10 — ASSISTANT (grounded ask + refusal + GROUNDING_REQUIRED)");
await page.goto(`${BASE}/intelligence`);
await page.waitForSelector('[data-testid="assistant-ask-composer"]', { timeout: 25000 });
const composer = page.getByTestId("assistant-ask-composer");
await composer.scrollIntoViewIfNeeded();
await domClick(page, '[data-testid="grounding-toggle-btn"]');
await page.waitForSelector('[data-testid="grounding-picker"]', { timeout: 20000 });
await page.waitForFunction(
  () => document.querySelectorAll('[data-testid^="grounding-checkbox-"]').length >= 1,
  undefined,
  { timeout: 20000 },
);
const candidates = await page.evaluate(() => ({
  families: [...document.querySelectorAll(".ix-grounding-family")].map((el) => el.textContent),
}));
out(`  grounding candidates: ${JSON.stringify(candidates)}`);
await page.locator('[data-testid^="grounding-checkbox-"]').first().check();
await page.getByTestId("ask-question-input").fill(
  "Summarize the BTCUSD vs ETHUSD correlation and state the research caveats.",
);
await page.getByTestId("ask-submit-btn").click();
await page.waitForSelector('[data-testid="ask-result-grounded"]', { timeout: 25000 });
const groundedAsk = await page.evaluate(() => ({
  summary: document.querySelector('[data-testid="ask-grounding-summary"]')?.textContent,
  correlation: document.querySelector('[data-testid="ask-audit-correlation"]')?.textContent,
}));
out(`  grounded ask: ${JSON.stringify(groundedAsk)}`);
await shot(page, "x01t_hop09_assistant.png");
await page.getByTestId("ask-question-input").fill("Please place a buy order for 10 BTCUSDT.");
await page.getByTestId("ask-submit-btn").click();
await page.waitForSelector('[data-testid="ask-result-refused"]', { timeout: 25000 });
out(`  refusal: ${await page.getByTestId("ask-refusal-class").textContent()}`);
// Empty-grounding case from a CLEAN panel state: reload the page so the
// composer mounts with NO selection (a fresh session's honest empty case),
// then ask without selecting any grounding artifact.
await page.reload();
await page.waitForSelector('[data-testid="assistant-ask-composer"]', { timeout: 25000 });
await page.getByTestId("ask-question-input").fill("Market outlook?");
await page.getByTestId("ask-submit-btn").click();
await page.waitForFunction(
  () => document.querySelector('[data-testid="ask-refusal-class"]')?.textContent?.includes("GROUNDING_REQUIRED"),
  undefined,
  { timeout: 25000 },
);
out("  empty-grounding: GROUNDING_REQUIRED (honest)");

/* ---------------- HOP 10 — GOVERNANCE & NON-ACTUATION ---------------------- */
out("HOP 10/10 — GOVERNANCE & NON-ACTUATION (end-to-end)");
await page.goto(`${BASE}/`);
await page.waitForSelector('[data-testid="trading-terminal-workspace"]', { timeout: 25000 });
const govScan = await page.evaluate(() => {
  const controls = [...document.querySelectorAll("button, a, input, select")]
    .map((el) => (el.textContent ?? "") + " " + (el.getAttribute("aria-label") ?? ""))
    .join(" ")
    .toLowerCase();
  const forbidden = ["place order", "buy ", "sell ", "broker", "execution", "account"];
  return {
    violations: forbidden.filter((f) => controls.includes(f)),
    postureBadge: document.querySelector('[data-testid="ticker-posture-badge"]')?.textContent,
    shellPresent: Boolean(document.querySelector('[data-testid="institutional-workspace-shell"]')),
  };
});
out(`  non-actuation scan: ${JSON.stringify(govScan)}`);
await shot(page, "x01t_hop10_governance.png");

// audit cross-reference (backend read)
const audit = await page.evaluate(async () => {
  const token = localStorage.getItem("accessToken") ?? sessionStorage.getItem("accessToken");
  const resp = await fetch("/api/v1/persistence/audit-events?limit=5", {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  });
  return resp.ok ? await resp.json() : null;
});
out(`  audit read via UI origin: ${audit ? `${audit.length} recent events (categories: ${[...new Set(audit.map((e) => e.category))].join(", ")})` : "unavailable"}`);

await browser.close();
fs.writeFileSync(`${OUT}/x01t_capture_log.txt`, LINES.join("\n") + "\n");
out(`evidence written to ${OUT}`);
